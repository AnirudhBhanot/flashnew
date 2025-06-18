#!/usr/bin/env python3
"""
Script to integrate monitoring and logging into the existing API server
"""

import sys
import os

def add_monitoring_imports():
    """Add monitoring imports to api_server.py"""
    imports_to_add = """
# Monitoring and Logging imports
from monitoring.logger_config import setup_logging, get_logger, model_logger, api_logger
from monitoring.metrics_collector import start_monitoring, stop_monitoring, get_metrics
from monitoring.api_middleware import setup_monitoring_middleware, log_prediction_metrics
from monitoring.monitoring_dashboard import dashboard_app
"""
    return imports_to_add

def add_monitoring_initialization():
    """Add monitoring initialization code"""
    init_code = """
# Initialize monitoring and logging
setup_logging(app_name="flash_api", log_level=os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

# Start monitoring
@app.on_event("startup")
async def startup_monitoring():
    start_monitoring()
    logger.info("Monitoring system started")

@app.on_event("shutdown")
async def shutdown_monitoring():
    stop_monitoring()
    logger.info("Monitoring system stopped")

# Setup monitoring middleware
setup_monitoring_middleware(app)

# Mount monitoring dashboard
app.mount("/monitoring", dashboard_app)
"""
    return init_code

def add_metrics_endpoint():
    """Add metrics endpoint code"""
    endpoint_code = """
@app.get("/metrics", tags=["monitoring"])
async def get_system_metrics():
    \"\"\"Get current system metrics\"\"\"
    return get_metrics()
"""
    return endpoint_code

def add_prediction_logging():
    """Add logging to prediction endpoint"""
    logging_code = """
    # Log prediction metrics
    log_prediction_metrics(
        model_name="ensemble",
        startup_id=str(hash(str(metrics.dict()))),
        prediction=response['success_probability'],
        confidence=response.get('confidence_interval', {}).get('upper', 0) - 
                   response.get('confidence_interval', {}).get('lower', 0),
        latency_ms=(time.time() - start_time) * 1000,
        features_count=len(metrics.dict())
    )
"""
    return logging_code

def create_monitoring_config():
    """Create monitoring configuration file"""
    config_content = """# Monitoring Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
METRICS_DIR=metrics
MONITORING_PORT=8080

# Alert Thresholds
LATENCY_THRESHOLD_MS=500
ERROR_RATE_THRESHOLD=0.05
CPU_THRESHOLD_PERCENT=80
MEMORY_THRESHOLD_PERCENT=90

# Retention Settings
LOG_RETENTION_DAYS=7
METRICS_RETENTION_DAYS=30
"""
    
    with open('.env.monitoring', 'w') as f:
        f.write(config_content)
    print("✅ Created .env.monitoring configuration file")

def create_example_scripts():
    """Create example monitoring scripts"""
    
    # Log analysis script
    log_analysis = """#!/usr/bin/env python3
\"\"\"
Analyze FLASH API logs for insights
\"\"\"

import json
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd

def analyze_logs(log_file='logs/flash_json.log', hours=24):
    \"\"\"Analyze recent logs\"\"\"
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    stats = {
        'total_requests': 0,
        'errors': 0,
        'endpoints': defaultdict(int),
        'slow_requests': [],
        'error_details': []
    }
    
    with open(log_file, 'r') as f:
        for line in f:
            try:
                log = json.loads(line)
                log_time = datetime.fromisoformat(log['timestamp'])
                
                if log_time < cutoff_time:
                    continue
                
                # Count requests
                if log['logger'] == 'api':
                    stats['total_requests'] += 1
                    
                    if 'endpoint' in log:
                        stats['endpoints'][log['endpoint']] += 1
                    
                    # Track errors
                    if log['level'] == 'ERROR':
                        stats['errors'] += 1
                        stats['error_details'].append({
                            'time': log_time,
                            'message': log['message'],
                            'request_id': log.get('request_id')
                        })
                    
                    # Track slow requests
                    if 'latency_ms' in log and log['latency_ms'] > 500:
                        stats['slow_requests'].append({
                            'time': log_time,
                            'endpoint': log.get('endpoint'),
                            'latency_ms': log['latency_ms']
                        })
                        
            except json.JSONDecodeError:
                continue
    
    # Print summary
    print(f"\\nLog Analysis Summary (last {hours} hours)")
    print("=" * 50)
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Errors: {stats['errors']} ({stats['errors']/stats['total_requests']*100:.1f}%)")
    print(f"\\nTop Endpoints:")
    for endpoint, count in sorted(stats['endpoints'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {endpoint}: {count}")
    
    if stats['slow_requests']:
        print(f"\\nSlow Requests: {len(stats['slow_requests'])}")
        df = pd.DataFrame(stats['slow_requests'])
        print(f"  Average latency: {df['latency_ms'].mean():.0f}ms")
        print(f"  Max latency: {df['latency_ms'].max():.0f}ms")
    
    return stats

if __name__ == "__main__":
    analyze_logs()
"""
    
    with open('scripts/analyze_logs.py', 'w') as f:
        f.write(log_analysis)
    
    # Metrics report script
    metrics_report = """#!/usr/bin/env python3
\"\"\"
Generate metrics report for FLASH platform
\"\"\"

import json
import glob
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def generate_report(metrics_dir='metrics', days=7):
    \"\"\"Generate metrics report\"\"\"
    
    # Load metrics files
    cutoff_time = datetime.now() - timedelta(days=days)
    metrics_data = []
    
    for file_path in glob.glob(f"{metrics_dir}/metrics_*.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            metrics_data.append(data)
    
    # Sort by timestamp
    metrics_data.sort(key=lambda x: x['timestamp'])
    
    # Extract time series data
    timestamps = []
    latencies = []
    success_rates = []
    request_rates = []
    
    for metric in metrics_data:
        timestamp = datetime.fromisoformat(metric['timestamp'])
        if timestamp > cutoff_time:
            timestamps.append(timestamp)
            latencies.append(metric['request_stats']['p95_latency_ms'])
            success_rates.append(metric['request_stats']['success_rate'])
            request_rates.append(metric['request_stats']['requests_per_minute'])
    
    # Create plots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Latency plot
    axes[0].plot(timestamps, latencies, 'b-')
    axes[0].set_ylabel('P95 Latency (ms)')
    axes[0].set_title('API Latency Trend')
    axes[0].grid(True, alpha=0.3)
    
    # Success rate plot
    axes[1].plot(timestamps, success_rates, 'g-')
    axes[1].set_ylabel('Success Rate')
    axes[1].set_title('API Success Rate')
    axes[1].set_ylim(0, 1.1)
    axes[1].grid(True, alpha=0.3)
    
    # Request rate plot
    axes[2].plot(timestamps, request_rates, 'r-')
    axes[2].set_ylabel('Requests/minute')
    axes[2].set_title('Request Rate')
    axes[2].set_xlabel('Time')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('metrics_report.png', dpi=150)
    print(f"✅ Metrics report saved to metrics_report.png")
    
    # Print summary
    print(f"\\nMetrics Summary (last {days} days)")
    print("=" * 50)
    print(f"Average P95 Latency: {sum(latencies)/len(latencies):.0f}ms")
    print(f"Average Success Rate: {sum(success_rates)/len(success_rates)*100:.1f}%")
    print(f"Average Request Rate: {sum(request_rates)/len(request_rates):.1f} req/min")

if __name__ == "__main__":
    generate_report()
"""
    
    os.makedirs('scripts', exist_ok=True)
    with open('scripts/generate_metrics_report.py', 'w') as f:
        f.write(metrics_report)
    
    print("✅ Created example monitoring scripts")

def create_monitoring_readme():
    """Create README for monitoring setup"""
    readme = """# FLASH Monitoring and Logging

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
"""
    
    with open('MONITORING_README.md', 'w') as f:
        f.write(readme)
    print("✅ Created MONITORING_README.md")

def main():
    """Main integration function"""
    print("=" * 60)
    print("FLASH Monitoring Integration")
    print("=" * 60)
    
    # Create configuration files
    create_monitoring_config()
    
    # Create example scripts
    create_example_scripts()
    
    # Create documentation
    create_monitoring_readme()
    
    print("\n✅ Monitoring integration complete!")
    print("\nTo integrate with api_server.py, add the following:")
    print("\n1. Imports:")
    print(add_monitoring_imports())
    print("\n2. After app creation:")
    print(add_monitoring_initialization())
    print("\n3. Add metrics endpoint:")
    print(add_metrics_endpoint())
    print("\n4. In prediction endpoint, add:")
    print(add_prediction_logging())
    print("\n5. Start the API server and access monitoring at:")
    print("   http://localhost:8000/monitoring")

if __name__ == "__main__":
    main()