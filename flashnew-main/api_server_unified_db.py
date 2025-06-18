#!/usr/bin/env python3
"""
FLASH API Server - Database Integrated Version
Full database integration with PostgreSQL/SQLite support
"""

import os
import sys
import logging
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
from contextlib import asynccontextmanager

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, Security, status, Request, Response, Depends, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import database components
from database.connection import init_database, get_db, check_connection, get_stats
from database.models import User, Prediction, StartupProfile, APIKey, AuditLog
from database.repositories import (
    PredictionRepository, StartupProfileRepository, 
    APIKeyRepository, AuditLogRepository
)

# Import models and utilities
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES
from frontend_models import FrontendStartupData
from config import settings
from utils.sanitization import sanitize_startup_data, sanitize_string
from utils.error_handling import (
    error_handler, handle_prediction_errors, DataValidationError,
    ModelError, validate_numeric_value, CircuitBreaker
)
from utils.data_validation import data_validator
from utils.redis_cache import redis_cache
from utils.background_tasks import task_manager, async_batch_predict, async_generate_report
from monitoring.metrics_collector import (
    metrics_collector, record_prometheus_request, record_prometheus_prediction,
    record_prometheus_error, update_prometheus_system_metrics, get_prometheus_metrics,
    PROMETHEUS_ENABLED
)

# Import enhanced analysis endpoint
try:
    from api_analysis_enhanced import analyze_enhanced
    ENHANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ENHANCED_ANALYSIS_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server_db.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize components
type_converter = None
orchestrator = None
prediction_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global type_converter, orchestrator
    
    # Startup
    logger.info("Starting FLASH API Server with Database Integration...")
    
    # Initialize database
    try:
        init_database()
        if check_connection():
            logger.info("✅ Database connection established")
        else:
            logger.error("❌ Database connection failed")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        # Continue without database in development
        if not settings.is_development():
            raise
    
    # Initialize components
    type_converter = TypeConverter()
    orchestrator = UnifiedOrchestratorV3()
    
    # Start background metrics collection
    if PROMETHEUS_ENABLED:
        import threading
        def update_metrics():
            while True:
                update_prometheus_system_metrics()
                time.sleep(60)
        metrics_thread = threading.Thread(target=update_metrics, daemon=True)
        metrics_thread.start()
    
    logger.info("✅ FLASH API Server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FLASH API Server...")
    redis_cache.close()

# Initialize FastAPI app
app = FastAPI(
    title="FLASH API with Database", 
    version="2.0.0",
    description="FLASH Platform API with Full Database Integration",
    lifespan=lifespan
)

# Add global exception handlers
app.add_exception_handler(Exception, error_handler)
app.add_exception_handler(ValidationError, error_handler)
app.add_exception_handler(DataValidationError, error_handler)
app.add_exception_handler(ModelError, error_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class StartupData(BaseModel):
    """Frontend startup data model with validation"""
    # Company basics
    startup_name: Optional[str] = Field(None, description="Company name")
    funding_stage: Optional[str] = Field(None, description="Current funding stage")
    sector: Optional[str] = Field(None, description="Industry sector")
    
    # Financial metrics
    total_capital_raised_usd: Optional[float] = Field(None, ge=0, description="Total capital raised")
    annual_revenue_run_rate: Optional[float] = Field(None, ge=0, description="Annual revenue run rate")
    revenue_growth_rate_percent: Optional[float] = Field(None, description="Revenue growth rate")
    burn_multiple: Optional[float] = Field(None, description="Burn multiple")
    gross_margin_percent: Optional[float] = Field(None, ge=0, le=100, description="Gross margin")
    
    # Team metrics
    team_size_full_time: Optional[int] = Field(None, ge=0, description="Full time team size")
    technical_team_percent: Optional[float] = Field(None, ge=0, le=100, description="Technical team percentage")
    
    # Market metrics
    tam_size_usd: Optional[float] = Field(None, ge=0, description="Total addressable market")
    sam_size_usd: Optional[float] = Field(None, ge=0, description="Serviceable addressable market")
    market_growth_rate_percent: Optional[float] = Field(None, description="Market growth rate")
    
    # Product metrics
    monthly_active_users: Optional[int] = Field(None, ge=0, description="Monthly active users")
    user_growth_rate_percent: Optional[float] = Field(None, description="User growth rate")
    nps_score: Optional[int] = Field(None, ge=-100, le=100, description="Net promoter score")
    
    class Config:
        extra = "allow"  # Allow additional fields

# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    # In production, use bcrypt or similar
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password: str) -> str:
    """Hash password"""
    # In production, use bcrypt or similar
    return hashlib.sha256(password.encode()).hexdigest()

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    api_key: Optional[str] = Security(api_key_header),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get current user from JWT or API key"""
    # Check API key first
    if api_key:
        api_key_repo = APIKeyRepository(db)
        key_obj = api_key_repo.validate_key(api_key)
        if key_obj:
            return {
                "user_id": f"api_key_{key_obj.id}",
                "username": key_obj.name,
                "is_api_key": True,
                "api_key_id": str(key_obj.id)
            }
    
    # Check JWT token
    if credentials:
        try:
            payload = jwt.decode(
                credentials.credentials, 
                SECRET_KEY, 
                algorithms=[ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            
            # Get user from database
            user = db.query(User).filter(User.username == username).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            return {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_api_key": False
            }
        except JWTError:
            pass
    
    # No valid authentication
    if settings.DISABLE_AUTH and settings.is_development():
        return {
            "user_id": "dev_user",
            "username": "development",
            "is_api_key": False
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )

# Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "FLASH API",
        "version": "2.0.0",
        "status": "operational",
        "database": "connected" if check_connection() else "disconnected",
        "features": {
            "predictions": True,
            "database_storage": True,
            "user_authentication": True,
            "api_keys": True,
            "audit_logging": True,
            "caching": True,
            "monitoring": PROMETHEUS_ENABLED
        }
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    db_status = "healthy"
    db_stats = {}
    
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_stats = get_stats()
    except Exception as e:
        db_status = "unhealthy"
        logger.error(f"Health check failed: {e}")
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "database_stats": db_stats,
        "models_loaded": orchestrator is not None,
        "cache_connected": redis_cache.is_connected()
    }

@app.post("/auth/register", response_model=Token)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | 
        (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # Log registration
    audit_repo = AuditLogRepository(db)
    audit_repo.log(
        action="user_registration",
        user_id=str(user.id),
        details={"username": user.username, "email": user.email}
    )
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/auth/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user"""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Log login
    audit_repo = AuditLogRepository(db)
    audit_repo.log(
        action="user_login",
        user_id=str(user.id),
        details={"username": user.username}
    )
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/predict")
async def predict(
    request: Request,
    background_tasks: BackgroundTasks,
    data: Annotated[StartupData, Body()],
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Main prediction endpoint with database storage"""
    start_time = time.time()
    
    try:
        # Sanitize and validate input
        data_dict = data.dict()
        sanitized_data = sanitize_startup_data(data_dict)
        
        is_valid, validation_errors, validated_data = data_validator.validate(sanitized_data)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Data validation failed",
                    "validation_errors": validation_errors[:5]
                }
            )
        
        # Check cache
        cache_key_data = {k: v for k, v in validated_data.items() if k != 'startup_name'}
        cached_result = redis_cache.get_prediction(cache_key_data)
        if cached_result:
            logger.info("Cache hit - returning cached prediction")
            # Still log to database for tracking
            background_tasks.add_task(
                log_cached_prediction,
                db, validated_data, cached_result, current_user
            )
            return cached_result
        
        # Convert and predict
        features = type_converter.convert_frontend_to_backend(validated_data)
        canonical_features = {k: features.get(k, None) for k in ALL_FEATURES}
        
        # Fill defaults
        for feature in ALL_FEATURES:
            if canonical_features[feature] is None:
                if feature in ['has_debt', 'network_effects_present', 'has_data_moat']:
                    canonical_features[feature] = False
                elif feature == 'funding_stage':
                    canonical_features[feature] = 'seed'
                elif feature == 'sector':
                    canonical_features[feature] = 'saas'
                else:
                    canonical_features[feature] = 0.0
        
        # Make prediction
        with prediction_circuit_breaker:
            result = orchestrator.predict(canonical_features)
        
        # Prepare response
        response = {
            "success_probability": float(result.get("success_probability", 0)),
            "confidence_score": float(result.get("confidence_score", 0)),
            "verdict": result.get("verdict", "UNKNOWN"),
            "verdict_strength": result.get("verdict_strength", "unknown"),
            "pillar_scores": result.get("pillar_scores", {}),
            "risk_factors": result.get("risk_factors", []),
            "success_factors": result.get("success_factors", []),
            "key_insights": result.get("key_insights", []),
            "confidence_interval": result.get("confidence_interval", {})
        }
        
        # Store in database
        startup_repo = StartupProfileRepository(db)
        prediction_repo = PredictionRepository(db)
        
        # Get or create startup profile
        startup_name = validated_data.get("startup_name", "Unknown")
        startup_profile = startup_repo.get_or_create(
            name=startup_name,
            sector=validated_data.get("sector"),
            funding_stage=validated_data.get("funding_stage"),
            hq_location=validated_data.get("hq_location")
        )
        
        # Create prediction record
        prediction = prediction_repo.create(
            input_features=canonical_features,
            success_probability=response["success_probability"],
            confidence_score=response["confidence_score"],
            verdict=response["verdict"],
            verdict_strength=response["verdict_strength"],
            camp_scores=response["pillar_scores"],
            model_predictions=result.get("model_predictions", {}),
            risk_factors=response["risk_factors"],
            success_factors=response["success_factors"],
            key_insights=response["key_insights"],
            startup_name=startup_name,
            user_id=current_user["user_id"],
            api_key_id=current_user.get("api_key_id"),
            model_version=orchestrator.get_version(),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        # Update startup profile
        startup_repo.update_latest_prediction(startup_profile, prediction)
        
        # Commit to database
        db.commit()
        
        # Cache result
        redis_cache.set_prediction(cache_key_data, response)
        
        # Log success
        audit_repo = AuditLogRepository(db)
        audit_repo.log(
            action="prediction",
            status="success",
            entity_type="prediction",
            entity_id=str(prediction.id),
            user_id=current_user["user_id"],
            details={
                "startup_name": startup_name,
                "verdict": response["verdict"],
                "probability": response["success_probability"]
            },
            duration_ms=int((time.time() - start_time) * 1000)
        )
        db.commit()
        
        # Record metrics
        metrics_collector.record_prediction(
            verdict=response["verdict"],
            confidence=response["confidence_score"],
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        return response
        
    except Exception as e:
        # Log error
        logger.error(f"Prediction error: {str(e)}")
        
        audit_repo = AuditLogRepository(db)
        audit_repo.log(
            action="prediction",
            status="error",
            user_id=current_user["user_id"],
            error_message=str(e),
            duration_ms=int((time.time() - start_time) * 1000)
        )
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

async def log_cached_prediction(
    db: Session,
    input_data: Dict,
    result: Dict,
    current_user: Dict
):
    """Background task to log cached predictions"""
    try:
        audit_repo = AuditLogRepository(db)
        audit_repo.log(
            action="prediction_cached",
            status="success",
            user_id=current_user["user_id"],
            details={
                "startup_name": input_data.get("startup_name"),
                "verdict": result.get("verdict"),
                "cached": True
            }
        )
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log cached prediction: {e}")

@app.get("/predictions/history")
async def get_prediction_history(
    limit: int = 100,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's prediction history"""
    prediction_repo = PredictionRepository(db)
    predictions = prediction_repo.get_user_predictions(
        user_id=current_user["user_id"],
        limit=limit,
        offset=offset
    )
    
    return {
        "predictions": [
            {
                "id": str(p.id),
                "created_at": p.created_at.isoformat(),
                "startup_name": p.startup_name,
                "verdict": p.verdict,
                "success_probability": p.success_probability,
                "confidence_score": p.confidence_score,
                "pillar_scores": {
                    "capital": p.capital_score,
                    "advantage": p.advantage_score,
                    "market": p.market_score,
                    "people": p.people_score
                }
            }
            for p in predictions
        ],
        "total": len(predictions),
        "limit": limit,
        "offset": offset
    }

@app.get("/predictions/{prediction_id}")
async def get_prediction_detail(
    prediction_id: str,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed prediction by ID"""
    prediction_repo = PredictionRepository(db)
    prediction = prediction_repo.get_by_id(prediction_id)
    
    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )
    
    # Check access
    if prediction.user_id != current_user["user_id"] and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    
    return {
        "id": str(prediction.id),
        "created_at": prediction.created_at.isoformat(),
        "startup_name": prediction.startup_name,
        "input_features": prediction.input_features,
        "verdict": prediction.verdict,
        "verdict_strength": prediction.verdict_strength,
        "success_probability": prediction.success_probability,
        "confidence_score": prediction.confidence_score,
        "pillar_scores": {
            "capital": prediction.capital_score,
            "advantage": prediction.advantage_score,
            "market": prediction.market_score,
            "people": prediction.people_score
        },
        "model_predictions": prediction.model_predictions,
        "risk_factors": prediction.risk_factors,
        "success_factors": prediction.success_factors,
        "key_insights": prediction.key_insights,
        "processing_time_ms": prediction.processing_time_ms
    }

@app.get("/startups/search")
async def search_startups(
    query: Optional[str] = None,
    sector: Optional[str] = None,
    funding_stage: Optional[str] = None,
    min_probability: Optional[float] = None,
    limit: int = 100,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search startup profiles"""
    startup_repo = StartupProfileRepository(db)
    startups = startup_repo.search(
        query=query,
        sector=sector,
        funding_stage=funding_stage,
        min_probability=min_probability,
        limit=limit
    )
    
    return {
        "startups": [
            {
                "id": str(s.id),
                "name": s.name,
                "sector": s.sector,
                "funding_stage": s.funding_stage,
                "location": s.hq_location,
                "avg_success_probability": s.avg_success_probability,
                "total_predictions": s.total_predictions,
                "last_prediction_date": s.last_prediction_date.isoformat() if s.last_prediction_date else None
            }
            for s in startups
        ],
        "total": len(startups)
    }

@app.post("/api-keys/create")
async def create_api_key(
    name: str,
    description: Optional[str] = None,
    rate_limit: int = 10,
    expires_days: int = 365,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new API key"""
    if current_user.get("is_api_key"):
        raise HTTPException(
            status_code=403,
            detail="Cannot create API keys with API key authentication"
        )
    
    api_key_repo = APIKeyRepository(db)
    key_obj, raw_key = api_key_repo.create(
        name=name,
        description=description,
        owner_email=current_user.get("email", ""),
        rate_limit_per_minute=rate_limit,
        expires_days=expires_days
    )
    
    # Log creation
    audit_repo = AuditLogRepository(db)
    audit_repo.log(
        action="api_key_created",
        entity_type="api_key",
        entity_id=str(key_obj.id),
        user_id=current_user["user_id"],
        details={"name": name}
    )
    
    db.commit()
    
    return {
        "api_key": raw_key,
        "key_id": str(key_obj.id),
        "name": name,
        "expires_at": key_obj.expires_at.isoformat(),
        "rate_limit": rate_limit,
        "message": "Save this key securely - it won't be shown again"
    }

@app.get("/stats/overview")
async def get_stats_overview(
    days: int = 30,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get platform statistics"""
    prediction_repo = PredictionRepository(db)
    stats = prediction_repo.get_statistics(days=days)
    
    return {
        "period_days": days,
        "statistics": stats,
        "database_stats": get_stats()
    }

@app.get("/metrics")
async def get_metrics(
    current_user: Dict = Depends(get_current_user)
):
    """Get Prometheus metrics"""
    if not PROMETHEUS_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="Metrics not available"
        )
    
    return Response(
        content=get_prometheus_metrics(),
        media_type="text/plain"
    )

# Batch prediction endpoint
@app.post("/predict/batch")
async def predict_batch(
    startups: List[StartupData],
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit batch prediction job"""
    if len(startups) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 startups per batch"
        )
    
    # Create task
    task_id = task_manager.create_task(
        task_type="batch_prediction",
        user_id=current_user["user_id"]
    )
    
    # Submit to background
    background_tasks.add_task(
        process_batch_predictions,
        task_id, startups, current_user, db
    )
    
    return {
        "task_id": task_id,
        "status": "submitted",
        "batch_size": len(startups)
    }

async def process_batch_predictions(
    task_id: str,
    startups: List[StartupData],
    current_user: Dict,
    db: Session
):
    """Process batch predictions in background"""
    try:
        results = []
        for startup in startups:
            # Process each startup
            # (Similar to single prediction logic)
            pass
        
        task_manager.update_task(task_id, "completed", results)
    except Exception as e:
        task_manager.update_task(task_id, "failed", {"error": str(e)})

@app.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get task status"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return task

# Legacy endpoints for compatibility
@app.post("/predict_simple")
async def predict_simple(
    request: Request,
    background_tasks: BackgroundTasks,
    data: StartupData,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Legacy endpoint - redirects to /predict"""
    return await predict(request, background_tasks, data, current_user, db)

@app.post("/predict_enhanced")
async def predict_enhanced_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    data: StartupData,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced prediction with pattern analysis"""
    # Get base prediction
    base_result = await predict(request, background_tasks, data, current_user, db)
    
    # Add enhanced analysis if available
    if ENHANCED_ANALYSIS_AVAILABLE:
        try:
            enhanced = analyze_enhanced(data.dict())
            base_result["enhanced_analysis"] = enhanced
        except Exception as e:
            logger.error(f"Enhanced analysis failed: {e}")
    
    return base_result

if __name__ == "__main__":
    # Run server
    uvicorn.run(
        "api_server_unified_db:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.is_development(),
        log_level="info"
    )