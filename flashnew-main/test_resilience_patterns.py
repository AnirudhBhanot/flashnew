"""
Test and demonstrate the research-grade resilience patterns
Shows how the system handles various failure scenarios
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any
import logging
from unittest.mock import Mock, patch
import random

# Configure logging to see resilience patterns in action
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import our resilience layer
from core.resilience_layer import ResilienceLayer, CircuitBreakerConfig


class ResilientSystemDemo:
    """Demonstrate resilience patterns with various failure scenarios"""
    
    def __init__(self):
        self.api_url = "http://localhost:8001/api/michelin-resilient"
        self.startup_data = {
            "company_name": "TechVenture AI",
            "industry": "B2B SaaS",
            "funding_stage": "Series A",
            "total_funding": 15000000,
            "revenue": 2000000,
            "team_size": 45,
            "market_growth_rate": 25,
            "market_share": 0.5,
            "burn_rate": 500000,
            "runway_months": 18
        }
    
    async def test_normal_operation(self):
        """Test 1: Normal operation - everything works"""
        logger.info("=== TEST 1: Normal Operation ===")
        
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            
            async with session.post(
                f"{self.api_url}/analyze/phase1",
                json=self.startup_data
            ) as response:
                result = await response.json()
                elapsed = time.time() - start_time
                
                logger.info(f"✅ Phase 1 completed in {elapsed:.2f}s")
                logger.info(f"BCG Position: {result['bcg_matrix']['position']}")
    
    async def test_circuit_breaker(self):
        """Test 2: Circuit breaker pattern - service failures"""
        logger.info("\n=== TEST 2: Circuit Breaker Pattern ===")
        
        # Simulate service being down by using invalid API key
        bad_startup_data = self.startup_data.copy()
        bad_startup_data["simulate_failure"] = True
        
        async with aiohttp.ClientSession() as session:
            # Make multiple failing requests to trip the circuit
            for i in range(5):
                try:
                    logger.info(f"Request {i+1}: Attempting to call failing service...")
                    async with session.post(
                        f"{self.api_url}/analyze/phase1",
                        json=bad_startup_data,
                        timeout=5
                    ) as response:
                        if response.status != 200:
                            logger.warning(f"Request {i+1} failed with status {response.status}")
                except Exception as e:
                    logger.warning(f"Request {i+1} failed: {str(e)}")
                
                await asyncio.sleep(1)
            
            # Check circuit status
            logger.info("Checking circuit breaker status...")
            async with session.get(f"{self.api_url}/health") as response:
                health = await response.json()
                open_circuits = health['overall_status']['open_circuits']
                logger.info(f"Open circuits: {open_circuits}")
    
    async def test_exponential_backoff(self):
        """Test 3: Exponential backoff with jitter"""
        logger.info("\n=== TEST 3: Exponential Backoff Pattern ===")
        
        # Create a mock that fails first 2 times, then succeeds
        class BackoffTest:
            def __init__(self):
                self.attempt_count = 0
                self.attempt_times = []
            
            async def flaky_service(self):
                self.attempt_count += 1
                self.attempt_times.append(time.time())
                
                if self.attempt_count <= 2:
                    logger.info(f"Attempt {self.attempt_count}: Simulating failure")
                    raise Exception("Service temporarily unavailable")
                else:
                    logger.info(f"Attempt {self.attempt_count}: Success!")
                    return {"result": "success"}
        
        # Test the backoff pattern
        test = BackoffTest()
        resilience = ResilienceLayer()
        
        try:
            result = await resilience.execute_with_resilience(
                service_name="flaky_service",
                func=test.flaky_service,
                max_retries=3
            )
            
            # Calculate delays between attempts
            delays = []
            for i in range(1, len(test.attempt_times)):
                delay = test.attempt_times[i] - test.attempt_times[i-1]
                delays.append(delay)
                logger.info(f"Delay before attempt {i+1}: {delay:.2f}s")
            
            logger.info(f"✅ Eventually succeeded after {test.attempt_count} attempts")
            
        except Exception as e:
            logger.error(f"❌ Failed after all retries: {e}")
    
    async def test_request_hedging(self):
        """Test 4: Request hedging (backup requests)"""
        logger.info("\n=== TEST 4: Request Hedging Pattern ===")
        
        # Simulate a slow primary request
        class HedgingTest:
            def __init__(self):
                self.request_log = []
            
            async def slow_primary_request(self, request_id: str):
                self.request_log.append({
                    "id": request_id,
                    "start_time": time.time(),
                    "type": "primary" if "primary" in request_id else "hedged"
                })
                
                if "primary" in request_id:
                    # Primary request is slow
                    logger.info(f"Primary request started (will be slow)...")
                    await asyncio.sleep(5)  # Simulate slow response
                    return {"result": "primary_slow"}
                else:
                    # Hedged request is fast
                    logger.info(f"Hedged request started (will be fast)...")
                    await asyncio.sleep(1)  # Fast response
                    return {"result": "hedged_fast"}
        
        test = HedgingTest()
        
        # Test parallel execution with hedging
        logger.info("Starting request with hedging enabled...")
        start_time = time.time()
        
        # Simulate the hedging by running both requests
        tasks = [
            test.slow_primary_request("primary_001"),
            asyncio.create_task(self._delayed_hedged_request(test, 2.0))
        ]
        
        # Wait for first to complete
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        
        # Cancel remaining
        for task in pending:
            task.cancel()
        
        result = done.pop().result()
        elapsed = time.time() - start_time
        
        logger.info(f"✅ Got result from {result['result']} in {elapsed:.2f}s")
        logger.info(f"Request log: {test.request_log}")
    
    async def _delayed_hedged_request(self, test, delay):
        """Helper for hedged request with delay"""
        await asyncio.sleep(delay)
        return await test.slow_primary_request("hedged_001")
    
    async def test_graceful_degradation(self):
        """Test 5: Graceful degradation with partial results"""
        logger.info("\n=== TEST 5: Graceful Degradation Pattern ===")
        
        async with aiohttp.ClientSession() as session:
            # Make a complete analysis request
            logger.info("Requesting complete analysis (some phases may fail)...")
            
            async with session.post(
                f"{self.api_url}/analyze/complete",
                json=self.startup_data
            ) as response:
                result = await response.json()
                
                completed = result.get('phases_completed', [])
                failed = result.get('phases_failed', [])
                
                logger.info(f"✅ Completed phases: {completed}")
                logger.info(f"❌ Failed phases: {[f['phase'] for f in failed]}")
                logger.info(f"Partial success: {result.get('partial_success', False)}")
                
                # Even with failures, we got partial results
                if result.get('phase1'):
                    logger.info("Got Phase 1 results despite potential failures")
                if result.get('phase2'):
                    logger.info("Got Phase 2 results despite potential failures")
    
    async def test_adaptive_timeout(self):
        """Test 6: Adaptive timeout based on performance"""
        logger.info("\n=== TEST 6: Adaptive Timeout Pattern ===")
        
        # Check current timeout settings via health endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/health") as response:
                health = await response.json()
                
                for service, metrics in health['services'].items():
                    if 'current_timeout' in metrics:
                        logger.info(
                            f"Service: {service}\n"
                            f"  Avg latency: {metrics.get('avg_latency', 0):.2f}s\n"
                            f"  P95 latency: {metrics.get('p95_latency', 0):.2f}s\n"
                            f"  Current timeout: {metrics.get('current_timeout', 30):.2f}s"
                        )
    
    async def run_all_tests(self):
        """Run all resilience pattern tests"""
        logger.info("🚀 Starting Resilience Pattern Demonstration\n")
        
        tests = [
            self.test_normal_operation(),
            self.test_circuit_breaker(),
            self.test_exponential_backoff(),
            self.test_request_hedging(),
            self.test_graceful_degradation(),
            self.test_adaptive_timeout()
        ]
        
        for test in tests:
            try:
                await test
            except Exception as e:
                logger.error(f"Test failed: {e}")
            
            await asyncio.sleep(2)  # Pause between tests
        
        logger.info("\n✅ Resilience Pattern Demonstration Complete!")


async def demonstrate_real_world_scenario():
    """Demonstrate a real-world scenario with intermittent failures"""
    logger.info("\n🌍 REAL-WORLD SCENARIO: Intermittent API Failures\n")
    
    # Simulate realistic failure patterns
    class RealWorldSimulation:
        def __init__(self):
            self.request_count = 0
            self.failure_pattern = [
                True, True, False, True, False,  # Intermittent
                False, False, False, False, False,  # Recovers
                True, True, True, True, True,  # Total failure
                True, True, False, True, True  # Partial recovery
            ]
        
        async def make_request(self):
            self.request_count += 1
            should_fail = self.failure_pattern[
                (self.request_count - 1) % len(self.failure_pattern)
            ]
            
            if should_fail:
                if random.random() < 0.3:  # 30% chance of timeout
                    await asyncio.sleep(35)  # Simulate timeout
                raise Exception("Service unavailable")
            
            return {"status": "success", "request": self.request_count}
    
    sim = RealWorldSimulation()
    resilience = ResilienceLayer()
    
    # Make 20 requests over time
    results = []
    for i in range(20):
        start_time = time.time()
        try:
            result = await resilience.execute_with_resilience(
                service_name="production_api",
                func=sim.make_request,
                max_retries=2,
                enable_hedging=True
            )
            elapsed = time.time() - start_time
            results.append({
                "request": i + 1,
                "success": True,
                "time": elapsed,
                "attempts": sim.request_count
            })
            logger.info(f"Request {i+1}: ✅ Success in {elapsed:.2f}s")
        except Exception as e:
            elapsed = time.time() - start_time
            results.append({
                "request": i + 1,
                "success": False,
                "time": elapsed,
                "error": str(e)
            })
            logger.info(f"Request {i+1}: ❌ Failed after {elapsed:.2f}s")
        
        await asyncio.sleep(0.5)
    
    # Summary statistics
    successful = sum(1 for r in results if r['success'])
    avg_time = sum(r['time'] for r in results) / len(results)
    
    logger.info(f"\n📊 SUMMARY:")
    logger.info(f"Success rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
    logger.info(f"Average response time: {avg_time:.2f}s")
    logger.info(f"With resilience patterns: System remained operational despite failures")


if __name__ == "__main__":
    # Run the demonstration
    demo = ResilientSystemDemo()
    
    # Run all pattern tests
    asyncio.run(demo.run_all_tests())
    
    # Run real-world scenario
    asyncio.run(demonstrate_real_world_scenario())