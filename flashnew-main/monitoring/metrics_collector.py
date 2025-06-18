"""
Metrics collection and monitoring for FLASH Platform
"""
import time
import psutil
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from collections import defaultdict, deque
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect and store application metrics"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics = {
            "requests": defaultdict(lambda: deque(maxlen=max_history)),
            "predictions": defaultdict(lambda: deque(maxlen=max_history)),
            "errors": defaultdict(lambda: deque(maxlen=max_history)),
            "system": defaultdict(lambda: deque(maxlen=max_history))
        }
        self.counters = defaultdict(int)
        self.start_time = time.time()
    
    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: float,
        request_id: str = None
    ):
        """Record API request metrics"""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "request_id": request_id
        }
        
        self.metrics["requests"]["all"].append(metric)
        self.metrics["requests"][endpoint].append(metric)
        
        # Update counters
        self.counters["total_requests"] += 1
        self.counters[f"requests_{endpoint}"] += 1
        self.counters[f"status_{status_code}"] += 1
        
        # Track response time percentiles
        self._update_percentiles("response_time", response_time_ms)
    
    def record_prediction(
        self,
        success_probability: float,
        confidence_score: float,
        verdict: str,
        processing_time_ms: float,
        model_version: str = None,
        pattern_detected: str = None
    ):
        """Record prediction metrics"""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "success_probability": success_probability,
            "confidence_score": confidence_score,
            "verdict": verdict,
            "processing_time_ms": processing_time_ms,
            "model_version": model_version,
            "pattern_detected": pattern_detected
        }
        
        self.metrics["predictions"]["all"].append(metric)
        self.metrics["predictions"][verdict].append(metric)
        
        # Update counters
        self.counters["total_predictions"] += 1
        self.counters[f"verdict_{verdict}"] += 1
        
        # Track prediction distribution
        prob_bucket = int(success_probability * 10) * 10
        self.counters[f"prob_bucket_{prob_bucket}"] += 1
    
    def record_error(
        self,
        error_type: str,
        error_message: str,
        endpoint: str = None,
        traceback: str = None
    ):
        """Record error metrics"""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "endpoint": endpoint,
            "traceback": traceback
        }
        
        self.metrics["errors"]["all"].append(metric)
        self.metrics["errors"][error_type].append(metric)
        
        # Update counters
        self.counters["total_errors"] += 1
        self.counters[f"error_{error_type}"] += 1
    
    def record_system_metrics(self):
        """Record system resource metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            
            metric = {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_mb": memory.used / 1024 / 1024,
                "memory_available_mb": memory.available / 1024 / 1024,
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / 1024 / 1024 / 1024,
                "process_memory_mb": process_memory.rss / 1024 / 1024,
                "process_cpu_percent": process.cpu_percent()
            }
            
            self.metrics["system"]["resources"].append(metric)
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    def _update_percentiles(self, metric_name: str, value: float):
        """Update percentile calculations for a metric"""
        key = f"{metric_name}_values"
        if key not in self.metrics:
            self.metrics[key] = deque(maxlen=self.max_history)
        self.metrics[key].append(value)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        uptime_seconds = time.time() - self.start_time
        
        # Calculate response time percentiles
        response_times = list(self.metrics.get("response_time_values", []))
        percentiles = {}
        if response_times:
            response_times.sort()
            percentiles = {
                "p50": response_times[len(response_times) // 2],
                "p95": response_times[int(len(response_times) * 0.95)],
                "p99": response_times[int(len(response_times) * 0.99)]
            }
        
        # Get latest system metrics
        latest_system = {}
        if self.metrics["system"]["resources"]:
            latest_system = self.metrics["system"]["resources"][-1]
        
        return {
            "uptime_seconds": uptime_seconds,
            "total_requests": self.counters["total_requests"],
            "total_predictions": self.counters["total_predictions"],
            "total_errors": self.counters["total_errors"],
            "requests_per_second": self.counters["total_requests"] / uptime_seconds,
            "predictions_per_second": self.counters["total_predictions"] / uptime_seconds,
            "error_rate": self.counters["total_errors"] / max(self.counters["total_requests"], 1),
            "response_time_percentiles": percentiles,
            "verdict_distribution": {
                "PASS": self.counters.get("verdict_PASS", 0),
                "CONDITIONAL PASS": self.counters.get("verdict_CONDITIONAL PASS", 0),
                "FAIL": self.counters.get("verdict_FAIL", 0)
            },
            "system_metrics": latest_system,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def export_metrics(self, filepath: str = "metrics_export.json"):
        """Export metrics to file"""
        try:
            export_data = {
                "summary": self.get_summary(),
                "counters": dict(self.counters),
                "recent_requests": list(self.metrics["requests"]["all"])[-100:],
                "recent_predictions": list(self.metrics["predictions"]["all"])[-100:],
                "recent_errors": list(self.metrics["errors"]["all"])[-50:]
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Metrics exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return False


# Global metrics collector instance
metrics_collector = MetricsCollector()


# Prometheus metrics (if prometheus_client is available)
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest
    
    # Define Prometheus metrics
    request_count = Counter(
        'flash_requests_total',
        'Total number of requests',
        ['method', 'endpoint', 'status']
    )
    
    request_duration = Histogram(
        'flash_request_duration_seconds',
        'Request duration in seconds',
        ['method', 'endpoint']
    )
    
    prediction_count = Counter(
        'flash_predictions_total',
        'Total number of predictions',
        ['verdict', 'model_version']
    )
    
    prediction_probability = Histogram(
        'flash_prediction_probability',
        'Prediction probability distribution',
        buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    )
    
    error_count = Counter(
        'flash_errors_total',
        'Total number of errors',
        ['error_type', 'endpoint']
    )
    
    # System metrics
    cpu_usage = Gauge('flash_cpu_usage_percent', 'CPU usage percentage')
    memory_usage = Gauge('flash_memory_usage_bytes', 'Memory usage in bytes')
    
    PROMETHEUS_ENABLED = True
    
except ImportError:
    PROMETHEUS_ENABLED = False
    logger.info("Prometheus client not available, metrics will be stored locally only")


def record_prometheus_request(method: str, endpoint: str, status: int, duration: float):
    """Record request metrics in Prometheus format"""
    if PROMETHEUS_ENABLED:
        request_count.labels(method=method, endpoint=endpoint, status=str(status)).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)


def record_prometheus_prediction(verdict: str, probability: float, model_version: str = "unknown"):
    """Record prediction metrics in Prometheus format"""
    if PROMETHEUS_ENABLED:
        prediction_count.labels(verdict=verdict, model_version=model_version).inc()
        prediction_probability.observe(probability)


def record_prometheus_error(error_type: str, endpoint: str = "unknown"):
    """Record error metrics in Prometheus format"""
    if PROMETHEUS_ENABLED:
        error_count.labels(error_type=error_type, endpoint=endpoint).inc()


def update_prometheus_system_metrics():
    """Update system metrics for Prometheus"""
    if PROMETHEUS_ENABLED:
        try:
            cpu_usage.set(psutil.cpu_percent())
            memory_usage.set(psutil.virtual_memory().used)
        except Exception as e:
            logger.error(f"Failed to update Prometheus system metrics: {e}")


def get_prometheus_metrics():
    """Get metrics in Prometheus format"""
    if PROMETHEUS_ENABLED:
        return generate_latest()
    return b""