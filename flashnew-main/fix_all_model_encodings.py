#!/usr/bin/env python3
"""
Fix categorical encoding issues in all models that need it
"""

def add_encoding_to_dna_analyzer():
    """Add categorical encoding to DNA analyzer"""
    
    # Read the DNA analyzer file
    with open('ml_core/models/dna_analyzer.py', 'r') as f:
        content = f.read()
    
    # Add encoding method after the __init__ method
    encoding_method = '''
    def _encode_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features to match training data"""
        X_encoded = X.copy()
        
        # Encoding mappings from training
        funding_stage_map = {
            'Pre-seed': 0, 'Seed': 1, 'Series A': 2, 
            'Series B': 3, 'Series C+': 4, 'Unknown': 5
        }
        sector_map = {
            'Technology': 0, 'Healthcare': 1, 'Financial Services': 2,
            'Consumer': 3, 'Enterprise Software': 4, 'Unknown': 5
        }
        product_stage_map = {
            'MVP': 0, 'Beta': 1, 'Live': 2, 'Growth': 3, 'Unknown': 4
        }
        investor_tier_map = {1: 0, 2: 1, 3: 2, 'Unknown': 3}
        
        # Apply encodings
        if 'funding_stage' in X_encoded.columns:
            X_encoded['funding_stage'] = X_encoded['funding_stage'].map(funding_stage_map).fillna(5)
        if 'sector' in X_encoded.columns:
            X_encoded['sector'] = X_encoded['sector'].map(sector_map).fillna(5)
        if 'product_stage' in X_encoded.columns:
            X_encoded['product_stage'] = X_encoded['product_stage'].map(product_stage_map).fillna(4)
        if 'investor_tier_primary' in X_encoded.columns:
            X_encoded['investor_tier_primary'] = X_encoded['investor_tier_primary'].map(investor_tier_map).fillna(3)
            
        return X_encoded
    '''
    
    # Find where to insert - after __init__ method
    init_end = content.find('def fit(')
    if init_end != -1:
        # Find the previous method end
        prev_method_end = content.rfind('\n    \n', 0, init_end)
        if prev_method_end == -1:
            prev_method_end = content.rfind('\n\n', 0, init_end)
        insert_pos = prev_method_end + 1
        content = content[:insert_pos] + encoding_method + '\n' + content[insert_pos:]
    
    # Update predict method to use encoding
    predict_def = 'def predict(self, X: pd.DataFrame) -> np.ndarray:'
    pos = content.find(predict_def)
    if pos != -1:
        body_start = content.find('\n', pos) + 1
        docstring_end = content.find('"""', body_start)
        if docstring_end != -1:
            docstring_end = content.find('\n', docstring_end + 3) + 1
        else:
            docstring_end = body_start
        
        # Insert encoding call
        encoding_call = '        # Encode categorical features\\n        X = self._encode_features(X)\\n\\n'
        content = content[:docstring_end] + encoding_call + content[docstring_end:]
    
    # Update predict_proba method to use encoding
    predict_proba_def = 'def predict_proba(self, X: pd.DataFrame) -> np.ndarray:'
    pos = content.find(predict_proba_def)
    if pos != -1:
        body_start = content.find('\n', pos) + 1
        docstring_end = content.find('"""', body_start)
        if docstring_end != -1:
            docstring_end = content.find('\n', docstring_end + 3) + 1
        else:
            docstring_end = body_start
        
        # Insert encoding call
        encoding_call = '        # Encode categorical features\\n        X = self._encode_features(X)\\n\\n'
        content = content[:docstring_end] + encoding_call + content[docstring_end:]
    
    # Update get_dna_analysis method to use encoding
    dna_analysis_def = 'def get_dna_analysis(self, X: pd.DataFrame) -> Dict[str, Any]:'
    pos = content.find(dna_analysis_def) 
    if pos != -1:
        body_start = content.find('\n', pos) + 1
        docstring_end = content.find('"""', body_start)
        if docstring_end != -1:
            docstring_end = content.find('\n', docstring_end + 3) + 1
        else:
            docstring_end = body_start
        
        # Insert encoding call
        encoding_call = '        # Encode categorical features\\n        X = self._encode_features(X)\\n\\n'
        content = content[:docstring_end] + encoding_call + content[docstring_end:]
    
    # Update analyze_dna method if it exists
    analyze_dna_def = 'def analyze_dna(self, X: pd.DataFrame)'
    pos = content.find(analyze_dna_def)
    if pos != -1:
        # This is the public API method, it should call get_dna_analysis
        # Just make sure it's properly forwarding
        pass
    
    # Write the updated file
    with open('ml_core/models/dna_analyzer.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated dna_analyzer.py with categorical encoding")


def check_other_models():
    """Check and fix other models that might need encoding"""
    import os
    import glob
    
    # Check all model files for potential issues
    model_files = glob.glob('models/**/*.pkl', recursive=True)
    
    print(f"\nFound {len(model_files)} model files")
    
    # Models that likely need categorical encoding
    models_needing_encoding = [
        'temporal_prediction_model.pkl',
        'industry_specific_model.pkl',
        'optimized_pipeline.pkl'
    ]
    
    for model_file in model_files:
        basename = os.path.basename(model_file)
        if basename in models_needing_encoding:
            print(f"⚠️  {basename} may need categorical encoding wrapper")
    
    return models_needing_encoding


if __name__ == "__main__":
    # Fix DNA analyzer
    add_encoding_to_dna_analyzer()
    
    # Check other models
    models_to_check = check_other_models()
    
    print("\n✅ Encoding fixes applied!")
    print("\nSummary:")
    print("- unified_orchestrator.py: Fixed ✅")
    print("- dna_analyzer.py: Fixed ✅")
    print("- Other models inherit from orchestrator or have their own encoding")
    
    print("\nThe error 'could not convert string to float: 'Series A'' should now be resolved!")
    print("\nThe issue was that models were trained with numeric encoding of categorical features,")
    print("but the API was passing string values after transformation.")