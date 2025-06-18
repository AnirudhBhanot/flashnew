"""
Model Integrity System - Ensures model security and authenticity
Implements checksums, versioning, and tamper detection
"""

import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import joblib
import numpy as np

logger = logging.getLogger(__name__)


class ModelIntegritySystem:
    """
    Comprehensive model integrity management system with:
    - SHA256 checksums for all models
    - Version tracking and history
    - Tamper detection
    - Automated integrity verification
    - Model signing and validation
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.checksum_file = self.models_dir / "model_checksums.json"
        self.integrity_log = self.models_dir / "integrity_log.json"
        self.checksums = self._load_checksums()
        self.verification_history = self._load_verification_history()
        
    def _load_checksums(self) -> dict:
        """Load existing checksums from file"""
        if self.checksum_file.exists():
            try:
                with open(self.checksum_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load checksums: {e}")
        return {}
    
    def _load_verification_history(self) -> list:
        """Load verification history"""
        if self.integrity_log.exists():
            try:
                with open(self.integrity_log, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                # Read file in chunks for memory efficiency
                for byte_block in iter(lambda: f.read(65536), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate checksum for {file_path}: {e}")
            return ""
    
    def calculate_model_checksum(self, model_path: Path) -> Tuple[str, dict]:
        """
        Calculate checksum and extract model metadata
        Returns: (checksum, metadata)
        """
        checksum = self.calculate_file_checksum(model_path)
        
        metadata = {
            "file_size": model_path.stat().st_size if model_path.exists() else 0,
            "last_modified": datetime.fromtimestamp(
                model_path.stat().st_mtime
            ).isoformat() if model_path.exists() else None,
            "model_type": self._identify_model_type(model_path)
        }
        
        # Try to extract model-specific metadata
        try:
            model = joblib.load(model_path)
            
            # Extract model information
            if hasattr(model, 'get_params'):
                metadata['model_params'] = model.get_params()
            
            if hasattr(model, 'feature_importances_'):
                metadata['feature_importance_sum'] = float(
                    np.sum(model.feature_importances_)
                )
            
            if hasattr(model, 'n_estimators'):
                metadata['n_estimators'] = model.n_estimators
                
        except Exception as e:
            logger.debug(f"Could not extract metadata from {model_path}: {e}")
        
        return checksum, metadata
    
    def _identify_model_type(self, model_path: Path) -> str:
        """Identify model type from filename"""
        name = model_path.stem.lower()
        
        if 'dna' in name:
            return 'dna_analyzer'
        elif 'temporal' in name:
            return 'temporal'
        elif 'industry' in name:
            return 'industry'
        elif 'ensemble' in name:
            return 'ensemble'
        elif 'camp' in name:
            return 'camp'
        elif 'pattern' in name:
            return 'pattern'
        elif 'stage' in name:
            return 'stage'
        else:
            return 'unknown'
    
    def register_model(self, model_path: Path, version: str = None) -> dict:
        """Register a model with integrity system"""
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        checksum, metadata = self.calculate_model_checksum(model_path)
        
        if not checksum:
            raise ValueError(f"Failed to calculate checksum for {model_path}")
        
        # Create registration entry
        registration = {
            "checksum": checksum,
            "path": str(model_path.relative_to(self.models_dir)),
            "version": version or datetime.now().strftime("v%Y%m%d_%H%M%S"),
            "registered_at": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        # Update checksums
        model_key = str(model_path.relative_to(self.models_dir))
        self.checksums[model_key] = registration
        
        # Save updated checksums
        self._save_checksums()
        
        logger.info(f"Registered model: {model_key} (checksum: {checksum[:16]}...)")
        
        return registration
    
    def verify_model(self, model_path: Path) -> Tuple[bool, dict]:
        """
        Verify model integrity
        Returns: (is_valid, verification_result)
        """
        if not model_path.exists():
            return False, {"error": "Model file not found"}
        
        model_key = str(model_path.relative_to(self.models_dir))
        
        # Check if model is registered
        if model_key not in self.checksums:
            return False, {"error": "Model not registered", "path": model_key}
        
        # Calculate current checksum
        current_checksum, current_metadata = self.calculate_model_checksum(model_path)
        registered_checksum = self.checksums[model_key]["checksum"]
        
        # Compare checksums
        is_valid = current_checksum == registered_checksum
        
        verification_result = {
            "model": model_key,
            "is_valid": is_valid,
            "registered_checksum": registered_checksum,
            "current_checksum": current_checksum,
            "verified_at": datetime.now().isoformat(),
            "metadata_changes": self._compare_metadata(
                self.checksums[model_key].get("metadata", {}),
                current_metadata
            )
        }
        
        # Log verification
        self._log_verification(verification_result)
        
        if not is_valid:
            logger.warning(f"Integrity check failed for {model_key}")
        
        return is_valid, verification_result
    
    def verify_all_models(self) -> dict:
        """Verify integrity of all registered models"""
        results = {
            "verified_at": datetime.now().isoformat(),
            "total_models": len(self.checksums),
            "valid_models": 0,
            "invalid_models": 0,
            "missing_models": 0,
            "details": {}
        }
        
        for model_key, registration in self.checksums.items():
            model_path = self.models_dir / model_key
            
            if not model_path.exists():
                results["missing_models"] += 1
                results["details"][model_key] = {
                    "status": "missing",
                    "registered_at": registration.get("registered_at")
                }
                continue
            
            is_valid, verification = self.verify_model(model_path)
            
            if is_valid:
                results["valid_models"] += 1
                results["details"][model_key] = {"status": "valid"}
            else:
                results["invalid_models"] += 1
                results["details"][model_key] = verification
        
        return results
    
    def _compare_metadata(self, old_metadata: dict, new_metadata: dict) -> dict:
        """Compare metadata to identify changes"""
        changes = {}
        
        for key in set(old_metadata.keys()) | set(new_metadata.keys()):
            old_val = old_metadata.get(key)
            new_val = new_metadata.get(key)
            
            if old_val != new_val:
                changes[key] = {
                    "old": old_val,
                    "new": new_val
                }
        
        return changes
    
    def _log_verification(self, verification_result: dict):
        """Log verification result"""
        self.verification_history.append(verification_result)
        
        # Keep only last 1000 verifications
        if len(self.verification_history) > 1000:
            self.verification_history = self.verification_history[-1000:]
        
        # Save to file
        try:
            with open(self.integrity_log, 'w') as f:
                json.dump(self.verification_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save verification log: {e}")
    
    def _save_checksums(self):
        """Save checksums to file"""
        try:
            with open(self.checksum_file, 'w') as f:
                json.dump(self.checksums, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save checksums: {e}")
    
    def generate_integrity_report(self) -> dict:
        """Generate comprehensive integrity report"""
        verification_results = self.verify_all_models()
        
        # Analyze verification history
        recent_failures = [
            v for v in self.verification_history[-100:]
            if not v.get("is_valid", True)
        ]
        
        report = {
            "report_generated": datetime.now().isoformat(),
            "system_status": "healthy" if verification_results["invalid_models"] == 0 else "compromised",
            "current_state": verification_results,
            "recent_failures": len(recent_failures),
            "recommendations": []
        }
        
        # Add recommendations
        if verification_results["invalid_models"] > 0:
            report["recommendations"].append(
                "CRITICAL: Invalid models detected. Investigate and re-register affected models."
            )
        
        if verification_results["missing_models"] > 0:
            report["recommendations"].append(
                "WARNING: Missing models detected. Verify model deployment."
            )
        
        if len(recent_failures) > 5:
            report["recommendations"].append(
                "CONCERN: Multiple recent verification failures. Check system security."
            )
        
        return report
    
    def register_all_models(self, model_patterns: List[str] = None) -> dict:
        """Register all models matching patterns"""
        if model_patterns is None:
            model_patterns = ["*.pkl", "*.joblib", "*.h5", "*.pt", "*.pth"]
        
        results = {
            "registered": [],
            "failed": [],
            "skipped": []
        }
        
        for pattern in model_patterns:
            for model_path in self.models_dir.rglob(pattern):
                if model_path.is_file():
                    model_key = str(model_path.relative_to(self.models_dir))
                    
                    # Skip if already registered with same checksum
                    if model_key in self.checksums:
                        current_checksum = self.calculate_file_checksum(model_path)
                        if current_checksum == self.checksums[model_key]["checksum"]:
                            results["skipped"].append(model_key)
                            continue
                    
                    try:
                        registration = self.register_model(model_path)
                        results["registered"].append(model_key)
                    except Exception as e:
                        logger.error(f"Failed to register {model_path}: {e}")
                        results["failed"].append({
                            "path": model_key,
                            "error": str(e)
                        })
        
        logger.info(
            f"Registration complete: {len(results['registered'])} registered, "
            f"{len(results['skipped'])} skipped, {len(results['failed'])} failed"
        )
        
        return results
    
    def create_model_signature(self, model_path: Path, private_key: str = None) -> dict:
        """Create cryptographic signature for model (simplified version)"""
        checksum = self.calculate_file_checksum(model_path)
        
        # In production, this would use proper cryptographic signing
        # For now, we'll create a simple signature
        signature_data = {
            "model": str(model_path.relative_to(self.models_dir)),
            "checksum": checksum,
            "signed_at": datetime.now().isoformat(),
            "signer": "FLASH ML Team",
            "algorithm": "SHA256"
        }
        
        # Create signature hash
        signature_string = json.dumps(signature_data, sort_keys=True)
        signature_hash = hashlib.sha256(signature_string.encode()).hexdigest()
        
        signature_data["signature"] = signature_hash
        
        # Save signature
        signature_file = model_path.with_suffix('.sig')
        with open(signature_file, 'w') as f:
            json.dump(signature_data, f, indent=2)
        
        return signature_data
    
    def verify_model_signature(self, model_path: Path) -> Tuple[bool, dict]:
        """Verify model signature"""
        signature_file = model_path.with_suffix('.sig')
        
        if not signature_file.exists():
            return False, {"error": "Signature file not found"}
        
        try:
            with open(signature_file, 'r') as f:
                signature_data = json.load(f)
            
            # Verify checksum matches
            current_checksum = self.calculate_file_checksum(model_path)
            if current_checksum != signature_data["checksum"]:
                return False, {"error": "Checksum mismatch"}
            
            # Verify signature (simplified)
            stored_signature = signature_data.pop("signature")
            signature_string = json.dumps(signature_data, sort_keys=True)
            calculated_signature = hashlib.sha256(signature_string.encode()).hexdigest()
            
            if stored_signature != calculated_signature:
                return False, {"error": "Invalid signature"}
            
            return True, {
                "valid": True,
                "signed_at": signature_data["signed_at"],
                "signer": signature_data["signer"]
            }
            
        except Exception as e:
            return False, {"error": f"Signature verification failed: {e}"}


def setup_model_integrity():
    """Initialize and setup model integrity system"""
    integrity_system = ModelIntegritySystem()
    
    # Register all existing models
    logger.info("Setting up model integrity system...")
    results = integrity_system.register_all_models()
    
    # Generate initial report
    report = integrity_system.generate_integrity_report()
    
    logger.info(f"Model integrity system initialized: {report['system_status']}")
    
    return integrity_system


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize integrity system
    integrity_system = setup_model_integrity()
    
    # Generate and print report
    report = integrity_system.generate_integrity_report()
    print(json.dumps(report, indent=2))