"""
Distributed Systems Resilience Layer
Implements research-grade patterns for handling distributed system failures

Author: FLASH CTO
Patterns implemented:
1. Exponential Backoff with Jitter
2. Circuit Breaker Pattern
3. Request Hedging (Backup Requests)
4. Graceful Degradation
5. Adaptive Timeout Management
"""

import asyncio
import time
import random
import logging
from typing import Optional, Callable, Any, Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
from collections import deque
import hashlib
import json

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 60  # seconds
    half_open_max_calls: int = 3
    success_threshold: int = 2


@dataclass
class BackoffConfig:
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class HedgingConfig:
    delay: float = 2.0  # Delay before sending backup request
    max_hedged_requests: int = 2


@dataclass
class RequestMetrics:
    """Track request performance metrics"""
    success_count: int = 0
    failure_count: int = 0
    total_latency: float = 0.0
    latencies: deque = field(default_factory=lambda: deque(maxlen=100))
    
    @property
    def avg_latency(self) -> float:
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)
    
    @property
    def p95_latency(self) -> float:
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx] if idx < len(sorted_latencies) else sorted_latencies[-1]


class CircuitBreaker:
    """Implements the Circuit Breaker pattern"""
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        
    def call_succeeded(self):
        """Record successful call"""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                logger.info("Circuit breaker closed - service recovered")
        
    def call_failed(self):
        """Record failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
        elif self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning("Circuit breaker reopened - service still failing")
            
    def can_execute(self) -> bool:
        """Check if request can be executed"""
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            if (time.time() - self.last_failure_time) > self.config.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                self.success_count = 0
                logger.info("Circuit breaker half-open - testing recovery")
                return True
            return False
            
        # HALF_OPEN state
        if self.half_open_calls < self.config.half_open_max_calls:
            self.half_open_calls += 1
            return True
        return False


class ExponentialBackoff:
    """Implements exponential backoff with jitter"""
    
    def __init__(self, config: BackoffConfig):
        self.config = config
        
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        delay = min(
            self.config.initial_delay * (self.config.exponential_base ** attempt),
            self.config.max_delay
        )
        
        if self.config.jitter:
            # Add jitter to prevent thundering herd
            delay = delay * (0.5 + random.random() * 0.5)
            
        return delay


class RequestHedger:
    """Implements request hedging (backup requests)"""
    
    def __init__(self, config: HedgingConfig):
        self.config = config
        
    async def execute_with_hedging(
        self, 
        primary_func: Callable, 
        *args, 
        **kwargs
    ) -> Tuple[Any, bool]:
        """
        Execute request with hedging
        Returns (result, was_hedged)
        """
        # Create tasks for primary and hedged requests
        tasks = []
        
        # Primary request
        primary_task = asyncio.create_task(primary_func(*args, **kwargs))
        tasks.append(("primary", primary_task))
        
        # Schedule hedged requests
        for i in range(self.config.max_hedged_requests):
            delay = self.config.delay * (i + 1)
            hedged_task = asyncio.create_task(
                self._delayed_request(delay, primary_func, *args, **kwargs)
            )
            tasks.append((f"hedged_{i}", hedged_task))
        
        # Wait for first successful response
        try:
            for task_name, task in tasks:
                try:
                    result = await asyncio.wait_for(task, timeout=None)
                    # Cancel remaining tasks
                    for other_name, other_task in tasks:
                        if other_name != task_name and not other_task.done():
                            other_task.cancel()
                    
                    was_hedged = task_name != "primary"
                    if was_hedged:
                        logger.info(f"Hedged request succeeded: {task_name}")
                    
                    return result, was_hedged
                except Exception as e:
                    logger.debug(f"Request {task_name} failed: {e}")
                    continue
                    
            raise Exception("All hedged requests failed")
            
        finally:
            # Ensure all tasks are cancelled
            for _, task in tasks:
                if not task.done():
                    task.cancel()
    
    async def _delayed_request(self, delay: float, func: Callable, *args, **kwargs):
        """Execute request after delay"""
        await asyncio.sleep(delay)
        return await func(*args, **kwargs)


class AdaptiveTimeout:
    """Implements adaptive timeout based on request latencies"""
    
    def __init__(self, min_timeout: float = 5.0, max_timeout: float = 60.0):
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self.metrics = RequestMetrics()
        
    def get_timeout(self) -> float:
        """Calculate timeout based on recent performance"""
        if len(self.metrics.latencies) < 10:
            # Not enough data, use default
            return 30.0
            
        # Use P95 latency with 50% buffer
        p95 = self.metrics.p95_latency
        timeout = p95 * 1.5
        
        # Clamp to min/max
        return max(self.min_timeout, min(timeout, self.max_timeout))
        
    def record_latency(self, latency: float):
        """Record request latency"""
        self.metrics.latencies.append(latency)


class ResilienceLayer:
    """
    Comprehensive resilience layer combining all patterns
    """
    
    def __init__(
        self,
        circuit_breaker_config: Optional[CircuitBreakerConfig] = None,
        backoff_config: Optional[BackoffConfig] = None,
        hedging_config: Optional[HedgingConfig] = None,
        enable_adaptive_timeout: bool = True
    ):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.circuit_breaker_config = circuit_breaker_config or CircuitBreakerConfig()
        
        self.backoff = ExponentialBackoff(backoff_config or BackoffConfig())
        self.hedger = RequestHedger(hedging_config or HedgingConfig())
        
        self.adaptive_timeouts: Dict[str, AdaptiveTimeout] = {}
        self.enable_adaptive_timeout = enable_adaptive_timeout
        
        self.partial_results: Dict[str, Any] = {}
        
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service"""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker(self.circuit_breaker_config)
        return self.circuit_breakers[service_name]
        
    def get_adaptive_timeout(self, service_name: str) -> AdaptiveTimeout:
        """Get or create adaptive timeout for service"""
        if service_name not in self.adaptive_timeouts:
            self.adaptive_timeouts[service_name] = AdaptiveTimeout()
        return self.adaptive_timeouts[service_name]
        
    async def execute_with_resilience(
        self,
        service_name: str,
        func: Callable,
        *args,
        fallback: Optional[Callable] = None,
        enable_hedging: bool = True,
        max_retries: int = 3,
        partial_result_key: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Execute function with full resilience patterns
        
        Args:
            service_name: Name of the service being called
            func: Async function to execute
            fallback: Optional fallback function if all retries fail
            enable_hedging: Whether to use request hedging
            max_retries: Maximum number of retry attempts
            partial_result_key: Key to store partial results for graceful degradation
        """
        circuit_breaker = self.get_circuit_breaker(service_name)
        
        # Check circuit breaker
        if not circuit_breaker.can_execute():
            logger.warning(f"Circuit breaker OPEN for {service_name}")
            if fallback:
                return await fallback(*args, **kwargs)
            raise Exception(f"Service {service_name} unavailable (circuit open)")
        
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            try:
                start_time = time.time()
                
                # Get adaptive timeout
                timeout = 30.0  # default
                if self.enable_adaptive_timeout:
                    adaptive_timeout = self.get_adaptive_timeout(service_name)
                    timeout = adaptive_timeout.get_timeout()
                
                # Execute with hedging if enabled
                if enable_hedging and attempt == 0:  # Only hedge on first attempt
                    result, was_hedged = await self.hedger.execute_with_hedging(
                        self._execute_with_timeout,
                        func, args, kwargs, timeout
                    )
                else:
                    result = await self._execute_with_timeout(func, args, kwargs, timeout)
                
                # Record success
                latency = time.time() - start_time
                circuit_breaker.call_succeeded()
                
                if self.enable_adaptive_timeout:
                    adaptive_timeout.record_latency(latency)
                
                # Store partial result for graceful degradation
                if partial_result_key:
                    self.partial_results[partial_result_key] = result
                
                logger.info(f"Request to {service_name} succeeded in {latency:.2f}s")
                return result
                
            except Exception as e:
                last_error = e
                attempt += 1
                
                # Record failure
                circuit_breaker.call_failed()
                
                if attempt < max_retries:
                    # Calculate backoff delay
                    delay = self.backoff.get_delay(attempt - 1)
                    logger.warning(
                        f"Request to {service_name} failed (attempt {attempt}/{max_retries}), "
                        f"retrying in {delay:.2f}s: {str(e)}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All retries failed for {service_name}: {str(e)}")
        
        # All retries failed
        if fallback:
            logger.info(f"Using fallback for {service_name}")
            return await fallback(*args, **kwargs)
        
        # Try graceful degradation with partial results
        if partial_result_key and partial_result_key in self.partial_results:
            logger.warning(f"Using cached partial result for {service_name}")
            return self.partial_results[partial_result_key]
        
        raise last_error or Exception(f"Failed to execute {service_name}")
    
    async def _execute_with_timeout(self, func: Callable, args: tuple, kwargs: dict, timeout: float):
        """Execute function with timeout"""
        return await asyncio.wait_for(
            func(*args, **kwargs),
            timeout=timeout
        )
    
    def get_service_health(self, service_name: str) -> Dict[str, Any]:
        """Get health metrics for a service"""
        circuit_breaker = self.circuit_breakers.get(service_name)
        adaptive_timeout = self.adaptive_timeouts.get(service_name)
        
        health = {
            "service": service_name,
            "circuit_state": circuit_breaker.state.value if circuit_breaker else "unknown",
            "failure_count": circuit_breaker.failure_count if circuit_breaker else 0,
        }
        
        if adaptive_timeout and adaptive_timeout.metrics.latencies:
            health.update({
                "avg_latency": adaptive_timeout.metrics.avg_latency,
                "p95_latency": adaptive_timeout.metrics.p95_latency,
                "current_timeout": adaptive_timeout.get_timeout()
            })
            
        return health


# Example usage for Michelin Analysis
async def create_resilient_michelin_client():
    """Create a Michelin API client with resilience patterns"""
    
    resilience = ResilienceLayer(
        circuit_breaker_config=CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=30,
            half_open_max_calls=2
        ),
        backoff_config=BackoffConfig(
            initial_delay=0.5,
            max_delay=30.0,
            exponential_base=2.0,
            jitter=True
        ),
        hedging_config=HedgingConfig(
            delay=3.0,  # Start hedging after 3 seconds
            max_hedged_requests=1
        ),
        enable_adaptive_timeout=True
    )
    
    return resilience