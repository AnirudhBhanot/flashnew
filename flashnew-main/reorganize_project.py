#!/usr/bin/env python3
"""
Reorganize FLASH project structure
Moves files from root to appropriate directories
"""

import os
import shutil
from pathlib import Path
import re

# Define file mappings
FILE_MAPPINGS = {
    # API related files
    'api_*.py': 'src/api/',
    'api_server*.py': 'src/api/',
    'frontend_models.py': 'src/api/models/',
    'response_transformer.py': 'src/api/transformers/',
    
    # Core business logic
    'feature_*.py': 'src/core/',
    'camp_*.py': 'src/core/',
    'type_converter*.py': 'src/core/converters/',
    'financial_calculator.py': 'src/core/calculators/',
    
    # ML/Models
    'train_*.py': 'src/ml/training/',
    'model_*.py': 'src/ml/',
    'dna_*.py': 'src/ml/',
    'temporal_*.py': 'src/ml/',
    'industry_*.py': 'src/ml/',
    'pattern_*.py': 'src/ml/patterns/',
    'ensemble_*.py': 'src/ml/',
    
    # Services
    'monitoring/*.py': 'src/services/monitoring/',
    'security/*.py': 'src/services/security/',
    'production_*.py': 'src/services/',
    
    # Utils
    'utils/*.py': 'src/utils/',
    'safe_math.py': 'src/utils/',
    'probability_utils.py': 'src/utils/',
    
    # Tests
    'test_*.py': 'tests/unit/',
    'tests/test_*.py': 'tests/unit/',
    
    # Scripts
    'fix_*.py': 'scripts/fixes/',
    'analyze_*.py': 'scripts/analysis/',
    'create_*.py': 'scripts/setup/',
    'validate_*.py': 'scripts/validation/',
    'debug_*.py': 'scripts/debug/',
    'run_*.py': 'scripts/',
    
    # Documentation
    '*.md': 'docs/',
    'API_*.md': 'docs/api/',
    'TECHNICAL_*.md': 'docs/technical/',
}

def get_destination(file_path: str) -> str:
    """Determine destination directory for a file"""
    file_name = os.path.basename(file_path)
    
    # Check exact patterns first
    for pattern, dest in FILE_MAPPINGS.items():
        if '*' in pattern:
            # Convert glob pattern to regex
            regex_pattern = pattern.replace('*', '.*')
            if re.match(regex_pattern, file_name):
                return dest
        elif file_name == pattern:
            return dest
    
    # Default destinations by file type
    if file_name.endswith('.py'):
        if 'test' in file_name:
            return 'tests/unit/'
        elif file_name.startswith(('train_', 'retrain_')):
            return 'src/ml/training/'
        else:
            return 'src/core/'
    elif file_name.endswith('.md'):
        return 'docs/'
    elif file_name.endswith('.json'):
        return 'data/config/'
    elif file_name.endswith('.pkl'):
        return 'models/'
    
    return None


def should_move(file_path: str) -> bool:
    """Check if file should be moved"""
    file_name = os.path.basename(file_path)
    
    # Don't move these files
    keep_in_root = {
        'api_server_unified.py',  # Main API server
        'config.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        '.env',
        '.env.example',
        '.gitignore',
        'README.md',
        'alembic.ini',
        'setup.py',
        'pyproject.toml',
    }
    
    # Don't move directories
    if os.path.isdir(file_path):
        return False
    
    # Don't move if in keep list
    if file_name in keep_in_root:
        return False
    
    # Don't move if already in organized directory
    organized_dirs = {'src', 'tests', 'scripts', 'docs', 'models', 'data', 'migrations', 'database', 'flash-frontend'}
    parts = Path(file_path).parts
    if any(d in parts for d in organized_dirs):
        return False
    
    return True


def reorganize_project(dry_run: bool = True):
    """Reorganize project files"""
    root_dir = Path.cwd()
    moves = []
    
    # Find all Python files in root
    for file_path in root_dir.glob('*.py'):
        if should_move(str(file_path)):
            dest_dir = get_destination(str(file_path))
            if dest_dir:
                dest_path = root_dir / dest_dir / file_path.name
                moves.append((file_path, dest_path))
    
    # Find all markdown files in root
    for file_path in root_dir.glob('*.md'):
        if should_move(str(file_path)) and file_path.name != 'README.md':
            dest_dir = get_destination(str(file_path))
            if dest_dir:
                dest_path = root_dir / dest_dir / file_path.name
                moves.append((file_path, dest_path))
    
    # Print plan
    print(f"Found {len(moves)} files to move:")
    print("=" * 60)
    
    for src, dest in sorted(moves):
        print(f"{src.name:40} -> {dest.parent.relative_to(root_dir)}/")
    
    if dry_run:
        print("\nDRY RUN - No files moved. Run with --execute to perform moves.")
        return
    
    # Execute moves
    print("\nExecuting moves...")
    for src, dest in moves:
        # Create destination directory
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        try:
            shutil.move(str(src), str(dest))
            print(f"✓ Moved {src.name}")
        except Exception as e:
            print(f"✗ Failed to move {src.name}: {e}")
    
    print(f"\n✅ Reorganization complete! Moved {len(moves)} files.")
    
    # Create __init__.py files
    print("\nCreating __init__.py files...")
    for dir_path in root_dir.glob('src/**'):
        if dir_path.is_dir():
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                print(f"✓ Created {init_file.relative_to(root_dir)}")


if __name__ == "__main__":
    import sys
    
    dry_run = '--execute' not in sys.argv
    reorganize_project(dry_run=dry_run)