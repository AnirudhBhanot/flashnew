#!/usr/bin/env python3
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# Ensure output directory exists
os.makedirs('models/production_v45_fixed', exist_ok=True)

# Load the dataset
print("Loading dataset...")
data = pd.read_csv('data/final_100k_dataset_45features.csv')

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

# Encode categorical features
categorical_features = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
label_encoders = {}

for cat_feature in categorical_features:
    le = LabelEncoder()
    data[cat_feature] = le.fit_transform(data[cat_feature])
    label_encoders[cat_feature] = le

# Prepare feature sets for ensemble  
X_base = data[CANONICAL_FEATURES]
y = data['success']

# Load the three trained models
print("\nLoading component models...")
dna_model = joblib.load('models/production_v45_fixed/dna_analyzer.pkl')
temporal_model = joblib.load('models/production_v45_fixed/temporal_model.pkl')
industry_model = joblib.load('models/production_v45_fixed/industry_model.pkl')

# Load preprocessing components
industry_scaler = joblib.load('models/production_v45_fixed/industry_scaler.pkl')

# Split data for ensemble training
X_train, X_test, y_train, y_test = train_test_split(X_base, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining data shape: {X_train.shape}")
print(f"Test data shape: {X_test.shape}")

# Helper functions for feature preparation
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
    return pd.concat([df[CANONICAL_FEATURES], camp_scores], axis=1)

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
    return pd.concat([df[CANONICAL_FEATURES], temporal_features], axis=1)

def prepare_industry_features(df):
    """Prepare features for industry model (45 base features only)."""
    return df[CANONICAL_FEATURES]

# Generate predictions from component models
print("\nGenerating predictions from component models...")

# DNA predictions
X_dna_train = prepare_dna_features(X_train)
X_dna_test = prepare_dna_features(X_test)
dna_train_pred = dna_model.predict_proba(X_dna_train)[:, 1]
dna_test_pred = dna_model.predict_proba(X_dna_test)[:, 1]

# Temporal predictions
X_temporal_train = prepare_temporal_features(X_train)
X_temporal_test = prepare_temporal_features(X_test)
temporal_train_pred = temporal_model.predict_proba(X_temporal_train)[:, 1]
temporal_test_pred = temporal_model.predict_proba(X_temporal_test)[:, 1]

# Industry predictions
X_industry_train = prepare_industry_features(X_train)
X_industry_test = prepare_industry_features(X_test)
X_industry_train_scaled = industry_scaler.transform(X_industry_train)
X_industry_test_scaled = industry_scaler.transform(X_industry_test)
industry_train_pred = industry_model.predict_proba(X_industry_train_scaled)[:, 1]
industry_test_pred = industry_model.predict_proba(X_industry_test_scaled)[:, 1]

# Create ensemble features
ensemble_train = np.column_stack([dna_train_pred, temporal_train_pred, industry_train_pred])
ensemble_test = np.column_stack([dna_test_pred, temporal_test_pred, industry_test_pred])

print(f"\nEnsemble training shape: {ensemble_train.shape}")
print(f"Ensemble test shape: {ensemble_test.shape}")

# Train ensemble model
print("\nTraining ensemble model...")
ensemble_model = GradientBoostingClassifier(
    n_estimators=50,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)
ensemble_model.fit(ensemble_train, y_train)

# Evaluate ensemble
ensemble_pred = ensemble_model.predict_proba(ensemble_test)[:, 1]
ensemble_auc = roc_auc_score(y_test, ensemble_pred)
print(f"Ensemble Model: {ensemble_auc:.4f} AUC")

# Save the ensemble model and metadata
print("\nSaving ensemble model...")
joblib.dump(ensemble_model, 'models/production_v45_fixed/ensemble_model.pkl')

# Save label encoders for categorical features
joblib.dump(label_encoders, 'models/production_v45_fixed/label_encoders.pkl')

# Create a metadata file for the ensemble
metadata = {
    'model_type': 'ensemble',
    'component_models': ['dna_analyzer', 'temporal_model', 'industry_model'],
    'n_features': 3,
    'feature_names': ['dna_probability', 'temporal_probability', 'industry_probability'],
    'auc_score': ensemble_auc,
    'canonical_features': CANONICAL_FEATURES,
    'categorical_features': categorical_features
}

import json
with open('models/production_v45_fixed/ensemble_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n✅ Ensemble model training complete!")
print(f"   Saved to: models/production_v45_fixed/ensemble_model.pkl")
print(f"   Performance: {ensemble_auc:.4f} AUC")