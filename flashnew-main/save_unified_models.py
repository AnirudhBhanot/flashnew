#!/usr/bin/env python3
"""
Save the already trained models without the problematic ensemble
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# Create manifest for the successfully trained models
manifest = {
    'version': 'unified_v45',
    'created_at': datetime.now().isoformat(),
    'models': {
        'dna_analyzer': {
            'path': 'models/unified_v45/dna_analyzer.pkl',
            'auc': 0.7749,
            'n_features': 45
        },
        'temporal_model': {
            'path': 'models/unified_v45/temporal_model.pkl', 
            'auc': 0.7707,
            'n_features': 45
        },
        'industry_model': {
            'path': 'models/unified_v45/industry_model.pkl',
            'auc': 0.7739,
            'n_features': 45
        }
    },
    'pipeline_path': 'models/unified_v45/data_pipeline.pkl',
    'average_auc': 0.7732,
    'training_time_seconds': 29.2,
    'dataset': 'data/final_100k_dataset_45features.csv',
    'notes': 'All models trained on canonical 45 features - no wrappers needed!'
}

# Save manifest
manifest_path = Path("models/unified_manifest.json")
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

print("Manifest created successfully!")
print(f"Average AUC: {manifest['average_auc']:.4f}")
print("All models trained on unified 45 features!")

# Update production symlinks
production_dir = Path("models/production_unified")
production_dir.mkdir(exist_ok=True)

# Create symlinks to unified models
for model_name in ['dna_analyzer', 'temporal_model', 'industry_model']:
    source = Path(f"../unified_v45/{model_name}.pkl")
    target = production_dir / f"{model_name}.pkl"
    if target.exists():
        target.unlink()
    try:
        target.symlink_to(source)
        print(f"Created symlink for {model_name}")
    except:
        # On Windows or if symlinks fail, copy instead
        shutil.copy2(f"models/unified_v45/{model_name}.pkl", target)
        print(f"Copied {model_name}")

# Copy pipeline
pipeline_source = Path("models/unified_v45/data_pipeline.pkl")
pipeline_target = production_dir / "data_pipeline.pkl"
if pipeline_target.exists():
    pipeline_target.unlink()
shutil.copy2(pipeline_source, pipeline_target)
print("Copied data pipeline")

print("\nModels ready for production use!")
print("No wrappers needed - all models use 45 features directly!")