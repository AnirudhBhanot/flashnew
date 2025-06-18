"""
Model Performance Monitoring and A/B Testing System
Real-time monitoring, alerting, and experimental framework
"""

import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import threading
import time
from scipy import stats

logger = logging.getLogger(__name__)


@dataclass
class PredictionMetrics:
    """Metrics for a single prediction"""
    timestamp: str
    model_version: str
    prediction: float
    confidence: float
    latency_ms: float
    features_hash: str
    actual_outcome: Optional[float] = None
    feedback_timestamp: Optional[str] = None


@dataclass
class PerformanceAlert:
    """Performance alert details"""
    alert_id: str
    alert_type: str  # 'degradation', 'latency', 'error_rate', 'drift'
    severity: str  # 'low', 'medium', 'high', 'critical'
    model_type: str
    model_version: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: str
    resolved: bool = False
    resolution_timestamp: Optional[str] = None


class ModelPerformanceMonitor:
    """
    Comprehensive model performance monitoring system
    Features:
    - Real-time performance tracking
    - Statistical drift detection
    - A/B testing framework
    - Automated alerting
    - Performance dashboards
    """
    
    def __init__(self, monitoring_dir: str = "monitoring"):
        self.monitoring_dir = Path(monitoring_dir)
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_file = self.monitoring_dir / "performance_metrics.json"
        self.alerts_file = self.monitoring_dir / "alerts.json"
        self.experiments_file = self.monitoring_dir / "experiments.json"
        
        self.metrics_buffer = []
        self.alerts = self._load_alerts()
        self.experiments = self._load_experiments()
        
        self.thresholds = {
            "latency_ms": {"warning": 100, "critical": 200},
            "error_rate": {"warning": 0.05, "critical": 0.10},
            "accuracy_drop": {"warning": 0.05, "critical": 0.10},
            "confidence_drop": {"warning": 0.10, "critical": 0.20}
        }
        
        # Start monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def _load_alerts(self) -> List[PerformanceAlert]:
        """Load existing alerts"""
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                data = json.load(f)
                return [PerformanceAlert(**alert) for alert in data]
        return []
    
    def _load_experiments(self) -> Dict:
        """Load A/B test experiments"""
        if self.experiments_file.exists():
            with open(self.experiments_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_alerts(self):
        """Save alerts to file"""
        with open(self.alerts_file, 'w') as f:
            json.dump([asdict(alert) for alert in self.alerts], f, indent=2)
    
    def _save_experiments(self):
        """Save experiments to file"""
        with open(self.experiments_file, 'w') as f:
            json.dump(self.experiments, f, indent=2)
    
    def record_prediction(self, model_type: str, model_version: str,
                         prediction: float, confidence: float,
                         latency_ms: float, features: Dict[str, Any]):
        """Record a prediction for monitoring"""
        
        # Create feature hash for tracking
        features_str = json.dumps(features, sort_keys=True)
        features_hash = str(hash(features_str))
        
        metric = PredictionMetrics(
            timestamp=datetime.now().isoformat(),
            model_version=f"{model_type}_{model_version}",
            prediction=prediction,
            confidence=confidence,
            latency_ms=latency_ms,
            features_hash=features_hash
        )
        
        self.metrics_buffer.append(metric)
        
        # Check for immediate alerts
        self._check_latency_alert(model_type, model_version, latency_ms)
        self._check_confidence_alert(model_type, model_version, confidence)
        
        # Flush buffer if large
        if len(self.metrics_buffer) > 1000:
            self._flush_metrics()
    
    def record_feedback(self, features_hash: str, actual_outcome: float):
        """Record actual outcome for a prediction"""
        # Update metrics with feedback
        for metric in self.metrics_buffer:
            if metric.features_hash == features_hash and metric.actual_outcome is None:
                metric.actual_outcome = actual_outcome
                metric.feedback_timestamp = datetime.now().isoformat()
                break
    
    def _flush_metrics(self):
        """Flush metrics buffer to disk"""
        if not self.metrics_buffer:
            return
        
        # Append to daily metrics file
        date_str = datetime.now().strftime("%Y%m%d")
        daily_file = self.monitoring_dir / f"metrics_{date_str}.json"
        
        existing_metrics = []
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                existing_metrics = json.load(f)
        
        # Add new metrics
        existing_metrics.extend([asdict(m) for m in self.metrics_buffer])
        
        with open(daily_file, 'w') as f:
            json.dump(existing_metrics, f, indent=2)
        
        # Clear buffer
        self.metrics_buffer = []
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                # Flush metrics periodically
                self._flush_metrics()
                
                # Check for drift
                self._check_model_drift()
                
                # Update experiment statistics
                self._update_experiments()
                
                # Clean old data
                self._cleanup_old_data()
                
                time.sleep(60)  # Run every minute
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
    
    def _check_latency_alert(self, model_type: str, model_version: str, latency_ms: float):
        """Check if latency exceeds threshold"""
        thresholds = self.thresholds["latency_ms"]
        
        if latency_ms > thresholds["critical"]:
            self._create_alert(
                alert_type="latency",
                severity="critical",
                model_type=model_type,
                model_version=model_version,
                metric_name="latency_ms",
                current_value=latency_ms,
                threshold=thresholds["critical"]
            )
        elif latency_ms > thresholds["warning"]:
            self._create_alert(
                alert_type="latency",
                severity="medium",
                model_type=model_type,
                model_version=model_version,
                metric_name="latency_ms",
                current_value=latency_ms,
                threshold=thresholds["warning"]
            )
    
    def _check_confidence_alert(self, model_type: str, model_version: str, confidence: float):
        """Check if confidence is too low"""
        if confidence < 0.5:
            self._create_alert(
                alert_type="degradation",
                severity="high",
                model_type=model_type,
                model_version=model_version,
                metric_name="confidence",
                current_value=confidence,
                threshold=0.5
            )
    
    def _check_model_drift(self):
        """Check for model drift using recent predictions"""
        # Load recent metrics
        recent_metrics = self._load_recent_metrics(hours=24)
        
        if len(recent_metrics) < 100:
            return  # Not enough data
        
        # Group by model version
        model_metrics = defaultdict(list)
        for metric in recent_metrics:
            model_metrics[metric["model_version"]].append(metric)
        
        for model_version, metrics in model_metrics.items():
            # Check prediction distribution
            predictions = [m["prediction"] for m in metrics]
            confidences = [m["confidence"] for m in metrics]
            
            # Simple drift detection: check if distribution has shifted
            if len(predictions) > 1000:
                # Compare first half vs second half
                mid = len(predictions) // 2
                first_half = predictions[:mid]
                second_half = predictions[mid:]
                
                # Kolmogorov-Smirnov test for distribution change
                ks_stat, p_value = stats.ks_2samp(first_half, second_half)
                
                if p_value < 0.01:  # Significant drift
                    self._create_alert(
                        alert_type="drift",
                        severity="high",
                        model_type=model_version.split('_')[0],
                        model_version=model_version,
                        metric_name="prediction_distribution",
                        current_value=ks_stat,
                        threshold=0.01
                    )
    
    def _create_alert(self, **kwargs):
        """Create a new alert"""
        alert = PerformanceAlert(
            alert_id=f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.alerts)}",
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
        
        # Check if similar alert already exists and is unresolved
        for existing_alert in self.alerts:
            if (not existing_alert.resolved and
                existing_alert.alert_type == alert.alert_type and
                existing_alert.model_version == alert.model_version and
                existing_alert.metric_name == alert.metric_name):
                return  # Don't create duplicate alert
        
        self.alerts.append(alert)
        self._save_alerts()
        
        logger.warning(f"Alert created: {alert.alert_type} - {alert.model_version} - {alert.metric_name}")
    
    def resolve_alert(self, alert_id: str):
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolution_timestamp = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def _load_recent_metrics(self, hours: int = 24) -> List[Dict]:
        """Load recent metrics from files"""
        metrics = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Include buffer metrics
        metrics.extend([asdict(m) for m in self.metrics_buffer])
        
        # Load from daily files
        for i in range(hours // 24 + 1):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y%m%d")
            daily_file = self.monitoring_dir / f"metrics_{date_str}.json"
            
            if daily_file.exists():
                with open(daily_file, 'r') as f:
                    daily_metrics = json.load(f)
                    
                # Filter by time
                for metric in daily_metrics:
                    if datetime.fromisoformat(metric["timestamp"]) > cutoff_time:
                        metrics.append(metric)
        
        return metrics
    
    def create_ab_test(self, experiment_name: str, model_a: str, model_b: str,
                      traffic_split: float = 0.5, min_samples: int = 1000):
        """Create an A/B test experiment"""
        experiment = {
            "name": experiment_name,
            "model_a": model_a,
            "model_b": model_b,
            "traffic_split": traffic_split,
            "min_samples": min_samples,
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "metrics_a": {"count": 0, "predictions": [], "outcomes": []},
            "metrics_b": {"count": 0, "predictions": [], "outcomes": []},
            "results": {}
        }
        
        self.experiments[experiment_name] = experiment
        self._save_experiments()
        
        logger.info(f"Started A/B test: {experiment_name}")
    
    def record_ab_prediction(self, experiment_name: str, is_model_a: bool,
                           prediction: float, actual_outcome: Optional[float] = None):
        """Record prediction for A/B test"""
        if experiment_name not in self.experiments:
            return
        
        experiment = self.experiments[experiment_name]
        if experiment["status"] != "running":
            return
        
        # Record in appropriate bucket
        bucket = "metrics_a" if is_model_a else "metrics_b"
        experiment[bucket]["count"] += 1
        experiment[bucket]["predictions"].append(prediction)
        
        if actual_outcome is not None:
            experiment[bucket]["outcomes"].append(actual_outcome)
        
        self._save_experiments()
    
    def _update_experiments(self):
        """Update experiment statistics"""
        for exp_name, experiment in self.experiments.items():
            if experiment["status"] != "running":
                continue
            
            # Check if we have enough samples
            outcomes_a = len(experiment["metrics_a"]["outcomes"])
            outcomes_b = len(experiment["metrics_b"]["outcomes"])
            
            if outcomes_a >= experiment["min_samples"] and outcomes_b >= experiment["min_samples"]:
                # Calculate statistics
                results = self._calculate_ab_statistics(experiment)
                experiment["results"] = results
                
                # Determine winner if significant
                if results["p_value"] < 0.05:
                    if results["mean_a"] > results["mean_b"]:
                        experiment["winner"] = "model_a"
                    else:
                        experiment["winner"] = "model_b"
                    experiment["status"] = "completed"
                    experiment["completed_at"] = datetime.now().isoformat()
                    
                    logger.info(f"A/B test {exp_name} completed. Winner: {experiment['winner']}")
                
                self._save_experiments()
    
    def _calculate_ab_statistics(self, experiment: Dict) -> Dict:
        """Calculate A/B test statistics"""
        outcomes_a = experiment["metrics_a"]["outcomes"]
        outcomes_b = experiment["metrics_b"]["outcomes"]
        
        # Basic statistics
        mean_a = np.mean(outcomes_a)
        mean_b = np.mean(outcomes_b)
        std_a = np.std(outcomes_a)
        std_b = np.std(outcomes_b)
        
        # T-test
        t_stat, p_value = stats.ttest_ind(outcomes_a, outcomes_b)
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt((std_a**2 + std_b**2) / 2)
        effect_size = (mean_a - mean_b) / pooled_std if pooled_std > 0 else 0
        
        # Confidence intervals
        ci_a = stats.t.interval(0.95, len(outcomes_a)-1, mean_a, stats.sem(outcomes_a))
        ci_b = stats.t.interval(0.95, len(outcomes_b)-1, mean_b, stats.sem(outcomes_b))
        
        return {
            "mean_a": mean_a,
            "mean_b": mean_b,
            "std_a": std_a,
            "std_b": std_b,
            "t_statistic": t_stat,
            "p_value": p_value,
            "effect_size": effect_size,
            "ci_a": ci_a,
            "ci_b": ci_b,
            "relative_improvement": (mean_b - mean_a) / mean_a if mean_a > 0 else 0
        }
    
    def get_performance_summary(self, model_type: str = None, hours: int = 24) -> Dict:
        """Get performance summary for models"""
        metrics = self._load_recent_metrics(hours)
        
        if model_type:
            metrics = [m for m in metrics if model_type in m["model_version"]]
        
        if not metrics:
            return {"error": "No metrics found"}
        
        # Group by model version
        version_metrics = defaultdict(list)
        for metric in metrics:
            version_metrics[metric["model_version"]].append(metric)
        
        summary = {}
        for version, version_data in version_metrics.items():
            predictions = [m["prediction"] for m in version_data]
            confidences = [m["confidence"] for m in version_data]
            latencies = [m["latency_ms"] for m in version_data]
            
            # Get feedback metrics
            with_feedback = [m for m in version_data if m.get("actual_outcome") is not None]
            
            accuracy = None
            if with_feedback:
                correct = sum(1 for m in with_feedback 
                            if (m["prediction"] > 0.5) == (m["actual_outcome"] > 0.5))
                accuracy = correct / len(with_feedback)
            
            summary[version] = {
                "total_predictions": len(version_data),
                "avg_prediction": np.mean(predictions),
                "avg_confidence": np.mean(confidences),
                "avg_latency_ms": np.mean(latencies),
                "p95_latency_ms": np.percentile(latencies, 95),
                "accuracy": accuracy,
                "feedback_rate": len(with_feedback) / len(version_data) if version_data else 0
            }
        
        return summary
    
    def get_active_alerts(self) -> List[Dict]:
        """Get active (unresolved) alerts"""
        return [asdict(alert) for alert in self.alerts if not alert.resolved]
    
    def get_experiment_results(self, experiment_name: str = None) -> Dict:
        """Get experiment results"""
        if experiment_name:
            return self.experiments.get(experiment_name, {"error": "Experiment not found"})
        return self.experiments
    
    def _cleanup_old_data(self):
        """Clean up old monitoring data"""
        # Keep only last 30 days of metrics
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for file in self.monitoring_dir.glob("metrics_*.json"):
            try:
                date_str = file.stem.split('_')[1]
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                if file_date < cutoff_date:
                    file.unlink()
                    logger.info(f"Deleted old metrics file: {file.name}")
            except:
                pass
        
        # Archive old resolved alerts
        active_alerts = [a for a in self.alerts if not a.resolved or 
                        (a.resolved and datetime.fromisoformat(a.resolution_timestamp) > cutoff_date)]
        
        if len(active_alerts) < len(self.alerts):
            self.alerts = active_alerts
            self._save_alerts()
    
    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "monitoring_period_hours": 168,  # Last week
            "summary": self.get_performance_summary(hours=168),
            "active_alerts": self.get_active_alerts(),
            "experiments": {
                "active": sum(1 for e in self.experiments.values() if e["status"] == "running"),
                "completed": sum(1 for e in self.experiments.values() if e["status"] == "completed"),
                "results": self.get_experiment_results()
            },
            "system_health": self._calculate_system_health()
        }
        
        return report
    
    def _calculate_system_health(self) -> Dict:
        """Calculate overall system health score"""
        active_alerts = self.get_active_alerts()
        
        # Health factors
        critical_alerts = sum(1 for a in active_alerts if a["severity"] == "critical")
        high_alerts = sum(1 for a in active_alerts if a["severity"] == "high")
        
        # Calculate health score (0-100)
        health_score = 100
        health_score -= critical_alerts * 20
        health_score -= high_alerts * 10
        health_score = max(0, health_score)
        
        return {
            "score": health_score,
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "unhealthy",
            "factors": {
                "critical_alerts": critical_alerts,
                "high_alerts": high_alerts,
                "total_alerts": len(active_alerts)
            }
        }
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring_active = False
        self._flush_metrics()
        logger.info("Monitoring system stopped")


def setup_monitoring():
    """Initialize monitoring system"""
    monitor = ModelPerformanceMonitor()
    logger.info("Model performance monitoring system initialized")
    return monitor


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    monitor = setup_monitoring()
    
    # Simulate some predictions
    for i in range(10):
        monitor.record_prediction(
            model_type="dna_analyzer",
            model_version="v20240604_123456",
            prediction=np.random.rand(),
            confidence=0.8 + np.random.rand() * 0.2,
            latency_ms=50 + np.random.rand() * 50,
            features={"feature1": i, "feature2": i*2}
        )
    
    # Get performance summary
    summary = monitor.get_performance_summary()
    print(json.dumps(summary, indent=2))
    
    # Create A/B test
    monitor.create_ab_test(
        "test_new_ensemble",
        model_a="ensemble_v1",
        model_b="ensemble_v2",
        traffic_split=0.5,
        min_samples=100
    )
    
    # Generate report
    report = monitor.generate_performance_report()
    print("\nPerformance Report:")
    print(json.dumps(report, indent=2))