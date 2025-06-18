#!/usr/bin/env python3
"""
Optimized complete model training with progress tracking
"""

import pandas as pd
import numpy as np
import joblib
import logging
from pathlib import Path
from datetime import datetime
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score, classification_report
from catboost import CatBoostClassifier
import xgboost as xgb
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.isotonic import IsotonicRegression
import warnings
warnings.filterwarnings('ignore')

# Set up logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handle categorical and numerical features"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.categorical_columns = []
        self.numerical_columns = []
        
    def fit_transform(self, df, exclude_columns):
        """Fit and transform in one step for efficiency"""
        # Identify column types
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.categorical_columns = [col for col in self.categorical_columns if col not in exclude_columns]
        
        self.numerical_columns = df.select_dtypes(exclude=['object']).columns.tolist()
        self.numerical_columns = [col for col in self.numerical_columns if col not in exclude_columns]
        
        df_transformed = df.copy()
        
        # Encode categorical columns
        for col in self.categorical_columns:
            le = LabelEncoder()
            df_transformed[col] = le.fit_transform(df[col].fillna('Unknown'))
            self.label_encoders[col] = le
            
        # Scale numerical columns
        if self.numerical_columns:
            df_transformed[self.numerical_columns] = self.scaler.fit_transform(df[self.numerical_columns])
            
        # Return feature columns only
        feature_columns = self.categorical_columns + self.numerical_columns
        return df_transformed[feature_columns].values


class OptimizedDNAPatternAnalyzer:
    """Optimized DNA Pattern Analyzer for faster training"""
    
    def __init__(self):
        self.pca = PCA(n_components=10)
        self.kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)  # Reduced clusters
        self.pattern_classifier = GradientBoostingClassifier(
            n_estimators=100,  # Reduced from 200
            max_depth=4,       # Reduced from 5
            learning_rate=0.15,  # Increased for faster convergence
            random_state=42,
            subsample=0.8,
            n_iter_no_change=5,  # Early stopping
            validation_fraction=0.1
        )
        
    def fit(self, X, y):
        """Extract and learn startup DNA patterns"""
        logger.info("Extracting DNA patterns...")
        start_time = time.time()
        
        # Extract principal components
        X_pca = self.pca.fit_transform(X)
        logger.info(f"PCA completed in {time.time() - start_time:.2f}s")
        
        # Create pattern clusters
        cluster_start = time.time()
        clusters = self.kmeans.fit_predict(X_pca)
        logger.info(f"Clustering completed in {time.time() - cluster_start:.2f}s")
        
        # Create DNA features efficiently
        dna_features = self._create_dna_features(X, X_pca, clusters)
        
        # Train pattern classifier
        classifier_start = time.time()
        self.pattern_classifier.fit(dna_features, y)
        logger.info(f"Classifier training completed in {time.time() - classifier_start:.2f}s")
        logger.info(f"Total DNA training time: {time.time() - start_time:.2f}s")
        
        return self
        
    def _create_dna_features(self, X, X_pca, clusters):
        """Create DNA features efficiently"""
        n_samples = X.shape[0]
        
        # Pre-allocate arrays for efficiency
        financial_dna = np.zeros((n_samples, 3))
        growth_dna = np.zeros((n_samples, 3))
        team_dna = np.zeros((n_samples, 3))
        market_dna = np.zeros((n_samples, 3))
        
        # Vectorized operations
        # Financial DNA
        capital_features = X[:, :10]
        financial_dna[:, 0] = np.mean(capital_features, axis=1) / (np.std(capital_features, axis=1) + 1e-6)
        financial_dna[:, 1] = np.std(capital_features, axis=1)
        financial_dna[:, 2] = np.mean(capital_features, axis=1)  # Simplified trend
        
        # Growth DNA
        growth_features = X[:, 10:20] if X.shape[1] > 20 else X[:, :10]
        growth_dna[:, 0] = np.mean(growth_features, axis=1)
        growth_dna[:, 1] = 1 / (np.std(growth_features, axis=1) + 1e-6)
        growth_dna[:, 2] = np.max(growth_features, axis=1)
        
        # Team DNA
        team_idx = min(30, X.shape[1]-10)
        team_features = X[:, team_idx:team_idx+10]
        team_dna[:, 0] = np.std(team_features, axis=1)
        team_dna[:, 1] = np.max(team_features, axis=1)
        team_dna[:, 2] = np.mean(team_features, axis=1)
        
        # Market DNA
        market_idx = min(20, X.shape[1]-10)
        market_features = X[:, market_idx:market_idx+10]
        market_dna[:, 0] = np.mean(market_features, axis=1)
        market_dna[:, 1] = np.max(market_features, axis=1) - np.min(market_features, axis=1)
        market_dna[:, 2] = np.percentile(market_features, 75, axis=1)
        
        # Combine all features
        return np.hstack([
            X_pca,
            clusters.reshape(-1, 1),
            financial_dna,
            growth_dna,
            team_dna,
            market_dna
        ])
        
    def predict_proba(self, X):
        """Predict probabilities"""
        X_pca = self.pca.transform(X)
        clusters = self.kmeans.predict(X_pca)
        dna_features = self._create_dna_features(X, X_pca, clusters)
        return self.pattern_classifier.predict_proba(dna_features)


class OptimizedTemporalModel:
    """Optimized temporal prediction model"""
    
    def __init__(self):
        self.temporal_forest = RandomForestClassifier(
            n_estimators=100,  # Reduced from 150
            max_depth=8,
            random_state=42,
            n_jobs=-1,  # Use all cores
            min_samples_split=10,
            min_samples_leaf=5
        )
        
    def fit(self, X, y):
        """Train temporal model"""
        logger.info("Training temporal model...")
        start_time = time.time()
        
        # Create temporal features
        temporal_features = self._create_temporal_features_fast(X)
        
        # Train model
        self.temporal_forest.fit(temporal_features, y)
        logger.info(f"Temporal training completed in {time.time() - start_time:.2f}s")
        
        return self
        
    def _create_temporal_features_fast(self, X):
        """Create temporal features efficiently"""
        n_samples, n_features = X.shape
        
        # Basic statistics (vectorized)
        feature_mean = np.mean(X, axis=1)
        feature_std = np.std(X, axis=1)
        feature_max = np.max(X, axis=1)
        feature_min = np.min(X, axis=1)
        
        # Simple trend (first vs last quartile)
        q1_mean = np.mean(X[:, :n_features//4], axis=1)
        q4_mean = np.mean(X[:, -n_features//4:], axis=1)
        trend = q4_mean - q1_mean
        
        # Volatility
        volatility = np.std(X[:, :10], axis=1) if n_features > 10 else feature_std
        
        # Combine features
        return np.column_stack([
            X,
            feature_mean,
            feature_std,
            feature_max,
            feature_min,
            trend,
            volatility
        ])
        
    def predict_proba(self, X):
        """Predict probabilities"""
        temporal_features = self._create_temporal_features_fast(X)
        return self.temporal_forest.predict_proba(temporal_features)


class OptimizedIndustryModel:
    """Optimized industry-specific model"""
    
    def __init__(self):
        self.global_model = CatBoostClassifier(
            iterations=200,  # Reduced from 300
            depth=5,  # Reduced from 6
            learning_rate=0.1,  # Increased from 0.05
            random_seed=42,
            verbose=False,
            early_stopping_rounds=20,
            use_best_model=True,
            task_type='CPU',
            thread_count=-1  # Use all cores
        )
        self.industry_models = {}
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
        
    def fit(self, X, y, industries=None):
        """Train industry model"""
        logger.info("Training industry-specific model...")
        start_time = time.time()
        
        # Create validation set for early stopping
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.1, random_state=42, stratify=y
        )
        
        # Train global model with early stopping
        self.global_model.fit(
            X_train, y_train,
            eval_set=(X_val, y_val),
            verbose=False
        )
        
        # Calibrate
        global_probs = self.global_model.predict_proba(X)[:, 1]
        self.calibrator.fit(global_probs, y)
        
        logger.info(f"Industry model training completed in {time.time() - start_time:.2f}s")
        
        return self
        
    def predict_proba(self, X, industries=None):
        """Predict probabilities"""
        global_probs = self.global_model.predict_proba(X)
        calibrated_probs = self.calibrator.transform(global_probs[:, 1])
        
        # Return as 2D array
        return np.column_stack([1 - calibrated_probs, calibrated_probs])


def train_complete_models():
    """Train all models with optimizations"""
    logger.info("="*60)
    logger.info("STARTING OPTIMIZED COMPLETE MODEL TRAINING")
    logger.info("="*60)
    
    overall_start = time.time()
    
    # Load data
    logger.info("\nLoading dataset...")
    data_start = time.time()
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    logger.info(f"Data loaded in {time.time() - data_start:.2f}s")
    logger.info(f"Dataset shape: {df.shape}")
    
    # Preprocess
    logger.info("\nPreprocessing data...")
    preprocess_start = time.time()
    exclude_columns = ['success', 'startup_id', 'startup_name', 'burn_multiple_calc']
    preprocessor = DataPreprocessor()
    X = preprocessor.fit_transform(df, exclude_columns)
    y = df['success'].values
    logger.info(f"Preprocessing completed in {time.time() - preprocess_start:.2f}s")
    
    # Split data
    logger.info("\nSplitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Training samples: {len(X_train):,}")
    logger.info(f"Test samples: {len(X_test):,}")
    
    # Create directories
    Path('models/complete_training').mkdir(parents=True, exist_ok=True)
    
    # Results storage
    results = {}
    
    # 1. Train DNA Pattern Analyzer
    logger.info("\n" + "="*50)
    logger.info("1. TRAINING DNA PATTERN ANALYZER")
    logger.info("="*50)
    dna_model = OptimizedDNAPatternAnalyzer()
    dna_start = time.time()
    dna_model.fit(X_train, y_train)
    dna_time = time.time() - dna_start
    
    # Evaluate
    dna_proba = dna_model.predict_proba(X_test)[:, 1]
    dna_auc = roc_auc_score(y_test, dna_proba)
    logger.info(f"DNA Model AUC: {dna_auc:.4f}")
    logger.info(f"Training time: {dna_time:.2f}s")
    
    # Save
    dna_package = {
        'model': dna_model,
        'preprocessor': preprocessor,
        'auc': dna_auc,
        'training_time': dna_time
    }
    joblib.dump(dna_package, 'models/complete_training/dna_pattern_model.pkl')
    results['dna'] = {'auc': dna_auc, 'time': dna_time}
    
    # 2. Train Temporal Model
    logger.info("\n" + "="*50)
    logger.info("2. TRAINING TEMPORAL MODEL")
    logger.info("="*50)
    temporal_model = OptimizedTemporalModel()
    temporal_start = time.time()
    temporal_model.fit(X_train, y_train)
    temporal_time = time.time() - temporal_start
    
    # Evaluate
    temporal_proba = temporal_model.predict_proba(X_test)[:, 1]
    temporal_auc = roc_auc_score(y_test, temporal_proba)
    logger.info(f"Temporal Model AUC: {temporal_auc:.4f}")
    logger.info(f"Training time: {temporal_time:.2f}s")
    
    # Save
    temporal_package = {
        'model': temporal_model,
        'preprocessor': preprocessor,
        'auc': temporal_auc,
        'training_time': temporal_time
    }
    joblib.dump(temporal_package, 'models/complete_training/temporal_model.pkl')
    results['temporal'] = {'auc': temporal_auc, 'time': temporal_time}
    
    # 3. Train Industry Model
    logger.info("\n" + "="*50)
    logger.info("3. TRAINING INDUSTRY-SPECIFIC MODEL")
    logger.info("="*50)
    industry_model = OptimizedIndustryModel()
    industry_start = time.time()
    industry_model.fit(X_train, y_train)
    industry_time = time.time() - industry_start
    
    # Evaluate
    industry_proba = industry_model.predict_proba(X_test)[:, 1]
    industry_auc = roc_auc_score(y_test, industry_proba)
    logger.info(f"Industry Model AUC: {industry_auc:.4f}")
    logger.info(f"Training time: {industry_time:.2f}s")
    
    # Save
    industry_package = {
        'model': industry_model,
        'preprocessor': preprocessor,
        'auc': industry_auc,
        'training_time': industry_time
    }
    joblib.dump(industry_package, 'models/complete_training/industry_model.pkl')
    results['industry'] = {'auc': industry_auc, 'time': industry_time}
    
    # 4. Create Ensemble Model
    logger.info("\n" + "="*50)
    logger.info("4. CREATING ENSEMBLE MODEL")
    logger.info("="*50)
    
    # Combine predictions
    ensemble_probs = np.column_stack([dna_proba, temporal_proba, industry_proba])
    
    # Train meta-learner
    meta_model = xgb.XGBClassifier(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    # Use a small validation set for meta-learning
    X_meta_train, X_meta_val, y_meta_train, y_meta_val = train_test_split(
        ensemble_probs, y_test, test_size=0.3, random_state=42
    )
    
    meta_model.fit(X_meta_train, y_meta_train)
    ensemble_proba = meta_model.predict_proba(X_meta_val)[:, 1]
    ensemble_auc = roc_auc_score(y_meta_val, ensemble_proba)
    
    logger.info(f"Ensemble Model AUC: {ensemble_auc:.4f}")
    
    # Save ensemble
    ensemble_package = {
        'dna_model': dna_model,
        'temporal_model': temporal_model,
        'industry_model': industry_model,
        'meta_model': meta_model,
        'preprocessor': preprocessor,
        'auc': ensemble_auc
    }
    joblib.dump(ensemble_package, 'models/complete_training/ensemble_model.pkl')
    results['ensemble'] = {'auc': ensemble_auc}
    
    # Total time
    total_time = time.time() - overall_start
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("TRAINING COMPLETE!")
    logger.info("="*60)
    logger.info(f"\nTotal training time: {total_time:.2f}s ({total_time/60:.1f} minutes)")
    logger.info("\nModel Performance:")
    logger.info(f"  DNA Pattern Analyzer: {results['dna']['auc']:.4f} AUC ({results['dna']['time']:.1f}s)")
    logger.info(f"  Temporal Model: {results['temporal']['auc']:.4f} AUC ({results['temporal']['time']:.1f}s)")
    logger.info(f"  Industry Model: {results['industry']['auc']:.4f} AUC ({results['industry']['time']:.1f}s)")
    logger.info(f"  Ensemble Model: {results['ensemble']['auc']:.4f} AUC")
    
    # Save summary
    import json
    summary = {
        'training_date': datetime.now().isoformat(),
        'total_time_seconds': total_time,
        'dataset': 'final_100k_dataset_45features.csv',
        'n_samples': len(df),
        'n_features': X.shape[1],
        'results': results,
        'preprocessor_info': {
            'categorical_features': preprocessor.categorical_columns,
            'numerical_features': preprocessor.numerical_columns[:10] + ['...']  # Sample
        }
    }
    
    with open('models/complete_training/training_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"\nAll models saved to: models/complete_training/")
    logger.info("Training summary saved to: models/complete_training/training_summary.json")
    
    # Copy to main models directory
    logger.info("\nUpdating production models...")
    import shutil
    shutil.copy2('models/complete_training/dna_pattern_model.pkl', 
                 'models/dna_analyzer/dna_pattern_model.pkl')
    shutil.copy2('models/complete_training/temporal_model.pkl',
                 'models/temporal_prediction_model.pkl')
    shutil.copy2('models/complete_training/industry_model.pkl',
                 'models/industry_specific_model.pkl')
    
    logger.info("✅ Production models updated!")
    
    return results


if __name__ == "__main__":
    # Check for XGBoost
    try:
        import xgboost
    except ImportError:
        logger.info("Installing XGBoost...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'xgboost'])
        import xgboost
    
    train_complete_models()