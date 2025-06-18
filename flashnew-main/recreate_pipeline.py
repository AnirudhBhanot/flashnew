#!/usr/bin/env python3
"""
Recreate the data pipeline with proper imports
"""

import pandas as pd
from pathlib import Path
import joblib
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import from proper module
from models.data_pipeline import UnifiedDataPipeline


def recreate_pipeline():
    """Recreate pipeline with proper module import"""
    logger.info("Recreating unified data pipeline...")
    
    # Load training data
    data_path = Path("data/final_100k_dataset_45features.csv")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples")
    
    # Create and fit pipeline
    pipeline = UnifiedDataPipeline()
    pipeline.fit(df)
    
    # Save pipeline
    output_path = Path("models/unified_v45/data_pipeline.pkl")
    joblib.dump(pipeline, output_path)
    logger.info(f"Saved pipeline to {output_path}")
    
    # Test it loads correctly
    loaded_pipeline = joblib.load(output_path)
    logger.info("✓ Pipeline loads correctly!")
    
    # Update metadata
    metadata_path = output_path.parent / "pipeline_metadata.json"
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    metadata['module'] = 'models.data_pipeline'
    metadata['class'] = 'UnifiedDataPipeline'
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info("✓ Pipeline recreated successfully!")
    return loaded_pipeline


if __name__ == "__main__":
    recreate_pipeline()