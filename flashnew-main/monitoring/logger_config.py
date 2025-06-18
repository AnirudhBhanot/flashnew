#!/usr/bin/env python3
"""
Centralized Logging Configuration for FLASH Platform
Provides structured logging with multiple handlers and formatters
"""

import logging
import logging.handlers
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import traceback


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'process_id': os.getpid(),
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'startup_id'):
            log_data['startup_id'] = record.startup_id
        if hasattr(record, 'model_name'):
            log_data['model_name'] = record.model_name
        if hasattr(record, 'prediction'):
            log_data['prediction'] = record.prediction
        if hasattr(record, 'latency_ms'):
            log_data['latency_ms'] = record.latency_ms
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        # Format the message
        result = super().format(record)
        
        # Reset level name
        record.levelname = levelname
        
        return result


class LoggerConfig:
    """Centralized logger configuration"""
    
    def __init__(self, 
                 app_name: str = "flash",
                 log_dir: str = "logs",
                 log_level: str = "INFO",
                 enable_console: bool = True,
                 enable_file: bool = True,
                 enable_json: bool = True):
        
        self.app_name = app_name
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.enable_console = enable_console
        self.enable_file = enable_file
        self.enable_json = enable_json
        
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        self._configure_root_logger()
        
    def _configure_root_logger(self):
        """Configure the root logger with handlers"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers
        root_logger.handlers = []
        
        # Add console handler
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
        
        # Add file handler for general logs
        if self.enable_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_dir / f"{self.app_name}.log",
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(self.log_level)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        
        # Add JSON file handler for structured logs
        if self.enable_json:
            json_handler = logging.handlers.RotatingFileHandler(
                self.log_dir / f"{self.app_name}_json.log",
                maxBytes=50 * 1024 * 1024,  # 50MB
                backupCount=10
            )
            json_handler.setLevel(self.log_level)
            json_handler.setFormatter(JSONFormatter())
            root_logger.addHandler(json_handler)
        
        # Add error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.app_name}_errors.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s\n%(exc_info)s'
        )
        error_handler.setFormatter(error_formatter)
        root_logger.addHandler(error_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the given name"""
        return logging.getLogger(name)
    
    def add_file_handler(self, logger_name: str, filename: str):
        """Add a specific file handler for a logger"""
        logger = logging.getLogger(logger_name)
        
        handler = logging.handlers.RotatingFileHandler(
            self.log_dir / filename,
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
        handler.setLevel(self.log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def configure_module_loggers(self):
        """Configure specific loggers for each module"""
        modules = [
            ('api', 'api.log'),
            ('models', 'models.log'),
            ('predictions', 'predictions.log'),
            ('performance', 'performance.log'),
            ('security', 'security.log'),
        ]
        
        for module_name, log_file in modules:
            self.add_file_handler(module_name, log_file)


class RequestLogger:
    """Logger for API requests with request ID tracking"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
    def log_request(self, request_id: str, method: str, path: str, 
                   client_ip: str, user_agent: Optional[str] = None):
        """Log incoming request"""
        self.logger.info(
            f"Request received: {method} {path}",
            extra={
                'request_id': request_id,
                'method': method,
                'path': path,
                'client_ip': client_ip,
                'user_agent': user_agent
            }
        )
    
    def log_response(self, request_id: str, status_code: int, 
                    latency_ms: float, response_size: int):
        """Log response details"""
        self.logger.info(
            f"Request completed: {status_code}",
            extra={
                'request_id': request_id,
                'status_code': status_code,
                'latency_ms': latency_ms,
                'response_size': response_size
            }
        )
    
    def log_error(self, request_id: str, error: Exception, 
                 status_code: int = 500):
        """Log request error"""
        self.logger.error(
            f"Request failed: {str(error)}",
            extra={
                'request_id': request_id,
                'status_code': status_code,
                'error_type': type(error).__name__
            },
            exc_info=True
        )


class ModelLogger:
    """Logger for model predictions and performance"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_prediction(self, model_name: str, startup_id: str,
                      prediction: float, confidence: float,
                      latency_ms: float, features: Optional[Dict] = None):
        """Log model prediction"""
        self.logger.info(
            f"Prediction made by {model_name}",
            extra={
                'model_name': model_name,
                'startup_id': startup_id,
                'prediction': prediction,
                'confidence': confidence,
                'latency_ms': latency_ms,
                'features_hash': hash(str(features)) if features else None
            }
        )
    
    def log_model_error(self, model_name: str, error: Exception,
                       startup_id: Optional[str] = None):
        """Log model error"""
        self.logger.error(
            f"Model {model_name} failed: {str(error)}",
            extra={
                'model_name': model_name,
                'startup_id': startup_id,
                'error_type': type(error).__name__
            },
            exc_info=True
        )
    
    def log_model_performance(self, model_name: str, metrics: Dict[str, float]):
        """Log model performance metrics"""
        self.logger.info(
            f"Model {model_name} performance metrics",
            extra={
                'model_name': model_name,
                **metrics
            }
        )


class SecurityLogger:
    """Logger for security events"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_rate_limit_exceeded(self, client_ip: str, endpoint: str):
        """Log rate limit violation"""
        self.logger.warning(
            f"Rate limit exceeded for {client_ip}",
            extra={
                'event_type': 'rate_limit_exceeded',
                'client_ip': client_ip,
                'endpoint': endpoint
            }
        )
    
    def log_invalid_input(self, client_ip: str, endpoint: str, 
                         validation_errors: Dict):
        """Log invalid input attempts"""
        self.logger.warning(
            f"Invalid input from {client_ip}",
            extra={
                'event_type': 'invalid_input',
                'client_ip': client_ip,
                'endpoint': endpoint,
                'validation_errors': validation_errors
            }
        )
    
    def log_suspicious_activity(self, client_ip: str, reason: str,
                               details: Optional[Dict] = None):
        """Log suspicious activity"""
        self.logger.warning(
            f"Suspicious activity from {client_ip}: {reason}",
            extra={
                'event_type': 'suspicious_activity',
                'client_ip': client_ip,
                'reason': reason,
                'details': details
            }
        )


# Initialize default logger configuration
default_config = LoggerConfig()

# Create specialized loggers
api_logger = RequestLogger(default_config.get_logger('api'))
model_logger = ModelLogger(default_config.get_logger('models'))
security_logger = SecurityLogger(default_config.get_logger('security'))
performance_logger = default_config.get_logger('performance')

# Configure module-specific loggers
default_config.configure_module_loggers()


def setup_logging(app_name: str = "flash", 
                 log_dir: str = "logs",
                 log_level: str = "INFO") -> LoggerConfig:
    """Setup logging configuration"""
    config = LoggerConfig(
        app_name=app_name,
        log_dir=log_dir,
        log_level=log_level
    )
    config.configure_module_loggers()
    return config


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)