"""
Simple Configuration Metrics Collector
Tracks configuration usage without Redis dependency
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict
import asyncio
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
config_access_counter = Counter(
    'flash_config_access_total',
    'Total configuration access count',
    ['config_key', 'user_type']
)

config_latency_histogram = Histogram(
    'flash_config_latency_seconds',
    'Configuration access latency',
    ['config_key']
)

config_cache_hits = Counter(
    'flash_config_cache_hits_total',
    'Cache hit count',
    ['config_key']
)

config_changes_counter = Counter(
    'flash_config_changes_total',
    'Configuration changes',
    ['config_key', 'change_type']
)

ab_test_metrics = Gauge(
    'flash_ab_test_conversion_rate',
    'A/B test conversion rates',
    ['test_name', 'variant']
)

# In-memory storage for metrics
metrics_storage = defaultdict(lambda: {
    'access_count': 0,
    'unique_users': set(),
    'cache_hits': 0,
    'total_latency': 0,
    'changes': []
})

# FastAPI app
app = FastAPI(title="Configuration Metrics API")

class AccessMetric(BaseModel):
    config_key: str
    user_id: str
    cache_hit: bool
    latency_ms: float

@app.post("/track/access")
async def track_access(metric: AccessMetric):
    """Track configuration access"""
    # Update Prometheus metrics
    config_access_counter.labels(
        config_key=metric.config_key,
        user_type='authenticated' if metric.user_id else 'anonymous'
    ).inc()
    
    config_latency_histogram.labels(config_key=metric.config_key).observe(metric.latency_ms / 1000)
    
    if metric.cache_hit:
        config_cache_hits.labels(config_key=metric.config_key).inc()
    
    # Update in-memory storage
    storage = metrics_storage[metric.config_key]
    storage['access_count'] += 1
    storage['unique_users'].add(metric.user_id)
    storage['cache_hits'] += 1 if metric.cache_hit else 0
    storage['total_latency'] += metric.latency_ms
    
    return {"status": "tracked"}

@app.get("/metrics/{config_key}")
async def get_metrics(config_key: str, hours: int = 24):
    """Get metrics for a specific configuration"""
    storage = metrics_storage.get(config_key)
    
    if not storage:
        raise HTTPException(status_code=404, detail="No metrics found")
    
    avg_latency = storage['total_latency'] / storage['access_count'] if storage['access_count'] > 0 else 0
    
    return {
        "config_key": config_key,
        "period_hours": hours,
        "access_count": storage['access_count'],
        "unique_users": len(storage['unique_users']),
        "cache_hit_rate": storage['cache_hits'] / storage['access_count'] if storage['access_count'] > 0 else 0,
        "average_latency_ms": avg_latency,
        "changes": len(storage['changes'])
    }

@app.get("/dashboard")
async def metrics_dashboard():
    """Simple metrics dashboard data"""
    dashboard_data = {
        "total_accesses": sum(m['access_count'] for m in metrics_storage.values()),
        "total_unique_users": len(set().union(*[m['unique_users'] for m in metrics_storage.values() if m['unique_users']])),
        "configurations": []
    }
    
    for key, metrics in metrics_storage.items():
        if metrics['access_count'] > 0:
            dashboard_data['configurations'].append({
                "key": key,
                "accesses": metrics['access_count'],
                "users": len(metrics['unique_users']),
                "cache_hit_rate": metrics['cache_hits'] / metrics['access_count']
            })
    
    return dashboard_data

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    # Start Prometheus metrics server
    start_http_server(9090)
    logger.info("Prometheus metrics server started on port 9090")
    
    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=9091)