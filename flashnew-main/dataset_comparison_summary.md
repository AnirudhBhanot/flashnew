# Dataset Analysis Summary

## Total Datasets Found: 13

### Dataset Breakdown

#### 1. **100k Dataset Family** (6 datasets)
- **Purpose**: Initial experiments with different feature sets
- **Success Rate**: All have 40.3% success (unrealistic)
- **Variations**:
  - `final_100k_dataset_45features.csv`: Base version (45 features)
  - `final_100k_dataset_75features.csv`: Added features (75 features)
  - `final_100k_dataset_complete.csv`: Kitchen sink (154 features!)
  - `final_100k_dataset_with_clusters.csv`: Added clustering
  - `final_100k_dataset_with_pitches.csv`: Added pitch data
  - `generated_100k_dataset.csv`: Different generation (19.1% success)

**Issue**: 40% success rate is way too high (real rate is ~10-20%)

#### 2. **200k Dataset Family** (3 datasets)
- **Purpose**: Larger scale, more realistic
- **Datasets**:
  - `realistic_startup_dataset_200k.csv`: 25% success (has outcome_type ⚠️)
  - `real_patterns_startup_dataset_200k.csv`: 20% success (has outcome_type ⚠️)
  - `realistic_200k_dataset.csv`: 23.1% success

**Issue**: Most recent datasets have data leakage via outcome_type

#### 3. **Sample Datasets** (3 datasets)
- Small 1,000 row samples for testing
- Not for training

#### 4. **Other** (1 dataset)
- `real_startup_data.csv`: Only 4 rows (manual examples)

## Key Findings

### 1. **Data Leakage Problem**
```
Datasets WITH leakage (outcome_type column):
- realistic_startup_dataset_200k.csv ❌
- real_patterns_startup_dataset_200k.csv ❌  
- realistic_dataset_sample_1k.csv ❌
- real_patterns_sample.csv ❌

Datasets WITHOUT leakage:
- All 100k family datasets ✅
- realistic_200k_dataset.csv ✅
- generated_100k_dataset.csv ✅
```

### 2. **Success Rate Distribution**
- 40.3% - Too high (100k family)
- 25.0% - Reasonable (realistic_startup)
- 20.0% - Most realistic (real_patterns)
- 19.1% - Good (generated_100k)

### 3. **Common Features** (26 core features present in all)
- Financial: capital_raised, burn_rate, runway, revenue
- Growth: revenue_growth, customer_growth, retention
- Team: founders_count, experience, prior_exits
- Market: market_growth, competitors

### 4. **Dataset Correlations**
- Very low correlations between datasets (-0.019 to -0.012)
- Indicates different generation methods
- Cannot simply combine them

## 🎯 Expert Recommendation

### DO NOT COMBINE ALL DATASETS

**Why:**
1. **Different Generation Methods** - Each used different logic
2. **Inconsistent Success Rates** - 19% to 40% (should be ~20%)
3. **Data Leakage** - 4 datasets have outcome_type
4. **Statistical Properties Differ** - Low correlations between datasets

### BEST APPROACH:

**Option 1: Start Fresh (Recommended)**
```python
# Create ONE high-quality dataset:
- 200k samples
- 20% success rate (realistic)
- No outcome_type or leakage columns
- Consistent generation logic
- Based on real startup statistics
```

**Option 2: Use Best Existing**
```
Use: realistic_200k_dataset.csv
- No outcome_type ✅
- 23.1% success rate ✅
- 200k samples ✅
- But: May have hidden correlations
```

### AVOID:
- ❌ real_patterns_startup_dataset_200k.csv (has outcome_type)
- ❌ realistic_startup_dataset_200k.csv (has outcome_type)
- ❌ Any 100k dataset (40% success too high)

### FOR PRODUCTION:
1. Archive all existing datasets
2. Create ONE canonical dataset with:
   - Real historical data (when available)
   - Proper train/val/test splits
   - No leakage
   - Documented generation process
3. Version control the dataset
4. Never mix synthetic and real data

## Bottom Line

**Quality > Quantity**: One well-designed 200k dataset is better than 13 problematic datasets combined. The current datasets have too many issues (leakage, unrealistic success rates, inconsistent generation) to combine meaningfully.

**Action**: Use `realistic_200k_dataset.csv` for now, but plan to replace with real historical data ASAP.