#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for FLASH Platform
Provides web-based dashboard for metrics visualization
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
from datetime import datetime
from typing import List
import logging

from .metrics_collector import metrics_collector, performance_monitor

logger = logging.getLogger(__name__)

# Create FastAPI app for dashboard
dashboard_app = FastAPI(title="FLASH Monitoring Dashboard")


class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # Connection might be closed
                pass


manager = ConnectionManager()


@dashboard_app.get("/")
async def get_dashboard():
    """Serve the monitoring dashboard HTML"""
    return HTMLResponse(content=DASHBOARD_HTML)


@dashboard_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Send metrics every 2 seconds
            metrics = metrics_collector.get_dashboard_metrics()
            alerts = performance_monitor.get_recent_alerts(minutes=5)
            
            await websocket.send_json({
                'type': 'metrics_update',
                'data': metrics,
                'alerts': alerts
            })
            
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@dashboard_app.get("/api/metrics")
async def get_metrics():
    """Get current metrics snapshot"""
    return metrics_collector.get_dashboard_metrics()


@dashboard_app.get("/api/alerts")
async def get_alerts(minutes: int = 60):
    """Get recent alerts"""
    return performance_monitor.get_recent_alerts(minutes)


@dashboard_app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Dashboard HTML template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FLASH Monitoring Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metric-card h3 {
            margin: 0 0 1rem 0;
            color: #2c3e50;
            font-size: 1.1rem;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        
        .status-healthy { color: #27ae60; }
        .status-warning { color: #f39c12; }
        .status-error { color: #e74c3c; }
        
        .chart-container {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        
        .alerts {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .alert {
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        
        .alert-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .alert-critical {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        
        .chart {
            height: 300px;
        }
        
        .connection-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .connected {
            background-color: #27ae60;
            color: white;
        }
        
        .disconnected {
            background-color: #e74c3c;
            color: white;
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
        }
        
        .metric-row span:first-child {
            color: #7f8c8d;
        }
        
        .metric-row span:last-child {
            font-weight: 500;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="header">
        <h1>FLASH Monitoring Dashboard</h1>
        <p style="margin: 0; opacity: 0.8;">Real-time system metrics and performance monitoring</p>
    </div>
    
    <div class="container">
        <!-- Key Metrics -->
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Request Rate</h3>
                <div class="metric-value" id="request-rate">0</div>
                <div class="metric-label">requests/minute</div>
            </div>
            
            <div class="metric-card">
                <h3>Success Rate</h3>
                <div class="metric-value" id="success-rate">0%</div>
                <div class="metric-label">last 5 minutes</div>
            </div>
            
            <div class="metric-card">
                <h3>P95 Latency</h3>
                <div class="metric-value" id="p95-latency">0ms</div>
                <div class="metric-label">95th percentile</div>
            </div>
            
            <div class="metric-card">
                <h3>System Health</h3>
                <div class="metric-value" id="system-health">Unknown</div>
                <div class="metric-label">
                    CPU: <span id="cpu-usage">0%</span> | 
                    Memory: <span id="memory-usage">0%</span>
                </div>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="chart-container">
            <h3>Request Latency Trend</h3>
            <canvas id="latency-chart" class="chart"></canvas>
        </div>
        
        <div class="metrics-grid">
            <div class="chart-container">
                <h3>Model Performance</h3>
                <div id="model-stats">
                    <div class="metric-row">
                        <span>Loading...</span>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Prediction Distribution</h3>
                <canvas id="prediction-chart" class="chart"></canvas>
            </div>
        </div>
        
        <!-- Alerts -->
        <div class="alerts">
            <h3>Recent Alerts</h3>
            <div id="alerts-container">
                <p style="color: #7f8c8d;">No recent alerts</p>
            </div>
        </div>
    </div>
    
    <div class="connection-status connected" id="connection-status">
        Connected
    </div>
    
    <script>
        // WebSocket connection
        let ws = null;
        let reconnectInterval = null;
        
        // Chart instances
        let latencyChart = null;
        let predictionChart = null;
        
        // Data storage
        const latencyData = {
            labels: [],
            datasets: [{
                label: 'P95 Latency (ms)',
                data: [],
                borderColor: '#3498db',
                tension: 0.1
            }, {
                label: 'Avg Latency (ms)',
                data: [],
                borderColor: '#2ecc71',
                tension: 0.1
            }]
        };
        
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            ws.onopen = () => {
                console.log('Connected to monitoring dashboard');
                document.getElementById('connection-status').className = 'connection-status connected';
                document.getElementById('connection-status').textContent = 'Connected';
                
                if (reconnectInterval) {
                    clearInterval(reconnectInterval);
                    reconnectInterval = null;
                }
            };
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                if (message.type === 'metrics_update') {
                    updateMetrics(message.data);
                    updateAlerts(message.alerts);
                }
            };
            
            ws.onclose = () => {
                console.log('Disconnected from monitoring dashboard');
                document.getElementById('connection-status').className = 'connection-status disconnected';
                document.getElementById('connection-status').textContent = 'Disconnected';
                
                // Reconnect after 5 seconds
                if (!reconnectInterval) {
                    reconnectInterval = setInterval(connectWebSocket, 5000);
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
        
        function updateMetrics(metrics) {
            // Update request metrics
            const requestStats = metrics.request_stats;
            document.getElementById('request-rate').textContent = 
                requestStats.requests_per_minute.toFixed(1);
            document.getElementById('success-rate').textContent = 
                (requestStats.success_rate * 100).toFixed(1) + '%';
            document.getElementById('p95-latency').textContent = 
                requestStats.p95_latency_ms.toFixed(0) + 'ms';
            
            // Update system health
            const systemHealth = metrics.system_health;
            const healthElement = document.getElementById('system-health');
            healthElement.textContent = systemHealth.status.charAt(0).toUpperCase() + 
                                      systemHealth.status.slice(1);
            healthElement.className = 'metric-value status-' + 
                (systemHealth.status === 'healthy' ? 'healthy' : 'warning');
            
            document.getElementById('cpu-usage').textContent = 
                systemHealth.cpu_percent.toFixed(1) + '%';
            document.getElementById('memory-usage').textContent = 
                systemHealth.memory_percent.toFixed(1) + '%';
            
            // Update latency chart
            updateLatencyChart(requestStats);
            
            // Update model stats
            updateModelStats(metrics.model_stats);
            
            // Update prediction distribution
            updatePredictionChart(metrics.model_stats.overall.prediction_distribution);
        }
        
        function updateLatencyChart(stats) {
            const now = new Date().toLocaleTimeString();
            
            latencyData.labels.push(now);
            latencyData.datasets[0].data.push(stats.p95_latency_ms);
            latencyData.datasets[1].data.push(stats.avg_latency_ms);
            
            // Keep only last 20 data points
            if (latencyData.labels.length > 20) {
                latencyData.labels.shift();
                latencyData.datasets[0].data.shift();
                latencyData.datasets[1].data.shift();
            }
            
            if (latencyChart) {
                latencyChart.update();
            }
        }
        
        function updateModelStats(modelStats) {
            const container = document.getElementById('model-stats');
            let html = '';
            
            for (const [model, stats] of Object.entries(modelStats.by_model)) {
                if (stats.predictions_count > 0) {
                    html += `
                        <div style="margin-bottom: 1rem;">
                            <strong>${model.replace('_', ' ').toUpperCase()}</strong>
                            <div class="metric-row">
                                <span>Predictions</span>
                                <span>${stats.predictions_count}</span>
                            </div>
                            <div class="metric-row">
                                <span>Avg Confidence</span>
                                <span>${(stats.avg_confidence * 100).toFixed(1)}%</span>
                            </div>
                            <div class="metric-row">
                                <span>Avg Latency</span>
                                <span>${stats.avg_latency_ms.toFixed(0)}ms</span>
                            </div>
                        </div>
                    `;
                }
            }
            
            container.innerHTML = html || '<p style="color: #7f8c8d;">No model data available</p>';
        }
        
        function updatePredictionChart(distribution) {
            if (!distribution) return;
            
            const data = {
                labels: ['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                datasets: [{
                    label: 'Predictions',
                    data: [
                        distribution.very_low,
                        distribution.low,
                        distribution.medium,
                        distribution.high,
                        distribution.very_high
                    ],
                    backgroundColor: [
                        '#e74c3c',
                        '#f39c12',
                        '#f1c40f',
                        '#2ecc71',
                        '#27ae60'
                    ]
                }]
            };
            
            if (predictionChart) {
                predictionChart.data = data;
                predictionChart.update();
            }
        }
        
        function updateAlerts(alerts) {
            const container = document.getElementById('alerts-container');
            
            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<p style="color: #7f8c8d;">No recent alerts</p>';
                return;
            }
            
            let html = '';
            for (const alert of alerts.slice(0, 10)) {
                const alertClass = 'alert-' + alert.level;
                const time = new Date(alert.timestamp).toLocaleTimeString();
                html += `
                    <div class="alert ${alertClass}">
                        <div>
                            <strong>${alert.type.replace('_', ' ').toUpperCase()}</strong>
                            <br>${alert.message}
                        </div>
                        <span style="font-size: 0.8rem; opacity: 0.7;">${time}</span>
                    </div>
                `;
            }
            
            container.innerHTML = html;
        }
        
        // Initialize charts
        function initCharts() {
            // Latency chart
            const latencyCtx = document.getElementById('latency-chart').getContext('2d');
            latencyChart = new Chart(latencyCtx, {
                type: 'line',
                data: latencyData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            
            // Prediction distribution chart
            const predictionCtx = document.getElementById('prediction-chart').getContext('2d');
            predictionChart = new Chart(predictionCtx, {
                type: 'bar',
                data: {
                    labels: ['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                    datasets: [{
                        label: 'Predictions',
                        data: [0, 0, 0, 0, 0],
                        backgroundColor: [
                            '#e74c3c',
                            '#f39c12',
                            '#f1c40f',
                            '#2ecc71',
                            '#27ae60'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Initialize on load
        window.onload = () => {
            initCharts();
            connectWebSocket();
        };
    </script>
</body>
</html>
"""