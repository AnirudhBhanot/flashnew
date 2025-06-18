#!/usr/bin/env python3
"""
Fix for Phase 2 timeout issue in Michelin Analysis
Adds proper timeout configuration to aiohttp session
"""

import os
import shutil
from datetime import datetime

# Backup the original file
original_file = "api_michelin_decomposed.py"
backup_file = f"api_michelin_decomposed_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"

print(f"Creating backup: {backup_file}")
shutil.copy(original_file, backup_file)

# Read the original file
with open(original_file, 'r') as f:
    content = f.read()

# Replace the session creation line to add timeout
old_line = "            self.session = aiohttp.ClientSession()"
new_line = """            timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
            logger.info("Created aiohttp session with 60s timeout")"""

if old_line in content:
    content = content.replace(old_line, new_line)
    print("✅ Added timeout configuration to aiohttp session")
else:
    print("❌ Could not find the session creation line")
    exit(1)

# Also update the _call_deepseek method to add explicit timeout
old_deepseek = "async with self.session.post(DEEPSEEK_API_URL, json=payload, headers=headers) as response:"
new_deepseek = """async with self.session.post(
                DEEPSEEK_API_URL, 
                json=payload, 
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:"""

if old_deepseek in content:
    content = content.replace(old_deepseek, new_deepseek)
    print("✅ Added explicit timeout to DeepSeek API calls")

# Write the updated content
with open(original_file, 'w') as f:
    f.write(content)

print(f"\n✅ Fixed timeout issues in {original_file}")
print("\nChanges made:")
print("1. Added 60-second total timeout to aiohttp ClientSession")
print("2. Added 30-second timeout to individual DeepSeek API calls")
print("\nNext steps:")
print("1. Restart the API server")
print("2. Test Phase 2 again")
print(f"\nBackup saved as: {backup_file}")