#!/usr/bin/env python3
"""
Hyperparameter optimization for FLASH models using the same 45 features.
Uses Optuna for Bayesian optimization to find better parameters.
"""
import numpy as np
import pandas as pd
import optuna
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
import json

# Same 45 features as training
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

def objective(trial, X, y, cat_indices):
    """Optuna objective function for hyperparameter tuning."""
    
    # Suggest hyperparameters
    params = {
        'iterations': trial.suggest_int('iterations', 500, 3000),
        'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
        'depth': trial.suggest_int('depth', 4, 12),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 0.1, 10.0, log=True),
        'random_strength': trial.suggest_float('random_strength', 0.0, 1.0),
        'border_count': trial.suggest_int('border_count', 32, 255),
        'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 1, 50),
        
        # Advanced parameters
        'grow_policy': trial.suggest_categorical('grow_policy', ['SymmetricTree', 'Depthwise', 'Lossguide']),
        'bootstrap_type': trial.suggest_categorical('bootstrap_type', ['Bayesian', 'Bernoulli', 'MVS']),
        
        # Fixed parameters
        'loss_function': 'Logloss',
        'eval_metric': 'AUC',
        'random_seed': 42,
        'early_stopping_rounds': 100,
        'use_best_model': True,
        'verbose': False
    }
    
    # Handle bootstrap-specific parameters
    if params['bootstrap_type'] == 'Bayesian':
        params['bagging_temperature'] = trial.suggest_float('bagging_temperature', 0.0, 5.0)
    elif params['bootstrap_type'] == 'Bernoulli':
        params['subsample'] = trial.suggest_float('subsample', 0.5, 1.0)
    
    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = []
    
    for train_idx, val_idx in cv.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        train_pool = Pool(X_train, y_train, cat_features=cat_indices)
        val_pool = Pool(X_val, y_val, cat_features=cat_indices)
        
        model = CatBoostClassifier(**params)
        model.fit(train_pool, eval_set=val_pool, plot=False)
        
        val_pred = model.predict_proba(X_val)[:, 1]
        cv_scores.append(roc_auc_score(y_val, val_pred))
    
    return np.mean(cv_scores)

def optimize_models(data_path, n_trials=100):
    """Run hyperparameter optimization."""
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Ensure we only use the 45 features
    X = df[FEATURES]
    y = df['success'].astype(int)
    
    # Get categorical indices
    cat_indices = [i for i, f in enumerate(FEATURES) if f in CATEGORICAL_FEATURES]
    
    print(f"Optimizing hyperparameters with {n_trials} trials...")
    print(f"Using {len(FEATURES)} features (no new features added)")
    
    # Create study
    study = optuna.create_study(
        direction='maximize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner()
    )
    
    # Optimize
    study.optimize(
        lambda trial: objective(trial, X, y, cat_indices),
        n_trials=n_trials,
        show_progress_bar=True
    )
    
    # Best parameters
    print("\nBest parameters found:")
    for key, value in study.best_params.items():
        print(f"  {key}: {value}")
    
    print(f"\nBest CV AUC: {study.best_value:.4f}")
    
    # Save results
    results = {
        'best_params': study.best_params,
        'best_auc': study.best_value,
        'n_trials': n_trials,
        'feature_count': len(FEATURES)
    }
    
    with open('optimized_hyperparameters.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return study.best_params

def train_optimized_model(data_path, params):
    """Train model with optimized parameters."""
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df['success'].astype(int)
    
    cat_indices = [i for i, f in enumerate(FEATURES) if f in CATEGORICAL_FEATURES]
    
    # Train with optimized parameters
    model = CatBoostClassifier(**params)
    
    # Use 80-20 split for final evaluation
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    train_pool = Pool(X_train, y_train, cat_features=cat_indices)
    test_pool = Pool(X_test, y_test, cat_features=cat_indices)
    
    model.fit(train_pool, eval_set=test_pool, plot=False)
    
    # Evaluate
    test_pred = model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, test_pred)
    
    print(f"\nOptimized model test AUC: {test_auc:.4f}")
    
    # Save optimized model
    model.save_model('models/optimized_model.cbm')
    
    return model, test_auc

if __name__ == "__main__":
    data_path = "data/final_100k_dataset_45features.csv"
    
    # Optimize hyperparameters with fewer trials for faster results
    best_params = optimize_models(data_path, n_trials=20)
    
    # Train with best parameters
    model, final_auc = train_optimized_model(data_path, best_params)
    
    print(f"\nExpected AUC improvement: {final_auc - 0.773:.4f}")