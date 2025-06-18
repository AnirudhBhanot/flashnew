#!/usr/bin/env python3
"""
Install missing dependencies for FLASH platform
"""

import subprocess
import sys
from pathlib import Path

def check_dependency(package):
    """Check if a package is installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_package(package, version=None):
    """Install a package using pip"""
    if version:
        package_spec = f"{package}=={version}"
    else:
        package_spec = package
    
    print(f"Installing {package_spec}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_spec])
        print(f"✅ Installed {package_spec}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_spec}")
        return False

def update_requirements():
    """Update requirements.txt with missing dependencies"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("Creating requirements.txt...")
        requirements_file.touch()
    
    current_reqs = requirements_file.read_text().strip().split('\n')
    current_packages = {line.split('==')[0].strip() for line in current_reqs if line.strip()}
    
    new_dependencies = [
        "psutil==5.9.5",
        "scipy==1.11.4",
        "requests==2.31.0",
        "tabulate==0.9.0",
        "python-jose==3.3.0",  # For JWT authentication
        "passlib==1.7.4",      # For password hashing
        "python-multipart==0.0.6",  # For file uploads
        "email-validator==2.0.0",   # For email validation
        "asyncpg==0.28.0",     # For async PostgreSQL
        "redis==5.0.0",        # For caching
        "celery==5.3.1",       # For async tasks
        "sentry-sdk==1.32.0",  # For error tracking
    ]
    
    lines_to_add = []
    for dep in new_dependencies:
        package_name = dep.split('==')[0]
        if package_name not in current_packages:
            lines_to_add.append(dep)
    
    if lines_to_add:
        with open(requirements_file, 'a') as f:
            f.write('\n' + '\n'.join(lines_to_add))
        print(f"✅ Added {len(lines_to_add)} dependencies to requirements.txt")
    else:
        print("✅ All dependencies already in requirements.txt")

def main():
    """Main installation process"""
    print("📦 Installing Missing Dependencies for FLASH")
    print("=" * 50)
    
    # Critical dependencies
    critical_deps = [
        ("psutil", "5.9.5", "System monitoring"),
        ("scipy", "1.11.4", "Statistical functions"),
    ]
    
    # Development dependencies
    dev_deps = [
        ("requests", "2.31.0", "HTTP requests for testing"),
        ("tabulate", "0.9.0", "Table formatting"),
    ]
    
    # Security dependencies
    security_deps = [
        ("python-jose", "3.3.0", "JWT authentication"),
        ("passlib", "1.7.4", "Password hashing"),
        ("email-validator", "2.0.0", "Email validation"),
    ]
    
    # Optional dependencies
    optional_deps = [
        ("autogluon", "0.8.2", "AutoML experiments"),
        ("optuna", "3.3.0", "Hyperparameter optimization"),
        ("redis", "5.0.0", "Caching layer"),
        ("celery", "5.3.1", "Async task queue"),
        ("sentry-sdk", "1.32.0", "Error tracking"),
    ]
    
    print("\n🔧 Installing Critical Dependencies...")
    for package, version, description in critical_deps:
        print(f"\n{package}: {description}")
        if check_dependency(package):
            print(f"✅ {package} already installed")
        else:
            install_package(package, version)
    
    print("\n🔧 Installing Development Dependencies...")
    for package, version, description in dev_deps:
        print(f"\n{package}: {description}")
        if check_dependency(package):
            print(f"✅ {package} already installed")
        else:
            install_package(package, version)
    
    print("\n🔐 Installing Security Dependencies...")
    for package, version, description in security_deps:
        print(f"\n{package}: {description}")
        if check_dependency(package.replace('-', '_')):
            print(f"✅ {package} already installed")
        else:
            install_package(package, version)
    
    print("\n📋 Optional Dependencies (install if needed):")
    for package, version, description in optional_deps:
        print(f"  pip install {package}=={version}  # {description}")
    
    print("\n📝 Updating requirements.txt...")
    update_requirements()
    
    print("\n✅ Dependency installation complete!")
    print("\n📋 Next steps:")
    print("1. Install PostgreSQL: brew install postgresql")
    print("2. Install Redis (optional): brew install redis")
    print("3. Run security fixes: python fix_critical_security.py")
    print("4. Initialize database: python init_database.py")

if __name__ == "__main__":
    main()