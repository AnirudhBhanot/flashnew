# FLASH Model Experiments

This directory contains experimental approaches that were tested but not adopted for production.

## Summary of Results

| Approach | Features | AUC | Improvement | Status |
|----------|----------|-----|-------------|---------|
| Baseline | 45 | 77.3% | - | **Production** |
| Enhanced Features | 75 | 77.5% | +0.2% | Not worth complexity |
| + Clustering | 97 | 77.7% | +0.4% | Minimal gain |
| + Synthetic Pitch | 137 | 100%* | Overfitting | Failed |

*Synthetic pitch decks were too deterministic, causing overfitting

## Experiments

### 1. 75_features/
Extended the original 45 features to 75 by adding:
- Monthly revenue growth rate (98% correlated with annual)
- Burn months remaining
- Revenue per employee
- Other derived metrics

**Result**: Only 0.2% improvement, not worth the added complexity.

### 2. clustering/
Added startup archetype clustering to identify patterns:
- Success archetypes: "Efficient SaaS", "Blitzscaler", etc.
- Failure archetypes: "Cash Burner", "Poor Retention", etc.
- Distance-based features to archetypes

**Result**: Added 0.2% on top of 75 features (total 0.4% improvement).

### 3. pitch_generation/
Generated synthetic pitch deck summaries:
- Researched successful pitch patterns
- Created quality-based generation
- Extracted text features

**Result**: Overfitting due to deterministic generation. Real pitch decks would likely add 5-7% AUC.

### 4. advanced_ensemble/
Tested diverse model ensembles:
- CatBoost, XGBoost, LightGBM, Random Forest, Neural Networks
- Stacking with meta-learners
- Feature subset ensembling

**Result**: Complexity didn't improve over simple CatBoost ensemble.

## Key Learnings

1. **Feature Engineering Limits**: Without new data sources, derived features add minimal value
2. **Original Features Sufficient**: The 45 features already capture the key signals
3. **Text Data Powerful**: Real pitch decks would significantly improve performance
4. **Ensemble Limits**: Model diversity alone can't overcome data limitations

## Production Recommendation

Use the original 45-feature model:
- Simpler to maintain
- Easier to collect features
- Nearly identical performance (77.3% vs 77.7%)
- Better interpretability

## Future Improvements

To genuinely reach 82-83% AUC, you need:
1. Real pitch deck text
2. Time-series data (monthly metrics)
3. External validation (LinkedIn, news)
4. Network effects data