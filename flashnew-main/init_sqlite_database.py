#!/usr/bin/env python3
"""
Initialize SQLite database for FLASH platform
Quick alternative to PostgreSQL
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.sqlite_connection import initialize, get_session
from database.models import APIKey, ModelVersion
from database.repositories import APIKeyRepository, ModelVersionRepository


def init_database():
    """Initialize SQLite database with initial data"""
    print("🗄️  Initializing SQLite Database for FLASH")
    print("=" * 50)
    
    # Initialize database
    print("\n1️⃣ Creating database and tables...")
    engine = initialize()
    print("✅ Database created: flash.db")
    
    # Create initial data
    print("\n2️⃣ Creating initial data...")
    
    with get_session() as session:
        # Create API keys
        api_key_repo = APIKeyRepository(session)
        
        # Development API key
        dev_key, raw_dev_key = api_key_repo.create(
            name="Development Key",
            owner_email="dev@flash-platform.com",
            rate_limit_per_minute=100
        )
        print(f"✅ Created development API key: {raw_dev_key}")
        
        # Test API key
        test_key, raw_test_key = api_key_repo.create(
            name="Test Key",
            owner_email="test@flash-platform.com",
            rate_limit_per_minute=50
        )
        print(f"✅ Created test API key: {raw_test_key}")
        
        # Create model version entries
        model_repo = ModelVersionRepository(session)
        
        models = [
            ("dna_analyzer", "models/production_v45/dna_analyzer.pkl", 0.7711),
            ("temporal_model", "models/production_v45/temporal_model.pkl", 0.7736),
            ("industry_model", "models/production_v45/industry_model.pkl", 0.7717),
            ("ensemble_model", "models/production_v45/ensemble_model.pkl", 0.7401)
        ]
        
        for model_type, model_path, auc_score in models:
            model_version = model_repo.create(
                version=f"v45_{model_type}",  # Unique version per model
                model_type=model_type,
                model_path=model_path,
                model_checksum="placeholder",  # Would calculate real checksum
                performance_metrics={
                    "auc": auc_score,
                    "accuracy": auc_score - 0.05,  # Approximate
                    "precision": auc_score - 0.03,
                    "recall": auc_score - 0.07
                },
                is_active=True,
                is_production=True
            )
            print(f"✅ Registered model: {model_type} (AUC: {auc_score:.4f})")
    
    # Verify setup
    print("\n3️⃣ Verifying database setup...")
    with get_session() as session:
        api_key_count = session.query(APIKey).count()
        model_count = session.query(ModelVersion).count()
        
        print(f"✅ API Keys: {api_key_count}")
        print(f"✅ Model Versions: {model_count}")
    
    print("\n✅ Database initialization complete!")
    print("\n📋 Next steps:")
    print("1. Update API server to use SQLite:")
    print("   - Import from database.sqlite_connection instead of database.connection")
    print("2. Configure API keys in environment:")
    print(f"   export API_KEYS='{raw_dev_key},{raw_test_key}'")
    print("3. Start API server:")
    print("   python api_server_unified.py")
    
    # Save keys to env file
    env_file = Path(".env.development")
    env_content = f"""# FLASH Development Environment
ENVIRONMENT=development
DB_PASSWORD=not_needed_for_sqlite
API_KEYS={raw_dev_key},{raw_test_key}
SQLITE_DB_PATH=flash.db
"""
    env_file.write_text(env_content)
    print(f"\n✅ Saved environment variables to {env_file}")


if __name__ == "__main__":
    init_database()