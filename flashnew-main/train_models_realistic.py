#!/usr/bin/env python3
"""
Train production models on the new realistic dataset
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class RealisticModelTrainer:
    def __init__(self, dataset_path='realistic_startup_dataset_100k.csv'):
        self.dataset_path = dataset_path
        self.feature_columns = None
        self.models = {}
        self.results = {}
        
    def load_and_prepare_data(self):
        """Load dataset and prepare for training"""
        print(f"Loading dataset from {self.dataset_path}...")
        df = pd.read_csv(self.dataset_path)
        print(f"Loaded {len(df):,} companies")
        
        # Define feature columns (excluding target and identifiers)
        exclude_cols = ['success', 'company_name']
        self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        # Handle categorical variables
        categorical_cols = ['funding_stage', 'sector', 'product_stage', 'investor_tier_primary']
        
        # Create dummy variables
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
        
        # Update feature columns after encoding
        self.feature_columns = [col for col in df_encoded.columns 
                               if col not in exclude_cols and not col.startswith('success')]
        
        # Handle missing values - use median for numeric columns
        for col in self.feature_columns:
            if df_encoded[col].dtype in ['float64', 'int64']:
                df_encoded[col].fillna(df_encoded[col].median(), inplace=True)
        
        # Handle boolean columns
        bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 
                     'regulatory_advantage_present', 'key_person_dependency', 
                     'has_repeat_founder']
        
        for col in bool_cols:
            if col in df_encoded.columns:
                df_encoded[col] = df_encoded[col].astype(int)
        
        # Prepare features and target
        X = df_encoded[self.feature_columns]
        y = df_encoded['success']
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution: {y.value_counts(normalize=True).to_dict()}")
        
        return X, y, df_encoded
    
    def create_specialized_features(self, df):
        """Create specialized features for different models"""
        features = {}
        
        # DNA Analyzer features (patterns and signals)
        dna_features = []
        
        # Growth patterns
        if 'revenue_growth_rate_percent' in df.columns:
            dna_features.append('revenue_growth_rate_percent')
        if 'user_growth_rate_percent' in df.columns:
            dna_features.append('user_growth_rate_percent')
        
        # Efficiency genes
        for col in ['burn_multiple', 'ltv_cac_ratio', 'gross_margin_percent', 
                    'cash_efficiency_score', 'operating_leverage_trend']:
            if col in df.columns:
                dna_features.append(col)
        
        # Market signals
        for col in ['market_growth_rate_percent', 'tam_size_usd', 'competition_intensity']:
            if col in df.columns:
                dna_features.append(col)
        
        # Founder DNA
        for col in ['prior_successful_exits_count', 'years_experience_avg', 
                    'domain_expertise_years_avg', 'has_repeat_founder']:
            if col in df.columns:
                dna_features.append(col)
        
        features['dna'] = dna_features
        
        # Temporal features (time-based metrics)
        temporal_features = []
        
        # Age and runway
        for col in ['company_age_months', 'runway_months', 'monthly_burn_usd']:
            if col in df.columns:
                temporal_features.append(col)
        
        # Growth over time
        if 'revenue_growth_rate_percent' in df.columns:
            temporal_features.append('revenue_growth_rate_percent')
        
        features['temporal'] = temporal_features
        
        # Industry-specific features
        industry_features = []
        
        # Sector dummies
        sector_cols = [col for col in df.columns if col.startswith('sector_')]
        industry_features.extend(sector_cols)
        
        # Industry-relevant metrics
        for col in ['gross_margin_percent', 'ltv_cac_ratio', 'net_dollar_retention_percent',
                    'customer_concentration_percent', 'regulatory_advantage_present']:
            if col in df.columns:
                industry_features.append(col)
        
        features['industry'] = industry_features
        
        return features
    
    def train_dna_analyzer(self, X_train, X_test, y_train, y_test, feature_names):
        """Train DNA Analyzer model"""
        print("\n" + "="*60)
        print("Training DNA Analyzer Model...")
        print("="*60)
        
        # Use specialized DNA features if available
        dna_features = [f for f in feature_names.get('dna', []) if f in X_train.columns]
        if len(dna_features) < 10:  # If not enough specialized features, use all
            X_train_dna = X_train
            X_test_dna = X_test
        else:
            X_train_dna = X_train[dna_features]
            X_test_dna = X_test[dna_features]
        
        # Random Forest for pattern recognition
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=50,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_dna, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_dna)
        y_pred_proba = model.predict_proba(X_test_dna)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"DNA Analyzer - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        
        self.models['dna_analyzer'] = model
        self.results['dna_analyzer'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train_dna.shape[1]
        }
        
        return model
    
    def train_temporal_model(self, X_train, X_test, y_train, y_test, feature_names):
        """Train Temporal Prediction Model"""
        print("\n" + "="*60)
        print("Training Temporal Model...")
        print("="*60)
        
        # XGBoost for temporal patterns
        model = XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Temporal Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        
        self.models['temporal_model'] = model
        self.results['temporal_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1]
        }
        
        return model
    
    def train_industry_model(self, X_train, X_test, y_train, y_test, feature_names):
        """Train Industry-Specific Model"""
        print("\n" + "="*60)
        print("Training Industry Model...")
        print("="*60)
        
        # XGBoost for industry patterns
        model = XGBClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Industry Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        
        self.models['industry_model'] = model
        self.results['industry_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1]
        }
        
        return model
    
    def train_ensemble_model(self, X_train, X_test, y_train, y_test):
        """Train Ensemble Model"""
        print("\n" + "="*60)
        print("Training Ensemble Model...")
        print("="*60)
        
        # Random Forest ensemble
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=50,
            min_samples_leaf=20,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Ensemble Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        
        self.models['ensemble_model'] = model
        self.results['ensemble_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1]
        }
        
        return model
    
    def save_models(self, output_dir='models/production_realistic/'):
        """Save trained models"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving models to {output_dir}...")
        
        # Save each model
        for model_name, model in self.models.items():
            filepath = os.path.join(output_dir, f"{model_name}.pkl")
            with open(filepath, 'wb') as f:
                pickle.dump(model, f)
            print(f"  Saved {model_name}.pkl")
        
        # Save feature columns
        with open(os.path.join(output_dir, 'feature_columns.pkl'), 'wb') as f:
            pickle.dump(self.feature_columns, f)
        
        # Save model metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'dataset': self.dataset_path,
            'n_samples': len(pd.read_csv(self.dataset_path)),
            'n_features': len(self.feature_columns),
            'models': self.results,
            'average_auc': np.mean([r['auc'] for r in self.results.values()]),
            'feature_columns': self.feature_columns[:20]  # Save first 20 for reference
        }
        
        with open(os.path.join(output_dir, 'model_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel training complete!")
        print(f"Average AUC across all models: {metadata['average_auc']:.3f}")
    
    def train_all(self):
        """Train all models"""
        # Load and prepare data
        X, y, df_encoded = self.load_and_prepare_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set size: {len(X_train):,}")
        print(f"Test set size: {len(X_test):,}")
        
        # Create specialized features
        feature_names = self.create_specialized_features(df_encoded)
        
        # Train models
        self.train_dna_analyzer(X_train, X_test, y_train, y_test, feature_names)
        self.train_temporal_model(X_train, X_test, y_train, y_test, feature_names)
        self.train_industry_model(X_train, X_test, y_train, y_test, feature_names)
        self.train_ensemble_model(X_train, X_test, y_train, y_test)
        
        # Save models
        self.save_models()
        
        # Print summary
        print("\n" + "="*60)
        print("TRAINING SUMMARY")
        print("="*60)
        for model_name, results in self.results.items():
            print(f"{model_name}:")
            print(f"  AUC: {results['auc']:.3f}")
            print(f"  Accuracy: {results['accuracy']:.3f}")
            print(f"  Features: {results['features_used']}")
        
        avg_auc = np.mean([r['auc'] for r in self.results.values()])
        print(f"\nAverage AUC: {avg_auc:.3f}")
        
        # Save training report
        self.save_training_report()
    
    def save_training_report(self):
        """Save detailed training report"""
        report = []
        report.append("="*60)
        report.append("MODEL TRAINING REPORT - REALISTIC DATASET")
        report.append("="*60)
        report.append(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Dataset: {self.dataset_path}")
        report.append("")
        
        for model_name, results in self.results.items():
            report.append(f"\n{model_name.upper()}:")
            report.append(f"  AUC Score: {results['auc']:.3f}")
            report.append(f"  Accuracy: {results['accuracy']:.3f}")
            report.append(f"  Features Used: {results['features_used']}")
        
        avg_auc = np.mean([r['auc'] for r in self.results.values()])
        report.append(f"\nAVERAGE AUC: {avg_auc:.3f}")
        
        report.append("\nNOTE: These models are trained on realistic data with:")
        report.append("- 85% of pre-seed companies have $0 revenue")
        report.append("- Natural missing data patterns")
        report.append("- Realistic team sizes and funding amounts")
        report.append("- 16% overall success rate")
        
        with open('training_report_realistic.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("\nTraining report saved to training_report_realistic.txt")


def main():
    """Main training function"""
    print("Starting model training on realistic dataset...")
    print("="*60)
    
    trainer = RealisticModelTrainer()
    trainer.train_all()
    
    print("\nTraining complete! Models saved to models/production_realistic/")
    print("\nTo use these models, update your API server to load from the new directory.")


if __name__ == "__main__":
    main()