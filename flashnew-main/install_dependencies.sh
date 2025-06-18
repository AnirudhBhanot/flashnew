#!/bin/bash
# Install all dependencies for FLASH Platform

echo "📦 Installing FLASH Platform Dependencies"
echo "========================================"

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Check if in virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected"
    echo "   It's recommended to use a virtual environment:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo ""
    read -p "Continue without virtual environment? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install production requirements
echo ""
echo "📦 Installing production requirements..."
python3 -m pip install -r requirements_production.txt

# Check Redis package
echo ""
echo "🔍 Checking Redis connection..."
python3 -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis package installed and server accessible')
except redis.ConnectionError:
    print('⚠️  Redis package installed but server not running')
    print('   Start Redis with: brew services start redis (macOS)')
except Exception as e:
    print(f'❌ Redis error: {e}')
"

# Check PostgreSQL connection
echo ""
echo "🔍 Checking PostgreSQL connection..."
python3 -c "
import psycopg2
import os
try:
    # Try to connect using environment variables
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database='postgres',  # Default DB to test connection
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )
    conn.close()
    print('✅ PostgreSQL connection successful')
except psycopg2.OperationalError as e:
    print('⚠️  PostgreSQL not accessible')
    print('   Using SQLite as fallback database')
    print(f'   PostgreSQL error: {e}')
except Exception as e:
    print(f'❌ PostgreSQL error: {e}')
"

# Install development dependencies (optional)
echo ""
read -p "Install development dependencies? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing development dependencies..."
    python3 -m pip install black flake8 mypy pre-commit
    
    # Set up pre-commit hooks
    if [ -f .pre-commit-config.yaml ]; then
        pre-commit install
        echo "✅ Pre-commit hooks installed"
    fi
fi

# Verify key packages
echo ""
echo "✅ Verifying key package installations..."
python3 -c "
packages = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'sqlalchemy': 'SQLAlchemy',
    'redis': 'Redis',
    'prometheus_client': 'Prometheus Client',
    'jose': 'Python-JOSE',
    'passlib': 'Passlib',
    'psutil': 'PSUtil',
    'slowapi': 'SlowAPI'
}

failed = []
for module, name in packages.items():
    try:
        __import__(module)
        print(f'✅ {name}')
    except ImportError:
        print(f'❌ {name}')
        failed.append(name)

if failed:
    print(f'\\n⚠️  Failed to install: {', '.join(failed)}')
else:
    print('\\n✅ All key packages installed successfully!')
"

echo ""
echo "📊 Installation Summary"
echo "======================"
pip list | grep -E "(fastapi|redis|prometheus|sqlalchemy|uvicorn|jose|passlib)"

echo ""
echo "✅ Dependency installation complete!"
echo ""
echo "📝 Next steps:"
echo "1. Start Redis: brew services start redis (macOS)"
echo "2. Configure .env file with your settings"
echo "3. Run the server: python api_server_unified.py"