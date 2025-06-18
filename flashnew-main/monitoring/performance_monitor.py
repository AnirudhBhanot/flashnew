#!/usr/bin/env python3
"""
Real-time Performance Monitoring for FLASH
KPI Impact: Maintain <200ms p99 latency, 99.9% uptime
"""

import time
import psutil
import json
from datetime import datetime, timedelta
from collections import deque, defaultdict
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and alert on system performance metrics"""
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.metrics = {
            'response_times': deque(maxlen=window_size),
            'prediction_scores': deque(maxlen=window_size),
            'error_counts': defaultdict(int),
            'feature_completeness': deque(maxlen=window_size),
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        self.alerts = []
        self.start_time = datetime.now()
        
    def record_prediction(self, 
                         response_time_ms: float,
                         prediction_score: float,
                         feature_count: int,
                         cache_hit: bool = False):
        """Record a prediction event"""
        self.metrics['response_times'].append(response_time_ms)
        self.metrics['prediction_scores'].append(prediction_score)
        self.metrics['feature_completeness'].append(feature_count / 45)  # 45 total features
        
        if cache_hit:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
            
        # Check for anomalies
        self._check_alerts(response_time_ms, prediction_score)
        
    def record_error(self, error_type: str):
        """Record an error event"""
        self.metrics['error_counts'][error_type] += 1
        
    def get_current_stats(self) -> Dict:
        """Get current performance statistics"""
        if not self.metrics['response_times']:
            return {'status': 'no_data'}
            
        response_times = list(self.metrics['response_times'])
        prediction_scores = list(self.metrics['prediction_scores'])
        
        # Calculate cache hit rate
        total_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = self.metrics['cache_hits'] / max(1, total_requests)
        
        stats = {
            'uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'total_predictions': len(response_times),
            'response_time': {
                'mean': np.mean(response_times),
                'p50': np.percentile(response_times, 50),
                'p95': np.percentile(response_times, 95),
                'p99': np.percentile(response_times, 99),
                'max': np.max(response_times)
            },
            'prediction_distribution': {
                'min': np.min(prediction_scores),
                'max': np.max(prediction_scores),
                'mean': np.mean(prediction_scores),
                'std': np.std(prediction_scores),
                'buckets': {
                    '0-20%': sum(1 for p in prediction_scores if p < 0.2) / len(prediction_scores),
                    '20-40%': sum(1 for p in prediction_scores if 0.2 <= p < 0.4) / len(prediction_scores),
                    '40-60%': sum(1 for p in prediction_scores if 0.4 <= p < 0.6) / len(prediction_scores),
                    '60-80%': sum(1 for p in prediction_scores if 0.6 <= p < 0.8) / len(prediction_scores),
                    '80-100%': sum(1 for p in prediction_scores if p >= 0.8) / len(prediction_scores),
                }
            },
            'cache_performance': {
                'hit_rate': cache_hit_rate,
                'total_hits': self.metrics['cache_hits'],
                'total_misses': self.metrics['cache_misses']
            },
            'error_rate': sum(self.metrics['error_counts'].values()) / max(1, total_requests),
            'errors_by_type': dict(self.metrics['error_counts']),
            'data_quality': {
                'avg_feature_completeness': np.mean(list(self.metrics['feature_completeness'])),
                'min_feature_completeness': np.min(list(self.metrics['feature_completeness']))
            },
            'system_resources': self._get_system_resources(),
            'active_alerts': self.alerts[-10:]  # Last 10 alerts
        }
        
        return stats
        
    def _check_alerts(self, response_time_ms: float, prediction_score: float):
        """Check for performance anomalies and generate alerts"""
        alerts = []
        
        # Response time alerts
        if response_time_ms > 500:
            alerts.append({
                'type': 'high_latency',
                'severity': 'critical' if response_time_ms > 1000 else 'warning',
                'message': f'Response time {response_time_ms:.0f}ms exceeds threshold',
                'timestamp': datetime.now().isoformat()
            })
            
        # Prediction distribution alerts
        recent_scores = list(self.metrics['prediction_scores'])[-100:]
        if len(recent_scores) >= 100:
            # Check if predictions are stuck in narrow range
            score_std = np.std(recent_scores)
            if score_std < 0.05:
                alerts.append({
                    'type': 'narrow_prediction_range',
                    'severity': 'warning',
                    'message': f'Predictions stuck in narrow range (std={score_std:.3f})',
                    'timestamp': datetime.now().isoformat()
                })
                
        # Error rate alerts
        total_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total_requests > 100:
            error_rate = sum(self.metrics['error_counts'].values()) / total_requests
            if error_rate > 0.05:
                alerts.append({
                    'type': 'high_error_rate',
                    'severity': 'critical',
                    'message': f'Error rate {error_rate:.1%} exceeds 5% threshold',
                    'timestamp': datetime.now().isoformat()
                })
                
        self.alerts.extend(alerts)
        
    def _get_system_resources(self) -> Dict:
        """Get current system resource usage"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage_percent': psutil.disk_usage('/').percent
        }
        
    def export_metrics(self, filepath: str = "metrics/performance_report.json"):
        """Export detailed metrics report"""
        Path(filepath).parent.mkdir(exist_ok=True)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'performance_stats': self.get_current_stats(),
            'sla_compliance': self._calculate_sla_compliance(),
            'recommendations': self._generate_recommendations()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
            
        logger.info(f"Performance report exported to {filepath}")
        
    def _calculate_sla_compliance(self) -> Dict:
        """Calculate SLA compliance metrics"""
        if not self.metrics['response_times']:
            return {'status': 'no_data'}
            
        response_times = list(self.metrics['response_times'])
        total_requests = len(response_times)
        
        return {
            'latency_sla': {
                'target': '<200ms p99',
                'actual': f"{np.percentile(response_times, 99):.0f}ms",
                'compliant': np.percentile(response_times, 99) < 200
            },
            'availability_sla': {
                'target': '99.9%',
                'actual': f"{(1 - sum(self.metrics['error_counts'].values()) / max(1, total_requests)) * 100:.2f}%",
                'compliant': sum(self.metrics['error_counts'].values()) / max(1, total_requests) < 0.001
            },
            'accuracy_sla': {
                'target': 'Full 0-100% range',
                'actual': f"{np.min(list(self.metrics['prediction_scores'])):.1%} - {np.max(list(self.metrics['prediction_scores'])):.1%}",
                'compliant': np.ptp(list(self.metrics['prediction_scores'])) > 0.7
            }
        }
        
    def _generate_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        stats = self.get_current_stats()
        
        # Latency recommendations
        if stats['response_time']['p99'] > 200:
            recommendations.append(
                f"High p99 latency ({stats['response_time']['p99']:.0f}ms). "
                "Consider: 1) Enabling Redis cache, 2) Optimizing feature engineering, "
                "3) Using model quantization"
            )
            
        # Cache recommendations
        if stats['cache_performance']['hit_rate'] < 0.5:
            recommendations.append(
                f"Low cache hit rate ({stats['cache_performance']['hit_rate']:.1%}). "
                "Consider: 1) Increasing cache TTL, 2) Pre-warming cache for common queries"
            )
            
        # Error recommendations
        if stats['error_rate'] > 0.01:
            top_error = max(stats['errors_by_type'].items(), key=lambda x: x[1])[0]
            recommendations.append(
                f"High error rate ({stats['error_rate']:.1%}), mostly '{top_error}'. "
                "Review error logs and add input validation"
            )
            
        # Distribution recommendations
        dist = stats['prediction_distribution']
        if dist['std'] < 0.1:
            recommendations.append(
                "Narrow prediction distribution. Check if models need recalibration"
            )
            
        return recommendations


# Global monitor instance
performance_monitor = PerformanceMonitor()


def create_dashboard_html(stats: Dict) -> str:
    """Create HTML dashboard for performance metrics"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FLASH Performance Dashboard</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{ font-family: -apple-system, Arial; background: #0a0a0c; color: #fff; padding: 20px; }}
            .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .metric-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
                          border-radius: 12px; padding: 20px; }}
            .metric-value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
            .good {{ color: #00C851; }}
            .warning {{ color: #FF8800; }}
            .bad {{ color: #FF4444; }}
            .chart {{ height: 100px; background: rgba(255,255,255,0.03); border-radius: 8px; 
                     display: flex; align-items: flex-end; padding: 10px; gap: 2px; }}
            .bar {{ background: #007AFF; border-radius: 2px; flex: 1; }}
        </style>
    </head>
    <body>
        <h1>FLASH Performance Dashboard</h1>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="metric-grid">
            <div class="metric-card">
                <h3>Response Time (p99)</h3>
                <div class="metric-value {('good' if stats['response_time']['p99'] < 200 else 'bad')}">
                    {stats['response_time']['p99']:.0f}ms
                </div>
                <small>Target: <200ms</small>
            </div>
            
            <div class="metric-card">
                <h3>Prediction Range</h3>
                <div class="metric-value good">
                    {stats['prediction_distribution']['min']:.1%} - {stats['prediction_distribution']['max']:.1%}
                </div>
                <small>Target: 0-100%</small>
            </div>
            
            <div class="metric-card">
                <h3>Cache Hit Rate</h3>
                <div class="metric-value {('good' if stats['cache_performance']['hit_rate'] > 0.7 else 'warning')}">
                    {stats['cache_performance']['hit_rate']:.1%}
                </div>
                <small>Total: {stats['cache_performance']['total_hits'] + stats['cache_performance']['total_misses']} requests</small>
            </div>
            
            <div class="metric-card">
                <h3>Error Rate</h3>
                <div class="metric-value {('good' if stats['error_rate'] < 0.01 else 'bad')}">
                    {stats['error_rate']:.2%}
                </div>
                <small>Target: <1%</small>
            </div>
            
            <div class="metric-card">
                <h3>Prediction Distribution</h3>
                <div class="chart">
                    <div class="bar" style="height: {stats['prediction_distribution']['buckets']['0-20%']*100}%"></div>
                    <div class="bar" style="height: {stats['prediction_distribution']['buckets']['20-40%']*100}%"></div>
                    <div class="bar" style="height: {stats['prediction_distribution']['buckets']['40-60%']*100}%"></div>
                    <div class="bar" style="height: {stats['prediction_distribution']['buckets']['60-80%']*100}%"></div>
                    <div class="bar" style="height: {stats['prediction_distribution']['buckets']['80-100%']*100}%"></div>
                </div>
                <small>0-20% | 20-40% | 40-60% | 60-80% | 80-100%</small>
            </div>
            
            <div class="metric-card">
                <h3>System Resources</h3>
                <div>CPU: {stats['system_resources']['cpu_percent']:.1f}%</div>
                <div>Memory: {stats['system_resources']['memory_percent']:.1f}%</div>
                <div>Disk: {stats['system_resources']['disk_usage_percent']:.1f}%</div>
            </div>
        </div>
        
        <h2>Recent Alerts</h2>
        <ul>
            {''.join(f"<li class='{alert['severity']}'>[{alert['timestamp']}] {alert['message']}</li>" 
                     for alert in stats.get('active_alerts', [])[-5:])}
        </ul>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Demo monitoring
    import random
    
    print("Simulating performance monitoring...")
    
    # Simulate some predictions
    for i in range(100):
        # Simulate varying performance
        response_time = random.gauss(150, 50)
        prediction = random.betavariate(2, 2)  # Tends toward middle
        features = random.randint(20, 45)
        cache_hit = random.random() > 0.3
        
        performance_monitor.record_prediction(
            response_time_ms=max(10, response_time),
            prediction_score=prediction,
            feature_count=features,
            cache_hit=cache_hit
        )
        
        # Simulate occasional errors
        if random.random() < 0.02:
            performance_monitor.record_error('validation_error')
            
    # Get stats
    stats = performance_monitor.get_current_stats()
    
    # Print summary
    print("\nPerformance Summary:")
    print(f"  Response Time (p99): {stats['response_time']['p99']:.0f}ms")
    print(f"  Prediction Range: {stats['prediction_distribution']['min']:.1%} - {stats['prediction_distribution']['max']:.1%}")
    print(f"  Cache Hit Rate: {stats['cache_performance']['hit_rate']:.1%}")
    print(f"  Error Rate: {stats['error_rate']:.2%}")
    
    # Export report
    performance_monitor.export_metrics()
    
    # Create dashboard
    with open('metrics/dashboard.html', 'w') as f:
        f.write(create_dashboard_html(stats))
    print("\nDashboard created at metrics/dashboard.html")