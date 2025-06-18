#!/usr/bin/env python3
"""
Clean up old API server and orchestrator versions
Archives old files and updates references
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Files to archive (not delete, for safety)
OLD_FILES = [
    'api_server.py',
    'api_server_v2.py', 
    'api_server_backup.py',
    'api_server_with_monitoring.py',
    'models/unified_orchestrator.py',
    'models/unified_orchestrator_v2.py'
]

# Create archive directory
ARCHIVE_DIR = Path('archive/old_versions')
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def archive_old_files():
    """Move old files to archive directory"""
    archived = []
    
    for file_path in OLD_FILES:
        src = Path(file_path)
        if src.exists():
            dst = ARCHIVE_DIR / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.move(str(src), str(dst))
                logger.info(f"Archived: {file_path} -> {dst}")
                archived.append(file_path)
            except Exception as e:
                logger.error(f"Failed to archive {file_path}: {e}")
    
    return archived

def create_symlinks():
    """Create symlinks for backward compatibility"""
    symlinks = {
        'api_server.py': 'api_server_final.py',
        'models/unified_orchestrator.py': 'models/unified_orchestrator_v3.py'
    }
    
    for link_name, target in symlinks.items():
        link_path = Path(link_name)
        target_path = Path(target)
        
        if not link_path.exists() and target_path.exists():
            try:
                link_path.symlink_to(target_path.name)
                logger.info(f"Created symlink: {link_name} -> {target}")
            except Exception as e:
                logger.error(f"Failed to create symlink {link_name}: {e}")

def update_documentation():
    """Create migration documentation"""
    migration_doc = """# API Migration Guide

## Overview
The FLASH API has been consolidated into a single, unified version that integrates:
- All 45 canonical features
- Hierarchical pattern system (31 active patterns)
- Enhanced validation and error handling
- Comprehensive API endpoints

## Migration Steps

### 1. Update API Server
Replace references to old API servers:
- `api_server.py` → `api_server_final.py`
- `api_server_v2.py` → `api_server_final.py`

### 2. Update Imports
```python
# Old
from models.unified_orchestrator import UnifiedModelOrchestrator

# New
from models.unified_orchestrator_v3 import get_orchestrator
```

### 3. Feature Configuration
All features are now centralized in `feature_config.py`:
```python
from feature_config import ALL_FEATURES, validate_features
```

### 4. API Endpoints
The final API includes all endpoints:
- `/predict` - Enhanced predictions with patterns
- `/analyze` - Detailed analysis
- `/patterns` - Pattern management
- `/features` - Feature documentation

### 5. Running the Server
```bash
# Start the final API server
python3 api_server_final.py

# Default port: 8001
# Health check: http://localhost:8001/health
```

## Archived Files
Old versions have been moved to `archive/old_versions/` for reference.

## Feature Count
The system now uses exactly 45 features as defined in the dataset:
- Capital: 7 features
- Advantage: 8 features  
- Market: 11 features
- People: 10 features
- Product: 9 features

Total: 45 features
"""
    
    with open('MIGRATION_GUIDE.md', 'w') as f:
        f.write(migration_doc)
    
    logger.info("Created MIGRATION_GUIDE.md")

def main():
    """Run cleanup process"""
    logger.info("Starting cleanup of old versions...")
    
    # Archive old files
    archived = archive_old_files()
    logger.info(f"Archived {len(archived)} files")
    
    # Create symlinks for compatibility
    create_symlinks()
    
    # Update documentation
    update_documentation()
    
    logger.info("\nCleanup complete!")
    logger.info("- Old files archived to: archive/old_versions/")
    logger.info("- Created symlinks for backward compatibility")
    logger.info("- Migration guide: MIGRATION_GUIDE.md")
    logger.info("\nUse api_server_final.py as the main API server")

if __name__ == "__main__":
    main()