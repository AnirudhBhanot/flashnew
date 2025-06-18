#!/usr/bin/env python3
"""
Fix import statements in test files after reorganization
"""

import os
from pathlib import Path

def fix_test_imports():
    """Update import statements in test files"""
    tests_dir = Path("/Users/sf/Desktop/FLASH/tests")
    
    # Common import replacements
    replacements = {
        "from api_server import": "from api_server_unified import",
        "import api_server": "import api_server_unified",
        "from unified_orchestrator import": "from models.unified_orchestrator_v3_integrated import",
        "import unified_orchestrator": "import models.unified_orchestrator_v3_integrated as unified_orchestrator",
    }
    
    fixed_files = []
    
    for test_file in tests_dir.glob("test_*.py"):
        if test_file.is_file():
            content = test_file.read_text()
            original_content = content
            
            # Apply replacements
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            # Fix relative imports that might need adjustment
            if "../" in content:
                # Tests are now in tests/ so need to go up one more level
                content = content.replace("from ..", "from ../..")
                content = content.replace("sys.path.append('..')", "sys.path.append('../..')")
                content = content.replace('sys.path.append("..")', 'sys.path.append("../..")')
                
            if content != original_content:
                test_file.write_text(content)
                fixed_files.append(test_file.name)
                print(f"✅ Fixed imports in: {test_file.name}")
    
    # Also fix conftest.py if it exists
    conftest = tests_dir / "conftest.py"
    if conftest.exists():
        content = conftest.read_text()
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if content != original_content:
            conftest.write_text(content)
            fixed_files.append("conftest.py")
            print(f"✅ Fixed imports in: conftest.py")
    
    return fixed_files

def main():
    print("🔧 Fixing test imports after reorganization...")
    print("="*50)
    
    fixed = fix_test_imports()
    
    if fixed:
        print(f"\n✅ Fixed {len(fixed)} files")
        print("\n💡 Next steps:")
        print("   1. Run a test to verify imports work:")
        print("      cd /Users/sf/Desktop/FLASH && python3 -m pytest tests/test_calculations.py -v")
        print("   2. Update any remaining import errors as needed")
    else:
        print("\n✅ No import changes needed")

if __name__ == "__main__":
    main()