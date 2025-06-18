#!/usr/bin/env python3
"""
Fix model feature mismatches in the FLASH system
"""

import numpy as np
import pandas as pd
import joblib
import json
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the feature configuration
from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES, BOOLEAN_FEATURES

def analyze_models():
    """Analyze all models to understand their requirements"""
    models_path = Path("models/production_v45_fixed")
    
    analysis = {}
    
    # Check each model
    for model_name in ['dna_analyzer', 'temporal_model', 'industry_model', 'ensemble_model']:
        model_path = models_path / f"{model_name}.pkl"
        if model_path.exists():
            try:
                model = joblib.load(model_path)
                info = {
                    'type': type(model).__name__,
                    'expected_features': getattr(model, 'n_features_in_', None),
                    'feature_names': list(getattr(model, 'feature_names_in_', [])),
                }
                
                # Check feature order file
                feature_order_path = models_path / f"{model_name.replace('_model', '')}_feature_order.pkl"
                if feature_order_path.exists():
                    try:
                        feature_order = joblib.load(feature_order_path)
                        info['feature_order_count'] = len(feature_order)
                        info['feature_order'] = feature_order
                    except:
                        logger.warning(f"Could not load feature order for {model_name}")
                
                analysis[model_name] = info
                logger.info(f"{model_name}: {info['expected_features']} features expected")
                
            except Exception as e:
                logger.error(f"Error loading {model_name}: {e}")
    
    return analysis

def fix_orchestrator_preparation():
    """Update the orchestrator to properly prepare features for each model"""
    
    # Create a fixed version of the orchestrator preparation methods
    orchestrator_fix = '''
    def _prepare_industry_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for industry model - expects 45 base features"""
        # Industry model expects exactly 45 canonical features
        from feature_config import ALL_FEATURES
        
        # Create a dataframe with all expected features
        prepared = pd.DataFrame(columns=ALL_FEATURES)
        
        # Copy over available features
        for col in ALL_FEATURES:
            if col in features.columns:
                prepared[col] = features[col].values
            else:
                # Use appropriate defaults
                if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency']:
                    prepared[col] = False
                elif col.endswith('_percent') or col.endswith('_score'):
                    prepared[col] = 0.0
                else:
                    prepared[col] = 0
        
        # Ensure numeric types
        for col in prepared.columns:
            if col not in CATEGORICAL_FEATURES:
                prepared[col] = pd.to_numeric(prepared[col], errors='coerce').fillna(0)
        
        return prepared
    
    def _prepare_temporal_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for temporal model - expects 46 features (45 base + burn_efficiency)"""
        # Start with the 45 base features
        temporal_features = self._prepare_industry_features(features)
        
        # Add burn_efficiency as the 46th feature
        if 'annual_revenue_run_rate' in temporal_features.columns and 'monthly_burn_usd' in temporal_features.columns:
            revenue = temporal_features['annual_revenue_run_rate'].fillna(0)
            burn = temporal_features['monthly_burn_usd'].fillna(1)  # Avoid division by zero
            temporal_features['burn_efficiency'] = (revenue / 12) / burn.replace(0, 1)
        else:
            temporal_features['burn_efficiency'] = 0.5  # Default middle value
        
        return temporal_features
    '''
    
    # Update the unified orchestrator file
    orchestrator_path = Path("models/unified_orchestrator_v3_integrated.py")
    if orchestrator_path.exists():
        content = orchestrator_path.read_text()
        
        # Find and replace the _prepare_temporal_features method
        import re
        
        # Replace the temporal features method
        temporal_pattern = r'def _prepare_temporal_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return temporal_features'
        temporal_replacement = '''def _prepare_temporal_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for temporal model - expects 46 features (45 base + burn_efficiency)"""
        # Start with the 45 base features
        from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES
        
        # Create a dataframe with all expected features
        temporal_features = pd.DataFrame(columns=ALL_FEATURES)
        
        # Copy over available features
        for col in ALL_FEATURES:
            if col in features.columns:
                temporal_features[col] = features[col].values
            else:
                # Use appropriate defaults
                if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency']:
                    temporal_features[col] = False
                elif col.endswith('_percent') or col.endswith('_score'):
                    temporal_features[col] = 0.0
                else:
                    temporal_features[col] = 0
        
        # Ensure numeric types
        for col in temporal_features.columns:
            if col not in CATEGORICAL_FEATURES:
                temporal_features[col] = pd.to_numeric(temporal_features[col], errors='coerce').fillna(0)
        
        # Add burn_efficiency as the 46th feature
        if 'annual_revenue_run_rate' in temporal_features.columns and 'monthly_burn_usd' in temporal_features.columns:
            revenue = temporal_features['annual_revenue_run_rate'].fillna(0)
            burn = temporal_features['monthly_burn_usd'].fillna(1)  # Avoid division by zero
            temporal_features['burn_efficiency'] = (revenue / 12) / burn.replace(0, 1)
        else:
            temporal_features['burn_efficiency'] = 0.5  # Default middle value
        
        return temporal_features'''
        
        content_new = re.sub(temporal_pattern, temporal_replacement, content, flags=re.DOTALL)
        
        # Add the _prepare_industry_features method if it doesn't exist
        if '_prepare_industry_features' not in content:
            # Find a good place to insert it (after _prepare_dna_features)
            dna_pattern = r'(def _prepare_dna_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return features\n)'
            industry_method = '''
    def _prepare_industry_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for industry model - expects 45 base features"""
        # Industry model expects exactly 45 canonical features
        from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES
        
        # Create a dataframe with all expected features
        prepared = pd.DataFrame(columns=ALL_FEATURES)
        
        # Copy over available features
        for col in ALL_FEATURES:
            if col in features.columns:
                prepared[col] = features[col].values
            else:
                # Use appropriate defaults
                if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency']:
                    prepared[col] = False
                elif col.endswith('_percent') or col.endswith('_score'):
                    prepared[col] = 0.0
                else:
                    prepared[col] = 0
        
        # Ensure numeric types
        for col in prepared.columns:
            if col not in CATEGORICAL_FEATURES:
                prepared[col] = pd.to_numeric(prepared[col], errors='coerce').fillna(0)
        
        return prepared
'''
            content_new = re.sub(dna_pattern, r'\1\n' + industry_method, content_new, flags=re.DOTALL)
        
        # Update how industry model is called in predict method
        industry_pattern = r'if "industry_model" in self\.models:\s*industry_pred = self\.models\["industry_model"\]\.predict_proba\(features\)'
        industry_replacement = '''if "industry_model" in self.models:
                industry_features = self._prepare_industry_features(features)
                industry_pred = self.models["industry_model"].predict_proba(industry_features)'''
        
        content_new = re.sub(industry_pattern, industry_replacement, content_new, flags=re.DOTALL)
        
        # Save the updated orchestrator
        orchestrator_path.write_text(content_new)
        logger.info("Updated orchestrator with fixed preparation methods")

def fix_ensemble_model():
    """Fix the ensemble model to use proper inputs"""
    # The ensemble model expects predictions from the other three models
    # We need to update how it's called in the orchestrator
    
    orchestrator_path = Path("models/unified_orchestrator_v3_integrated.py")
    if orchestrator_path.exists():
        content = orchestrator_path.read_text()
        
        # Add ensemble prediction logic after all base models have predicted
        ensemble_fix = '''
            # 5. Ensemble Model (if available)
            if "ensemble_model" in self.models and all(k in predictions for k in ["dna_analyzer", "temporal_prediction", "industry_specific"]):
                # Ensemble expects predictions from the three base models
                ensemble_features = pd.DataFrame({
                    'dna_probability': [predictions["dna_analyzer"]],
                    'temporal_probability': [predictions["temporal_prediction"]],
                    'industry_probability': [predictions["industry_specific"]]
                })
                ensemble_pred = self.models["ensemble_model"].predict_proba(ensemble_features)[:, 1]
                predictions["ensemble"] = float(ensemble_pred[0])
                # Add ensemble to the weighted score
                if "ensemble" in weights:
                    confidence_scores.append(ensemble_pred[0] * weights["ensemble"])
'''
        
        # Find the place to insert ensemble logic (after temporal prediction)
        temporal_end = content.find('confidence_scores.append(temporal_pred[0] * weights["temporal_prediction"])')
        if temporal_end > 0:
            # Find the next line break after this
            next_newline = content.find('\n', temporal_end)
            if next_newline > 0:
                # Insert the ensemble fix
                content_new = content[:next_newline+1] + ensemble_fix + content[next_newline+1:]
                
                # Also update the weights config to include ensemble
                weights_pattern = r'"weights": \{[^}]+\}'
                weights_replacement = '''"weights": {
                    "camp_evaluation": 0.40,
                    "pattern_analysis": 0.15,
                    "industry_specific": 0.15,
                    "temporal_prediction": 0.15,
                    "ensemble": 0.15
                }'''
                content_new = re.sub(weights_pattern, weights_replacement, content_new)
                
                orchestrator_path.write_text(content_new)
                logger.info("Added ensemble model integration")

def main():
    """Main function to fix all model issues"""
    logger.info("Starting model fix process...")
    
    # 1. Analyze current models
    logger.info("\n1. Analyzing current models...")
    analysis = analyze_models()
    
    # 2. Fix orchestrator preparation methods
    logger.info("\n2. Fixing orchestrator preparation methods...")
    fix_orchestrator_preparation()
    
    # 3. Fix ensemble model integration
    logger.info("\n3. Fixing ensemble model integration...")
    fix_ensemble_model()
    
    logger.info("\nModel fixes completed!")
    logger.info("\nSummary of changes:")
    logger.info("- Industry model: Now properly receives 45 canonical features")
    logger.info("- Temporal model: Now properly receives 46 features (45 + burn_efficiency)")
    logger.info("- Ensemble model: Now properly receives 3 probability features from base models")
    logger.info("- Pattern system: Kept disabled as configured")
    
    logger.info("\nPlease restart the API server to apply these changes.")

if __name__ == "__main__":
    main()