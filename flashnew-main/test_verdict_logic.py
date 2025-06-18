#!/usr/bin/env python3
"""Test verdict calculation logic"""

def test_verdict(prob):
    """Test verdict logic from api_server_unified.py"""
    if prob >= 0.7:
        verdict = "PASS"
        strength_level = "Strong" if prob >= 0.8 else "Moderate"
    elif prob >= 0.5:
        verdict = "CONDITIONAL PASS"
        strength_level = "Moderate" if prob >= 0.6 else "Weak"
    else:
        verdict = "FAIL"
        strength_level = "Weak"
    
    return verdict, strength_level

# Test cases
test_scores = [0.493, 0.50, 0.55, 0.65, 0.70, 0.75, 0.80, 0.85]

print("Testing verdict logic:\n")
print("Score  | Verdict           | Strength")
print("-------|-------------------|----------")

for score in test_scores:
    verdict, strength = test_verdict(score)
    print(f"{score:.1%} | {verdict:<17} | {strength}")

print("\n❌ ISSUE: 49.3% should be FAIL, not CONDITIONAL PASS")
print("\nPossible causes:")
print("1. Rounding error (49.3% being rounded to 50%)")
print("2. Different verdict logic being applied elsewhere")
print("3. Pre-seed specific rules overriding general logic")