#!/usr/bin/env python3
"""
Clean up API server versions
Archives old versions and sets up the unified server
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_api_servers():
    """Archive old API server versions and set up unified server"""
    
    # Create archive directory
    archive_dir = Path('archive/api_servers')
    archive_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created archive directory: {archive_dir}")
    
    # Files to archive
    old_versions = [
        'api_server_v3.py',
        'api_server_final.py'
    ]
    
    # Archive old versions
    for old_file in old_versions:
        if Path(old_file).exists():
            shutil.move(old_file, archive_dir / old_file)
            logger.info(f"Archived {old_file}")
    
    # Remove old symlink
    if Path('api_server.py').is_symlink():
        os.unlink('api_server.py')
        logger.info("Removed old symlink")
    
    # Create new symlink to unified server
    os.symlink('api_server_unified.py', 'api_server.py')
    logger.info("Created symlink: api_server.py -> api_server_unified.py")
    
    # Create a documentation file
    doc_content = """# API Server Architecture

## Current Structure (After Cleanup)

- `api_server.py` -> Symlink to `api_server_unified.py`
- `api_server_unified.py` -> Main unified API server with feature alignment

## Archived Versions

The following API server versions have been archived to `archive/api_servers/`:
- `api_server_v3.py` - Previous version 3
- `api_server_final.py` - Previous "final" version

## Key Improvements in Unified Server

1. **Feature Alignment**: Automatically handles models expecting different feature counts
2. **Consolidated Code**: Single source of truth for API logic
3. **Better Error Handling**: Comprehensive error messages and logging
4. **Pattern Integration**: Seamless pattern system integration
5. **Model Management**: Centralized model loading and prediction

## Usage

```bash
# Start the API server
python api_server.py

# Or directly
python api_server_unified.py
```

The server runs on port 8001 by default.
"""
    
    with open('API_SERVER_ARCHITECTURE.md', 'w') as f:
        f.write(doc_content)
    logger.info("Created API_SERVER_ARCHITECTURE.md")
    
    # Update imports in other files
    files_to_check = [
        'test_api.py',
        'test_pattern_api.py',
        'run_tests.py'
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            logger.info(f"Note: Check {file_path} for import updates if needed")
    
    logger.info("\nCleanup complete!")
    logger.info("Next steps:")
    logger.info("1. Test the unified API server: python api_server.py")
    logger.info("2. Update any test files that import specific API versions")
    logger.info("3. Update documentation to reference the unified server")

if __name__ == "__main__":
    cleanup_api_servers()