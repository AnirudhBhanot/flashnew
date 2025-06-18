#!/usr/bin/env python3
"""
Retrain all FLASH models from scratch using the contractual architecture
This ensures all models are properly aligned with contracts from the beginning
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.feature_registry import feature_registry
from core.training_system import UnifiedTrainingSystem
from core.api_server_contractual import ModelRegistry
from core.feature_mapping import map_dataset_to_registry, get_available_features

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_data_exists(data_path: str) -> bool:
    """Check if training data exists"""
    if not os.path.exists(data_path):
        logger.error(f"Training data not found at {data_path}")
        logger.error("Please ensure the data file exists before training")
        return False
    
    # Check data is valid
    try:
        df = pd.read_csv(data_path, nrows=5)
        logger.info(f"Found training data with {len(df.columns)} columns")
        
        # Check for required target column
        if 'success_label' not in df.columns and 'success' not in df.columns:
            logger.error("Target column 'success_label' or 'success' not found in data")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Error reading data file: {e}")
        return False


def verify_feature_alignment(data_path: str) -> bool:
    """Verify data features match registry after mapping"""
    df = pd.read_csv(data_path, nrows=100)
    
    # Get expected features from registry
    expected_features = set(feature_registry.get_feature_names())
    
    # Get available features after mapping
    available_features = set(get_available_features(df))
    
    # Check coverage
    coverage = len(available_features) / len(expected_features) * 100
    logger.info(f"Feature coverage: {len(available_features)}/{len(expected_features)} ({coverage:.1f}%)")
    
    # Missing features will be filled with defaults
    missing = expected_features - available_features
    if missing:
        logger.warning(f"Features to be filled with defaults: {len(missing)} features")
        logger.debug(f"Missing features: {missing}")
    
    # As long as we have reasonable coverage, we can proceed
    if coverage < 50:
        logger.error(f"Insufficient feature coverage: {coverage:.1f}%")
        return False
    
    logger.info("✓ Feature alignment verified (missing features will use defaults)")
    return True


def analyze_data_quality(data_path: str) -> dict:
    """Analyze data quality before training"""
    logger.info("Analyzing data quality...")
    
    df = pd.read_csv(data_path)
    
    analysis = {
        'total_samples': len(df),
        'features': len(df.columns) - 1,  # Exclude target
        'missing_values': {},
        'class_distribution': {},
        'feature_stats': {}
    }
    
    # Check class distribution
    target_col = 'success_label' if 'success_label' in df.columns else 'success'
    if target_col in df.columns:
        class_dist = df[target_col].value_counts().to_dict()
        analysis['class_distribution'] = {
            'success': class_dist.get(1, 0),
            'failure': class_dist.get(0, 0),
            'ratio': class_dist.get(1, 0) / len(df)
        }
        logger.info(f"Class distribution - Success: {class_dist.get(1, 0)}, Failure: {class_dist.get(0, 0)}")
    
    # Check missing values
    missing = df.isnull().sum()
    missing_features = missing[missing > 0].to_dict()
    if missing_features:
        analysis['missing_values'] = missing_features
        logger.warning(f"Found missing values in {len(missing_features)} features")
    
    # Basic statistics for numeric features
    numeric_features = df.select_dtypes(include=[np.number]).columns
    for feat in numeric_features[:5]:  # Sample a few
        if feat != 'success_label':
            analysis['feature_stats'][feat] = {
                'mean': float(df[feat].mean()),
                'std': float(df[feat].std()),
                'min': float(df[feat].min()),
                'max': float(df[feat].max())
            }
    
    return analysis


def train_models_with_contracts(data_path: str, output_dir: str = "models/contractual"):
    """Train all models using the contractual architecture"""
    
    logger.info("="*60)
    logger.info("FLASH Model Training with Contractual Architecture")
    logger.info("="*60)
    
    # Step 1: Verify data exists and is valid
    if not check_data_exists(data_path):
        return False
    
    # Step 2: Verify feature alignment
    if not verify_feature_alignment(data_path):
        return False
    
    # Step 3: Analyze data quality
    data_analysis = analyze_data_quality(data_path)
    
    # Step 4: Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {output_path}")
    
    # Step 5: Initialize training system
    logger.info("\nInitializing unified training system...")
    trainer = UnifiedTrainingSystem(
        feature_registry=feature_registry,
        output_dir=str(output_path)
    )
    
    # Step 6: Train all models
    logger.info("\nStarting model training...")
    logger.info("This will train 4 models:")
    logger.info("  1. DNA Analyzer (49 features: 45 base + 4 CAMP)")
    logger.info("  2. Temporal Model (48 features: 45 base + 3 temporal)")
    logger.info("  3. Industry Model (45 features: base only)")
    logger.info("  4. Ensemble Model (3 features: model predictions)")
    
    try:
        models = trainer.train_all_models(
            data_path=data_path,
            save_models=True
        )
        
        logger.info("\n✓ All models trained successfully!")
        
        # Step 7: Generate summary report
        summary = {
            'training_timestamp': datetime.now().isoformat(),
            'data_analysis': data_analysis,
            'models_trained': {},
            'feature_registry_version': feature_registry.version,
            'output_directory': str(output_path)
        }
        
        for name, model in models.items():
            model_info = model.get_model_info()
            summary['models_trained'][name] = {
                'model_id': model_info['model_id'],
                'feature_count': model_info['feature_count'],
                'performance': model_info['performance_metrics']
            }
        
        # Save summary
        summary_path = output_path / "training_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\nTraining summary saved to: {summary_path}")
        
        # Display performance summary
        logger.info("\nModel Performance Summary:")
        logger.info("-" * 40)
        for name, info in summary['models_trained'].items():
            auc = info['performance'].get('test_auc', 0)
            logger.info(f"{name:20s}: {auc:.4f} AUC")
        
        return True
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_trained_models(model_dir: str = "models/contractual"):
    """Verify the trained models work correctly"""
    logger.info("\n" + "="*60)
    logger.info("Verifying Trained Models")
    logger.info("="*60)
    
    # Load models using the model registry
    registry = ModelRegistry()
    # Use asyncio to run the async method
    import asyncio
    asyncio.run(registry.load_models(model_dir))
    
    if not registry.models:
        logger.error("No models found!")
        return False
    
    logger.info(f"Loaded {len(registry.models)} models")
    
    # Create test data
    test_data = {
        'funding_stage': 'seed',
        'revenue_growth_rate': 150.0,
        'team_size_full_time': 15,
        'total_capital_raised_usd': 2000000.0,
        'annual_recurring_revenue_millions': 1.0,
        'annual_revenue_run_rate': 1000000.0,
        'burn_multiple': 1.5,
        'market_tam_billions': 10.0,
        'market_growth_rate': 25.0,
        'market_competitiveness': 3,
        'customer_acquisition_cost': 200.0,
        'customer_lifetime_value': 2000.0,
        'customer_growth_rate': 100.0,
        'net_revenue_retention': 120.0,
        'average_deal_size': 5000.0,
        'sales_cycle_days': 45,
        'international_revenue_percent': 20.0,
        'target_enterprise': True,
        'product_market_fit_score': 4,
        'technology_score': 4,
        'scalability_score': 5,
        'has_patent': True,
        'research_development_percent': 20.0,
        'uses_ai_ml': True,
        'cloud_native': True,
        'mobile_first': False,
        'platform_business': True,
        'founder_experience_years': 12,
        'repeat_founder': True,
        'technical_founder': True,
        'employee_growth_rate': 150.0,
        'advisor_quality_score': 4,
        'board_diversity_score': 4,
        'team_industry_experience': 10,
        'key_person_dependency': 2,
        'top_university_alumni': True,
        'investor_tier_primary': 'tier_1',
        'active_investors': 5,
        'cash_on_hand_months': 24.0,
        'runway_months': 24.0,
        'time_to_next_funding': 12,
        'previous_exit': True,
        'industry_connections': 5,
        'media_coverage': 4,
        'regulatory_risk': 2
    }
    
    logger.info("\nTesting predictions with sample startup data...")
    
    # Test each model
    predictions = {}
    for name, model in registry.models.items():
        try:
            if name == 'ensemble_model':
                # Ensemble needs predictions from other models
                ensemble_input = {
                    'dna_prediction': predictions.get('dna_analyzer', 0.7),
                    'temporal_prediction': predictions.get('temporal_model', 0.7),
                    'industry_prediction': predictions.get('industry_model', 0.7)
                }
                pred, diagnostics = model.predict(ensemble_input, return_diagnostics=True)
            else:
                pred, diagnostics = model.predict(test_data, return_diagnostics=True)
            
            predictions[name] = float(pred[0])
            
            logger.info(f"✓ {name:20s}: {pred[0]:.4f} (took {diagnostics['duration_ms']:.1f}ms)")
            
        except Exception as e:
            logger.error(f"✗ {name:20s}: Failed - {e}")
            return False
    
    # Verify predictions are reasonable
    for name, pred in predictions.items():
        if not (0 <= pred <= 1):
            logger.error(f"Invalid prediction from {name}: {pred}")
            return False
    
    logger.info("\n✓ All models verified successfully!")
    
    # Test feature importance
    logger.info("\nTesting feature importance extraction...")
    for name, model in registry.models.items():
        if name != 'ensemble_model':  # Ensemble doesn't have feature importance
            importance = model.get_feature_importance()
            if importance is not None:
                top_features = importance.head(5)['feature'].tolist()
                logger.info(f"{name} top features: {', '.join(top_features)}")
    
    return True


def main():
    """Main training workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Train FLASH models with contractual architecture"
    )
    parser.add_argument(
        '--data-path',
        default='data/final_100k_dataset_45features.csv',
        help='Path to training data CSV file'
    )
    parser.add_argument(
        '--output-dir',
        default='models/contractual',
        help='Output directory for trained models'
    )
    parser.add_argument(
        '--skip-verification',
        action='store_true',
        help='Skip model verification after training'
    )
    
    args = parser.parse_args()
    
    # Train models
    success = train_models_with_contracts(
        data_path=args.data_path,
        output_dir=args.output_dir
    )
    
    if not success:
        logger.error("Training failed!")
        sys.exit(1)
    
    # Verify models unless skipped
    if not args.skip_verification:
        if not verify_trained_models(args.output_dir):
            logger.error("Model verification failed!")
            sys.exit(1)
    
    logger.info("\n" + "="*60)
    logger.info("✓ FLASH models successfully trained with contracts!")
    logger.info("="*60)
    logger.info(f"\nModels saved to: {args.output_dir}")
    logger.info("\nTo use the new models:")
    logger.info("  1. Start the API server:")
    logger.info("     cd core && python api_server_contractual.py")
    logger.info("  2. Or load models programmatically:")
    logger.info("     from core.model_wrapper import ContractualModel")
    logger.info(f"     model = ContractualModel.load('{args.output_dir}/dna_analyzer.pkl')")


if __name__ == "__main__":
    main()