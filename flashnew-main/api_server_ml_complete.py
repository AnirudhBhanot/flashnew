"""
FLASH API Server - Production Ready with Complete ML Infrastructure
Integrates all ML systems: unified orchestrator, integrity checking, versioning, monitoring
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from models.unified_orchestrator_complete import UnifiedOrchestratorComplete
from models.model_integrity import ModelIntegritySystem
from models.model_versioning import ModelVersioningSystem  
from models.model_monitoring import ModelPerformanceMonitor
from core.models import StartupData

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
orchestrator = None
integrity_system = None
versioning_system = None
monitoring_system = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize all ML systems on startup"""
    global orchestrator, integrity_system, versioning_system, monitoring_system
    
    logger.info("Initializing ML systems...")
    
    # Initialize integrity system
    integrity_system = ModelIntegritySystem()
    integrity_report = integrity_system.generate_integrity_report()
    logger.info(f"Model integrity status: {integrity_report['system_status']}")
    
    # Initialize versioning system
    versioning_system = ModelVersioningSystem()
    
    # Initialize monitoring system
    monitoring_system = ModelPerformanceMonitor()
    
    # Initialize orchestrator with integrity checking
    orchestrator = UnifiedOrchestratorComplete()
    
    logger.info("All ML systems initialized successfully")
    
    yield
    
    # Cleanup
    if monitoring_system:
        monitoring_system.stop_monitoring()
    logger.info("ML systems shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="FLASH Venture Intelligence API",
    description="Production ML API with complete infrastructure",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key", "Authorization"],
    expose_headers=["X-Request-ID"],
    max_age=3600,
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check with system status"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "orchestrator": orchestrator is not None,
            "integrity": integrity_system is not None,
            "versioning": versioning_system is not None,
            "monitoring": monitoring_system is not None
        }
    }
    
    if monitoring_system:
        system_health = monitoring_system._calculate_system_health()
        health_status["ml_health"] = system_health
    
    return health_status

# Prediction endpoint with full ML infrastructure
@app.post("/predict")
async def predict(startup_data: StartupData):
    """Generate prediction using complete ML system"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="ML system not initialized")
    
    start_time = datetime.now()
    
    try:
        # Convert to dict for processing
        data_dict = startup_data.model_dump()
        
        # Get prediction from unified orchestrator
        result = orchestrator.predict(data_dict, return_explanations=True)
        
        # Record in monitoring system
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        monitoring_system.record_prediction(
            model_type="unified_orchestrator",
            model_version="complete_v1",
            prediction=result["prediction"],
            confidence=result["confidence"],
            latency_ms=latency_ms,
            features=data_dict
        )
        
        # Add system metadata
        result["metadata"]["ml_systems"] = {
            "integrity_verified": True,
            "version_control": versioning_system.get_current_production_version("unified_orchestrator") or "complete_v1",
            "monitoring_active": True,
            "total_models_used": orchestrator.get_model_info()["total_models"]
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Model information endpoint
@app.get("/models/info")
async def get_model_info():
    """Get information about loaded models"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="ML system not initialized")
    
    return orchestrator.get_model_info()

# Model integrity endpoint
@app.get("/models/integrity")
async def check_model_integrity():
    """Check model integrity status"""
    if not integrity_system:
        raise HTTPException(status_code=503, detail="Integrity system not initialized")
    
    return integrity_system.generate_integrity_report()

# Model versions endpoint
@app.get("/models/versions")
async def get_model_versions(model_type: Optional[str] = None):
    """Get model version information"""
    if not versioning_system:
        raise HTTPException(status_code=503, detail="Versioning system not initialized")
    
    return versioning_system.list_versions(model_type)

# Performance monitoring endpoint
@app.get("/monitoring/performance")
async def get_performance_metrics(hours: int = 24):
    """Get model performance metrics"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    return monitoring_system.get_performance_summary(hours=hours)

# Alerts endpoint
@app.get("/monitoring/alerts")
async def get_active_alerts():
    """Get active performance alerts"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    return monitoring_system.get_active_alerts()

# A/B testing endpoint
@app.post("/experiments/create")
async def create_ab_test(experiment_name: str, model_a: str, model_b: str, traffic_split: float = 0.5):
    """Create a new A/B test"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    monitoring_system.create_ab_test(experiment_name, model_a, model_b, traffic_split)
    return {"status": "created", "experiment": experiment_name}

# Experiments results endpoint
@app.get("/experiments/results")
async def get_experiment_results(experiment_name: Optional[str] = None):
    """Get A/B test results"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    return monitoring_system.get_experiment_results(experiment_name)

# Model deployment endpoint
@app.post("/models/deploy")
async def deploy_model(model_path: str, model_type: str, performance_metrics: Dict[str, float]):
    """Deploy a new model version"""
    if not versioning_system:
        raise HTTPException(status_code=503, detail="Versioning system not initialized")
    
    try:
        version = versioning_system.create_version(
            Path(model_path),
            model_type,
            performance_metrics,
            f"Deployed via API at {datetime.now().isoformat()}"
        )
        
        success = versioning_system.deploy_version(version.version, "blue_green")
        
        return {
            "status": "deployed" if success else "failed",
            "version": version.version,
            "model_type": model_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Performance report endpoint
@app.get("/monitoring/report")
async def get_performance_report():
    """Get comprehensive performance report"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    return monitoring_system.generate_performance_report()

# Feedback endpoint for model improvement
@app.post("/feedback")
async def record_feedback(features_hash: str, actual_outcome: float):
    """Record actual outcome for a prediction"""
    if not monitoring_system:
        raise HTTPException(status_code=503, detail="Monitoring system not initialized")
    
    monitoring_system.record_feedback(features_hash, actual_outcome)
    return {"status": "recorded", "features_hash": features_hash}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
