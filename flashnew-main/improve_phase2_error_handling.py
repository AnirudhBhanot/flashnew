#!/usr/bin/env python3
"""
Improve error handling in Phase 2 to provide better diagnostics
"""

import re

# Read the current file
with open("api_michelin_decomposed.py", 'r') as f:
    content = f.read()

# Add import for traceback at the top if not already present
if "import traceback" not in content:
    # Find the imports section and add traceback
    import_pattern = r'(import asyncio\nimport re)'
    replacement = r'\1\nimport traceback'
    content = re.sub(import_pattern, replacement, content)
    print("✅ Added traceback import")

# Improve the analyze_phase2 exception handling
old_except = """        except Exception as e:
            logger.error(f"Decomposed Phase 2 analysis failed: {e}")
            raise"""

new_except = """        except asyncio.TimeoutError:
            logger.error(f"Phase 2 analysis timed out for {startup_data.startup_name}")
            raise Exception("Phase 2 analysis timed out - DeepSeek API may be slow")
        except Exception as e:
            logger.error(f"Decomposed Phase 2 analysis failed: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise"""

if old_except in content:
    content = content.replace(old_except, new_except)
    print("✅ Improved error handling in analyze_phase2")

# Improve error messages in API calls
old_bare_except = """        except:
            # Fallback"""

# Find all occurrences and replace with better error handling
import_added = False
for match in re.finditer(r'        except:\n            # Fallback', content):
    if not import_added:
        # Need to add traceback import if not done already
        if "import traceback" not in content:
            content = content.replace("import re", "import re\nimport traceback")
        import_added = True

# Replace bare except clauses with more informative ones
content = re.sub(
    r'(        )except:\n(            # Fallback)',
    r'\1except Exception as e:\n\1    logger.debug(f"Falling back to default: {e}")\n\2',
    content
)
print("✅ Replaced bare except clauses with logged exceptions")

# Write the updated content
with open("api_michelin_decomposed.py", 'w') as f:
    f.write(content)

print("\n✅ Improved error handling in api_michelin_decomposed.py")
print("\nImprovements made:")
print("1. Added timeout-specific error handling")
print("2. Added traceback logging for debugging")
print("3. Replaced bare except clauses with logged exceptions")
print("\nThis will help identify the specific cause of Phase 2 failures.")