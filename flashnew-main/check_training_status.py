#!/usr/bin/env python3
"""
Monitor and report on model training status
"""
import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

def check_training_status():
    """Check the status of model training"""
    
    print("=" * 80)
    print("FLASH Model Training Status Report")
    print("=" * 80)
    
    # Check if training is still running
    pid_file = Path("training.pid")
    if pid_file.exists():
        with open(pid_file, 'r') as f:
            pid = f.read().strip()
        
        # Check if process is still running
        try:
            os.kill(int(pid), 0)
            print(f"⏳ Training is STILL RUNNING (PID: {pid})")
        except ProcessLookupError:
            print("✅ Training has COMPLETED")
            
    # Check training log
    log_file = Path("training.log")
    if log_file.exists():
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        print(f"\n📊 Training Log Summary ({len(lines)} lines):")
        
        # Extract key metrics
        for line in lines:
            if "Test Set Performance:" in line:
                print("\n🎯 Final Test Set Performance:")
            elif "AUC:" in line and "Test" not in line:
                print(f"  {line.strip()}")
            elif any(metric in line for metric in ["AUC:", "Accuracy:", "Precision:", "Recall:"]):
                print(f"  {line.strip()}")
                
    # Check test results
    results_file = Path("models/hierarchical_45features/test_results.json")
    if results_file.exists():
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        print("\n📈 Model Performance Summary:")
        print(f"  - Test AUC: {results.get('test_auc', 'N/A'):.3f}")
        print(f"  - Test Accuracy: {results.get('test_accuracy', 'N/A'):.3f}")
        print(f"  - Test Precision: {results.get('test_precision', 'N/A'):.3f}")
        print(f"  - Test Recall: {results.get('test_recall', 'N/A'):.3f}")
        print(f"  - Training Samples: {results.get('training_samples', 'N/A'):,}")
        print(f"  - Test Samples: {results.get('test_samples', 'N/A'):,}")
        
    # Check created models
    model_dir = Path("models/hierarchical_45features")
    if model_dir.exists():
        models = list(model_dir.glob("*.pkl"))
        print(f"\n🗃️  Models Created ({len(models)} files):")
        for model in sorted(models):
            size_mb = model.stat().st_size / (1024 * 1024)
            print(f"  - {model.name}: {size_mb:.1f} MB")
            
    # Check metadata
    metadata_file = Path("models/hierarchical_45features/hierarchical_metadata.json")
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        print("\n📋 Model Metadata:")
        print(f"  - Version: {metadata.get('version', 'N/A')}")
        print(f"  - Created: {metadata.get('created_at', 'N/A')}")
        print(f"  - Features Used: {metadata.get('features_used', 'N/A')}")
        
        if 'models' in metadata:
            print("\n🔧 Model Components:")
            for model_type, details in metadata['models'].items():
                if isinstance(details, list):
                    print(f"  - {model_type}: {len(details)} variants")
                elif isinstance(details, dict):
                    for k, v in details.items():
                        print(f"    - {k}: {v}")
                        
    # Compare with old models
    print("\n📊 Model Improvement (100k vs 10k dataset):")
    print("  - Old AUC (10k): 0.780 (quick training)")
    if results_file.exists():
        new_auc = results.get('test_auc', 0)
        improvement = (new_auc - 0.780) / 0.780 * 100
        print(f"  - New AUC (100k): {new_auc:.3f}")
        print(f"  - Improvement: {improvement:+.1f}%")
    
    print("\n" + "=" * 80)
    print("Training Status Check Complete")
    print("=" * 80)

if __name__ == "__main__":
    check_training_status()