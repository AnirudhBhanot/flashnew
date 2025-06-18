"""
End-to-end tests for complete workflows
"""

import pytest
import time
from unittest.mock import patch, Mock
import pandas as pd
import numpy as np

# Import components
from type_converter_simple import TypeConverter
from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from utils.probability_utils import ensure_probability_bounds
from utils.safe_math import safe_divide


class TestCompleteWorkflow:
    """Test complete prediction workflow"""
    
    @pytest.fixture
    def frontend_data(self):
        """Simulated frontend data"""
        return {
            # Capital features
            "total_capital_raised_usd": "5000000",
            "funding_stage": "Series A",
            "cash_on_hand_usd": 2000000,
            "monthly_burn_usd": 200000,
            
            # Advantage features
            "tech_differentiation_score": 4,
            "has_strategic_partnerships": True,  # Boolean as bool
            "patent_count": 2,
            
            # Market features
            "total_addressable_market_usd": 10000000000,
            "market_growth_rate_percent": 25.5,
            "sector": "Enterprise SaaS",
            
            # People features
            "founders_count": 2,
            "team_size_full_time": 25,
            "prior_successful_exits_count": 1,
            
            # Product features
            "product_stage": "Growth",
            "product_retention_30d": 85,  # As percentage
            "revenue_growth_rate_percent": 200,
            
            # Extra frontend fields
            "startup_name": "TechCorp",
            "hq_location": "San Francisco"
        }
    
    def test_frontend_to_prediction_flow(self, frontend_data):
        """Test complete flow from frontend data to prediction"""
        # Step 1: Type conversion
        converter = TypeConverter()
        backend_data = converter.convert_frontend_to_backend(frontend_data)
        
        # Verify conversion
        assert backend_data["funding_stage"] == "series_a"  # Lowercased
        assert backend_data["sector"] == "enterprise_saas"  # Underscored
        assert backend_data["has_strategic_partnerships"] == 1  # Bool to int
        assert backend_data["product_retention_30d"] == 0.85  # Percentage to decimal
        assert "startup_name" not in backend_data  # Frontend field removed
        
        # Step 2: Create DataFrame for model
        features_df = pd.DataFrame([backend_data])
        
        # Step 3: Get prediction (mocked)
        with patch.object(UnifiedOrchestratorV3, 'predict') as mock_predict:
            mock_predict.return_value = {
                "success_probability": 0.72,
                "confidence_score": 0.85,
                "predictions": {
                    "dna_analyzer": 0.70,
                    "temporal_prediction": 0.75,
                    "industry_specific": 0.71
                },
                "pillar_scores": {
                    "capital": 0.65,
                    "advantage": 0.78,
                    "market": 0.82,
                    "people": 0.68
                }
            }
            
            orchestrator = UnifiedOrchestratorV3()
            result = orchestrator.predict(features_df)
        
        # Verify result
        assert result["success_probability"] == 0.72
        assert result["verdict"]["verdict"] == "PASS"
        assert len(result["pillar_scores"]) == 4
    
    def test_data_validation_flow(self, frontend_data):
        """Test data validation workflow"""
        # Remove required fields
        incomplete_data = frontend_data.copy()
        del incomplete_data["total_capital_raised_usd"]
        del incomplete_data["funding_stage"]
        
        # Convert
        converter = TypeConverter()
        backend_data = converter.convert_frontend_to_backend(incomplete_data)
        
        # Check completeness
        from feature_config import ALL_FEATURES
        provided_features = set(backend_data.keys())
        expected_features = set(ALL_FEATURES)
        
        completeness = len(provided_features.intersection(expected_features)) / len(expected_features)
        
        assert completeness < 1.0  # Not complete
        assert completeness > 0.5  # But has some data


class TestProbabilityNormalization:
    """Test probability normalization in workflow"""
    
    def test_model_ensemble_normalization(self):
        """Test that ensemble probabilities are normalized"""
        model_predictions = {
            "model1": 0.6,
            "model2": 0.7,
            "model3": 0.8,
            "model4": 0.65
        }
        
        # Mock weights
        weights = {
            "model1": 0.25,
            "model2": 0.25,
            "model3": 0.3,
            "model4": 0.2
        }
        
        # Calculate weighted average
        total_weight = sum(weights.values())
        normalized_weights = {k: v/total_weight for k, v in weights.items()}
        
        weighted_sum = sum(
            model_predictions[k] * normalized_weights[k] 
            for k in model_predictions
        )
        
        # Ensure bounded
        final_prob = ensure_probability_bounds(weighted_sum)
        
        assert 0 < final_prob < 1
        assert final_prob == pytest.approx(0.6875, rel=0.01)


class TestErrorRecovery:
    """Test error recovery in workflows"""
    
    def test_missing_model_recovery(self):
        """Test recovery when a model is missing"""
        with patch.object(UnifiedOrchestratorV3, '_load_models') as mock_load:
            # Simulate partial model loading
            mock_load.side_effect = lambda: setattr(
                UnifiedOrchestratorV3, 
                'models', 
                {"dna_analyzer": Mock()}  # Only one model loaded
            )
            
            orchestrator = UnifiedOrchestratorV3()
            
            # Should handle missing models gracefully
            features_df = pd.DataFrame([{"test": 1}])
            
            with patch.object(orchestrator, '_calculate_camp_scores_safe') as mock_camp:
                mock_camp.return_value = {
                    "capital": 0.5,
                    "advantage": 0.6,
                    "market": 0.7,
                    "people": 0.55
                }
                
                # This should not crash
                result = orchestrator.predict(features_df)
                
                # Should return some prediction
                assert "success_probability" in result
                assert 0 <= result["success_probability"] <= 1
    
    def test_feature_mismatch_recovery(self):
        """Test recovery from feature mismatches"""
        # Create orchestrator
        orchestrator = UnifiedOrchestratorV3()
        
        # Data with wrong features
        wrong_features = pd.DataFrame([{
            "unknown_feature_1": 100,
            "unknown_feature_2": "test",
            "partial_match": 0.5
        }])
        
        # Mock the models to avoid actual loading
        with patch.object(orchestrator, 'models', {}):
            result = orchestrator.predict(wrong_features)
        
        # Should still return a result
        assert "success_probability" in result
        assert "pillar_scores" in result
        assert result.get("confidence_score", 0) < 0.7  # Low confidence


class TestDivisionByZeroProtection:
    """Test division by zero protection in calculations"""
    
    def test_financial_calculations(self):
        """Test financial metric calculations"""
        # LTV/CAC with zero CAC
        ltv = 10000
        cac = 0
        
        ratio = safe_divide(ltv, cac, default=0)
        assert ratio == 0
        
        # Burn multiple with zero revenue
        burn = 100000
        revenue = 0
        
        burn_multiple = safe_divide(burn, revenue, default=float('inf'))
        assert burn_multiple == float('inf')
        
        # Runway with zero burn
        cash = 1000000
        burn = 0
        
        runway = safe_divide(cash, burn, default=float('inf'))
        assert runway == float('inf')
    
    def test_percentage_calculations(self):
        """Test percentage calculations"""
        # Growth rate with zero base
        current = 1000
        previous = 0
        
        growth = safe_divide(current - previous, previous, default=1.0) * 100
        growth_pct = min(growth, 100)  # Cap at 100%
        
        assert growth_pct == 100
        
        # Retention with zero users
        retained = 0
        total = 0
        
        retention = safe_divide(retained, total, default=0)
        assert retention == 0


class TestIntegrationWithDatabase:
    """Test integration with database operations"""
    
    @patch('database.connection.get_session')
    def test_prediction_storage_workflow(self, mock_session):
        """Test storing prediction results"""
        from database.repositories import PredictionRepository
        
        # Mock session
        session = Mock()
        mock_session.return_value.__enter__ = Mock(return_value=session)
        mock_session.return_value.__exit__ = Mock(return_value=None)
        
        # Create repository
        repo = PredictionRepository(session)
        
        # Prediction data
        prediction_data = {
            "input_features": {"test": 1},
            "success_probability": 0.75,
            "confidence_score": 0.85,
            "verdict": "PASS",
            "camp_scores": {
                "capital": 0.7,
                "advantage": 0.8,
                "market": 0.75,
                "people": 0.72
            },
            "model_predictions": {
                "dna": 0.74,
                "temporal": 0.76
            }
        }
        
        # Create prediction
        prediction = repo.create(**prediction_data)
        
        # Verify repository methods were called
        session.add.assert_called_once()
        session.flush.assert_called_once()


class TestPerformanceMetrics:
    """Test performance tracking in workflows"""
    
    def test_latency_tracking(self):
        """Test tracking of processing latency"""
        start_time = time.time()
        
        # Simulate processing
        time.sleep(0.1)  # 100ms
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        assert 90 < latency_ms < 150  # Allow some variance
        
        # Check if latency is acceptable
        assert latency_ms < 1000  # Should be under 1 second


class TestModelVersioning:
    """Test model versioning workflow"""
    
    def test_model_version_tracking(self):
        """Test tracking model versions"""
        from security.model_integrity import ModelIntegrityChecker
        
        checker = ModelIntegrityChecker()
        
        # Test model path
        test_model_path = "models/test_model.pkl"
        
        # Calculate checksum (mocked)
        with patch.object(checker, 'calculate_checksum') as mock_checksum:
            mock_checksum.return_value = "abc123def456"
            
            # Verify model (should add to manifest)
            with patch('pathlib.Path.exists', return_value=True):
                is_valid = checker.verify_model(test_model_path)
            
            assert is_valid  # First time seeing model
            assert test_model_path in checker.manifest


if __name__ == "__main__":
    pytest.main([__file__, "-v"])