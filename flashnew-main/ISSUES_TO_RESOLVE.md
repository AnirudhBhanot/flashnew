# Issues to Resolve for Pattern System

## Priority 1: Feature Mismatch (Blocking) 🔴

### Issue
```
Error: X has 12 features, but RandomForestClassifier is expecting 10 features as input
```

### Details
- Occurs in all prediction endpoints: `/predict`, `/predict_enhanced`, `/analyze_pattern`
- The capital pillar model expects 10 features but receives 12
- Likely affects all pillar models (capital, advantage, market, people)

### Investigation Needed
1. Check what features the models were trained with:
   - Look in `train_pattern_models.py`
   - Check `models/pattern_models/` for model metadata
   - Review training logs if available

2. Compare with current feature definitions:
   ```python
   # Current in api_server.py
   CAPITAL_FEATURES = [
       "funding_stage",                # 1
       "total_capital_raised_usd",     # 2
       "cash_on_hand_usd",            # 3
       "monthly_burn_usd",            # 4
       "runway_months",               # 5
       "annual_revenue_run_rate",     # 6
       "revenue_growth_rate_percent", # 7
       "gross_margin_percent",        # 8
       "burn_multiple",               # 9
       "ltv_cac_ratio",              # 10
       "investor_tier_primary",       # 11
       "has_debt"                     # 12
   ]
   ```

### Potential Solutions
1. **Quick Fix**: Remove 2 features before prediction
   - Identify which 2 features to remove
   - Modify `_get_pillar_features` in orchestrator

2. **Proper Fix**: Align features with training
   - Find exact feature list used in training
   - Create feature mapping/filtering

3. **Long-term Fix**: Retrain models with current features
   - Use `train_pattern_models.py` with updated features
   - Ensure consistency across all models

## Priority 2: Missing Models (Non-blocking) ⚠️

### Issue
```
ERROR: [Errno 2] No such file or directory: 'models/stage_hierarchical/pre-seed_model.pkl'
```

### Details
- Stage-based hierarchical models are missing
- System falls back gracefully
- Reduces accuracy but doesn't break functionality

### Solution
- Run stage model training: `python train_stage_hierarchical_models.py`
- Or disable stage model loading if not needed

## Priority 3: Testing & Validation 🟡

### Once Feature Mismatch is Fixed:

1. **API Testing**
   ```bash
   python test_pattern_api.py
   ```
   Should show:
   - Successful predictions with pattern analysis
   - Pattern confidence scores
   - Similar companies and recommendations

2. **Frontend Testing**
   - Start frontend: `cd flash-frontend && npm start`
   - Complete a startup analysis
   - Verify pattern insights appear in results
   - Check both business and technical views

3. **Pattern Matching Validation**
   - Test with different startup profiles
   - Verify pattern assignments make sense
   - Check confidence scores are reasonable

## File Modifications Needed

### 1. Fix Feature Selection
**File**: `/models/unified_orchestrator.py`
**Method**: `_get_pillar_features()`
**Action**: Filter features to match model training

### 2. Add Feature Metadata
**File**: `/models/pattern_models/metadata.json`
**Action**: Document exact features used in training

### 3. Update Test Data
**File**: `/test_pattern_api.py`
**Action**: Ensure test data includes all required fields

## Success Criteria

✅ Pattern System is ready when:
1. `/predict_enhanced` returns 200 status
2. Response includes `pattern_analysis` object
3. Frontend displays pattern insights
4. No feature mismatch errors in logs
5. Pattern confidence scores are between 0-1
6. Similar companies list is populated

## Quick Debug Commands

```bash
# Check API health
curl http://localhost:8001/health

# List patterns
curl http://localhost:8001/patterns

# Test prediction (will fail until fixed)
python test_pattern_api.py

# Check logs
tail -f api_v2.log

# Find feature definitions
grep -n "CAPITAL_FEATURES" api_server.py
grep -n "_get_pillar_features" models/unified_orchestrator.py
```

## Timeline Estimate

- **Feature Fix**: 30-60 minutes
- **Testing**: 30 minutes
- **Total**: 1-2 hours to full functionality

The pattern system is very close to being fully operational. The main blocker is understanding and aligning the feature expectations between the API and the trained models.