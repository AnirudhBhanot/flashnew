#!/usr/bin/env python3
"""
Fix the API integration by updating the orchestrator to work with 45-feature models
"""

import shutil
from datetime import datetime

print("🔧 Fixing API Integration")
print("=" * 60)

# Backup the current orchestrator
backup_path = f"models/unified_orchestrator_v3_integrated_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
shutil.copy("models/unified_orchestrator_v3_integrated.py", backup_path)
print(f"✅ Backed up orchestrator to {backup_path}")

# Read the current orchestrator
with open("models/unified_orchestrator_v3_integrated.py", "r") as f:
    content = f.read()

# Find and replace the DNA feature preparation to NOT add CAMP scores
old_dna_method = '''    def _prepare_dna_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for DNA analyzer which expects 49 features (45 base + 4 CAMP scores)"""'''

new_dna_method = '''    def _prepare_dna_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for DNA analyzer which expects 45 features"""
        # DNA analyzer now expects only the base 45 features, no CAMP scores
        return features'''

if old_dna_method in content:
    # Find the full method and replace it
    start = content.find(old_dna_method)
    # Find the next method definition
    next_def = content.find("\n    def ", start + 1)
    if next_def > 0:
        # Replace the entire method
        old_full_method = content[start:next_def]
        content = content.replace(old_full_method, new_dna_method + "\n")
        print("✅ Updated _prepare_dna_features to return 45 features only")
else:
    print("⚠️  Could not find the exact method to replace")

# Also update the temporal features method to expect 45 features
old_temporal = "_prepare_temporal_features(self, features: pd.DataFrame)"
if old_temporal in content:
    # Find and update the comment
    temporal_start = content.find("# Temporal model expects 48 features")
    if temporal_start > 0:
        content = content.replace(
            "# Temporal model expects 48 features (45 base + 3 temporal metrics)",
            "# Temporal model expects 45 features (same as base)"
        )
        print("✅ Updated temporal model comment")

# Write the updated orchestrator
with open("models/unified_orchestrator_v3_integrated.py", "w") as f:
    f.write(content)

print("\n✅ Orchestrator updated to work with 45-feature models")
print("   The API should now work correctly with the frontend!")

# Test the fix
print("\n🧪 Testing the fix...")
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Reload the module
import importlib
if 'models.unified_orchestrator_v3_integrated' in sys.modules:
    importlib.reload(sys.modules['models.unified_orchestrator_v3_integrated'])

from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
from type_converter_simple import TypeConverter
from feature_config import ALL_FEATURES

orchestrator = UnifiedOrchestratorV3()
type_converter = TypeConverter()

# Test data
test_data = {
    "total_capital_raised_usd": 5000000,
    "funding_stage": "series_a",
    "sector": "saas",
    "team_size_full_time": 25,
    "product_stage": "growth"
}

backend_data = type_converter.convert_frontend_to_backend(test_data)
canonical_features = {k: backend_data.get(k, 0) for k in ALL_FEATURES}

try:
    result = orchestrator.predict(canonical_features)
    print("✅ Prediction successful!")
    print(f"   Success Probability: {result.get('success_probability', 0):.1%}")
except Exception as e:
    print(f"❌ Still failing: {str(e)}")