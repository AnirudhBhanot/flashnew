#!/usr/bin/env python3
"""
Update model paths to use real trained models instead of placeholders
"""

import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_model_paths():
    """Replace placeholder models with real trained models"""
    
    # Model mappings from hierarchical_45features to main models directory
    model_mappings = [
        ('models/hierarchical_45features/dna_pattern_model.pkl', 
         'models/dna_analyzer/dna_pattern_model.pkl'),
        
        ('models/hierarchical_45features/temporal_hierarchical_model.pkl', 
         'models/temporal_prediction_model.pkl'),
        
        ('models/hierarchical_45features/industry_specific_model.pkl', 
         'models/industry_specific_model.pkl'),
    ]
    
    # Backup old placeholder models
    logger.info("Backing up placeholder models...")
    for _, dest in model_mappings:
        if os.path.exists(dest):
            backup_path = dest + '.placeholder_backup'
            shutil.copy2(dest, backup_path)
            logger.info(f"Backed up {dest} to {backup_path}")
    
    # Copy real models to replace placeholders
    logger.info("\nReplacing placeholder models with real trained models...")
    for src, dest in model_mappings:
        if os.path.exists(src):
            shutil.copy2(src, dest)
            logger.info(f"Copied {src} to {dest}")
            
            # Check file sizes to confirm
            src_size = os.path.getsize(src)
            dest_size = os.path.getsize(dest)
            logger.info(f"  Source size: {src_size:,} bytes")
            logger.info(f"  Destination size: {dest_size:,} bytes")
        else:
            logger.warning(f"Source file not found: {src}")
    
    # Also update the startup_dna_analyzer if needed
    if os.path.exists('models/hierarchical_45features/dna_pattern_model.pkl'):
        if os.path.exists('models/startup_dna_analyzer.pkl'):
            # Check if it's already a real model (not 29625 bytes)
            size = os.path.getsize('models/startup_dna_analyzer.pkl')
            if size == 29625:
                logger.info("\nReplacing startup_dna_analyzer placeholder...")
                shutil.copy2('models/startup_dna_analyzer.pkl', 
                           'models/startup_dna_analyzer.pkl.placeholder_backup')
                shutil.copy2('models/hierarchical_45features/dna_pattern_model.pkl',
                           'models/startup_dna_analyzer.pkl')
                logger.info("Replaced startup_dna_analyzer.pkl with real model")
    
    logger.info("\nModel update complete!")
    
    # Verify the updates
    logger.info("\nVerifying model files:")
    all_models = [
        'models/dna_analyzer/dna_pattern_model.pkl',
        'models/temporal_prediction_model.pkl',
        'models/industry_specific_model.pkl',
        'models/startup_dna_analyzer.pkl'
    ]
    
    for model_path in all_models:
        if os.path.exists(model_path):
            size = os.path.getsize(model_path)
            logger.info(f"{model_path}: {size:,} bytes")
            if size == 29625:
                logger.warning(f"  WARNING: This appears to still be a placeholder!")
        else:
            logger.error(f"{model_path}: NOT FOUND")

if __name__ == "__main__":
    update_model_paths()