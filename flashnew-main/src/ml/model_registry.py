"""
Model Registry and Version Management
Tracks model versions, performance, and deployment status
"""

import json
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil
import logging

from database.connection import get_session
from database.models import ModelVersion
from database.repositories import ModelVersionRepository
from security.model_integrity import ModelIntegrityChecker

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Central registry for ML model management"""
    
    def __init__(self, registry_path: str = "models/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.registry_path / "manifest.json"
        self.integrity_checker = ModelIntegrityChecker()
        self._load_manifest()
    
    def _load_manifest(self):
        """Load the registry manifest"""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                "models": {},
                "active_versions": {},
                "deployment_history": []
            }
    
    def _save_manifest(self):
        """Save the registry manifest"""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2, default=str)
    
    def register_model(
        self,
        model_path: str,
        model_type: str,
        version: str,
        performance_metrics: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a new model version
        
        Args:
            model_path: Path to the model file
            model_type: Type of model (dna_analyzer, temporal, etc.)
            version: Version string (e.g., "1.2.3")
            performance_metrics: Dict with auc, accuracy, etc.
            metadata: Additional metadata
            
        Returns:
            Model ID
        """
        # Calculate checksum
        checksum = self.integrity_checker.calculate_checksum(model_path)
        
        # Generate model ID
        model_id = f"{model_type}_v{version}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Copy model to registry
        dest_path = self.registry_path / model_type / f"{model_id}.pkl"
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(model_path, dest_path)
        
        # Create model entry
        model_entry = {
            "id": model_id,
            "type": model_type,
            "version": version,
            "path": str(dest_path),
            "checksum": checksum,
            "registered_at": datetime.utcnow().isoformat(),
            "performance": performance_metrics,
            "metadata": metadata or {},
            "status": "registered"
        }
        
        # Add to manifest
        self.manifest["models"][model_id] = model_entry
        self._save_manifest()
        
        # Update integrity manifest
        self.integrity_checker.manifest[str(dest_path)] = checksum
        self.integrity_checker._save_manifest()
        
        # Store in database if available
        try:
            with get_session() as session:
                repo = ModelVersionRepository(session)
                repo.create(
                    version=version,
                    model_type=model_type,
                    model_path=str(dest_path),
                    model_checksum=checksum,
                    performance_metrics=performance_metrics,
                    metadata=metadata,
                    training_date=datetime.utcnow()
                )
        except Exception as e:
            logger.warning(f"Could not store model in database: {e}")
        
        logger.info(f"Registered model: {model_id}")
        return model_id
    
    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model information by ID"""
        return self.manifest["models"].get(model_id)
    
    def get_active_version(self, model_type: str) -> Optional[str]:
        """Get the active version for a model type"""
        return self.manifest["active_versions"].get(model_type)
    
    def list_models(
        self, 
        model_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List models with optional filters"""
        models = list(self.manifest["models"].values())
        
        if model_type:
            models = [m for m in models if m["type"] == model_type]
        
        if status:
            models = [m for m in models if m.get("status") == status]
        
        # Sort by registration date
        models.sort(key=lambda x: x["registered_at"], reverse=True)
        
        return models
    
    def promote_model(self, model_id: str, environment: str = "staging"):
        """
        Promote a model to a specific environment
        
        Args:
            model_id: Model ID to promote
            environment: Target environment (staging, production)
        """
        model = self.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        # Verify model integrity
        if not self.integrity_checker.verify_model(model["path"]):
            raise ValueError(f"Model {model_id} failed integrity check")
        
        # Update status
        model["status"] = environment
        model[f"promoted_to_{environment}_at"] = datetime.utcnow().isoformat()
        
        # If promoting to production, update active version
        if environment == "production":
            old_active = self.manifest["active_versions"].get(model["type"])
            self.manifest["active_versions"][model["type"]] = model_id
            
            # Record deployment
            deployment = {
                "model_id": model_id,
                "model_type": model["type"],
                "environment": environment,
                "deployed_at": datetime.utcnow().isoformat(),
                "replaced_model": old_active
            }
            self.manifest["deployment_history"].append(deployment)
            
            # Update old model status
            if old_active and old_active in self.manifest["models"]:
                self.manifest["models"][old_active]["status"] = "archived"
        
        self._save_manifest()
        
        # Update database
        try:
            with get_session() as session:
                repo = ModelVersionRepository(session)
                db_model = session.query(ModelVersion).filter_by(
                    version=model["version"],
                    model_type=model["type"]
                ).first()
                
                if db_model and environment == "production":
                    repo.set_production(db_model)
        except Exception as e:
            logger.warning(f"Could not update database: {e}")
        
        logger.info(f"Promoted model {model_id} to {environment}")
    
    def rollback_model(self, model_type: str):
        """Rollback to the previous production model"""
        # Find current and previous production models
        history = [
            d for d in self.manifest["deployment_history"]
            if d["model_type"] == model_type and d["environment"] == "production"
        ]
        
        if len(history) < 2:
            raise ValueError(f"No previous version to rollback to for {model_type}")
        
        # Get previous deployment
        current = history[-1]
        previous = history[-2]
        
        # Promote previous model back to production
        if previous["replaced_model"]:
            self.promote_model(previous["replaced_model"], "production")
            logger.info(f"Rolled back {model_type} to {previous['replaced_model']}")
    
    def compare_models(self, model_id1: str, model_id2: str) -> Dict[str, Any]:
        """Compare two model versions"""
        model1 = self.get_model(model_id1)
        model2 = self.get_model(model_id2)
        
        if not model1 or not model2:
            raise ValueError("One or both models not found")
        
        comparison = {
            "model1": {
                "id": model_id1,
                "version": model1["version"],
                "performance": model1["performance"]
            },
            "model2": {
                "id": model_id2,
                "version": model2["version"],
                "performance": model2["performance"]
            },
            "performance_diff": {}
        }
        
        # Calculate performance differences
        for metric in model1["performance"]:
            if metric in model2["performance"]:
                diff = model2["performance"][metric] - model1["performance"][metric]
                comparison["performance_diff"][metric] = {
                    "absolute": diff,
                    "relative": diff / model1["performance"][metric] if model1["performance"][metric] != 0 else 0
                }
        
        return comparison
    
    def cleanup_old_models(self, keep_last_n: int = 5):
        """Clean up old model files, keeping the last N versions"""
        model_types = {}
        
        # Group models by type
        for model in self.manifest["models"].values():
            model_type = model["type"]
            if model_type not in model_types:
                model_types[model_type] = []
            model_types[model_type].append(model)
        
        # Clean up each type
        for model_type, models in model_types.items():
            # Sort by registration date
            models.sort(key=lambda x: x["registered_at"], reverse=True)
            
            # Keep active/production models and last N
            to_keep = set()
            
            # Always keep active version
            active_id = self.manifest["active_versions"].get(model_type)
            if active_id:
                to_keep.add(active_id)
            
            # Keep production/staging models
            for model in models:
                if model["status"] in ["production", "staging"]:
                    to_keep.add(model["id"])
            
            # Keep last N
            for model in models[:keep_last_n]:
                to_keep.add(model["id"])
            
            # Delete others
            for model in models:
                if model["id"] not in to_keep:
                    # Delete file
                    model_path = Path(model["path"])
                    if model_path.exists():
                        model_path.unlink()
                        logger.info(f"Deleted old model file: {model_path}")
                    
                    # Remove from manifest
                    del self.manifest["models"][model["id"]]
        
        self._save_manifest()
        logger.info(f"Cleaned up old models, keeping last {keep_last_n} versions")
    
    def export_metrics(self) -> pd.DataFrame:
        """Export all model metrics as DataFrame"""
        import pandas as pd
        
        records = []
        for model in self.manifest["models"].values():
            record = {
                "id": model["id"],
                "type": model["type"],
                "version": model["version"],
                "status": model["status"],
                "registered_at": model["registered_at"]
            }
            
            # Add performance metrics
            for metric, value in model["performance"].items():
                record[f"perf_{metric}"] = value
            
            records.append(record)
        
        return pd.DataFrame(records)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Model Registry CLI")
    parser.add_argument("command", choices=["list", "register", "promote", "rollback", "compare", "cleanup"])
    parser.add_argument("--model-id", help="Model ID")
    parser.add_argument("--model-type", help="Model type")
    parser.add_argument("--version", help="Model version")
    parser.add_argument("--path", help="Model file path")
    parser.add_argument("--environment", default="staging", help="Target environment")
    parser.add_argument("--keep-last", type=int, default=5, help="Number of versions to keep")
    
    args = parser.parse_args()
    
    registry = ModelRegistry()
    
    if args.command == "list":
        models = registry.list_models(model_type=args.model_type)
        for model in models:
            print(f"{model['id']} - {model['type']} v{model['version']} - {model['status']}")
    
    elif args.command == "promote":
        if not args.model_id:
            print("Error: --model-id required")
        else:
            registry.promote_model(args.model_id, args.environment)
            print(f"Promoted {args.model_id} to {args.environment}")
    
    elif args.command == "cleanup":
        registry.cleanup_old_models(keep_last_n=args.keep_last)
        print(f"Cleaned up old models, keeping last {args.keep_last}")
    
    # Add more commands as needed