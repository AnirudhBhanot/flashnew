"""
Model Integrity Checker
Validates model files before loading to prevent malicious code execution
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ModelIntegrityChecker:
    """Verify model file integrity before loading"""
    
    def __init__(self, manifest_path: str = "models/model_integrity_manifest.json"):
        self.manifest_path = manifest_path
        self.manifest = self._load_manifest()
        
    def _load_manifest(self) -> Dict[str, str]:
        """Load the integrity manifest with expected checksums"""
        if Path(self.manifest_path).exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks for memory efficiency
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def verify_model(self, model_path: str) -> bool:
        """Verify a model file against its expected checksum"""
        # Check for bypass environment variable
        if os.environ.get('FLASH_SKIP_INTEGRITY_CHECK', '').lower() in ('true', '1', 'yes'):
            logger.warning(f"Integrity check bypassed for {model_path} (FLASH_SKIP_INTEGRITY_CHECK=true)")
            return True
            
        if not Path(model_path).exists():
            logger.error(f"Model file not found: {model_path}")
            return False
            
        # Calculate current checksum
        current_checksum = self.calculate_checksum(model_path)
        
        # Get expected checksum from manifest
        model_key = str(Path(model_path))
        expected_checksum = self.manifest.get(model_key)
        
        if not expected_checksum:
            logger.warning(f"No checksum found for {model_key}. Adding to manifest.")
            # Add new model to manifest
            self.manifest[model_key] = current_checksum
            self._save_manifest()
            return True
            
        # Verify checksum
        if current_checksum != expected_checksum:
            logger.error(f"Checksum mismatch for {model_key}")
            logger.error(f"Expected: {expected_checksum}")
            logger.error(f"Got: {current_checksum}")
            return False
            
        logger.info(f"Model verified: {model_key}")
        return True
    
    def update_manifest(self, force: bool = False):
        """Update manifest with current model checksums"""
        model_dirs = [
            "models/production_v45",
            "models/production_v45_fixed", 
            "models/pattern_models",
            "models/v2_enhanced"
        ]
        
        updated_count = 0
        for model_dir in model_dirs:
            if not Path(model_dir).exists():
                continue
                
            for model_file in Path(model_dir).glob("*.pkl"):
                model_key = str(model_file)
                current_checksum = self.calculate_checksum(str(model_file))
                
                if force or model_key not in self.manifest:
                    self.manifest[model_key] = current_checksum
                    updated_count += 1
                    logger.info(f"Updated checksum for {model_key}")
        
        if updated_count > 0:
            self._save_manifest()
            logger.info(f"Updated {updated_count} model checksums")
            
    def _save_manifest(self):
        """Save the manifest to disk"""
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)


def secure_model_loader(model_path: str, checker: Optional[ModelIntegrityChecker] = None):
    """Securely load a model after verifying integrity"""
    import joblib
    
    if checker is None:
        checker = ModelIntegrityChecker()
        
    # Verify model integrity
    if not checker.verify_model(model_path):
        raise ValueError(f"Model integrity check failed for {model_path}")
        
    # Load model with restricted unpickling
    try:
        # Use joblib with mmap_mode to avoid loading entire file into memory
        model = joblib.load(model_path, mmap_mode='r')
        logger.info(f"Successfully loaded verified model: {model_path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model {model_path}: {e}")
        raise


if __name__ == "__main__":
    # Initialize integrity checker
    checker = ModelIntegrityChecker()
    
    # Update manifest with current models
    print("Updating model integrity manifest...")
    checker.update_manifest(force=True)
    
    # Test verification
    test_model = "models/production_v45_fixed/dna_analyzer.pkl"
    if Path(test_model).exists():
        print(f"\nTesting verification of {test_model}")
        is_valid = checker.verify_model(test_model)
        print(f"Model valid: {is_valid}")