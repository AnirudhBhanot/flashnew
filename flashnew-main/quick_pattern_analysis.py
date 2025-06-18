#!/usr/bin/env python3
"""
Quick Pattern Analysis - Simplified version
"""

import pandas as pd
import numpy as np
from collections import Counter
import json

# Load data
print("Loading data...")
df = pd.read_csv('data/final_100k_dataset_45features.csv')

# Basic stats
print(f"\nDataset: {len(df):,} startups, {df['success'].mean():.1%} success rate")

# Analyze key segments
print("\n=== KEY INSIGHTS FOR PATTERN EXPANSION ===")

# 1. Business model patterns based on economics
print("\n1. BUSINESS MODEL PATTERNS")
# High margin SaaS
saas_pattern = (df['gross_margin_percent'] > 70) & (df['ltv_cac_ratio'] > 3)
print(f"   - High-Margin SaaS: {saas_pattern.sum():,} ({saas_pattern.mean():.1%})")

# Marketplace
marketplace = (df['gross_margin_percent'] < 40) & (df['network_effects_present'] == 1)
print(f"   - Marketplace Model: {marketplace.sum():,} ({marketplace.mean():.1%})")

# Hardware/Physical
hardware = (df['gross_margin_percent'] < 50) & (df['patent_count'] > 0)
print(f"   - Hardware/Physical: {hardware.sum():,} ({hardware.mean():.1%})")

# 2. Growth patterns
print("\n2. GROWTH DYNAMICS PATTERNS")
# Hypergrowth
hypergrowth = (df['revenue_growth_rate_percent'] > 200) & (df['user_growth_rate_percent'] > 200)
print(f"   - Hypergrowth: {hypergrowth.sum():,} ({hypergrowth.mean():.1%})")

# Steady growth
steady = (df['revenue_growth_rate_percent'].between(50, 150)) & (df['burn_multiple'] < 2)
print(f"   - Steady Efficient: {steady.sum():,} ({steady.mean():.1%})")

# Struggling
struggling = (df['revenue_growth_rate_percent'] < 20) & (df['burn_multiple'] > 5)
print(f"   - Struggling/Pivoting: {struggling.sum():,} ({struggling.mean():.1%})")

# 3. Technology depth
print("\n3. TECHNOLOGY PATTERNS")
# Deep tech
deep_tech = (df['tech_differentiation_score'] >= 4) & (df['patent_count'] > 5)
print(f"   - Deep Tech: {deep_tech.sum():,} ({deep_tech.mean():.1%})")

# AI/Data
ai_data = (df['has_data_moat'] == 1) & (df['tech_differentiation_score'] >= 4)
print(f"   - AI/Data-Driven: {ai_data.sum():,} ({ai_data.mean():.1%})")

# Platform
platform = (df['network_effects_present'] == 1) & (df['scalability_score'] >= 4)
print(f"   - Platform Tech: {platform.sum():,} ({platform.mean():.1%})")

# 4. Operational patterns
print("\n4. OPERATIONAL PATTERNS")
# Capital efficient
efficient = (df['burn_multiple'] < 1.5) & (df['gross_margin_percent'] > 60)
print(f"   - Capital Efficient: {efficient.sum():,} ({efficient.mean():.1%})")

# High burn
high_burn = (df['burn_multiple'] > 5) & (df['runway_months'] < 12)
print(f"   - High Burn Rate: {high_burn.sum():,} ({high_burn.mean():.1%})")

# 5. Market approach
print("\n5. MARKET APPROACH PATTERNS")
# Enterprise
enterprise = (df['ltv_cac_ratio'] > 3) & (df['customer_concentration_percent'] > 20)
print(f"   - Enterprise B2B: {enterprise.sum():,} ({enterprise.mean():.1%})")

# SMB
smb = (df['customer_count'] > 100) & (df['customer_concentration_percent'] < 10)
print(f"   - SMB Focused: {smb.sum():,} ({smb.mean():.1%})")

# Consumer
consumer = (df['customer_count'] > 1000) & (df['dau_mau_ratio'] > 0.3)
print(f"   - Consumer Mass: {consumer.sum():,} ({consumer.mean():.1%})")

# 6. Success rates by pattern
print("\n=== SUCCESS RATES BY PATTERN ===")
patterns = {
    'High-Margin SaaS': saas_pattern,
    'Marketplace': marketplace,
    'Hypergrowth': hypergrowth,
    'Steady Efficient': steady,
    'Deep Tech': deep_tech,
    'AI/Data-Driven': ai_data,
    'Capital Efficient': efficient,
    'Enterprise B2B': enterprise
}

for name, mask in patterns.items():
    if mask.sum() > 100:
        success_rate = df[mask]['success'].mean()
        print(f"{name:20} Success: {success_rate:.1%} (n={mask.sum():,})")

# 7. Underserved segments
print("\n=== UNDERSERVED SEGMENTS (Need New Patterns) ===")
# Find startups that don't match any major pattern
no_pattern = ~(saas_pattern | marketplace | hardware | hypergrowth | steady | struggling | deep_tech | ai_data | platform)
print(f"No clear pattern: {no_pattern.sum():,} startups ({no_pattern.mean():.1%})")

# Analyze these orphan startups
orphans = df[no_pattern]
print(f"Orphan success rate: {orphans['success'].mean():.1%}")
print(f"Orphan characteristics:")
print(f"  - Avg team size: {orphans['team_size_full_time'].mean():.0f}")
print(f"  - Avg burn multiple: {orphans['burn_multiple'].mean():.1f}")
print(f"  - Avg growth rate: {orphans['revenue_growth_rate_percent'].mean():.0f}%")

# Recommendations
print("\n=== RECOMMENDATIONS ===")
print("1. Current 14 patterns → Expand to 45 patterns")
print("2. Add industry verticals (FinTech, HealthTech, EdTech, etc.)")
print("3. Add geographic patterns (US, Europe, Asia strategies)")
print("4. Add funding patterns (Bootstrap, VC-backed, Grant-funded)")
print("5. Create hybrid patterns (e.g., 'AI-powered Marketplace')")
print(f"6. Focus on {no_pattern.sum():,} startups without clear patterns")

# Save summary
summary = {
    'total_startups': len(df),
    'success_rate': float(df['success'].mean()),
    'pattern_coverage': {
        'with_clear_pattern': float(1 - no_pattern.mean()),
        'without_pattern': float(no_pattern.mean())
    },
    'pattern_sizes': {name: int(mask.sum()) for name, mask in patterns.items() if mask.sum() > 100},
    'pattern_success_rates': {name: float(df[mask]['success'].mean()) for name, mask in patterns.items() if mask.sum() > 100},
    'recommendation': 'Expand from 14 to 45 patterns for 95% coverage'
}

with open('pattern_expansion_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\nAnalysis complete! Summary saved to pattern_expansion_summary.json")