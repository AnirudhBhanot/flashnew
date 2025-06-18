"""
Database Models for FLASH Platform
Uses SQLAlchemy ORM for PostgreSQL support
"""

from sqlalchemy import Column, String, Float, Boolean, Integer, JSON, DateTime, ForeignKey, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class User(Base):
    """User accounts for authentication"""
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Authentication
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255))
    organization = Column(String(255))
    role = Column(String(50), default='user')  # 'user', 'admin', 'api_user'
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    predictions = relationship("Prediction", backref="user", foreign_keys="Prediction.user_id")
    api_keys = relationship("APIKey", backref="owner", foreign_keys="APIKey.owner_id")


class Prediction(Base):
    """Store all prediction requests and results"""
    __tablename__ = 'predictions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Request data
    startup_name = Column(String(255))
    user_id = Column(String(255))  # External user ID
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id'))
    
    # Input features (stored as JSON for flexibility)
    input_features = Column(JSON, nullable=False)
    
    # Prediction results
    success_probability = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    verdict = Column(String(50), nullable=False)
    verdict_strength = Column(String(20))
    
    # CAMP scores
    capital_score = Column(Float)
    advantage_score = Column(Float)
    market_score = Column(Float)
    people_score = Column(Float)
    
    # Model predictions
    model_predictions = Column(JSON)  # Dict of model_name -> prediction
    
    # Additional insights
    risk_factors = Column(JSON)  # List of risk factors
    success_factors = Column(JSON)  # List of success factors
    key_insights = Column(JSON)  # List of insights
    
    # Metadata
    model_version = Column(String(50))
    processing_time_ms = Column(Integer)
    error = Column(Text)  # Store any errors
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_created_at', created_at),
        Index('idx_user_id', user_id),
        Index('idx_verdict', verdict),
        Index('idx_success_probability', success_probability),
    )


class StartupProfile(Base):
    """Store detailed startup profiles for tracking"""
    __tablename__ = 'startup_profiles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Basic info
    name = Column(String(255), nullable=False, unique=True)
    sector = Column(String(100))
    funding_stage = Column(String(50))
    hq_location = Column(String(255))
    
    # Latest metrics (updated periodically)
    latest_features = Column(JSON)
    latest_prediction_id = Column(UUID(as_uuid=True), ForeignKey('predictions.id'))
    
    # Tracking
    first_prediction_date = Column(DateTime(timezone=True))
    last_prediction_date = Column(DateTime(timezone=True))
    total_predictions = Column(Integer, default=0)
    
    # Performance tracking
    avg_success_probability = Column(Float)
    probability_trend = Column(String(20))  # 'improving', 'stable', 'declining'
    
    # Relationships will be defined separately to avoid circular dependencies


class APIKey(Base):
    """Manage API keys for authentication"""
    __tablename__ = 'api_keys'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Key details
    key_hash = Column(String(255), nullable=False, unique=True)  # Store hashed key
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Permissions
    is_active = Column(Boolean, default=True)
    rate_limit_per_minute = Column(Integer, default=10)
    allowed_endpoints = Column(JSON)  # List of allowed endpoints
    
    # Usage tracking
    last_used_at = Column(DateTime(timezone=True))
    total_requests = Column(Integer, default=0)
    
    # Owner info
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    owner_email = Column(String(255))
    owner_organization = Column(String(255))
    
    # Expiration
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    predictions = relationship("Prediction", backref="api_key")


class ModelVersion(Base):
    """Track model versions and performance"""
    __tablename__ = 'model_versions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Version info
    version = Column(String(50), nullable=False, unique=True)
    model_type = Column(String(50), nullable=False)  # 'dna_analyzer', 'temporal', etc.
    
    # Performance metrics
    auc_score = Column(Float)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    
    # Model details
    feature_count = Column(Integer)
    training_samples = Column(Integer)
    training_date = Column(DateTime(timezone=True))
    
    # Files
    model_path = Column(String(500))
    model_checksum = Column(String(64))  # SHA-256
    
    # Status
    is_active = Column(Boolean, default=False)
    is_production = Column(Boolean, default=False)
    
    # Additional info
    model_metadata = Column(JSON)  # Additional model info


class AuditLog(Base):
    """Audit trail for all system actions"""
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Action details
    action = Column(String(100), nullable=False)  # 'prediction', 'model_update', etc.
    entity_type = Column(String(50))  # 'prediction', 'model', 'api_key'
    entity_id = Column(String(255))
    
    # User info
    user_id = Column(String(255))
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id'))
    ip_address = Column(String(45))  # Support IPv6
    
    # Details
    details = Column(JSON)
    status = Column(String(20))  # 'success', 'failure', 'error'
    error_message = Column(Text)
    
    # Performance
    duration_ms = Column(Integer)
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_timestamp', timestamp),
        Index('idx_audit_action', action),
        Index('idx_audit_user', user_id),
    )


class PerformanceMetrics(Base):
    """Track system performance metrics"""
    __tablename__ = 'performance_metrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Metric details
    metric_type = Column(String(50), nullable=False)  # 'api_latency', 'model_latency', etc.
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20))  # 'ms', 'count', 'percentage'
    
    # Context
    endpoint = Column(String(255))
    model_version = Column(String(50))
    
    # Aggregation support
    period = Column(String(20))  # 'minute', 'hour', 'day'
    count = Column(Integer, default=1)
    min_value = Column(Float)
    max_value = Column(Float)
    avg_value = Column(Float)
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_timestamp', timestamp),
        Index('idx_metrics_type', metric_type),
        Index('idx_metrics_period', period),
    )