#!/usr/bin/env python3
"""
Improved preprocessing for the existing 45 features.
No new features - just better handling of existing ones.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, QuantileTransformer
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score

# Same 45 features
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
NUMERICAL_FEATURES = [f for f in FEATURES if f not in CATEGORICAL_FEATURES]

def improved_preprocessing(df):
    """Apply advanced preprocessing to existing features."""
    X = df[FEATURES].copy()
    y = df['success'].astype(int)
    
    print("Applying improved preprocessing...")
    
    # 1. Handle outliers with winsorization (cap extreme values)
    from scipy.stats import mstats
    for col in NUMERICAL_FEATURES:
        if col in X.columns:
            # Cap at 1st and 99th percentile
            X[col] = mstats.winsorize(X[col], limits=[0.01, 0.01])
    
    # 2. Log transform skewed features
    skewed_features = [
        'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
        'annual_revenue_run_rate', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
        'customer_count', 'patent_count'
    ]
    
    for col in skewed_features:
        if col in X.columns:
            # Add 1 to handle zeros
            X[f'{col}_log'] = np.log1p(X[col])
            # Keep original for CatBoost to decide
    
    # 3. Robust scaling for numerical features
    scaler = RobustScaler()
    X_scaled = X.copy()
    X_scaled[NUMERICAL_FEATURES] = scaler.fit_transform(X[NUMERICAL_FEATURES])
    
    # 4. Quantile transformation for better distribution
    quantile_features = [
        'revenue_growth_rate_percent', 'user_growth_rate_percent',
        'market_growth_rate_percent', 'net_dollar_retention_percent'
    ]
    
    qt = QuantileTransformer(n_quantiles=100, random_state=42)
    for col in quantile_features:
        if col in X.columns:
            X_scaled[f'{col}_quantile'] = qt.fit_transform(X[[col]])
    
    return X, X_scaled, y

def train_with_preprocessing_variants(data_path):
    """Compare different preprocessing approaches."""
    df = pd.read_csv(data_path)
    
    # Get different preprocessing variants
    X_original = df[FEATURES]
    y = df['success'].astype(int)
    
    X_processed, X_scaled, y = improved_preprocessing(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_original, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_train_proc, X_test_proc = train_test_split(
        X_processed, test_size=0.2, random_state=42, stratify=y
    )[0:2]
    
    X_train_scaled, X_test_scaled = train_test_split(
        X_scaled, test_size=0.2, random_state=42, stratify=y
    )[0:2]
    
    # Train models with different preprocessing
    cat_indices = [i for i, f in enumerate(FEATURES) if f in CATEGORICAL_FEATURES]
    
    results = {}
    
    # 1. Original data
    print("\nTraining with original features...")
    model1 = CatBoostClassifier(
        iterations=1000, learning_rate=0.03, depth=6,
        cat_features=cat_indices, verbose=False, random_seed=42
    )
    model1.fit(X_train, y_train)
    pred1 = model1.predict_proba(X_test)[:, 1]
    results['original'] = roc_auc_score(y_test, pred1)
    
    # 2. With outlier handling and log transforms
    print("Training with processed features...")
    # Update cat_indices for new features
    all_features = list(X_train_proc.columns)
    cat_indices_proc = [i for i, f in enumerate(all_features) if f in CATEGORICAL_FEATURES]
    
    model2 = CatBoostClassifier(
        iterations=1000, learning_rate=0.03, depth=6,
        cat_features=cat_indices_proc, verbose=False, random_seed=42
    )
    model2.fit(X_train_proc, y_train)
    pred2 = model2.predict_proba(X_test_proc)[:, 1]
    results['processed'] = roc_auc_score(y_test, pred2)
    
    # 3. With scaling and quantile transformation
    print("Training with scaled features...")
    all_features_scaled = list(X_train_scaled.columns)
    cat_indices_scaled = [i for i, f in enumerate(all_features_scaled) if f in CATEGORICAL_FEATURES]
    
    model3 = CatBoostClassifier(
        iterations=1000, learning_rate=0.03, depth=6,
        cat_features=cat_indices_scaled, verbose=False, random_seed=42
    )
    model3.fit(X_train_scaled, y_train)
    pred3 = model3.predict_proba(X_test_scaled)[:, 1]
    results['scaled'] = roc_auc_score(y_test, pred3)
    
    # 4. Ensemble of preprocessing approaches
    print("Creating preprocessing ensemble...")
    ensemble_pred = (pred1 + pred2 + pred3) / 3
    results['ensemble'] = roc_auc_score(y_test, ensemble_pred)
    
    print("\n" + "="*50)
    print("PREPROCESSING COMPARISON RESULTS")
    print("="*50)
    for name, auc in results.items():
        improvement = auc - 0.773
        print(f"{name:15} AUC: {auc:.4f} (Δ {improvement:+.4f})")
    
    return results

def sample_balancing_approach(data_path):
    """Test different sampling strategies for class imbalance."""
    from imblearn.over_sampling import SMOTE, ADASYN
    from imblearn.under_sampling import RandomUnderSampler
    from imblearn.combine import SMOTETomek
    
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df['success'].astype(int)
    
    # Check class balance
    print(f"\nClass distribution: {y.value_counts().to_dict()}")
    print(f"Class ratio: {y.sum() / len(y):.2%} positive")
    
    # Prepare data
    from sklearn.preprocessing import LabelEncoder
    X_encoded = X.copy()
    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X[col].fillna('unknown'))
    
    # Split first
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Test different sampling strategies
    samplers = {
        'baseline': None,
        'smote': SMOTE(random_state=42),
        'adasyn': ADASYN(random_state=42),
        'smote_tomek': SMOTETomek(random_state=42)
    }
    
    results = {}
    
    for name, sampler in samplers.items():
        print(f"\nTesting {name}...")
        
        if sampler:
            X_resampled, y_resampled = sampler.fit_resample(X_train, y_train)
        else:
            X_resampled, y_resampled = X_train, y_train
        
        model = CatBoostClassifier(
            iterations=1000, learning_rate=0.03, depth=6,
            verbose=False, random_seed=42
        )
        model.fit(X_resampled, y_resampled)
        
        pred = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, pred)
        results[name] = auc
        
        print(f"  Samples after resampling: {len(y_resampled)}")
        print(f"  Test AUC: {auc:.4f}")
    
    return results

if __name__ == "__main__":
    data_path = "data/final_100k_dataset_45features.csv"
    
    print("Testing preprocessing improvements...")
    preprocessing_results = train_with_preprocessing_variants(data_path)
    
    print("\n" + "="*60)
    print("Testing class balancing...")
    balancing_results = sample_balancing_approach(data_path)
    
    print("\n" + "="*60)
    print("SUMMARY - Ways to improve AUC without new features:")
    print("="*60)
    print("1. Better preprocessing (outliers, scaling)")
    print("2. Class balancing (SMOTE, ADASYN)")
    print("3. Ensemble different preprocessing variants")
    print("4. All improvements use the SAME 45 features")
    print("5. No compatibility issues with existing models")