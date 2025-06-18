"""
Model file integrity checking using SHA256 checksums
"""
import hashlib
import json
import os
import pickle
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ModelIntegrityChecker:
    """Verify model file integrity using checksums"""
    
    def __init__(self, checksum_file: str = "model_checksums.json"):
        self.checksum_file = checksum_file
        self.checksums = self._load_checksums()
    
    def _load_checksums(self) -> Dict[str, str]:
        """Load checksums from file"""
        if os.path.exists(self.checksum_file):
            try:
                with open(self.checksum_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load checksums: {e}")
                return {}
        return {}
    
    def _save_checksums(self):
        """Save checksums to file"""
        try:
            with open(self.checksum_file, 'w') as f:
                json.dump(self.checksums, f, indent=2)
            logger.info(f"Saved checksums to {self.checksum_file}")
        except Exception as e:
            logger.error(f"Failed to save checksums: {e}")
    
    def calculate_checksum(self, filepath: str) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                # Read in chunks to handle large files
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate checksum for {filepath}: {e}")
            raise
    
    def verify_model(self, filepath: str, expected_checksum: Optional[str] = None) -> bool:
        """Verify model file integrity"""
        # Check for bypass environment variable
        if os.environ.get('FLASH_SKIP_INTEGRITY_CHECK', '').lower() in ('true', '1', 'yes'):
            logger.warning(f"Integrity check bypassed for {filepath} (FLASH_SKIP_INTEGRITY_CHECK=true)")
            return True
            
        if not os.path.exists(filepath):
            logger.error(f"Model file not found: {filepath}")
            return False
        
        # Calculate current checksum
        try:
            current_checksum = self.calculate_checksum(filepath)
        except Exception:
            return False
        
        # Use provided checksum or lookup from stored checksums
        if expected_checksum is None:
            expected_checksum = self.checksums.get(filepath)
        
        if expected_checksum is None:
            logger.warning(f"No checksum found for {filepath}, storing current checksum")
            self.register_model(filepath, current_checksum)
            return True
        
        # Verify checksum
        if current_checksum == expected_checksum:
            logger.info(f"Model integrity verified: {filepath}")
            return True
        else:
            logger.error(f"Model integrity check failed for {filepath}")
            logger.error(f"Expected: {expected_checksum}")
            logger.error(f"Got: {current_checksum}")
            return False
    
    def register_model(self, filepath: str, checksum: Optional[str] = None):
        """Register a model file with its checksum"""
        if checksum is None:
            checksum = self.calculate_checksum(filepath)
        
        self.checksums[filepath] = checksum
        self._save_checksums()
        logger.info(f"Registered model {filepath} with checksum {checksum}")
    
    def load_model_safe(self, filepath: str, expected_checksum: Optional[str] = None) -> Any:
        """Load a model file after verifying integrity"""
        if not self.verify_model(filepath, expected_checksum):
            raise ValueError(f"Model integrity check failed for {filepath}")
        
        try:
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Safely loaded model from {filepath}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model from {filepath}: {e}")
            raise
    
    def generate_checksums_for_directory(self, directory: str, pattern: str = "*.pkl"):
        """Generate checksums for all model files in a directory"""
        model_dir = Path(directory)
        if not model_dir.exists():
            logger.error(f"Directory not found: {directory}")
            return
        
        model_files = list(model_dir.glob(pattern))
        logger.info(f"Found {len(model_files)} model files in {directory}")
        
        for model_file in model_files:
            filepath = str(model_file)
            try:
                checksum = self.calculate_checksum(filepath)
                self.checksums[filepath] = checksum
                logger.info(f"Generated checksum for {filepath}: {checksum}")
            except Exception as e:
                logger.error(f"Failed to generate checksum for {filepath}: {e}")
        
        self._save_checksums()
        logger.info(f"Generated checksums for {len(model_files)} files")
    
    def verify_all_models(self) -> Dict[str, bool]:
        """Verify all registered models"""
        results = {}
        for filepath, expected_checksum in self.checksums.items():
            results[filepath] = self.verify_model(filepath, expected_checksum)
        
        passed = sum(1 for v in results.values() if v)
        logger.info(f"Model verification complete: {passed}/{len(results)} passed")
        
        return results


# Global instance
model_integrity_checker = ModelIntegrityChecker()


def generate_production_checksums():
    """Generate checksums for all production models"""
    checker = ModelIntegrityChecker("production_model_checksums.json")
    
    # Generate checksums for production models
    checker.generate_checksums_for_directory("models/production_v45")
    
    # Also generate for pattern models if they exist
    if os.path.exists("models/pattern_success_models"):
        checker.generate_checksums_for_directory("models/pattern_success_models")
    
    return checker


def verify_production_models() -> bool:
    """Verify all production models before server startup"""
    checker = ModelIntegrityChecker("production_model_checksums.json")
    results = checker.verify_all_models()
    
    # Check if all models passed
    all_passed = all(results.values())
    
    if not all_passed:
        failed_models = [f for f, passed in results.items() if not passed]
        logger.error(f"Model verification failed for: {failed_models}")
    
    return all_passed


if __name__ == "__main__":
    # Generate checksums for production models
    print("Generating checksums for production models...")
    checker = generate_production_checksums()
    
    print("\nVerifying all models...")
    results = checker.verify_all_models()
    
    print("\nVerification Results:")
    for filepath, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {filepath}")