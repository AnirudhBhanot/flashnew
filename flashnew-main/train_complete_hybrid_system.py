#!/usr/bin/env python3
"""
Train Complete Hybrid System
Includes Pattern, Stage, Industry, and CAMP-specific models
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
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompleteHybridTrainer:
    """Train all components of the hybrid system"""
    
    def __init__(self, data_path="data/final_100k_dataset_45features.csv"):
        self.data_path = data_path
        self.output_dir = Path("models/complete_hybrid")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'models_trained': {},
            'average_performance': {}
        }
        
    def load_data(self):
        """Load and prepare data"""
        logger.info("Loading data...")
        self.df = pd.read_csv(self.data_path)
        
        # Prepare features
        feature_cols = [col for col in self.df.columns if col not in 
                       ['startup_id', 'startup_name', 'founding_year', 'success', 'burn_multiple_calc']]
        self.X = self.df[feature_cols].copy()
        self.y = self.df['success']
        
        # Handle categorical encoding
        self.categorical_cols = ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector']
        self.encoders = {}
        
        for col in self.categorical_cols:
            if col in self.X.columns:
                self.X[f'{col}_encoded'] = pd.Categorical(self.X[col]).codes
                self.encoders[col] = pd.Categorical(self.X[col]).categories
        
        logger.info(f"Loaded {len(self.df)} samples with {len(feature_cols)} features")
        
    def train_stage_models(self):
        """Train funding stage-specific models"""
        logger.info("\n" + "="*60)
        logger.info("Training Stage-Specific Models")
        logger.info("="*60)
        
        stage_models = {}
        stage_scores = {}
        
        # Define stages
        stages = ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Series C+']
        
        for stage in stages:
            stage_mask = self.df['funding_stage'] == stage
            stage_count = stage_mask.sum()
            
            if stage_count < 100:
                logger.warning(f"Skipping {stage} - only {stage_count} samples")
                continue
                
            logger.info(f"\nTraining {stage} model ({stage_count} samples)...")
            
            # Get stage-specific data
            X_stage = self.X[stage_mask]
            y_stage = self.y[stage_mask]
            
            # Balance with non-stage samples
            non_stage_mask = ~stage_mask
            non_stage_sample = min(stage_count * 2, non_stage_mask.sum())
            non_stage_idx = self.df[non_stage_mask].sample(non_stage_sample).index
            
            # Combine
            all_idx = X_stage.index.union(non_stage_idx)
            X_train_full = self.X.loc[all_idx]
            y_train_full = self.y.loc[all_idx]
            
            # Split
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_full, y_train_full, test_size=0.2, random_state=42, stratify=y_train_full
            )
            
            # Train model
            model = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                objective='binary',
                metric='auc',
                random_state=42,
                verbosity=-1
            )
            
            # Use encoded columns
            feature_cols = [col for col in X_train.columns if not col.endswith('_encoded')]
            feature_cols = [col for col in feature_cols if col not in self.categorical_cols]
            feature_cols.extend([f'{col}_encoded' for col in self.categorical_cols if f'{col}_encoded' in X_train.columns])
            
            model.fit(X_train[feature_cols], y_train)
            
            # Evaluate
            val_pred = model.predict_proba(X_val[feature_cols])[:, 1]
            val_auc = roc_auc_score(y_val, val_pred)
            
            logger.info(f"{stage} AUC: {val_auc:.4f}")
            
            # Save
            stage_models[stage] = model
            stage_scores[stage] = val_auc
            model_path = self.output_dir / f"stage_{stage.lower().replace(' ', '_').replace('+', '_plus')}_model.pkl"
            joblib.dump(model, model_path)
            
        self.results['models_trained']['stage_models'] = stage_scores
        self.results['average_performance']['stages'] = np.mean(list(stage_scores.values()))
        
        return stage_models, stage_scores
    
    def train_industry_models(self):
        """Train industry-specific models"""
        logger.info("\n" + "="*60)
        logger.info("Training Industry-Specific Models")
        logger.info("="*60)
        
        industry_models = {}
        industry_scores = {}
        
        # Get top industries
        top_industries = self.df['sector'].value_counts().head(10).index.tolist()
        
        for industry in top_industries:
            industry_mask = self.df['sector'] == industry
            industry_count = industry_mask.sum()
            
            if industry_count < 100:
                logger.warning(f"Skipping {industry} - only {industry_count} samples")
                continue
                
            logger.info(f"\nTraining {industry} model ({industry_count} samples)...")
            
            # Similar approach as stage models
            X_industry = self.X[industry_mask]
            y_industry = self.y[industry_mask]
            
            # Balance dataset
            non_industry_mask = ~industry_mask
            non_industry_sample = min(industry_count * 2, non_industry_mask.sum())
            non_industry_idx = self.df[non_industry_mask].sample(non_industry_sample).index
            
            all_idx = X_industry.index.union(non_industry_idx)
            X_train_full = self.X.loc[all_idx]
            y_train_full = self.y.loc[all_idx]
            
            # Split and train
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_full, y_train_full, test_size=0.2, random_state=42, stratify=y_train_full
            )
            
            # Choose model based on industry characteristics
            if industry in ['AI/ML', 'Biotech', 'Deep Tech']:
                # Complex industries benefit from XGBoost
                model = xgb.XGBClassifier(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    objective='binary:logistic',
                    use_label_encoder=False,
                    eval_metric='auc',
                    random_state=42
                )
            else:
                # Others use LightGBM
                model = lgb.LGBMClassifier(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    objective='binary',
                    metric='auc',
                    random_state=42,
                    verbosity=-1
                )
            
            # Prepare features
            feature_cols = [col for col in X_train.columns if not col.endswith('_encoded')]
            feature_cols = [col for col in feature_cols if col not in self.categorical_cols]
            feature_cols.extend([f'{col}_encoded' for col in self.categorical_cols if f'{col}_encoded' in X_train.columns])
            
            model.fit(X_train[feature_cols], y_train)
            
            # Evaluate
            val_pred = model.predict_proba(X_val[feature_cols])[:, 1]
            val_auc = roc_auc_score(y_val, val_pred)
            
            logger.info(f"{industry} AUC: {val_auc:.4f}")
            
            # Save
            industry_models[industry] = model
            industry_scores[industry] = val_auc
            model_path = self.output_dir / f"industry_{industry.lower().replace(' ', '_').replace('/', '_')}_model.pkl"
            joblib.dump(model, model_path)
            
        self.results['models_trained']['industry_models'] = industry_scores
        self.results['average_performance']['industries'] = np.mean(list(industry_scores.values()))
        
        return industry_models, industry_scores
    
    def train_camp_models(self):
        """Train CAMP-specific models"""
        logger.info("\n" + "="*60)
        logger.info("Training CAMP-Specific Models")
        logger.info("="*60)
        
        camp_models = {}
        camp_scores = {}
        
        # Define CAMP features
        camp_features = {
            'capital': ['total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd', 
                       'runway_months', 'burn_multiple', 'investor_tier_primary_encoded'],
            'advantage': ['patent_count', 'network_effects_present', 'has_data_moat', 
                         'regulatory_advantage_present', 'tech_differentiation_score', 
                         'switching_cost_score', 'brand_strength_score', 'scalability_score'],
            'market': ['tam_size_usd', 'sam_size_usd', 'som_size_usd', 'market_growth_rate_percent',
                      'customer_count', 'customer_concentration_percent', 'user_growth_rate_percent',
                      'net_dollar_retention_percent', 'competition_intensity', 'competitors_named_count',
                      'sector_encoded'],
            'people': ['founders_count', 'team_size_full_time', 'years_experience_avg',
                      'domain_expertise_years_avg', 'prior_startup_experience_count',
                      'prior_successful_exits_count', 'board_advisor_experience_score',
                      'advisors_count', 'team_diversity_percent', 'key_person_dependency']
        }
        
        for camp_type, features in camp_features.items():
            logger.info(f"\nTraining {camp_type.upper()} model...")
            
            # Filter features that exist
            available_features = [f for f in features if f in self.X.columns]
            
            # Add some general features for context
            general_features = ['funding_stage_encoded', 'product_stage_encoded', 
                              'annual_revenue_run_rate', 'revenue_growth_rate_percent']
            all_features = available_features + [f for f in general_features if f in self.X.columns]
            
            # Split data
            X_train, X_val, y_train, y_val = train_test_split(
                self.X[all_features], self.y, test_size=0.2, random_state=42, stratify=self.y
            )
            
            # Train focused model
            model = lgb.LGBMClassifier(
                n_estimators=150,  # More trees for focused learning
                max_depth=5,       # Slightly less depth
                learning_rate=0.1,
                objective='binary',
                metric='auc',
                random_state=42,
                verbosity=-1,
                feature_fraction=0.8,  # Use 80% of features per tree
                bagging_fraction=0.8,  # Use 80% of data per tree
                bagging_freq=5
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate
            val_pred = model.predict_proba(X_val)[:, 1]
            val_auc = roc_auc_score(y_val, val_pred)
            
            logger.info(f"{camp_type.upper()} AUC: {val_auc:.4f}")
            logger.info(f"Using {len(all_features)} features")
            
            # Save
            camp_models[camp_type] = model
            camp_scores[camp_type] = val_auc
            model_path = self.output_dir / f"camp_{camp_type}_model.pkl"
            joblib.dump(model, model_path)
            
        self.results['models_trained']['camp_models'] = camp_scores
        self.results['average_performance']['camp'] = np.mean(list(camp_scores.values()))
        
        return camp_models, camp_scores
    
    def train_all(self):
        """Train all model types"""
        logger.info("="*60)
        logger.info("Training Complete Hybrid System")
        logger.info("="*60)
        
        # Load data
        self.load_data()
        
        # Train all model types
        stage_models, stage_scores = self.train_stage_models()
        industry_models, industry_scores = self.train_industry_models()
        camp_models, camp_scores = self.train_camp_models()
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("TRAINING COMPLETE")
        logger.info("="*60)
        
        logger.info(f"\nStage Models: {len(stage_models)} trained")
        logger.info(f"Average Stage AUC: {self.results['average_performance']['stages']:.4f}")
        
        logger.info(f"\nIndustry Models: {len(industry_models)} trained")
        logger.info(f"Average Industry AUC: {self.results['average_performance']['industries']:.4f}")
        
        logger.info(f"\nCAMP Models: {len(camp_models)} trained")
        logger.info(f"Average CAMP AUC: {self.results['average_performance']['camp']:.4f}")
        
        # Overall average
        all_scores = list(stage_scores.values()) + list(industry_scores.values()) + list(camp_scores.values())
        overall_avg = np.mean(all_scores)
        self.results['average_performance']['overall'] = overall_avg
        
        logger.info(f"\nOVERALL AVERAGE AUC: {overall_avg:.4f}")
        
        # Save results
        with open(self.output_dir / 'training_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save encoders
        joblib.dump(self.encoders, self.output_dir / 'label_encoders.pkl')
        
        return self.results

if __name__ == "__main__":
    trainer = CompleteHybridTrainer()
    results = trainer.train_all()