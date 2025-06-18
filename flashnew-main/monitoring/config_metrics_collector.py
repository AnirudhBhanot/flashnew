"""
Configuration Metrics Collector
Tracks configuration usage, changes, and performance
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict
import asyncio
import redis
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import logging

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
    'Configuration fetch latency',
    ['config_key']
)

config_cache_hit_rate = Gauge(
    'flash_config_cache_hit_rate',
    'Cache hit rate for configurations',
    ['time_window']
)

config_change_counter = Counter(
    'flash_config_changes_total',
    'Total configuration changes',
    ['config_key', 'change_type']
)

ab_test_exposure_counter = Counter(
    'flash_ab_test_exposures_total',
    'A/B test exposures',
    ['test_name', 'variant']
)

ab_test_conversion_rate = Gauge(
    'flash_ab_test_conversion_rate',
    'A/B test conversion rates',
    ['test_name', 'variant']
)

# Database setup
Base = declarative_base()
DATABASE_URL = "sqlite:///./config_metrics.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class ConfigMetric(Base):
    __tablename__ = "config_metrics"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    config_key = Column(String, index=True)
    access_count = Column(Integer, default=0)
    cache_hits = Column(Integer, default=0)
    cache_misses = Column(Integer, default=0)
    avg_latency_ms = Column(Float, default=0)
    unique_users = Column(Integer, default=0)

class ConfigChangeMetric(Base):
    __tablename__ = "config_change_metrics"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    config_key = Column(String, index=True)
    changed_by = Column(String)
    change_type = Column(String)  # create, update, rollback
    old_value_hash = Column(String)
    new_value_hash = Column(String)

class ABTestMetric(Base):
    __tablename__ = "ab_test_metrics"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    test_name = Column(String, index=True)
    variant = Column(String)
    exposures = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0)
    user_segments = Column(JSON)

Base.metadata.create_all(bind=engine)

class MetricsCollector:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None
        self.metrics_buffer = defaultdict(lambda: {
            'access_count': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'latencies': [],
            'users': set()
        })
        self.ab_test_buffer = defaultdict(lambda: defaultdict(lambda: {
            'exposures': 0,
            'conversions': 0,
            'revenue': 0.0
        }))
        
    async def connect(self):
        """Connect to Redis for real-time metrics"""
        self.redis = await aioredis.from_url(self.redis_url)
        
    async def track_config_access(self, config_key: str, user_id: str, 
                                 cache_hit: bool, latency_ms: float):
        """Track configuration access metrics"""
        # Update Prometheus metrics
        config_access_counter.labels(
            config_key=config_key,
            user_type='authenticated' if user_id else 'anonymous'
        ).inc()
        
        config_latency_histogram.labels(config_key=config_key).observe(latency_ms / 1000)
        
        # Buffer metrics for batch processing
        self.metrics_buffer[config_key]['access_count'] += 1
        if cache_hit:
            self.metrics_buffer[config_key]['cache_hits'] += 1
        else:
            self.metrics_buffer[config_key]['cache_misses'] += 1
        self.metrics_buffer[config_key]['latencies'].append(latency_ms)
        if user_id:
            self.metrics_buffer[config_key]['users'].add(user_id)
        
        # Store in Redis for real-time dashboard
        await self.redis.hincrby(f"config:access:{config_key}", "total", 1)
        await self.redis.hincrby(f"config:access:{config_key}", 
                                "cache_hits" if cache_hit else "cache_misses", 1)
        
    async def track_config_change(self, config_key: str, changed_by: str,
                                 change_type: str, old_value: Any, new_value: Any):
        """Track configuration changes"""
        config_change_counter.labels(
            config_key=config_key,
            change_type=change_type
        ).inc()
        
        # Store change metric
        db = SessionLocal()
        change_metric = ConfigChangeMetric(
            config_key=config_key,
            changed_by=changed_by,
            change_type=change_type,
            old_value_hash=self._hash_value(old_value),
            new_value_hash=self._hash_value(new_value)
        )
        db.add(change_metric)
        db.commit()
        db.close()
        
        # Alert on critical changes
        if config_key in ['success-thresholds', 'model-weights']:
            await self._send_alert(f"Critical configuration changed: {config_key}")
        
    async def track_ab_test_event(self, test_name: str, variant: str,
                                 event_type: str, user_id: str, value: float = 0):
        """Track A/B test events"""
        if event_type == 'exposure':
            ab_test_exposure_counter.labels(
                test_name=test_name,
                variant=variant
            ).inc()
            self.ab_test_buffer[test_name][variant]['exposures'] += 1
            
        elif event_type == 'conversion':
            self.ab_test_buffer[test_name][variant]['conversions'] += 1
            self.ab_test_buffer[test_name][variant]['revenue'] += value
            
        # Store in Redis
        await self.redis.hincrby(f"ab:test:{test_name}:{variant}", event_type, 1)
        if value > 0:
            await self.redis.hincrbyfloat(f"ab:test:{test_name}:{variant}", "revenue", value)
            
    async def flush_metrics(self):
        """Flush buffered metrics to database"""
        db = SessionLocal()
        
        # Process configuration metrics
        for config_key, metrics in self.metrics_buffer.items():
            if metrics['access_count'] > 0:
                avg_latency = sum(metrics['latencies']) / len(metrics['latencies']) if metrics['latencies'] else 0
                
                config_metric = ConfigMetric(
                    config_key=config_key,
                    access_count=metrics['access_count'],
                    cache_hits=metrics['cache_hits'],
                    cache_misses=metrics['cache_misses'],
                    avg_latency_ms=avg_latency,
                    unique_users=len(metrics['users'])
                )
                db.add(config_metric)
                
                # Update cache hit rate gauge
                hit_rate = metrics['cache_hits'] / metrics['access_count'] if metrics['access_count'] > 0 else 0
                config_cache_hit_rate.labels(time_window='1m').set(hit_rate)
        
        # Process A/B test metrics
        for test_name, variants in self.ab_test_buffer.items():
            for variant, metrics in variants.items():
                if metrics['exposures'] > 0:
                    ab_metric = ABTestMetric(
                        test_name=test_name,
                        variant=variant,
                        exposures=metrics['exposures'],
                        conversions=metrics['conversions'],
                        revenue=metrics['revenue']
                    )
                    db.add(ab_metric)
                    
                    # Update conversion rate gauge
                    conversion_rate = metrics['conversions'] / metrics['exposures'] if metrics['exposures'] > 0 else 0
                    ab_test_conversion_rate.labels(
                        test_name=test_name,
                        variant=variant
                    ).set(conversion_rate)
        
        db.commit()
        db.close()
        
        # Clear buffers
        self.metrics_buffer.clear()
        self.ab_test_buffer.clear()
        
    async def get_config_analytics(self, config_key: str, hours: int = 24) -> Dict:
        """Get analytics for a specific configuration"""
        db = SessionLocal()
        since = datetime.utcnow() - timedelta(hours=hours)
        
        metrics = db.query(ConfigMetric).filter(
            ConfigMetric.config_key == config_key,
            ConfigMetric.timestamp >= since
        ).all()
        
        changes = db.query(ConfigChangeMetric).filter(
            ConfigChangeMetric.config_key == config_key,
            ConfigChangeMetric.timestamp >= since
        ).all()
        
        db.close()
        
        # Calculate aggregates
        total_access = sum(m.access_count for m in metrics)
        total_cache_hits = sum(m.cache_hits for m in metrics)
        cache_hit_rate = total_cache_hits / total_access if total_access > 0 else 0
        avg_latency = sum(m.avg_latency_ms * m.access_count for m in metrics) / total_access if total_access > 0 else 0
        unique_users = sum(m.unique_users for m in metrics)
        
        return {
            'config_key': config_key,
            'period_hours': hours,
            'total_access': total_access,
            'cache_hit_rate': cache_hit_rate,
            'avg_latency_ms': avg_latency,
            'unique_users': unique_users,
            'changes': len(changes),
            'access_trend': [
                {
                    'timestamp': m.timestamp.isoformat(),
                    'access_count': m.access_count,
                    'cache_hit_rate': m.cache_hits / m.access_count if m.access_count > 0 else 0
                }
                for m in sorted(metrics, key=lambda x: x.timestamp)
            ]
        }
        
    async def get_ab_test_results(self, test_name: str) -> Dict:
        """Get A/B test results and statistics"""
        db = SessionLocal()
        
        metrics = db.query(ABTestMetric).filter(
            ABTestMetric.test_name == test_name
        ).all()
        
        db.close()
        
        # Aggregate by variant
        results = defaultdict(lambda: {
            'exposures': 0,
            'conversions': 0,
            'revenue': 0.0
        })
        
        for metric in metrics:
            results[metric.variant]['exposures'] += metric.exposures
            results[metric.variant]['conversions'] += metric.conversions
            results[metric.variant]['revenue'] += metric.revenue
        
        # Calculate statistics
        test_results = {}
        for variant, data in results.items():
            conversion_rate = data['conversions'] / data['exposures'] if data['exposures'] > 0 else 0
            avg_revenue = data['revenue'] / data['conversions'] if data['conversions'] > 0 else 0
            
            test_results[variant] = {
                'exposures': data['exposures'],
                'conversions': data['conversions'],
                'conversion_rate': conversion_rate,
                'total_revenue': data['revenue'],
                'avg_revenue_per_conversion': avg_revenue
            }
        
        # Calculate statistical significance if we have 2 variants
        if len(test_results) == 2:
            variants = list(test_results.keys())
            control = test_results[variants[0]]
            treatment = test_results[variants[1]]
            
            # Simple z-test for conversion rate
            p1 = control['conversion_rate']
            p2 = treatment['conversion_rate']
            n1 = control['exposures']
            n2 = treatment['exposures']
            
            if n1 > 0 and n2 > 0:
                p_pooled = (control['conversions'] + treatment['conversions']) / (n1 + n2)
                se = ((p_pooled * (1 - p_pooled)) * (1/n1 + 1/n2)) ** 0.5
                z_score = (p2 - p1) / se if se > 0 else 0
                
                # Two-tailed test at 95% confidence
                is_significant = abs(z_score) > 1.96
                
                test_results['statistical_significance'] = {
                    'z_score': z_score,
                    'is_significant': is_significant,
                    'confidence_level': 0.95
                }
        
        return {
            'test_name': test_name,
            'variants': test_results
        }
        
    def _hash_value(self, value: Any) -> str:
        """Hash configuration value for comparison"""
        import hashlib
        return hashlib.md5(json.dumps(value, sort_keys=True).encode()).hexdigest()
        
    async def _send_alert(self, message: str):
        """Send alert for critical events"""
        # In production, integrate with Slack, PagerDuty, etc.
        logger.warning(f"ALERT: {message}")
        
    async def run_collector(self, flush_interval: int = 60):
        """Run the metrics collector with periodic flushing"""
        await self.connect()
        
        while True:
            await asyncio.sleep(flush_interval)
            await self.flush_metrics()

# FastAPI endpoints for metrics dashboard
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

metrics_app = FastAPI(title="Configuration Metrics API")

collector = MetricsCollector()

@metrics_app.on_event("startup")
async def startup():
    await collector.connect()
    # Start Prometheus metrics server
    start_http_server(9090)
    # Start background collector
    asyncio.create_task(collector.run_collector())

@metrics_app.get("/metrics/config/{config_key}")
async def get_config_metrics(
    config_key: str,
    hours: int = Query(24, description="Hours to look back")
):
    """Get metrics for a specific configuration"""
    return await collector.get_config_analytics(config_key, hours)

@metrics_app.get("/metrics/ab-test/{test_name}")
async def get_ab_test_metrics(test_name: str):
    """Get A/B test results"""
    return await collector.get_ab_test_results(test_name)

@metrics_app.get("/dashboard", response_class=HTMLResponse)
async def metrics_dashboard():
    """Simple HTML dashboard for metrics"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Configuration Metrics Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .metric-card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .metric-value { font-size: 2em; font-weight: bold; color: #007AFF; }
            .metric-label { color: #666; }
            .chart { margin: 20px 0; }
            h1 { color: #333; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Configuration Metrics Dashboard</h1>
        <div id="metrics-container"></div>
        
        <script>
            // Add your dashboard JavaScript here
            async function loadMetrics() {
                // Fetch and display metrics
                const configs = ['success-thresholds', 'model-weights', 'revenue-benchmarks'];
                
                for (const config of configs) {
                    const response = await fetch(`/metrics/config/${config}?hours=24`);
                    const data = await response.json();
                    displayMetric(data);
                }
            }
            
            function displayMetric(data) {
                const container = document.getElementById('metrics-container');
                const card = document.createElement('div');
                card.className = 'metric-card';
                card.innerHTML = `
                    <h3>${data.config_key}</h3>
                    <div class="grid">
                        <div>
                            <div class="metric-label">Total Access</div>
                            <div class="metric-value">${data.total_access}</div>
                        </div>
                        <div>
                            <div class="metric-label">Cache Hit Rate</div>
                            <div class="metric-value">${(data.cache_hit_rate * 100).toFixed(1)}%</div>
                        </div>
                        <div>
                            <div class="metric-label">Avg Latency</div>
                            <div class="metric-value">${data.avg_latency_ms.toFixed(1)}ms</div>
                        </div>
                        <div>
                            <div class="metric-label">Unique Users</div>
                            <div class="metric-value">${data.unique_users}</div>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            }
            
            loadMetrics();
            setInterval(loadMetrics, 30000); // Refresh every 30 seconds
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(metrics_app, host="0.0.0.0", port=9091)