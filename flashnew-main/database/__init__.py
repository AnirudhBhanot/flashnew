"""
Database Package
Provides database models, connection management, and repositories
"""

from database.connection import (
    init_database,
    get_session,
    get_db,
    check_connection,
    close_database,
    create_tables,
    drop_tables,
    get_stats
)

from database.models import (
    Base,
    Prediction,
    StartupProfile,
    APIKey,
    ModelVersion,
    AuditLog,
    PerformanceMetrics
)

from database.repositories import (
    PredictionRepository,
    StartupProfileRepository,
    APIKeyRepository,
    ModelVersionRepository,
    AuditLogRepository
)

__all__ = [
    # Connection management
    'init_database',
    'get_session',
    'get_db',
    'check_connection',
    'close_database',
    'create_tables',
    'drop_tables',
    'get_stats',
    
    # Models
    'Base',
    'Prediction',
    'StartupProfile',
    'APIKey',
    'ModelVersion',
    'AuditLog',
    'PerformanceMetrics',
    
    # Repositories
    'PredictionRepository',
    'StartupProfileRepository',
    'APIKeyRepository',
    'ModelVersionRepository',
    'AuditLogRepository',
]