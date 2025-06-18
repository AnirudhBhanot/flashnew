"""
Database Connection Management
Handles PostgreSQL connections with pooling and retry logic
"""

import os
import logging
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

from database.models import Base
from config import Settings

logger = logging.getLogger(__name__)

# Global engine and session factory
_engine: Optional[Engine] = None
_SessionFactory: Optional[sessionmaker] = None


def get_database_url() -> str:
    """Get database URL from environment or config"""
    # Check for explicit DATABASE_URL first
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    # Check if using SQLite
    sqlite_path = os.getenv("SQLITE_DB_PATH")
    if sqlite_path or Settings.is_development():
        # Use SQLite for development by default
        db_path = sqlite_path or "flash.db"
        return f"sqlite:///{db_path}"
    
    # Build PostgreSQL URL from components
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "flash_db")
    db_user = os.getenv("DB_USER", "flash_user")
    
    # Password must be set via environment variable for PostgreSQL
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError(
            "DB_PASSWORD environment variable must be set for PostgreSQL. "
            "For development, use SQLite or set: export DB_PASSWORD='your-secure-password'"
        )
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def init_database(database_url: Optional[str] = None) -> Engine:
    """Initialize database connection with connection pooling"""
    global _engine, _SessionFactory
    
    if _engine is not None:
        return _engine
    
    url = database_url or get_database_url()
    
    # Create engine with appropriate settings for database type
    if url.startswith("sqlite"):
        # SQLite specific settings
        _engine = create_engine(
            url,
            connect_args={"check_same_thread": False},  # Allow multi-threading
            poolclass=pool.StaticPool,  # Use StaticPool for SQLite
            echo=Settings.DEBUG,  # Log SQL in debug mode
        )
    else:
        # PostgreSQL settings
        _engine = create_engine(
            url,
            # Connection pool settings
            poolclass=pool.QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,  # Recycle connections after 1 hour
            
            # Performance settings
            echo=Settings.DEBUG,  # Log SQL in debug mode
            echo_pool=Settings.DEBUG,
            
            # Connection args
            connect_args={
                "connect_timeout": 10,
                "application_name": "flash_api",
                "options": "-c statement_timeout=30000"  # 30 second statement timeout
            }
        )
    
    # Add event listeners
    @event.listens_for(_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """Set connection parameters"""
        if 'postgresql' in url:
            cursor = dbapi_connection.cursor()
            cursor.execute("SET TIME ZONE 'UTC'")
            cursor.close()
    
    # Create session factory
    _SessionFactory = sessionmaker(
        bind=_engine,
        expire_on_commit=False,  # Don't expire objects after commit
        autoflush=False,  # Don't auto-flush before queries
    )
    
    logger.info(f"Database engine initialized: {url.split('@')[1] if '@' in url else url}")
    
    return _engine


def create_tables():
    """Create all tables in the database"""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    try:
        Base.metadata.create_all(_engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create tables: {e}")
        raise


def drop_tables():
    """Drop all tables in the database (use with caution!)"""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    try:
        Base.metadata.drop_all(_engine)
        logger.warning("All database tables dropped!")
    except SQLAlchemyError as e:
        logger.error(f"Failed to drop tables: {e}")
        raise


@contextmanager
def get_session() -> Session:
    """Get a database session with automatic cleanup"""
    if _SessionFactory is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    session = _SessionFactory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_db() -> Session:
    """Dependency for FastAPI to get DB session"""
    if _SessionFactory is None:
        init_database()
    
    session = _SessionFactory()
    try:
        yield session
    finally:
        session.close()


def check_connection() -> bool:
    """Check if database connection is working"""
    try:
        if _engine is None:
            init_database()
        
        with _engine.connect() as conn:
            result = conn.execute("SELECT 1")
            result.fetchone()
        
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


def close_database():
    """Close database connections and cleanup"""
    global _engine, _SessionFactory
    
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _SessionFactory = None
        logger.info("Database connections closed")


# Health check query
def get_stats() -> dict:
    """Get database statistics"""
    if _engine is None:
        return {"status": "not_initialized"}
    
    try:
        pool_status = _engine.pool.status()
        
        with get_session() as session:
            # Count records in main tables
            from database.models import Prediction, StartupProfile, APIKey
            
            stats = {
                "status": "connected",
                "pool_status": pool_status,
                "predictions_count": session.query(Prediction).count(),
                "startups_count": session.query(StartupProfile).count(),
                "api_keys_count": session.query(APIKey).count(),
            }
            
        return stats
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }