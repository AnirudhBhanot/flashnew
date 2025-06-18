"""
Migration Script - Convert existing models to contractual system
This script migrates the current FLASH models to the new contract-based architecture
"""

import os
import sys
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import json

# Add core module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.feature_registry import feature_registry
from core.model_contracts import ContractBuilder
from core.feature_pipeline import UnifiedFeaturePipeline
from core.model_wrapper import ContractualModel, ModelMetadata
from core.training_system import UnifiedTrainingSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelMigrator:
    """Migrate existing models to contractual system"""
    
    def __init__(self, 
                 existing_models_dir: str = "models/production_v45",
                 output_dir: str = "models/contractual",
                 data_path: str = "data/final_100k_dataset_45features.csv"):
        self.existing_models_dir = Path(existing_models_dir)
        self.output_dir = Path(output_dir)
        self.data_path = data_path
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.registry = feature_registry
        self.pipeline = None
        self.migration_report = {
            'timestamp': datetime.now().isoformat(),
            'models_migrated': [],
            'errors': [],
            'warnings': []
        }
    
    def prepare_pipeline(self):
        """Prepare the unified feature pipeline"""
        logger.info("Preparing unified feature pipeline...")
        
        # Load sample data to fit pipeline
        df = pd.read_csv(self.data_path)
        
        # Take a sample for fitting (faster)
        sample_size = min(1000, len(df))
        sample_df = df.sample(n=sample_size, random_state=42)
        
        # Drop target column if exists
        if 'success_label' in sample_df.columns:
            sample_df = sample_df.drop(columns=['success_label'])
        
        # Create and fit pipeline
        self.pipeline = UnifiedFeaturePipeline(self.registry)
        self.pipeline.fit(sample_df)
        
        # Save fitted pipeline
        pipeline_path = self.output_dir / "unified_pipeline.pkl"
        self.pipeline.save(str(pipeline_path))
        logger.info(f"Saved fitted pipeline to {pipeline_path}")
    
    def migrate_dna_analyzer(self):
        """Migrate DNA Analyzer model"""
        model_name = "dna_analyzer"
        model_path = self.existing_models_dir / f"{model_name}.pkl"
        
        if not model_path.exists():
            self.migration_report['errors'].append(f"{model_name} not found at {model_path}")
            return
        
        try:
            logger.info(f"Migrating {model_name}...")
            
            # Load existing model
            model = joblib.load(model_path)
            
            # Create contract for DNA analyzer (45 + 4 CAMP = 49 features)
            contract = ContractBuilder.build_dna_analyzer_contract(self.registry)
            
            # Create metadata from existing model
            metadata = ModelMetadata(
                model_name=model_name,
                model_version="2.0.0",
                training_date=datetime.now(),
                training_dataset="migrated_from_v45",
                performance_metrics={
                    'test_auc': 0.7712,  # From documentation
                    'migrated': True
                }
            )
            
            # Wrap in contractual model
            contractual_model = ContractualModel(
                model=model,
                contract=contract,
                feature_pipeline=self.pipeline,
                metadata=metadata
            )
            
            # Test the model with sample data
            test_successful = self._test_migrated_model(contractual_model, model_name)
            
            if test_successful:
                # Save contractual model
                output_path = self.output_dir / f"{model_name}.pkl"
                contractual_model.save(str(output_path))
                logger.info(f"Saved {model_name} to {output_path}")
                
                self.migration_report['models_migrated'].append({
                    'name': model_name,
                    'contract_features': contract.feature_count,
                    'output_path': str(output_path)
                })
            else:
                self.migration_report['errors'].append(f"{model_name} failed testing")
                
        except Exception as e:
            logger.error(f"Failed to migrate {model_name}: {e}")
            self.migration_report['errors'].append(f"{model_name}: {str(e)}")
    
    def migrate_temporal_model(self):
        """Migrate Temporal model"""
        model_name = "temporal_model"
        model_path = self.existing_models_dir / f"{model_name}.pkl"
        
        if not model_path.exists():
            self.migration_report['errors'].append(f"{model_name} not found at {model_path}")
            return
        
        try:
            logger.info(f"Migrating {model_name}...")
            
            # Load existing model
            model = joblib.load(model_path)
            
            # Create contract for temporal model (45 + 3 temporal = 48 features)
            contract = ContractBuilder.build_temporal_model_contract(self.registry)
            
            # Create metadata
            metadata = ModelMetadata(
                model_name=model_name,
                model_version="2.0.0",
                training_date=datetime.now(),
                training_dataset="migrated_from_v45",
                performance_metrics={
                    'test_auc': 0.7736,  # From documentation
                    'migrated': True
                }
            )
            
            # Wrap in contractual model
            contractual_model = ContractualModel(
                model=model,
                contract=contract,
                feature_pipeline=self.pipeline,
                metadata=metadata
            )
            
            # Test the model
            test_successful = self._test_migrated_model(contractual_model, model_name)
            
            if test_successful:
                # Save contractual model
                output_path = self.output_dir / f"{model_name}.pkl"
                contractual_model.save(str(output_path))
                logger.info(f"Saved {model_name} to {output_path}")
                
                self.migration_report['models_migrated'].append({
                    'name': model_name,
                    'contract_features': contract.feature_count,
                    'output_path': str(output_path)
                })
            else:
                self.migration_report['errors'].append(f"{model_name} failed testing")
                
        except Exception as e:
            logger.error(f"Failed to migrate {model_name}: {e}")
            self.migration_report['errors'].append(f"{model_name}: {str(e)}")
    
    def migrate_industry_model(self):
        """Migrate Industry model"""
        model_name = "industry_model"
        model_path = self.existing_models_dir / f"{model_name}.pkl"
        
        if not model_path.exists():
            self.migration_report['errors'].append(f"{model_name} not found at {model_path}")
            return
        
        try:
            logger.info(f"Migrating {model_name}...")
            
            # Load existing model
            model = joblib.load(model_path)
            
            # Create contract for industry model (45 features only)
            contract = ContractBuilder.build_industry_model_contract(self.registry)
            
            # Create metadata
            metadata = ModelMetadata(
                model_name=model_name,
                model_version="2.0.0",
                training_date=datetime.now(),
                training_dataset="migrated_from_v45",
                performance_metrics={
                    'test_auc': 0.7728,  # From documentation
                    'migrated': True
                }
            )
            
            # Wrap in contractual model
            contractual_model = ContractualModel(
                model=model,
                contract=contract,
                feature_pipeline=self.pipeline,
                metadata=metadata
            )
            
            # Test the model
            test_successful = self._test_migrated_model(contractual_model, model_name)
            
            if test_successful:
                # Save contractual model
                output_path = self.output_dir / f"{model_name}.pkl"
                contractual_model.save(str(output_path))
                logger.info(f"Saved {model_name} to {output_path}")
                
                self.migration_report['models_migrated'].append({
                    'name': model_name,
                    'contract_features': contract.feature_count,
                    'output_path': str(output_path)
                })
            else:
                self.migration_report['errors'].append(f"{model_name} failed testing")
                
        except Exception as e:
            logger.error(f"Failed to migrate {model_name}: {e}")
            self.migration_report['errors'].append(f"{model_name}: {str(e)}")
    
    def migrate_ensemble_model(self):
        """Migrate or create ensemble model"""
        model_name = "ensemble_model"
        model_path = self.existing_models_dir / f"{model_name}.pkl"
        
        # Note: Ensemble might need special handling or retraining
        if model_path.exists():
            self.migration_report['warnings'].append(
                f"{model_name} found but needs retraining with new base models"
            )
        else:
            self.migration_report['warnings'].append(
                f"{model_name} not found - needs to be trained after base model migration"
            )
        
        logger.info(f"Ensemble model migration skipped - requires retraining")
    
    def _test_migrated_model(self, model: ContractualModel, model_name: str) -> bool:
        """Test a migrated model with sample data"""
        try:
            # Create test data
            test_data = {
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
            
            # Test prediction
            prediction = model.predict(test_data)
            
            # Validate prediction
            if len(prediction) > 0 and 0 <= prediction[0] <= 1:
                logger.info(f"{model_name} test successful - prediction: {prediction[0]:.4f}")
                return True
            else:
                logger.error(f"{model_name} test failed - invalid prediction: {prediction}")
                return False
                
        except Exception as e:
            logger.error(f"{model_name} test failed with error: {e}")
            return False
    
    def migrate_all_models(self):
        """Migrate all models"""
        logger.info("=== Starting Model Migration ===")
        
        # Prepare pipeline first
        self.prepare_pipeline()
        
        # Migrate each model
        self.migrate_dna_analyzer()
        self.migrate_temporal_model()
        self.migrate_industry_model()
        self.migrate_ensemble_model()
        
        # Save migration report
        report_path = self.output_dir / "migration_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.migration_report, f, indent=2)
        
        logger.info(f"\n=== Migration Complete ===")
        logger.info(f"Models migrated: {len(self.migration_report['models_migrated'])}")
        logger.info(f"Errors: {len(self.migration_report['errors'])}")
        logger.info(f"Warnings: {len(self.migration_report['warnings'])}")
        logger.info(f"Report saved to: {report_path}")
        
        return self.migration_report


def retrain_with_contracts():
    """Alternative: Retrain all models with contracts from scratch"""
    logger.info("=== Retraining Models with Contracts ===")
    
    # Initialize training system
    trainer = UnifiedTrainingSystem(feature_registry)
    
    # Train all models
    data_path = "data/final_100k_dataset_45features.csv"
    models = trainer.train_all_models(data_path, save_models=True)
    
    logger.info(f"Trained {len(models)} models with contracts")
    
    # Generate report
    for name, model in models.items():
        info = model.get_model_info()
        logger.info(f"{name}: {info['feature_count']} features, "
                   f"AUC: {info['performance_metrics'].get('test_auc', 0):.4f}")


def verify_migration():
    """Verify migrated models work correctly"""
    logger.info("=== Verifying Migration ===")
    
    from core.api_server_contractual import ModelRegistry
    
    # Load models
    registry = ModelRegistry()
    registry.load_models("models/contractual")
    
    # Test prediction
    test_data = {
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
    
    # Test each model
    for name, model in registry.models.items():
        try:
            pred = model.predict(test_data)
            logger.info(f"{name}: {pred[0]:.4f} ✓")
        except Exception as e:
            logger.error(f"{name}: Failed - {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate FLASH models to contractual system")
    parser.add_argument('--mode', choices=['migrate', 'retrain', 'verify'], 
                       default='migrate',
                       help='Migration mode: migrate existing models or retrain from scratch')
    parser.add_argument('--models-dir', default='models/production_v45',
                       help='Directory containing existing models')
    parser.add_argument('--output-dir', default='models/contractual',
                       help='Output directory for contractual models')
    parser.add_argument('--data-path', default='data/final_100k_dataset_45features.csv',
                       help='Path to training data')
    
    args = parser.parse_args()
    
    if args.mode == 'migrate':
        # Migrate existing models
        migrator = ModelMigrator(
            existing_models_dir=args.models_dir,
            output_dir=args.output_dir,
            data_path=args.data_path
        )
        report = migrator.migrate_all_models()
        
    elif args.mode == 'retrain':
        # Retrain from scratch
        retrain_with_contracts()
        
    elif args.mode == 'verify':
        # Verify migration
        verify_migration()