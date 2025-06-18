#!/usr/bin/env python3
"""
Comprehensive fix for FLASH model issues
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_orchestrator_comprehensive():
    """Apply comprehensive fixes to the orchestrator"""
    
    orchestrator_path = Path("models/unified_orchestrator_v3_integrated.py")
    if not orchestrator_path.exists():
        logger.error("Orchestrator file not found!")
        return
    
    # Read the current content
    content = orchestrator_path.read_text()
    
    # Find and update the _prepare_features method to handle categorical encoding
    new_prepare_features = '''    def _prepare_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for model input with proper encoding"""
        # Ensure all required features are present
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        
        # Import necessary configs
        from feature_config import ALL_FEATURES, CATEGORICAL_FEATURES, BOOLEAN_FEATURES
        
        # Create a properly ordered dataframe with all features
        prepared = pd.DataFrame(index=features.index)
        
        # Process each feature in the correct order
        for col in ALL_FEATURES:
            if col in features.columns:
                prepared[col] = features[col].values
            else:
                # Use appropriate defaults
                if col in BOOLEAN_FEATURES or col in ['has_debt', 'network_effects_present', 
                                                       'has_data_moat', 'regulatory_advantage_present', 
                                                       'key_person_dependency']:
                    prepared[col] = False
                elif col in CATEGORICAL_FEATURES:
                    # Default categorical values
                    if col == 'funding_stage':
                        prepared[col] = 'Seed'
                    elif col == 'investor_tier_primary':
                        prepared[col] = 'Tier_3'
                    elif col == 'product_stage':
                        prepared[col] = 'MVP'
                    elif col == 'sector':
                        prepared[col] = 'SaaS'
                    else:
                        prepared[col] = 'Unknown'
                elif col.endswith('_percent') or col.endswith('_score'):
                    prepared[col] = 0.0
                else:
                    prepared[col] = 0
        
        # Handle categorical encoding
        if hasattr(self, 'encoders') and self.encoders:
            for col in CATEGORICAL_FEATURES:
                if col in prepared.columns and col in self.encoders:
                    try:
                        # Ensure string type for encoding
                        prepared[col] = prepared[col].astype(str)
                        # Handle unknown categories
                        known_categories = set(self.encoders[col].classes_)
                        prepared[col] = prepared[col].apply(
                            lambda x: x if x in known_categories else self.encoders[col].classes_[0]
                        )
                        prepared[col] = self.encoders[col].transform(prepared[col])
                    except Exception as e:
                        logger.warning(f"Error encoding {col}: {e}")
                        prepared[col] = 0
        else:
            # Manual encoding if no encoders available
            encoding_maps = {
                'funding_stage': {'Pre_Seed': 0, 'Seed': 1, 'Series_A': 2, 'Series_B': 3, 
                                 'Series_C': 4, 'Series_D': 5, 'Series_E': 6, 'Series_F': 7},
                'investor_tier_primary': {'Tier_1': 2, 'Tier_2': 1, 'Tier_3': 0},
                'product_stage': {'Concept': 0, 'MVP': 1, 'Beta': 2, 'Live': 3, 'Growth': 4},
                'sector': {'SaaS': 0, 'Fintech': 1, 'Healthcare': 2, 'E-commerce': 3, 
                          'AI/ML': 4, 'Biotech': 5, 'EdTech': 6, 'Other': 7}
            }
            
            for col in CATEGORICAL_FEATURES:
                if col in prepared.columns and col in encoding_maps:
                    prepared[col] = prepared[col].map(encoding_maps[col]).fillna(0).astype(int)
        
        # Convert boolean columns
        for col in BOOLEAN_FEATURES:
            if col in prepared.columns:
                prepared[col] = prepared[col].astype(bool).astype(int)
        
        # Convert numeric columns
        numeric_cols = [col for col in prepared.columns if col not in CATEGORICAL_FEATURES]
        for col in numeric_cols:
            try:
                prepared[col] = pd.to_numeric(prepared[col], errors='coerce').fillna(0)
            except:
                prepared[col] = 0
        
        return prepared'''
    
    # Replace the _prepare_features method
    import re
    pattern = r'def _prepare_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return features'
    content = re.sub(pattern, new_prepare_features, content, flags=re.DOTALL)
    
    # Update _prepare_dna_features to use feature order
    new_dna_features = '''    def _prepare_dna_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for DNA analyzer which expects 45 features in specific order"""
        # Load feature order if available
        feature_order_path = Path("models/production_v45_fixed/dna_feature_order.pkl")
        if feature_order_path.exists():
            try:
                feature_order = joblib.load(feature_order_path)
                # Reorder columns to match training
                ordered_features = pd.DataFrame()
                for col in feature_order:
                    if col in features.columns:
                        ordered_features[col] = features[col]
                    else:
                        # Use defaults based on feature type
                        if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                                  'regulatory_advantage_present', 'key_person_dependency']:
                            ordered_features[col] = 0
                        elif col.endswith('_percent') or col.endswith('_score'):
                            ordered_features[col] = 0.0
                        else:
                            ordered_features[col] = 0
                return ordered_features
            except Exception as e:
                logger.warning(f"Could not load DNA feature order: {e}")
        
        return features'''
    
    # Replace _prepare_dna_features
    pattern = r'def _prepare_dna_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return features'
    content = re.sub(pattern, new_dna_features, content, flags=re.DOTALL)
    
    # Update _prepare_industry_features to use feature order
    new_industry_features = '''    def _prepare_industry_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for industry model - expects 45 base features in specific order"""
        # Load feature order if available
        feature_order_path = Path("models/production_v45_fixed/industry_feature_order.pkl")
        if feature_order_path.exists():
            try:
                feature_order = joblib.load(feature_order_path)
                # Reorder columns to match training
                ordered_features = pd.DataFrame()
                for col in feature_order:
                    if col in features.columns:
                        ordered_features[col] = features[col]
                    else:
                        # Use defaults based on feature type
                        if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                                  'regulatory_advantage_present', 'key_person_dependency']:
                            ordered_features[col] = 0
                        elif col.endswith('_percent') or col.endswith('_score'):
                            ordered_features[col] = 0.0
                        else:
                            ordered_features[col] = 0
                return ordered_features
            except Exception as e:
                logger.warning(f"Could not load industry feature order: {e}")
        
        # Fallback to ALL_FEATURES order
        from feature_config import ALL_FEATURES
        ordered_features = pd.DataFrame()
        for col in ALL_FEATURES:
            if col in features.columns:
                ordered_features[col] = features[col]
            else:
                if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency']:
                    ordered_features[col] = 0
                elif col.endswith('_percent') or col.endswith('_score'):
                    ordered_features[col] = 0.0
                else:
                    ordered_features[col] = 0
        
        return ordered_features'''
    
    # Find and replace _prepare_industry_features
    pattern = r'def _prepare_industry_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return prepared'
    content = re.sub(pattern, new_industry_features, content, flags=re.DOTALL)
    
    # Update _prepare_temporal_features to use feature order
    new_temporal_features = '''    def _prepare_temporal_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for temporal model - expects 46 features in specific order"""
        # Load feature order if available
        feature_order_path = Path("models/production_v45_fixed/temporal_feature_order.pkl")
        if feature_order_path.exists():
            try:
                feature_order = joblib.load(feature_order_path)
                # Reorder columns to match training
                ordered_features = pd.DataFrame()
                for col in feature_order:
                    if col in features.columns:
                        ordered_features[col] = features[col]
                    elif col == 'burn_efficiency':
                        # Calculate burn efficiency
                        if 'annual_revenue_run_rate' in features.columns and 'monthly_burn_usd' in features.columns:
                            revenue = features['annual_revenue_run_rate'].fillna(0)
                            burn = features['monthly_burn_usd'].fillna(1)
                            ordered_features[col] = (revenue / 12) / burn.replace(0, 1)
                        else:
                            ordered_features[col] = 0.5
                    else:
                        # Use defaults based on feature type
                        if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                                  'regulatory_advantage_present', 'key_person_dependency']:
                            ordered_features[col] = 0
                        elif col.endswith('_percent') or col.endswith('_score'):
                            ordered_features[col] = 0.0
                        else:
                            ordered_features[col] = 0
                return ordered_features
            except Exception as e:
                logger.warning(f"Could not load temporal feature order: {e}")
        
        # Fallback - use base features + burn_efficiency
        from feature_config import ALL_FEATURES
        ordered_features = pd.DataFrame()
        for col in ALL_FEATURES:
            if col in features.columns:
                ordered_features[col] = features[col]
            else:
                if col in ['has_debt', 'network_effects_present', 'has_data_moat', 
                          'regulatory_advantage_present', 'key_person_dependency']:
                    ordered_features[col] = 0
                elif col.endswith('_percent') or col.endswith('_score'):
                    ordered_features[col] = 0.0
                else:
                    ordered_features[col] = 0
        
        # Add burn_efficiency as the 46th feature
        if 'annual_revenue_run_rate' in features.columns and 'monthly_burn_usd' in features.columns:
            revenue = features['annual_revenue_run_rate'].fillna(0)
            burn = features['monthly_burn_usd'].fillna(1)
            ordered_features['burn_efficiency'] = (revenue / 12) / burn.replace(0, 1)
        else:
            ordered_features['burn_efficiency'] = 0.5
        
        return ordered_features'''
    
    # Replace _prepare_temporal_features
    pattern = r'def _prepare_temporal_features\(self, features: pd\.DataFrame\) -> pd\.DataFrame:.*?return temporal_features'
    content = re.sub(pattern, new_temporal_features, content, flags=re.DOTALL)
    
    # Add necessary imports at the top if not already present
    if 'from pathlib import Path' not in content:
        # Find the imports section
        import_end = content.find('logger = logging.getLogger(__name__)')
        if import_end > 0:
            content = content[:import_end] + 'from pathlib import Path\n' + content[import_end:]
    
    # Write the updated content
    orchestrator_path.write_text(content)
    logger.info("Applied comprehensive fixes to orchestrator")

def main():
    """Apply all fixes"""
    logger.info("Applying comprehensive model fixes...")
    
    # Apply the fixes
    fix_orchestrator_comprehensive()
    
    logger.info("\nFixes applied successfully!")
    logger.info("\nKey changes:")
    logger.info("1. Added proper categorical encoding with fallbacks")
    logger.info("2. Updated all model preparation methods to use feature order files")
    logger.info("3. Added proper default values for missing features")
    logger.info("4. Fixed feature ordering to match model training")
    logger.info("\nPlease test the models again to verify the fixes work.")

if __name__ == "__main__":
    main()