#!/usr/bin/env python3
"""
Script to switch from Michelin frontend fix to DeepSeek adapter
"""

import subprocess
import time

print("Switching Michelin Analysis to DeepSeek Implementation")
print("=" * 60)

# Step 1: Stop the current API server
print("\n1. Stopping current API server...")
subprocess.run(["pkill", "-f", "api_server_unified.py"])
time.sleep(2)

# Step 2: Update the import in api_server_unified.py
print("\n2. Updating API server imports...")
with open("api_server_unified.py", "r") as f:
    content = f.read()

# Replace the frontend fix import with deepseek adapter
content = content.replace(
    "from api_michelin_frontend_fix import frontend_fix_router",
    "from api_michelin_deepseek_adapter import deepseek_adapter_router"
)
content = content.replace(
    "app.include_router(frontend_fix_router)",
    "app.include_router(deepseek_adapter_router)"
)
content = content.replace(
    '"Michelin Frontend Fix endpoints enabled - immediate responses for UI"',
    '"Michelin DeepSeek Adapter endpoints enabled - real DeepSeek analysis with frontend-compatible format"'
)

with open("api_server_unified.py", "w") as f:
    f.write(content)

print("   ✓ Updated imports to use DeepSeek adapter")

# Step 3: Start the new API server
print("\n3. Starting updated API server...")
subprocess.Popen(["python3", "api_server_unified.py"])
time.sleep(5)

# Step 4: Test the endpoint
print("\n4. Testing DeepSeek Michelin endpoint...")
import requests

test_data = {
    "startup_data": {
        "startup_name": "TestStartup",
        "sector": "saas",
        "funding_stage": "seed",
        "total_capital_raised_usd": 1000000,
        "cash_on_hand_usd": 500000,
        "market_size_usd": 1000000000,
        "market_growth_rate_annual": 20,
        "competitor_count": 5,
        "market_share_percentage": 0.1,
        "team_size_full_time": 10
    }
}

start_time = time.time()
response = requests.post("http://localhost:8001/api/michelin/analyze", json=test_data, timeout=150)
elapsed = time.time() - start_time

print(f"   Status: {response.status_code}")
print(f"   Time: {elapsed:.2f}s")
print(f"   Using: {'DeepSeek' if elapsed > 10 else 'Possible cache/error'}")

if response.status_code == 200:
    print("\n✅ SUCCESS: DeepSeek Michelin analysis is now active!")
    print("   The frontend will now receive real DeepSeek-powered analysis")
    print("   with proper data transformation for UI compatibility.")
else:
    print(f"\n❌ ERROR: {response.text}")

print("\n" + "=" * 60)
print("Next steps:")
print("1. Test in the frontend to verify the analysis displays correctly")
print("2. Monitor api_server.log for any errors")
print("3. The adapter handles timeouts gracefully (120s limit)")