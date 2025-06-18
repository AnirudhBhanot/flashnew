#!/usr/bin/env python3
"""
Train FLASH models with ONLY the canonical 45 features
No feature engineering - keep it simple and consistent
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
import xgboost as xgb
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# The canonical 45 features in order
FEATURES_45 = [
    # Capital (7)
    'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
    'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt',
    
    # Advantage (8)
    'patent_count', 'network_effects_present', 'has_data_moat',
    'regulatory_advantage_present', 'tech_differentiation_score',
    'switching_cost_score', 'brand_strength_score', 'scalability_score',
    
    # Market (11)
    'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
    'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
    'user_growth_rate_percent', 'net_dollar_retention_percent',
    'competition_intensity', 'competitors_named_count',
    
    # People (10)
    'founders_count', 'team_size_full_time', 'years_experience_avg',
    'domain_expertise_years_avg', 'prior_startup_experience_count',
    'prior_successful_exits_count', 'board_advisor_experience_score',
    'advisors_count', 'team_diversity_percent', 'key_person_dependency',
    
    # Product (9)
    'product_stage', 'product_retention_30d', 'product_retention_90d',
    'dau_mau_ratio', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
    'gross_margin_percent', 'ltv_cac_ratio', 'funding_stage'
]

def load_and_prepare_data():
    """Load the 100k dataset and prepare ONLY 45 features"""
    
    print("📊 Loading 100k realistic startup dataset...")
    
    # Load data
    df = pd.read_csv('generated_100k_dataset.csv')
    
    print(f"✅ Loaded {len(df)} companies")
    print(f"   Success rate: {df['success'].mean():.1%}")
    
    # Map columns to the 45 features
    feature_mapping = {
        # Direct mappings
        'total_capital_raised_usd': 'total_capital_raised_usd',
        'cash_on_hand_usd': 'cash_on_hand_usd',
        'monthly_burn_usd': 'monthly_burn_usd',
        'runway_months': 'runway_months',
        'burn_multiple': 'burn_multiple',
        'investor_tier_primary': 'investor_tier_primary',
        'has_debt': 'has_debt',
        'patent_count': 'patent_count',
        'network_effects_present': 'network_effects_present',
        'has_data_moat': 'has_data_moat',
        'regulatory_advantage_present': 'regulatory_advantage_present',
        'tech_differentiation_score': 'tech_differentiation_score',
        'switching_cost_score': 'switching_cost_score',
        'brand_strength_score': 'brand_strength_score',
        'scalability_score': 'scalability_score',
        'sector': 'sector',
        'tam_size_usd': 'tam_size_usd',
        'sam_size_usd': 'sam_size_usd',
        'som_size_usd': 'som_size_usd',
        'market_growth_rate_percent': 'market_growth_rate_percent',
        'customer_count': 'customer_count',
        'customer_concentration_percent': 'customer_concentration_percent',
        'user_growth_rate_percent': 'user_growth_rate_percent',
        'net_dollar_retention_percent': 'net_dollar_retention_percent',
        'competition_intensity': 'competition_intensity',
        'competitors_named_count': 'competitors_named_count',
        'founders_count': 'founders_count',
        'team_size_full_time': 'team_size_full_time',
        'years_experience_avg': 'years_experience_avg',
        'domain_expertise_years_avg': 'domain_expertise_years_avg',
        'prior_startup_experience_count': 'prior_startup_experience_count',
        'prior_successful_exits_count': 'prior_successful_exits_count',
        'board_advisor_experience_score': 'board_advisor_experience_score',
        'advisors_count': 'advisors_count',
        'team_diversity_percent': 'team_diversity_percent',
        'key_person_dependency': 'key_person_dependency',
        'product_stage': 'product_stage',
        'product_retention_30d': 'product_retention_30d',
        'product_retention_90d': 'product_retention_90d',
        'dau_mau_ratio': 'dau_mau_ratio',
        'annual_revenue_run_rate': 'annual_revenue_run_rate',
        'revenue_growth_rate_percent': 'revenue_growth_rate_percent',
        'gross_margin_percent': 'gross_margin_percent',
        'ltv_cac_ratio': 'ltv_cac_ratio',
        'funding_stage': 'funding_stage'
    }
    
    # Create X with exactly 45 features
    X = pd.DataFrame()
    
    for feature in FEATURES_45:
        if feature in df.columns:
            X[feature] = df[feature]
        else:
            # Handle missing mappings
            if feature == 'monthly_burn_usd':
                X[feature] = df.get('monthly_burn_usd', df.get('cash_on_hand_usd', 0) / 12)
            elif feature == 'net_dollar_retention_percent':
                X[feature] = df.get('net_dollar_retention_percent', 100)
            else:
                print(f"   ⚠️ Missing {feature}, using default")
                X[feature] = 0
    
    # Encode categorical features
    categorical_features = ['sector', 'product_stage', 'investor_tier_primary', 'funding_stage']
    
    for cat_feature in categorical_features:
        if cat_feature in X.columns:
            # Simple label encoding
            if X[cat_feature].dtype == 'object':
                unique_vals = X[cat_feature].unique()
                mapping = {val: i for i, val in enumerate(unique_vals)}
                X[cat_feature] = X[cat_feature].map(mapping).fillna(0)
    
    # Ensure all features are numeric
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)
    
    # Get labels
    y = df['success'].astype(int)
    
    print(f"\n✅ Prepared dataset with exactly {X.shape[1]} features")
    assert X.shape[1] == 45, f"Expected 45 features, got {X.shape[1]}"
    
    return X, y

def train_models(X_train, y_train, X_val, y_val):
    """Train simple models on 45 features"""
    
    print("\n🤖 Training Models on 45 Features...")
    
    # Random Forest
    print("\n🌲 Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict_proba(X_val)[:, 1]
    rf_auc = roc_auc_score(y_val, rf_pred)
    print(f"   Random Forest AUC: {rf_auc:.4f}")
    
    # XGBoost
    print("\n🚀 Training XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=10,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict_proba(X_val)[:, 1]
    xgb_auc = roc_auc_score(y_val, xgb_pred)
    print(f"   XGBoost AUC: {xgb_auc:.4f}")
    
    # Ensemble
    ensemble_pred = (rf_pred + xgb_pred) / 2
    ensemble_auc = roc_auc_score(y_val, ensemble_pred)
    print(f"\n🎯 Ensemble AUC: {ensemble_auc:.4f}")
    
    return rf_model, xgb_model

def save_models_45(rf_model, xgb_model, scaler):
    """Save models trained on 45 features"""
    
    print("\n💾 Saving 45-Feature Models...")
    
    import os
    os.makedirs('models/production_45_features', exist_ok=True)
    
    # Save with clear names
    joblib.dump(rf_model, 'models/production_45_features/random_forest_45.pkl')
    joblib.dump(xgb_model, 'models/production_45_features/xgboost_45.pkl')
    joblib.dump(scaler, 'models/production_45_features/scaler_45.pkl')
    
    # Also save for production
    joblib.dump(rf_model, 'models/production_v45/dna_analyzer.pkl')
    joblib.dump(xgb_model, 'models/production_v45/temporal_model.pkl')
    joblib.dump(xgb_model, 'models/production_v45/industry_model.pkl')
    joblib.dump(rf_model, 'models/production_v45/ensemble_model.pkl')
    joblib.dump(scaler, 'models/production_v45/feature_scaler.pkl')
    
    # Save feature order
    with open('models/production_v45/feature_order.json', 'w') as f:
        json.dump(FEATURES_45, f, indent=2)
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'dataset_size': 100000,
        'feature_count': 45,
        'features': FEATURES_45,
        'models': {
            'random_forest': 'RandomForestClassifier',
            'xgboost': 'XGBClassifier'
        }
    }
    
    with open('models/production_45_features/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Models saved for 45-feature system")

def main():
    """Main training pipeline - 45 features only"""
    
    print("🚀 FLASH Model Training - 45 Features Only")
    print("=" * 60)
    print("Training models on EXACTLY 45 canonical features")
    print("No feature engineering - maintaining consistency")
    print("=" * 60)
    
    # Load and prepare data
    X, y = load_and_prepare_data()
    
    # Verify 45 features
    print(f"\n📋 Feature verification: {len(X.columns)} features")
    for i, feature in enumerate(X.columns):
        if i % 5 == 0:
            print()
        print(f"{feature:30}", end="")
    print()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"\n📊 Data Split:")
    print(f"   Training: {len(X_train):,} samples")
    print(f"   Validation: {len(X_val):,} samples")
    print(f"   Test: {len(X_test):,} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Verify scaler expects 45 features
    print(f"\n✅ Scaler configured for {scaler.n_features_in_} features")
    
    # Train models
    rf_model, xgb_model = train_models(
        X_train_scaled, y_train, X_val_scaled, y_val
    )
    
    # Test evaluation
    print("\n🎯 Final Test Set Evaluation...")
    rf_test_pred = rf_model.predict_proba(X_test_scaled)[:, 1]
    xgb_test_pred = xgb_model.predict_proba(X_test_scaled)[:, 1]
    ensemble_test_pred = (rf_test_pred + xgb_test_pred) / 2
    
    test_auc = roc_auc_score(y_test, ensemble_test_pred)
    print(f"   Test AUC: {test_auc:.4f}")
    
    # Save models
    save_models_45(rf_model, xgb_model, scaler)
    
    print("\n" + "="*60)
    print("🎉 Training Complete!")
    print(f"   Models trained on exactly 45 features")
    print(f"   Test AUC: {test_auc:.4f}")
    print("   Ready for production deployment!")

if __name__ == "__main__":
    main()