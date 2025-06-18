#!/usr/bin/env python3
"""
Manage model integrity checks for FLASH
Allows disabling/enabling integrity checks and updating checksums
"""

import os
import sys
import argparse
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def disable_integrity_checks():
    """Disable integrity checks by setting environment variable"""
    print("To disable integrity checks, set the environment variable:")
    print("export FLASH_SKIP_INTEGRITY_CHECK=true")
    print("\nOr run the API server with:")
    print("FLASH_SKIP_INTEGRITY_CHECK=true python api_server_unified.py")


def rename_checksum_files(restore=False):
    """Rename checksum files to disable/enable integrity checks"""
    checksum_files = [
        "production_model_checksums.json",
        "model_checksums.json",
        "models/model_integrity_manifest.json"
    ]
    
    for file in checksum_files:
        if restore:
            # Restore disabled files
            disabled_file = f"{file}.disabled"
            if os.path.exists(disabled_file):
                os.rename(disabled_file, file)
                logger.info(f"Restored: {file}")
        else:
            # Disable by renaming
            if os.path.exists(file):
                os.rename(file, f"{file}.disabled")
                logger.info(f"Disabled: {file}")


def update_checksums():
    """Update checksums for all models"""
    from utils.model_integrity import ModelIntegrityChecker
    from security.model_integrity import ModelIntegrityChecker as SecurityChecker
    
    # Update production checksums
    print("Updating production model checksums...")
    prod_checker = ModelIntegrityChecker("production_model_checksums.json")
    
    # Check various model directories
    model_dirs = [
        "models/production_v45",
        "models/production_v45_fixed",
        "models/pattern_success_models",
        "models/hierarchical_45features",
        "models"
    ]
    
    for model_dir in model_dirs:
        if os.path.exists(model_dir):
            print(f"Scanning {model_dir}...")
            prod_checker.generate_checksums_for_directory(model_dir)
    
    # Update security manifest
    print("\nUpdating security manifest...")
    sec_checker = SecurityChecker()
    sec_checker.update_manifest(force=True)
    
    print("\nChecksum update complete!")


def verify_models():
    """Verify all models against checksums"""
    from utils.model_integrity import verify_production_models
    
    print("Verifying production models...")
    result = verify_production_models()
    
    if result:
        print("✅ All models passed integrity checks")
    else:
        print("❌ Some models failed integrity checks")
        print("Run with --update to update checksums for new models")


def main():
    parser = argparse.ArgumentParser(description="Manage FLASH model integrity checks")
    parser.add_argument("command", choices=["disable", "enable", "update", "verify", "help"],
                       help="Command to execute")
    
    args = parser.parse_args()
    
    if args.command == "disable":
        print("Disabling integrity checks...")
        rename_checksum_files(restore=False)
        disable_integrity_checks()
        
    elif args.command == "enable":
        print("Enabling integrity checks...")
        rename_checksum_files(restore=True)
        print("Integrity checks re-enabled")
        
    elif args.command == "update":
        update_checksums()
        
    elif args.command == "verify":
        verify_models()
        
    elif args.command == "help":
        print("FLASH Model Integrity Management")
        print("================================")
        print("\nCommands:")
        print("  disable - Disable integrity checks (rename checksum files)")
        print("  enable  - Re-enable integrity checks (restore checksum files)")
        print("  update  - Update checksums for all current models")
        print("  verify  - Verify all models against stored checksums")
        print("\nEnvironment variable:")
        print("  FLASH_SKIP_INTEGRITY_CHECK=true - Skip integrity checks without modifying files")


if __name__ == "__main__":
    main()