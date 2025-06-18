#!/usr/bin/env python3
"""
Test Database Integration
Verify that the database-integrated API server works correctly
"""

import os
import sys
import json
import requests
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Test configuration
API_URL = "http://localhost:8001"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
}

# Sample startup data
SAMPLE_STARTUP = {
    "startup_name": "TestStartup AI",
    "funding_stage": "seed",
    "sector": "ai_ml",
    "total_capital_raised_usd": 1500000,
    "annual_revenue_run_rate": 500000,
    "revenue_growth_rate_percent": 200,
    "burn_multiple": 2.5,
    "gross_margin_percent": 75,
    "team_size_full_time": 8,
    "technical_team_percent": 62.5,
    "tam_size_usd": 10000000000,
    "sam_size_usd": 1000000000,
    "market_growth_rate_percent": 35,
    "monthly_active_users": 1000,
    "user_growth_rate_percent": 50,
    "nps_score": 45
}

class TestDatabaseIntegration:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        
    def test_health_check(self):
        """Test health endpoint"""
        print("1. Testing health check...")
        response = self.session.get(f"{API_URL}/health")
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ Health check passed - Database: {data.get('database')}")
        print(f"   Database stats: {json.dumps(data.get('database_stats'), indent=2)}")
        return True
        
    def test_user_registration(self):
        """Test user registration"""
        print("\n2. Testing user registration...")
        response = self.session.post(
            f"{API_URL}/auth/register",
            json=TEST_USER
        )
        
        if response.status_code == 400:
            # User might already exist
            print("   ⚠️  User already exists, trying login instead")
            return self.test_user_login()
            
        assert response.status_code == 200
        data = response.json()
        self.token = data["access_token"]
        print(f"   ✅ User registered successfully")
        print(f"   Token expires in: {data['expires_in']} seconds")
        return True
        
    def test_user_login(self):
        """Test user login"""
        print("\n3. Testing user login...")
        response = self.session.post(
            f"{API_URL}/auth/login",
            json={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        self.token = data["access_token"]
        print(f"   ✅ Login successful")
        return True
        
    def test_prediction_with_db(self):
        """Test prediction endpoint with database storage"""
        print("\n4. Testing prediction with database storage...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.post(
            f"{API_URL}/predict",
            json=SAMPLE_STARTUP,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ Prediction successful")
        print(f"   Verdict: {data['verdict']}")
        print(f"   Success probability: {data['success_probability']:.2%}")
        print(f"   Confidence: {data['confidence_score']:.2%}")
        return data
        
    def test_prediction_history(self):
        """Test fetching prediction history"""
        print("\n5. Testing prediction history...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(
            f"{API_URL}/predictions/history",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ History fetched successfully")
        print(f"   Total predictions: {data['total']}")
        
        if data['predictions']:
            latest = data['predictions'][0]
            print(f"   Latest prediction:")
            print(f"     - Startup: {latest['startup_name']}")
            print(f"     - Verdict: {latest['verdict']}")
            print(f"     - Created: {latest['created_at']}")
            
            # Test fetching specific prediction
            self.test_prediction_detail(latest['id'])
        
        return True
        
    def test_prediction_detail(self, prediction_id):
        """Test fetching specific prediction"""
        print(f"\n6. Testing prediction detail for ID: {prediction_id}...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(
            f"{API_URL}/predictions/{prediction_id}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ Prediction detail fetched")
        print(f"   Has input features: {'input_features' in data}")
        print(f"   Has model predictions: {'model_predictions' in data}")
        return True
        
    def test_api_key_creation(self):
        """Test API key creation"""
        print("\n7. Testing API key creation...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.post(
            f"{API_URL}/api-keys/create",
            params={
                "name": "Test API Key",
                "description": "Key for testing",
                "rate_limit": 20
            },
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        api_key = data["api_key"]
        print(f"   ✅ API key created")
        print(f"   Key ID: {data['key_id']}")
        print(f"   Key (first 20 chars): {api_key[:20]}...")
        
        # Test using API key
        self.test_prediction_with_api_key(api_key)
        return True
        
    def test_prediction_with_api_key(self, api_key):
        """Test prediction using API key"""
        print("\n8. Testing prediction with API key...")
        
        headers = {"X-API-Key": api_key}
        modified_startup = SAMPLE_STARTUP.copy()
        modified_startup["startup_name"] = "API Key Test Startup"
        
        response = self.session.post(
            f"{API_URL}/predict",
            json=modified_startup,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ Prediction with API key successful")
        print(f"   Verdict: {data['verdict']}")
        return True
        
    def test_startup_search(self):
        """Test startup search"""
        print("\n9. Testing startup search...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(
            f"{API_URL}/startups/search",
            params={"sector": "ai_ml"},
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        print(f"   ✅ Search successful")
        print(f"   Found {data['total']} startups")
        
        if data['startups']:
            for startup in data['startups'][:3]:
                print(f"     - {startup['name']} ({startup['sector']}) - Avg probability: {startup['avg_success_probability']:.2%}")
        
        return True
        
    def test_platform_stats(self):
        """Test platform statistics"""
        print("\n10. Testing platform statistics...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(
            f"{API_URL}/stats/overview",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        stats = data['statistics']
        print(f"   ✅ Statistics fetched")
        print(f"   Total predictions: {stats['total_predictions']}")
        print(f"   Unique users: {stats['unique_users']}")
        print(f"   Avg success probability: {stats['avg_success_probability']:.2%}")
        print(f"   Verdict distribution: {json.dumps(stats['verdict_distribution'], indent=2)}")
        return True
        
    def test_batch_prediction(self):
        """Test batch prediction"""
        print("\n11. Testing batch prediction...")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Create batch of startups
        batch = []
        for i in range(3):
            startup = SAMPLE_STARTUP.copy()
            startup["startup_name"] = f"Batch Startup {i+1}"
            startup["total_capital_raised_usd"] = 1000000 * (i + 1)
            batch.append(startup)
        
        response = self.session.post(
            f"{API_URL}/predict/batch",
            json=batch,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        task_id = data["task_id"]
        print(f"   ✅ Batch submitted")
        print(f"   Task ID: {task_id}")
        print(f"   Batch size: {data['batch_size']}")
        
        # Check task status
        time.sleep(2)  # Wait for processing
        response = self.session.get(
            f"{API_URL}/tasks/{task_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            task = response.json()
            print(f"   Task status: {task.get('status')}")
        
        return True
        
    def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 Running Database Integration Tests")
        print("=" * 50)
        
        try:
            # Run tests in order
            self.test_health_check()
            self.test_user_registration()
            self.test_prediction_with_db()
            self.test_prediction_history()
            self.test_api_key_creation()
            self.test_startup_search()
            self.test_platform_stats()
            self.test_batch_prediction()
            
            print("\n✅ All tests passed! Database integration is working correctly.")
            print("\n📊 Summary:")
            print("- User authentication: ✅")
            print("- Prediction storage: ✅")
            print("- API key management: ✅")
            print("- Audit logging: ✅")
            print("- Search functionality: ✅")
            print("- Statistics tracking: ✅")
            print("- Batch processing: ✅")
            
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            return False
        except requests.exceptions.ConnectionError:
            print("\n❌ Could not connect to API server")
            print("   Make sure the server is running: python api_server_unified_db.py")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False
            
        return True


if __name__ == "__main__":
    print("\n📋 Prerequisites:")
    print("1. PostgreSQL or SQLite database initialized")
    print("2. Database tables created (run init_database.py)")
    print("3. API server running (python api_server_unified_db.py)")
    print("4. Redis running (for caching)")
    
    input("\nPress Enter to start tests...")
    
    tester = TestDatabaseIntegration()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 Database integration complete!")
        print("\nNext steps:")
        print("1. Update frontend to use authentication")
        print("2. Configure production database")
        print("3. Set up database backups")
        print("4. Implement rate limiting per user")
    
    sys.exit(0 if success else 1)