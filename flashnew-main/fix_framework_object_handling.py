#!/usr/bin/env python3
"""
Fix Framework database object handling issues
"""

import os
import re

def fix_framework_object_handling():
    """Fix all framework object handling issues"""
    
    fixes_applied = []
    
    # List of files to fix
    files_to_fix = [
        'api_framework_intelligent.py',
        'api_framework_intelligent_enhanced.py',
        'api_framework_endpoints.py',
        'api_framework_implementation.py',
        'api_framework_adapter.py'
    ]
    
    for filename in files_to_fix:
        filepath = f"/Users/sf/Desktop/FLASH/{filename}"
        if not os.path.exists(filepath):
            continue
            
        print(f"\nFixing {filename}...")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        original_content = content
        fixes_for_file = []
        
        # Fix 1: Replace framework['name'] with proper attribute access
        if "framework['name']" in content:
            content = content.replace("framework['name']", "framework.name if hasattr(framework, 'name') else framework.get('name', '')")
            fixes_for_file.append("framework['name'] access")
        
        # Fix 2: Replace framework['id'] with proper attribute access
        if "framework['id']" in content:
            content = content.replace("framework['id']", "framework.id if hasattr(framework, 'id') else framework.get('id', '')")
            fixes_for_file.append("framework['id'] access")
        
        # Fix 3: Replace framework.get() calls with proper attribute access
        # Pattern: framework.get('attribute')
        pattern = r'framework\.get\([\'"](\w+)[\'"]\)'
        def replace_get(match):
            attr = match.group(1)
            return f"getattr(framework, '{attr}', None) if hasattr(framework, '{attr}') else framework.get('{attr}') if isinstance(framework, dict) else None"
        
        new_content = re.sub(pattern, replace_get, content)
        if new_content != content:
            content = new_content
            fixes_for_file.append("framework.get() calls")
        
        # Fix 4: Add helper function for safe framework access
        if 'def get_framework_attr(' not in content and len(fixes_for_file) > 0:
            # Add helper function after imports
            helper_function = '''
def get_framework_attr(framework, attr_name, default=None):
    """Safely get attribute from framework object or dict"""
    if hasattr(framework, attr_name):
        return getattr(framework, attr_name)
    elif isinstance(framework, dict):
        return framework.get(attr_name, default)
    return default
'''
            # Find a good place to insert (after imports, before first function/class)
            import_end = 0
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith(('import ', 'from ', '#')) and i > 10:
                    import_end = i
                    break
            
            lines.insert(import_end, helper_function)
            content = '\n'.join(lines)
            fixes_for_file.append("Added get_framework_attr helper")
        
        # Fix 5: Fix specific patterns in api_framework_intelligent.py
        if filename == 'api_framework_intelligent.py':
            # Fix the specific line causing issues
            content = content.replace(
                "framework['name'],",
                "get_framework_attr(framework, 'name', framework_name),"
            )
            
            # Fix framework database access
            content = content.replace(
                "framework = framework_database.get_framework_by_id(framework_id)",
                "framework = framework_database.get_framework_by_id(framework_id) if hasattr(framework_database, 'get_framework_by_id') else framework_database.FRAMEWORKS.get(framework_id)"
            )
        
        # Fix 6: Ensure consistent framework iteration
        # Pattern: for framework_id, framework in FRAMEWORKS.items()
        if 'for framework_id, framework in' in content:
            # Make sure we handle both dict and dataclass frameworks
            pattern = r'for framework_id, framework in ([^:]+):'
            def fix_iteration(match):
                source = match.group(1).strip()
                return f'for framework_id, framework in {source}:'
            
            content = re.sub(pattern, fix_iteration, content)
        
        # Write updated content if changes were made
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            fixes_applied.append(f"{filename}: {', '.join(fixes_for_file)}")
            print(f"✅ Fixed {len(fixes_for_file)} issues")
        else:
            print(f"ℹ️  No changes needed")
    
    # Fix framework_database.py to ensure consistent interface
    db_file = "/Users/sf/Desktop/FLASH/framework_intelligence/framework_database.py"
    if os.path.exists(db_file):
        print(f"\nChecking {os.path.basename(db_file)}...")
        
        with open(db_file, 'r') as f:
            db_content = f.read()
        
        # Ensure get_framework_by_id returns consistent type
        if 'def get_framework_by_id(' in db_content and 'return FRAMEWORKS.get(framework_id)' in db_content:
            # Already returns Framework objects
            print("✅ framework_database already returns Framework objects")
        else:
            print("⚠️  framework_database may need updates for consistent returns")
    
    return fixes_applied

if __name__ == "__main__":
    fixed = fix_framework_object_handling()
    
    print(f"\n🎉 Framework object handling fixes complete!")
    print(f"Fixed {len(fixed)} files:")
    for fix in fixed:
        print(f"  - {fix}")