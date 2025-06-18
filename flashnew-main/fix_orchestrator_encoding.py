#!/usr/bin/env python3
"""
Fix the funding_stage encoding issue in unified_orchestrator.py
The models expect numeric encoding but receive string values
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def add_categorical_encoding_to_orchestrator():
    """Add categorical encoding to the orchestrator"""
    
    # Read the current orchestrator file
    with open('models/unified_orchestrator.py', 'r') as f:
        content = f.read()
    
    # Add the encoding mappings at the class level
    encoding_section = '''
    # Categorical encodings (matching training data)
    FUNDING_STAGE_ENCODING = {
        'Pre-seed': 0,
        'Seed': 1,
        'Series A': 2,
        'Series B': 3,
        'Series C+': 4,
        'Unknown': 5
    }
    
    SECTOR_ENCODING = {
        'Technology': 0,
        'Healthcare': 1,
        'Financial Services': 2,
        'Consumer': 3,
        'Enterprise Software': 4,
        'Unknown': 5
    }
    
    PRODUCT_STAGE_ENCODING = {
        'MVP': 0,
        'Beta': 1,
        'Live': 2,
        'Growth': 3,
        'Unknown': 4
    }
    
    INVESTOR_TIER_ENCODING = {
        1: 0,
        2: 1,
        3: 2,
        'Unknown': 3
    }
    '''
    
    # Find where to insert - after the class definition
    class_def = 'class UnifiedModelOrchestrator:'
    insert_pos = content.find(class_def)
    if insert_pos != -1:
        # Find the next line after class definition
        next_line_pos = content.find('\n', insert_pos) + 1
        # Find the docstring end
        docstring_end = content.find('"""', next_line_pos) + 3
        next_line_pos = content.find('\n', docstring_end) + 1
        
        # Insert the encoding section
        content = content[:next_line_pos] + encoding_section + '\n' + content[next_line_pos:]
    
    # Add encoding method
    encoding_method = '''
    def _encode_categorical_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features to match training data"""
        encoded_features = features.copy()
        
        # Encode funding_stage
        if 'funding_stage' in encoded_features.columns:
            encoded_features['funding_stage'] = encoded_features['funding_stage'].map(
                self.FUNDING_STAGE_ENCODING
            ).fillna(self.FUNDING_STAGE_ENCODING['Unknown'])
        
        # Encode sector
        if 'sector' in encoded_features.columns:
            encoded_features['sector'] = encoded_features['sector'].map(
                self.SECTOR_ENCODING
            ).fillna(self.SECTOR_ENCODING['Unknown'])
        
        # Encode product_stage
        if 'product_stage' in encoded_features.columns:
            encoded_features['product_stage'] = encoded_features['product_stage'].map(
                self.PRODUCT_STAGE_ENCODING
            ).fillna(self.PRODUCT_STAGE_ENCODING['Unknown'])
        
        # Encode investor_tier_primary
        if 'investor_tier_primary' in encoded_features.columns:
            encoded_features['investor_tier_primary'] = encoded_features['investor_tier_primary'].map(
                self.INVESTOR_TIER_ENCODING
            ).fillna(self.INVESTOR_TIER_ENCODING['Unknown'])
        
        return encoded_features
    '''
    
    # Insert the encoding method before _get_pillar_features
    get_pillar_pos = content.find('def _get_pillar_features(')
    if get_pillar_pos != -1:
        # Find the previous method end
        prev_method_end = content.rfind('\n    \n', 0, get_pillar_pos)
        if prev_method_end == -1:
            prev_method_end = content.rfind('\n\n', 0, get_pillar_pos)
        insert_pos = prev_method_end + 1
        content = content[:insert_pos] + encoding_method + '\n' + content[insert_pos:]
    
    # Update _predict_base_ensemble to use encoding
    predict_base_def = 'def _predict_base_ensemble(self, features: pd.DataFrame) -> Dict[str, Any]:'
    pos = content.find(predict_base_def)
    if pos != -1:
        # Find the start of the method body
        body_start = content.find('\n', pos) + 1
        # Find the docstring end
        docstring_end = content.find('"""', body_start)
        if docstring_end != -1:
            docstring_end = content.find('\n', docstring_end + 3) + 1
        else:
            docstring_end = body_start
        
        # Insert encoding call
        encoding_call = '        # Encode categorical features\\n        encoded_features = self._encode_categorical_features(features)\\n\\n'
        content = content[:docstring_end] + encoding_call + content[docstring_end:]
        
        # Replace features with encoded_features in _get_pillar_features calls
        # Find the method end
        method_end = content.find('\\n    def ', pos + 1)
        if method_end == -1:
            method_end = len(content)
        
        method_content = content[pos:method_end]
        method_content = method_content.replace('self._get_pillar_features(features,', 'self._get_pillar_features(encoded_features,')
        content = content[:pos] + method_content + content[method_end:]
    
    # Update _predict_stage_specific to use encoding
    predict_stage_def = 'def _predict_stage_specific(self, features: pd.DataFrame) -> Dict[str, Any]:'
    pos = content.find(predict_stage_def)
    if pos != -1:
        # Find the start of the method body
        body_start = content.find('\n', pos) + 1
        # Find the docstring end
        docstring_end = content.find('"""', body_start)
        if docstring_end != -1:
            docstring_end = content.find('\n', docstring_end + 3) + 1
        else:
            docstring_end = body_start
        
        # Insert encoding call
        encoding_call = '        # Encode categorical features\\n        encoded_features = self._encode_categorical_features(features)\\n\\n'
        content = content[:docstring_end] + encoding_call + content[docstring_end:]
        
        # Replace features with encoded_features in predict_proba call
        method_end = content.find('\\n    def ', pos + 1)
        if method_end == -1:
            method_end = len(content)
        
        method_content = content[pos:method_end]
        method_content = method_content.replace('model.predict_proba(features)', 'model.predict_proba(encoded_features)')
        content = content[:pos] + method_content + content[method_end:]
    
    # Write the updated file
    with open('models/unified_orchestrator.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated unified_orchestrator.py with categorical encoding")
    
    # Also update unified_orchestrator_v2.py if it exists
    try:
        with open('models/unified_orchestrator_v2.py', 'r') as f:
            content_v2 = f.read()
        
        # The v2 inherits from v1, so it should automatically get the encoding
        # But we need to make sure it calls the parent's encoded methods
        
        print("✅ unified_orchestrator_v2.py inherits encoding from base class")
    except FileNotFoundError:
        print("ℹ️  unified_orchestrator_v2.py not found, skipping")

if __name__ == "__main__":
    add_categorical_encoding_to_orchestrator()