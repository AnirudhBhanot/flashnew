#!/usr/bin/env python3
"""
Fix all import errors in framework-related API files
"""

import os
import re

def fix_framework_imports():
    """Fix all relative imports in framework API files"""
    
    # List of files to fix
    api_files = [
        'api_framework_endpoints.py',
        'api_framework_implementation.py',
        'api_framework_adapter.py',
        'api_framework_analysis.py',
        'api_framework_analysis_endpoints.py',
        'api_framework_deep_analysis.py'
    ]
    
    fixes_applied = []
    
    for filename in api_files:
        filepath = f"/Users/sf/Desktop/FLASH/{filename}"
        if not os.path.exists(filepath):
            print(f"Skipping {filename} - not found")
            continue
            
        print(f"\nFixing {filename}...")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Replace relative imports with absolute imports
        # from .framework_selector -> from framework_intelligence.framework_selector
        content = re.sub(
            r'from\s+\.(\w+)\s+import',
            r'from framework_intelligence.\1 import',
            content
        )
        
        # Fix 2: Fix framework_database imports
        # from framework_database import FRAMEWORKS as FRAMEWORK_DATABASE
        # -> from framework_intelligence.framework_database import FRAMEWORKS
        content = re.sub(
            r'from framework_database import',
            r'from framework_intelligence.framework_database import',
            content
        )
        
        content = re.sub(
            r'from framework_selector import',
            r'from framework_intelligence.framework_selector import',
            content
        )
        
        # Fix 3: Fix FRAMEWORK_DATABASE references
        # FRAMEWORK_DATABASE -> FRAMEWORKS
        if 'FRAMEWORK_DATABASE' in content and 'FRAMEWORKS as FRAMEWORK_DATABASE' not in content:
            content = content.replace('FRAMEWORK_DATABASE', 'FRAMEWORKS')
        
        # Fix 4: Remove sys.path manipulations that cause issues
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
                
            # Skip problematic sys.path manipulations
            if 'sys.path.insert' in line and 'framework_dir' in line:
                continue
            elif 'framework_dir = ' in line and 'framework_intelligence' in line:
                continue
            elif line.strip() == 'sys.path.insert(0, framework_dir)':
                continue
            elif line.strip() == 'sys.path.insert(0, current_dir)':
                continue
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Fix 5: Ensure proper imports at the top
        if 'from framework_intelligence' not in content and ('FrameworkSelector' in content or 'FRAMEWORKS' in content):
            # Find where imports are
            import_section_end = 0
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith(('import ', 'from ', '#', '"""', "'''")) and i > 10:
                    import_section_end = i
                    break
            
            # Add the imports
            framework_imports = """
# Framework intelligence imports
from framework_intelligence.framework_selector import (
    FrameworkSelector, StartupContext, BusinessStage, 
    IndustryType, ChallengeType
)
from framework_intelligence.framework_database import (
    FRAMEWORKS, Framework, FrameworkCategory, ComplexityLevel,
    get_framework_by_id, get_frameworks_by_category
)
"""
            lines.insert(import_section_end, framework_imports)
            content = '\n'.join(lines)
        
        # Fix 6: Fix specific errors in each file
        if filename == 'api_framework_implementation.py':
            # Fix FRAMEWORK_DATABASE reference
            content = content.replace(
                'from framework_intelligence.framework_database import FRAMEWORK_DATABASE',
                'from framework_intelligence.framework_database import FRAMEWORKS'
            )
            content = content.replace('FRAMEWORK_DATABASE[', 'FRAMEWORKS[')
            
        if filename == 'api_framework_adapter.py':
            # Ensure it has proper imports
            if 'from framework_intelligence.framework_selector import FrameworkSelector' not in content:
                content = content.replace(
                    'from framework_selector import FrameworkSelector',
                    'from framework_intelligence.framework_selector import FrameworkSelector'
                )
        
        # Fix 7: Fix get_framework calls
        content = content.replace(
            'db.get_framework(',
            'get_framework_by_id('
        )
        
        # Fix 8: Remove duplicate imports
        lines = content.split('\n')
        seen_imports = set()
        new_lines = []
        
        for line in lines:
            if line.strip().startswith(('from framework_intelligence', 'import framework_intelligence')):
                if line.strip() not in seen_imports:
                    seen_imports.add(line.strip())
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            fixes_applied.append(filename)
            print(f"✅ Fixed imports in {filename}")
        else:
            print(f"ℹ️  No changes needed in {filename}")
    
    # Fix the enhanced_framework_selector imports
    enhanced_selector_path = "/Users/sf/Desktop/FLASH/framework_intelligence/enhanced_framework_selector.py"
    if os.path.exists(enhanced_selector_path):
        print(f"\nFixing enhanced_framework_selector.py...")
        with open(enhanced_selector_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix relative imports
        content = content.replace(
            'from .framework_database import',
            'from framework_intelligence.framework_database import'
        )
        content = content.replace(
            'from .framework_selector import',
            'from framework_intelligence.framework_selector import'
        )
        
        # For imports within the same package, we can use relative imports
        content = content.replace(
            'from framework_intelligence.framework_database import',
            'from .framework_database import'
        )
        content = content.replace(
            'from framework_intelligence.framework_selector import',
            'from .framework_selector import'
        )
        
        if content != original_content:
            with open(enhanced_selector_path, 'w') as f:
                f.write(content)
            print("✅ Fixed imports in enhanced_framework_selector.py")
    
    print(f"\n🎉 Fixed imports in {len(fixes_applied)} files")
    return fixes_applied

if __name__ == "__main__":
    fixed_files = fix_framework_imports()
    print("\nFixed files:")
    for f in fixed_files:
        print(f"  - {f}")