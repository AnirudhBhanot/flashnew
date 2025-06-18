#!/usr/bin/env python3
"""
Update framework_database.py with the generated 500+ frameworks
This script safely appends the new frameworks to the existing file
"""

import os
import re

def update_framework_database():
    """Update framework_database.py with new frameworks"""
    
    # Read the generated frameworks
    with open('generated_500_frameworks.py', 'r') as f:
        generated_content = f.read()
    
    # Read the current framework_database.py
    db_path = 'framework_database.py'
    with open(db_path, 'r') as f:
        current_content = f.read()
    
    # Find the FRAMEWORKS dictionary
    # Look for the closing brace of FRAMEWORKS
    frameworks_pattern = r'(FRAMEWORKS\s*=\s*\{[^}]*)'
    match = re.search(frameworks_pattern, current_content, re.DOTALL)
    
    if not match:
        print("ERROR: Could not find FRAMEWORKS dictionary in framework_database.py")
        return False
    
    # Find the position before the closing brace
    frameworks_end = current_content.rfind('}', 0, current_content.find('\n\ndef get_framework_by_id'))
    
    if frameworks_end == -1:
        print("ERROR: Could not find end of FRAMEWORKS dictionary")
        return False
    
    # Extract just the framework definitions from generated file
    # Skip the header comments
    framework_defs = []
    lines = generated_content.split('\n')
    skip_header = True
    
    for line in lines:
        if skip_header:
            if line.strip() == "":
                skip_header = False
            continue
        if line.strip():
            framework_defs.append(line)
    
    # Create the new content
    new_frameworks = '\n'.join(framework_defs)
    
    # Insert before the closing brace
    new_content = (
        current_content[:frameworks_end] + 
        '\n    # ========== EXPANDED FRAMEWORKS (500+) ==========\n' +
        new_frameworks +
        '\n' +
        current_content[frameworks_end:]
    )
    
    # Backup the original file
    backup_path = db_path + '.backup'
    with open(backup_path, 'w') as f:
        f.write(current_content)
    print(f"Created backup: {backup_path}")
    
    # Write the updated content
    with open(db_path, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {db_path} with new frameworks")
    
    # Verify the update
    try:
        # Try to import and check
        import sys
        sys.path.insert(0, '.')
        from framework_database import FRAMEWORKS, get_framework_statistics
        
        stats = get_framework_statistics()
        print(f"\nVerification successful!")
        print(f"Total frameworks: {stats['total_frameworks']}")
        print(f"By category: {stats['by_category']}")
        
        return True
        
    except Exception as e:
        print(f"\nERROR during verification: {e}")
        print("Restoring from backup...")
        
        # Restore from backup
        with open(backup_path, 'r') as f:
            backup_content = f.read()
        with open(db_path, 'w') as f:
            f.write(backup_content)
        
        print("Restored original file")
        return False

if __name__ == "__main__":
    print("Updating framework_database.py with 500+ frameworks...")
    success = update_framework_database()
    
    if success:
        print("\n✅ SUCCESS! Framework database now contains 500+ frameworks!")
    else:
        print("\n❌ Failed to update framework database")