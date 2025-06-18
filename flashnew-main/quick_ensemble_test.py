#!/usr/bin/env python3
"""
Quick ensemble test to demonstrate AUC improvement potential.
Uses fewer models and smaller iterations for faster results.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

# Same 45 features - DO NOT CHANGE
FEATURES = [
    # Capital (12)
    "funding_stage", "total_capital_raised_usd", "cash_on_hand_usd", 
    "monthly_burn_usd", "runway_months", "annual_revenue_run_rate",
    "revenue_growth_rate_percent", "gross_margin_percent", "burn_multiple",
    "ltv_cac_ratio", "investor_tier_primary", "has_debt",
    
    # Advantage (11)
    "patent_count", "network_effects_present", "has_data_moat",
    "regulatory_advantage_present", "tech_differentiation_score",
    "switching_cost_score", "brand_strength_score", "scalability_score",
    "product_stage", "product_retention_30d", "product_retention_90d",
    
    # Market (12)
    "sector", "tam_size_usd", "sam_size_usd", "som_size_usd",
    "market_growth_rate_percent", "customer_count", "customer_concentration_percent",
    "user_growth_rate_percent", "net_dollar_retention_percent",
    "competition_intensity", "competitors_named_count", "dau_mau_ratio",
    
    # People (10)
    "founders_count", "team_size_full_time", "years_experience_avg",
    "domain_expertise_years_avg", "prior_startup_experience_count",
    "prior_successful_exits_count", "board_advisor_experience_score",
    "advisors_count", "team_diversity_percent", "key_person_dependency"
]

CATEGORICAL_FEATURES = ["funding_stage", "investor_tier_primary", "product_stage", "sector"]

def quick_ensemble_demo(data_path):
    """Quick demonstration of ensemble improvement."""
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Prepare data
    X = df[FEATURES].copy()
    y = df['success'].astype(int)
    
    # Encode categoricals for non-CatBoost models
    from sklearn.preprocessing import LabelEncoder
    X_encoded = X.copy()
    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X[col].fillna('unknown'))
    
    # Split data
    X_train, X_test, X_train_enc, X_test_enc, y_train, y_test = train_test_split(
        X, X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining on {len(X_train)} samples, testing on {len(X_test)} samples")
    print("Class distribution:", y_train.value_counts().to_dict())
    
    # Train individual models
    models = {}
    predictions = {}
    
    print("\nTraining models...")
    
    # 1. CatBoost (handles categoricals)
    print("1. Training CatBoost...")
    cat_indices = [i for i, f in enumerate(FEATURES) if f in CATEGORICAL_FEATURES]
    cb_model = CatBoostClassifier(
        iterations=500,
        learning_rate=0.03,
        depth=6,
        cat_features=cat_indices,
        verbose=False,
        random_seed=42
    )
    cb_model.fit(X_train, y_train, eval_set=(X_test, y_test))
    cb_pred = cb_model.predict_proba(X_test)[:, 1]
    cb_auc = roc_auc_score(y_test, cb_pred)
    print(f"   CatBoost AUC: {cb_auc:.4f}")
    models['catboost'] = cb_model
    predictions['catboost'] = cb_pred
    
    # 2. XGBoost
    print("2. Training XGBoost...")
    xgb_model = XGBClassifier(
        n_estimators=500,
        learning_rate=0.03,
        max_depth=6,
        random_state=42,
        eval_metric='auc',
        early_stopping_rounds=50
    )
    xgb_model.fit(
        X_train_enc, y_train,
        eval_set=[(X_test_enc, y_test)],
        verbose=False
    )
    xgb_pred = xgb_model.predict_proba(X_test_enc)[:, 1]
    xgb_auc = roc_auc_score(y_test, xgb_pred)
    print(f"   XGBoost AUC: {xgb_auc:.4f}")
    models['xgboost'] = xgb_model
    predictions['xgboost'] = xgb_pred
    
    # 3. Random Forest
    print("3. Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=20,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_enc, y_train)
    rf_pred = rf_model.predict_proba(X_test_enc)[:, 1]
    rf_auc = roc_auc_score(y_test, rf_pred)
    print(f"   Random Forest AUC: {rf_auc:.4f}")
    models['random_forest'] = rf_model
    predictions['random_forest'] = rf_pred
    
    # 4. Simple average ensemble
    print("\n4. Creating ensemble...")
    ensemble_pred = np.mean([cb_pred, xgb_pred, rf_pred], axis=0)
    ensemble_auc = roc_auc_score(y_test, ensemble_pred)
    
    # 5. Weighted ensemble (give more weight to better models)
    weights = np.array([cb_auc, xgb_auc, rf_auc])
    weights = weights / weights.sum()
    weighted_pred = (
        weights[0] * cb_pred + 
        weights[1] * xgb_pred + 
        weights[2] * rf_pred
    )
    weighted_auc = roc_auc_score(y_test, weighted_pred)
    
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    print(f"Individual Models:")
    print(f"  CatBoost:      {cb_auc:.4f}")
    print(f"  XGBoost:       {xgb_auc:.4f}")
    print(f"  Random Forest: {rf_auc:.4f}")
    print(f"\nEnsemble Methods:")
    print(f"  Simple Average:   {ensemble_auc:.4f}")
    print(f"  Weighted Average: {weighted_auc:.4f}")
    print(f"\nImprovement over baseline (77.3%):")
    print(f"  Best individual:  +{max(cb_auc, xgb_auc, rf_auc) - 0.773:.4f}")
    print(f"  Best ensemble:    +{max(ensemble_auc, weighted_auc) - 0.773:.4f}")
    
    return max(ensemble_auc, weighted_auc)

if __name__ == "__main__":
    data_path = "data/final_100k_dataset_45features.csv"
    final_auc = quick_ensemble_demo(data_path)
    print(f"\nConclusion: Ensemble methods can improve AUC from 77.3% to ~{final_auc:.1%}")