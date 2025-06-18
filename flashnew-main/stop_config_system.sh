#!/bin/bash

# Stop Configuration System Services

echo "Stopping FLASH Configuration System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Load PIDs from file
if [ -f .config_pids ]; then
    source .config_pids
    
    # Stop Configuration API
    if [ ! -z "$CONFIG_API_PID" ]; then
        if kill -0 $CONFIG_API_PID 2>/dev/null; then
            kill $CONFIG_API_PID
            echo -e "${GREEN}✓ Stopped Configuration API (PID: $CONFIG_API_PID)${NC}"
        else
            echo -e "${RED}Configuration API was not running${NC}"
        fi
    fi
    
    # Stop Metrics Collector
    if [ ! -z "$METRICS_PID" ]; then
        if kill -0 $METRICS_PID 2>/dev/null; then
            kill $METRICS_PID
            echo -e "${GREEN}✓ Stopped Metrics Collector (PID: $METRICS_PID)${NC}"
        else
            echo -e "${RED}Metrics Collector was not running${NC}"
        fi
    fi
    
    rm .config_pids
else
    echo -e "${RED}No PID file found. Services may not be running.${NC}"
fi

# Additional cleanup - find processes by port
echo "Checking for any remaining processes..."

# Kill process on port 8002 (Config API)
CONFIG_PID=$(lsof -ti:8002)
if [ ! -z "$CONFIG_PID" ]; then
    kill $CONFIG_PID
    echo -e "${GREEN}✓ Stopped process on port 8002${NC}"
fi

# Kill process on port 9091 (Metrics)
METRICS_PID=$(lsof -ti:9091)
if [ ! -z "$METRICS_PID" ]; then
    kill $METRICS_PID
    echo -e "${GREEN}✓ Stopped process on port 9091${NC}"
fi

# Kill process on port 9090 (Prometheus)
PROM_PID=$(lsof -ti:9090)
if [ ! -z "$PROM_PID" ]; then
    kill $PROM_PID
    echo -e "${GREEN}✓ Stopped process on port 9090${NC}"
fi

echo -e "\n${GREEN}Configuration System stopped.${NC}"