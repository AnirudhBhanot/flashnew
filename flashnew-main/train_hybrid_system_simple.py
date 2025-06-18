#!/usr/bin/env python3
"""
Simplified Pattern Model Training for Hybrid System
Trains pattern models using contractual architecture for hybrid orchestration
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import roc_auc_score
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Feature mappings for the dataset
FEATURE_MAPPING = {
    'revenue_growth_rate': 'revenue_growth_rate_percent',
    'net_revenue_retention': 'net_dollar_retention_percent',
    'customer_growth_rate': 'user_growth_rate_percent',
    'annual_recurring_revenue_millions': 'annual_revenue_run_rate',
    'customer_acquisition_cost': 'ltv_cac_ratio',  # Use proxy
    'target_enterprise': 'funding_stage',  # Proxy: Series B+ = enterprise
    'uses_ai_ml': 'tech_differentiation_score',  # Proxy: score > 4 = AI/ML
    'technical_founder': 'domain_expertise_years_avg',  # Proxy: > 5 years
    'platform_business': 'network_effects_present',
}

def detect_startup_patterns(df):
    """Detect patterns based on available features"""
    patterns = {}
    
    # Efficient Growth: High growth with low burn
    patterns['efficient_growth'] = (
        (df['revenue_growth_rate_percent'] > 100) & 
        (df['burn_multiple'] < 1.5) &
        (df['runway_months'] > 18)
    ).astype(int)
    
    # VC Hypergrowth: High capital, high growth
    patterns['vc_hypergrowth'] = (
        (df['total_capital_raised_usd'] > 10000000) & 
        (df['revenue_growth_rate_percent'] > 200) &
        (df['team_size_full_time'] > 30)
    ).astype(int)
    
    # Bootstrap Profitable: Low capital, sustainable
    patterns['bootstrap_profitable'] = (
        (df['burn_multiple'] < 1.0) & 
        (df['total_capital_raised_usd'] < 1000000) &
        (df['runway_months'] > 24)
    ).astype(int)
    
    # B2B SaaS: High retention, enterprise focus
    patterns['b2b_saas'] = (
        (df['net_dollar_retention_percent'] > 110) & 
        (df['funding_stage'].isin(['Series B', 'Series C', 'Series C+'])) &
        (df['annual_revenue_run_rate'] > 1000000)
    ).astype(int)
    
    # AI/ML Core: Tech differentiation
    patterns['ai_ml_core'] = (
        (df['tech_differentiation_score'] > 4) & 
        (df['patent_count'] > 5) &
        (df['domain_expertise_years_avg'] > 5)
    ).astype(int)
    
    # Platform Network: Network effects
    patterns['platform_network'] = (
        (df['network_effects_present'] == True) & 
        (df['user_growth_rate_percent'] > 100) &
        (df['scalability_score'] > 4)
    ).astype(int)
    
    # Product-Led Growth
    patterns['product_led'] = (
        (df['product_retention_30d'] > 0.7) & 
        (df['product_retention_90d'] > 0.5) &
        (df['dau_mau_ratio'] > 0.5)
    ).astype(int)
    
    # Deep Tech R&D
    patterns['deep_tech'] = (
        (df['patent_count'] > 10) & 
        (df['tech_differentiation_score'] > 4.5) &
        (df['domain_expertise_years_avg'] > 10)
    ).astype(int)
    
    # Market Leader
    patterns['market_leader'] = (
        (df['customer_count'] > df['customer_count'].quantile(0.9)) &
        (df['market_growth_rate_percent'] > 20) &
        (df['brand_strength_score'] > 4)
    ).astype(int)
    
    # Capital Efficient
    patterns['capital_efficient'] = (
        (df['burn_multiple'] < 1.2) &
        (df['gross_margin_percent'] > 70) &
        (df['ltv_cac_ratio'] > 3)
    ).astype(int)
    
    return pd.DataFrame(patterns)

def train_pattern_model(X, y, pattern_mask, pattern_name):
    """Train a model for a specific pattern"""
    # Get positive and negative samples
    positive_idx = pattern_mask[pattern_mask > 0].index
    
    if len(positive_idx) < 100:
        logger.warning(f"Not enough samples for {pattern_name}: {len(positive_idx)}")
        return None, 0.5
    
    # Balance dataset with 2:1 negative to positive ratio
    negative_idx = pattern_mask[pattern_mask == 0].sample(min(len(positive_idx) * 2, len(pattern_mask) - len(positive_idx))).index
    
    # Combine indices
    train_idx = positive_idx.union(negative_idx)
    X_pattern = X.loc[train_idx]
    y_pattern = y.loc[train_idx]
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X_pattern, y_pattern, test_size=0.2, random_state=42, stratify=y_pattern)
    
    # Train model (using LightGBM for efficiency)
    model = lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        objective='binary',
        metric='auc',
        random_state=42,
        verbosity=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    val_pred = model.predict_proba(X_val)[:, 1]
    val_auc = roc_auc_score(y_val, val_pred)
    
    logger.info(f"{pattern_name} - Samples: {len(positive_idx)}, Val AUC: {val_auc:.4f}")
    
    return model, val_auc

def main():
    logger.info("="*60)
    logger.info("Training Pattern Models for Hybrid System")
    logger.info("="*60)
    
    # Load data
    logger.info("Loading data...")
    df = pd.read_csv("data/final_100k_dataset_45features.csv")
    logger.info(f"Loaded {len(df)} samples")
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in ['startup_id', 'startup_name', 'founding_year', 'success', 'burn_multiple_calc']]
    X = df[feature_cols].copy()
    y = df['success']
    
    # Handle categorical features
    categorical_cols = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
    for col in categorical_cols:
        if col in X.columns:
            # Simple label encoding
            X[col] = pd.Categorical(X[col]).codes
    
    # Detect patterns
    logger.info("Detecting patterns...")
    pattern_df = detect_startup_patterns(df)
    
    # Show pattern distribution
    logger.info("\nPattern Distribution:")
    for pattern in pattern_df.columns:
        count = pattern_df[pattern].sum()
        pct = count / len(df) * 100
        logger.info(f"  {pattern}: {count} ({pct:.1f}%)")
    
    # Create output directory
    output_dir = Path("models/hybrid_patterns")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Train models for each pattern
    pattern_models = {}
    pattern_scores = {}
    
    logger.info("\nTraining pattern models...")
    for pattern_name in pattern_df.columns:
        model, auc = train_pattern_model(X, y, pattern_df[pattern_name], pattern_name)
        if model is not None:
            pattern_models[pattern_name] = model
            pattern_scores[pattern_name] = auc
            
            # Save model
            model_path = output_dir / f"{pattern_name}_model.pkl"
            joblib.dump(model, model_path)
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Training Complete!")
    logger.info(f"Trained {len(pattern_models)} pattern models")
    logger.info("\nModel Performance:")
    
    avg_auc = np.mean(list(pattern_scores.values()))
    for pattern, auc in sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {pattern}: {auc:.4f} AUC")
    logger.info(f"\nAverage AUC: {avg_auc:.4f}")
    
    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'patterns_trained': list(pattern_models.keys()),
        'pattern_scores': pattern_scores,
        'average_auc': avg_auc,
        'total_samples': len(df)
    }
    
    import json
    with open(output_dir / 'training_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return pattern_models, pattern_scores

if __name__ == "__main__":
    pattern_models, scores = main()