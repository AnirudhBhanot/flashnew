#!/usr/bin/env python3
"""Diagnose why advanced models fail to load"""
import joblib
import pickle
import sys
from pathlib import Path

def check_model_internals(model_path):
    """Check what's inside a pickled model"""
    print(f"\nChecking {model_path}...")
    
    try:
        # Try loading with joblib
        with open(model_path, 'rb') as f:
            # Read pickle header to see what classes it references
            data = f.read()
            
        # Look for class names in the pickle
        class_refs = []
        for line in str(data).split('\\x'):
            if 'DNAPatternAnalyzer' in line or 'OptimizedDNAPatternAnalyzer' in line:
                class_refs.append(line)
                
        if class_refs:
            print("Found class references:")
            for ref in class_refs[:3]:  # Show first 3
                print(f"  {ref[:100]}...")
                
        # Try to load and see the error
        try:
            model = joblib.load(model_path)
            print(f"✅ Successfully loaded! Type: {type(model)}")
        except Exception as e:
            print(f"❌ Load error: {e}")
            
    except Exception as e:
        print(f"Error reading file: {e}")

def test_import_fix():
    """Test if importing the module helps"""
    print("\nTesting with module imports...")
    
    # Import the modules that define the classes
    try:
        # First, add the modules to the namespace
        from dna_pattern_analysis import StartupDNAAnalyzer
        from temporal_models import TemporalPredictionModel
        from industry_specific_models import IndustrySpecificModel
        
        # Also try importing from train scripts that might have created them
        sys.path.insert(0, '/Users/sf/Desktop/FLASH')
        
        # Now try loading
        models_to_test = [
            ('models/startup_dna_analyzer.pkl', 'DNA Analyzer'),
            ('models/temporal_prediction_model.pkl', 'Temporal Model'),
            ('models/industry_specific_model.pkl', 'Industry Model')
        ]
        
        for model_path, name in models_to_test:
            try:
                model = joblib.load(model_path)
                print(f"✅ {name} loaded successfully after imports!")
            except Exception as e:
                print(f"❌ {name} still fails: {e}")
                
    except ImportError as e:
        print(f"Import error: {e}")

def check_hierarchical_models():
    """Check the hierarchical models in the subdirectory"""
    print("\nChecking hierarchical models...")
    
    hierarchical_path = Path('models/hierarchical_45features')
    if hierarchical_path.exists():
        for model_file in hierarchical_path.glob('*.pkl'):
            print(f"\n{model_file.name}:")
            try:
                model = joblib.load(model_file)
                print(f"  ✅ Loaded successfully, type: {type(model)}")
            except Exception as e:
                print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    print("=== Model Loading Diagnostics ===")
    
    # Check the problematic models
    check_model_internals('models/dna_analyzer/dna_pattern_model.pkl')
    check_model_internals('models/temporal_prediction_model.pkl')
    check_model_internals('models/industry_specific_model.pkl')
    
    # Test with imports
    test_import_fix()
    
    # Check hierarchical models
    check_hierarchical_models()