"""
Performance and load testing for FLASH API
"""
import time
import requests
import concurrent.futures
import statistics
import json
import random
from typing import List, Dict, Any, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


BASE_URL = "http://localhost:8001"
API_KEY = "test-api-key-123"


class PerformanceMetrics:
    """Track performance metrics"""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.status_codes: List[int] = []
        self.errors: List[str] = []
        self.start_time = time.time()
    
    def add_result(self, response_time: float, status_code: int, error: str = None):
        self.response_times.append(response_time)
        self.status_codes.append(status_code)
        if error:
            self.errors.append(error)
    
    def get_summary(self) -> Dict[str, Any]:
        if not self.response_times:
            return {"error": "No data collected"}
        
        duration = time.time() - self.start_time
        successful = len([s for s in self.status_codes if 200 <= s < 300])
        
        return {
            "duration_seconds": duration,
            "total_requests": len(self.response_times),
            "successful_requests": successful,
            "failed_requests": len(self.response_times) - successful,
            "error_rate": (len(self.response_times) - successful) / len(self.response_times) * 100,
            "requests_per_second": len(self.response_times) / duration,
            "response_times": {
                "min": min(self.response_times),
                "max": max(self.response_times),
                "mean": statistics.mean(self.response_times),
                "median": statistics.median(self.response_times),
                "p95": np.percentile(self.response_times, 95),
                "p99": np.percentile(self.response_times, 99)
            },
            "status_code_distribution": {
                code: self.status_codes.count(code) 
                for code in set(self.status_codes)
            },
            "errors": len(self.errors)
        }
    
    def plot_results(self, filename: str = "performance_results.png"):
        """Generate performance visualization"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Response time distribution
        ax1.hist(self.response_times, bins=50, alpha=0.7, color='blue')
        ax1.set_xlabel('Response Time (seconds)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Response Time Distribution')
        ax1.axvline(statistics.mean(self.response_times), color='red', 
                   linestyle='dashed', label=f'Mean: {statistics.mean(self.response_times):.3f}s')
        ax1.legend()
        
        # Response time over time
        ax2.plot(self.response_times, alpha=0.6)
        ax2.set_xlabel('Request Number')
        ax2.set_ylabel('Response Time (seconds)')
        ax2.set_title('Response Time Over Time')
        
        # Status code distribution
        status_counts = {}
        for code in set(self.status_codes):
            status_counts[str(code)] = self.status_codes.count(code)
        ax3.bar(status_counts.keys(), status_counts.values(), color='green')
        ax3.set_xlabel('Status Code')
        ax3.set_ylabel('Count')
        ax3.set_title('Status Code Distribution')
        
        # Percentiles
        percentiles = [50, 75, 90, 95, 99]
        percentile_values = [np.percentile(self.response_times, p) for p in percentiles]
        ax4.bar([f"p{p}" for p in percentiles], percentile_values, color='orange')
        ax4.set_xlabel('Percentile')
        ax4.set_ylabel('Response Time (seconds)')
        ax4.set_title('Response Time Percentiles')
        
        plt.tight_layout()
        plt.savefig(filename)
        print(f"Performance plot saved to {filename}")


def generate_test_startup() -> Dict[str, Any]:
    """Generate random startup data for testing"""
    stages = ["pre_seed", "seed", "series_a", "series_b", "series_c"]
    sectors = ["saas", "fintech", "healthtech", "edtech", "ecommerce"]
    
    return {
        "startup_name": f"TestStartup_{random.randint(1000, 9999)}",
        "funding_stage": random.choice(stages),
        "sector": random.choice(sectors),
        "total_capital_raised_usd": random.randint(100000, 10000000),
        "monthly_burn_usd": random.randint(10000, 500000),
        "runway_months": random.randint(6, 36),
        "team_size_full_time": random.randint(5, 100),
        "founders_count": random.randint(1, 4),
        "customer_count": random.randint(10, 10000),
        "annual_revenue_run_rate": random.randint(0, 5000000),
        "market_growth_rate_percent": random.uniform(-10, 100),
        "user_growth_rate_percent": random.uniform(-20, 200),
        "tech_differentiation_score": random.randint(1, 5),
        "scalability_score": random.randint(1, 5),
        "competition_intensity": random.randint(1, 5)
    }


def make_prediction_request() -> Tuple[float, int, str]:
    """Make a single prediction request"""
    headers = {"X-API-Key": API_KEY}
    data = generate_test_startup()
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/predict",
            headers=headers,
            json=data,
            timeout=30
        )
        response_time = time.time() - start_time
        
        return response_time, response.status_code, None
        
    except Exception as e:
        response_time = time.time() - start_time
        return response_time, 0, str(e)


class LoadTests:
    """Various load testing scenarios"""
    
    @staticmethod
    def test_single_user_sequential(num_requests: int = 100) -> PerformanceMetrics:
        """Test sequential requests from single user"""
        print(f"\n🔄 Running sequential test with {num_requests} requests...")
        metrics = PerformanceMetrics()
        
        for i in range(num_requests):
            response_time, status_code, error = make_prediction_request()
            metrics.add_result(response_time, status_code, error)
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{num_requests} requests completed")
        
        return metrics
    
    @staticmethod
    def test_concurrent_users(num_users: int = 10, requests_per_user: int = 10) -> PerformanceMetrics:
        """Test concurrent requests from multiple users"""
        print(f"\n👥 Running concurrent test with {num_users} users, "
              f"{requests_per_user} requests each...")
        metrics = PerformanceMetrics()
        
        def user_session(user_id: int):
            results = []
            for _ in range(requests_per_user):
                result = make_prediction_request()
                results.append(result)
            return results
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [
                executor.submit(user_session, i) 
                for i in range(num_users)
            ]
            
            for future in concurrent.futures.as_completed(futures):
                user_results = future.result()
                for response_time, status_code, error in user_results:
                    metrics.add_result(response_time, status_code, error)
        
        return metrics
    
    @staticmethod
    def test_spike_load(
        baseline_rps: int = 5,
        spike_rps: int = 50,
        duration_seconds: int = 60
    ) -> PerformanceMetrics:
        """Test sudden spike in traffic"""
        print(f"\n📈 Running spike test: {baseline_rps} RPS → {spike_rps} RPS")
        metrics = PerformanceMetrics()
        
        # Baseline period (first third)
        baseline_duration = duration_seconds // 3
        print(f"  Baseline period ({baseline_rps} RPS) for {baseline_duration}s...")
        LoadTests._generate_load(metrics, baseline_rps, baseline_duration)
        
        # Spike period (middle third)
        spike_duration = duration_seconds // 3
        print(f"  Spike period ({spike_rps} RPS) for {spike_duration}s...")
        LoadTests._generate_load(metrics, spike_rps, spike_duration)
        
        # Recovery period (last third)
        recovery_duration = duration_seconds - baseline_duration - spike_duration
        print(f"  Recovery period ({baseline_rps} RPS) for {recovery_duration}s...")
        LoadTests._generate_load(metrics, baseline_rps, recovery_duration)
        
        return metrics
    
    @staticmethod
    def test_sustained_load(target_rps: int = 20, duration_seconds: int = 300) -> PerformanceMetrics:
        """Test sustained load over time"""
        print(f"\n⏱️  Running sustained load test: {target_rps} RPS for {duration_seconds}s...")
        metrics = PerformanceMetrics()
        
        LoadTests._generate_load(metrics, target_rps, duration_seconds)
        
        return metrics
    
    @staticmethod
    def _generate_load(metrics: PerformanceMetrics, target_rps: int, duration_seconds: int):
        """Generate load at specified requests per second"""
        start_time = time.time()
        request_interval = 1.0 / target_rps
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(target_rps, 50)) as executor:
            futures = []
            
            while time.time() - start_time < duration_seconds:
                futures.append(executor.submit(make_prediction_request))
                time.sleep(request_interval)
                
                # Process completed futures
                done_futures = [f for f in futures if f.done()]
                for future in done_futures:
                    response_time, status_code, error = future.result()
                    metrics.add_result(response_time, status_code, error)
                    futures.remove(future)
            
            # Wait for remaining futures
            for future in concurrent.futures.as_completed(futures):
                response_time, status_code, error = future.result()
                metrics.add_result(response_time, status_code, error)


class CachePerformanceTest:
    """Test cache performance impact"""
    
    @staticmethod
    def test_cache_effectiveness(num_unique: int = 10, repeats: int = 10) -> Dict[str, Any]:
        """Test cache hit/miss performance"""
        print(f"\n💾 Testing cache effectiveness...")
        
        # Generate unique test data
        test_data = [generate_test_startup() for _ in range(num_unique)]
        headers = {"X-API-Key": API_KEY}
        
        # First pass - cache misses
        miss_times = []
        for data in test_data:
            start = time.time()
            response = requests.post(f"{BASE_URL}/predict", headers=headers, json=data)
            miss_times.append(time.time() - start)
        
        # Subsequent passes - cache hits
        hit_times = []
        for _ in range(repeats):
            for data in test_data:
                start = time.time()
                response = requests.post(f"{BASE_URL}/predict", headers=headers, json=data)
                hit_times.append(time.time() - start)
        
        return {
            "cache_miss_avg": statistics.mean(miss_times),
            "cache_hit_avg": statistics.mean(hit_times),
            "speedup_factor": statistics.mean(miss_times) / statistics.mean(hit_times),
            "miss_times": miss_times,
            "hit_times": hit_times
        }


def run_performance_tests():
    """Run comprehensive performance test suite"""
    print("🚀 FLASH API Performance Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API server not healthy")
            return
    except:
        print("❌ Cannot connect to API server at", BASE_URL)
        return
    
    results = {}
    
    # 1. Baseline Performance
    print("\n1️⃣ Baseline Performance Test")
    baseline = LoadTests.test_single_user_sequential(50)
    results["baseline"] = baseline.get_summary()
    print(f"✅ Average response time: {results['baseline']['response_times']['mean']:.3f}s")
    
    # 2. Concurrent Users
    print("\n2️⃣ Concurrent Users Test")
    concurrent = LoadTests.test_concurrent_users(20, 5)
    results["concurrent"] = concurrent.get_summary()
    print(f"✅ Requests per second: {results['concurrent']['requests_per_second']:.2f}")
    
    # 3. Cache Performance
    print("\n3️⃣ Cache Performance Test")
    cache_results = CachePerformanceTest.test_cache_effectiveness(5, 5)
    results["cache"] = cache_results
    print(f"✅ Cache speedup: {cache_results['speedup_factor']:.2f}x faster")
    
    # 4. Spike Test
    print("\n4️⃣ Traffic Spike Test")
    spike = LoadTests.test_spike_load(5, 30, 30)
    results["spike"] = spike.get_summary()
    print(f"✅ Handled spike with {results['spike']['error_rate']:.1f}% error rate")
    
    # 5. Sustained Load (optional - takes longer)
    # print("\n5️⃣ Sustained Load Test")
    # sustained = LoadTests.test_sustained_load(10, 60)
    # results["sustained"] = sustained.get_summary()
    
    # Generate visualizations
    baseline.plot_results("baseline_performance.png")
    concurrent.plot_results("concurrent_performance.png")
    spike.plot_results("spike_performance.png")
    
    # Save results
    with open("performance_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    # Print summary
    print("\n📊 Performance Test Summary")
    print("=" * 50)
    print(f"Baseline Response Time: {results['baseline']['response_times']['mean']:.3f}s")
    print(f"Concurrent RPS: {results['concurrent']['requests_per_second']:.2f}")
    print(f"Cache Speedup: {results['cache']['speedup_factor']:.2f}x")
    print(f"Spike Error Rate: {results['spike']['error_rate']:.1f}%")
    print(f"\nDetailed results saved to performance_results.json")
    
    # Performance recommendations
    print("\n💡 Performance Recommendations:")
    
    if results['baseline']['response_times']['mean'] > 1.0:
        print("  ⚠️  Baseline response time >1s - consider optimization")
    
    if results['concurrent']['error_rate'] > 5:
        print("  ⚠️  High error rate under concurrent load - check connection limits")
    
    if results['cache']['speedup_factor'] < 2:
        print("  ⚠️  Cache speedup <2x - verify Redis is working")
    
    if results['spike']['response_times']['p99'] > 5:
        print("  ⚠️  P99 >5s during spike - consider auto-scaling")


if __name__ == "__main__":
    run_performance_tests()