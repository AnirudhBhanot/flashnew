"""
Comprehensive Tests for Contractual Architecture
Tests the entire new system end-to-end
"""

import unittest
import sys
import os
import tempfile
import json
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.feature_registry import feature_registry
from core.model_contracts import ModelContract, ContractBuilder
from core.feature_pipeline import UnifiedFeaturePipeline
from core.model_wrapper import ContractualModel, ModelMetadata
from core.training_system import UnifiedTrainingSystem
from core.schema_evolution import SchemaEvolution
from core.contract_testing import run_contract_tests


class TestContractualArchitecture(unittest.TestCase):
    """End-to-end tests for the contractual architecture"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test environment once"""
        # Create test data
        cls.test_data = cls._create_test_dataset()
        cls.test_data_path = "test_data.csv"
        cls.test_data.to_csv(cls.test_data_path, index=False)
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup after tests"""
        if os.path.exists(cls.test_data_path):
            os.remove(cls.test_data_path)
    
    @classmethod
    def _create_test_dataset(cls, n_samples=500):
        """Create realistic test dataset"""
        np.random.seed(42)
        
        data = {
            # Capital features
            'funding_stage': np.random.choice(['pre_seed', 'seed', 'series_a', 'series_b'], n_samples),
            'revenue_growth_rate': np.random.uniform(-50, 300, n_samples),
            'total_capital_raised_usd': np.random.lognormal(13, 2, n_samples),
            'annual_recurring_revenue_millions': np.random.lognormal(0, 1, n_samples),
            'annual_revenue_run_rate': np.random.lognormal(12, 2, n_samples),
            'burn_multiple': np.random.uniform(0.5, 5, n_samples),
            'investor_tier_primary': np.random.choice(['tier_1', 'tier_2', 'tier_3'], n_samples),
            'active_investors': np.random.randint(1, 10, n_samples),
            'cash_on_hand_months': np.random.uniform(6, 36, n_samples),
            'runway_months': np.random.uniform(6, 36, n_samples),
            'time_to_next_funding': np.random.randint(6, 24, n_samples),
            
            # Market features
            'market_tam_billions': np.random.lognormal(2, 1, n_samples),
            'market_growth_rate': np.random.uniform(5, 50, n_samples),
            'market_competitiveness': np.random.randint(1, 6, n_samples),
            'customer_acquisition_cost': np.random.lognormal(4, 1, n_samples),
            'customer_lifetime_value': np.random.lognormal(7, 1, n_samples),
            'customer_growth_rate': np.random.uniform(-20, 200, n_samples),
            'net_revenue_retention': np.random.uniform(80, 150, n_samples),
            'average_deal_size': np.random.lognormal(7, 2, n_samples),
            'sales_cycle_days': np.random.randint(7, 180, n_samples),
            'international_revenue_percent': np.random.uniform(0, 50, n_samples),
            'target_enterprise': np.random.choice([True, False], n_samples),
            'media_coverage': np.random.randint(1, 6, n_samples),
            'regulatory_risk': np.random.randint(1, 6, n_samples),
            
            # Product features
            'product_market_fit_score': np.random.randint(1, 6, n_samples),
            'technology_score': np.random.randint(1, 6, n_samples),
            'scalability_score': np.random.randint(1, 6, n_samples),
            'has_patent': np.random.choice([True, False], n_samples),
            'research_development_percent': np.random.uniform(5, 30, n_samples),
            'uses_ai_ml': np.random.choice([True, False], n_samples),
            'cloud_native': np.random.choice([True, False], n_samples),
            'mobile_first': np.random.choice([True, False], n_samples),
            'platform_business': np.random.choice([True, False], n_samples),
            
            # People features
            'team_size_full_time': np.random.randint(1, 100, n_samples),
            'founder_experience_years': np.random.randint(0, 30, n_samples),
            'repeat_founder': np.random.choice([True, False], n_samples),
            'technical_founder': np.random.choice([True, False], n_samples),
            'employee_growth_rate': np.random.uniform(-50, 300, n_samples),
            'advisor_quality_score': np.random.randint(1, 6, n_samples),
            'board_diversity_score': np.random.randint(1, 6, n_samples),
            'team_industry_experience': np.random.randint(0, 20, n_samples),
            'key_person_dependency': np.random.randint(1, 6, n_samples),
            'top_university_alumni': np.random.choice([True, False], n_samples),
            'previous_exit': np.random.choice([True, False], n_samples),
            'industry_connections': np.random.randint(1, 6, n_samples),
            
            # Target (create realistic success labels based on features)
            'success_label': np.zeros(n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create realistic success labels based on feature combinations
        success_score = (
            (df['revenue_growth_rate'] > 100).astype(int) +
            (df['product_market_fit_score'] >= 4).astype(int) +
            (df['net_revenue_retention'] > 110).astype(int) +
            (df['burn_multiple'] < 2).astype(int) +
            (df['repeat_founder']).astype(int) +
            (df['customer_lifetime_value'] > df['customer_acquisition_cost'] * 3).astype(int)
        )
        
        df['success_label'] = (success_score >= 4).astype(int)
        
        return df
    
    def test_01_feature_registry(self):
        """Test feature registry is properly initialized"""
        # Check registry has correct number of features
        self.assertEqual(len(feature_registry.features), 45)
        
        # Check all features have required attributes
        for name, feature in feature_registry.features.items():
            self.assertIsNotNone(feature.position)
            self.assertIn(feature.category, ['capital', 'advantage', 'market', 'people', 'product'])
    
    def test_02_model_contracts(self):
        """Test model contracts are created correctly"""
        # Test each contract type
        contracts = {
            'dna': ContractBuilder.build_dna_analyzer_contract(feature_registry),
            'temporal': ContractBuilder.build_temporal_model_contract(feature_registry),
            'industry': ContractBuilder.build_industry_model_contract(feature_registry),
            'ensemble': ContractBuilder.build_ensemble_model_contract()
        }
        
        # Verify feature counts
        self.assertEqual(contracts['dna'].feature_count, 49)  # 45 + 4 CAMP
        self.assertEqual(contracts['temporal'].feature_count, 48)  # 45 + 3 temporal
        self.assertEqual(contracts['industry'].feature_count, 45)  # Base only
        self.assertEqual(contracts['ensemble'].feature_count, 3)  # Predictions only
    
    def test_03_training_system(self):
        """Test the unified training system"""
        # Create training system
        trainer = UnifiedTrainingSystem(feature_registry, output_dir="test_models")
        
        # Train models (using small test dataset)
        models = trainer.train_all_models(self.test_data_path, save_models=False)
        
        # Verify all models trained
        self.assertEqual(len(models), 4)
        self.assertIn('dna_analyzer', models)
        self.assertIn('temporal_model', models)
        self.assertIn('industry_model', models)
        self.assertIn('ensemble_model', models)
        
        # Test predictions
        sample = self.test_data.iloc[:1].drop(columns=['success_label'])
        
        for name, model in models.items():
            if name != 'ensemble_model':  # Ensemble needs special input
                pred = model.predict(sample)
                self.assertEqual(len(pred), 1)
                self.assertTrue(0 <= pred[0] <= 1)
    
    def test_04_contractual_model_features(self):
        """Test contractual model wrapper features"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Create simple model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        contract = ContractBuilder.build_industry_model_contract(feature_registry)
        
        # Prepare data
        pipeline = UnifiedFeaturePipeline(feature_registry)
        X = self.test_data.drop(columns=['success_label'])
        y = self.test_data['success_label']
        
        pipeline.fit(X)
        X_transformed = pipeline.transform(X, contract)
        model.fit(X_transformed, y)
        
        # Create metadata
        metadata = ModelMetadata(
            model_name="test_model",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset="test",
            performance_metrics={'test_auc': 0.75}
        )
        
        # Create contractual model
        contractual_model = ContractualModel(model, contract, pipeline, metadata)
        
        # Test features
        # 1. Prediction with diagnostics
        sample = X.iloc[:1]
        pred, diag = contractual_model.predict(sample, return_diagnostics=True)
        self.assertIn('duration_ms', diag)
        self.assertTrue(diag['success'])
        
        # 2. Model info
        info = contractual_model.get_model_info()
        self.assertEqual(info['model_name'], 'test_model')
        self.assertEqual(info['feature_count'], 45)
        
        # 3. Feature importance
        importance = contractual_model.get_feature_importance()
        self.assertIsNotNone(importance)
        self.assertEqual(len(importance), 45)
    
    def test_05_schema_evolution(self):
        """Test schema evolution capabilities"""
        # Create evolution system
        evolution = SchemaEvolution(feature_registry)
        
        # Add a new feature
        migration = evolution.add_feature(
            feature_name="test_feature",
            dtype=float,
            category="market",
            description="Test feature for evolution",
            default_value=0.0,
            computation=lambda df: df['revenue_growth_rate'] * 2
        )
        
        self.assertEqual(migration.migration_type.value, "add_feature")
        self.assertEqual(evolution.current_version, "1.0.1")
        
        # Test data migration
        sample_data = {'revenue_growth_rate': 100.0, 'team_size_full_time': 10}
        migrated = evolution.migrate_data(sample_data, "1.0.0", "1.0.1")
        
        self.assertIn('test_feature', migrated)
        self.assertEqual(migrated['test_feature'], 200.0)  # 100 * 2
    
    def test_06_api_integration(self):
        """Test API server integration"""
        from core.api_server_contractual import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        # Test features endpoint
        response = client.get("/features")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_features'], 45)
        
        # Test validation endpoint
        test_input = {
            'funding_stage': 'seed',
            'revenue_growth_rate': 100.0,
            'team_size_full_time': 10,
            'total_capital_raised_usd': 1000000.0,
            'annual_recurring_revenue_millions': 0.5,
            'annual_revenue_run_rate': 500000.0,
            'burn_multiple': 2.0,
            'market_tam_billions': 5.0,
            'market_growth_rate': 20.0,
            'market_competitiveness': 3,
            'customer_acquisition_cost': 100.0,
            'customer_lifetime_value': 1000.0,
            'customer_growth_rate': 50.0,
            'net_revenue_retention': 110.0,
            'average_deal_size': 1000.0,
            'sales_cycle_days': 30,
            'international_revenue_percent': 10.0,
            'target_enterprise': False,
            'product_market_fit_score': 4,
            'technology_score': 4,
            'scalability_score': 4,
            'has_patent': False,
            'research_development_percent': 15.0,
            'uses_ai_ml': True,
            'cloud_native': True,
            'mobile_first': False,
            'platform_business': True,
            'founder_experience_years': 10,
            'repeat_founder': True,
            'technical_founder': True,
            'employee_growth_rate': 100.0,
            'advisor_quality_score': 4,
            'board_diversity_score': 3,
            'team_industry_experience': 8,
            'key_person_dependency': 2,
            'top_university_alumni': True,
            'investor_tier_primary': 'tier_1',
            'active_investors': 3,
            'cash_on_hand_months': 18.0,
            'runway_months': 18.0,
            'time_to_next_funding': 12,
            'previous_exit': True,
            'industry_connections': 4,
            'media_coverage': 3,
            'regulatory_risk': 2
        }
        
        response = client.post("/validate", json=test_input)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['valid'])
    
    def test_07_contract_testing_framework(self):
        """Test the contract testing framework itself"""
        # Run contract tests
        # Note: This would normally use unittest discovery
        # but we'll just verify the framework exists
        from core.contract_testing import ContractTestCase, TestFeatureRegistry
        
        # Create test instance
        test = TestFeatureRegistry()
        test.setUp()
        
        # Run a sample test
        test.test_registry_initialization()
        test.test_feature_ordering()
        
        # If we get here without exceptions, tests passed
        self.assertTrue(True)
    
    def test_08_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Create training system
        trainer = UnifiedTrainingSystem(feature_registry, output_dir="test_e2e_models")
        
        # 2. Train models
        models = trainer.train_all_models(self.test_data_path, save_models=True)
        
        # 3. Make predictions
        sample = self.test_data.iloc[:5].drop(columns=['success_label'])
        
        predictions = {}
        for name, model in models.items():
            if name != 'ensemble_model':
                predictions[name] = model.predict(sample)
        
        # 4. Verify ensemble uses base predictions
        ensemble_input = pd.DataFrame({
            'dna_prediction': predictions['dna_analyzer'],
            'temporal_prediction': predictions['temporal_model'],
            'industry_prediction': predictions['industry_model']
        })
        
        ensemble_pred = models['ensemble_model'].predict(ensemble_input)
        
        # 5. Verify all predictions are valid
        for name, preds in predictions.items():
            self.assertEqual(len(preds), 5)
            self.assertTrue(all(0 <= p <= 1 for p in preds))
        
        self.assertEqual(len(ensemble_pred), 5)
        self.assertTrue(all(0 <= p <= 1 for p in ensemble_pred))
        
        # 6. Test model persistence
        # Save and reload a model
        test_model = models['industry_model']
        test_model.save("test_e2e_models/test_save.pkl")
        
        loaded_model = ContractualModel.load("test_e2e_models/test_save.pkl", feature_registry)
        
        # Verify loaded model works
        loaded_pred = loaded_model.predict(sample)
        np.testing.assert_array_almost_equal(predictions['industry_model'], loaded_pred)
        
        # Cleanup
        import shutil
        if os.path.exists("test_e2e_models"):
            shutil.rmtree("test_e2e_models")
    
    def test_09_error_handling(self):
        """Test error handling and edge cases"""
        from sklearn.ensemble import RandomForestClassifier
        
        # Create model with specific contract
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        contract = ContractBuilder.build_industry_model_contract(feature_registry)
        
        # Prepare pipeline
        pipeline = UnifiedFeaturePipeline(feature_registry)
        X = self.test_data.drop(columns=['success_label'])
        y = self.test_data['success_label']
        
        pipeline.fit(X)
        X_transformed = pipeline.transform(X, contract)
        model.fit(X_transformed, y)
        
        # Create contractual model
        metadata = ModelMetadata(
            model_name="error_test",
            model_version="1.0.0",
            training_date=datetime.now(),
            training_dataset="test",
            performance_metrics={}
        )
        
        contractual_model = ContractualModel(model, contract, pipeline, metadata)
        
        # Test 1: Missing features
        with self.assertRaises(ValueError):
            contractual_model.predict({'funding_stage': 'seed'})  # Incomplete
        
        # Test 2: Wrong feature types
        bad_data = X.iloc[:1].to_dict('records')[0]
        bad_data['team_size_full_time'] = 'not_a_number'
        
        with self.assertRaises(Exception):
            contractual_model.predict(bad_data)
        
        # Test 3: Extra features (should be ignored)
        extra_data = X.iloc[:1].to_dict('records')[0]
        extra_data['extra_feature'] = 'ignored'
        
        # This should work - extra features are ignored
        pred = contractual_model.predict(extra_data)
        self.assertEqual(len(pred), 1)


def run_all_tests():
    """Run all contractual architecture tests"""
    # Run unit tests
    print("Running Contractual Architecture Tests...")
    unittest.main(module=__name__, exit=False, verbosity=2)
    
    # Run contract framework tests
    print("\nRunning Contract Framework Tests...")
    run_contract_tests()


if __name__ == "__main__":
    run_all_tests()