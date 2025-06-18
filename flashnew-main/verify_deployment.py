#!/usr/bin/env python3
"""
Verify FLASH Platform deployment readiness
"""
import os
import sys
import json
import subprocess
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False


def check_environment():
    """Check environment variables"""
    print("\n🔧 Checking Environment Variables")
    print("=" * 40)
    
    required_vars = [
        "JWT_SECRET_KEY",
        "API_KEYS",
        "DB_PASSWORD"
    ]
    
    all_good = True
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set")
            all_good = False
    
    return all_good


def check_models():
    """Check model files and checksums"""
    print("\n🤖 Checking Models")
    print("=" * 40)
    
    # Check if checksums file exists
    if not os.path.exists("production_model_checksums.json"):
        print("❌ Model checksums file missing")
        print("   Run: python3 utils/model_integrity.py")
        return False
    
    # Verify models
    try:
        from utils.model_integrity import verify_production_models
        if verify_production_models():
            print("✅ All models verified")
            return True
        else:
            print("❌ Model verification failed")
            return False
    except Exception as e:
        print(f"❌ Error verifying models: {e}")
        return False


def check_dependencies():
    """Check Python dependencies"""
    print("\n📦 Checking Dependencies")
    print("=" * 40)
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "redis",
        "jose",
        "passlib",
        "prometheus_client",
        "psutil"
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            all_good = False
    
    return all_good


def check_services():
    """Check external services"""
    print("\n🔍 Checking Services")
    print("=" * 40)
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✅ Redis is accessible")
    except:
        print("⚠️  Redis not accessible (caching will be disabled)")
    
    # Check PostgreSQL
    try:
        import psycopg2
        # This will fail if not configured, which is OK
        print("ℹ️  PostgreSQL check skipped (SQLite will be used)")
    except ImportError:
        print("ℹ️  psycopg2 not installed (SQLite will be used)")


def check_security():
    """Check security configurations"""
    print("\n🔒 Checking Security")
    print("=" * 40)
    
    checks = []
    
    # Check .env file permissions
    if os.path.exists(".env"):
        stat_info = os.stat(".env")
        mode = oct(stat_info.st_mode)[-3:]
        if mode == "600" or mode == "640":
            print("✅ .env file permissions are secure")
            checks.append(True)
        else:
            print(f"⚠️  .env file permissions ({mode}) should be 600 or 640")
            checks.append(False)
    
    # Check for default passwords
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "your-secure-password" in content or "change-this" in content:
                print("❌ Default passwords found in .env")
                checks.append(False)
            else:
                print("✅ No default passwords detected")
                checks.append(True)
    
    return all(checks) if checks else False


def main():
    """Run all deployment checks"""
    print("🚀 FLASH Platform Deployment Verification")
    print("=" * 50)
    
    checks = []
    
    # File checks
    print("\n📁 Checking Required Files")
    print("=" * 40)
    checks.append(check_file_exists("api_server_unified.py", "Main API server"))
    checks.append(check_file_exists(".env", "Environment configuration"))
    checks.append(check_file_exists("requirements_production.txt", "Production requirements"))
    checks.append(check_file_exists("models/production_v45/dna_analyzer.pkl", "DNA Analyzer model"))
    
    # Other checks
    checks.append(check_environment())
    checks.append(check_models())
    checks.append(check_dependencies())
    check_services()  # Don't fail on service checks
    checks.append(check_security())
    
    # Summary
    print("\n📊 Deployment Readiness Summary")
    print("=" * 50)
    
    passed = sum(1 for c in checks if c)
    total = len(checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"Checks passed: {passed}/{total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print("\n✅ System is ready for deployment!")
        print("\nTo start:")
        print("  ./start_production.sh")
        print("\nOr with Docker:")
        print("  docker-compose up -d")
    elif percentage >= 75:
        print("\n⚠️  System is mostly ready but has some issues")
        print("Review the warnings above before deploying")
    else:
        print("\n❌ System is not ready for deployment")
        print("Please fix the issues above first")
    
    return 0 if percentage >= 75 else 1


if __name__ == "__main__":
    sys.exit(main())