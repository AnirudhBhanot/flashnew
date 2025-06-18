"""
Contract Testing Framework
Comprehensive tests to ensure contracts are properly enforced
"""

import unittest
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import tempfile
import json
from datetime import datetime

from .feature_registry import FeatureRegistry, feature_registry
from .model_contracts import ModelContract, ContractBuilder
from .feature_pipeline import UnifiedFeaturePipeline
from .model_wrapper import ContractualModel, ModelMetadata
from .training_system import UnifiedTrainingSystem


class ContractTestCase(unittest.TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Setup test environment"""
        self.registry = feature_registry
        self.pipeline = UnifiedFeaturePipeline(self.registry)
        
        # Create sample data
        self.sample_data = self._create_sample_data()
        
        # Fit pipeline
        self.pipeline.fit(self.sample_data)
    
    def _create_sample_data(self, n_samples: int = 100) -> pd.DataFrame:
        """Create sample data matching feature registry"""
        data = {}
        
        for name, feature in self.registry.features.items():
            if feature.dtype == int:
                if feature.allowed_values:
                    data[name] = np.random.choice(feature.allowed_values, n_samples)
                else:
                    min_val = feature.min_value or 0
                    max_val = feature.max_value or 100
                    data[name] = np.random.randint(min_val, max_val + 1, n_samples)
            
            elif feature.dtype == float:
                min_val = feature.min_value or 0
                max_val = feature.max_value or 100
                data[name] = np.random.uniform(min_val, max_val, n_samples)
            
            elif feature.dtype == str:
                if feature.allowed_values:
                    data[name] = np.random.choice(feature.allowed_values, n_samples)
                else:
                    data[name] = [f"value_{i}" for i in range(n_samples)]
            
            elif feature.dtype == bool:
                data[name] = np.random.choice([True, False], n_samples)
        
        return pd.DataFrame(data)


class TestFeatureRegistry(ContractTestCase):
    """Test feature registry functionality"""
    
    def test_registry_initialization(self):
        """Test registry has all 45 features"""
        self.assertEqual(len(self.registry.features), 45)
        
        # Check all features have required attributes
        for name, feature in self.registry.features.items():
            self.assertIsNotNone(feature.name)
            self.assertIsNotNone(feature.position)
            self.assertIsNotNone(feature.dtype)
            self.assertIsNotNone(feature.category)
    
    def test_feature_ordering(self):
        """Test features are in correct position order"""
        positions = []
        for name, feature in self.registry.features.items():
            positions.append(feature.position)
        
        # Positions should be 0-44
        self.assertEqual(sorted(positions), list(range(45)))
    
    def test_feature_validation(self):
        """Test feature validation works correctly"""
        # Test valid values
        feature = self.registry.get_feature('funding_stage')
        is_valid, error = feature.validate('seed')
        self.assertTrue(is_valid)
        
        # Test invalid values
        is_valid, error = feature.validate('invalid_stage')
        self.assertFalse(is_valid)
        
        # Test numeric range validation
        feature = self.registry.get_feature('team_size_full_time')
        is_valid, error = feature.validate(50)
        self.assertTrue(is_valid)
        
        is_valid, error = feature.validate(-10)
        self.assertFalse(is_valid)
    
    def test_dataframe_validation(self):
        """Test dataframe validation"""
        # Valid dataframe
        is_valid, errors = self.registry.validate_dataframe(self.sample_data)
        self.assertTrue(is_valid)
        
        # Missing columns
        incomplete_df = self.sample_data.drop(columns=['funding_stage'])
        is_valid, errors = self.registry.validate_dataframe(incomplete_df)
        self.assertFalse(is_valid)
        self.assertTrue(any('funding_stage' in str(e) for e in errors))


class TestModelContracts(ContractTestCase):
    """Test model contract system"""
    
    def test_contract_creation(self):
        """Test creating contracts for different models"""
        # DNA Analyzer contract
        dna_contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
        self.assertEqual(dna_contract.feature_count, 49)  # 45 + 4 CAMP
        self.assertEqual(dna_contract.model_name, 'dna_analyzer')
        
        # Temporal contract
        temporal_contract = ContractBuilder.build_temporal_model_contract(self.registry)
        self.assertEqual(temporal_contract.feature_count, 48)  # 45 + 3 temporal
        
        # Industry contract
        industry_contract = ContractBuilder.build_industry_model_contract(self.registry)
        self.assertEqual(industry_contract.feature_count, 45)  # Base features only
        
        # Ensemble contract
        ensemble_contract = ContractBuilder.build_ensemble_model_contract()
        self.assertEqual(ensemble_contract.feature_count, 3)  # Model predictions only
    
    def test_contract_validation(self):
        """Test contract input validation"""
        contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
        
        # Valid input
        is_valid, errors = contract.validate_input(self.sample_data)
        self.assertTrue(is_valid)
        
        # Missing required features
        incomplete_data = self.sample_data.drop(columns=['funding_stage'])
        is_valid, errors = contract.validate_input(incomplete_data)
        self.assertFalse(is_valid)
    
    def test_feature_preparation(self):
        """Test contract prepares features correctly"""
        # DNA contract should add CAMP scores
        dna_contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
        features = dna_contract.prepare_features(self.sample_data.iloc[:1])
        
        self.assertEqual(features.shape[1], 49)
        
        # Temporal contract should add temporal features
        temporal_contract = ContractBuilder.build_temporal_model_contract(self.registry)
        features = temporal_contract.prepare_features(self.sample_data.iloc[:1])
        
        self.assertEqual(features.shape[1], 48)


class TestFeaturePipeline(ContractTestCase):
    """Test unified feature pipeline"""
    
    def test_pipeline_fitting(self):
        """Test pipeline fits correctly"""
        pipeline = UnifiedFeaturePipeline(self.registry)
        pipeline.fit(self.sample_data)
        
        self.assertTrue(pipeline.is_fitted)
        self.assertGreater(len(pipeline.numeric_features), 0)
        self.assertGreater(len(pipeline.categorical_features), 0)
    
    def test_camp_score_calculation(self):
        """Test CAMP scores are calculated correctly"""
        # Transform with DNA contract (includes CAMP scores)
        dna_contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
        transformed = self.pipeline.transform(self.sample_data, dna_contract)
        
        # Should have 49 features (45 + 4 CAMP)
        self.assertEqual(transformed.shape[1], 49)
    
    def test_temporal_feature_extraction(self):
        """Test temporal features are extracted correctly"""
        temporal_contract = ContractBuilder.build_temporal_model_contract(self.registry)
        transformed = self.pipeline.transform(self.sample_data, temporal_contract)
        
        # Should have 48 features (45 + 3 temporal)
        self.assertEqual(transformed.shape[1], 48)
    
    def test_categorical_encoding(self):
        """Test categorical features are encoded properly"""
        # Check that categorical features are encoded
        transformed = self.pipeline.transform(self.sample_data)
        
        # All values should be numeric after transformation
        self.assertTrue(np.issubdtype(transformed.dtype, np.number))


class TestContractualModel(ContractTestCase):
    """Test contractual model wrapper"""
    
    def setUp(self):
        super().setUp()
        
        # Create a dummy model for testing
        from sklearn.ensemble import RandomForestClassifier
        self.dummy_model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        # Create dummy training data
        X = self.sample_data
        y = np.random.randint(0, 2, len(X))
        
        # Fit pipeline and model
        self.pipeline.fit(X)
        
        # Create contract and prepare features
        self.contract = ContractBuilder.build_industry_model_contract(self.registry)
        X_transformed = self.pipeline.transform(X, self.contract)
        self.dummy_model.fit(X_transformed, y)
        
        # Create metadata
        self.metadata = ModelMetadata(
            model_name="test_model",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset="test_data",
            performance_metrics={'test_auc': 0.75}
        )
    
    def test_contractual_model_creation(self):
        """Test creating a contractual model"""
        model = ContractualModel(
            model=self.dummy_model,
            contract=self.contract,
            feature_pipeline=self.pipeline,
            metadata=self.metadata
        )
        
        self.assertEqual(model.metadata.model_name, "test_model")
        self.assertEqual(model.contract.feature_count, 45)
    
    def test_prediction_with_validation(self):
        """Test prediction validates input"""
        model = ContractualModel(
            model=self.dummy_model,
            contract=self.contract,
            feature_pipeline=self.pipeline,
            metadata=self.metadata
        )
        
        # Valid prediction
        sample = self.sample_data.iloc[:1]
        predictions = model.predict(sample)
        self.assertEqual(len(predictions), 1)
        self.assertTrue(0 <= predictions[0] <= 1)
        
        # Invalid prediction (missing features)
        with self.assertRaises(ValueError):
            model.predict({'funding_stage': 'seed'})  # Incomplete
    
    def test_model_diagnostics(self):
        """Test model returns diagnostics"""
        model = ContractualModel(
            model=self.dummy_model,
            contract=self.contract,
            feature_pipeline=self.pipeline,
            metadata=self.metadata
        )
        
        sample = self.sample_data.iloc[:1]
        predictions, diagnostics = model.predict(sample, return_diagnostics=True)
        
        self.assertIn('model_id', diagnostics)
        self.assertIn('duration_ms', diagnostics)
        self.assertIn('features_prepared', diagnostics)
        self.assertTrue(diagnostics['success'])
    
    def test_model_persistence(self):
        """Test saving and loading contractual models"""
        model = ContractualModel(
            model=self.dummy_model,
            contract=self.contract,
            feature_pipeline=self.pipeline,
            metadata=self.metadata
        )
        
        # Save model
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            model.save(tmp.name)
            
            # Load model
            loaded_model = ContractualModel.load(tmp.name, self.registry)
            
            # Verify loaded model works
            sample = self.sample_data.iloc[:1]
            original_pred = model.predict(sample)
            loaded_pred = loaded_model.predict(sample)
            
            np.testing.assert_array_almost_equal(original_pred, loaded_pred)


class TestContractConsistency(ContractTestCase):
    """Test contract consistency across the system"""
    
    def test_feature_count_consistency(self):
        """Test feature counts are consistent"""
        # Create contracts
        dna_contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
        temporal_contract = ContractBuilder.build_temporal_model_contract(self.registry)
        industry_contract = ContractBuilder.build_industry_model_contract(self.registry)
        
        # Transform data with each contract
        dna_features = self.pipeline.transform(self.sample_data, dna_contract)
        temporal_features = self.pipeline.transform(self.sample_data, temporal_contract)
        industry_features = self.pipeline.transform(self.sample_data, industry_contract)
        
        # Verify shapes match contracts
        self.assertEqual(dna_features.shape[1], dna_contract.feature_count)
        self.assertEqual(temporal_features.shape[1], temporal_contract.feature_count)
        self.assertEqual(industry_features.shape[1], industry_contract.feature_count)
    
    def test_prediction_consistency(self):
        """Test predictions are consistent for same input"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Create and train a model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        contract = ContractBuilder.build_industry_model_contract(self.registry)
        
        X = self.sample_data
        y = np.random.randint(0, 2, len(X))
        
        X_transformed = self.pipeline.transform(X, contract)
        model.fit(X_transformed, y)
        
        # Create contractual model
        metadata = ModelMetadata(
            model_name="consistency_test",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset="test",
            performance_metrics={}
        )
        
        contractual_model = ContractualModel(
            model=model,
            contract=contract,
            feature_pipeline=self.pipeline,
            metadata=metadata
        )
        
        # Test same input gives same output
        sample = self.sample_data.iloc[:1]
        pred1 = contractual_model.predict(sample)
        pred2 = contractual_model.predict(sample)
        
        np.testing.assert_array_equal(pred1, pred2)
    
    def test_contract_validation_prevents_errors(self):
        """Test contracts prevent feature mismatch errors"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Train model with 45 features
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        contract = ContractBuilder.build_industry_model_contract(self.registry)
        
        X = self.sample_data
        y = np.random.randint(0, 2, len(X))
        
        X_transformed = self.pipeline.transform(X, contract)
        model.fit(X_transformed, y)
        
        # Try to use model with different contract (should fail gracefully)
        wrong_contract = ContractBuilder.build_ensemble_model_contract()
        
        metadata = ModelMetadata(
            model_name="mismatch_test",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset="test",
            performance_metrics={}
        )
        
        contractual_model = ContractualModel(
            model=model,
            contract=wrong_contract,  # Wrong contract!
            feature_pipeline=self.pipeline,
            metadata=metadata
        )
        
        # Should raise error due to contract mismatch
        with self.assertRaises(ValueError):
            contractual_model.predict({'dna_prediction': 0.5, 'temporal_prediction': 0.6, 'industry_prediction': 0.7})


def run_contract_tests():
    """Run all contract tests"""
    unittest.main(module=__name__, exit=False, verbosity=2)


if __name__ == "__main__":
    run_contract_tests()