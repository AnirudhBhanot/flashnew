"""
SQLite Database Connection for FLASH Platform
Alternative to PostgreSQL for development/testing
"""
import os
import logging
from contextlib import contextmanager
from typing import Optional
from pathlib import Path

from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from database.models import Base

logger = logging.getLogger(__name__)

# Global engine and session factory
_engine: Optional[object] = None
_SessionFactory: Optional[sessionmaker] = None


def get_sqlite_url() -> str:
    """Get SQLite database URL"""
    db_path = os.getenv("SQLITE_DB_PATH", "flash.db")
    
    # Ensure the directory exists
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    return f"sqlite:///{db_path}"


def init_sqlite_database() -> object:
    """Initialize SQLite database connection"""
    global _engine, _SessionFactory
    
    if _engine is not None:
        return _engine
    
    url = get_sqlite_url()
    
    # Create engine with optimized settings
    _engine = create_engine(
        url,
        connect_args={
            "check_same_thread": False,  # Allow multi-threading
            "timeout": 30.0,  # 30 second timeout
            "isolation_level": "AUTOCOMMIT"  # Better performance
        },
        poolclass=pool.StaticPool,  # Use static pool for SQLite
        pool_pre_ping=True,  # Verify connections before use
        echo=False
    )
    
    # Enable foreign keys and optimizations for SQLite
    @event.listens_for(_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging for better concurrency
        cursor.execute("PRAGMA synchronous=NORMAL")  # Better performance
        cursor.execute("PRAGMA cache_size=10000")  # Larger cache
        cursor.execute("PRAGMA temp_store=MEMORY")  # Use memory for temp tables
        cursor.close()
    
    # Create session factory
    _SessionFactory = sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=False
    )
    
    logger.info(f"SQLite database initialized: {url}")
    
    # Create tables
    create_tables()
    
    return _engine


def create_tables():
    """Create all tables in the database"""
    if _engine is None:
        raise RuntimeError("Database not initialized")
    
    try:
        Base.metadata.create_all(_engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create tables: {e}")
        raise


@contextmanager
def get_session() -> Session:
    """Get a database session with automatic cleanup"""
    if _SessionFactory is None:
        init_sqlite_database()
    
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
        init_sqlite_database()
    
    session = _SessionFactory()
    try:
        yield session
    finally:
        session.close()


# Initialize on import for convenience
def initialize():
    """Initialize the SQLite database"""
    return init_sqlite_database()