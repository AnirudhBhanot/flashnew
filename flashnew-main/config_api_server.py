"""
Configuration API Server for FLASH Platform
Provides dynamic configuration management for frontend values
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os
import redis
import hashlib
from sqlalchemy import create_engine, Column, String, JSON, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FLASH Configuration API",
    description="Dynamic configuration management for FLASH platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./flash_config.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis setup for caching
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
memory_cache = {}  # Initialize memory cache for fallback
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_available = True
except:
    logger.warning("Redis not available, using in-memory cache")
    redis_client = None
    redis_available = False

# Database Models
class Configuration(Base):
    __tablename__ = "configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(JSON)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True)

class ConfigurationAudit(Base):
    __tablename__ = "configuration_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String, index=True)
    old_value = Column(JSON)
    new_value = Column(JSON)
    changed_by = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(String)

class ABTestConfig(Base):
    __tablename__ = "ab_test_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String, unique=True, index=True)
    config_key = Column(String)
    variants = Column(JSON)  # {"A": value1, "B": value2}
    traffic_split = Column(JSON)  # {"A": 0.5, "B": 0.5}
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cache helpers
def get_cache_key(key: str) -> str:
    return f"config:{key}"

def get_from_cache(key: str) -> Optional[Any]:
    global redis_available
    cache_key = get_cache_key(key)
    if redis_available and redis_client:
        try:
            value = redis_client.get(cache_key)
            if value:
                return json.loads(value)
        except:
            # Redis connection failed, fall back to memory cache
            redis_available = False
            if cache_key in memory_cache:
                return memory_cache[cache_key]
    elif cache_key in memory_cache:
        return memory_cache[cache_key]
    return None

def set_cache(key: str, value: Any, ttl: int = 300):
    global redis_available
    cache_key = get_cache_key(key)
    value_str = json.dumps(value)
    if redis_available and redis_client:
        try:
            redis_client.setex(cache_key, ttl, value_str)
        except:
            # Redis connection failed, fall back to memory cache
            redis_available = False
            memory_cache[cache_key] = value
    else:
        memory_cache[cache_key] = value

def invalidate_cache(key: str):
    global redis_available
    cache_key = get_cache_key(key)
    if redis_available and redis_client:
        try:
            redis_client.delete(cache_key)
        except:
            # Redis connection failed, fall back to memory cache
            redis_available = False
            if cache_key in memory_cache:
                del memory_cache[cache_key]
    elif cache_key in memory_cache:
        del memory_cache[cache_key]

# Default configurations
DEFAULT_CONFIGS = {
    "success-thresholds": {
        "STRONG_INVESTMENT": {
            "minProbability": 0.75,
            "text": "STRONG INVESTMENT OPPORTUNITY",
            "emoji": "🚀",
            "className": "strong-yes"
        },
        "PROMISING": {
            "minProbability": 0.65,
            "text": "PROMISING OPPORTUNITY",
            "emoji": "✨",
            "className": "yes"
        },
        "CONDITIONAL": {
            "minProbability": 0.55,
            "text": "PROCEED WITH CONDITIONS",
            "emoji": "📊",
            "className": "conditional"
        },
        "NEEDS_IMPROVEMENT": {
            "minProbability": 0.45,
            "text": "NEEDS IMPROVEMENT",
            "emoji": "🔧",
            "className": "needs-work"
        },
        "NOT_READY": {
            "minProbability": 0,
            "text": "NOT READY FOR INVESTMENT",
            "emoji": "⚠️",
            "className": "not-ready"
        }
    },
    "model-weights": {
        "base_analysis": {"weight": 0.35, "label": "Base Analysis", "percentage": "35%"},
        "pattern_detection": {"weight": 0.25, "label": "Pattern Detection", "percentage": "25%"},
        "stage_factors": {"weight": 0.15, "label": "Stage Factors", "percentage": "15%"},
        "industry_specific": {"weight": 0.15, "label": "Industry Specific", "percentage": "15%"},
        "camp_framework": {"weight": 0.10, "label": "CAMP Framework", "percentage": "10%"}
    },
    "revenue-benchmarks": {
        "pre_seed": {"p25": "0%", "p50": "0%", "p75": "100%", "threshold": 0},
        "seed": {"p25": "50%", "p50": "150%", "p75": "300%", "threshold": 50},
        "series_a": {"p25": "100%", "p50": "200%", "p75": "400%", "threshold": 100},
        "series_b": {"p25": "100%", "p50": "200%", "p75": "400%", "threshold": 150},
        "series_c": {"p25": "75%", "p50": "150%", "p75": "300%", "threshold": 100},
        "growth": {"p25": "50%", "p50": "100%", "p75": "200%", "threshold": 75}
    },
    "company-comparables": {
        "SaaS": {
            "Series A": ["Slack at Series A ($340M → $28B)", "Zoom at Series A ($30M → $100B)"],
            "Series B": ["Datadog at Series B ($94M → $40B)", "Monday.com at Series B ($84M → $7B)"]
        },
        "AI/ML": {
            "Series A": ["Hugging Face at Series A ($40M → $2B)", "Scale AI at Series A ($100M → $7B)"],
            "Series B": ["Anthropic at Series B ($124M → $5B)", "Cohere at Series B ($125M → $2B)"]
        },
        "FinTech": {
            "Series A": ["Square at Series A ($10M → $100B)", "Stripe at Series A ($2M → $95B)"],
            "Series B": ["Robinhood at Series B ($110M → $11B)", "Coinbase at Series B ($75M → $85B)"]
        },
        "HealthTech": {
            "Series A": ["Oscar Health at Series A ($30M → $7B)", "Flatiron Health at Series A ($8M → $1.9B)"],
            "Series B": ["Tempus at Series B ($70M → $8B)", "Ro at Series B ($88M → $7B)"]
        },
        "E-commerce": {
            "Series A": ["Warby Parker at Series A ($12M → $3B)", "Casper at Series A ($15M → $1.1B)"],
            "Series B": ["Glossier at Series B ($24M → $1.8B)", "Allbirds at Series B ($17M → $1.7B)"]
        }
    },
    "display-limits": {
        "insights": 3,
        "recommendations": 2,
        "similar_companies": 3,
        "strengths": 3,
        "risks": 3,
        "action_steps": 3,
        "total_insights": 6
    },
    "stage-weights": {
        "pre_seed": {
            "people": 0.40,
            "advantage": 0.30,
            "market": 0.20,
            "capital": 0.10
        },
        "seed": {
            "people": 0.30,
            "advantage": 0.30,
            "market": 0.25,
            "capital": 0.15
        },
        "series_a": {
            "market": 0.30,
            "people": 0.25,
            "advantage": 0.25,
            "capital": 0.20
        },
        "series_b": {
            "market": 0.35,
            "capital": 0.25,
            "advantage": 0.20,
            "people": 0.20
        },
        "series_c": {
            "capital": 0.35,
            "market": 0.30,
            "people": 0.20,
            "advantage": 0.15
        },
        "growth": {
            "capital": 0.35,
            "market": 0.30,
            "people": 0.20,
            "advantage": 0.15
        }
    },
    "model-performance": {
        "dna_analyzer": {"accuracy": 0.7674, "name": "DNA Pattern Analyzer"},
        "temporal_predictor": {"accuracy": 0.7732, "name": "Temporal Predictor"},
        "industry_model": {"accuracy": 0.7744, "name": "Industry-Specific Model"},
        "ensemble_model": {"accuracy": 0.7700, "name": "Ensemble Model"},
        "pattern_matcher": {"accuracy": 0.7700, "name": "Pattern Matcher"},
        "meta_learner": {"accuracy": 0.7681, "name": "Meta Learner"},
        "overall_accuracy": 0.7717,
        "dataset_size": "100k"
    },
    "company-examples": {
        "pre_seed": {
            "company": "Airbnb",
            "story": "Airbnb's founders were rejected by many VCs, but their persistence and execution skills turned a simple idea into a $75B company."
        },
        "seed": {
            "company": "Stripe",
            "story": "Stripe succeeded because the Collison brothers (team) built dramatically better payment APIs (advantage) than existing solutions."
        },
        "series_a": {
            "company": "Uber",
            "story": "Uber raised Series A after proving the ride-sharing market was massive and their model could scale beyond San Francisco."
        },
        "series_b": {
            "company": "DoorDash",
            "story": "DoorDash's Series B focused on their path to market leadership and improving delivery economics."
        },
        "series_c": {
            "company": "Spotify",
            "story": "Spotify's later rounds focused heavily on improving gross margins and reducing customer acquisition costs."
        },
        "growth": {
            "company": "Canva",
            "story": "Canva maintained high growth while achieving profitability, making it attractive for growth investors."
        }
    }
}

# Initialize default configurations
def init_default_configs(db: Session):
    for key, value in DEFAULT_CONFIGS.items():
        existing = db.query(Configuration).filter(Configuration.key == key).first()
        if not existing:
            config = Configuration(
                key=key,
                value=value,
                created_by="system",
                description=f"Default configuration for {key}"
            )
            db.add(config)
    db.commit()

# Authentication helper (simplified for demo)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    # In production, verify JWT token
    # For now, just return a user identifier
    return "admin"

# Pydantic models
class ConfigUpdate(BaseModel):
    value: Dict[str, Any]
    reason: Optional[str] = Field(None, description="Reason for change")

class ABTestCreate(BaseModel):
    test_name: str
    config_key: str
    variants: Dict[str, Any]
    traffic_split: Dict[str, float]
    duration_days: int = 30

# API Endpoints
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    init_default_configs(db)
    db.close()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "redis": redis_available,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/config/{config_key}")
async def get_config(
    config_key: str,
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get configuration by key with caching"""
    # Check cache first
    cached = get_from_cache(config_key)
    if cached:
        return cached
    
    # Check for A/B test
    if user_id:
        ab_test = db.query(ABTestConfig).filter(
            ABTestConfig.config_key == config_key,
            ABTestConfig.is_active == True,
            ABTestConfig.expires_at > datetime.utcnow()
        ).first()
        
        if ab_test:
            # Simple hash-based assignment
            variant = "A" if int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100 < ab_test.traffic_split["A"] * 100 else "B"
            value = ab_test.variants[variant]
            return {"value": value, "variant": variant, "test": ab_test.test_name}
    
    # Get from database
    config = db.query(Configuration).filter(
        Configuration.key == config_key,
        Configuration.is_active == True
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Configuration '{config_key}' not found")
    
    result = config.value
    set_cache(config_key, result)
    return result

@app.put("/config/{config_key}")
async def update_config(
    config_key: str,
    update: ConfigUpdate,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update configuration with audit trail"""
    config = db.query(Configuration).filter(Configuration.key == config_key).first()
    
    if not config:
        # Create new configuration
        config = Configuration(
            key=config_key,
            value=update.value,
            created_by=current_user,
            description=update.reason
        )
        db.add(config)
        old_value = None
    else:
        old_value = config.value
        config.value = update.value
        config.version += 1
        config.updated_at = datetime.utcnow()
    
    # Create audit record
    audit = ConfigurationAudit(
        config_key=config_key,
        old_value=old_value,
        new_value=update.value,
        changed_by=current_user,
        change_reason=update.reason
    )
    db.add(audit)
    
    db.commit()
    db.refresh(config)
    
    # Invalidate cache
    invalidate_cache(config_key)
    
    return {"message": "Configuration updated", "version": config.version}

@app.get("/config")
async def list_configs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all configurations"""
    configs = db.query(Configuration).filter(
        Configuration.is_active == True
    ).offset(skip).limit(limit).all()
    
    return {
        "configs": [
            {
                "key": c.key,
                "version": c.version,
                "updated_at": c.updated_at,
                "description": c.description
            }
            for c in configs
        ]
    }

@app.get("/config/{config_key}/history")
async def get_config_history(
    config_key: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get configuration change history"""
    history = db.query(ConfigurationAudit).filter(
        ConfigurationAudit.config_key == config_key
    ).order_by(ConfigurationAudit.changed_at.desc()).limit(limit).all()
    
    return {
        "history": [
            {
                "changed_at": h.changed_at,
                "changed_by": h.changed_by,
                "change_reason": h.change_reason,
                "old_value": h.old_value,
                "new_value": h.new_value
            }
            for h in history
        ]
    }

@app.post("/config/{config_key}/rollback")
async def rollback_config(
    config_key: str,
    version: int,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Rollback configuration to a previous version"""
    # Get the historical value
    history = db.query(ConfigurationAudit).filter(
        ConfigurationAudit.config_key == config_key
    ).order_by(ConfigurationAudit.changed_at.desc()).all()
    
    if version >= len(history):
        raise HTTPException(status_code=404, detail="Version not found")
    
    target_value = history[version].old_value if version > 0 else history[version].new_value
    
    # Update current configuration
    config = db.query(Configuration).filter(Configuration.key == config_key).first()
    if config:
        old_value = config.value
        config.value = target_value
        config.version += 1
        config.updated_at = datetime.utcnow()
        
        # Create audit record
        audit = ConfigurationAudit(
            config_key=config_key,
            old_value=old_value,
            new_value=target_value,
            changed_by=current_user,
            change_reason=f"Rollback to version {version}"
        )
        db.add(audit)
        db.commit()
        
        # Invalidate cache
        invalidate_cache(config_key)
        
        return {"message": "Configuration rolled back", "version": config.version}
    
    raise HTTPException(status_code=404, detail="Configuration not found")

@app.post("/ab-test")
async def create_ab_test(
    test: ABTestCreate,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create an A/B test"""
    # Validate traffic split
    total_split = sum(test.traffic_split.values())
    if abs(total_split - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail="Traffic split must sum to 1.0")
    
    ab_test = ABTestConfig(
        test_name=test.test_name,
        config_key=test.config_key,
        variants=test.variants,
        traffic_split=test.traffic_split,
        expires_at=datetime.utcnow() + timedelta(days=test.duration_days)
    )
    db.add(ab_test)
    db.commit()
    
    return {"message": "A/B test created", "test_id": ab_test.id}

@app.get("/ab-tests")
async def list_ab_tests(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List A/B tests"""
    query = db.query(ABTestConfig)
    if active_only:
        query = query.filter(
            ABTestConfig.is_active == True,
            ABTestConfig.expires_at > datetime.utcnow()
        )
    
    tests = query.all()
    return {
        "tests": [
            {
                "id": t.id,
                "test_name": t.test_name,
                "config_key": t.config_key,
                "variants": list(t.variants.keys()),
                "traffic_split": t.traffic_split,
                "expires_at": t.expires_at,
                "is_active": t.is_active
            }
            for t in tests
        ]
    }

@app.put("/ab-test/{test_id}/stop")
async def stop_ab_test(
    test_id: int,
    winner: Optional[str] = None,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Stop an A/B test and optionally apply winner"""
    test = db.query(ABTestConfig).filter(ABTestConfig.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="A/B test not found")
    
    test.is_active = False
    
    # If winner specified, update the configuration
    if winner and winner in test.variants:
        config = db.query(Configuration).filter(Configuration.key == test.config_key).first()
        if config:
            old_value = config.value
            config.value = test.variants[winner]
            config.version += 1
            
            # Create audit record
            audit = ConfigurationAudit(
                config_key=test.config_key,
                old_value=old_value,
                new_value=test.variants[winner],
                changed_by=current_user,
                change_reason=f"A/B test '{test.test_name}' winner: {winner}"
            )
            db.add(audit)
            
            # Invalidate cache
            invalidate_cache(test.config_key)
    
    db.commit()
    return {"message": "A/B test stopped", "winner_applied": winner is not None}

@app.post("/config/export")
async def export_configs(
    keys: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Export configurations"""
    query = db.query(Configuration).filter(Configuration.is_active == True)
    if keys:
        query = query.filter(Configuration.key.in_(keys))
    
    configs = query.all()
    
    export_data = {
        "exported_at": datetime.utcnow().isoformat(),
        "configurations": {
            c.key: {
                "value": c.value,
                "version": c.version,
                "description": c.description,
                "updated_at": c.updated_at.isoformat()
            }
            for c in configs
        }
    }
    
    return export_data

@app.post("/config/import")
async def import_configs(
    data: Dict[str, Any],
    overwrite: bool = False,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Import configurations"""
    imported = 0
    skipped = 0
    
    for key, config_data in data.get("configurations", {}).items():
        existing = db.query(Configuration).filter(Configuration.key == key).first()
        
        if existing and not overwrite:
            skipped += 1
            continue
        
        if existing:
            old_value = existing.value
            existing.value = config_data["value"]
            existing.version += 1
            existing.updated_at = datetime.utcnow()
            
            # Create audit record
            audit = ConfigurationAudit(
                config_key=key,
                old_value=old_value,
                new_value=config_data["value"],
                changed_by=current_user,
                change_reason="Configuration import"
            )
            db.add(audit)
        else:
            config = Configuration(
                key=key,
                value=config_data["value"],
                created_by=current_user,
                description=config_data.get("description", "Imported configuration")
            )
            db.add(config)
        
        imported += 1
        invalidate_cache(key)
    
    db.commit()
    
    return {"imported": imported, "skipped": skipped}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)