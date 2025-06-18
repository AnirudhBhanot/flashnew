#!/usr/bin/env python3
"""
API Middleware for Monitoring and Logging Integration
"""

import time
import uuid
from datetime import datetime
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
import logging

from .logger_config import api_logger, security_logger, performance_logger
from .metrics_collector import record_api_request, record_model_prediction

logger = logging.getLogger(__name__)


class MonitoringMiddleware:
    """Middleware for request/response monitoring"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Record request start
        start_time = time.time()
        
        # Get client info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log request
        api_logger.log_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=client_ip,
            user_agent=user_agent
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate metrics
            latency_ms = (time.time() - start_time) * 1000
            
            # Log response
            api_logger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                latency_ms=latency_ms,
                response_size=int(response.headers.get("content-length", 0))
            )
            
            # Record metrics
            record_api_request(
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                latency_ms=latency_ms,
                request_size=int(request.headers.get("content-length", 0)),
                response_size=int(response.headers.get("content-length", 0))
            )
            
            # Add monitoring headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{latency_ms:.0f}ms"
            
            return response
            
        except Exception as e:
            # Log error
            latency_ms = (time.time() - start_time) * 1000
            api_logger.log_error(request_id=request_id, error=e)
            
            # Record error metrics
            record_api_request(
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=500,
                latency_ms=latency_ms,
                request_size=int(request.headers.get("content-length", 0)),
                response_size=0
            )
            
            raise


class LoggingRoute(APIRoute):
    """Custom route class that logs all requests"""
    
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            # Get request ID from middleware
            request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
            
            # Log endpoint access
            logger.info(f"Endpoint accessed: {request.method} {request.url.path}",
                       extra={"request_id": request_id})
            
            # Call original handler
            response = await original_route_handler(request)
            
            return response
        
        return custom_route_handler


def log_prediction_metrics(
    model_name: str,
    startup_id: str,
    prediction: float,
    confidence: float,
    latency_ms: float,
    features_count: int
):
    """Log model prediction metrics"""
    # Log to model logger
    from .logger_config import model_logger
    
    model_logger.log_prediction(
        model_name=model_name,
        startup_id=startup_id,
        prediction=prediction,
        confidence=confidence,
        latency_ms=latency_ms,
        features={'count': features_count}
    )
    
    # Record metrics
    record_model_prediction(
        model_name=model_name,
        startup_id=startup_id,
        prediction=prediction,
        confidence=confidence,
        latency_ms=latency_ms,
        features_used=features_count
    )


def log_security_event(event_type: str, client_ip: str, **kwargs):
    """Log security-related events"""
    if event_type == "rate_limit_exceeded":
        security_logger.log_rate_limit_exceeded(
            client_ip=client_ip,
            endpoint=kwargs.get("endpoint", "unknown")
        )
    elif event_type == "invalid_input":
        security_logger.log_invalid_input(
            client_ip=client_ip,
            endpoint=kwargs.get("endpoint", "unknown"),
            validation_errors=kwargs.get("errors", {})
        )
    elif event_type == "suspicious_activity":
        security_logger.log_suspicious_activity(
            client_ip=client_ip,
            reason=kwargs.get("reason", "unknown"),
            details=kwargs.get("details", {})
        )


class PerformanceLoggingMiddleware:
    """Middleware for detailed performance logging"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Skip for health checks and metrics endpoints
        if request.url.path in ["/health", "/metrics", "/api/metrics"]:
            return await call_next(request)
        
        # Track detailed timing
        timings = {
            "start": time.time(),
            "request_parsed": None,
            "processing_start": None,
            "processing_end": None,
            "response_start": None,
            "end": None
        }
        
        timings["request_parsed"] = time.time()
        
        # Process request
        timings["processing_start"] = time.time()
        response = await call_next(request)
        timings["processing_end"] = time.time()
        
        timings["response_start"] = time.time()
        timings["end"] = time.time()
        
        # Calculate detailed metrics
        total_time = (timings["end"] - timings["start"]) * 1000
        processing_time = (timings["processing_end"] - timings["processing_start"]) * 1000
        
        # Log performance metrics
        if total_time > 1000:  # Log slow requests (>1s)
            performance_logger.warning(
                f"Slow request detected: {request.method} {request.url.path}",
                extra={
                    "request_id": getattr(request.state, "request_id", "unknown"),
                    "total_time_ms": total_time,
                    "processing_time_ms": processing_time,
                    "endpoint": request.url.path,
                    "method": request.method
                }
            )
        
        return response


def setup_monitoring_middleware(app):
    """Setup all monitoring middleware for the app"""
    # Add monitoring middleware
    app.middleware("http")(MonitoringMiddleware())
    
    # Add performance logging for slow requests
    app.middleware("http")(PerformanceLoggingMiddleware())
    
    # Use custom route class for endpoint logging
    app.router.route_class = LoggingRoute
    
    logger.info("Monitoring middleware configured")