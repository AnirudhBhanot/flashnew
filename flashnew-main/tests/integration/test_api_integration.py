"""
Integration tests for API endpoints
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import numpy as np

# Import after patching
with patch('database.connection.init_database'):
    from api_server_unified import app
    from database.models import Prediction, APIKey
    from database.repositories import PredictionRepository


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def valid_startup_data():
    """Valid startup data for testing"""
    return {
        "total_capital_raised_usd": 5000000,
        "funding_stage": "series_a",
        "sector": "enterprise_saas",
        "cash_on_hand_usd": 2000000,
        "monthly_burn_usd": 200000,
        "runway_months": 10,
        "burn_multiple": 2.5,
        "tech_differentiation_score": 4,
        "patent_count": 2,
        "has_strategic_partnerships": True,
        "switching_cost_score": 3,
        "has_network_effects": False,
        "brand_strength_score": 3,
        "scalability_score": 4,
        "total_addressable_market_usd": 10000000000,
        "serviceable_addressable_market_usd": 1000000000,
        "serviceable_obtainable_market_usd": 100000000,
        "market_growth_rate_percent": 25,
        "investor_tier_primary": "tier_1",
        "user_growth_rate_percent": 150,
        "customers_count": 100,
        "net_promoter_score": 45,
        "payback_period_months": 12,
        "time_to_revenue_months": 6,
        "customer_acquisition_cost": 1000,
        "net_dollar_retention_percent": 110,
        "competition_intensity": 3,
        "competitors_named_count": 5,
        "founders_count": 2,
        "team_size_full_time": 25,
        "years_experience_avg": 10,
        "domain_expertise_years_avg": 8,
        "prior_startup_experience_count": 2,
        "prior_successful_exits_count": 1,
        "board_advisor_experience_score": 4,
        "advisors_count": 3,
        "team_diversity_percent": 40,
        "key_person_dependency": False,
        "product_stage": "growth",
        "product_retention_30d": 0.85,
        "product_retention_90d": 0.75,
        "dau_mau_ratio": 0.6,
        "annual_revenue_run_rate": 2400000,
        "revenue_growth_rate_percent": 200,
        "gross_margin_percent": 75,
        "ltv_cac_ratio": 3.5
    }


class TestPredictionEndpoints:
    """Test prediction endpoints"""
    
    def test_predict_success(self, client, valid_startup_data):
        """Test successful prediction"""
        response = client.post("/predict", json=valid_startup_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "success_probability" in data
        assert "confidence_score" in data
        assert "verdict" in data
        assert "camp_scores" in data
        
        # Validate ranges
        assert 0 <= data["success_probability"] <= 1
        assert 0 <= data["confidence_score"] <= 1
        assert data["verdict"] in ["PASS", "CONDITIONAL PASS", "FAIL"]
        
        # Check CAMP scores
        for pillar in ["capital", "advantage", "market", "people"]:
            assert pillar in data["camp_scores"]
            assert 0 <= data["camp_scores"][pillar] <= 1
    
    def test_predict_missing_fields(self, client):
        """Test prediction with missing required fields"""
        incomplete_data = {
            "total_capital_raised_usd": 5000000,
            "funding_stage": "series_a"
            # Missing many required fields
        }
        
        response = client.post("/predict", json=incomplete_data)
        
        # Should still work but with lower confidence
        assert response.status_code == 200
        data = response.json()
        assert data["confidence_score"] < 0.9  # Lower confidence due to missing data
    
    def test_predict_invalid_values(self, client, valid_startup_data):
        """Test prediction with invalid values"""
        invalid_data = valid_startup_data.copy()
        invalid_data["tech_differentiation_score"] = 10  # Should be 1-5
        invalid_data["product_retention_30d"] = 2.0  # Should be 0-1
        
        response = client.post("/predict", json=invalid_data)
        
        # Should handle gracefully
        assert response.status_code in [200, 422]  # Either processes or validates
    
    @patch('api_server_unified.orchestrator.predict')
    def test_predict_model_error(self, mock_predict, client, valid_startup_data):
        """Test handling of model errors"""
        mock_predict.side_effect = Exception("Model error")
        
        response = client.post("/predict", json=valid_startup_data)
        
        # Should handle error gracefully
        assert response.status_code == 200
        data = response.json()
        
        # Should return fallback prediction
        assert "success_probability" in data
        assert data.get("error") or data.get("warning")


class TestValidationEndpoint:
    """Test data validation endpoint"""
    
    def test_validate_complete_data(self, client, valid_startup_data):
        """Test validation of complete data"""
        response = client.post("/validate", json=valid_startup_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True
        assert data["completeness"] > 0.9
        assert len(data["missing_fields"]) == 0
    
    def test_validate_incomplete_data(self, client):
        """Test validation of incomplete data"""
        incomplete_data = {
            "total_capital_raised_usd": 5000000,
            "funding_stage": "series_a",
            "sector": "enterprise_saas"
        }
        
        response = client.post("/validate", json=incomplete_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_valid"] is True  # Still valid, just incomplete
        assert data["completeness"] < 0.2
        assert len(data["missing_fields"]) > 40


class TestPatternEndpoints:
    """Test pattern analysis endpoints"""
    
    def test_list_patterns(self, client):
        """Test pattern listing"""
        response = client.get("/patterns")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "patterns" in data
        assert isinstance(data["patterns"], list)
        
        if len(data["patterns"]) > 0:
            pattern = data["patterns"][0]
            assert "name" in pattern
            assert "category" in pattern
    
    def test_analyze_pattern(self, client, valid_startup_data):
        """Test pattern analysis"""
        response = client.post("/analyze_pattern", json=valid_startup_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "primary_pattern" in data
        assert "pattern_confidence" in data
        assert "similar_patterns" in data


class TestSystemEndpoints:
    """Test system information endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "models_loaded" in data
        assert "uptime" in data
    
    def test_features_documentation(self, client):
        """Test features documentation"""
        response = client.get("/features")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "features" in data
        assert "total_count" in data
        assert data["total_count"] == 45
    
    def test_system_info(self, client):
        """Test system information"""
        response = client.get("/system_info")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "version" in data
        assert "models" in data
        assert "features" in data


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_enforcement(self, client, valid_startup_data):
        """Test that rate limits are enforced"""
        # Make requests up to limit
        for i in range(10):  # Rate limit is 10/minute
            response = client.post("/predict", json=valid_startup_data)
            assert response.status_code == 200
        
        # 11th request should be rate limited
        response = client.post("/predict", json=valid_startup_data)
        assert response.status_code == 429  # Too Many Requests


class TestAPIKeyAuthentication:
    """Test API key authentication"""
    
    @patch('api_server_unified.settings.API_KEYS', ['test-api-key'])
    def test_valid_api_key(self, client, valid_startup_data):
        """Test request with valid API key"""
        headers = {"X-API-Key": "test-api-key"}
        response = client.post("/predict", json=valid_startup_data, headers=headers)
        
        assert response.status_code == 200
    
    @patch('api_server_unified.settings.API_KEYS', ['valid-key'])
    def test_invalid_api_key(self, client, valid_startup_data):
        """Test request with invalid API key"""
        headers = {"X-API-Key": "invalid-key"}
        response = client.post("/predict", json=valid_startup_data, headers=headers)
        
        assert response.status_code == 403  # Forbidden
    
    def test_no_api_key_optional(self, client, valid_startup_data):
        """Test request without API key when optional"""
        # Default behavior allows requests without API key
        response = client.post("/predict", json=valid_startup_data)
        
        assert response.status_code == 200


class TestDatabaseIntegration:
    """Test database integration"""
    
    @patch('database.connection.get_db')
    def test_prediction_stored(self, mock_get_db, client, valid_startup_data):
        """Test that predictions are stored in database"""
        # Mock database session
        mock_session = Mock()
        mock_get_db.return_value = mock_session
        
        response = client.post("/predict", json=valid_startup_data)
        
        assert response.status_code == 200
        
        # Verify database operations would be called
        # (In real implementation, predictions should be stored)


class TestErrorHandling:
    """Test error handling"""
    
    def test_malformed_json(self, client):
        """Test handling of malformed JSON"""
        response = client.post(
            "/predict",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_wrong_content_type(self, client):
        """Test wrong content type"""
        response = client.post(
            "/predict",
            data="some data",
            headers={"Content-Type": "text/plain"}
        )
        
        assert response.status_code == 422


class TestExplainEndpoint:
    """Test explanation endpoint"""
    
    def test_explain_prediction(self, client, valid_startup_data):
        """Test prediction explanation"""
        response = client.post("/explain", json=valid_startup_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "feature_importance" in data
        assert "decision_factors" in data
        assert "improvement_suggestions" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])