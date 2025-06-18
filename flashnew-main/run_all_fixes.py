#!/usr/bin/env python3
"""
Run all fixes for FLASH platform in the correct order
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}...")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_environment():
    """Check and set up environment variables"""
    print("\n📋 Checking Environment Variables...")
    
    env_vars = {
        "DB_PASSWORD": "flash_secure_password_2025",
        "VALID_API_KEYS": "test_key_123456789012345678901234567890,prod_key_098765432109876543210987654321",
        "DB_NAME": "flash_db",
        "DB_USER": "flash_user",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:3001",
        "ENVIRONMENT": "development"
    }
    
    missing_vars = []
    for var, default in env_vars.items():
        if not os.getenv(var):
            os.environ[var] = default
            missing_vars.append(f"{var}={default}")
    
    if missing_vars:
        print("⚠️  Setting default environment variables:")
        for var in missing_vars:
            print(f"   {var}")
        print("\n   ⚠️  IMPORTANT: Change these values for production!")
    else:
        print("✅ All environment variables are set")
    
    return True

def main():
    """Run all fixes in order"""
    print("🚀 FLASH Platform - Running All Fixes")
    print("=" * 50)
    
    # Define fix steps in order
    steps = [
        # 1. Environment setup
        (check_environment, "Environment setup"),
        
        # 2. Install dependencies
        ([sys.executable, "install_missing_dependencies.py"], "Installing missing dependencies"),
        
        # 3. Security fixes
        ([sys.executable, "fix_critical_security.py"], "Applying security fixes"),
        
        # 4. Database initialization (if PostgreSQL is available)
        ([sys.executable, "init_database.py"], "Initializing database"),
        
        # 5. Model checksum generation
        ([sys.executable, "generate_model_checksums.py"], "Generating model checksums"),
        
        # 6. File reorganization (optional - commented out)
        # ([sys.executable, "reorganize_project.py"], "Reorganizing project structure"),
    ]
    
    success_count = 0
    failed_steps = []
    
    for step_cmd, step_name in steps:
        if callable(step_cmd):
            # It's a function
            if step_cmd():
                success_count += 1
            else:
                failed_steps.append(step_name)
        else:
            # It's a command
            script_name = step_cmd[-1] if isinstance(step_cmd, list) else step_cmd.split()[-1]
            if not Path(script_name).exists():
                print(f"\n⚠️  Skipping {step_name} - Script not found: {script_name}")
                continue
            
            if run_command(step_cmd, step_name):
                success_count += 1
            else:
                failed_steps.append(step_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {len(failed_steps)}")
    
    if failed_steps:
        print("\n❌ Failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
    
    # Test the system
    print("\n🧪 Testing the system...")
    test_result = run_command([sys.executable, "test_minimal_prediction.py"], "Running minimal prediction test")
    
    if test_result:
        print("\n✅ FLASH Platform is ready to use!")
    else:
        print("\n⚠️  System test failed. Please check the errors above.")
    
    # Next steps
    print("\n📋 Next Steps:")
    print("1. Review security fixes in fix_critical_security.py")
    print("2. Update environment variables for production")
    print("3. Set up PostgreSQL if not already done:")
    print("   brew install postgresql")
    print("   brew services start postgresql")
    print("4. Run comprehensive tests:")
    print("   python test_working_integration.py")
    print("5. Start the API server:")
    print("   python api_server_unified.py")
    
    # Create a status file
    status = {
        "fixes_applied": success_count,
        "fixes_failed": len(failed_steps),
        "failed_steps": failed_steps,
        "test_passed": test_result,
        "timestamp": str(Path.cwd().stat().st_mtime)
    }
    
    Path("fixes_status.json").write_text(
        __import__('json').dumps(status, indent=2)
    )
    print("\n📄 Status saved to fixes_status.json")

if __name__ == "__main__":
    main()