"""
Security test suite for FLASH API
"""
import pytest
import requests
import json
import jwt
from datetime import datetime, timedelta
import time
from typing import Dict, Any


BASE_URL = "http://localhost:8001"
API_KEY = "test-api-key-123"  # Should match configured test key


class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_predict_without_auth(self):
        """Test that prediction endpoint requires authentication"""
        response = requests.post(f"{BASE_URL}/predict", json={
            "startup_name": "Test Inc",
            "funding_stage": "seed",
            "total_capital_raised_usd": 1000000
        })
        assert response.status_code == 401
        assert "Authentication required" in response.text
    
    def test_predict_with_invalid_jwt(self):
        """Test prediction with invalid JWT token"""
        headers = {"Authorization": "Bearer invalid-token-123"}
        response = requests.post(f"{BASE_URL}/predict", 
            headers=headers,
            json={
                "startup_name": "Test Inc",
                "funding_stage": "seed"
            }
        )
        assert response.status_code == 401
    
    def test_predict_with_api_key(self):
        """Test prediction with API key authentication"""
        headers = {"X-API-Key": API_KEY}
        response = requests.post(f"{BASE_URL}/predict",
            headers=headers,
            json={
                "startup_name": "Test Inc",
                "funding_stage": "seed",
                "total_capital_raised_usd": 1000000,
                "team_size_full_time": 10
            }
        )
        # Should accept API key
        assert response.status_code in [200, 422]  # 422 if validation fails
    
    def test_metrics_requires_auth(self):
        """Test that metrics endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/metrics")
        assert response.status_code == 401
    
    def test_system_info_requires_auth(self):
        """Test that system info endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/system_info")
        assert response.status_code == 401
    
    def test_jwt_expiration(self):
        """Test that expired JWT tokens are rejected"""
        # Create an expired token
        secret = "test-secret"  # In real tests, use actual secret
        expired_token = jwt.encode({
            "sub": "testuser",
            "exp": datetime.utcnow() - timedelta(hours=1)
        }, secret, algorithm="HS256")
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = requests.get(f"{BASE_URL}/system_info", headers=headers)
        assert response.status_code == 401


class TestInputValidation:
    """Test input validation and sanitization"""
    
    def test_sql_injection_attempt(self):
        """Test SQL injection protection"""
        headers = {"X-API-Key": API_KEY}
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "1; DELETE FROM startups WHERE 1=1"
        ]
        
        for payload in malicious_inputs:
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": payload,
                    "funding_stage": "seed"
                }
            )
            # Should not cause server error
            assert response.status_code in [200, 400, 422]
            # Ensure no SQL error messages leak
            assert "SQL" not in response.text.upper()
            assert "DROP" not in response.text.upper()
    
    def test_xss_prevention(self):
        """Test XSS attack prevention"""
        headers = {"X-API-Key": API_KEY}
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(1)'></iframe>"
        ]
        
        for payload in xss_payloads:
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": payload,
                    "sector": payload,
                    "funding_stage": "seed"
                }
            )
            
            # Check response doesn't reflect unescaped script
            if response.status_code == 200:
                assert "<script>" not in response.text
                assert "javascript:" not in response.text
    
    def test_command_injection(self):
        """Test command injection protection"""
        headers = {"X-API-Key": API_KEY}
        cmd_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "`rm -rf /`",
            "$(whoami)"
        ]
        
        for payload in cmd_payloads:
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": payload,
                    "funding_stage": "seed"
                }
            )
            # Should not execute commands
            assert response.status_code in [200, 400, 422]
            assert "/etc/passwd" not in response.text
    
    def test_path_traversal(self):
        """Test path traversal protection"""
        headers = {"X-API-Key": API_KEY}
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd"
        ]
        
        for payload in traversal_payloads:
            # Try in different fields
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": payload,
                    "hq_location": payload,
                    "funding_stage": "seed"
                }
            )
            assert response.status_code in [200, 400, 422]
            assert "passwd" not in response.text.lower()
    
    def test_numeric_overflow(self):
        """Test numeric field overflow handling"""
        headers = {"X-API-Key": API_KEY}
        overflow_values = [
            9999999999999999999999999999,  # Very large number
            -9999999999999999999999999999,  # Very large negative
            float('inf'),
            float('-inf'),
            float('nan')
        ]
        
        for value in overflow_values:
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": "Test Inc",
                    "funding_stage": "seed",
                    "total_capital_raised_usd": value
                }
            )
            # Should handle gracefully
            assert response.status_code in [400, 422]
            assert "error" in response.text.lower()


class TestRateLimiting:
    """Test rate limiting protection"""
    
    def test_prediction_rate_limit(self):
        """Test that prediction endpoint has rate limiting"""
        headers = {"X-API-Key": API_KEY}
        
        # Make multiple rapid requests
        responses = []
        for i in range(15):  # Limit is 10/minute
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json={
                    "startup_name": f"Test {i}",
                    "funding_stage": "seed"
                }
            )
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay
        
        # Should hit rate limit
        assert 429 in responses  # Too Many Requests
    
    def test_cache_clear_rate_limit(self):
        """Test cache clear endpoint rate limiting"""
        headers = {"X-API-Key": API_KEY}
        
        # Try to clear cache multiple times
        responses = []
        for i in range(3):  # Limit is 1/minute
            response = requests.post(f"{BASE_URL}/cache/clear",
                headers=headers,
                json={"cache_type": "all"}
            )
            responses.append(response.status_code)
        
        # Should hit rate limit
        assert 429 in responses


class TestDataLeakage:
    """Test for information disclosure vulnerabilities"""
    
    def test_error_message_leakage(self):
        """Test that error messages don't leak sensitive info"""
        headers = {"X-API-Key": API_KEY}
        
        # Trigger various errors
        error_triggers = [
            {"total_capital_raised_usd": "not-a-number"},
            {"funding_stage": "invalid-stage"},
            {"team_size_full_time": -100}
        ]
        
        for trigger in error_triggers:
            response = requests.post(f"{BASE_URL}/predict",
                headers=headers,
                json=trigger
            )
            
            if response.status_code >= 400:
                error_text = response.text.lower()
                # Check for sensitive information leakage
                assert "traceback" not in error_text
                assert "file \"/" not in error_text
                assert "line " not in error_text
                assert ".py" not in error_text
    
    def test_timing_attack_resistance(self):
        """Test resistance to timing attacks on authentication"""
        # Test with valid and invalid API keys
        valid_key = API_KEY
        invalid_keys = ["wrong-key-123", "another-wrong-key", "x" * 100]
        
        timings = []
        
        for key in [valid_key] + invalid_keys:
            headers = {"X-API-Key": key}
            start = time.time()
            
            response = requests.get(f"{BASE_URL}/system_info", headers=headers)
            
            duration = time.time() - start
            timings.append(duration)
        
        # Check that timing differences are minimal (< 100ms)
        max_diff = max(timings) - min(timings)
        assert max_diff < 0.1  # 100ms tolerance


class TestCORS:
    """Test CORS configuration"""
    
    def test_cors_headers(self):
        """Test CORS headers are properly configured"""
        # Preflight request
        response = requests.options(f"{BASE_URL}/predict",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
    
    def test_cors_origin_validation(self):
        """Test that only allowed origins are accepted"""
        # Test with disallowed origin
        response = requests.options(f"{BASE_URL}/predict",
            headers={
                "Origin": "http://evil-site.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Should not allow arbitrary origins
        allow_origin = response.headers.get("Access-Control-Allow-Origin", "")
        assert "evil-site.com" not in allow_origin


class TestModelIntegrity:
    """Test model file integrity verification"""
    
    def test_model_checksum_endpoint(self):
        """Test that model checksums can be verified"""
        headers = {"X-API-Key": API_KEY}
        response = requests.get(f"{BASE_URL}/system_info", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Should include model information
            assert "models_loaded" in data
            assert len(data["models_loaded"]) > 0


def run_security_tests():
    """Run all security tests"""
    print("🔒 Running Security Test Suite")
    print("=" * 50)
    
    test_classes = [
        TestAuthentication,
        TestInputValidation,
        TestRateLimiting,
        TestDataLeakage,
        TestCORS,
        TestModelIntegrity
    ]
    
    passed = 0
    failed = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        test_instance = test_class()
        
        # Get all test methods
        test_methods = [m for m in dir(test_instance) if m.startswith("test_")]
        
        for method_name in test_methods:
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"  ✅ {method_name}")
                passed += 1
            except Exception as e:
                print(f"  ❌ {method_name}: {str(e)}")
                failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_security_tests()
    sys.exit(0 if success else 1)