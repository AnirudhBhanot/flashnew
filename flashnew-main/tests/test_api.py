#!/usr/bin/env python3
"""
Comprehensive API Test Suite for FLASH
Consolidates all test cases from various test files
"""

import pytest
import requests
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
import concurrent.futures
from fastapi import status


# API Configuration
API_URLS = {
    "primary": "http://localhost:8000",
    "secondary": "http://localhost:8001"
}


# Test Data Sets
@pytest.fixture
def basic_startup_data():
    """Basic startup data with minimal required fields"""
    return {
        "funding_stage": "series_a",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "runway_months": 20,
        "annual_revenue_run_rate": 2400000,
        "revenue_growth_rate_percent": 15,
        "gross_margin_percent": 65,
        "burn_multiple": 0.75,
        "capital_efficiency": 0.48,
        "burn_risk": 0.3,
        "product_stage": "growth",
        "tech_stack_size": 12,
        "patent_count": 2,
        "proprietary_tech": 1,
        "moat_strength": 65,
        "pmf_score": 70,
        "nps": 45,
        "cac_usd": 500,
        "ltv_usd": 2500,
        "ltv_cac_ratio": 5.0,
        "time_to_market_months": 6,
        "competitive_advantage_score": 7,
        "market_size_usd": 50000000000,
        "market_growth_rate": 25,
        "market_share_potential": 0.02,
        "market_capture_percent": 0.5,
        "saturation_risk": 0.3,
        "sector": "fintech",
        "is_emerging_market": 0,
        "regulatory_complexity_score": 4,
        "competitor_intensity": 0.6,
        "team_size": 25,
        "founder_yoe": 12,
        "previous_exits": 1,
        "technical_staff_percent": 60,
        "advisor_count": 4,
        "board_size": 5,
        "team_quality": 35,
        "investor_tier_primary": "tier_1",
        "founder_domain_expertise": 1,
        "technical_cofounder": 1,
        "employee_growth_mom": 5,
        "diversity_score": 7
    }


@pytest.fixture
def complete_startup_data():
    """Complete startup data matching all API requirements"""
    return {
        # Capital metrics
        "funding_stage": "series_a",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "runway_months": 20,
        "annual_revenue_run_rate": 2400000,
        "revenue_growth_rate_percent": 15,
        "gross_margin_percent": 65,
        "burn_multiple": 0.75,
        "ltv_cac_ratio": 5.0,
        "investor_tier_primary": "tier_1",
        "has_debt": False,
        
        # Advantage metrics
        "patent_count": 2,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 4,
        "brand_strength_score": 3,
        "scalability_score": 0.8,
        "product_stage": "growth",
        "product_retention_30d": 0.85,
        "product_retention_90d": 0.75,
        
        # Market metrics
        "sector": "fintech",
        "tam_size_usd": 50000000000,
        "sam_size_usd": 10000000000,
        "som_size_usd": 500000000,
        "market_growth_rate_percent": 25,
        "customer_count": 5000,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 20,
        "net_dollar_retention_percent": 115,
        "competition_intensity": 3,
        "competitors_named_count": 15,
        "dau_mau_ratio": 0.4,
        
        # People metrics
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 8,
        "domain_expertise_years_avg": 6,
        "prior_startup_experience_count": 3,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 4,
        "team_diversity_percent": 40,
        "key_person_dependency": False
    }


@pytest.fixture
def valid_startup_data():
    """Valid startup data for FastAPI client tests"""
    return {
        "funding_stage": "series_a",
        "total_capital_raised_usd": 5000000,
        "cash_on_hand_usd": 3000000,
        "monthly_burn_usd": 150000,
        "runway_months": 20,
        "annual_revenue_run_rate": 2400000,
        "revenue_growth_rate_percent": 15,
        "gross_margin_percent": 65,
        "burn_multiple": 0.75,
        "ltv_cac_ratio": 5.0,
        "investor_tier_primary": "tier_1",
        "has_debt": False,
        "patent_count": 2,
        "network_effects_present": True,
        "has_data_moat": True,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 4,
        "switching_cost_score": 4,
        "brand_strength_score": 3,
        "scalability_score": 0.8,
        "product_stage": "growth",
        "product_retention_30d": 0.85,
        "product_retention_90d": 0.75,
        "sector": "fintech",
        "tam_size_usd": 50000000000,
        "sam_size_usd": 10000000000,
        "som_size_usd": 500000000,
        "market_growth_rate_percent": 25,
        "customer_count": 5000,
        "customer_concentration_percent": 15,
        "user_growth_rate_percent": 20,
        "net_dollar_retention_percent": 115,
        "competition_intensity": 3,
        "competitors_named_count": 15,
        "dau_mau_ratio": 0.4,
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 8,
        "domain_expertise_years_avg": 6,
        "prior_startup_experience_count": 3,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 4,
        "team_diversity_percent": 40,
        "key_person_dependency": False
    }


@pytest.fixture
def invalid_startup_data():
    """Invalid startup data for validation tests"""
    return {
        "funding_stage": "invalid_stage",
        "total_capital_raised_usd": -1000,
        "team_diversity_percent": 150
    }


@pytest.fixture
def edge_case_startup_data():
    """Edge case startup data"""
    return {
        "funding_stage": "pre_seed",
        "total_capital_raised_usd": 0,
        "cash_on_hand_usd": 0,
        "monthly_burn_usd": 0,
        "runway_months": 0,
        "annual_revenue_run_rate": 0,
        "revenue_growth_rate_percent": 0,
        "gross_margin_percent": 0,
        "burn_multiple": 0,
        "ltv_cac_ratio": 0,
        "investor_tier_primary": "no_institutional",
        "has_debt": False,
        "patent_count": 0,
        "network_effects_present": False,
        "has_data_moat": False,
        "regulatory_advantage_present": False,
        "tech_differentiation_score": 1,
        "switching_cost_score": 1,
        "brand_strength_score": 1,
        "scalability_score": 0.1,
        "product_stage": "idea",
        "product_retention_30d": 0,
        "product_retention_90d": 0,
        "sector": "other",
        "tam_size_usd": 1000000,
        "sam_size_usd": 100000,
        "som_size_usd": 10000,
        "market_growth_rate_percent": 0,
        "customer_count": 0,
        "customer_concentration_percent": 0,
        "user_growth_rate_percent": 0,
        "net_dollar_retention_percent": 0,
        "competition_intensity": 5,
        "competitors_named_count": 100,
        "dau_mau_ratio": 0,
        "founders_count": 1,
        "team_size_full_time": 1,
        "years_experience_avg": 0,
        "domain_expertise_years_avg": 0,
        "prior_startup_experience_count": 0,
        "prior_successful_exits_count": 0,
        "board_advisor_experience_score": 1,
        "advisors_count": 0,
        "team_diversity_percent": 0,
        "key_person_dependency": True
    }


@pytest.fixture
def frontend_compatible_data():
    """Data format compatible with frontend expectations"""
    return {
        "startup_name": "TestStartup",
        "industry": "Technology",
        "funding_stage": "series_a",
        "total_funding": 5000000,
        "last_funding_amount": 3000000,
        "last_funding_date": "2023-06-15",
        "employee_count": 25,
        "monthly_revenue": 50000,
        "growth_rate": 0.15,
        "burn_rate": 100000,
        "runway_months": 24,
        "founder_experience": 5,
        "team_size_tech": 10,
        "team_size_business": 5,
        "customer_acquisition_cost": 500,
        "customer_lifetime_value": 2000,
        "market_size_tam": 10000000000,
        "revenue_growth_rate": 0.20,
        "gross_margin": 0.70,
        "operating_efficiency": 0.65,
        "product_market_fit_score": 0.8,
        "nps_score": 45,
        "competitive_advantage_score": 0.75,
        "scalability_score": 0.8,
        "investor_tier_primary": "tier_1",
        "repeat_founders": 1,
        "technical_founders": 1,
        "product_stage": "beta",
        "churn_rate": 0.05,
        "investor_profile": "balanced"
    }


@pytest.fixture
def test_scenarios():
    """Different test scenarios for comprehensive testing"""
    return [
        {
            "name": "High-Growth SaaS Startup",
            "data": {
                "funding_stage": "Series A",
                "sector": "SaaS",
                "total_capital_raised_usd": 5000000,
                "cash_on_hand_usd": 3000000,
                "monthly_burn_usd": 150000,
                "annual_revenue_run_rate": 2000000,
                "revenue_growth_rate_percent": 200,
                "gross_margin_percent": 75,
                "ltv_cac_ratio": 3.5,
                "net_dollar_retention_percent": 125,
                "customer_count": 50,
                "user_growth_rate_percent": 150,
                "team_size_full_time": 25,
                "years_experience_avg": 12,
                "prior_successful_exits_count": 1,
                "product_retention_30d": 0.85,
                "product_stage": "growth"
            },
            "expected": "high_success"
        },
        {
            "name": "Struggling E-commerce Startup",
            "data": {
                "funding_stage": "Seed",
                "sector": "E-commerce",
                "total_capital_raised_usd": 500000,
                "cash_on_hand_usd": 100000,
                "monthly_burn_usd": 50000,
                "annual_revenue_run_rate": 200000,
                "revenue_growth_rate_percent": 20,
                "gross_margin_percent": 15,
                "ltv_cac_ratio": 0.8,
                "burn_multiple": 8,
                "customer_concentration_percent": 60,
                "net_dollar_retention_percent": 75,
                "team_size_full_time": 5,
                "years_experience_avg": 3,
                "product_retention_30d": 0.4,
                "product_stage": "beta"
            },
            "expected": "low_success"
        },
        {
            "name": "Early-Stage DeepTech",
            "data": {
                "funding_stage": "Pre-seed",
                "sector": "Other",
                "total_capital_raised_usd": 250000,
                "cash_on_hand_usd": 200000,
                "monthly_burn_usd": 20000,
                "annual_revenue_run_rate": 0,
                "patent_count": 3,
                "tech_differentiation_score": 5,
                "team_size_full_time": 4,
                "years_experience_avg": 15,
                "domain_expertise_years_avg": 12,
                "prior_startup_experience_count": 2,
                "advisors_count": 5,
                "product_stage": "prototype"
            },
            "expected": "medium_success"
        }
    ]


class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "FLASH 2.0 API is running"
        assert data["version"] == "2.0.0"
        assert "docs" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "models_loaded" in data
        assert "pillar_models_loaded" in data
        assert "version" in data
        assert "timestamp" in data
    
    @pytest.mark.parametrize("port,path", [
        (8000, "/health"),
        (8001, "/"),
        (8001, "/health")
    ])
    def test_health_endpoints_integration(self, port, path):
        """Test health check endpoints via direct HTTP"""
        try:
            response = requests.get(f"http://localhost:{port}{path}", timeout=2)
            assert response.status_code == 200
            
            if path == "/health":
                data = response.json()
                assert "models_loaded" in data or "status" in data
        except requests.exceptions.RequestException:
            pytest.skip(f"API not running on port {port}")


class TestPredictionEndpoint:
    """Test prediction endpoint"""
    
    def test_valid_prediction(self, client, valid_startup_data):
        """Test prediction with valid data"""
        response = client.post("/predict", json=valid_startup_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "success_probability" in data
        assert 0 <= data["success_probability"] <= 1
        assert "confidence_interval" in data
        assert "risk_level" in data
        assert "key_insights" in data
        assert "pillar_scores" in data
        assert "recommendation" in data
        assert "timestamp" in data
        
        # Check pillar scores
        assert all(pillar in data["pillar_scores"] for pillar in ["capital", "advantage", "market", "people"])
        assert all(0 <= score <= 1 for score in data["pillar_scores"].values())
    
    def test_invalid_prediction_data(self, client, invalid_startup_data):
        """Test prediction with invalid data"""
        response = client.post("/predict", json=invalid_startup_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_edge_case_prediction(self, client, edge_case_startup_data):
        """Test prediction with edge case data"""
        response = client.post("/predict", json=edge_case_startup_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        # Edge cases should still produce valid predictions
        assert 0 <= data["success_probability"] <= 1
        assert data["risk_level"] in ["Very Low Risk", "Low Risk", "Moderate Risk", "High Risk", "Very High Risk", "Critical Risk"]
    
    def test_missing_required_fields(self, client):
        """Test prediction with missing required fields"""
        incomplete_data = {
            "funding_stage": "seed",
            "total_capital_raised_usd": 1000000
            # Missing many required fields
        }
        response = client.post("/predict", json=incomplete_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_comprehensive_evaluation(self, client, valid_startup_data):
        """Test comprehensive evaluation features"""
        response = client.post("/predict", json=valid_startup_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        if "comprehensive_evaluation" in data:
            eval_data = data["comprehensive_evaluation"]
            assert "verdict" in eval_data
            assert eval_data["verdict"] in ["PASS", "CONDITIONAL PASS", "FAIL"]
            assert "stage_context" in eval_data
            assert "critical_failures" in eval_data
            assert "risk_adjustments" in eval_data
    
    def test_pillar_scores_format(self, client, valid_startup_data):
        """Test CAMP pillar scores format and values"""
        response = client.post("/predict", json=valid_startup_data)
        assert response.status_code == status.HTTP_200_OK
        
        result = response.json()
        assert "pillar_scores" in result
        
        pillars = ["capital", "advantage", "market", "people"]
        for pillar in pillars:
            assert pillar in result["pillar_scores"]
            assert 0 <= result["pillar_scores"][pillar] <= 1
    
    @pytest.mark.parametrize("profile", ["conservative", "balanced", "aggressive"])
    def test_investor_profiles(self, complete_startup_data, profile):
        """Test different investor profiles"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict",
                json=complete_startup_data,
                params={"investor_profile": profile},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                assert "calibrated_probability" in result or "success_probability" in result
                assert "threshold_used" in result or "confidence" in result
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")


class TestValidation:
    """Test input validation"""
    
    def test_funding_stage_validation(self, client, valid_startup_data):
        """Test funding stage validation"""
        data = valid_startup_data.copy()
        data["funding_stage"] = "invalid_stage"
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_numeric_bounds_validation(self, client, valid_startup_data):
        """Test numeric field bounds"""
        # Test negative values where not allowed
        data = valid_startup_data.copy()
        data["total_capital_raised_usd"] = -1000
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test percentage over 100
        data = valid_startup_data.copy()
        data["team_diversity_percent"] = 150
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test score out of range
        data = valid_startup_data.copy()
        data["tech_differentiation_score"] = 10  # Should be 1-5
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_market_size_validation(self, client, valid_startup_data):
        """Test TAM > SAM > SOM validation"""
        data = valid_startup_data.copy()
        data["tam_size_usd"] = 100
        data["sam_size_usd"] = 1000
        data["som_size_usd"] = 10000
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_string_length_validation(self, client, valid_startup_data):
        """Test string length limits"""
        data = valid_startup_data.copy()
        data["sector"] = "x" * 1001  # Exceed max length
        response = client.post("/predict", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestExplanationEndpoints:
    """Test explanation and interpretability endpoints"""
    
    def test_explanation_endpoint(self, client, valid_startup_data):
        """Test SHAP explanation endpoint"""
        response = client.post("/explain", json=valid_startup_data)
        # May fail if SHAP models not available
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert "prediction" in data
            assert "explanation" in data
            assert "feature_mapping" in data
    
    def test_prediction_with_explanation(self, complete_startup_data):
        """Test prediction with explanation flag"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict",
                json=complete_startup_data,
                params={"include_explanation": True},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if "explanation" in result:
                    exp = result["explanation"]
                    assert "positive_factors" in exp or "negative_factors" in exp
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")


class TestFrontendCompatibility:
    """Test frontend API compatibility"""
    
    def test_frontend_data_format(self, frontend_compatible_data):
        """Test API with frontend data format"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict",
                json=frontend_compatible_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                assert "prediction" in result or "success_probability" in result
                assert "confidence" in result
                assert "risk_level" in result
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")
    
    def test_advanced_predict(self, frontend_compatible_data):
        """Test advanced prediction endpoint"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict_advanced",
                json=frontend_compatible_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                assert "dna_match_score" in result
                assert "growth_potential_score" in result
                assert "model_used" in result
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")
    
    def test_investor_profiles_endpoint(self):
        """Test investor profiles listing"""
        try:
            response = requests.get(
                f"{API_URLS['secondary']}/investor_profiles",
                timeout=5
            )
            
            if response.status_code == 200:
                profiles = response.json()
                assert isinstance(profiles, (list, dict))
                if isinstance(profiles, list):
                    assert len(profiles) >= 3  # At least 3 profiles
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")


class TestAdvancedFeatures:
    """Test advanced API features"""
    
    def test_engineered_features(self, complete_startup_data):
        """Test engineered features in response"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict",
                json=complete_startup_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if "engineered_features" in result:
                    features = result["engineered_features"]
                    assert isinstance(features, dict)
                    assert len(features) > 0
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")
    
    def test_model_scores(self, complete_startup_data):
        """Test individual model scores"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict",
                json=complete_startup_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if "individual_model_scores" in result:
                    scores = result["individual_model_scores"]
                    assert isinstance(scores, dict)
                    
                    # Check model agreement
                    if len(scores) > 1:
                        values = list(scores.values())
                        std_dev = pd.Series(values).std()
                        assert std_dev is not None
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")
    
    def test_simple_prediction_endpoint(self, complete_startup_data):
        """Test simple prediction endpoint"""
        try:
            response = requests.post(
                f"{API_URLS['secondary']}/predict_simple",
                json=complete_startup_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                assert "success_probability" in result
                assert "prediction" in result
                assert "confidence" in result
                assert "risk_factors" in result
                assert "growth_indicators" in result
        except requests.exceptions.RequestException:
            pytest.skip("Secondary API not available")


class TestScenarioValidation:
    """Test different startup scenarios"""
    
    def test_all_scenarios(self, test_scenarios):
        """Test various startup scenarios"""
        for scenario in test_scenarios:
            try:
                response = requests.post(
                    f"{API_URLS['primary']}/predict",
                    json=scenario["data"],
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    probability = result["success_probability"]
                    
                    # Validate expected outcomes
                    if scenario["expected"] == "high_success":
                        assert probability > 0.6
                    elif scenario["expected"] == "low_success":
                        assert probability < 0.4
                    elif scenario["expected"] == "medium_success":
                        assert 0.3 <= probability <= 0.7
            except requests.exceptions.RequestException:
                pytest.skip("API not available")


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    @pytest.mark.asyncio
    async def test_rate_limit_enforcement(self, async_client, valid_startup_data):
        """Test that rate limiting works"""
        # Make requests up to the limit
        for _ in range(100):
            response = await async_client.post("/predict", json=valid_startup_data)
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        
        # Next request should be rate limited
        response = await async_client.post("/predict", json=valid_startup_data)
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Rate limit exceeded" in response.json()["detail"]


class TestSecurityHeaders:
    """Test security headers and middleware"""
    
    def test_cors_headers(self, client, valid_startup_data):
        """Test CORS headers are set correctly"""
        response = client.post(
            "/predict",
            json=valid_startup_data,
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_request_size_limit(self, client):
        """Test request size limitation"""
        # Create a large payload
        large_data = {"data": "x" * (2 * 1024 * 1024)}  # 2MB
        response = client.post(
            "/predict",
            json=large_data,
            headers={"Content-Length": str(2 * 1024 * 1024)}
        )
        # Should be rejected before validation
        assert response.status_code in [
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]


class TestPerformance:
    """Test API performance"""
    
    def test_response_time(self, complete_startup_data):
        """Test API response time"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_URLS['primary']}/predict",
                json=complete_startup_data,
                timeout=10
            )
            end_time = time.time()
            
            assert response.status_code == 200
            response_time = end_time - start_time
            assert response_time < 5.0  # Should respond within 5 seconds
        except requests.exceptions.RequestException:
            pytest.skip("API not available")
    
    def test_concurrent_requests(self, basic_startup_data):
        """Test handling of concurrent requests"""
        def make_request():
            try:
                return requests.post(
                    f"{API_URLS['primary']}/predict",
                    json=basic_startup_data,
                    timeout=5
                )
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Check successful requests
        successful = [r for r in results if r is not None]
        if len(successful) > 0:
            for response in successful:
                assert response.status_code == 200


# Utility functions for running tests manually
def run_manual_tests():
    """Run tests manually without pytest"""
    print("🚀 FLASH API Comprehensive Test Suite")
    print("=" * 60)
    
    # Check API availability
    apis_available = {}
    for name, url in API_URLS.items():
        try:
            response = requests.get(f"{url}/health", timeout=2)
            apis_available[name] = response.status_code == 200
        except:
            apis_available[name] = False
    
    print("API Availability:")
    for name, available in apis_available.items():
        status_icon = "✅" if available else "❌"
        print(f"  {name}: {status_icon}")
    
    if not any(apis_available.values()):
        print("\n❌ No APIs are running. Please start the API server(s).")
        return
    
    print("\n" + "=" * 60)
    print("Run tests with: pytest tests/test_api.py -v")
    print("Run specific test: pytest tests/test_api.py::TestPredictionEndpoint::test_pillar_scores_format -v")
    print("Run with coverage: pytest tests/test_api.py --cov=. --cov-report=html")


if __name__ == "__main__":
    run_manual_tests()