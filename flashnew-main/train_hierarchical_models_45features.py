"""
Train Hierarchical Models for 45-Feature Dataset
Implements Stage-Based, Temporal, Industry-Specific, and DNA Pattern models
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import catboost as cb
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import logging
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define feature groups based on CAMP framework
CAPITAL_FEATURES = [
    'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
    'runway_months', 'burn_multiple', 'investor_tier_primary', 'has_debt'
]

ADVANTAGE_FEATURES = [
    'patent_count', 'network_effects_present', 'has_data_moat',
    'regulatory_advantage_present', 'tech_differentiation_score',
    'switching_cost_score', 'brand_strength_score', 'scalability_score'
]

MARKET_FEATURES = [
    'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
    'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
    'user_growth_rate_percent', 'net_dollar_retention_percent',
    'competition_intensity', 'competitors_named_count'
]

PEOPLE_FEATURES = [
    'founders_count', 'team_size_full_time', 'years_experience_avg',
    'domain_expertise_years_avg', 'prior_startup_experience_count',
    'prior_successful_exits_count', 'board_advisor_experience_score',
    'advisors_count', 'team_diversity_percent', 'key_person_dependency'
]

PRODUCT_FEATURES = [
    'product_stage', 'product_retention_30d', 'product_retention_90d',
    'dau_mau_ratio', 'annual_revenue_run_rate', 'revenue_growth_rate_percent',
    'gross_margin_percent', 'ltv_cac_ratio'
]

ALL_FEATURES = CAPITAL_FEATURES + ADVANTAGE_FEATURES + MARKET_FEATURES + PEOPLE_FEATURES + PRODUCT_FEATURES


class StageBasedHierarchicalModel:
    """Stage-specific models with different feature weightings"""
    
    def __init__(self):
        self.stage_models = {}
        self.stage_weights = {
            'pre_seed': {'people': 0.4, 'advantage': 0.3, 'market': 0.2, 'capital': 0.1},
            'seed': {'people': 0.3, 'advantage': 0.3, 'market': 0.25, 'capital': 0.15},
            'series_a': {'market': 0.3, 'advantage': 0.25, 'capital': 0.25, 'people': 0.2},
            'series_b': {'market': 0.35, 'capital': 0.3, 'advantage': 0.2, 'people': 0.15},
            'series_c': {'capital': 0.4, 'market': 0.3, 'advantage': 0.2, 'people': 0.1}
        }
        self.meta_model = None
        
    def map_funding_stage(self, stage):
        """Map funding stages to simplified categories"""
        stage_lower = stage.lower()
        if 'pre' in stage_lower or 'angel' in stage_lower:
            return 'pre_seed'
        elif 'seed' in stage_lower:
            return 'seed'
        elif 'series a' in stage_lower or 'seriesa' in stage_lower:
            return 'series_a'
        elif 'series b' in stage_lower or 'seriesb' in stage_lower:
            return 'series_b'
        else:  # Series C+
            return 'series_c'
    
    def train(self, X, y):
        """Train stage-specific models"""
        # Add simplified stage column
        X['stage_simplified'] = X['funding_stage'].apply(self.map_funding_stage)
        
        for stage in ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']:
            stage_mask = X['stage_simplified'] == stage
            if stage_mask.sum() < 100:
                logger.warning(f"Skipping {stage} - insufficient data ({stage_mask.sum()} samples)")
                continue
                
            X_stage = X[stage_mask][ALL_FEATURES]
            y_stage = y[stage_mask]
            
            # Train CatBoost model for this stage
            model = cb.CatBoostClassifier(
                iterations=300,
                learning_rate=0.03,
                depth=6,
                l2_leaf_reg=3,
                random_seed=42,
                verbose=False,
                task_type='CPU',
                thread_count=-1
            )
            
            # Handle categorical features
            cat_features = ['sector', 'product_stage', 'investor_tier_primary']
            cat_indices = [X_stage.columns.get_loc(col) for col in cat_features if col in X_stage.columns]
            
            model.fit(X_stage, y_stage, cat_features=cat_indices)
            self.stage_models[stage] = model
            
            logger.info(f"Trained {stage} model - AUC: {roc_auc_score(y_stage, model.predict_proba(X_stage)[:, 1]):.3f}")
        
        # Train meta-model on stage predictions
        stage_predictions = self._get_stage_predictions(X[ALL_FEATURES], X['stage_simplified'])
        self.meta_model = cb.CatBoostClassifier(
            iterations=100,
            learning_rate=0.05,
            depth=4,
            verbose=False
        )
        self.meta_model.fit(stage_predictions, y)
        
        return self
    
    def _get_stage_predictions(self, X, stages):
        """Get predictions from all stage models"""
        predictions = []
        
        for idx, stage in enumerate(stages):
            if stage in self.stage_models:
                pred = self.stage_models[stage].predict_proba(X.iloc[[idx]])[:, 1]
            else:
                # Use average of available models for unknown stages
                preds = []
                for model in self.stage_models.values():
                    preds.append(model.predict_proba(X.iloc[[idx]])[:, 1])
                pred = np.mean(preds) if preds else [0.5]
            predictions.append(pred[0])
        
        return np.array(predictions).reshape(-1, 1)
    
    def predict_proba(self, X):
        """Predict using stage-aware ensemble"""
        X = X.copy()
        X['stage_simplified'] = X['funding_stage'].apply(self.map_funding_stage)
        stage_preds = self._get_stage_predictions(X[ALL_FEATURES], X['stage_simplified'])
        return self.meta_model.predict_proba(stage_preds)


class TemporalHierarchicalModel:
    """Time-horizon based models"""
    
    def __init__(self):
        self.temporal_models = {
            'short_term': None,  # 0-12 months
            'medium_term': None,  # 12-24 months
            'long_term': None    # 24+ months
        }
        self.temporal_weights = {
            'short_term': ['burn_multiple', 'runway_months', 'monthly_burn_usd', 'cash_on_hand_usd'],
            'medium_term': ['revenue_growth_rate_percent', 'user_growth_rate_percent', 'net_dollar_retention_percent'],
            'long_term': ['market_growth_rate_percent', 'tam_size_usd', 'tech_differentiation_score']
        }
        self.meta_model = None
    
    def train(self, X, y):
        """Train temporal models with different feature emphasis"""
        # Short-term model (focus on burn and runway)
        short_features = CAPITAL_FEATURES + PRODUCT_FEATURES[:4]
        self.temporal_models['short_term'] = self._train_temporal_model(
            X[short_features], y, 'short_term'
        )
        
        # Medium-term model (focus on growth metrics)
        medium_features = PRODUCT_FEATURES + MARKET_FEATURES[:8]
        self.temporal_models['medium_term'] = self._train_temporal_model(
            X[medium_features], y, 'medium_term'
        )
        
        # Long-term model (focus on market and differentiation)
        long_features = MARKET_FEATURES + ADVANTAGE_FEATURES + PEOPLE_FEATURES[:5]
        self.temporal_models['long_term'] = self._train_temporal_model(
            X[long_features], y, 'long_term'
        )
        
        # Train meta-model
        temporal_preds = self._get_temporal_predictions(X)
        self.meta_model = cb.CatBoostClassifier(
            iterations=100,
            learning_rate=0.05,
            depth=4,
            verbose=False
        )
        self.meta_model.fit(temporal_preds, y)
        
        return self
    
    def _train_temporal_model(self, X, y, horizon):
        """Train a single temporal model"""
        model = cb.CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            depth=5,
            random_seed=42,
            verbose=False
        )
        
        # Handle categorical features if present
        cat_features = []
        for col in ['sector', 'product_stage', 'investor_tier_primary']:
            if col in X.columns:
                cat_features.append(X.columns.get_loc(col))
        
        model.fit(X, y, cat_features=cat_features)
        logger.info(f"Trained {horizon} model - AUC: {roc_auc_score(y, model.predict_proba(X)[:, 1]):.3f}")
        return model
    
    def _get_temporal_predictions(self, X):
        """Get predictions from all temporal models"""
        short_features = CAPITAL_FEATURES + PRODUCT_FEATURES[:4]
        medium_features = PRODUCT_FEATURES + MARKET_FEATURES[:8]
        long_features = MARKET_FEATURES + ADVANTAGE_FEATURES + PEOPLE_FEATURES[:5]
        
        short_pred = self.temporal_models['short_term'].predict_proba(X[short_features])[:, 1]
        medium_pred = self.temporal_models['medium_term'].predict_proba(X[medium_features])[:, 1]
        long_pred = self.temporal_models['long_term'].predict_proba(X[long_features])[:, 1]
        
        return np.column_stack([short_pred, medium_pred, long_pred])
    
    def predict_proba(self, X):
        """Predict using temporal ensemble"""
        temporal_preds = self._get_temporal_predictions(X)
        return self.meta_model.predict_proba(temporal_preds)


class IndustrySpecificModel:
    """Industry-specific models with custom features"""
    
    def __init__(self):
        self.industry_models = {}
        self.industry_features = {
            'SaaS': ['net_dollar_retention_percent', 'ltv_cac_ratio', 'gross_margin_percent', 'burn_multiple'],
            'FinTech': ['regulatory_advantage_present', 'has_data_moat', 'customer_count', 'brand_strength_score'],
            'HealthTech': ['patent_count', 'regulatory_advantage_present', 'years_experience_avg', 'advisors_count'],
            'E-commerce': ['gross_margin_percent', 'ltv_cac_ratio', 'customer_concentration_percent', 'scalability_score'],
            'DeepTech': ['patent_count', 'tech_differentiation_score', 'years_experience_avg', 'board_advisor_experience_score']
        }
        self.general_model = None
        self.meta_model = None
    
    def train(self, X, y):
        """Train industry-specific models"""
        # Train models for each major industry
        for industry in ['SaaS', 'FinTech', 'HealthTech', 'E-commerce']:
            industry_mask = X['sector'] == industry
            if industry_mask.sum() < 100:
                logger.warning(f"Skipping {industry} - insufficient data")
                continue
            
            # Use industry-specific features + general features
            industry_feats = self.industry_features.get(industry, [])
            all_feats = list(set(ALL_FEATURES) | set(industry_feats))
            
            X_industry = X[industry_mask][all_feats]
            y_industry = y[industry_mask]
            
            model = cb.CatBoostClassifier(
                iterations=200,
                learning_rate=0.05,
                depth=5,
                random_seed=42,
                verbose=False
            )
            
            cat_features = ['sector', 'product_stage', 'investor_tier_primary']
            cat_indices = [X_industry.columns.get_loc(col) for col in cat_features if col in X_industry.columns]
            
            model.fit(X_industry, y_industry, cat_features=cat_indices)
            self.industry_models[industry] = model
            
            logger.info(f"Trained {industry} model - AUC: {roc_auc_score(y_industry, model.predict_proba(X_industry)[:, 1]):.3f}")
        
        # Train general model for other industries
        known_industries = list(self.industry_models.keys())
        other_mask = ~X['sector'].isin(known_industries)
        
        X_other = X[other_mask][ALL_FEATURES]
        y_other = y[other_mask]
        
        self.general_model = cb.CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            depth=5,
            random_seed=42,
            verbose=False
        )
        
        cat_features = ['sector', 'product_stage', 'investor_tier_primary']
        cat_indices = [X_other.columns.get_loc(col) for col in cat_features if col in X_other.columns]
        
        self.general_model.fit(X_other, y_other, cat_features=cat_indices)
        
        # Train meta-model
        industry_preds = self._get_industry_predictions(X)
        self.meta_model = cb.CatBoostClassifier(
            iterations=100,
            learning_rate=0.05,
            depth=4,
            verbose=False
        )
        self.meta_model.fit(industry_preds, y)
        
        return self
    
    def _get_industry_predictions(self, X):
        """Get predictions from industry-specific models"""
        predictions = []
        
        for idx, row in X.iterrows():
            sector = row['sector']
            if sector in self.industry_models:
                # Use industry-specific features
                industry_feats = self.industry_features.get(sector, [])
                all_feats = list(set(ALL_FEATURES) | set(industry_feats))
                pred = self.industry_models[sector].predict_proba(row[all_feats].values.reshape(1, -1))[:, 1]
            else:
                # Use general model
                pred = self.general_model.predict_proba(row[ALL_FEATURES].values.reshape(1, -1))[:, 1]
            predictions.append(pred[0])
        
        return np.array(predictions).reshape(-1, 1)
    
    def predict_proba(self, X):
        """Predict using industry-aware ensemble"""
        industry_preds = self._get_industry_predictions(X)
        return self.meta_model.predict_proba(industry_preds)


class DNAPatternAnalyzer:
    """DNA-style pattern recognition for startups"""
    
    def __init__(self):
        self.pattern_library = {}
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=10)
        self.success_patterns = []
        self.failure_patterns = []
        self.pattern_model = None
        
        # Define startup DNA components
        self.dna_components = {
            'growth_velocity': ['revenue_growth_rate_percent', 'user_growth_rate_percent'],
            'efficiency_genes': ['burn_multiple', 'ltv_cac_ratio', 'gross_margin_percent'],
            'market_dominance': ['customer_concentration_percent', 'net_dollar_retention_percent'],
            'founder_dna': ['years_experience_avg', 'prior_successful_exits_count', 'domain_expertise_years_avg'],
            'product_evolution': ['product_stage', 'product_retention_30d', 'dau_mau_ratio']
        }
    
    def train(self, X, y):
        """Extract and learn DNA patterns"""
        # Extract DNA features
        dna_features = []
        for component, features in self.dna_components.items():
            available_features = [f for f in features if f in X.columns and f != 'product_stage']
            if available_features:
                component_data = X[available_features].fillna(0)
                dna_features.append(component_data)
        
        # Combine DNA features
        dna_matrix = pd.concat(dna_features, axis=1)
        
        # Scale and reduce dimensionality
        dna_scaled = self.scaler.fit_transform(dna_matrix)
        dna_reduced = self.pca.fit_transform(dna_scaled)
        
        # Identify success/failure patterns using clustering
        success_dna = dna_reduced[y == 1]
        failure_dna = dna_reduced[y == 0]
        
        # Cluster successful startups to find patterns
        if len(success_dna) > 10:
            success_clusters = KMeans(n_clusters=min(5, len(success_dna) // 10), random_state=42)
            success_clusters.fit(success_dna)
            self.success_patterns = success_clusters.cluster_centers_
        
        # Cluster failed startups to find anti-patterns
        if len(failure_dna) > 10:
            failure_clusters = KMeans(n_clusters=min(5, len(failure_dna) // 10), random_state=42)
            failure_clusters.fit(failure_dna)
            self.failure_patterns = failure_clusters.cluster_centers_
        
        # Create pattern-based features
        pattern_features = self._extract_pattern_features(dna_reduced)
        
        # Train pattern recognition model
        self.pattern_model = cb.CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            depth=5,
            random_seed=42,
            verbose=False
        )
        self.pattern_model.fit(pattern_features, y)
        
        logger.info(f"Trained DNA pattern model - AUC: {roc_auc_score(y, self.pattern_model.predict_proba(pattern_features)[:, 1]):.3f}")
        
        return self
    
    def _extract_pattern_features(self, dna_data):
        """Extract features based on similarity to known patterns"""
        features = []
        
        for dna in dna_data:
            feat = []
            
            # Distance to nearest success pattern
            if len(self.success_patterns) > 0:
                success_distances = [np.linalg.norm(dna - pattern) for pattern in self.success_patterns]
                feat.extend([
                    np.min(success_distances),
                    np.mean(success_distances),
                    np.argmin(success_distances)  # Nearest success pattern ID
                ])
            else:
                feat.extend([0, 0, 0])
            
            # Distance to nearest failure pattern
            if len(self.failure_patterns) > 0:
                failure_distances = [np.linalg.norm(dna - pattern) for pattern in self.failure_patterns]
                feat.extend([
                    np.min(failure_distances),
                    np.mean(failure_distances),
                    np.argmin(failure_distances)  # Nearest failure pattern ID
                ])
            else:
                feat.extend([0, 0, 0])
            
            features.append(feat)
        
        return np.array(features)
    
    def predict_proba(self, X):
        """Predict using DNA pattern matching"""
        # Extract DNA features
        dna_features = []
        for component, features in self.dna_components.items():
            available_features = [f for f in features if f in X.columns and f != 'product_stage']
            if available_features:
                component_data = X[available_features].fillna(0)
                dna_features.append(component_data)
        
        dna_matrix = pd.concat(dna_features, axis=1)
        dna_scaled = self.scaler.transform(dna_matrix)
        dna_reduced = self.pca.transform(dna_scaled)
        
        # Extract pattern features
        pattern_features = self._extract_pattern_features(dna_reduced)
        
        return self.pattern_model.predict_proba(pattern_features)


class HierarchicalEnsemble:
    """Master ensemble combining all hierarchical approaches"""
    
    def __init__(self):
        self.stage_model = StageBasedHierarchicalModel()
        self.temporal_model = TemporalHierarchicalModel()
        self.industry_model = IndustrySpecificModel()
        self.dna_model = DNAPatternAnalyzer()
        self.meta_ensemble = None
        
    def train(self, X, y):
        """Train all hierarchical models and meta-ensemble"""
        logger.info("Training Stage-Based Hierarchical Model...")
        self.stage_model.train(X.copy(), y)
        
        logger.info("Training Temporal Hierarchical Model...")
        self.temporal_model.train(X.copy(), y)
        
        logger.info("Training Industry-Specific Model...")
        self.industry_model.train(X.copy(), y)
        
        logger.info("Training DNA Pattern Analyzer...")
        self.dna_model.train(X.copy(), y)
        
        # Get predictions from all models
        logger.info("Creating meta-ensemble...")
        ensemble_features = self._get_ensemble_predictions(X)
        
        # Train final meta-ensemble
        self.meta_ensemble = cb.CatBoostClassifier(
            iterations=150,
            learning_rate=0.05,
            depth=4,
            random_seed=42,
            verbose=False
        )
        self.meta_ensemble.fit(ensemble_features, y)
        
        # Evaluate final ensemble
        final_pred = self.meta_ensemble.predict_proba(ensemble_features)[:, 1]
        logger.info(f"Final Hierarchical Ensemble - AUC: {roc_auc_score(y, final_pred):.3f}")
        
        return self
    
    def _get_ensemble_predictions(self, X):
        """Get predictions from all hierarchical models"""
        stage_pred = self.stage_model.predict_proba(X.copy())[:, 1]
        temporal_pred = self.temporal_model.predict_proba(X.copy())[:, 1]
        industry_pred = self.industry_model.predict_proba(X.copy())[:, 1]
        dna_pred = self.dna_model.predict_proba(X.copy())[:, 1]
        
        return np.column_stack([stage_pred, temporal_pred, industry_pred, dna_pred])
    
    def predict_proba(self, X):
        """Predict using full hierarchical ensemble"""
        ensemble_preds = self._get_ensemble_predictions(X)
        return self.meta_ensemble.predict_proba(ensemble_preds)
    
    def save_models(self, output_dir):
        """Save all trained models"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save individual models
        joblib.dump(self.stage_model, output_path / 'stage_hierarchical_model.pkl')
        joblib.dump(self.temporal_model, output_path / 'temporal_hierarchical_model.pkl')
        joblib.dump(self.industry_model, output_path / 'industry_specific_model.pkl')
        joblib.dump(self.dna_model, output_path / 'dna_pattern_model.pkl')
        joblib.dump(self.meta_ensemble, output_path / 'hierarchical_meta_ensemble.pkl')
        
        # Save metadata
        metadata = {
            'version': '1.0-hierarchical-45features',
            'created_at': datetime.now().isoformat(),
            'models': {
                'stage_based': list(self.stage_model.stage_models.keys()),
                'temporal': list(self.temporal_model.temporal_models.keys()),
                'industry': list(self.industry_model.industry_models.keys()),
                'dna_patterns': {
                    'success_patterns': len(self.dna_model.success_patterns),
                    'failure_patterns': len(self.dna_model.failure_patterns)
                }
            },
            'features_used': 45,
            'approach': 'Hierarchical Ensemble with Stage, Temporal, Industry, and DNA models'
        }
        
        with open(output_path / 'hierarchical_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved hierarchical models to {output_path}")


def main():
    """Train and save hierarchical models for 45-feature dataset"""
    # Load dataset
    logger.info("Loading 45-feature dataset...")
    df = pd.read_csv('data/final_100k_dataset_45features.csv')
    
    # Prepare features and labels
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    y = df['success'].astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"Training set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    
    # Train hierarchical ensemble
    ensemble = HierarchicalEnsemble()
    ensemble.train(X_train, y_train)
    
    # Evaluate on test set
    test_pred = ensemble.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, test_pred)
    test_acc = accuracy_score(y_test, (test_pred > 0.5).astype(int))
    test_precision = precision_score(y_test, (test_pred > 0.5).astype(int))
    test_recall = recall_score(y_test, (test_pred > 0.5).astype(int))
    
    logger.info(f"\nTest Set Performance:")
    logger.info(f"AUC: {test_auc:.3f}")
    logger.info(f"Accuracy: {test_acc:.3f}")
    logger.info(f"Precision: {test_precision:.3f}")
    logger.info(f"Recall: {test_recall:.3f}")
    
    # Save models
    ensemble.save_models('models/hierarchical_45features')
    
    # Save test results
    results = {
        'test_auc': test_auc,
        'test_accuracy': test_acc,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'model_type': 'Hierarchical Ensemble',
        'features_used': 45,
        'training_samples': len(X_train),
        'test_samples': len(X_test)
    }
    
    with open('models/hierarchical_45features/test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info("\nHierarchical model training complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train hierarchical models for FLASH')
    args = parser.parse_args()
    
    main()