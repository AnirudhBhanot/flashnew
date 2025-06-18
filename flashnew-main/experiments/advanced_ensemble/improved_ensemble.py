#!/usr/bin/env python3
"""
Improved ensemble using multiple algorithms with the same 45 features.
No new features - just better model diversity.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
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

def prepare_data_for_models(df):
    """Prepare data with proper encoding for different models."""
    X = df[FEATURES].copy()
    y = df['success'].astype(int)
    
    # Encode categoricals for tree-based models that need numeric
    from sklearn.preprocessing import LabelEncoder
    
    X_encoded = X.copy()
    label_encoders = {}
    
    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X[col].fillna('unknown'))
        label_encoders[col] = le
    
    return X, X_encoded, y, label_encoders

def create_diverse_models():
    """Create diverse models that handle the same 45 features differently."""
    
    models = {
        # CatBoost - handles categoricals natively
        'catboost_1': CatBoostClassifier(
            iterations=1500,
            learning_rate=0.02,
            depth=8,
            l2_leaf_reg=3,
            random_seed=42,
            verbose=False
        ),
        
        'catboost_2': CatBoostClassifier(
            iterations=1000,
            learning_rate=0.05,
            depth=6,
            l2_leaf_reg=5,
            grow_policy='Lossguide',
            random_seed=43,
            verbose=False
        ),
        
        # XGBoost - different splitting criteria
        'xgboost': XGBClassifier(
            n_estimators=1000,
            learning_rate=0.02,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        ),
        
        # LightGBM - different tree structure
        'lightgbm': LGBMClassifier(
            n_estimators=1000,
            learning_rate=0.02,
            num_leaves=64,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbose=-1
        ),
        
        # Random Forest - bagging approach
        'random_forest': RandomForestClassifier(
            n_estimators=500,
            max_depth=12,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            n_jobs=-1
        ),
        
        # Extra Trees - more randomness
        'extra_trees': ExtraTreesClassifier(
            n_estimators=500,
            max_depth=12,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            n_jobs=-1
        )
    }
    
    return models

def train_ensemble_with_blending(data_path):
    """Train ensemble using blending (out-of-fold predictions)."""
    print("Loading data...")
    df = pd.read_csv(data_path)
    X, X_encoded, y, label_encoders = prepare_data_for_models(df)
    
    # Split data
    X_train, X_test, X_train_enc, X_test_enc, y_train, y_test = train_test_split(
        X, X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")
    
    models = create_diverse_models()
    
    # Store out-of-fold predictions for blending
    n_folds = 5
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    # Initialize blend features
    blend_train = np.zeros((len(X_train), len(models)))
    blend_test = np.zeros((len(X_test), len(models)))
    
    print("\nTraining models with out-of-fold predictions...")
    
    for idx, (name, model) in enumerate(models.items()):
        print(f"\nTraining {name}...")
        
        # Store test predictions from each fold
        test_preds_folds = []
        
        # Get out-of-fold predictions
        oof_preds = np.zeros(len(X_train))
        
        for fold, (train_idx, val_idx) in enumerate(cv.split(X_train, y_train)):
            # Use appropriate data format for each model
            if 'catboost' in name:
                # CatBoost handles categoricals
                X_fold_train = X_train.iloc[train_idx]
                X_fold_val = X_train.iloc[val_idx]
                
                cat_indices = [i for i, f in enumerate(FEATURES) if f in CATEGORICAL_FEATURES]
                model.fit(X_fold_train, y_train.iloc[train_idx], 
                         cat_features=cat_indices,
                         eval_set=(X_fold_val, y_train.iloc[val_idx]),
                         early_stopping_rounds=50)
                
                oof_preds[val_idx] = model.predict_proba(X_fold_val)[:, 1]
                test_preds_folds.append(model.predict_proba(X_test)[:, 1])
                
            else:
                # Other models need encoded features
                X_fold_train = X_train_enc.iloc[train_idx]
                X_fold_val = X_train_enc.iloc[val_idx]
                
                model.fit(X_fold_train, y_train.iloc[train_idx])
                
                oof_preds[val_idx] = model.predict_proba(X_fold_val)[:, 1]
                test_preds_folds.append(model.predict_proba(X_test_enc)[:, 1])
        
        # Average test predictions across folds
        blend_train[:, idx] = oof_preds
        blend_test[:, idx] = np.mean(test_preds_folds, axis=0)
        
        # Report OOF performance
        oof_auc = roc_auc_score(y_train, oof_preds)
        print(f"  {name} OOF AUC: {oof_auc:.4f}")
    
    # Train meta-learner on blend features
    print("\nTraining meta-learner...")
    from sklearn.linear_model import LogisticRegression
    
    meta_model = LogisticRegression(C=0.1, random_state=42)
    meta_model.fit(blend_train, y_train)
    
    # Final predictions
    final_train_pred = meta_model.predict_proba(blend_train)[:, 1]
    final_test_pred = meta_model.predict_proba(blend_test)[:, 1]
    
    # Evaluate
    train_auc = roc_auc_score(y_train, final_train_pred)
    test_auc = roc_auc_score(y_test, final_test_pred)
    
    print("\n" + "="*50)
    print("ENSEMBLE RESULTS (Same 45 Features)")
    print("="*50)
    print(f"Train AUC: {train_auc:.4f}")
    print(f"Test AUC: {test_auc:.4f}")
    
    # Compare with individual models
    print("\nIndividual model test performance:")
    for idx, name in enumerate(models.keys()):
        model_auc = roc_auc_score(y_test, blend_test[:, idx])
        print(f"  {name}: {model_auc:.4f}")
    
    # Save predictions for analysis
    results_df = pd.DataFrame({
        'y_true': y_test,
        'ensemble_pred': final_test_pred,
        **{f'{name}_pred': blend_test[:, idx] for idx, name in enumerate(models.keys())}
    })
    results_df.to_csv('ensemble_predictions.csv', index=False)
    
    return test_auc

if __name__ == "__main__":
    data_path = "data/final_100k_dataset_45features.csv"
    final_auc = train_ensemble_with_blending(data_path)
    
    print(f"\nExpected AUC improvement: {final_auc - 0.773:.4f}")
    print("\nNOTE: Using same 45 features - no data compatibility issues!")