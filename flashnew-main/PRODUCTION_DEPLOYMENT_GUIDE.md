# FLASH Production Deployment Guide

## Executive Summary

This guide provides step-by-step instructions for deploying FLASH improvements to production with zero downtime, comprehensive monitoring, and rollback capabilities.

## Architecture Overview

```
                    ┌─────────────┐
                    │   Nginx LB   │ (SSL, Rate Limiting)
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │                     │
          ┌─────▼─────┐        ┌─────▼─────┐
          │  API Pod 1 │        │  API Pod 2 │ (Auto-scaling)
          └─────┬─────┘        └─────┬─────┘
                │                     │
                └──────────┬──────────┘
                           │
                    ┌──────▼──────┐
                    │    Redis     │ (Caching Layer)
                    └─────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
   ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
   │Prometheus │    │  Grafana   │    │   Logs    │
   └───────────┘    └────────────┘    └───────────┘
```

## Pre-Deployment Checklist

### 1. Model Validation
```bash
# Verify improved models exist and perform correctly
python3 -c "
from calibrated_orchestrator import CalibratedOrchestrator
import pandas as pd

# Test prediction
orch = CalibratedOrchestrator()
test_data = pd.DataFrame([{'total_capital_raised_usd': 1000000, 'funding_stage': 'seed'}])
result = orch.predict(test_data)

# Validate output
assert 0 <= result['success_probability'] <= 1
assert result['confidence_interval']['lower'] <= result['success_probability'] <= result['confidence_interval']['upper']
print('✅ Model validation passed')
"
```

### 2. Performance Baseline
```bash
# Run performance tests
python3 test_improvements.py

# Expected results:
# - Response time p99: <200ms
# - Probability range: 0-100%
# - No errors in 1000 requests
```

### 3. Security Audit
```bash
# Check for secrets in code
git secrets --scan

# Verify environment variables
grep -r "SECRET\|PASSWORD\|KEY" --exclude-dir=.git .

# Ensure all models have checksums
ls -la models/improved_v1/*.pkl | wc -l  # Should be 6+ files
```

## Deployment Steps

### Phase 1: Staging Deployment

#### 1.1 Build and Test Docker Image
```bash
cd deployment
docker build -t flash-api:v2.0.0 -f Dockerfile ..

# Test locally
docker run -p 8001:8001 --rm \
  -v $(pwd)/../models:/app/models:ro \
  flash-api:v2.0.0

# Verify health
curl http://localhost:8001/health
```

#### 1.2 Deploy to Staging
```bash
# Tag for registry
docker tag flash-api:v2.0.0 your-registry/flash-api:v2.0.0
docker push your-registry/flash-api:v2.0.0

# Deploy to staging cluster
kubectl apply -f k8s/staging/ -n flash-staging

# Wait for rollout
kubectl rollout status deployment/flash-api -n flash-staging
```

#### 1.3 Staging Validation
```bash
# Run integration tests against staging
FLASH_API_URL=https://staging.flash.api python3 test_improvements.py

# Load test
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" \
  https://staging.flash.api/predict
```

### Phase 2: Production Deployment (Blue-Green)

#### 2.1 Deploy Green Environment
```bash
# Create green deployment
kubectl apply -f k8s/production/green-deployment.yaml

# Verify green pods are ready
kubectl get pods -l version=green,app=flash-api

# Test green environment directly
kubectl port-forward svc/flash-api-green 8002:8001
curl http://localhost:8002/health
```

#### 2.2 Canary Testing (5% Traffic)
```bash
# Update nginx to send 5% traffic to green
kubectl apply -f k8s/production/nginx-canary-5.yaml

# Monitor metrics for 15 minutes
watch -n 5 'kubectl exec -it prometheus-0 -- \
  promtool query instant \
    "rate(http_requests_total{version=\"green\"}[5m])"'
```

#### 2.3 Progressive Rollout
```bash
# If metrics look good, increase traffic progressively
for percent in 25 50 75 100; do
  echo "Shifting $percent% traffic to green..."
  kubectl apply -f k8s/production/nginx-canary-$percent.yaml
  
  # Monitor for 10 minutes
  sleep 600
  
  # Check error rate
  ERROR_RATE=$(kubectl exec -it prometheus-0 -- \
    promtool query instant \
      'rate(http_requests_total{status=~"5..",version="green"}[5m])' | \
    jq -r '.data.result[0].value[1]')
  
  if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
    echo "❌ High error rate detected. Rolling back..."
    kubectl apply -f k8s/production/nginx-canary-0.yaml
    exit 1
  fi
done
```

#### 2.4 Complete Migration
```bash
# Switch all traffic to green
kubectl apply -f k8s/production/nginx-green-only.yaml

# Wait 5 minutes for connections to drain
sleep 300

# Delete blue deployment
kubectl delete deployment flash-api-blue

# Relabel green as new blue for next deployment
kubectl label deployment flash-api-green version=blue --overwrite
```

### Phase 3: Post-Deployment

#### 3.1 Monitoring Setup
```bash
# Import Grafana dashboards
curl -X POST http://admin:flash123@grafana:3001/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @grafana/dashboards/flash-performance.json

# Set up alerts
kubectl apply -f k8s/monitoring/alerts.yaml
```

#### 3.2 Performance Validation
```python
# Run production validation
from monitoring.performance_monitor import PerformanceMonitor
import requests

monitor = PerformanceMonitor()

# Test 100 production requests
for _ in range(100):
    response = requests.post(
        "https://api.flash.com/predict",
        json={"total_capital_raised_usd": 1000000},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    
    monitor.record_prediction(
        response.elapsed.total_seconds() * 1000,
        response.json()['success_probability'],
        45,
        False
    )

# Check SLAs
stats = monitor.get_current_stats()
sla = monitor._calculate_sla_compliance()

for metric, result in sla.items():
    print(f"{metric}: {'✅' if result['compliant'] else '❌'} {result['actual']}")
```

## Rollback Procedure

### Immediate Rollback (< 5 minutes)
```bash
# Switch traffic back to blue
kubectl apply -f k8s/production/nginx-blue-only.yaml

# Delete problematic green deployment
kubectl delete deployment flash-api-green
```

### Model Rollback
```bash
# Revert to previous model version
cd models
mv improved_v1 improved_v1_failed
mv improved_v1_backup improved_v1

# Restart API pods
kubectl rollout restart deployment/flash-api
```

## Monitoring & Alerts

### Key Metrics to Watch

1. **Latency SLA**
   - Alert: p99 > 300ms for 5 minutes
   - Page: p99 > 500ms for 2 minutes

2. **Error Rate**
   - Alert: >2% errors for 5 minutes
   - Page: >5% errors for 1 minute

3. **Prediction Distribution**
   - Alert: std(predictions) < 0.05 for 10 minutes
   - Indicates model calibration issues

4. **Resource Usage**
   - Alert: CPU > 80% for 10 minutes
   - Alert: Memory > 90% for 5 minutes

### Grafana Dashboards

Access at: https://grafana.flash.com

1. **FLASH Overview** - System health at a glance
2. **API Performance** - Latency percentiles, throughput
3. **Model Metrics** - Prediction distribution, feature importance
4. **Business Metrics** - Predictions by verdict, confidence levels

## Troubleshooting

### High Latency
```bash
# Check cache hit rate
redis-cli info stats | grep keyspace_hits

# Profile slow requests
kubectl logs -l app=flash-api --tail=1000 | \
  grep "response_time" | \
  jq -r 'select(.response_time_ms > 500)'
```

### Narrow Prediction Range
```bash
# Check calibration
kubectl exec -it flash-api-pod -- python3 -c "
from calibrated_orchestrator import CalibratedOrchestrator
orch = CalibratedOrchestrator()
print(f'Calibration loaded: {\"main\" in orch.calibrators}')
"
```

### Memory Leaks
```bash
# Get memory profile
kubectl exec -it flash-api-pod -- python3 -m memory_profiler api_server_improved.py

# Force garbage collection
kubectl exec -it flash-api-pod -- python3 -c "
import gc
gc.collect()
print(f'Collected {gc.collect()} objects')
"
```

## Security Considerations

1. **API Keys**: Rotate every 90 days
2. **SSL Certificates**: Auto-renew with cert-manager
3. **Model Files**: Read-only volume mounts
4. **Redis**: Enable AUTH and use SSL
5. **Monitoring**: Restrict metrics endpoints to internal IPs

## Cost Optimization

1. **Auto-scaling**: Scale down during low traffic (nights/weekends)
2. **Spot Instances**: Use for non-critical batch processing
3. **Cache TTL**: Optimize based on usage patterns
4. **Model Quantization**: Reduce model size by 50% with minimal accuracy loss

## Success Criteria

Post-deployment validation checklist:

- [ ] Response time p99 < 200ms
- [ ] Prediction range spans 0-100%
- [ ] Error rate < 1%
- [ ] Cache hit rate > 70%
- [ ] All monitoring dashboards populated
- [ ] Alerts configured and tested
- [ ] Rollback procedure validated
- [ ] Performance 10x better than v1

## Contact

- **Engineering Lead**: engineering@flash.com
- **On-Call**: +1-xxx-xxx-xxxx
- **Slack**: #flash-production
- **PagerDuty**: flash-api-oncall

---

Last Updated: 2024-01-06
Version: 2.0.0