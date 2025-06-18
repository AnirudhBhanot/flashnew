# FLASH System Investigation Report

## Executive Summary

The FLASH system has **THREE CRITICAL ISSUES** preventing proper investment assessments:

1. **CAMP Score Calculation**: Was using raw monetary values causing scores > 10,000,000%
2. **Model Predictions**: Models are returning high probabilities (70-80%) regardless of input quality
3. **Verdict Logic**: Had incorrect default to "CONDITIONAL PASS"

## Issues Found and Status

### Issue 1: CAMP Score Calculation ✅ FIXED
**Problem**: The CAMP score calculation was averaging raw monetary values (e.g., $10,000) with percentages and binary values, resulting in scores like 10,092,418%.

**Solution**: Implemented proper feature normalization:
- Monetary values: Log scale ($1K-$1B range)
- Percentages: Scaled to 0-1 range
- Scores (1-5): Mapped to 0-1 range
- Special handling for inverse metrics (burn_multiple)

**Result**: CAMP scores now properly range from 0-100%

### Issue 2: Verdict Default ✅ FIXED
**Problem**: When extracting verdict from orchestrator response, system defaulted to "CONDITIONAL PASS" instead of calculating based on probability.

**Solution**: Now calculates verdict based on probability if missing:
- < 50%: FAIL
- 50-70%: CONDITIONAL PASS
- ≥ 70%: PASS

### Issue 3: Model Predictions ❌ CRITICAL - NOT FIXED
**Problem**: The ML models are returning high success probabilities (70-80%) even for terrible startups.

**Evidence**:
- Terrible startup (40% avg CAMP) → 80.9% success probability
- Excellent startup (61% avg CAMP) → 69.0% success probability
- Models are INVERSELY correlated with quality!

**Root Causes Identified**:
1. **Temporal Model**: Always returns ~90% regardless of input
2. **DNA Analyzer**: Limited discrimination (32% for bad, 65% for good)
3. **Industry Model**: Poor discrimination (49% for bad, 70% for good)
4. **Weights**: 60% DNA, 25% Industry, 15% Temporal (Pattern system disabled)

## Why Pre-seed with 49.3% Shows CONDITIONAL PASS

Based on the investigation:
1. Even with poor CAMP scores (40-50%), models predict 70-80% success
2. This inflated probability (>50%) triggers CONDITIONAL PASS
3. The models are fundamentally broken and need retraining

## Recommended Fixes

### Immediate (Quick Fix)
1. **Disable broken models** and use CAMP scores directly:
   ```python
   success_probability = np.mean([
       scores['capital'], 
       scores['advantage'],
       scores['market'],
       scores['people']
   ])
   ```

2. **Adjust verdict thresholds** for CAMP-based scoring:
   - < 40%: FAIL
   - 40-60%: CONDITIONAL PASS
   - 60-75%: PASS
   - > 75%: STRONG PASS

### Long-term (Proper Fix)
1. **Retrain all models** with proper feature normalization
2. **Validate model predictions** match expected outcomes
3. **Implement model monitoring** to catch degradation
4. **Add integration tests** for edge cases

## Testing Results

| Startup Type | CAMP Avg | Model Prediction | Expected | Actual Verdict |
|-------------|----------|------------------|----------|----------------|
| Terrible | 40% | 80.9% ❌ | FAIL | STRONG PASS ❌ |
| Excellent | 61% | 69.0% ❌ | PASS | PASS ✓ |
| Borderline | 44% | 75.7% ❌ | FAIL | PASS ❌ |

## Conclusion

The system's core logic is now correct, but the ML models are producing nonsensical predictions. A pre-seed startup with 49.3% CAMP score SHOULD get FAIL, but the broken models inflate this to 70-80%, causing incorrect CONDITIONAL PASS verdicts.

**Recommendation**: Implement the immediate fix to use CAMP scores directly until models can be retrained.