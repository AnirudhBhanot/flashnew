#!/usr/bin/env python3
"""
Test suite for Unified Model Orchestrator
"""
import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.unified_orchestrator import UnifiedModelOrchestrator, OrchestratorConfig


class TestUnifiedOrchestrator:
    """Test cases for the Unified Model Orchestrator"""
    
    @pytest.fixture
    def sample_features(self):
        """Sample startup features for testing"""
        return pd.DataFrame([{
            # Capital features
            'funding_stage': 'Series A',
            'total_capital_raised_usd': 5000000,
            'cash_on_hand_usd': 3000000,
            'monthly_burn_usd': 150000,
            'runway_months': 20,
            'annual_revenue_run_rate': 1200000,
            'revenue_growth_rate_percent': 150,
            'gross_margin_percent': 70,
            'burn_multiple': 2.5,
            'ltv_cac_ratio': 3.5,
            'investor_tier_primary': 'tier_1',
            'has_debt': False,
            
            # Advantage features
            'patent_count': 3,
            'network_effects_present': True,
            'has_data_moat': True,
            'regulatory_advantage_present': False,
            'tech_differentiation_score': 4.2,
            'switching_cost_score': 3.8,
            'brand_strength_score': 3.5,
            'scalability_score': 4.5,
            'product_stage': 'growth',
            'product_retention_30d': 0.85,
            'product_retention_90d': 0.75,
            
            # Market features
            'sector': 'fintech',
            'tam_size_usd': 50000000000,
            'sam_size_usd': 10000000000,
            'som_size_usd': 500000000,
            'market_growth_rate_percent': 25,
            'customer_count': 1000,
            'customer_concentration_percent': 15,
            'user_growth_rate_percent': 200,
            'net_dollar_retention_percent': 125,
            'competition_intensity': 3.5,
            'competitors_named_count': 10,
            'dau_mau_ratio': 0.65,
            
            # People features
            'founders_count': 2,
            'team_size_full_time': 25,
            'years_experience_avg': 12,
            'domain_expertise_years_avg': 8,
            'prior_startup_experience_count': 3,
            'prior_successful_exits_count': 1,
            'board_advisor_experience_score': 4.0,
            'advisors_count': 5,
            'team_diversity_percent': 40,
            'key_person_dependency': False
        }])
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        config = OrchestratorConfig(
            enable_calibration=True,
            enable_shap=True,
            enable_ab_testing=True,
            ab_test_percentage=0.5
        )
        return UnifiedModelOrchestrator(config=config)
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes correctly"""
        assert orchestrator is not None
        assert orchestrator.config.enable_calibration is True
        assert orchestrator.config.enable_shap is True
        assert len(orchestrator.models) == 0
        assert len(orchestrator.config.model_weights) == 6
    
    @patch('joblib.load')
    @patch('catboost.CatBoostClassifier')
    def test_model_loading(self, mock_catboost, mock_joblib, orchestrator):
        """Test model loading functionality"""
        # Mock model loading
        mock_model = Mock()
        mock_joblib.return_value = mock_model
        mock_catboost.return_value.load_model = Mock()
        
        # Mock file existence
        with patch('pathlib.Path.exists', return_value=True):
            success = orchestrator.load_models()
        
        assert success is True
        assert len(orchestrator.models) > 0
    
    def test_prediction_without_models(self, orchestrator, sample_features):
        """Test prediction handling when models aren't loaded"""
        result = orchestrator.predict(sample_features)
        
        assert 'prediction' in result
        assert 'probability' in result
        assert result['probability'] == 0.5  # Default fallback
    
    @patch.object(UnifiedModelOrchestrator, '_predict_base_ensemble')
    def test_prediction_with_mocked_models(self, mock_base_ensemble, orchestrator, sample_features):
        """Test prediction flow with mocked models"""
        # Mock base ensemble prediction
        mock_base_ensemble.return_value = {
            'prediction': 1,
            'probability': 0.75,
            'pillar_scores': {
                'capital': 0.7,
                'advantage': 0.8,
                'market': 0.65,
                'people': 0.85
            }
        }
        
        # Add mock models
        orchestrator.models['base_ensemble'] = Mock()
        
        result = orchestrator.predict(sample_features)
        
        assert result['prediction'] == 1
        assert 0 <= result['probability'] <= 1
        assert 'confidence_interval' in result
        assert 'model_consensus' in result
    
    def test_confidence_interval_calculation(self, orchestrator):
        """Test confidence interval calculation"""
        probabilities = {
            'model1': 0.7,
            'model2': 0.75,
            'model3': 0.65,
            'model4': 0.8
        }
        
        interval = orchestrator._calculate_confidence_interval(probabilities)
        
        assert len(interval) == 2
        assert interval[0] < interval[1]
        assert 0 <= interval[0] <= 1
        assert 0 <= interval[1] <= 1
    
    def test_weighted_ensemble(self, orchestrator):
        """Test weighted ensemble calculation"""
        probabilities = {
            'base_ensemble': 0.7,
            'stage_hierarchical': 0.75,
            'dna_analyzer': 0.65,
            'temporal': 0.8,
            'industry_specific': 0.72,
            'optimized_pipeline': 0.78
        }
        
        result = orchestrator._weighted_ensemble(probabilities)
        
        assert 0 <= result <= 1
        # Result should be weighted average
        weights = orchestrator.config.model_weights
        expected = sum(probabilities[k] * weights[k] for k in probabilities) / sum(weights.values())
        assert abs(result - expected) < 0.01
    
    def test_calibration(self, orchestrator):
        """Test probability calibration"""
        # Test various probabilities
        test_probs = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        for prob in test_probs:
            calibrated = orchestrator._calibrate_probability(prob)
            assert 0 <= calibrated <= 1
            
            # Calibration should preserve order
            if prob < 0.5:
                assert calibrated < 0.5
            elif prob > 0.5:
                assert calibrated > 0.5
    
    def test_performance_tracking(self, orchestrator):
        """Test performance history tracking"""
        predictions = {'model1': 0.7, 'model2': 0.8}
        
        orchestrator._track_performance(predictions, 0.75)
        
        assert len(orchestrator.performance_history) == 1
        assert orchestrator.performance_history[0]['final_probability'] == 0.75
    
    def test_ab_testing(self, orchestrator, sample_features):
        """Test A/B testing functionality"""
        # Force A/B test groups
        result_old = orchestrator.predict(sample_features, ab_test_group='old')
        result_new = orchestrator.predict(sample_features, ab_test_group='new')
        
        assert result_old['ab_test_group'] == 'old'
        assert result_new['ab_test_group'] == 'new'
    
    def test_get_performance_summary(self, orchestrator):
        """Test performance summary generation"""
        # Add some performance history
        for i in range(5):
            orchestrator._track_performance({'model1': 0.7}, 0.7 + i * 0.02)
        
        summary = orchestrator.get_performance_summary()
        
        assert 'total_predictions' in summary
        assert summary['total_predictions'] == 5
        assert 'avg_confidence' in summary
        assert 'model_weights' in summary
    
    @patch('sklearn.metrics.roc_auc_score')
    def test_weight_optimization(self, mock_auc, orchestrator):
        """Test model weight optimization"""
        # Mock AUC calculation
        mock_auc.return_value = 0.8
        
        # Create validation data
        X_val = pd.DataFrame(np.random.rand(10, 45), columns=[f'feature_{i}' for i in range(45)])
        y_val = np.random.randint(0, 2, 10)
        
        # Mock predict method to avoid actual model calls
        with patch.object(orchestrator, 'predict', return_value={'probability': 0.7}):
            orchestrator.optimize_weights(X_val, y_val)
        
        # Weights should sum to 1
        total_weight = sum(orchestrator.config.model_weights.values())
        assert abs(total_weight - 1.0) < 0.01
    
    def test_pillar_feature_extraction(self, orchestrator, sample_features):
        """Test extraction of pillar-specific features"""
        capital_features = orchestrator._get_pillar_features(sample_features, 'capital')
        
        assert len(capital_features.columns) == 12  # Number of capital features
        assert 'funding_stage' in capital_features.columns
        assert 'total_capital_raised_usd' in capital_features.columns
    
    def test_explanation_generation(self, orchestrator):
        """Test SHAP explanation generation"""
        factors = [('capital', 0.3), ('market', -0.2), ('people', 0.1), ('advantage', 0.05)]
        
        text = orchestrator._generate_explanation_text(factors, 0.75)
        
        assert 'strong' in text
        assert 'positive' in text
        assert 'Capital' in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])