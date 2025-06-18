#!/usr/bin/env python3
"""
Test if API can start up
"""
import subprocess
import time
import requests
import signal
import os

print("Testing API startup...")
print("=" * 50)

# Start API server in background
process = subprocess.Popen(
    ["python3", "api_server_unified.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Give it time to start
time.sleep(3)

# Check if process is still running
if process.poll() is None:
    print("✅ API server started successfully!")
    
    # Try to connect
    try:
        response = requests.get("http://localhost:8001/health", timeout=2)
        if response.status_code == 200:
            print("✅ Health endpoint responding!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint returned {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
    
    # Kill the process
    process.terminate()
    process.wait()
    print("✅ API server stopped cleanly")
else:
    # Process died, show error
    stdout, stderr = process.communicate()
    print("❌ API server failed to start!")
    print(f"Exit code: {process.returncode}")
    if stdout:
        print(f"Stdout:\n{stdout}")
    if stderr:
        print(f"Stderr:\n{stderr}")

print("=" * 50)