#!/usr/bin/env python3
"""
Fix the orchestrator's CAMP score calculation to properly normalize features
and handle the temporal model feature mismatch
"""

import shutil
from pathlib import Path

# First, let's fix the orchestrator file
orchestrator_path = Path("models/unified_orchestrator_v3_integrated.py")
backup_path = Path("models/unified_orchestrator_v3_integrated.py.backup")

# Create backup
shutil.copy(orchestrator_path, backup_path)
print(f"Created backup at {backup_path}")

# Read the file
with open(orchestrator_path, 'r') as f:
    content = f.read()

# Fix 1: Update the _calculate_camp_scores_safe method to properly normalize features
camp_score_fix = '''    def _calculate_camp_scores_safe(self, features: pd.DataFrame) -> Dict[str, float]:
        """Safely calculate CAMP scores with proper normalization"""
        from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES
        from utils.safe_math import safe_mean, clip_value
        
        scores = {}
        
        # Helper function to normalize feature values
        def normalize_feature(feature_name, value):
            """Normalize a single feature value to 0-1 range"""
            if pd.isna(value) or value is None:
                return 0.5
            
            try:
                # Handle different feature types
                if feature_name in ['total_capital_raised_usd', 'cash_on_hand_usd']:
                    # Log scale for large monetary values
                    return min(1.0, np.log10(float(value) + 1) / 8)  # Up to $100M
                elif feature_name == 'monthly_burn_usd':
                    # Inverse - lower burn is better
                    return max(0, 1.0 - (float(value) / 1000000))  # $1M/month = 0
                elif feature_name == 'runway_months':
                    return min(1.0, float(value) / 24)  # 24 months = perfect
                elif feature_name == 'burn_multiple':
                    # Inverse - lower is better
                    return max(0, 1.0 - (float(value) / 10))
                elif feature_name in ['tam_size_usd', 'sam_size_usd', 'som_size_usd']:
                    # Log scale for market sizes
                    return min(1.0, np.log10(float(value) + 1) / 10)  # Up to $10B
                elif feature_name == 'annual_revenue_run_rate':
                    # Log scale for revenue
                    return min(1.0, np.log10(float(value) + 1) / 7)  # Up to $10M
                elif feature_name.endswith('_percent'):
                    return min(1.0, max(0, float(value) / 100.0))
                elif feature_name.endswith('_score'):
                    return min(1.0, max(0, (float(value) - 1) / 4.0))  # 1-5 scale to 0-1
                elif feature_name in ['customer_count', 'team_size_full_time', 'founders_count', 'advisors_count']:
                    # Log scale for counts
                    return min(1.0, np.log10(float(value) + 1) / 4)  # Up to 10,000
                elif feature_name in ['patent_count', 'competitors_named_count']:
                    return min(1.0, float(value) / 20)  # 20+ = max
                elif isinstance(value, bool) or feature_name in ['network_effects_present', 'has_data_moat', 
                                                                'regulatory_advantage_present', 'has_debt']:
                    return 1.0 if value else 0.0
                elif feature_name == 'key_person_dependency':
                    # Inverse - dependency is bad
                    return 0.0 if value else 1.0
                elif feature_name in ['product_retention_30d', 'product_retention_90d', 'dau_mau_ratio']:
                    # Already in 0-1 range
                    return float(value)
                elif feature_name == 'ltv_cac_ratio':
                    # Good LTV/CAC is 3+
                    return min(1.0, float(value) / 3.0)
                elif feature_name == 'gross_margin_percent':
                    # Convert negative margins to 0, positive to 0-1
                    return max(0, min(1.0, float(value) / 100.0))
                else:
                    # Default normalization for other numeric features
                    return min(1.0, max(0, float(value)))
            except (ValueError, TypeError):
                return 0.5
        
        # Calculate normalized scores for each CAMP pillar
        # Capital score
        capital_values = []
        for f in CAPITAL_FEATURES:
            if f in features.columns:
                val = features[f].iloc[0] if len(features) > 0 else 0
                normalized = normalize_feature(f, val)
                capital_values.append(normalized)
        scores['capital'] = safe_mean(capital_values, default=0.5) if capital_values else 0.5
        
        # Advantage score
        advantage_values = []
        for f in ADVANTAGE_FEATURES:
            if f in features.columns:
                val = features[f].iloc[0] if len(features) > 0 else 0
                normalized = normalize_feature(f, val)
                advantage_values.append(normalized)
        scores['advantage'] = safe_mean(advantage_values, default=0.5) if advantage_values else 0.5
        
        # Market score
        market_values = []
        for f in MARKET_FEATURES:
            if f in features.columns:
                val = features[f].iloc[0] if len(features) > 0 else 0
                normalized = normalize_feature(f, val)
                market_values.append(normalized)
        scores['market'] = safe_mean(market_values, default=0.5) if market_values else 0.5
        
        # People score
        people_values = []
        for f in PEOPLE_FEATURES:
            if f in features.columns:
                val = features[f].iloc[0] if len(features) > 0 else 0
                normalized = normalize_feature(f, val)
                people_values.append(normalized)
        scores['people'] = safe_mean(people_values, default=0.5) if people_values else 0.5
        
        return scores'''

# Fix 2: Update the _prepare_temporal_features to add the missing burn_efficiency feature
temporal_fix = '''    def _prepare_temporal_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for temporal model which expects 46 features (45 + burn_efficiency)"""
        # Make a copy to avoid modifying original
        temporal_features = features.copy()
        
        # Add burn_efficiency if not present (temporal model expects this as 46th feature)
        if 'burn_efficiency' not in temporal_features.columns:
            # Calculate burn efficiency: revenue / burn (higher is better)
            if 'annual_revenue_run_rate' in temporal_features.columns and 'monthly_burn_usd' in temporal_features.columns:
                revenue = temporal_features['annual_revenue_run_rate'].fillna(0)
                burn = temporal_features['monthly_burn_usd'].fillna(1)  # Avoid division by zero
                temporal_features['burn_efficiency'] = (revenue / 12) / burn.replace(0, 1)  # Monthly revenue / monthly burn
            else:
                temporal_features['burn_efficiency'] = 0.5  # Default middle value
        
        return temporal_features'''

# Apply fixes
import re

# Fix 1: Replace the _calculate_camp_scores_safe method
pattern1 = r'def _calculate_camp_scores_safe\(self.*?\n        return scores'
content = re.sub(pattern1, camp_score_fix.strip(), content, flags=re.DOTALL)

# Fix 2: Replace the _prepare_temporal_features method
pattern2 = r'def _prepare_temporal_features\(self.*?\n        return features'
content = re.sub(pattern2, temporal_fix.strip(), content, flags=re.DOTALL)

# Write the fixed content
with open(orchestrator_path, 'w') as f:
    f.write(content)

print("Fixed the orchestrator with:")
print("1. Proper CAMP score normalization")
print("2. Temporal model feature handling (adds burn_efficiency as 46th feature)")
print("\nThe success_probability should now return reasonable values instead of 1.0")