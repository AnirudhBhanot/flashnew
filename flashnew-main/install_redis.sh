#!/bin/bash
# Redis Installation Script for FLASH Platform

echo "🔧 Redis Installation Guide for FLASH"
echo "===================================="

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    echo ""
    echo "To install Redis:"
    echo "1. Install Homebrew if not already installed:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
    echo "2. Install Redis:"
    echo "   brew install redis"
    echo ""
    echo "3. Start Redis service:"
    echo "   brew services start redis"
    echo ""
    echo "4. Verify installation:"
    echo "   redis-cli ping"
    echo "   (should return 'PONG')"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "1. Update package list:"
    echo "   sudo apt update"
    echo ""
    echo "2. Install Redis:"
    echo "   sudo apt install redis-server"
    echo ""
    echo "3. Start Redis service:"
    echo "   sudo systemctl start redis-server"
    echo "   sudo systemctl enable redis-server"
    echo ""
    echo "4. Verify installation:"
    echo "   redis-cli ping"
    
    echo ""
    echo "For RHEL/CentOS:"
    echo "1. Install EPEL repository:"
    echo "   sudo yum install epel-release"
    echo ""
    echo "2. Install Redis:"
    echo "   sudo yum install redis"
    echo ""
    echo "3. Start Redis service:"
    echo "   sudo systemctl start redis"
    echo "   sudo systemctl enable redis"
fi

echo ""
echo "📝 Redis Configuration for FLASH:"
echo "================================"
echo "Default configuration should work, but for production consider:"
echo ""
echo "1. Set a password in /etc/redis/redis.conf:"
echo "   requirepass your_redis_password"
echo ""
echo "2. Configure persistence:"
echo "   appendonly yes"
echo "   appendfsync everysec"
echo ""
echo "3. Set memory limit:"
echo "   maxmemory 256mb"
echo "   maxmemory-policy allkeys-lru"
echo ""
echo "4. Restart Redis after configuration changes:"
echo "   sudo systemctl restart redis"

echo ""
echo "🔍 Checking current Redis status..."
echo ""

# Check if Redis is installed
if command -v redis-cli &> /dev/null; then
    echo "✅ Redis CLI found"
    
    # Try to ping Redis
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis server is running"
        
        # Get Redis info
        echo ""
        echo "Redis Version:"
        redis-cli --version
        
        echo ""
        echo "Redis Memory Usage:"
        redis-cli info memory | grep used_memory_human
        
    else
        echo "❌ Redis server not running or not accessible"
        echo "   Try starting it with the commands above"
    fi
else
    echo "❌ Redis not installed"
    echo "   Please install using the commands above"
fi

echo ""
echo "🔧 Testing Redis connection from Python..."
python3 -c "
try:
    import redis
    print('✅ Python redis package installed')
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Successfully connected to Redis from Python')
except ImportError:
    print('❌ Python redis package not installed')
    print('   Install with: pip install redis')
except Exception as e:
    print(f'❌ Could not connect to Redis: {e}')
"

echo ""
echo "Done! Redis setup check complete."