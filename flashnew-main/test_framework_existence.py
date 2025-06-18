#!/usr/bin/env python3
"""
Test if frameworks exist in database
"""

from framework_intelligence.framework_database import get_framework_by_id

# Test the frameworks that should be selected
test_frameworks = [
    "ansoff_matrix",
    "porters_five_forces", 
    "blue_ocean_strategy",
    "bcg_matrix",
    "unit_economics",
    "swot_analysis"
]

print("Checking framework existence in database:")
for fw_id in test_frameworks:
    framework = get_framework_by_id(fw_id)
    if framework:
        print(f"✓ {fw_id}: {framework.name}")
    else:
        print(f"✗ {fw_id}: NOT FOUND")