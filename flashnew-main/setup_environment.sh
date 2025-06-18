#!/bin/bash
# Environment Setup Script for FLASH Platform

echo "🚀 Setting up FLASH Platform Environment"
echo "========================================"

# Generate secure random keys
generate_secret() {
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"
}

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists. Backing up to .env.backup"
    cp .env .env.backup
fi

# Copy production template
cp .env.production .env

# Generate secure keys
echo ""
echo "🔐 Generating secure keys..."

JWT_SECRET=$(generate_secret)
API_KEY_1=$(generate_secret)
API_KEY_2=$(generate_secret)
API_KEY_3=$(generate_secret)
DB_PASSWORD=$(generate_secret)
REDIS_PASSWORD=$(generate_secret)

# Update .env with generated keys (macOS compatible)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/your-secure-database-password-here/$DB_PASSWORD/g" .env
    sed -i '' "s/your-redis-password-here/$REDIS_PASSWORD/g" .env
    sed -i '' "s/your-super-secret-jwt-key-change-this-in-production/$JWT_SECRET/g" .env
    sed -i '' "s/api-key-1,api-key-2,api-key-3/$API_KEY_1,$API_KEY_2,$API_KEY_3/g" .env
else
    # Linux
    sed -i "s/your-secure-database-password-here/$DB_PASSWORD/g" .env
    sed -i "s/your-redis-password-here/$REDIS_PASSWORD/g" .env
    sed -i "s/your-super-secret-jwt-key-change-this-in-production/$JWT_SECRET/g" .env
    sed -i "s/api-key-1,api-key-2,api-key-3/$API_KEY_1,$API_KEY_2,$API_KEY_3/g" .env
fi

echo "✅ Generated secure keys and updated .env"

# Create required directories
echo ""
echo "📁 Creating required directories..."
mkdir -p data logs
echo "✅ Created data/ and logs/ directories"

# Export environment variables for current session
echo ""
echo "🔧 Exporting environment variables..."
export $(grep -v '^#' .env | xargs)
echo "✅ Environment variables exported"

# Display important values (masked)
echo ""
echo "📋 Configuration Summary:"
echo "========================"
echo "DB_PASSWORD: ${DB_PASSWORD:0:8}..."
echo "REDIS_PASSWORD: ${REDIS_PASSWORD:0:8}..."
echo "JWT_SECRET_KEY: ${JWT_SECRET:0:8}..."
echo "API_KEYS: ${API_KEY_1:0:8}..., ${API_KEY_2:0:8}..., ${API_KEY_3:0:8}..."
echo ""
echo "🔒 Full credentials saved in .env file"
echo ""

# Create systemd service file (for Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📝 Creating systemd service file..."
    sudo tee /etc/systemd/system/flash-api.service > /dev/null <<EOF
[Unit]
Description=FLASH API Server
After=network.target redis.service postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin
EnvironmentFile=$(pwd)/.env
ExecStart=/usr/bin/python3 $(pwd)/api_server_unified.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    echo "✅ Systemd service created"
    echo ""
    echo "To enable and start the service:"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable flash-api"
    echo "  sudo systemctl start flash-api"
    echo "  sudo systemctl status flash-api"
fi

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Review and update .env file with your actual values"
echo "2. Ensure Redis is installed and running"
echo "3. Install Python dependencies: pip install -r requirements.txt"
echo "4. Start the server: python api_server_unified.py"
echo ""
echo "🔐 IMPORTANT: Keep your .env file secure and never commit it to git!"