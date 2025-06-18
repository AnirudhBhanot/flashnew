# FLASH Monitoring and Logging

## Overview

The FLASH platform includes comprehensive monitoring and logging capabilities:

- Structured JSON logging
- Real-time metrics collection
- Performance monitoring
- Security event logging
- Web-based monitoring dashboard

## Components

### 1. Logging System

**Log Files:**
- `logs/flash.log` - General application logs
- `logs/flash_json.log` - Structured JSON logs
- `logs/flash_errors.log` - Error logs only
- `logs/api.log` - API request/response logs
- `logs/models.log` - Model prediction logs
- `logs/performance.log` - Performance metrics
- `logs/security.log` - Security events

**Log Levels:**
- DEBUG: Detailed debugging information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

### 2. Metrics Collection

**Collected Metrics:**
- Request rate and latency
- Success/error rates
- Model prediction performance
- System resources (CPU, memory, disk)
- Model-specific metrics

**Metrics Storage:**
- Real-time in-memory storage
- Persistent JSON files in `metrics/` directory
- Configurable retention period

### 3. Monitoring Dashboard

Access the monitoring dashboard at: `http://localhost:8000/monitoring`

**Features:**
- Real-time metrics updates
- Request latency trends
- Model performance stats
- System health monitoring
- Recent alerts

### 4. API Endpoints

**Monitoring Endpoints:**
- `GET /metrics` - Current system metrics
- `GET /health` - Health check
- `GET /monitoring` - Web dashboard

## Configuration

Environment variables (`.env.monitoring`):
```
LOG_LEVEL=INFO
LOG_DIR=logs
METRICS_DIR=metrics
MONITORING_PORT=8080
LATENCY_THRESHOLD_MS=500
ERROR_RATE_THRESHOLD=0.05
CPU_THRESHOLD_PERCENT=80
MEMORY_THRESHOLD_PERCENT=90
```

## Usage

### Viewing Logs

```bash
# Tail application logs
tail -f logs/flash.log

# View JSON logs with jq
tail -f logs/flash_json.log | jq '.'

# Filter error logs
grep ERROR logs/flash.log

# View specific model logs
grep "model_name.*stage_hierarchical" logs/models.log
```

### Analyzing Metrics

```bash
# Run log analysis
python scripts/analyze_logs.py

# Generate metrics report
python scripts/generate_metrics_report.py

# Export metrics for analysis
python -c "import json; from monitoring.metrics_collector import get_metrics; print(json.dumps(get_metrics(), indent=2))"
```

### Monitoring Alerts

The system automatically generates alerts for:
- High latency (P95 > 500ms)
- High error rate (> 5%)
- High CPU usage (> 80%)
- High memory usage (> 90%)

### Custom Logging

```python
from monitoring.logger_config import get_logger

logger = get_logger(__name__)

# Log with extra context
logger.info("Processing request", extra={
    "request_id": "123",
    "user_id": "456",
    "startup_id": "789"
})
```

### Recording Custom Metrics

```python
from monitoring.metrics_collector import metrics_collector

# Record custom metric
metrics_collector.record_prediction(
    model_name="custom_model",
    startup_id="123",
    prediction=0.75,
    confidence=0.85,
    latency_ms=45.2,
    features_used=45
)
```

## Troubleshooting

### High Memory Usage
1. Check log rotation settings
2. Reduce metrics retention period
3. Increase log file max size

### Missing Metrics
1. Verify monitoring is started
2. Check metrics directory permissions
3. Review error logs

### Dashboard Not Loading
1. Check WebSocket connection
2. Verify monitoring port is open
3. Check browser console for errors

## Best Practices

1. **Log Levels**: Use appropriate log levels
   - DEBUG for development only
   - INFO for general flow
   - WARNING for recoverable issues
   - ERROR for exceptions

2. **Structured Logging**: Include context
   ```python
   logger.info("Action completed", extra={
       "action": "prediction",
       "duration_ms": 123,
       "result": "success"
   })
   ```

3. **Metrics Naming**: Use consistent names
   - `model_<name>_latency`
   - `api_<endpoint>_requests`
   - `system_<resource>_usage`

4. **Regular Monitoring**: 
   - Check dashboard daily
   - Review alerts promptly
   - Analyze trends weekly

## Maintenance

### Log Rotation
Logs are automatically rotated when they reach size limits:
- General logs: 10MB per file, 5 backups
- JSON logs: 50MB per file, 10 backups

### Metrics Cleanup
Old metrics files are automatically deleted after 24 hours.

### Manual Cleanup
```bash
# Clean logs older than 7 days
find logs -name "*.log.*" -mtime +7 -delete

# Clean metrics older than 30 days  
find metrics -name "metrics_*.json" -mtime +30 -delete
```
