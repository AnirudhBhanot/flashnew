"""
Database Repositories
Provides data access layer with business logic
"""

import hashlib
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from database.models import (
    Prediction, StartupProfile, APIKey, 
    ModelVersion, AuditLog, PerformanceMetrics
)


class PredictionRepository:
    """Repository for prediction operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        input_features: Dict[str, Any],
        success_probability: float,
        confidence_score: float,
        verdict: str,
        camp_scores: Dict[str, float],
        model_predictions: Dict[str, float],
        **kwargs
    ) -> Prediction:
        """Create a new prediction record"""
        prediction = Prediction(
            input_features=input_features,
            success_probability=success_probability,
            confidence_score=confidence_score,
            verdict=verdict,
            capital_score=camp_scores.get('capital'),
            advantage_score=camp_scores.get('advantage'),
            market_score=camp_scores.get('market'),
            people_score=camp_scores.get('people'),
            model_predictions=model_predictions,
            **kwargs
        )
        
        self.session.add(prediction)
        self.session.flush()
        return prediction
    
    def get_by_id(self, prediction_id: uuid.UUID) -> Optional[Prediction]:
        """Get prediction by ID"""
        return self.session.query(Prediction).filter_by(id=prediction_id).first()
    
    def get_user_predictions(
        self, 
        user_id: str, 
        limit: int = 100,
        offset: int = 0
    ) -> List[Prediction]:
        """Get predictions for a specific user"""
        return (
            self.session.query(Prediction)
            .filter_by(user_id=user_id)
            .order_by(desc(Prediction.created_at))
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get prediction statistics for the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        stats = self.session.query(
            func.count(Prediction.id).label('total'),
            func.avg(Prediction.success_probability).label('avg_probability'),
            func.avg(Prediction.confidence_score).label('avg_confidence'),
            func.count(func.distinct(Prediction.user_id)).label('unique_users')
        ).filter(Prediction.created_at >= cutoff_date).first()
        
        verdict_counts = (
            self.session.query(
                Prediction.verdict,
                func.count(Prediction.id).label('count')
            )
            .filter(Prediction.created_at >= cutoff_date)
            .group_by(Prediction.verdict)
            .all()
        )
        
        return {
            'total_predictions': stats.total or 0,
            'avg_success_probability': float(stats.avg_probability or 0),
            'avg_confidence_score': float(stats.avg_confidence or 0),
            'unique_users': stats.unique_users or 0,
            'verdict_distribution': {v: c for v, c in verdict_counts}
        }


class StartupProfileRepository:
    """Repository for startup profile operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_or_create(self, name: str, **kwargs) -> StartupProfile:
        """Get existing profile or create new one"""
        profile = self.session.query(StartupProfile).filter_by(name=name).first()
        
        if not profile:
            profile = StartupProfile(name=name, **kwargs)
            self.session.add(profile)
            self.session.flush()
        
        return profile
    
    def update_latest_prediction(
        self, 
        profile: StartupProfile, 
        prediction: Prediction
    ):
        """Update profile with latest prediction data"""
        profile.latest_features = prediction.input_features
        profile.latest_prediction_id = prediction.id
        profile.last_prediction_date = prediction.created_at
        
        if not profile.first_prediction_date:
            profile.first_prediction_date = prediction.created_at
        
        profile.total_predictions = (profile.total_predictions or 0) + 1
        
        # Update average probability
        if profile.avg_success_probability:
            # Incremental average
            n = profile.total_predictions
            profile.avg_success_probability = (
                (profile.avg_success_probability * (n - 1) + prediction.success_probability) / n
            )
        else:
            profile.avg_success_probability = prediction.success_probability
        
        self.session.flush()
    
    def search(
        self,
        query: Optional[str] = None,
        sector: Optional[str] = None,
        funding_stage: Optional[str] = None,
        min_probability: Optional[float] = None,
        limit: int = 100
    ) -> List[StartupProfile]:
        """Search startup profiles"""
        q = self.session.query(StartupProfile)
        
        if query:
            q = q.filter(StartupProfile.name.ilike(f'%{query}%'))
        if sector:
            q = q.filter_by(sector=sector)
        if funding_stage:
            q = q.filter_by(funding_stage=funding_stage)
        if min_probability is not None:
            q = q.filter(StartupProfile.avg_success_probability >= min_probability)
        
        return q.order_by(desc(StartupProfile.last_prediction_date)).limit(limit).all()


class APIKeyRepository:
    """Repository for API key operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        name: str,
        owner_email: str,
        rate_limit_per_minute: int = 10,
        expires_days: int = 365,
        **kwargs
    ) -> tuple[APIKey, str]:
        """Create new API key and return (key_object, raw_key)"""
        # Generate random key
        raw_key = f"sk_{uuid.uuid4().hex}"
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        # Create key object
        api_key = APIKey(
            key_hash=key_hash,
            name=name,
            owner_email=owner_email,
            rate_limit_per_minute=rate_limit_per_minute,
            expires_at=datetime.utcnow() + timedelta(days=expires_days),
            **kwargs
        )
        
        self.session.add(api_key)
        self.session.flush()
        
        return api_key, raw_key
    
    def validate_key(self, raw_key: str) -> Optional[APIKey]:
        """Validate API key and return key object if valid"""
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        api_key = self.session.query(APIKey).filter_by(
            key_hash=key_hash,
            is_active=True
        ).first()
        
        if api_key:
            # Check expiration
            if api_key.expires_at and api_key.expires_at < datetime.utcnow():
                return None
            
            # Update usage
            api_key.last_used_at = datetime.utcnow()
            api_key.total_requests = (api_key.total_requests or 0) + 1
            self.session.flush()
        
        return api_key
    
    def get_all_active(self) -> List[APIKey]:
        """Get all active API keys"""
        return self.session.query(APIKey).filter_by(is_active=True).all()


class ModelVersionRepository:
    """Repository for model version operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        version: str,
        model_type: str,
        model_path: str,
        model_checksum: str,
        performance_metrics: Dict[str, float],
        **kwargs
    ) -> ModelVersion:
        """Create new model version"""
        model = ModelVersion(
            version=version,
            model_type=model_type,
            model_path=model_path,
            model_checksum=model_checksum,
            auc_score=performance_metrics.get('auc'),
            accuracy=performance_metrics.get('accuracy'),
            precision=performance_metrics.get('precision'),
            recall=performance_metrics.get('recall'),
            **kwargs
        )
        
        self.session.add(model)
        self.session.flush()
        return model
    
    def get_active_version(self, model_type: str) -> Optional[ModelVersion]:
        """Get active version for a model type"""
        return self.session.query(ModelVersion).filter_by(
            model_type=model_type,
            is_active=True
        ).first()
    
    def set_production(self, model_version: ModelVersion):
        """Set a model version as production"""
        # Deactivate other versions
        self.session.query(ModelVersion).filter_by(
            model_type=model_version.model_type
        ).update({'is_production': False})
        
        # Activate this version
        model_version.is_active = True
        model_version.is_production = True
        self.session.flush()


class AuditLogRepository:
    """Repository for audit log operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def log(
        self,
        action: str,
        status: str = 'success',
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict] = None,
        duration_ms: Optional[int] = None,
        **kwargs
    ):
        """Create audit log entry"""
        log = AuditLog(
            action=action,
            status=status,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            details=details,
            duration_ms=duration_ms,
            **kwargs
        )
        
        self.session.add(log)
        self.session.flush()
        
    def get_recent(self, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs"""
        return (
            self.session.query(AuditLog)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
            .all()
        )