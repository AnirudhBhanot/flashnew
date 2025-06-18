#!/usr/bin/env python3
"""
Train real models to replace placeholder models - with categorical feature handling
"""

import pandas as pd
import numpy as np
import joblib
import logging
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support, classification_report
from catboost import CatBoostClassifier
import xgboost as xgb
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.isotonic import IsotonicRegression

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handle categorical and numerical features"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.categorical_columns = []
        self.numerical_columns = []
        
    def fit(self, df, exclude_columns):
        """Fit preprocessing on dataframe"""
        # Identify column types
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.categorical_columns = [col for col in self.categorical_columns if col not in exclude_columns]
        
        self.numerical_columns = df.select_dtypes(exclude=['object']).columns.tolist()
        self.numerical_columns = [col for col in self.numerical_columns if col not in exclude_columns]
        
        # Fit label encoders for categorical columns
        for col in self.categorical_columns:
            le = LabelEncoder()
            le.fit(df[col].fillna('Unknown'))
            self.label_encoders[col] = le
            
        # Fit scaler on numerical columns
        if self.numerical_columns:
            self.scaler.fit(df[self.numerical_columns])
            
        return self
        
    def transform(self, df):
        """Transform dataframe"""
        df_transformed = df.copy()
        
        # Encode categorical columns
        for col in self.categorical_columns:
            if col in self.label_encoders:
                df_transformed[col] = self.label_encoders[col].transform(df[col].fillna('Unknown'))
                
        # Scale numerical columns
        if self.numerical_columns:
            df_transformed[self.numerical_columns] = self.scaler.transform(df[self.numerical_columns])
            
        # Return feature columns only
        feature_columns = self.categorical_columns + self.numerical_columns
        return df_transformed[feature_columns].values
        
    def get_feature_names(self):
        """Get ordered feature names"""
        return self.categorical_columns + self.numerical_columns


class DNAPatternAnalyzer:
    """Analyze startup 'DNA' - fundamental patterns that predict success"""
    
    def __init__(self):
        self.pca = PCA(n_components=10)
        self.kmeans = KMeans(n_clusters=8, random_state=42)
        self.pattern_classifier = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.preprocessor = None
        
    def fit(self, X, y):
        """Extract and learn startup DNA patterns"""
        logger.info("Extracting startup DNA patterns...")
        
        # Extract principal components
        X_pca = self.pca.fit_transform(X)
        
        # Create pattern clusters
        clusters = self.kmeans.fit_predict(X_pca)
        
        # Create DNA features
        dna_features = np.column_stack([
            X_pca,
            clusters.reshape(-1, 1),
            self._extract_financial_dna(X),
            self._extract_growth_dna(X),
            self._extract_team_dna(X),
            self._extract_market_dna(X)
        ])
        
        # Train pattern classifier
        self.pattern_classifier.fit(dna_features, y)
        
        return self
        
    def _extract_financial_dna(self, X):
        """Extract financial health patterns"""
        # Capital efficiency metrics - using normalized indices
        n_features = X.shape[1]
        capital_indices = range(min(10, n_features))  # First 10 features or less
        capital_features = X[:, capital_indices]
        
        efficiency = np.mean(capital_features, axis=1) / (np.std(capital_features, axis=1) + 1e-6)
        volatility = np.std(capital_features, axis=1)
        trend = np.array([np.polyfit(range(len(capital_indices)), row[capital_indices], 1)[0] 
                         for row in X])
        
        return np.column_stack([efficiency, volatility, trend])
        
    def _extract_growth_dna(self, X):
        """Extract growth trajectory patterns"""
        # Growth indicators
        n_features = X.shape[1]
        growth_indices = range(10, min(20, n_features))
        
        if len(growth_indices) > 0:
            growth_features = X[:, growth_indices]
            growth_rate = np.mean(growth_features, axis=1)
            consistency = 1 / (np.std(growth_features, axis=1) + 1e-6)
        else:
            growth_rate = np.zeros(X.shape[0])
            consistency = np.ones(X.shape[0])
        
        # Overall trend
        trend = np.array([np.mean(row) for row in X])
        
        return np.column_stack([growth_rate, consistency, trend])
        
    def _extract_team_dna(self, X):
        """Extract team composition patterns"""
        # Team-related features
        n_features = X.shape[1]
        team_indices = range(max(0, n_features-15), n_features)  # Last 15 features
        
        team_features = X[:, team_indices]
        diversity = np.std(team_features, axis=1)
        strength = np.max(team_features, axis=1)
        balance = np.mean(team_features, axis=1) / (np.max(np.abs(team_features), axis=1) + 1e-6)
        
        return np.column_stack([diversity, strength, balance])
        
    def _extract_market_dna(self, X):
        """Extract market positioning patterns"""
        # Market features
        n_features = X.shape[1]
        market_indices = range(20, min(30, n_features))
        
        if len(market_indices) > 0:
            market_features = X[:, market_indices]
            market_fit = np.mean(market_features, axis=1)
            differentiation = np.max(market_features, axis=1) - np.min(market_features, axis=1)
        else:
            market_fit = np.mean(X, axis=1)
            differentiation = np.std(X, axis=1)
            
        timing = np.array([np.percentile(row, 75) for row in X])
        
        return np.column_stack([market_fit, differentiation, timing])
        
    def predict(self, X):
        """Predict based on DNA patterns"""
        X_pca = self.pca.transform(X)
        clusters = self.kmeans.predict(X_pca)
        
        dna_features = np.column_stack([
            X_pca,
            clusters.reshape(-1, 1),
            self._extract_financial_dna(X),
            self._extract_growth_dna(X),
            self._extract_team_dna(X),
            self._extract_market_dna(X)
        ])
        
        return self.pattern_classifier.predict(dna_features)
        
    def predict_proba(self, X):
        """Predict probabilities based on DNA patterns"""
        X_pca = self.pca.transform(X)
        clusters = self.kmeans.predict(X_pca)
        
        dna_features = np.column_stack([
            X_pca,
            clusters.reshape(-1, 1),
            self._extract_financial_dna(X),
            self._extract_growth_dna(X),
            self._extract_team_dna(X),
            self._extract_market_dna(X)
        ])
        
        return self.pattern_classifier.predict_proba(dna_features)


class TemporalPredictionModel:
    """Model that considers temporal patterns and time-series aspects"""
    
    def __init__(self):
        self.lstm_approximator = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
        self.temporal_forest = RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            random_state=42
        )
        
    def fit(self, X, y):
        """Train temporal prediction model"""
        logger.info("Training temporal prediction model...")
        
        # Create temporal features
        temporal_features = self._create_temporal_features(X)
        
        # Train models
        self.lstm_approximator.fit(temporal_features, y)
        self.temporal_forest.fit(temporal_features, y)
        
        return self
        
    def _create_temporal_features(self, X):
        """Create time-based features"""
        # Moving averages (safe implementation)
        window_sizes = [3, 5, 7]
        ma_features = []
        
        for w in window_sizes:
            if X.shape[1] >= w:
                ma = np.array([np.convolve(row, np.ones(w)/w, mode='valid').mean() 
                              for row in X])
                ma_features.append(ma)
            else:
                ma_features.append(np.mean(X, axis=1))
                
        # Volatility measures
        volatility = np.std(X, axis=1)
        
        # Trend indicators
        if X.shape[1] > 1:
            trends = np.array([np.polyfit(range(X.shape[1]), row, 1)[0] for row in X])
        else:
            trends = np.zeros(X.shape[0])
        
        # Momentum indicators (safe)
        if X.shape[1] > 1:
            momentum = np.mean(np.diff(X, axis=1), axis=1)
        else:
            momentum = np.zeros(X.shape[0])
        
        # Seasonality proxy (using feature patterns)
        n_components = min(10, X.shape[1])
        if n_components > 0:
            seasonality = np.array([np.abs(np.fft.fft(row)[:n_components]).mean() for row in X])
        else:
            seasonality = np.zeros(X.shape[0])
        
        # Combine all temporal features
        temporal_features = np.column_stack([
            X,
            *ma_features,
            volatility,
            trends,
            momentum,
            seasonality
        ])
        
        return temporal_features
        
    def predict(self, X):
        """Make temporal predictions"""
        temporal_features = self._create_temporal_features(X)
        
        # Ensemble predictions
        lstm_pred = self.lstm_approximator.predict_proba(temporal_features)[:, 1]
        forest_pred = self.temporal_forest.predict_proba(temporal_features)[:, 1]
        
        # Weighted average
        final_pred = 0.6 * forest_pred + 0.4 * lstm_pred
        return (final_pred > 0.5).astype(int)
        
    def predict_proba(self, X):
        """Predict probabilities with temporal model"""
        temporal_features = self._create_temporal_features(X)
        
        # Ensemble predictions
        lstm_pred = self.lstm_approximator.predict_proba(temporal_features)
        forest_pred = self.temporal_forest.predict_proba(temporal_features)
        
        # Weighted average
        final_pred = 0.6 * forest_pred + 0.4 * lstm_pred
        return final_pred


class IndustrySpecificModel:
    """Model that considers industry-specific factors"""
    
    def __init__(self):
        self.industry_models = {}
        self.global_model = CatBoostClassifier(
            iterations=300,
            depth=6,
            learning_rate=0.05,
            random_seed=42,
            verbose=False
        )
        self.calibrator = IsotonicRegression(out_of_bounds='clip')
        self.industry_encoder = None
        
    def fit(self, X, y, industries=None):
        """Train industry-specific models"""
        logger.info("Training industry-specific model...")
        
        # If no industry info, create synthetic industries based on feature patterns
        if industries is None:
            industries = self._infer_industries(X)
        else:
            # Encode industry strings if provided
            self.industry_encoder = LabelEncoder()
            industries = self.industry_encoder.fit_transform(industries)
            
        # Train global model
        self.global_model.fit(X, y)
        
        # Train industry-specific models
        unique_industries = np.unique(industries)
        for industry in unique_industries:
            mask = industries == industry
            if np.sum(mask) > 100:  # Only create model if enough samples
                logger.info(f"Training model for industry {industry}")
                
                # Use XGBoost for even industries, RandomForest for odd
                if industry % 2 == 0:
                    model = xgb.XGBClassifier(
                        n_estimators=150,
                        max_depth=5,
                        learning_rate=0.1,
                        random_state=42,
                        use_label_encoder=False,
                        eval_metric='logloss'
                    )
                else:
                    model = RandomForestClassifier(
                        n_estimators=200,
                        max_depth=8,
                        random_state=42
                    )
                    
                model.fit(X[mask], y[mask])
                self.industry_models[industry] = model
                
        # Calibrate on validation predictions
        global_probs = self.global_model.predict_proba(X)[:, 1]
        self.calibrator.fit(global_probs, y)
        
        return self
        
    def _infer_industries(self, X):
        """Infer industries from feature patterns"""
        # Use clustering to create synthetic industries
        n_industries = min(8, X.shape[0] // 1000)  # Scale with data size
        kmeans = KMeans(n_clusters=n_industries, random_state=42)
        
        # Select features for clustering
        n_features = X.shape[1]
        if n_features > 5:
            # Use subset of features
            feature_indices = [
                min(20, n_features-1),  # Market feature
                min(35, n_features-1),  # Team feature
                0,  # First feature
                n_features//2,  # Middle feature
                n_features-1  # Last feature
            ]
            feature_indices = [i for i in feature_indices if i < n_features]
            industry_features = X[:, feature_indices]
        else:
            industry_features = X
        
        industries = kmeans.fit_predict(industry_features)
        return industries
        
    def predict(self, X, industries=None):
        """Make industry-aware predictions"""
        if industries is None:
            industries = self._infer_industries(X)
        elif self.industry_encoder is not None:
            industries = self.industry_encoder.transform(industries)
            
        predictions = np.zeros(len(X))
        
        # Get global predictions
        global_probs = self.global_model.predict_proba(X)[:, 1]
        global_probs_cal = self.calibrator.transform(global_probs)
        
        # Blend with industry-specific predictions where available
        for i, industry in enumerate(industries):
            if industry in self.industry_models:
                industry_prob = self.industry_models[industry].predict_proba(X[i:i+1])[:, 1]
                # Weighted average: 70% industry, 30% global
                predictions[i] = 0.7 * industry_prob + 0.3 * global_probs_cal[i]
            else:
                predictions[i] = global_probs_cal[i]
                
        return (predictions > 0.5).astype(int)
        
    def predict_proba(self, X, industries=None):
        """Predict probabilities with industry awareness"""
        if industries is None:
            industries = self._infer_industries(X)
        elif self.industry_encoder is not None:
            industries = self.industry_encoder.transform(industries)
            
        predictions = np.zeros((len(X), 2))
        
        # Get global predictions
        global_probs = self.global_model.predict_proba(X)[:, 1]
        global_probs_cal = self.calibrator.transform(global_probs)
        
        # Blend with industry-specific predictions where available
        for i, industry in enumerate(industries):
            if industry in self.industry_models:
                industry_prob = self.industry_models[industry].predict_proba(X[i:i+1])[:, 1][0]
                # Weighted average: 70% industry, 30% global
                prob = 0.7 * industry_prob + 0.3 * global_probs_cal[i]
            else:
                prob = global_probs_cal[i]
                
            predictions[i] = [1 - prob, prob]
                
        return predictions


def train_all_models():
    """Train all models to replace placeholders"""
    logger.info("Starting model training...")
    
    # Load data
    logger.info("Loading dataset...")
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    
    # Prepare preprocessor
    exclude_columns = ['success', 'startup_id', 'startup_name', 'burn_multiple_calc']
    preprocessor = DataPreprocessor()
    preprocessor.fit(df, exclude_columns)
    
    # Transform features
    X = preprocessor.transform(df)
    y = df['success'].values
    
    # Get industry information if available
    industries = df['sector'].values if 'sector' in df.columns else None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    if industries is not None:
        industries_train, industries_test = train_test_split(
            industries, test_size=0.2, random_state=42, stratify=y
        )
    else:
        industries_train = industries_test = None
    
    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    logger.info(f"Features: {X.shape[1]}")
    
    # Create directories
    Path('models/dna_analyzer').mkdir(parents=True, exist_ok=True)
    Path('models/temporal').mkdir(parents=True, exist_ok=True)
    Path('models/industry_specific').mkdir(parents=True, exist_ok=True)
    
    # Train DNA Pattern Analyzer
    logger.info("\n" + "="*50)
    logger.info("Training DNA Pattern Analyzer...")
    dna_model = DNAPatternAnalyzer()
    dna_model.preprocessor = preprocessor  # Store preprocessor
    dna_model.fit(X_train, y_train)
    
    # Evaluate DNA model
    dna_pred = dna_model.predict(X_test)
    dna_proba = dna_model.predict_proba(X_test)[:, 1]
    dna_auc = roc_auc_score(y_test, dna_proba)
    logger.info(f"DNA Model AUC: {dna_auc:.4f}")
    
    # Save DNA model
    joblib.dump(dna_model, 'models/dna_analyzer/dna_pattern_model.pkl')
    logger.info("DNA model saved to models/dna_analyzer/dna_pattern_model.pkl")
    
    # Train Temporal Prediction Model
    logger.info("\n" + "="*50)
    logger.info("Training Temporal Prediction Model...")
    temporal_model = TemporalPredictionModel()
    temporal_model.fit(X_train, y_train)
    
    # Evaluate temporal model
    temporal_pred = temporal_model.predict(X_test)
    temporal_proba = temporal_model.predict_proba(X_test)[:, 1]
    temporal_auc = roc_auc_score(y_test, temporal_proba)
    logger.info(f"Temporal Model AUC: {temporal_auc:.4f}")
    
    # Save temporal model
    joblib.dump(temporal_model, 'models/temporal_prediction_model.pkl')
    logger.info("Temporal model saved to models/temporal_prediction_model.pkl")
    
    # Train Industry-Specific Model
    logger.info("\n" + "="*50)
    logger.info("Training Industry-Specific Model...")
    industry_model = IndustrySpecificModel()
    industry_model.fit(X_train, y_train, industries_train)
    
    # Evaluate industry model
    industry_pred = industry_model.predict(X_test, industries_test)
    industry_proba = industry_model.predict_proba(X_test, industries_test)[:, 1]
    industry_auc = roc_auc_score(y_test, industry_proba)
    logger.info(f"Industry Model AUC: {industry_auc:.4f}")
    
    # Save industry model
    joblib.dump(industry_model, 'models/industry_specific_model.pkl')
    logger.info("Industry model saved to models/industry_specific_model.pkl")
    
    # Save preprocessor
    joblib.dump(preprocessor, 'models/data_preprocessor.pkl')
    logger.info("Preprocessor saved to models/data_preprocessor.pkl")
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("Model Training Complete!")
    logger.info(f"DNA Pattern Analyzer AUC: {dna_auc:.4f}")
    logger.info(f"Temporal Prediction Model AUC: {temporal_auc:.4f}")
    logger.info(f"Industry-Specific Model AUC: {industry_auc:.4f}")
    logger.info("\nAll models have been trained and saved successfully!")
    
    # Create model summary
    summary = {
        'training_date': datetime.now().isoformat(),
        'dataset': 'final_100k_dataset_45features.csv',
        'n_samples': len(df),
        'n_features': X.shape[1],
        'categorical_features': preprocessor.categorical_columns,
        'numerical_features': preprocessor.numerical_columns,
        'models': {
            'dna_pattern_analyzer': {
                'auc': float(dna_auc),
                'path': 'models/dna_analyzer/dna_pattern_model.pkl'
            },
            'temporal_prediction': {
                'auc': float(temporal_auc),
                'path': 'models/temporal_prediction_model.pkl'
            },
            'industry_specific': {
                'auc': float(industry_auc),
                'path': 'models/industry_specific_model.pkl'
            }
        },
        'preprocessor_path': 'models/data_preprocessor.pkl'
    }
    
    import json
    with open('models/model_training_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    return dna_auc, temporal_auc, industry_auc


if __name__ == "__main__":
    try:
        from xgboost import XGBClassifier
    except ImportError:
        logger.warning("XGBoost not installed. Installing...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'xgboost'])
        from xgboost import XGBClassifier
        
    train_all_models()