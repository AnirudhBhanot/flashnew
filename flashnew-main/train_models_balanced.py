#!/usr/bin/env python3
"""
Train balanced models on realistic dataset with proper handling of class imbalance
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.utils.class_weight import compute_class_weight
import warnings
warnings.filterwarnings('ignore')

class BalancedModelTrainer:
    def __init__(self, dataset_path='realistic_startup_dataset_100k.csv'):
        self.dataset_path = dataset_path
        self.feature_columns = None
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        
    def load_and_prepare_data(self):
        """Load dataset and prepare for training"""
        print(f"Loading dataset from {self.dataset_path}...")
        df = pd.read_csv(self.dataset_path)
        print(f"Loaded {len(df):,} companies")
        
        # Define feature columns (excluding target and identifiers)
        exclude_cols = ['success', 'company_name']
        
        # Handle categorical variables first
        categorical_cols = ['funding_stage', 'sector', 'product_stage', 'investor_tier_primary']
        
        # Create dummy variables
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
        
        # Get feature columns after encoding
        self.feature_columns = [col for col in df_encoded.columns 
                               if col not in exclude_cols]
        
        # Handle missing values more intelligently
        print("Handling missing values...")
        
        # For numeric columns, use different strategies based on the column
        for col in self.feature_columns:
            if df_encoded[col].dtype in ['float64', 'int64']:
                missing_pct = df_encoded[col].isnull().sum() / len(df_encoded) * 100
                
                if missing_pct > 0:
                    # For revenue/customer related fields, missing often means 0
                    if any(keyword in col for keyword in ['revenue', 'customer', 'retention', 'ltv', 'dau']):
                        df_encoded[col].fillna(0, inplace=True)
                    # For other fields, use median
                    else:
                        df_encoded[col].fillna(df_encoded[col].median(), inplace=True)
        
        # Handle boolean columns
        bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 
                     'regulatory_advantage_present', 'key_person_dependency', 
                     'has_repeat_founder']
        
        for col in bool_cols:
            if col in df_encoded.columns:
                df_encoded[col] = df_encoded[col].astype(int)
        
        # Create some engineered features that might help
        print("Engineering features...")
        
        # Capital efficiency
        df_encoded['capital_efficiency'] = np.where(
            df_encoded['annual_revenue_run_rate'] > 0,
            df_encoded['annual_revenue_run_rate'] / (df_encoded['total_capital_raised_usd'] + 1),
            0
        )
        
        # Burn rate relative to funding
        df_encoded['relative_burn'] = np.where(
            df_encoded['cash_on_hand_usd'] > 0,
            df_encoded['monthly_burn_usd'] / (df_encoded['cash_on_hand_usd'] + 1),
            1
        )
        
        # Team productivity
        df_encoded['revenue_per_employee'] = np.where(
            df_encoded['team_size_full_time'] > 0,
            df_encoded['annual_revenue_run_rate'] / df_encoded['team_size_full_time'],
            0
        )
        
        # Market opportunity score
        df_encoded['market_opportunity'] = np.where(
            df_encoded['tam_size_usd'] > 0,
            df_encoded['som_size_usd'] / df_encoded['tam_size_usd'],
            0
        )
        
        # Update feature columns
        self.feature_columns = [col for col in df_encoded.columns 
                               if col not in exclude_cols]
        
        # Prepare features and target
        X = df_encoded[self.feature_columns]
        y = df_encoded['success'].astype(int)
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution: {y.value_counts(normalize=True).to_dict()}")
        
        return X, y, df_encoded
    
    def balance_dataset(self, X_train, y_train):
        """Balance the training dataset using SMOTE"""
        print("\nBalancing dataset with SMOTE...")
        print(f"Before balancing: {y_train.value_counts().to_dict()}")
        
        # Apply SMOTE
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_balanced, y_balanced = smote.fit_resample(X_train, y_train)
        
        print(f"After balancing: {pd.Series(y_balanced).value_counts().to_dict()}")
        
        return X_balanced, y_balanced
    
    def train_dna_analyzer(self, X_train, X_test, y_train, y_test):
        """Train DNA Analyzer model with balanced data"""
        print("\n" + "="*60)
        print("Training DNA Analyzer Model (Balanced)...")
        print("="*60)
        
        # Balance the training data
        X_balanced, y_balanced = self.balance_dataset(X_train, y_train)
        
        # Scale features
        X_balanced_scaled = self.scaler.fit_transform(X_balanced)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Random Forest with balanced parameters
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=15,
            min_samples_split=20,
            min_samples_leaf=10,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        model.fit(X_balanced_scaled, y_balanced)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"DNA Analyzer - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        print(f"Confusion Matrix:\n{cm}")
        print(f"True Positive Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.3f}")
        print(f"True Negative Rate: {cm[0,0]/(cm[0,0]+cm[0,1]):.3f}")
        
        self.models['dna_analyzer'] = model
        self.results['dna_analyzer'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1],
            'tpr': cm[1,1]/(cm[1,0]+cm[1,1]),
            'tnr': cm[0,0]/(cm[0,0]+cm[0,1])
        }
        
        return model
    
    def train_temporal_model(self, X_train, X_test, y_train, y_test):
        """Train Temporal Prediction Model with balanced data"""
        print("\n" + "="*60)
        print("Training Temporal Model (Balanced)...")
        print("="*60)
        
        # Calculate scale_pos_weight for XGBoost
        scale_pos_weight = len(y_train[y_train==0]) / len(y_train[y_train==1])
        
        # XGBoost with balanced parameters
        model = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
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
        
        # Get confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"Temporal Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        print(f"Confusion Matrix:\n{cm}")
        print(f"True Positive Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.3f}")
        print(f"True Negative Rate: {cm[0,0]/(cm[0,0]+cm[0,1]):.3f}")
        
        self.models['temporal_model'] = model
        self.results['temporal_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1],
            'tpr': cm[1,1]/(cm[1,0]+cm[1,1]),
            'tnr': cm[0,0]/(cm[0,0]+cm[0,1])
        }
        
        return model
    
    def train_industry_model(self, X_train, X_test, y_train, y_test):
        """Train Industry-Specific Model with balanced data"""
        print("\n" + "="*60)
        print("Training Industry Model (Balanced)...")
        print("="*60)
        
        # Balance the training data
        X_balanced, y_balanced = self.balance_dataset(X_train, y_train)
        
        # XGBoost for industry patterns
        model = XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        model.fit(X_balanced, y_balanced)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"Industry Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        print(f"Confusion Matrix:\n{cm}")
        print(f"True Positive Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.3f}")
        print(f"True Negative Rate: {cm[0,0]/(cm[0,0]+cm[0,1]):.3f}")
        
        self.models['industry_model'] = model
        self.results['industry_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1],
            'tpr': cm[1,1]/(cm[1,0]+cm[1,1]),
            'tnr': cm[0,0]/(cm[0,0]+cm[0,1])
        }
        
        return model
    
    def train_ensemble_model(self, X_train, X_test, y_train, y_test):
        """Train Ensemble Model with balanced data"""
        print("\n" + "="*60)
        print("Training Ensemble Model (Balanced)...")
        print("="*60)
        
        # Calculate class weights
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = dict(zip(classes, class_weights))
        
        # Random Forest ensemble with class weights
        model = RandomForestClassifier(
            n_estimators=400,
            max_depth=20,
            min_samples_split=20,
            min_samples_leaf=10,
            max_features='sqrt',
            class_weight=class_weight_dict,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"Ensemble Model - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
        print(f"Confusion Matrix:\n{cm}")
        print(f"True Positive Rate: {cm[1,1]/(cm[1,0]+cm[1,1]):.3f}")
        print(f"True Negative Rate: {cm[0,0]/(cm[0,0]+cm[0,1]):.3f}")
        
        # Feature importance analysis
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False).head(20)
        
        print("\nTop 20 Most Important Features:")
        for idx, row in feature_importance.iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
        
        self.models['ensemble_model'] = model
        self.results['ensemble_model'] = {
            'auc': auc,
            'accuracy': accuracy,
            'features_used': X_train.shape[1],
            'tpr': cm[1,1]/(cm[1,0]+cm[1,1]),
            'tnr': cm[0,0]/(cm[0,0]+cm[0,1]),
            'top_features': feature_importance.to_dict('records')
        }
        
        return model
    
    def save_models(self, output_dir='models/production_realistic_balanced/'):
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
        
        # Save scaler
        with open(os.path.join(output_dir, 'scaler.pkl'), 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save model metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'dataset': self.dataset_path,
            'n_samples': 100000,
            'n_features': len(self.feature_columns),
            'models': self.results,
            'average_auc': np.mean([r['auc'] for r in self.results.values()]),
            'average_tpr': np.mean([r['tpr'] for r in self.results.values()]),
            'average_tnr': np.mean([r['tnr'] for r in self.results.values()])
        }
        
        with open(os.path.join(output_dir, 'model_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nModel training complete!")
        print(f"Average AUC across all models: {metadata['average_auc']:.3f}")
        print(f"Average True Positive Rate: {metadata['average_tpr']:.3f}")
        print(f"Average True Negative Rate: {metadata['average_tnr']:.3f}")
    
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
        print(f"Class distribution in training: {y_train.value_counts(normalize=True).to_dict()}")
        
        # Train models
        self.train_dna_analyzer(X_train, X_test, y_train, y_test)
        self.train_temporal_model(X_train, X_test, y_train, y_test)
        self.train_industry_model(X_train, X_test, y_train, y_test)
        self.train_ensemble_model(X_train, X_test, y_train, y_test)
        
        # Save models
        self.save_models()
        
        # Print summary
        print("\n" + "="*60)
        print("TRAINING SUMMARY (BALANCED)")
        print("="*60)
        for model_name, results in self.results.items():
            print(f"{model_name}:")
            print(f"  AUC: {results['auc']:.3f}")
            print(f"  Accuracy: {results['accuracy']:.3f}")
            print(f"  True Positive Rate: {results['tpr']:.3f}")
            print(f"  True Negative Rate: {results['tnr']:.3f}")
        
        avg_auc = np.mean([r['auc'] for r in self.results.values()])
        print(f"\nAverage AUC: {avg_auc:.3f}")
        
        # Save training report
        self.save_training_report()
    
    def save_training_report(self):
        """Save detailed training report"""
        report = []
        report.append("="*60)
        report.append("MODEL TRAINING REPORT - REALISTIC DATASET (BALANCED)")
        report.append("="*60)
        report.append(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Dataset: {self.dataset_path}")
        report.append("")
        
        for model_name, results in self.results.items():
            report.append(f"\n{model_name.upper()}:")
            report.append(f"  AUC Score: {results['auc']:.3f}")
            report.append(f"  Accuracy: {results['accuracy']:.3f}")
            report.append(f"  True Positive Rate: {results['tpr']:.3f}")
            report.append(f"  True Negative Rate: {results['tnr']:.3f}")
            report.append(f"  Features Used: {results['features_used']}")
        
        avg_auc = np.mean([r['auc'] for r in self.results.values()])
        avg_tpr = np.mean([r['tpr'] for r in self.results.values()])
        avg_tnr = np.mean([r['tnr'] for r in self.results.values()])
        
        report.append(f"\nAVERAGE METRICS:")
        report.append(f"  Average AUC: {avg_auc:.3f}")
        report.append(f"  Average TPR: {avg_tpr:.3f}")
        report.append(f"  Average TNR: {avg_tnr:.3f}")
        
        report.append("\nKEY IMPROVEMENTS:")
        report.append("- Used SMOTE for balancing training data")
        report.append("- Applied class weights for imbalanced learning")
        report.append("- Added engineered features for better signal")
        report.append("- Properly handled missing values")
        
        report.append("\nDATASET CHARACTERISTICS:")
        report.append("- 85% of pre-seed companies have $0 revenue")
        report.append("- Natural missing data patterns")
        report.append("- Realistic team sizes and funding amounts")
        report.append("- 16% overall success rate")
        report.append("- Power law distributions")
        
        with open('training_report_balanced.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("\nTraining report saved to training_report_balanced.txt")


def main():
    """Main training function"""
    print("Starting balanced model training on realistic dataset...")
    print("="*60)
    
    trainer = BalancedModelTrainer()
    trainer.train_all()
    
    print("\nTraining complete! Models saved to models/production_realistic_balanced/")
    print("\nThese models are properly balanced and should give meaningful predictions")
    print("for both successful and unsuccessful startups.")


if __name__ == "__main__":
    main()