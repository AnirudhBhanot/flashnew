#!/usr/bin/env python3
"""
Initialize PostgreSQL database for FLASH platform
"""

import os
import sys
import subprocess
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_postgresql():
    """Check if PostgreSQL is installed and running"""
    try:
        # Check if psql command exists
        result = subprocess.run(['which', 'psql'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ PostgreSQL not found. Install with: brew install postgresql")
            return False
        
        # Check if PostgreSQL is running
        result = subprocess.run(['pg_isready'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ PostgreSQL is not running. Start with: brew services start postgresql")
            return False
        
        print("✅ PostgreSQL is installed and running")
        return True
    except Exception as e:
        print(f"❌ Error checking PostgreSQL: {e}")
        return False

def create_database():
    """Create the FLASH database"""
    db_name = os.getenv("DB_NAME", "flash_db")
    db_user = os.getenv("DB_USER", os.getenv("USER", "postgres"))
    
    try:
        # Connect to PostgreSQL as superuser
        conn = psycopg2.connect(
            host="localhost",
            user=db_user,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ Database '{db_name}' already exists")
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Created database '{db_name}'")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_user():
    """Create database user with proper permissions"""
    db_name = os.getenv("DB_NAME", "flash_db")
    db_user = os.getenv("DB_USER", "flash_user")
    db_password = os.getenv("DB_PASSWORD")
    
    if not db_password:
        print("⚠️  DB_PASSWORD not set. Using default (NOT SECURE!)")
        db_password = "flash_dev_password"
    
    try:
        # Connect as superuser
        conn = psycopg2.connect(
            host="localhost",
            user=os.getenv("USER", "postgres"),
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(f"SELECT 1 FROM pg_user WHERE usename = '{db_user}'")
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ User '{db_user}' already exists")
            # Update password
            cursor.execute(f"ALTER USER {db_user} WITH PASSWORD '{db_password}'")
        else:
            # Create user
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
            print(f"✅ Created user '{db_user}'")
        
        # Grant permissions
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        print(f"✅ Granted privileges on '{db_name}' to '{db_user}'")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False

def run_alembic_migrations():
    """Run Alembic migrations"""
    alembic_ini = Path("alembic.ini")
    if not alembic_ini.exists():
        print("❌ alembic.ini not found. Creating basic configuration...")
        create_alembic_config()
    
    try:
        # Run migrations
        result = subprocess.run(['alembic', 'upgrade', 'head'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Alembic migrations completed")
        else:
            print(f"⚠️  Alembic migrations failed: {result.stderr}")
            print("   Falling back to direct table creation...")
            return create_tables_directly()
        return True
    except Exception as e:
        print(f"⚠️  Alembic not available: {e}")
        print("   Falling back to direct table creation...")
        return create_tables_directly()

def create_alembic_config():
    """Create basic Alembic configuration"""
    config_content = """[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
    Path("alembic.ini").write_text(config_content)
    print("✅ Created alembic.ini")

def create_tables_directly():
    """Create tables directly using SQLAlchemy"""
    try:
        # Add project root to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from database.connection import engine, Base
        from database.models import (
            Prediction, StartupProfile, ModelVersion, 
            APIKey, RateLimitEntry, User
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Created database tables")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_indexes():
    """Create database indexes for performance"""
    db_name = os.getenv("DB_NAME", "flash_db")
    db_user = os.getenv("DB_USER", "flash_user")
    db_password = os.getenv("DB_PASSWORD", "flash_dev_password")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_predictions_startup_id ON predictions(startup_id)",
            "CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at DESC)",
            "CREATE INDEX IF NOT EXISTS idx_predictions_success_prob ON predictions(success_probability)",
            "CREATE INDEX IF NOT EXISTS idx_api_keys_key ON api_keys(key)",
            "CREATE INDEX IF NOT EXISTS idx_api_keys_active ON api_keys(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_rate_limits_key_endpoint ON rate_limit_entries(api_key, endpoint)",
        ]
        
        for index in indexes:
            cursor.execute(index)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Created database indexes")
        return True
        
    except Exception as e:
        print(f"⚠️  Error creating indexes: {e}")
        return False

def verify_setup():
    """Verify database setup"""
    db_name = os.getenv("DB_NAME", "flash_db")
    db_user = os.getenv("DB_USER", "flash_user")
    db_password = os.getenv("DB_PASSWORD", "flash_dev_password")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print("\n📊 Database Tables:")
        for table in tables:
            print(f"   ✓ {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database setup verified!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False

def main():
    """Main initialization process"""
    print("🗄️  Initializing FLASH Database")
    print("=" * 50)
    
    # Check environment
    print("\n📋 Environment Configuration:")
    print(f"   DB_NAME: {os.getenv('DB_NAME', 'flash_db')}")
    print(f"   DB_USER: {os.getenv('DB_USER', 'flash_user')}")
    print(f"   DB_HOST: {os.getenv('DB_HOST', 'localhost')}")
    print(f"   DB_PORT: {os.getenv('DB_PORT', '5432')}")
    
    if not os.getenv("DB_PASSWORD"):
        print("\n⚠️  WARNING: DB_PASSWORD not set!")
        print("   Using development password (NOT SECURE)")
        print("   Set with: export DB_PASSWORD='your-secure-password'")
    
    # Initialize database
    steps = [
        ("Checking PostgreSQL", check_postgresql),
        ("Creating database", create_database),
        ("Creating user", create_user),
        ("Running migrations", run_alembic_migrations),
        ("Creating indexes", create_indexes),
        ("Verifying setup", verify_setup),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔧 {step_name}...")
        if not step_func():
            print(f"\n❌ Failed at step: {step_name}")
            print("   Please fix the issue and run again")
            return
    
    print("\n✅ Database initialization complete!")
    print("\n📋 Next steps:")
    print("1. Set secure password: export DB_PASSWORD='your-secure-password'")
    print("2. Run security fixes: python fix_critical_security.py")
    print("3. Start API server: python api_server_unified.py")
    print("4. Run tests: python test_working_integration.py")

if __name__ == "__main__":
    main()