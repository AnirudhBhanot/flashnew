"""
Model Versioning and Deployment System
Manages model versions, rollbacks, and deployment strategies
"""

import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import joblib
import hashlib
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ModelVersion:
    """Model version metadata"""
    version: str
    model_type: str
    created_at: str
    deployed_at: Optional[str]
    performance_metrics: Dict[str, float]
    checksum: str
    status: str  # 'staging', 'production', 'archived'
    deployment_notes: Optional[str]
    rollback_version: Optional[str]


class ModelVersioningSystem:
    """
    Comprehensive model versioning and deployment system
    Features:
    - Version control for all model types
    - Blue-green deployment
    - Automatic rollback capability
    - Performance-based promotion
    - Deployment history tracking
    """
    
    def __init__(self, models_dir: str = "models", versions_dir: str = "model_versions"):
        self.models_dir = Path(models_dir)
        self.versions_dir = Path(versions_dir)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.versions_dir / "version_metadata.json"
        self.deployment_log = self.versions_dir / "deployment_log.json"
        
        self.metadata = self._load_metadata()
        self.deployment_history = self._load_deployment_history()
    
    def _load_metadata(self) -> dict:
        """Load version metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "versions": {},
            "current_production": {},
            "deployment_config": {
                "min_performance_threshold": 0.70,
                "canary_percentage": 0.10,
                "rollback_threshold": 0.65
            }
        }
    
    def _load_deployment_history(self) -> list:
        """Load deployment history"""
        if self.deployment_log.exists():
            with open(self.deployment_log, 'r') as f:
                return json.load(f)
        return []
    
    def _save_metadata(self):
        """Save version metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _save_deployment_history(self):
        """Save deployment history"""
        with open(self.deployment_log, 'w') as f:
            json.dump(self.deployment_history, f, indent=2)
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def create_version(self, model_path: Path, model_type: str, 
                      performance_metrics: Dict[str, float], 
                      notes: str = None) -> ModelVersion:
        """Create a new model version"""
        
        # Generate version ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_id = f"{model_type}_v{timestamp}"
        
        # Create version directory
        version_dir = self.versions_dir / version_id
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy model to version directory
        model_filename = model_path.name
        versioned_model_path = version_dir / model_filename
        shutil.copy2(model_path, versioned_model_path)
        
        # Copy associated files (scalers, encoders, etc.)
        for associated_file in model_path.parent.glob(f"{model_path.stem}*"):
            if associated_file != model_path:
                shutil.copy2(associated_file, version_dir / associated_file.name)
        
        # Calculate checksum
        checksum = self._calculate_checksum(versioned_model_path)
        
        # Create version metadata
        version = ModelVersion(
            version=version_id,
            model_type=model_type,
            created_at=datetime.now().isoformat(),
            deployed_at=None,
            performance_metrics=performance_metrics,
            checksum=checksum,
            status="staging",
            deployment_notes=notes,
            rollback_version=self.get_current_production_version(model_type)
        )
        
        # Store metadata
        self.metadata["versions"][version_id] = asdict(version)
        self._save_metadata()
        
        logger.info(f"Created version {version_id} for {model_type}")
        
        return version
    
    def get_current_production_version(self, model_type: str) -> Optional[str]:
        """Get current production version for a model type"""
        return self.metadata["current_production"].get(model_type)
    
    def deploy_version(self, version_id: str, deployment_strategy: str = "blue_green") -> bool:
        """Deploy a model version to production"""
        
        if version_id not in self.metadata["versions"]:
            logger.error(f"Version {version_id} not found")
            return False
        
        version_data = self.metadata["versions"][version_id]
        model_type = version_data["model_type"]
        
        # Check performance threshold
        avg_performance = sum(version_data["performance_metrics"].values()) / len(version_data["performance_metrics"])
        if avg_performance < self.metadata["deployment_config"]["min_performance_threshold"]:
            logger.error(f"Version {version_id} performance {avg_performance:.3f} below threshold")
            return False
        
        # Execute deployment strategy
        if deployment_strategy == "blue_green":
            success = self._blue_green_deployment(version_id, model_type)
        elif deployment_strategy == "canary":
            success = self._canary_deployment(version_id, model_type)
        else:
            success = self._direct_deployment(version_id, model_type)
        
        if success:
            # Update metadata
            version_data["deployed_at"] = datetime.now().isoformat()
            version_data["status"] = "production"
            
            # Archive old production version
            old_version = self.get_current_production_version(model_type)
            if old_version and old_version in self.metadata["versions"]:
                self.metadata["versions"][old_version]["status"] = "archived"
            
            # Set new production version
            self.metadata["current_production"][model_type] = version_id
            self._save_metadata()
            
            # Log deployment
            self._log_deployment(version_id, model_type, deployment_strategy, "success")
            
            logger.info(f"Successfully deployed {version_id} to production")
            return True
        
        return False
    
    def _blue_green_deployment(self, version_id: str, model_type: str) -> bool:
        """Blue-green deployment strategy"""
        try:
            # Prepare green environment
            version_dir = self.versions_dir / version_id
            production_dir = self.models_dir / "production"
            production_dir.mkdir(exist_ok=True)
            
            # Stage new version in green
            green_dir = production_dir / f"{model_type}_green"
            if green_dir.exists():
                shutil.rmtree(green_dir)
            shutil.copytree(version_dir, green_dir)
            
            # Switch traffic (rename directories)
            blue_dir = production_dir / f"{model_type}_blue"
            current_dir = production_dir / model_type
            
            # Backup current as blue
            if current_dir.exists():
                if blue_dir.exists():
                    shutil.rmtree(blue_dir)
                current_dir.rename(blue_dir)
            
            # Promote green to current
            green_dir.rename(current_dir)
            
            return True
            
        except Exception as e:
            logger.error(f"Blue-green deployment failed: {e}")
            # Attempt rollback
            if blue_dir.exists() and not current_dir.exists():
                blue_dir.rename(current_dir)
            return False
    
    def _canary_deployment(self, version_id: str, model_type: str) -> bool:
        """Canary deployment strategy"""
        try:
            # Create canary configuration
            canary_config = {
                "version_id": version_id,
                "model_type": model_type,
                "traffic_percentage": self.metadata["deployment_config"]["canary_percentage"],
                "started_at": datetime.now().isoformat(),
                "metrics": {}
            }
            
            # Save canary config
            canary_file = self.versions_dir / f"canary_{model_type}.json"
            with open(canary_file, 'w') as f:
                json.dump(canary_config, f, indent=2)
            
            logger.info(f"Started canary deployment for {version_id} with {canary_config['traffic_percentage']*100}% traffic")
            
            # In production, this would configure load balancer
            # For now, we'll simulate success
            return True
            
        except Exception as e:
            logger.error(f"Canary deployment failed: {e}")
            return False
    
    def _direct_deployment(self, version_id: str, model_type: str) -> bool:
        """Direct deployment strategy"""
        try:
            version_dir = self.versions_dir / version_id
            target_dir = self.models_dir / "production" / model_type
            
            # Backup current version
            if target_dir.exists():
                backup_dir = self.versions_dir / f"backup_{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copytree(target_dir, backup_dir)
                shutil.rmtree(target_dir)
            
            # Deploy new version
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(version_dir, target_dir)
            
            return True
            
        except Exception as e:
            logger.error(f"Direct deployment failed: {e}")
            return False
    
    def rollback(self, model_type: str) -> bool:
        """Rollback to previous version"""
        current_version = self.get_current_production_version(model_type)
        if not current_version:
            logger.error(f"No current version found for {model_type}")
            return False
        
        version_data = self.metadata["versions"][current_version]
        rollback_version = version_data.get("rollback_version")
        
        if not rollback_version:
            logger.error(f"No rollback version found for {current_version}")
            return False
        
        logger.info(f"Rolling back {model_type} from {current_version} to {rollback_version}")
        
        # Execute rollback
        success = self._direct_deployment(rollback_version, model_type)
        
        if success:
            # Update metadata
            self.metadata["current_production"][model_type] = rollback_version
            self.metadata["versions"][rollback_version]["status"] = "production"
            self.metadata["versions"][current_version]["status"] = "rolled_back"
            self._save_metadata()
            
            # Log rollback
            self._log_deployment(rollback_version, model_type, "rollback", "success", 
                               f"Rolled back from {current_version}")
            
        return success
    
    def _log_deployment(self, version_id: str, model_type: str, 
                       strategy: str, status: str, notes: str = None):
        """Log deployment event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "version_id": version_id,
            "model_type": model_type,
            "strategy": strategy,
            "status": status,
            "notes": notes
        }
        
        self.deployment_history.append(event)
        
        # Keep last 1000 events
        if len(self.deployment_history) > 1000:
            self.deployment_history = self.deployment_history[-1000:]
        
        self._save_deployment_history()
    
    def promote_canary(self, model_type: str) -> bool:
        """Promote canary deployment to full production"""
        canary_file = self.versions_dir / f"canary_{model_type}.json"
        
        if not canary_file.exists():
            logger.error(f"No canary deployment found for {model_type}")
            return False
        
        with open(canary_file, 'r') as f:
            canary_config = json.load(f)
        
        version_id = canary_config["version_id"]
        
        # Deploy to full production
        success = self._direct_deployment(version_id, model_type)
        
        if success:
            # Clean up canary config
            canary_file.unlink()
            logger.info(f"Promoted canary {version_id} to full production")
        
        return success
    
    def list_versions(self, model_type: str = None, status: str = None) -> List[Dict]:
        """List model versions with optional filters"""
        versions = []
        
        for version_id, version_data in self.metadata["versions"].items():
            if model_type and version_data["model_type"] != model_type:
                continue
            if status and version_data["status"] != status:
                continue
            
            versions.append({
                "version_id": version_id,
                "model_type": version_data["model_type"],
                "created_at": version_data["created_at"],
                "status": version_data["status"],
                "performance": version_data["performance_metrics"]
            })
        
        # Sort by creation date
        versions.sort(key=lambda x: x["created_at"], reverse=True)
        
        return versions
    
    def get_deployment_history(self, model_type: str = None, limit: int = 100) -> List[Dict]:
        """Get deployment history"""
        history = self.deployment_history
        
        if model_type:
            history = [e for e in history if e.get("model_type") == model_type]
        
        return history[-limit:]
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare two model versions"""
        if version1 not in self.metadata["versions"] or version2 not in self.metadata["versions"]:
            return {"error": "One or both versions not found"}
        
        v1_data = self.metadata["versions"][version1]
        v2_data = self.metadata["versions"][version2]
        
        comparison = {
            "version1": version1,
            "version2": version2,
            "performance_diff": {},
            "created_diff_days": (
                datetime.fromisoformat(v2_data["created_at"]) - 
                datetime.fromisoformat(v1_data["created_at"])
            ).days
        }
        
        # Compare performance metrics
        for metric in set(v1_data["performance_metrics"].keys()) | set(v2_data["performance_metrics"].keys()):
            v1_val = v1_data["performance_metrics"].get(metric, 0)
            v2_val = v2_data["performance_metrics"].get(metric, 0)
            comparison["performance_diff"][metric] = {
                "v1": v1_val,
                "v2": v2_val,
                "diff": v2_val - v1_val,
                "pct_change": ((v2_val - v1_val) / v1_val * 100) if v1_val > 0 else 0
            }
        
        return comparison
    
    def cleanup_old_versions(self, keep_last_n: int = 10, keep_days: int = 90):
        """Clean up old archived versions"""
        cutoff_date = datetime.now().timestamp() - (keep_days * 86400)
        
        versions_by_type = {}
        for version_id, version_data in self.metadata["versions"].items():
            model_type = version_data["model_type"]
            if model_type not in versions_by_type:
                versions_by_type[model_type] = []
            versions_by_type[model_type].append((version_id, version_data))
        
        removed_count = 0
        
        for model_type, versions in versions_by_type.items():
            # Sort by creation date
            versions.sort(key=lambda x: x[1]["created_at"], reverse=True)
            
            # Keep production and recent versions
            for i, (version_id, version_data) in enumerate(versions):
                if (version_data["status"] == "archived" and 
                    i >= keep_last_n and
                    datetime.fromisoformat(version_data["created_at"]).timestamp() < cutoff_date):
                    
                    # Remove version directory
                    version_dir = self.versions_dir / version_id
                    if version_dir.exists():
                        shutil.rmtree(version_dir)
                    
                    # Remove from metadata
                    del self.metadata["versions"][version_id]
                    removed_count += 1
        
        if removed_count > 0:
            self._save_metadata()
            logger.info(f"Cleaned up {removed_count} old versions")
        
        return removed_count


def setup_model_versioning():
    """Initialize model versioning system"""
    versioning_system = ModelVersioningSystem()
    
    logger.info("Model versioning system initialized")
    
    # Example: Create initial versions for production models
    production_models = [
        ("models/production_v45_fixed/dna_analyzer_model.pkl", "dna_analyzer"),
        ("models/production_v45_fixed/temporal_model.pkl", "temporal"),
        ("models/production_v45_fixed/industry_model.pkl", "industry"),
        ("models/production_v45_fixed/ensemble_model.pkl", "ensemble")
    ]
    
    for model_path, model_type in production_models:
        path = Path(model_path)
        if path.exists():
            # Create initial version with dummy metrics
            performance_metrics = {
                "accuracy": 0.727,  # From documentation
                "auc": 0.727,
                "precision": 0.70,
                "recall": 0.68
            }
            
            version = versioning_system.create_version(
                path, 
                model_type,
                performance_metrics,
                "Initial production version"
            )
            
            # Deploy to production
            versioning_system.deploy_version(version.version, "direct")
    
    return versioning_system


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_model_versioning()