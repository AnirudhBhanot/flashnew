"""
Schema Evolution System
Handle feature changes over time while maintaining backward compatibility
"""

import json
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

from .feature_registry import FeatureRegistry, FeatureDefinition

logger = logging.getLogger(__name__)


class MigrationType(Enum):
    """Types of schema migrations"""
    ADD_FEATURE = "add_feature"
    REMOVE_FEATURE = "remove_feature"
    RENAME_FEATURE = "rename_feature"
    CHANGE_TYPE = "change_type"
    CHANGE_CONSTRAINTS = "change_constraints"
    ADD_COMPUTATION = "add_computation"


@dataclass
class Migration:
    """A single schema migration"""
    version: str
    migration_type: MigrationType
    timestamp: datetime
    description: str
    
    # Migration details
    feature_name: Optional[str] = None
    old_name: Optional[str] = None
    new_name: Optional[str] = None
    old_type: Optional[type] = None
    new_type: Optional[type] = None
    default_value: Optional[Any] = None
    computation: Optional[Callable] = None
    rollback_computation: Optional[Callable] = None
    
    # Additional metadata
    author: Optional[str] = None
    is_breaking: bool = False
    affected_models: List[str] = None
    
    def __post_init__(self):
        if self.affected_models is None:
            self.affected_models = []
    
    def to_dict(self) -> Dict:
        """Serialize migration (without functions)"""
        return {
            'version': self.version,
            'migration_type': self.migration_type.value,
            'timestamp': self.timestamp.isoformat(),
            'description': self.description,
            'feature_name': self.feature_name,
            'old_name': self.old_name,
            'new_name': self.new_name,
            'old_type': self.old_type.__name__ if self.old_type else None,
            'new_type': self.new_type.__name__ if self.new_type else None,
            'default_value': self.default_value,
            'has_computation': self.computation is not None,
            'has_rollback': self.rollback_computation is not None,
            'author': self.author,
            'is_breaking': self.is_breaking,
            'affected_models': self.affected_models
        }


class SchemaVersion:
    """Represents a specific version of the schema"""
    
    def __init__(self, version: str, registry: FeatureRegistry, parent_version: Optional[str] = None):
        self.version = version
        self.registry = registry
        self.parent_version = parent_version
        self.created_at = datetime.now()
        self.migrations_applied: List[str] = []
    
    def get_feature_names(self) -> List[str]:
        """Get all feature names in this version"""
        return self.registry.get_feature_names()
    
    def get_feature_count(self) -> int:
        """Get total feature count"""
        return len(self.registry.features)
    
    def to_dict(self) -> Dict:
        """Serialize version info"""
        return {
            'version': self.version,
            'parent_version': self.parent_version,
            'created_at': self.created_at.isoformat(),
            'feature_count': self.get_feature_count(),
            'migrations_applied': self.migrations_applied
        }


class SchemaEvolution:
    """Manage schema evolution and migrations"""
    
    def __init__(self, base_registry: FeatureRegistry, evolution_dir: str = "schema_evolution"):
        self.base_registry = base_registry
        self.evolution_dir = Path(evolution_dir)
        self.evolution_dir.mkdir(exist_ok=True)
        
        # Track versions and migrations
        self.versions: Dict[str, SchemaVersion] = {}
        self.migrations: List[Migration] = []
        self.current_version: str = "1.0.0"
        
        # Initialize with base version
        self.versions[self.current_version] = SchemaVersion(
            self.current_version, 
            base_registry
        )
        
        # Migration functions registry
        self.migration_functions: Dict[str, Callable] = {}
        
        # Load existing migrations
        self._load_migrations()
    
    def add_feature(self,
                   feature_name: str,
                   dtype: type,
                   category: str,
                   description: str = "",
                   default_value: Optional[Any] = None,
                   computation: Optional[Callable] = None,
                   min_value: Optional[float] = None,
                   max_value: Optional[float] = None,
                   allowed_values: Optional[List[Any]] = None,
                   affected_models: Optional[List[str]] = None) -> Migration:
        """Add a new feature to the schema"""
        # Create new version
        new_version = self._increment_version()
        
        # Create migration
        migration = Migration(
            version=new_version,
            migration_type=MigrationType.ADD_FEATURE,
            timestamp=datetime.now(),
            description=f"Add feature '{feature_name}'",
            feature_name=feature_name,
            new_type=dtype,
            default_value=default_value,
            computation=computation,
            is_breaking=False,  # Adding with default is not breaking
            affected_models=affected_models or []
        )
        
        # Apply migration to create new registry
        new_registry = self._copy_registry(self.base_registry)
        
        # Find next position
        max_position = max(f.position for f in new_registry.features.values())
        
        # Add feature
        new_registry.register_feature(
            name=feature_name,
            position=max_position + 1,
            dtype=dtype,
            category=category,
            description=description,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            allowed_values=allowed_values,
            is_required=False  # New features are optional for compatibility
        )
        
        # Create new version
        new_schema_version = SchemaVersion(new_version, new_registry, self.current_version)
        new_schema_version.migrations_applied.append(migration.version)
        
        # Update tracking
        self.versions[new_version] = new_schema_version
        self.migrations.append(migration)
        self.current_version = new_version
        
        # Store migration function if provided
        if computation:
            self.migration_functions[f"{new_version}_{feature_name}"] = computation
        
        logger.info(f"Added feature '{feature_name}' in version {new_version}")
        
        return migration
    
    def remove_feature(self,
                      feature_name: str,
                      rollback_computation: Optional[Callable] = None,
                      affected_models: Optional[List[str]] = None) -> Migration:
        """Remove a feature (mark as deprecated)"""
        new_version = self._increment_version()
        
        migration = Migration(
            version=new_version,
            migration_type=MigrationType.REMOVE_FEATURE,
            timestamp=datetime.now(),
            description=f"Remove feature '{feature_name}'",
            feature_name=feature_name,
            rollback_computation=rollback_computation,
            is_breaking=True,  # Removing is breaking
            affected_models=affected_models or []
        )
        
        # Note: We don't actually remove from registry, just mark deprecated
        # This maintains compatibility
        
        self.migrations.append(migration)
        logger.info(f"Marked feature '{feature_name}' for removal in version {new_version}")
        
        return migration
    
    def rename_feature(self,
                      old_name: str,
                      new_name: str,
                      affected_models: Optional[List[str]] = None) -> Migration:
        """Rename a feature"""
        new_version = self._increment_version()
        
        migration = Migration(
            version=new_version,
            migration_type=MigrationType.RENAME_FEATURE,
            timestamp=datetime.now(),
            description=f"Rename '{old_name}' to '{new_name}'",
            old_name=old_name,
            new_name=new_name,
            is_breaking=False,  # Can maintain compatibility
            affected_models=affected_models or []
        )
        
        self.migrations.append(migration)
        logger.info(f"Renamed feature '{old_name}' to '{new_name}' in version {new_version}")
        
        return migration
    
    def migrate_data(self,
                    data: Union[pd.DataFrame, Dict],
                    from_version: str,
                    to_version: str) -> Union[pd.DataFrame, Dict]:
        """Migrate data between schema versions"""
        if from_version == to_version:
            return data
        
        # Find migration path
        migrations_to_apply = self._find_migration_path(from_version, to_version)
        
        # Convert dict to dataframe for easier manipulation
        if isinstance(data, dict):
            df = pd.DataFrame([data])
            was_dict = True
        else:
            df = data.copy()
            was_dict = False
        
        # Apply migrations in sequence
        for migration in migrations_to_apply:
            df = self._apply_migration(df, migration)
        
        # Convert back to dict if needed
        if was_dict:
            return df.iloc[0].to_dict()
        return df
    
    def _apply_migration(self, df: pd.DataFrame, migration: Migration) -> pd.DataFrame:
        """Apply a single migration to data"""
        logger.info(f"Applying migration: {migration.description}")
        
        if migration.migration_type == MigrationType.ADD_FEATURE:
            # Add new feature with default or computed value
            if migration.feature_name not in df.columns:
                if migration.computation:
                    # Look up stored computation function
                    func_key = f"{migration.version}_{migration.feature_name}"
                    if func_key in self.migration_functions:
                        df[migration.feature_name] = self.migration_functions[func_key](df)
                    else:
                        df[migration.feature_name] = migration.default_value
                else:
                    df[migration.feature_name] = migration.default_value
        
        elif migration.migration_type == MigrationType.REMOVE_FEATURE:
            # Remove feature if it exists
            if migration.feature_name in df.columns:
                df = df.drop(columns=[migration.feature_name])
        
        elif migration.migration_type == MigrationType.RENAME_FEATURE:
            # Rename feature
            if migration.old_name in df.columns:
                df = df.rename(columns={migration.old_name: migration.new_name})
        
        elif migration.migration_type == MigrationType.CHANGE_TYPE:
            # Change data type
            if migration.feature_name in df.columns:
                df[migration.feature_name] = df[migration.feature_name].astype(migration.new_type)
        
        return df
    
    def _find_migration_path(self, from_version: str, to_version: str) -> List[Migration]:
        """Find migrations needed to go from one version to another"""
        # Simple implementation - assumes linear versioning
        migrations_in_range = []
        
        found_start = False
        for migration in self.migrations:
            if found_start:
                migrations_in_range.append(migration)
                if migration.version == to_version:
                    break
            elif migration.version == from_version:
                found_start = True
        
        return migrations_in_range
    
    def get_compatibility_report(self, 
                               model_contracts: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate compatibility report for models"""
        report = {
            'current_version': self.current_version,
            'total_migrations': len(self.migrations),
            'breaking_changes': [],
            'model_impacts': {}
        }
        
        # Find breaking changes
        for migration in self.migrations:
            if migration.is_breaking:
                report['breaking_changes'].append({
                    'version': migration.version,
                    'description': migration.description,
                    'affected_models': migration.affected_models
                })
        
        # Analyze model impacts
        for model_name, required_features in model_contracts.items():
            impacts = []
            for migration in self.migrations:
                if model_name in migration.affected_models:
                    impacts.append({
                        'version': migration.version,
                        'type': migration.migration_type.value,
                        'description': migration.description
                    })
            
            report['model_impacts'][model_name] = impacts
        
        return report
    
    def _increment_version(self) -> str:
        """Increment version number"""
        parts = self.current_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
    
    def _copy_registry(self, registry: FeatureRegistry) -> FeatureRegistry:
        """Create a copy of a feature registry"""
        new_registry = FeatureRegistry()
        new_registry.features = registry.features.copy()
        new_registry.version = registry.version
        return new_registry
    
    def save_migrations(self):
        """Save migrations to disk"""
        migrations_data = {
            'current_version': self.current_version,
            'migrations': [m.to_dict() for m in self.migrations],
            'versions': {v: info.to_dict() for v, info in self.versions.items()}
        }
        
        migrations_file = self.evolution_dir / "migrations.json"
        with open(migrations_file, 'w') as f:
            json.dump(migrations_data, f, indent=2)
        
        logger.info(f"Saved {len(self.migrations)} migrations to {migrations_file}")
    
    def _load_migrations(self):
        """Load migrations from disk"""
        migrations_file = self.evolution_dir / "migrations.json"
        if not migrations_file.exists():
            return
        
        with open(migrations_file, 'r') as f:
            data = json.load(f)
        
        self.current_version = data.get('current_version', '1.0.0')
        
        # Note: Cannot deserialize computation functions
        # They need to be re-registered
        logger.info(f"Loaded {len(data.get('migrations', []))} migrations")


class VersionAdapter:
    """Adapt data between different schema versions"""
    
    def __init__(self, evolution: SchemaEvolution):
        self.evolution = evolution
    
    def create_adapter(self, from_version: str, to_version: str) -> Callable:
        """Create an adapter function for version migration"""
        def adapter(data: Union[pd.DataFrame, Dict]) -> Union[pd.DataFrame, Dict]:
            return self.evolution.migrate_data(data, from_version, to_version)
        
        return adapter
    
    def create_model_adapter(self, model_version: str, current_version: str) -> Callable:
        """Create adapter for model expecting specific version"""
        def model_adapter(data: Union[pd.DataFrame, Dict]) -> Union[pd.DataFrame, Dict]:
            # First migrate to model's expected version
            adapted_data = self.evolution.migrate_data(data, current_version, model_version)
            return adapted_data
        
        return model_adapter


# Example migrations for FLASH system
def create_example_migrations():
    """Create example migrations showing how to evolve the schema"""
    
    # Initialize with base registry
    evolution = SchemaEvolution(feature_registry)
    
    # Example 1: Add a new computed feature
    evolution.add_feature(
        feature_name="ltv_cac_ratio",
        dtype=float,
        category="market",
        description="LTV/CAC ratio",
        computation=lambda df: df['customer_lifetime_value'] / df['customer_acquisition_cost'].replace(0, 1),
        default_value=3.0,
        min_value=0,
        max_value=100,
        affected_models=['dna_analyzer', 'temporal_model']
    )
    
    # Example 2: Add ML readiness score
    evolution.add_feature(
        feature_name="ml_readiness_score",
        dtype=int,
        category="advantage",
        description="ML/AI readiness score",
        default_value=3,
        min_value=1,
        max_value=5,
        allowed_values=[1, 2, 3, 4, 5],
        affected_models=['industry_model']
    )
    
    # Example 3: Rename feature for clarity
    evolution.rename_feature(
        old_name="runway_months",
        new_name="cash_runway_months",
        affected_models=['dna_analyzer', 'temporal_model', 'industry_model']
    )
    
    # Save migrations
    evolution.save_migrations()
    
    return evolution


if __name__ == "__main__":
    # Example usage
    evolution = create_example_migrations()
    
    # Generate compatibility report
    model_contracts = {
        'dna_analyzer': ['all features'],
        'temporal_model': ['all features'],
        'industry_model': ['all features']
    }
    
    report = evolution.get_compatibility_report(model_contracts)
    print(json.dumps(report, indent=2))