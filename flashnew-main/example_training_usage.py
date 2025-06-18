#!/usr/bin/env python3
"""
Example usage of the generated 100k dataset for model training.
Shows how to load, preprocess, and use the data for FLASH predictions.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

def prepare_dataset_for_training(df_path: str = 'generated_100k_dataset.csv'):
    """Load and prepare the dataset for training."""
    print("Loading dataset...")
    df = pd.read_csv(df_path)
    
    # Define feature groups
    financial_features = [
        'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
        'runway_months', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
        'gross_margin_percent', 'burn_multiple', 'ltv_cac_ratio'
    ]
    
    market_features = [
        'tam_size_usd', 'sam_size_usd', 'som_size_usd', 'market_growth_rate_percent',
        'competition_intensity', 'competitors_named_count'
    ]
    
    product_features = [
        'customer_count', 'customer_concentration_percent', 'user_growth_rate_percent',
        'net_dollar_retention_percent', 'product_retention_30d', 'product_retention_90d',
        'dau_mau_ratio', 'tech_differentiation_score', 'switching_cost_score',
        'brand_strength_score', 'scalability_score'
    ]
    
    team_features = [
        'founders_count', 'team_size_full_time', 'years_experience_avg',
        'domain_expertise_years_avg', 'prior_startup_experience_count',
        'prior_successful_exits_count', 'board_advisor_experience_score',
        'advisors_count', 'team_diversity_percent'
    ]
    
    boolean_features = [
        'has_debt', 'network_effects_present', 'has_data_moat',
        'regulatory_advantage_present', 'key_person_dependency'
    ]
    
    categorical_features = [
        'funding_stage', 'sector', 'product_stage', 'investor_tier_primary'
    ]
    
    # All features to use
    all_features = (financial_features + market_features + product_features + 
                   team_features + boolean_features + categorical_features)
    
    # Prepare features
    X = df[all_features].copy()
    y = df['success'].astype(int)
    
    # Convert boolean columns to int
    for col in boolean_features:
        X[col] = X[col].astype(int)
    
    # Encode categorical variables
    label_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
    
    print(f"\nDataset prepared:")
    print(f"  Total samples: {len(X):,}")
    print(f"  Features: {len(all_features)}")
    print(f"  Success rate: {y.mean():.2%}")
    
    return X, y, all_features, label_encoders

def train_example_model(X, y):
    """Train an example XGBoost model."""
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Training set: {len(X_train):,} samples")
    print(f"  Test set: {len(X_test):,} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train XGBoost model
    print("\nTraining XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\nEvaluating model...")
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC AUC Score: {auc_score:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 15 Most Important Features:")
    for idx, row in feature_importance.head(15).iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")
    
    return model, scaler, feature_importance

def demonstrate_prediction(model, scaler, X_test_sample):
    """Show example predictions with probability scores."""
    print("\n" + "="*60)
    print("EXAMPLE PREDICTIONS")
    print("="*60)
    
    # Get predictions
    X_scaled = scaler.transform(X_test_sample)
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]
    
    for i in range(min(5, len(X_test_sample))):
        print(f"\nStartup {i+1}:")
        print(f"  Predicted: {'Success' if predictions[i] else 'Failure'}")
        print(f"  Success probability: {probabilities[i]:.2%}")
        print("  Key metrics:")
        print(f"    - Revenue: ${X_test_sample.iloc[i]['annual_revenue_run_rate']:,.0f}")
        print(f"    - Growth rate: {X_test_sample.iloc[i]['revenue_growth_rate_percent']:.1f}%")
        print(f"    - Burn multiple: {X_test_sample.iloc[i]['burn_multiple']:.1f}")
        print(f"    - Team size: {X_test_sample.iloc[i]['team_size_full_time']}")
        print(f"    - LTV/CAC: {X_test_sample.iloc[i]['ltv_cac_ratio']:.2f}")

def main():
    """Main function to demonstrate dataset usage."""
    print("="*60)
    print("FLASH 100K Dataset Training Example")
    print("="*60)
    
    # Prepare dataset
    X, y, features, encoders = prepare_dataset_for_training()
    
    # Train model
    model, scaler, feature_importance = train_example_model(X, y)
    
    # Show example predictions
    X_sample = X.sample(5, random_state=42)
    demonstrate_prediction(model, scaler, X_sample)
    
    # Save feature importance
    feature_importance.to_csv('model_feature_importance.csv', index=False)
    print("\n\nFeature importance saved to model_feature_importance.csv")
    
    print("\nTraining complete! The dataset is ready for:")
    print("  - Model experimentation")
    print("  - Feature engineering")
    print("  - Ensemble methods")
    print("  - Deep learning approaches")
    print("  - Real-world deployment")

if __name__ == "__main__":
    main()