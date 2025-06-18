#!/usr/bin/env python3
"""
Generate metrics report for FLASH platform
"""

import json
import glob
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def generate_report(metrics_dir='metrics', days=7):
    """Generate metrics report"""
    
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
    print(f"\nMetrics Summary (last {days} days)")
    print("=" * 50)
    print(f"Average P95 Latency: {sum(latencies)/len(latencies):.0f}ms")
    print(f"Average Success Rate: {sum(success_rates)/len(success_rates)*100:.1f}%")
    print(f"Average Request Rate: {sum(request_rates)/len(request_rates):.1f} req/min")

if __name__ == "__main__":
    generate_report()
