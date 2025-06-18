#!/usr/bin/env python3
"""
Setup script to initialize model integrity system
Generates checksums for all existing models
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.model_integrity import ModelIntegritySystem

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Initialize model integrity system and register all models"""
    
    logger.info("Initializing Model Integrity System...")
    
    # Create integrity system
    integrity_system = ModelIntegritySystem()
    
    # Define model directories to scan
    model_dirs = [
        "models/production_v45_fixed",
        "models/complete_hybrid",
        "models/pattern_success_models",
        "models/backup",
        "models"
    ]
    
    # Register all models
    all_results = {
        "registered": [],
        "failed": [],
        "skipped": []
    }
    
    for model_dir in model_dirs:
        dir_path = Path(model_dir)
        if dir_path.exists():
            logger.info(f"Scanning directory: {model_dir}")
            
            # Register models in this directory
            for model_file in dir_path.glob("*.pkl"):
                if model_file.is_file():
                    try:
                        result = integrity_system.register_model(model_file)
                        all_results["registered"].append(str(model_file))
                        logger.info(f"✓ Registered: {model_file.name}")
                    except Exception as e:
                        all_results["failed"].append({
                            "file": str(model_file),
                            "error": str(e)
                        })
                        logger.error(f"✗ Failed: {model_file.name} - {e}")
            
            # Also scan for .joblib files
            for model_file in dir_path.glob("*.joblib"):
                if model_file.is_file():
                    try:
                        result = integrity_system.register_model(model_file)
                        all_results["registered"].append(str(model_file))
                        logger.info(f"✓ Registered: {model_file.name}")
                    except Exception as e:
                        all_results["failed"].append({
                            "file": str(model_file),
                            "error": str(e)
                        })
                        logger.error(f"✗ Failed: {model_file.name} - {e}")
    
    # Generate integrity report
    logger.info("\nGenerating integrity report...")
    report = integrity_system.generate_integrity_report()
    
    # Save report
    report_path = Path("models/integrity_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("MODEL INTEGRITY SYSTEM SETUP COMPLETE")
    print("="*60)
    print(f"Total models registered: {len(all_results['registered'])}")
    print(f"Failed registrations: {len(all_results['failed'])}")
    print(f"System status: {report['system_status']}")
    print(f"Integrity report saved to: {report_path}")
    
    if all_results['failed']:
        print("\nFailed registrations:")
        for failure in all_results['failed']:
            print(f"  - {failure['file']}: {failure['error']}")
    
    # Create signature for critical models
    critical_models = [
        "models/production_v45_fixed/dna_analyzer_model.pkl",
        "models/production_v45_fixed/temporal_model.pkl",
        "models/production_v45_fixed/industry_model.pkl",
        "models/production_v45_fixed/ensemble_model.pkl"
    ]
    
    print("\nCreating signatures for critical models...")
    for model_path_str in critical_models:
        model_path = Path(model_path_str)
        if model_path.exists():
            try:
                signature = integrity_system.create_model_signature(model_path)
                print(f"  ✓ Signed: {model_path.name}")
            except Exception as e:
                print(f"  ✗ Failed to sign {model_path.name}: {e}")
    
    print("\nModel integrity system is now active!")
    print("All future model loads will be verified for integrity.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())