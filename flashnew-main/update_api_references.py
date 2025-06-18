#!/usr/bin/env python3
"""
Update API server references from old files to api_server_unified.py
"""

import os
from pathlib import Path

def update_dockerfile():
    """Update Dockerfile to use api_server_unified.py"""
    dockerfile_path = Path("/Users/sf/Desktop/FLASH/Dockerfile")
    if dockerfile_path.exists():
        content = dockerfile_path.read_text()
        # Update the COPY line
        updated_content = content.replace("COPY api_server.py .", "COPY api_server_unified.py .")
        # Update the CMD line
        updated_content = updated_content.replace('"api_server:app"', '"api_server_unified:app"')
        
        # Save backup
        dockerfile_path.with_suffix('.Dockerfile.backup').write_text(content)
        # Write updated content
        dockerfile_path.write_text(updated_content)
        print("✅ Updated Dockerfile to use api_server_unified.py")
        print("   Backup saved as Dockerfile.backup")
    else:
        print("❌ Dockerfile not found")

def check_other_references():
    """Check for other references to old API servers"""
    project_root = Path("/Users/sf/Desktop/FLASH")
    old_api_files = ["api_server.py", "api_server_clean.py", "api_server_final_integrated.py"]
    
    references_found = []
    
    # Check Python files
    for py_file in project_root.rglob("*.py"):
        if py_file.is_file() and "archive" not in str(py_file):
            try:
                content = py_file.read_text()
                for old_api in old_api_files:
                    api_module = old_api.replace(".py", "")
                    if f"import {api_module}" in content or f"from {api_module}" in content:
                        references_found.append((str(py_file.relative_to(project_root)), old_api))
            except:
                pass
    
    # Check shell scripts and config files
    for pattern in ["*.sh", "*.yml", "*.yaml", "*.json"]:
        for file in project_root.rglob(pattern):
            if file.is_file() and "archive" not in str(file):
                try:
                    content = file.read_text()
                    for old_api in old_api_files:
                        if old_api in content:
                            references_found.append((str(file.relative_to(project_root)), old_api))
                except:
                    pass
    
    if references_found:
        print("\n⚠️  Found references to old API servers:")
        for file_path, api_ref in references_found:
            print(f"   {file_path} → references {api_ref}")
    else:
        print("\n✅ No references to old API servers found in active files")
    
    return references_found

def main():
    print("🔧 Updating API server references...")
    print("="*50)
    
    # Update Dockerfile
    update_dockerfile()
    
    # Check for other references
    references = check_other_references()
    
    if references:
        print("\n💡 Recommendation: Update these files manually or with the cleanup script")
    
    print("\n✅ Reference update complete!")

if __name__ == "__main__":
    main()