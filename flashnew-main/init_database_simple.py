#!/usr/bin/env python3
"""
Simple Database Initialization for FLASH
Works with both SQLite and PostgreSQL
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import init_database, create_tables, check_connection
from database.models import Base

def main():
    """Initialize database"""
    print("🗄️  Initializing FLASH Database")
    print("=" * 50)
    
    # Determine database type
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        # Default to SQLite for development
        print("📁 Using SQLite database (flash.db)")
        os.environ["SQLITE_DB_PATH"] = "flash.db"
    else:
        print(f"🔗 Using database: {db_url.split('@')[0]}...")
    
    try:
        # Initialize database connection
        print("\n🔌 Connecting to database...")
        engine = init_database()
        
        # Create tables
        print("\n🔨 Creating tables...")
        create_tables()
        
        # Verify connection
        if check_connection():
            print("\n✅ Database initialized successfully!")
            
            # Show connection info
            from database.connection import get_database_url
            url = get_database_url()
            if url.startswith("sqlite"):
                print(f"\n📋 SQLite database: {url.replace('sqlite:///', '')}")
            else:
                print(f"\n📋 PostgreSQL database connected")
            
            print("\n🚀 To start the API server with database:")
            print("   python api_server_unified_db.py")
            
            print("\n🧪 To test the integration:")
            print("   python test_database_integration.py")
            
            print("\n💡 For development, you can use:")
            print("   export DISABLE_AUTH=true  # Disable authentication")
            
        else:
            print("\n❌ Database connection check failed")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)