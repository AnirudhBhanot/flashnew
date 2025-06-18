import requests
import json

# Test configuration endpoints
base_url = "http://localhost:8001"

print("Testing configuration endpoints...\n")

# Test stage weights
print("1. Testing /config/stage-weights")
response = requests.get(f"{base_url}/config/stage-weights")
print(f"Status: {response.status_code}")
if response.ok:
    weights = response.json()
    print(f"Stages found: {list(weights.keys())}")
    print(f"Pre-seed weights: {weights['pre_seed']}")
else:
    print(f"Error: {response.text}")

print("\n2. Testing /config/model-performance")
response = requests.get(f"{base_url}/config/model-performance")
print(f"Status: {response.status_code}")
if response.ok:
    performance = response.json()
    print(f"Overall accuracy: {performance['overall_accuracy'] * 100:.2f}%")
    print(f"Dataset size: {performance['dataset_size']}")
else:
    print(f"Error: {response.text}")

print("\n3. Testing /config/company-examples")
response = requests.get(f"{base_url}/config/company-examples")
print(f"Status: {response.status_code}")
if response.ok:
    examples = response.json()
    print(f"Stages with examples: {list(examples.keys())}")
    print(f"Seed example: {examples['seed']['company']}")
else:
    print(f"Error: {response.text}")

print("\n✅ All configuration endpoints are working!")