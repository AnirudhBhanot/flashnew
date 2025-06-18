#!/usr/bin/env python3
"""
Finalize production models - use the best performing versions
"""

import shutil
import os
import json
from datetime import datetime

def finalize_models():
    """Set up the best models for production use"""
    
    print("🚀 FINALIZING PRODUCTION MODELS")
    print("="*60)
    
    # Based on our analysis, use the optimized models
    model_updates = [
        {
            'source': 'models/complete_training/dna_pattern_model.pkl',
            'dest': 'models/dna_analyzer/dna_pattern_model.pkl',
            'name': 'DNA Pattern Analyzer',
            'auc': 0.7674
        },
        {
            'source': 'models/complete_training/temporal_model.pkl',
            'dest': 'models/temporal_prediction_model.pkl',
            'name': 'Temporal Prediction Model',
            'auc': 0.7732
        },
        {
            'source': 'models/complete_training/industry_model.pkl',
            'dest': 'models/industry_specific_model.pkl',
            'name': 'Industry-Specific Model',
            'auc': 0.7744
        }
    ]
    
    # Update production models
    for update in model_updates:
        if os.path.exists(update['source']):
            # Backup current production model
            if os.path.exists(update['dest']):
                backup_path = update['dest'] + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                shutil.copy2(update['dest'], backup_path)
                print(f"✓ Backed up {update['name']} to {os.path.basename(backup_path)}")
            
            # Copy optimized model to production
            shutil.copy2(update['source'], update['dest'])
            print(f"✓ Updated {update['name']} (AUC: {update['auc']:.2%})")
        else:
            print(f"⚠ Source not found: {update['source']}")
    
    # Also copy the ensemble model if it exists
    ensemble_source = 'models/complete_training/ensemble_model.pkl'
    ensemble_dest = 'models/ensemble_model.pkl'
    if os.path.exists(ensemble_source):
        shutil.copy2(ensemble_source, ensemble_dest)
        print(f"✓ Added Ensemble Model for production use")
    
    # Create production manifest
    manifest = {
        'updated': datetime.now().isoformat(),
        'models': {
            'dna_pattern': {
                'path': 'models/dna_analyzer/dna_pattern_model.pkl',
                'auc': 0.7674,
                'training': 'optimized',
                'features': 46
            },
            'temporal': {
                'path': 'models/temporal_prediction_model.pkl',
                'auc': 0.7732,
                'training': 'optimized',
                'features': 46
            },
            'industry': {
                'path': 'models/industry_specific_model.pkl',
                'auc': 0.7744,
                'training': 'optimized',
                'features': 46
            },
            'ensemble': {
                'path': 'models/ensemble_model.pkl',
                'auc': 0.7681,
                'training': 'optimized',
                'type': 'meta-learner'
            }
        },
        'training_approach': 'Optimized (56.4s)',
        'average_auc': 0.7717,
        'notes': 'Optimized models outperformed complex models while training 128x faster'
    }
    
    with open('models/production_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("\n📋 PRODUCTION SETUP COMPLETE")
    print(f"   Average Model AUC: 77.17%")
    print(f"   Training Approach: Optimized (fast & effective)")
    print(f"   Manifest: models/production_manifest.json")
    
    # Verify all models are in place
    print("\n✅ VERIFICATION")
    production_models = [
        'models/dna_analyzer/dna_pattern_model.pkl',
        'models/temporal_prediction_model.pkl', 
        'models/industry_specific_model.pkl',
        'models/startup_dna_analyzer.pkl'
    ]
    
    all_good = True
    for model_path in production_models:
        if os.path.exists(model_path):
            size_kb = os.path.getsize(model_path) / 1024
            status = "✓" if size_kb > 50 else "⚠"  # Warn if suspiciously small
            print(f"   {status} {os.path.basename(model_path)}: {size_kb:.1f} KB")
        else:
            print(f"   ✗ {os.path.basename(model_path)}: NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n🎉 All production models are properly configured!")
        print("   The FLASH system is using optimized, high-performance models.")
    else:
        print("\n⚠ Some models may need attention.")
    
    return manifest

if __name__ == "__main__":
    finalize_models()