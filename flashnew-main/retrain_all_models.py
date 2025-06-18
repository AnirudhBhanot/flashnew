#!/usr/bin/env python3
"""
Script to retrain all models on full 100k dataset and create missing models
"""
import subprocess
import logging
import time
from pathlib import Path
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('model_retraining.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_training_script(script_name, description):
    """Run a training script and log the output"""
    logger.info(f"Starting: {description}")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        duration = time.time() - start_time
        logger.info(f"Completed {description} in {duration:.1f} seconds")
        logger.info(f"Output: {result.stdout[-500:]}")  # Last 500 chars of output
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed {description}: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def main():
    """Main function to retrain all models"""
    logger.info("=" * 80)
    logger.info("Starting complete model retraining on 100k dataset")
    logger.info("=" * 80)
    
    # Track progress
    tasks = [
        ("train_hierarchical_models_45features.py", "Hierarchical Models (Stage, Temporal, Industry, DNA)"),
        ("train_flash_v2_ensemble.py", "V2 Ensemble Models (if needed)"),
    ]
    
    completed = 0
    failed = 0
    
    for script, description in tasks:
        if Path(script).exists():
            if run_training_script(script, description):
                completed += 1
            else:
                failed += 1
        else:
            logger.warning(f"Script not found: {script}")
            failed += 1
    
    # Create missing advanced models
    logger.info("\nCreating missing advanced models...")
    create_missing_models()
    
    # Summary
    logger.info("=" * 80)
    logger.info(f"Training Summary: {completed} completed, {failed} failed")
    logger.info("Check model_retraining.log for details")
    logger.info("=" * 80)

def create_missing_models():
    """Create the missing advanced models that the orchestrator expects"""
    from pathlib import Path
    import joblib
    import shutil
    
    logger.info("Checking for missing models...")
    
    # Map of expected models to their likely sources
    model_mapping = {
        'models/startup_dna_analyzer.pkl': 'models/hierarchical_45features/dna_pattern_model.pkl',
        'models/temporal_prediction_model.pkl': 'models/hierarchical_45features/temporal_hierarchical_model.pkl',
        'models/industry_specific_model.pkl': 'models/hierarchical_45features/industry_specific_model.pkl',
        'models/optimized_pipeline.pkl': None,  # Will need to create separately
        'models/production_ensemble.pkl': 'models/hierarchical_45features/hierarchical_meta_ensemble.pkl'
    }
    
    for target, source in model_mapping.items():
        target_path = Path(target)
        
        if not target_path.exists():
            if source and Path(source).exists():
                logger.info(f"Copying {source} to {target}")
                shutil.copy2(source, target)
            else:
                logger.warning(f"Cannot create {target} - source not found")
        else:
            logger.info(f"Model already exists: {target}")
    
    # Create stage hierarchical directory if needed
    stage_dir = Path('models/stage_hierarchical')
    if not stage_dir.exists():
        stage_dir.mkdir(parents=True)
        logger.info(f"Created directory: {stage_dir}")
        
        # Copy stage models if they exist
        hierarchical_dir = Path('models/hierarchical_45features')
        if hierarchical_dir.exists():
            for file in ['stage_hierarchical_model.pkl']:
                source_file = hierarchical_dir / file
                if source_file.exists():
                    shutil.copy2(source_file, stage_dir / file)
                    logger.info(f"Copied {file} to stage_hierarchical directory")

if __name__ == "__main__":
    main()