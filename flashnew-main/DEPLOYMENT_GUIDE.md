# 🚀 FLASH Platform Production Deployment Guide

## Overview
This guide covers deploying the FLASH platform in production with all security features, monitoring, and optimizations enabled.

## Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional but recommended)
- Redis (for caching)
- PostgreSQL (optional, SQLite works as alternative)

## 🛠️ Deployment Options

### Option 1: Docker Compose (Recommended)
Complete production stack with all services.

```bash
# 1. Set up environment
./setup_environment.sh

# 2. Build and start all services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f api
```

Services included:
- FLASH API (port 8001)
- Redis Cache (port 6379)
- PostgreSQL Database (port 5432)
- Nginx Reverse Proxy (port 80/443)
- Prometheus Monitoring (port 9090)
- Grafana Dashboard (port 3000)

### Option 2: Direct Installation
For servers without Docker.

```bash
# 1. Install Redis
brew install redis  # macOS
sudo apt install redis-server  # Ubuntu

# 2. Set up environment
./setup_environment.sh

# 3. Install dependencies
./install_dependencies.sh

# 4. Start services
redis-server &  # Start Redis
./start_production.sh  # Start FLASH API
```

### Option 3: Systemd Service (Linux)
For production Linux servers.

```bash
# 1. Run setup
./setup_environment.sh

# 2. Copy service file
sudo cp flash-api.service /etc/systemd/system/

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable flash-api
sudo systemctl start flash-api

# 4. Check status
sudo systemctl status flash-api
```

## 📋 Configuration Checklist

### 1. Environment Variables (.env)
```bash
# Required
DB_PASSWORD=<secure-password>
JWT_SECRET_KEY=<secure-key>
API_KEYS=<comma-separated-keys>

# Optional but recommended
REDIS_PASSWORD=<redis-password>
ALLOWED_ORIGINS=https://your-domain.com
```

### 2. SSL/TLS Setup
For HTTPS in production:

```bash
# Using Let's Encrypt
sudo certbot --nginx -d your-domain.com

# Or mount certificates in docker-compose.yml
volumes:
  - ./ssl/cert.pem:/etc/nginx/ssl/cert.pem
  - ./ssl/key.pem:/etc/nginx/ssl/key.pem
```

### 3. Model Integrity
Verify all models before deployment:

```bash
python3 utils/model_integrity.py
```

### 4. Database Setup
```bash
# PostgreSQL (if using)
createdb flash_db
psql flash_db < schema.sql

# SQLite (automatic)
# Database created on first run
```

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure ALLOWED_ORIGINS
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure log rotation
- [ ] Set up backup strategy

## 📊 Monitoring

### Prometheus Metrics
Access at: http://localhost:9090

Key metrics to monitor:
- `flash_requests_total` - Total API requests
- `flash_predictions_total` - Total predictions made
- `flash_request_duration_seconds` - Response times
- `flash_errors_total` - Error count

### Grafana Dashboard
Access at: http://localhost:3000
- Default login: admin/admin
- Import dashboard from `grafana/dashboards/`

### Health Checks
```bash
# API health
curl http://localhost:8001/health

# System metrics
curl -H "X-API-Key: your-key" http://localhost:8001/metrics/summary
```

## 🚦 Testing Production

### 1. Security Test
```bash
python3 tests/test_security.py
```

### 2. Performance Test
```bash
python3 tests/test_performance.py
```

### 3. API Test
```bash
# Test prediction
curl -X POST http://localhost:8001/predict \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "startup_name": "Test Inc",
    "funding_stage": "seed",
    "total_capital_raised_usd": 1000000,
    "team_size_full_time": 10
  }'
```

## 🔧 Maintenance

### Log Rotation
```bash
# Add to /etc/logrotate.d/flash-api
/path/to/flash/logs/*.log {
    daily
    rotate 14
    compress
    notifempty
    create 0640 flash flash
    postrotate
        systemctl reload flash-api
    endscript
}
```

### Backup Strategy
```bash
# Database backup (PostgreSQL)
pg_dump flash_db > backup_$(date +%Y%m%d).sql

# SQLite backup
cp data/flash.db backup_flash_$(date +%Y%m%d).db

# Model backup
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

### Cache Management
```bash
# Clear all cache
curl -X POST http://localhost:8001/cache/clear \
  -H "Authorization: Bearer your-jwt-token"

# Monitor cache stats
redis-cli info stats
```

## 🚨 Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Start Redis
   sudo systemctl start redis
   ```

2. **Model Loading Error**
   ```bash
   # Verify checksums
   python3 utils/model_integrity.py
   
   # Regenerate checksums if needed
   python3 -c "from utils.model_integrity import generate_production_checksums; generate_production_checksums()"
   ```

3. **High Memory Usage**
   ```bash
   # Check memory
   docker stats
   
   # Limit Redis memory
   redis-cli CONFIG SET maxmemory 2gb
   ```

4. **Rate Limiting Issues**
   ```bash
   # Check current limits
   grep limit_ nginx.conf
   
   # Adjust in nginx.conf
   limit_req_zone ... rate=100r/s;
   ```

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
api:
  scale: 4  # Run 4 instances
```

### Load Balancing
```nginx
upstream flash_api {
    least_conn;
    server api1:8001;
    server api2:8001;
    server api3:8001;
    server api4:8001;
}
```

### Caching Strategy
- Predictions: 4-hour TTL
- Pattern analysis: 8-hour TTL
- Metrics: 1-minute TTL

## 🎯 Performance Optimization

1. **Enable Redis** - 10x speedup for repeated predictions
2. **Use PostgreSQL** - Better for concurrent access than SQLite
3. **Enable connection pooling** - Already configured
4. **Use Nginx** - For SSL termination and rate limiting
5. **Monitor metrics** - Identify bottlenecks early

## 📝 Production Checklist

Before going live:
- [ ] All tests passing
- [ ] SSL certificate installed
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Log rotation set up
- [ ] Rate limits configured
- [ ] API keys generated
- [ ] Documentation updated
- [ ] Disaster recovery plan tested
- [ ] Performance benchmarks met

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs api`
2. Run diagnostics: `python3 test_monitoring_integration.py`
3. Review metrics: http://localhost:9090
4. Check documentation: `ALL_ISSUES_RESOLVED.md`

---
**Last Updated**: January 6, 2025
**Platform Version**: 1.0.0
**Status**: Production Ready ✅