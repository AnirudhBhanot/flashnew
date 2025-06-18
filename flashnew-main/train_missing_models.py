#!/usr/bin/env python3
"""
Train all missing models to complete the FLASH system
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from catboost import CatBoostClassifier
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load dataset
def load_data():
    """Load the training dataset"""
    try:
        df = pd.read_csv('data/final_100k_dataset_45features.csv')
        logger.info(f"Loaded dataset with {len(df)} rows and {df.shape[1]} columns")
        return df
    except Exception as e:
        logger.error(f"Could not load dataset: {e}")
        return None

def prepare_features(df):
    """Prepare features for training"""
    # Define feature columns - exclude ID, name, and target columns
    exclude_cols = ['startup_id', 'startup_name', 'company_id', 'success', 'success_label', 'founding_year', 'burn_multiple_calc']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    # Handle categorical features
    categorical_features = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
    
    # Create label encoders
    label_encoders = {}
    df_encoded = df.copy()
    
    # Drop excluded columns
    for col in exclude_cols:
        if col in df_encoded.columns and col != 'success':
            df_encoded = df_encoded.drop(col, axis=1)
    
    # Convert boolean columns to int
    bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 
                 'regulatory_advantage_present', 'key_person_dependency']
    for col in bool_cols:
        if col in df_encoded.columns:
            df_encoded[col] = df_encoded[col].astype(int)
    
    for cat_col in categorical_features:
        if cat_col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[cat_col] = le.fit_transform(df_encoded[cat_col].astype(str))
            label_encoders[cat_col] = le
    
    # Get features and target
    X = df_encoded[feature_cols]
    y = df_encoded['success'].astype(int) if 'success' in df_encoded.columns else df_encoded['success_label']
    
    return X, y, feature_cols, label_encoders

def train_dna_models(X_train, y_train, X_test, y_test):
    """Train DNA pattern analysis models"""
    logger.info("Training DNA pattern models...")
    
    # Create DNA analyzer components
    models = {}
    
    # 1. Pattern clustering model
    logger.info("Training pattern clustering...")
    n_clusters = 8
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X_train)
    models['clustering'] = kmeans
    
    # 2. Success pattern classifier
    logger.info("Training success pattern classifier...")
    success_model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    success_model.fit(X_train, y_train)
    models['success_classifier'] = success_model
    
    # 3. Neural network for pattern recognition
    logger.info("Training neural pattern recognizer...")
    nn_model = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        learning_rate='adaptive',
        max_iter=500,
        random_state=42
    )
    nn_model.fit(X_train, y_train)
    models['pattern_nn'] = nn_model
    
    # 4. Scaler for preprocessing
    scaler = StandardScaler()
    scaler.fit(X_train)
    models['scaler'] = scaler
    
    # Save models
    Path('models/dna_analyzer').mkdir(parents=True, exist_ok=True)
    
    for name, model in models.items():
        joblib.dump(model, f'models/dna_analyzer/{name}.pkl')
    
    # Create main DNA model wrapper
    dna_model = {
        'models': models,
        'n_clusters': n_clusters,
        'feature_names': list(X_train.columns)
    }
    joblib.dump(dna_model, 'models/dna_analyzer/dna_pattern_model.pkl')
    
    logger.info("✅ DNA pattern models trained and saved")
    
    # Test accuracy
    test_score = success_model.score(X_test, y_test)
    logger.info(f"DNA model test accuracy: {test_score:.4f}")

def train_temporal_models(X_train, y_train, X_test, y_test):
    """Train temporal prediction models"""
    logger.info("Training temporal models...")
    
    models = {}
    
    # 1. Short-term predictor (0-6 months)
    logger.info("Training short-term predictor...")
    short_term = CatBoostClassifier(
        iterations=200,
        learning_rate=0.05,
        depth=6,
        verbose=False,
        random_seed=42
    )
    short_term.fit(X_train, y_train)
    models['short_term'] = short_term
    
    # 2. Medium-term predictor (6-18 months)
    logger.info("Training medium-term predictor...")
    medium_term = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    medium_term.fit(X_train, y_train)
    models['medium_term'] = medium_term
    
    # 3. Long-term predictor (18+ months)
    logger.info("Training long-term predictor...")
    long_term = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=6,
        random_state=42
    )
    long_term.fit(X_train, y_train)
    models['long_term'] = long_term
    
    # Save models
    Path('models/temporal').mkdir(parents=True, exist_ok=True)
    
    for name, model in models.items():
        joblib.dump(model, f'models/temporal/{name}_model.pkl')
    
    # Create main temporal model wrapper
    temporal_model = {
        'models': models,
        'feature_names': list(X_train.columns)
    }
    joblib.dump(temporal_model, 'models/temporal_prediction_model.pkl')
    
    logger.info("✅ Temporal models trained and saved")
    
    # Test accuracy
    test_score = short_term.score(X_test, y_test)
    logger.info(f"Temporal model test accuracy: {test_score:.4f}")

def train_industry_models(df, X_train, y_train, X_test, y_test):
    """Train industry-specific models"""
    logger.info("Training industry-specific models...")
    
    # Get unique industries
    industries = df['sector'].unique()
    logger.info(f"Found {len(industries)} unique industries")
    
    models = {}
    
    # Train a model for each industry with sufficient data
    for industry in industries:
        industry_mask_train = df.loc[X_train.index, 'sector'] == industry
        industry_mask_test = df.loc[X_test.index, 'sector'] == industry
        
        n_samples = industry_mask_train.sum()
        
        if n_samples >= 100:  # Only train if we have enough samples
            logger.info(f"Training model for {industry} ({n_samples} samples)...")
            
            X_industry = X_train[industry_mask_train]
            y_industry = y_train[industry_mask_train]
            
            # Use CatBoost for consistency
            model = CatBoostClassifier(
                iterations=150,
                learning_rate=0.05,
                depth=5,
                verbose=False,
                random_seed=42
            )
            model.fit(X_industry, y_industry)
            
            models[industry] = model
            
            # Test accuracy if we have test samples
            if industry_mask_test.sum() > 0:
                X_test_industry = X_test[industry_mask_test]
                y_test_industry = y_test[industry_mask_test]
                score = model.score(X_test_industry, y_test_industry)
                logger.info(f"  {industry} accuracy: {score:.4f}")
    
    # Train a general model for industries with insufficient data
    logger.info("Training general industry model...")
    general_model = CatBoostClassifier(
        iterations=200,
        learning_rate=0.05,
        depth=6,
        verbose=False,
        random_seed=42
    )
    general_model.fit(X_train, y_train)
    models['general'] = general_model
    
    # Save models
    Path('models/industry_specific').mkdir(parents=True, exist_ok=True)
    
    for name, model in models.items():
        safe_name = name.replace('/', '_').replace(' ', '_')
        joblib.dump(model, f'models/industry_specific/{safe_name}_model.pkl')
    
    # Create main industry model wrapper
    industry_model = {
        'models': models,
        'industries': list(models.keys()),
        'feature_names': list(X_train.columns)
    }
    joblib.dump(industry_model, 'models/industry_specific_model.pkl')
    
    logger.info(f"✅ Industry models trained and saved ({len(models)} models)")

def train_v2_classifiers(X_train, y_train, X_test, y_test):
    """Train v2 CAMP pillar classifiers"""
    logger.info("Training v2 CAMP pillar classifiers...")
    
    # Define CAMP pillar features
    pillars = {
        'capital': ['funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd',
                   'monthly_burn_usd', 'runway_months', 'annual_revenue_run_rate',
                   'revenue_growth_rate_percent', 'gross_margin_percent', 'burn_multiple',
                   'ltv_cac_ratio', 'investor_tier_primary', 'has_debt'],
        'advantage': ['patent_count', 'network_effects_present', 'has_data_moat',
                     'regulatory_advantage_present', 'tech_differentiation_score',
                     'switching_cost_score', 'brand_strength_score', 'scalability_score',
                     'product_stage', 'product_retention_30d', 'product_retention_90d'],
        'market': ['sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
                  'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
                  'user_growth_rate_percent', 'net_dollar_retention_percent',
                  'competition_intensity', 'competitors_named_count', 'dau_mau_ratio'],
        'people': ['founders_count', 'team_size_full_time', 'years_experience_avg',
                  'domain_expertise_years_avg', 'prior_startup_experience_count',
                  'prior_successful_exits_count', 'board_advisor_experience_score',
                  'advisors_count', 'team_diversity_percent', 'key_person_dependency']
    }
    
    Path('models/v2').mkdir(parents=True, exist_ok=True)
    pillar_predictions_train = {}
    pillar_predictions_test = {}
    
    # Train classifier and ensemble for each pillar
    for pillar_name, pillar_features in pillars.items():
        logger.info(f"Training {pillar_name} models...")
        
        # Filter features that exist in the dataset
        available_features = [f for f in pillar_features if f in X_train.columns]
        
        X_pillar_train = X_train[available_features]
        X_pillar_test = X_test[available_features]
        
        # Train classifier
        classifier = CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            depth=6,
            verbose=False,
            random_seed=42
        )
        classifier.fit(X_pillar_train, y_train)
        joblib.dump(classifier, f'models/v2/{pillar_name}_classifier_v2.pkl')
        
        # Train ensemble (using RandomForest as second model)
        ensemble = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42,
            n_jobs=-1
        )
        ensemble.fit(X_pillar_train, y_train)
        joblib.dump(ensemble, f'models/v2/{pillar_name}_ensemble_v2.pkl')
        
        # Store predictions for meta model
        pillar_predictions_train[pillar_name] = classifier.predict_proba(X_pillar_train)[:, 1]
        pillar_predictions_test[pillar_name] = classifier.predict_proba(X_pillar_test)[:, 1]
        
        # Test accuracy
        score = classifier.score(X_pillar_test, y_test)
        logger.info(f"  {pillar_name} classifier accuracy: {score:.4f}")
    
    # Train meta classifier
    logger.info("Training meta classifier...")
    
    X_meta_train = pd.DataFrame(pillar_predictions_train)
    X_meta_test = pd.DataFrame(pillar_predictions_test)
    
    meta_classifier = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
    meta_classifier.fit(X_meta_train, y_train)
    joblib.dump(meta_classifier, 'models/v2/meta_classifier_v2.pkl')
    
    # Test meta classifier
    meta_score = meta_classifier.score(X_meta_test, y_test)
    logger.info(f"Meta classifier accuracy: {meta_score:.4f}")
    
    logger.info("✅ V2 classifiers trained and saved")

def main():
    """Main training function"""
    logger.info("Starting model training...")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Prepare features
    X, y, feature_cols, label_encoders = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    
    # Train all missing models
    train_dna_models(X_train, y_train, X_test, y_test)
    train_temporal_models(X_train, y_train, X_test, y_test)
    train_industry_models(df, X_train, y_train, X_test, y_test)
    train_v2_classifiers(X_train, y_train, X_test, y_test)
    
    # Save label encoders
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    logger.info("\n✅ All models trained successfully!")
    logger.info("Models saved in:")
    logger.info("  - models/dna_analyzer/")
    logger.info("  - models/temporal/")
    logger.info("  - models/industry_specific/")
    logger.info("  - models/v2/")

if __name__ == "__main__":
    main()