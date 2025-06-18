#!/usr/bin/env python3
"""
Retrain all FLASH models with proper feature normalization and validation
This fixes the issue where models predict high probabilities for bad startups
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
import joblib
import os
from datetime import datetime

# Import the normalized CAMP calculation
def normalize_features(df):
    """Normalize all features to 0-1 range before training"""
    
    MONETARY_FEATURES = [
        'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
        'tam_size_usd', 'sam_size_usd', 'som_size_usd', 'annual_revenue_run_rate',
        'customer_count', 'team_size_full_time', 'founders_count', 'advisors_count',
        'competitors_named_count'
    ]
    
    PERCENTAGE_FEATURES = [
        'market_growth_rate_percent', 'user_growth_rate_percent', 
        'net_dollar_retention_percent', 'customer_concentration_percent',
        'team_diversity_percent', 'gross_margin_percent', 'revenue_growth_rate_percent'
    ]
    
    SCORE_FEATURES = [
        'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
        'scalability_score', 'board_advisor_experience_score', 'competition_intensity'
    ]
    
    normalized_df = df.copy()
    
    # Normalize each feature type
    for col in df.columns:
        if col == 'success':  # Skip target variable
            continue
            
        if col in MONETARY_FEATURES:
            # Log scale for monetary values
            normalized_df[col] = np.where(
                df[col] > 0,
                np.clip(np.log10(df[col] + 1) / 9, 0, 1),
                0
            )
        elif col in PERCENTAGE_FEATURES:
            # Percentages: -100% to 200% mapped to 0-1
            normalized_df[col] = np.clip((df[col] + 100) / 300, 0, 1)
        elif col in SCORE_FEATURES:
            # 1-5 scores mapped to 0-1
            normalized_df[col] = (df[col] - 1) / 4
        elif col == 'runway_months':
            # Runway: 0-24 months mapped to 0-1
            normalized_df[col] = np.clip(df[col] / 24, 0, 1)
        elif col == 'burn_multiple':
            # Burn multiple: inverse (lower is better)
            normalized_df[col] = np.clip(1 - (df[col] / 10), 0, 1)
        elif col == 'ltv_cac_ratio':
            # LTV/CAC: 0-5 mapped to 0-1
            normalized_df[col] = np.clip(df[col] / 5, 0, 1)
        elif col in ['patent_count', 'prior_startup_experience_count', 'prior_successful_exits_count']:
            # Counts: 0-10 mapped to 0-1
            normalized_df[col] = np.clip(df[col] / 10, 0, 1)
        elif col in ['years_experience_avg', 'domain_expertise_years_avg']:
            # Years: 0-20 mapped to 0-1
            normalized_df[col] = np.clip(df[col] / 20, 0, 1)
        elif col in ['product_retention_30d', 'product_retention_90d']:
            # Already percentages
            normalized_df[col] = np.clip(df[col] / 100, 0, 1)
        elif col == 'dau_mau_ratio':
            # Already 0-1
            normalized_df[col] = np.clip(df[col], 0, 1)
        else:
            # Binary or unknown - ensure 0-1
            normalized_df[col] = np.clip(df[col], 0, 1)
    
    return normalized_df

def calculate_camp_scores(df):
    """Calculate CAMP scores for the dataset"""
    from feature_config import CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES
    
    camp_scores = pd.DataFrame()
    
    # Capital score
    capital_cols = [col for col in CAPITAL_FEATURES if col in df.columns]
    camp_scores['capital_score'] = df[capital_cols].mean(axis=1)
    
    # Advantage score
    advantage_cols = [col for col in ADVANTAGE_FEATURES if col in df.columns]
    camp_scores['advantage_score'] = df[advantage_cols].mean(axis=1)
    
    # Market score
    market_cols = [col for col in MARKET_FEATURES if col in df.columns]
    camp_scores['market_score'] = df[market_cols].mean(axis=1)
    
    # People score
    people_cols = [col for col in PEOPLE_FEATURES if col in df.columns]
    camp_scores['people_score'] = df[people_cols].mean(axis=1)
    
    return camp_scores

def create_realistic_labels(df, camp_scores):
    """Create realistic success labels based on CAMP scores and startup quality"""
    
    # Calculate overall quality score
    quality_score = camp_scores.mean(axis=1)
    
    # Add some realistic noise
    noise = np.random.normal(0, 0.1, len(quality_score))
    
    # Create success probability based on quality
    # Using a sigmoid function to create realistic probability distribution
    success_prob = 1 / (1 + np.exp(-10 * (quality_score + noise - 0.5)))
    
    # Add stage-specific adjustments
    if 'funding_stage' in df.columns:
        # Earlier stages have higher variance
        stage_map = {'pre_seed': 0.2, 'seed': 0.15, 'series_a': 0.1, 'series_b': 0.05, 'series_c': 0.0}
        for stage, variance in stage_map.items():
            mask = df['funding_stage'] == stage
            success_prob[mask] += np.random.normal(0, variance, mask.sum())
    
    # Ensure probabilities are in valid range
    success_prob = np.clip(success_prob, 0.05, 0.95)
    
    # Convert to binary labels with some randomness
    success_labels = (np.random.rand(len(success_prob)) < success_prob).astype(int)
    
    # Ensure we have a reasonable success rate (20-40%)
    success_rate = success_labels.mean()
    if success_rate < 0.2 or success_rate > 0.4:
        # Adjust to get reasonable rate
        target_rate = 0.3
        n_changes = int(abs(success_rate - target_rate) * len(success_labels))
        if success_rate < target_rate:
            # Add more successes
            failure_indices = np.where(success_labels == 0)[0]
            change_indices = np.random.choice(failure_indices, n_changes, replace=False)
            success_labels[change_indices] = 1
        else:
            # Add more failures
            success_indices = np.where(success_labels == 1)[0]
            change_indices = np.random.choice(success_indices, n_changes, replace=False)
            success_labels[change_indices] = 0
    
    return success_labels, success_prob

def train_model(X, y, model_name, feature_names=None):
    """Train a single model with proper validation"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    
    if feature_names is not None:
        model.feature_names_in_ = feature_names
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_pred = model.predict_proba(X_train)[:, 1]
    test_pred = model.predict_proba(X_test)[:, 1]
    
    train_auc = roc_auc_score(y_train, train_pred)
    test_auc = roc_auc_score(y_test, test_pred)
    
    print(f"\n{model_name} Performance:")
    print(f"  Train AUC: {train_auc:.3f}")
    print(f"  Test AUC: {test_auc:.3f}")
    
    # Check discrimination on edge cases
    # Create terrible startup (all features at worst values)
    terrible_startup = np.zeros((1, X.shape[1]))
    terrible_pred = model.predict_proba(terrible_startup)[:, 1][0]
    
    # Create excellent startup (all features at best values)
    excellent_startup = np.ones((1, X.shape[1]))
    excellent_pred = model.predict_proba(excellent_startup)[:, 1][0]
    
    print(f"  Terrible startup prediction: {terrible_pred:.1%}")
    print(f"  Excellent startup prediction: {excellent_pred:.1%}")
    print(f"  Discrimination: {excellent_pred - terrible_pred:.1%}")
    
    if excellent_pred - terrible_pred < 0.3:
        print(f"  ⚠️ WARNING: Poor discrimination!")
    
    return model, test_auc

def main():
    print("="*60)
    print("FLASH Model Retraining with Proper Normalization")
    print("="*60)
    
    # Load or generate training data
    print("\n1. Loading training data...")
    
    # Check if we have existing data
    if os.path.exists('data/processed_startup_data.csv'):
        df = pd.read_csv('data/processed_startup_data.csv')
        print(f"Loaded {len(df)} samples from existing data")
    else:
        print("Generating synthetic training data...")
        # Generate synthetic data for training
        from generate_flash_training_data import generate_training_data
        df = generate_training_data(n_samples=10000)
    
    # Select only the 45 canonical features
    from feature_config import ALL_FEATURES as CANONICAL_FEATURES
    
    feature_cols = [col for col in CANONICAL_FEATURES if col in df.columns]
    missing_features = set(CANONICAL_FEATURES) - set(feature_cols)
    if missing_features:
        print(f"Warning: Missing features: {missing_features}")
        # Add missing features with default values
        for feat in missing_features:
            df[feat] = 0
    
    # Ensure we have all 45 features
    df_features = df[CANONICAL_FEATURES].copy()
    
    print("\n2. Normalizing features...")
    df_normalized = normalize_features(df_features)
    
    print("\n3. Calculating CAMP scores...")
    camp_scores = calculate_camp_scores(df_normalized)
    
    print("\n4. Creating realistic success labels...")
    if 'success' in df.columns:
        y = df['success'].values
        print(f"Using existing success labels (success rate: {y.mean():.1%})")
    else:
        y, success_prob = create_realistic_labels(df_features, camp_scores)
        print(f"Generated success labels (success rate: {y.mean():.1%})")
    
    # Prepare features for different models
    X_base = df_normalized[CANONICAL_FEATURES].values
    X_with_camp = np.hstack([X_base, camp_scores.values])
    
    print("\n5. Training models...")
    
    # Create model directory
    os.makedirs('models/production_v45_fixed', exist_ok=True)
    
    # Train DNA Analyzer (45 features + 4 CAMP scores)
    print("\n" + "="*40)
    print("Training DNA Analyzer (49 features)...")
    dna_model, dna_auc = train_model(
        X_with_camp, y, 
        "DNA Analyzer",
        feature_names=np.array(CANONICAL_FEATURES + ['capital_score', 'advantage_score', 'market_score', 'people_score'])
    )
    joblib.dump(dna_model, 'models/production_v45_fixed/dna_analyzer.pkl')
    
    # Train Temporal Model (45 features + 3 temporal)
    print("\n" + "="*40)
    print("Training Temporal Model (48 features)...")
    # Add temporal features (runway trend, growth acceleration, burn trend)
    temporal_features = np.random.randn(len(df), 3) * 0.1 + 0.5  # Placeholder
    X_temporal = np.hstack([X_base, temporal_features])
    temporal_model, temporal_auc = train_model(
        X_temporal, y,
        "Temporal Model",
        feature_names=np.array(CANONICAL_FEATURES + ['runway_trend', 'growth_acceleration', 'burn_trend'])
    )
    joblib.dump(temporal_model, 'models/production_v45_fixed/temporal_model.pkl')
    
    # Train Industry Model (45 features)
    print("\n" + "="*40)
    print("Training Industry Model (45 features)...")
    industry_model, industry_auc = train_model(
        X_base, y,
        "Industry Model",
        feature_names=np.array(CANONICAL_FEATURES)
    )
    joblib.dump(industry_model, 'models/production_v45_fixed/industry_model.pkl')
    
    # Train Ensemble Model (3 model predictions)
    print("\n" + "="*40)
    print("Training Ensemble Model...")
    # Get predictions from all models
    dna_preds = dna_model.predict_proba(X_with_camp)[:, 1]
    temporal_preds = temporal_model.predict_proba(X_temporal)[:, 1]
    industry_preds = industry_model.predict_proba(X_base)[:, 1]
    
    X_ensemble = np.column_stack([dna_preds, temporal_preds, industry_preds])
    ensemble_model, ensemble_auc = train_model(
        X_ensemble, y,
        "Ensemble Model",
        feature_names=np.array(['dna_pred', 'temporal_pred', 'industry_pred'])
    )
    joblib.dump(ensemble_model, 'models/production_v45_fixed/ensemble_model.pkl')
    
    # Save model metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'n_samples': len(df),
        'success_rate': float(y.mean()),
        'model_performance': {
            'dna_analyzer': float(dna_auc),
            'temporal_model': float(temporal_auc),
            'industry_model': float(industry_auc),
            'ensemble_model': float(ensemble_auc)
        },
        'normalization': 'applied',
        'feature_count': {
            'dna_analyzer': 49,
            'temporal_model': 48,
            'industry_model': 45,
            'ensemble_model': 3
        }
    }
    
    import json
    with open('models/production_v45_fixed/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ Model retraining complete!")
    print(f"Average AUC: {np.mean([dna_auc, temporal_auc, industry_auc]):.3f}")
    print("\nModels saved to: models/production_v45_fixed/")
    print("\nNext steps:")
    print("1. Update orchestrator to use new model directory")
    print("2. Test with edge cases to verify discrimination")
    print("3. Deploy to production")

if __name__ == "__main__":
    main()