#!/usr/bin/env python3
"""
Fix funding_stage mapping in API server
"""

def add_funding_stage_transform():
    """Add funding stage transformation to api_server.py and api_server_v2.py"""
    
    # The transformation code to add
    transform_code = '''
        # Transform funding_stage from API format to feature engineering format
        stage_transform_map = {
            'pre_seed': 'Pre-seed',
            'seed': 'Seed', 
            'series_a': 'Series A',
            'series_b': 'Series B',
            'series_c': 'Series C',
            'growth': 'Series C+'
        }
        if 'funding_stage' in data.columns:
            data['funding_stage'] = data['funding_stage'].map(stage_transform_map).fillna(data['funding_stage'])
'''
    
    # Files to update
    files_to_update = ['api_server.py', 'api_server_v2.py']
    
    for filename in files_to_update:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Find where to insert the transformation
            # It should be right after converting to DataFrame and before create_engineered_features
            
            # For api_server.py
            if filename == 'api_server.py':
                search_pattern = '        # Convert to DataFrame\n        data = pd.DataFrame([metrics.dict()])\n        \n        # Create engineered features'
                replacement = f'        # Convert to DataFrame\n        data = pd.DataFrame([metrics.dict()])\n        {transform_code}\n        # Create engineered features'
                
                if search_pattern in content:
                    content = content.replace(search_pattern, replacement)
                    with open(filename, 'w') as f:
                        f.write(content)
                    print(f"✅ Updated {filename} with funding_stage transformation")
                else:
                    print(f"⚠️  Could not find the exact pattern in {filename}")
                    print("   Looking for alternative pattern...")
                    
                    # Alternative pattern for the orchestrator path
                    alt_pattern = '                # Convert to DataFrame\n                data = pd.DataFrame([metrics.dict()])\n                \n                # Get unified prediction'
                    alt_replacement = f'                # Convert to DataFrame\n                data = pd.DataFrame([metrics.dict()])\n                {transform_code}\n                # Get unified prediction'
                    
                    if alt_pattern in content:
                        content = content.replace(alt_pattern, alt_replacement)
                        with open(filename, 'w') as f:
                            f.write(content)
                        print(f"✅ Updated {filename} orchestrator path with funding_stage transformation")
            
            # For api_server_v2.py
            elif filename == 'api_server_v2.py':
                # Need to check if this file uses the same pattern
                if 'pd.DataFrame([metrics.dict()])' in content and 'create_engineered_features' not in content:
                    # api_server_v2 might rely on the orchestrator to handle this
                    print(f"ℹ️  {filename} delegates to orchestrator for feature engineering")
        
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")

if __name__ == "__main__":
    add_funding_stage_transform()