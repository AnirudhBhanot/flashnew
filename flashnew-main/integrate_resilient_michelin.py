"""
Script to integrate the resilient Michelin API into the main API server
"""

import os
import shutil
from pathlib import Path

def integrate_resilient_michelin():
    """Integrate the resilient Michelin endpoints into api_server_unified.py"""
    
    # Read the current api_server_unified.py
    api_server_path = Path("/Users/sf/Desktop/FLASH/api_server_unified.py")
    with open(api_server_path, 'r') as f:
        lines = f.readlines()
    
    # Find where to insert the import
    import_insert_line = None
    for i, line in enumerate(lines):
        if "from api_framework_intelligent import" in line:
            import_insert_line = i + 1
            break
    
    if import_insert_line is None:
        print("Could not find import location")
        return
    
    # Add the resilient Michelin import
    import_statement = "from api_michelin_resilient import router as michelin_resilient_router\n"
    if import_statement not in lines:
        lines.insert(import_insert_line, import_statement)
    
    # Find where routers are included (after app creation)
    router_insert_line = None
    for i, line in enumerate(lines):
        if "app.include_router(auth_router)" in line:
            # Find the last router inclusion
            for j in range(i, len(lines)):
                if "app.include_router" in lines[j]:
                    router_insert_line = j + 1
                else:
                    break
    
    if router_insert_line is None:
        print("Could not find router inclusion location")
        return
    
    # Add the resilient router
    router_statement = "app.include_router(michelin_resilient_router)\n"
    if router_statement not in lines:
        lines.insert(router_insert_line, router_statement)
    
    # Backup the original file
    backup_path = api_server_path.with_suffix('.py.backup_before_resilience')
    shutil.copy(api_server_path, backup_path)
    print(f"Created backup: {backup_path}")
    
    # Write the modified file
    with open(api_server_path, 'w') as f:
        f.writelines(lines)
    
    print("✅ Successfully integrated resilient Michelin API")
    print("\nNew endpoints added:")
    print("  - POST /api/michelin-resilient/analyze/phase1")
    print("  - POST /api/michelin-resilient/analyze/phase2")
    print("  - POST /api/michelin-resilient/analyze/complete")
    print("  - GET  /api/michelin-resilient/health")
    print("\nTo test the resilient system:")
    print("  1. Restart the API server: python api_server_unified.py")
    print("  2. Run the test suite: python test_resilience_patterns.py")
    print("\nThe resilient API includes:")
    print("  - Circuit breaker pattern (prevents cascading failures)")
    print("  - Exponential backoff with jitter (smart retries)")
    print("  - Request hedging (backup requests for slow responses)")
    print("  - Graceful degradation (partial results on failure)")
    print("  - Adaptive timeouts (learns from performance)")

if __name__ == "__main__":
    integrate_resilient_michelin()