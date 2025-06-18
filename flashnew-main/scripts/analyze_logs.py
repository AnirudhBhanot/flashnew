#!/usr/bin/env python3
"""
Analyze FLASH API logs for insights
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd

def analyze_logs(log_file='logs/flash_json.log', hours=24):
    """Analyze recent logs"""
    
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
    print(f"\nLog Analysis Summary (last {hours} hours)")
    print("=" * 50)
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Errors: {stats['errors']} ({stats['errors']/stats['total_requests']*100:.1f}%)")
    print(f"\nTop Endpoints:")
    for endpoint, count in sorted(stats['endpoints'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {endpoint}: {count}")
    
    if stats['slow_requests']:
        print(f"\nSlow Requests: {len(stats['slow_requests'])}")
        df = pd.DataFrame(stats['slow_requests'])
        print(f"  Average latency: {df['latency_ms'].mean():.0f}ms")
        print(f"  Max latency: {df['latency_ms'].max():.0f}ms")
    
    return stats

if __name__ == "__main__":
    analyze_logs()
