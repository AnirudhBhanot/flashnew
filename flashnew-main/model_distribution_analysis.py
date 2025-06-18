#!/usr/bin/env python3
"""
Create visual analysis of model score distributions
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Data from our analysis
model_scores = {
    "Strong Startup": {
        "CAMP Average": 0.60,  # (90+50+50+50)/4
        "DNA Analyzer": 0.218,  # From debug
        "Industry Model": 0.0,
        "Temporal Model": 0.0,
        "Pattern Model": None,  # Disabled
        "Final Score": 0.136
    },
    "Average Startup": {
        "CAMP Average": 0.4875,  # (70+50+25+50)/4
        "DNA Analyzer": 0.22,  # Estimated
        "Industry Model": 0.0,
        "Temporal Model": 0.0,
        "Pattern Model": None,
        "Final Score": 0.134
    },
    "Weak Startup": {
        "CAMP Average": 0.425,  # (60+50+10+50)/4
        "DNA Analyzer": 0.20,  # Estimated
        "Industry Model": 0.0,
        "Temporal Model": 0.0,
        "Pattern Model": None,
        "Final Score": 0.128
    }
}

# Create figure
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('FLASH Model Score Distribution Analysis', fontsize=16, fontweight='bold')

# Plot 1: Model Contributions by Startup Type
startup_types = list(model_scores.keys())
x = np.arange(len(startup_types))
width = 0.15

models = ["CAMP Average", "DNA Analyzer", "Industry Model", "Temporal Model", "Final Score"]
colors = ['gold', 'skyblue', 'lightcoral', 'lightgreen', 'darkred']

for i, model in enumerate(models):
    values = [model_scores[startup][model] if model_scores[startup][model] is not None else 0 
              for startup in startup_types]
    ax1.bar(x + i*width - 2*width, values, width, label=model, color=colors[i])

ax1.set_xlabel('Startup Profile')
ax1.set_ylabel('Score')
ax1.set_title('Model Score Distribution by Startup Type')
ax1.set_xticks(x)
ax1.set_xticklabels(startup_types)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1)

# Plot 2: Weight vs Actual Contribution
weights = {
    "CAMP (DNA Analyzer)": {"configured": 0.5, "actual": 0.625, "working": True},
    "Industry Model": {"configured": 0.2, "actual": 0.25, "working": False},
    "Temporal Model": {"configured": 0.1, "actual": 0.125, "working": False},
    "Pattern Model": {"configured": 0.2, "actual": 0.0, "working": False}
}

models = list(weights.keys())
configured = [weights[m]["configured"] for m in models]
actual = [weights[m]["actual"] for m in models]
working = [weights[m]["working"] for m in models]

x = np.arange(len(models))
width = 0.35

bars1 = ax2.bar(x - width/2, configured, width, label='Configured Weight', color='lightblue')
bars2 = ax2.bar(x + width/2, actual, width, label='Actual Weight', color='orange')

# Add working/broken indicators
for i, (bar1, bar2, is_working) in enumerate(zip(bars1, bars2, working)):
    if not is_working:
        ax2.text(bar1.get_x() + bar1.get_width()/2, bar1.get_height() + 0.02, 
                '❌', ha='center', fontsize=20)
        ax2.text(bar2.get_x() + bar2.get_width()/2, bar2.get_height() + 0.02, 
                '❌', ha='center', fontsize=20)

ax2.set_xlabel('Model')
ax2.set_ylabel('Weight')
ax2.set_title('Configured vs Actual Model Weights (❌ = Broken Model)')
ax2.set_xticks(x)
ax2.set_xticklabels(models, rotation=15, ha='right')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: The Gap Problem
gap_data = []
for startup in startup_types:
    camp_avg = model_scores[startup]["CAMP Average"]
    final = model_scores[startup]["Final Score"]
    gap = camp_avg - final
    gap_data.append({
        'startup': startup,
        'camp': camp_avg,
        'final': final,
        'gap': gap
    })

startups = [d['startup'] for d in gap_data]
camps = [d['camp'] for d in gap_data]
finals = [d['final'] for d in gap_data]
gaps = [d['gap'] for d in gap_data]

x = np.arange(len(startups))
width = 0.35

ax3.bar(x - width/2, camps, width, label='CAMP Average', color='green', alpha=0.7)
ax3.bar(x + width/2, finals, width, label='Final Score', color='red', alpha=0.7)

# Add gap annotations
for i, gap in enumerate(gaps):
    ax3.annotate(f'Gap: {gap:.1%}', 
                xy=(i, max(camps[i], finals[i]) + 0.05),
                ha='center', fontsize=10, fontweight='bold')

ax3.set_xlabel('Startup Profile')
ax3.set_ylabel('Score')
ax3.set_title('CAMP Average vs Final Score - The Perception Gap')
ax3.set_xticks(x)
ax3.set_xticklabels(startups)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Root Cause Analysis
ax4.text(0.5, 0.9, 'ROOT CAUSE ANALYSIS', ha='center', fontsize=16, fontweight='bold', transform=ax4.transAxes)

issues = [
    "1. Industry Model returns 0% for ALL inputs",
    "2. Temporal Model returns 0% for ALL inputs",
    "3. Ensemble Model expects 3 features but receives 45",
    "4. Pattern Model is disabled",
    "5. Only DNA Analyzer (CAMP) is functional",
    "",
    "RESULT: Final score = CAMP score × weight only",
    "Users see good CAMP but low overall score",
    "",
    "IMPACT:",
    "• 75% of the scoring system is broken",
    "• Users lose trust when seeing contradictions",
    "• Recommendations based on broken models"
]

for i, issue in enumerate(issues):
    weight = 'bold' if issue.startswith('RESULT:') or issue.startswith('IMPACT:') else 'normal'
    color = 'red' if '0%' in issue or 'broken' in issue else 'black'
    ax4.text(0.05, 0.85 - i*0.06, issue, transform=ax4.transAxes, 
             fontsize=11, fontweight=weight, color=color)

ax4.axis('off')

# Add solution box
solution_text = """IMMEDIATE FIXES NEEDED:
1. Fix Industry & Temporal models (retrain or debug)
2. Fix Ensemble model feature mismatch
3. Enable Pattern model or remove from weights
4. Align frontend display with actual weights"""

ax4.text(0.5, 0.15, solution_text, transform=ax4.transAxes,
         fontsize=10, ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.3))

plt.tight_layout()
plt.savefig('model_distribution_breakdown.png', dpi=150, bbox_inches='tight')
print("Analysis saved as 'model_distribution_breakdown.png'")

# Also create a simple summary
print("\n" + "="*60)
print("FLASH SCORING SYSTEM CRITICAL ISSUES")
print("="*60)
print("\nMODEL STATUS:")
print(f"✅ DNA Analyzer (CAMP): Working - contributes 62.5% of score")
print(f"❌ Industry Model: BROKEN - returns 0% always")
print(f"❌ Temporal Model: BROKEN - returns 0% always")
print(f"❌ Ensemble Model: BROKEN - feature count mismatch")
print(f"❌ Pattern Model: DISABLED")
print(f"\nEFFECTIVE SCORING:")
print(f"Final Score = DNA Analyzer Score × 62.5%")
print(f"Example: 21.8% × 62.5% = 13.6%")
print(f"\nUSER EXPERIENCE:")
print(f"Sees: CAMP scores 60-90% → Expects high score")
print(f"Gets: Final score 13% → Confusion & mistrust")
print("="*60)