#!/usr/bin/env python3
"""
Train balanced models using class weights instead of SMOTE
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
import warnings
warnings.filterwarnings('ignore')

class SimpleModelTrainer:
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
        
        # Handle categorical variables
        categorical_cols = ['funding_stage', 'sector', 'product_stage', 'investor_tier_primary']
        
        # Create dummy variables
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
        
        # Get feature columns after encoding
        self.feature_columns = [col for col in df_encoded.columns 
                               if col not in exclude_cols]
        
        # Handle missing values intelligently
        print("Handling missing values...")
        for col in self.feature_columns:
            if df_encoded[col].dtype in ['float64', 'int64']:
                # For revenue/customer fields, missing = 0
                if any(keyword in col for keyword in ['revenue', 'customer', 'retention', 'ltv', 'dau']):
                    df_encoded[col].fillna(0, inplace=True)
                else:
                    df_encoded[col].fillna(df_encoded[col].median(), inplace=True)
        
        # Handle boolean columns
        bool_cols = ['has_debt', 'network_effects_present', 'has_data_moat', 
                     'regulatory_advantage_present', 'key_person_dependency', 
                     'has_repeat_founder']
        
        for col in bool_cols:
            if col in df_encoded.columns:
                df_encoded[col] = df_encoded[col].astype(int)
        
        # Engineer key features
        print("Engineering features...")
        
        # Capital efficiency (avoiding division by zero)
        df_encoded['capital_efficiency'] = np.where(
            (df_encoded['total_capital_raised_usd'] > 0) & (df_encoded['annual_revenue_run_rate'] > 0),
            df_encoded['annual_revenue_run_rate'] / df_encoded['total_capital_raised_usd'],
            0
        )
        
        # Burn efficiency
        df_encoded['burn_efficiency'] = np.where(
            df_encoded['monthly_burn_usd'] > 0,
            df_encoded['cash_on_hand_usd'] / (df_encoded['monthly_burn_usd'] * 12),
            1
        )
        
        # Team productivity
        df_encoded['revenue_per_employee'] = np.where(
            df_encoded['team_size_full_time'] > 0,
            df_encoded['annual_revenue_run_rate'] / df_encoded['team_size_full_time'],
            0
        )
        
        # Growth potential
        df_encoded['growth_potential'] = np.where(
            df_encoded['tam_size_usd'] > 0,
            (df_encoded['som_size_usd'] / df_encoded['tam_size_usd']) * df_encoded['market_growth_rate_percent'],
            0
        )
        
        # Experience score
        df_encoded['experience_score'] = (
            df_encoded['years_experience_avg'] * 0.3 +
            df_encoded['domain_expertise_years_avg'] * 0.4 +
            df_encoded['prior_startup_experience_count'] * 5 +
            df_encoded['prior_successful_exits_count'] * 10
        )
        
        # Update feature columns
        self.feature_columns = [col for col in df_encoded.columns 
                               if col not in exclude_cols]
        
        # Prepare features and target
        X = df_encoded[self.feature_columns]
        y = df_encoded['success'].astype(int)
        
        print(f"Features shape: {X.shape}")
        print(f"Success rate: {y.mean():.2%}")
        
        return X, y
    
    def train_model(self, X_train, X_test, y_train, y_test, model_name, model_type='rf'):
        """Train a single model with proper class balancing"""
        print(f"\n{'='*60}")
        print(f"Training {model_name}...")
        print(f"{'='*60}")
        
        # Calculate class weights
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = dict(zip(classes, class_weights))
        
        print(f"Class weights: {class_weight_dict}")
        
        if model_type == 'rf':
            model = RandomForestClassifier(
                n_estimators=300,
                max_depth=15,
                min_samples_split=20,
                min_samples_leaf=10,
                max_features='sqrt',
                class_weight=class_weight_dict,
                random_state=42,
                n_jobs=-1
            )
        else:  # xgb
            scale_pos_weight = class_weights[1] / class_weights[0]
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
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Evaluate
        auc = roc_auc_score(y_test, y_pred_proba)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        tpr = tp / (tp + fn)  # Sensitivity / Recall
        tnr = tn / (tn + fp)  # Specificity
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        
        print(f"\nResults for {model_name}:")
        print(f"AUC: {auc:.3f}")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"True Positive Rate (Sensitivity): {tpr:.3f}")
        print(f"True Negative Rate (Specificity): {tnr:.3f}")
        print(f"Precision: {precision:.3f}")
        print(f"\nConfusion Matrix:")
        print(f"              Predicted")
        print(f"              0      1")
        print(f"Actual 0  {tn:5d}  {fp:5d}")
        print(f"       1  {fn:5d}  {tp:5d}")
        
        # Feature importance for RF models
        if model_type == 'rf' and hasattr(model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False).head(15)
            
            print(f"\nTop 15 Features for {model_name}:")
            for idx, row in feature_importance.iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
        
        # Store results
        self.models[model_name] = model
        self.results[model_name] = {
            'auc': auc,
            'accuracy': accuracy,
            'tpr': tpr,
            'tnr': tnr,
            'precision': precision,
            'confusion_matrix': cm.tolist()
        }
        
        return model
    
    def train_all(self):
        """Train all models"""
        # Load data
        X, y = self.load_and_prepare_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set: {len(X_train):,} samples")
        print(f"Test set: {len(X_test):,} samples")
        print(f"Features: {X_train.shape[1]}")
        
        # Train models
        self.train_model(X_train, X_test, y_train, y_test, 'dna_analyzer', 'rf')
        self.train_model(X_train, X_test, y_train, y_test, 'temporal_model', 'xgb')
        self.train_model(X_train, X_test, y_train, y_test, 'industry_model', 'xgb')
        self.train_model(X_train, X_test, y_train, y_test, 'ensemble_model', 'rf')
        
        # Save everything
        self.save_models()
        self.print_summary()
    
    def save_models(self):
        """Save trained models"""
        import os
        output_dir = 'models/production_v46_realistic/'
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nSaving models to {output_dir}...")
        
        # Save models
        for name, model in self.models.items():
            with open(os.path.join(output_dir, f"{name}.pkl"), 'wb') as f:
                pickle.dump(model, f)
            print(f"  Saved {name}.pkl")
        
        # Save metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'dataset': self.dataset_path,
            'n_features': len(self.feature_columns),
            'feature_columns': self.feature_columns,
            'models': self.results,
            'average_auc': np.mean([r['auc'] for r in self.results.values()]),
            'dataset_info': {
                'total_samples': 100000,
                'success_rate': 0.16,
                'pre_seed_no_revenue': 0.85,
                'realistic': True
            }
        }
        
        with open(os.path.join(output_dir, 'model_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save scaler and feature columns separately
        with open(os.path.join(output_dir, 'feature_columns.pkl'), 'wb') as f:
            pickle.dump(self.feature_columns, f)
    
    def print_summary(self):
        """Print training summary"""
        print("\n" + "="*60)
        print("TRAINING SUMMARY - REALISTIC MODELS")
        print("="*60)
        
        # Calculate averages
        avg_auc = np.mean([r['auc'] for r in self.results.values()])
        avg_tpr = np.mean([r['tpr'] for r in self.results.values()])
        avg_tnr = np.mean([r['tnr'] for r in self.results.values()])
        
        print(f"\nModel Performance:")
        print(f"{'Model':<20} {'AUC':>8} {'TPR':>8} {'TNR':>8} {'Accuracy':>8}")
        print("-" * 60)
        
        for name, results in self.results.items():
            print(f"{name:<20} {results['auc']:>8.3f} {results['tpr']:>8.3f} "
                  f"{results['tnr']:>8.3f} {results['accuracy']:>8.3f}")
        
        print("-" * 60)
        print(f"{'AVERAGE':<20} {avg_auc:>8.3f} {avg_tpr:>8.3f} {avg_tnr:>8.3f}")
        
        print(f"\nKey Insights:")
        print(f"- Models trained on truly realistic data")
        print(f"- Average AUC: {avg_auc:.3f} (realistic for hard problem)")
        print(f"- Models can identify {avg_tpr:.1%} of successful startups")
        print(f"- Models correctly reject {avg_tnr:.1%} of failing startups")
        
        # Save report
        report = [
            "="*60,
            "REALISTIC MODEL TRAINING REPORT",
            "="*60,
            f"Date: {datetime.now()}",
            f"Dataset: {self.dataset_path}",
            "",
            "Model Performance:",
            f"Average AUC: {avg_auc:.3f}",
            f"Average TPR: {avg_tpr:.3f}",
            f"Average TNR: {avg_tnr:.3f}",
            "",
            "Individual Models:"
        ]
        
        for name, results in self.results.items():
            report.append(f"\n{name}:")
            report.append(f"  AUC: {results['auc']:.3f}")
            report.append(f"  TPR: {results['tpr']:.3f}")
            report.append(f"  TNR: {results['tnr']:.3f}")
        
        with open('training_report_final.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("\nReport saved to training_report_final.txt")


def main():
    print("Training models on realistic startup dataset...")
    print("This dataset represents real-world startup characteristics.")
    
    trainer = SimpleModelTrainer()
    trainer.train_all()
    
    print("\n✅ Training complete!")
    print("Models saved to: models/production_v46_realistic/")
    print("\nThese models are trained on realistic data where:")
    print("- 85% of pre-seed have $0 revenue")
    print("- Natural failure patterns")
    print("- Realistic team sizes and funding")


if __name__ == "__main__":
    main()