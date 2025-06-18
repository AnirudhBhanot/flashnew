#!/usr/bin/env python3
import pandas as pd
import numpy as np
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

# Load test data
print("Loading test data...")
data = pd.read_csv('data/final_100k_dataset_45features.csv')
test_sample = data.sample(n=1000, random_state=42)

# Define canonical 45 features
CANONICAL_FEATURES = [
    'funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd',
    'monthly_burn_usd', 'runway_months', 'annual_revenue_run_rate',
    'revenue_growth_rate_percent', 'gross_margin_percent', 'burn_multiple',
    'ltv_cac_ratio', 'investor_tier_primary', 'has_debt', 'patent_count',
    'network_effects_present', 'has_data_moat', 'regulatory_advantage_present',
    'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
    'scalability_score', 'product_stage', 'product_retention_30d',
    'product_retention_90d', 'sector', 'tam_size_usd', 'sam_size_usd',
    'som_size_usd', 'market_growth_rate_percent', 'customer_count',
    'customer_concentration_percent', 'user_growth_rate_percent',
    'net_dollar_retention_percent', 'competition_intensity',
    'competitors_named_count', 'dau_mau_ratio', 'founders_count',
    'team_size_full_time', 'years_experience_avg', 'domain_expertise_years_avg',
    'prior_startup_experience_count', 'prior_successful_exits_count',
    'board_advisor_experience_score', 'advisors_count', 'team_diversity_percent',
    'key_person_dependency'
]

# Load models and preprocessors
print("\nLoading models...")
dna_model = joblib.load('models/production_v45/dna_analyzer.pkl')
temporal_model = joblib.load('models/production_v45/temporal_model.pkl')
industry_model = joblib.load('models/production_v45/industry_model.pkl')
ensemble_model = joblib.load('models/production_v45/ensemble_model.pkl')
industry_scaler = joblib.load('models/production_v45/industry_scaler.pkl')
label_encoders = joblib.load('models/production_v45/label_encoders.pkl')

# Load feature orders
dna_feature_order = joblib.load('models/production_v45/dna_feature_order.pkl')
temporal_feature_order = joblib.load('models/production_v45/temporal_feature_order.pkl')
industry_feature_order = joblib.load('models/production_v45/industry_feature_order.pkl')

print(f"\nDNA features expected: {len(dna_feature_order)}")
print(f"Temporal features expected: {len(temporal_feature_order)}")
print(f"Industry features expected: {len(industry_feature_order)}")

# Encode categorical features
categorical_features = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
for cat_feature in categorical_features:
    test_sample[cat_feature] = label_encoders[cat_feature].transform(test_sample[cat_feature])

# Helper functions
def calculate_camp_scores(df):
    """Calculate CAMP scores from base features."""
    capital_cols = ['funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd', 
                   'monthly_burn_usd', 'runway_months', 'investor_tier_primary', 'has_debt']
    advantage_cols = ['patent_count', 'network_effects_present', 'has_data_moat',
                     'regulatory_advantage_present', 'tech_differentiation_score',
                     'switching_cost_score', 'brand_strength_score', 'scalability_score']
    market_cols = ['sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
                  'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
                  'user_growth_rate_percent', 'net_dollar_retention_percent',
                  'competition_intensity', 'competitors_named_count']
    people_cols = ['founders_count', 'team_size_full_time', 'years_experience_avg',
                  'domain_expertise_years_avg', 'prior_startup_experience_count',
                  'prior_successful_exits_count', 'board_advisor_experience_score',
                  'advisors_count', 'team_diversity_percent', 'key_person_dependency']
    
    scores = pd.DataFrame(index=df.index)
    scores['capital_score'] = df[capital_cols].mean(axis=1).astype(float)
    scores['advantage_score'] = df[advantage_cols].mean(axis=1).astype(float)
    scores['market_score'] = df[market_cols].mean(axis=1).astype(float)
    scores['people_score'] = df[people_cols].mean(axis=1).astype(float)
    
    return scores

def prepare_dna_features(df):
    """Prepare features for DNA analyzer (45 base + 4 CAMP = 49)."""
    camp_scores = calculate_camp_scores(df)
    all_features = pd.concat([df[CANONICAL_FEATURES], camp_scores], axis=1)
    # Ensure correct feature order
    return all_features[dna_feature_order]

def prepare_temporal_features(df):
    """Prepare features for temporal model (45 base + 3 temporal = 48)."""
    temporal_features = pd.DataFrame(index=df.index)
    temporal_features['growth_momentum'] = (
        df['revenue_growth_rate_percent'] * 0.4 +
        df['user_growth_rate_percent'] * 0.3 +
        df['net_dollar_retention_percent'] * 0.3
    )
    temporal_features['efficiency_trend'] = (
        df['gross_margin_percent'] * 0.5 +
        (100 - df['burn_multiple'].clip(0, 100)) * 0.3 +
        df['ltv_cac_ratio'].clip(0, 10) * 10 * 0.2
    )
    temporal_features['stage_velocity'] = (
        df['funding_stage'] * 0.5 +
        df['product_stage'] * 0.3 +
        np.log1p(df['annual_revenue_run_rate']) / 20 * 0.2
    )
    all_features = pd.concat([df[CANONICAL_FEATURES], temporal_features], axis=1)
    # Ensure correct feature order
    return all_features[temporal_feature_order]

def prepare_industry_features(df):
    """Prepare features for industry model (45 base features only)."""
    # Ensure correct feature order
    return df[industry_feature_order]

# Test predictions
print("\nTesting predictions...")
X_base = test_sample[CANONICAL_FEATURES]

# DNA predictions
X_dna = prepare_dna_features(test_sample)
print(f"\nDNA input shape: {X_dna.shape}")
dna_pred = dna_model.predict_proba(X_dna)[:, 1]
print(f"DNA predictions - Mean: {dna_pred.mean():.3f}, Std: {dna_pred.std():.3f}")

# Temporal predictions
X_temporal = prepare_temporal_features(test_sample)
print(f"\nTemporal input shape: {X_temporal.shape}")
temporal_pred = temporal_model.predict_proba(X_temporal)[:, 1]
print(f"Temporal predictions - Mean: {temporal_pred.mean():.3f}, Std: {temporal_pred.std():.3f}")

# Industry predictions
X_industry = prepare_industry_features(test_sample)
print(f"\nIndustry input shape: {X_industry.shape}")
X_industry_scaled = industry_scaler.transform(X_industry)
industry_pred = industry_model.predict_proba(X_industry_scaled)[:, 1]
print(f"Industry predictions - Mean: {industry_pred.mean():.3f}, Std: {industry_pred.std():.3f}")

# Ensemble predictions
ensemble_features = np.column_stack([dna_pred, temporal_pred, industry_pred])
print(f"\nEnsemble input shape: {ensemble_features.shape}")
ensemble_pred = ensemble_model.predict_proba(ensemble_features)[:, 1]
print(f"Ensemble predictions - Mean: {ensemble_pred.mean():.3f}, Std: {ensemble_pred.std():.3f}")

# Calculate discrimination power
actual_success = test_sample['success'].values
success_probs = ensemble_pred[actual_success == 1]
failure_probs = ensemble_pred[actual_success == 0]

print(f"\n📊 Discrimination Power Analysis:")
print(f"Success cases: Mean prob = {success_probs.mean():.3f}, Std = {success_probs.std():.3f}")
print(f"Failure cases: Mean prob = {failure_probs.mean():.3f}, Std = {failure_probs.std():.3f}")
print(f"Discrimination: {(success_probs.mean() - failure_probs.mean()) * 100:.2f}%")

# Model agreement analysis
predictions_df = pd.DataFrame({
    'dna': dna_pred,
    'temporal': temporal_pred,
    'industry': industry_pred,
    'ensemble': ensemble_pred
})

# Calculate pairwise correlations
correlations = predictions_df.corr()
print(f"\n🤝 Model Agreement (Correlations):")
print(correlations.round(3))

# Check for any NaN predictions
print(f"\n🔍 NaN Check:")
print(f"DNA NaNs: {np.isnan(dna_pred).sum()}")
print(f"Temporal NaNs: {np.isnan(temporal_pred).sum()}")
print(f"Industry NaNs: {np.isnan(industry_pred).sum()}")
print(f"Ensemble NaNs: {np.isnan(ensemble_pred).sum()}")

# Sample predictions
print(f"\n📋 Sample Predictions (first 5):")
for i in range(5):
    print(f"Sample {i+1}: DNA={dna_pred[i]:.3f}, Temporal={temporal_pred[i]:.3f}, "
          f"Industry={industry_pred[i]:.3f}, Ensemble={ensemble_pred[i]:.3f}, "
          f"Actual={test_sample.iloc[i]['success']}")

print("\n✅ Test complete!")