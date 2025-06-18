#!/bin/bash

# Start Configuration System Services

echo "Starting FLASH Configuration System..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}Warning: Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Create necessary directories
mkdir -p logs
mkdir -p monitoring

# Check Redis
echo -e "${BLUE}Checking Redis...${NC}"
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${YELLOW}Redis is not running. Starting Redis...${NC}"
    if command -v redis-server &> /dev/null; then
        redis-server --daemonize yes
        sleep 2
    else
        echo -e "${YELLOW}Redis not installed. Configuration API will use in-memory cache.${NC}"
    fi
else
    echo -e "${GREEN}✓ Redis is running${NC}"
fi

# Start Configuration API Server
echo -e "${BLUE}Starting Configuration API Server (port 8002)...${NC}"
if check_port 8002; then
    python3 config_api_server.py > logs/config_api.log 2>&1 &
    CONFIG_API_PID=$!
    echo "Configuration API PID: $CONFIG_API_PID"
    sleep 3
    
    # Check if API started successfully
    if curl -s http://localhost:8002/health > /dev/null; then
        echo -e "${GREEN}✓ Configuration API is running${NC}"
    else
        echo -e "${YELLOW}Configuration API failed to start. Check logs/config_api.log${NC}"
    fi
fi

# Start Metrics Collector
echo -e "${BLUE}Starting Metrics Collector (port 9091)...${NC}"
if check_port 9091; then
    cd monitoring
    python3 config_metrics_collector.py > ../logs/metrics_collector.log 2>&1 &
    METRICS_PID=$!
    cd ..
    echo "Metrics Collector PID: $METRICS_PID"
    sleep 3
    echo -e "${GREEN}✓ Metrics Collector is running${NC}"
fi

# Update Frontend Configuration
echo -e "${BLUE}Updating Frontend Configuration...${NC}"
cd flash-frontend

# Create .env.local if it doesn't exist
if [ ! -f .env.local ]; then
    echo "REACT_APP_CONFIG_API_URL=http://localhost:8002" > .env.local
    echo -e "${GREEN}✓ Created .env.local with configuration API URL${NC}"
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
fi

cd ..

# Create admin route if not exists
echo -e "${BLUE}Setting up admin route...${NC}"
ADMIN_ROUTE_FILE="flash-frontend/src/components/admin/index.ts"
if [ ! -f "$ADMIN_ROUTE_FILE" ]; then
    echo "export { ConfigurationAdmin } from './ConfigurationAdmin';" > $ADMIN_ROUTE_FILE
    echo -e "${GREEN}✓ Created admin route export${NC}"
fi

# Save PIDs to file for shutdown script
echo "CONFIG_API_PID=$CONFIG_API_PID" > .config_pids
echo "METRICS_PID=$METRICS_PID" >> .config_pids

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Configuration System Started! 🚀${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Services running:"
echo "  - Configuration API: http://localhost:8002"
echo "  - Metrics Dashboard: http://localhost:9091/dashboard"
echo "  - Prometheus Metrics: http://localhost:9090/metrics"
echo ""
echo "Admin Interface:"
echo "  1. Start frontend: cd flash-frontend && npm start"
echo "  2. Navigate to: http://localhost:3000/admin/config"
echo ""
echo "API Documentation:"
echo "  - Swagger UI: http://localhost:8002/docs"
echo "  - ReDoc: http://localhost:8002/redoc"
echo ""
echo "To stop all services: ./stop_config_system.sh"
echo ""
echo -e "${BLUE}Running tests...${NC}"
sleep 2
python3 test_config_system.py