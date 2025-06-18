# Immediate Technical Implementation Guide
## Making Advanced Models Work in FLASH

This guide provides step-by-step instructions to fix the current advanced model loading issues and implement a robust model architecture.

---

## Step 1: Create Model Architecture Module

### 1.1 Create the ML Core Package

```bash
mkdir -p ml_core/{models,utils,interfaces}
touch ml_core/__init__.py
touch ml_core/models/__init__.py
touch ml_core/utils/__init__.py
touch ml_core/interfaces/__init__.py
```

### 1.2 Define Model Interfaces

Create `ml_core/interfaces/base_models.py`:

```python
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, Union
import joblib
import json
from pathlib import Path

class BaseMLModel(ABC):
    """Base class for all FLASH ML models"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.model_version = "1.0.0"
        self.model_type = self.__class__.__name__
        self.metadata = {
            "created_at": None,
            "trained_on_samples": 0,
            "feature_names": [],
            "performance_metrics": {}
        }
    
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'BaseMLModel':
        """Train the model"""
        pass
    
    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict probabilities"""
        pass
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Binary predictions"""
        probs = self.predict_proba(X)
        return (probs[:, 1] >= self.config.get('threshold', 0.5)).astype(int)
    
    def save(self, path: Union[str, Path]) -> None:
        """Save model with metadata"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save model components
        model_data = {
            'model_type': self.model_type,
            'model_version': self.model_version,
            'config': self.config,
            'metadata': self.metadata,
            'components': self._get_serializable_components()
        }
        
        # Save main file
        joblib.dump(model_data, path / 'model.pkl')
        
        # Save metadata separately
        with open(path / 'metadata.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    @classmethod
    def load(cls, path: Union[str, Path]) -> 'BaseMLModel':
        """Load model from disk"""
        path = Path(path)
        
        # Load model data
        model_data = joblib.dump(path / 'model.pkl')
        
        # Create instance
        instance = cls(config=model_data['config'])
        instance.metadata = model_data['metadata']
        instance._load_components(model_data['components'])
        
        return instance
    
    @abstractmethod
    def _get_serializable_components(self) -> Dict[str, Any]:
        """Get components that can be serialized"""
        pass
    
    @abstractmethod
    def _load_components(self, components: Dict[str, Any]) -> None:
        """Load components from serialized data"""
        pass
```

### 1.3 Implement DNA Pattern Analyzer

Create `ml_core/models/dna_analyzer.py`:

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb
from catboost import CatBoostClassifier
from typing import Dict, Any, Optional
import logging

from ..interfaces.base_models import BaseMLModel

logger = logging.getLogger(__name__)

class DNAPatternAnalyzer(BaseMLModel):
    """Advanced DNA Pattern Analysis for Startups"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        
        # Default configuration
        self.config.update({
            'n_patterns': self.config.get('n_patterns', 8),
            'n_components': self.config.get('n_components', 20),
            'use_deep_features': self.config.get('use_deep_features', True),
            'ensemble_models': self.config.get('ensemble_models', True)
        })
        
        # Initialize components
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.config['n_components'], random_state=42)
        self.pattern_clusterer = KMeans(
            n_clusters=self.config['n_patterns'],
            random_state=42,
            n_init=10
        )
        
        # Pattern classifiers
        self.pattern_models = {
            'gradient_boost': GradientBoostingClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            ),
            'catboost': CatBoostClassifier(
                iterations=200,
                depth=6,
                learning_rate=0.1,
                random_seed=42,
                verbose=False
            )
        }
        
        # Success pattern memory
        self.success_patterns = {}
        self.failure_patterns = {}
        self.pattern_weights = None
        
    def fit(self, X: pd.DataFrame, y: np.ndarray) -> 'DNAPatternAnalyzer':
        """Train DNA pattern analyzer"""
        logger.info(f"Training DNA Pattern Analyzer on {len(X)} samples")
        
        # Store feature names
        self.metadata['feature_names'] = X.columns.tolist()
        self.metadata['trained_on_samples'] = len(X)
        
        # Convert to numpy if needed
        X_np = X.values if isinstance(X, pd.DataFrame) else X
        
        # Step 1: Standardize features
        X_scaled = self.scaler.fit_transform(X_np)
        
        # Step 2: Dimensionality reduction
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Step 3: Discover patterns through clustering
        clusters = self.pattern_clusterer.fit_predict(X_pca)
        
        # Step 4: Analyze success/failure patterns
        self._analyze_patterns(X_scaled, clusters, y)
        
        # Step 5: Create DNA features
        dna_features = self._create_dna_features(X_scaled, X_pca, clusters)
        
        # Step 6: Train pattern classifiers
        for name, model in self.pattern_models.items():
            logger.info(f"Training {name} pattern classifier")
            model.fit(dna_features, y)
        
        # Step 7: Calculate pattern weights based on performance
        self._calculate_pattern_weights(dna_features, y)
        
        logger.info("DNA Pattern Analyzer training complete")
        return self
    
    def _analyze_patterns(self, X: np.ndarray, clusters: np.ndarray, y: np.ndarray):
        """Analyze success and failure patterns"""
        for cluster_id in range(self.config['n_patterns']):
            cluster_mask = clusters == cluster_id
            cluster_success_rate = y[cluster_mask].mean()
            
            if cluster_success_rate > 0.6:
                self.success_patterns[cluster_id] = {
                    'success_rate': cluster_success_rate,
                    'feature_means': X[cluster_mask & (y == 1)].mean(axis=0),
                    'feature_stds': X[cluster_mask & (y == 1)].std(axis=0)
                }
            elif cluster_success_rate < 0.4:
                self.failure_patterns[cluster_id] = {
                    'failure_rate': 1 - cluster_success_rate,
                    'feature_means': X[cluster_mask & (y == 0)].mean(axis=0),
                    'feature_stds': X[cluster_mask & (y == 0)].std(axis=0)
                }
    
    def _create_dna_features(self, X: np.ndarray, X_pca: np.ndarray, 
                            clusters: np.ndarray) -> np.ndarray:
        """Create comprehensive DNA features"""
        n_samples = X.shape[0]
        
        # Base features
        features = [X_pca, clusters.reshape(-1, 1)]
        
        # Pattern similarity scores
        success_similarities = np.zeros((n_samples, len(self.success_patterns)))
        failure_similarities = np.zeros((n_samples, len(self.failure_patterns)))
        
        for i, (pattern_id, pattern_data) in enumerate(self.success_patterns.items()):
            similarity = self._calculate_pattern_similarity(X, pattern_data)
            success_similarities[:, i] = similarity
        
        for i, (pattern_id, pattern_data) in enumerate(self.failure_patterns.items()):
            similarity = self._calculate_pattern_similarity(X, pattern_data)
            failure_similarities[:, i] = similarity
        
        features.extend([success_similarities, failure_similarities])
        
        if self.config['use_deep_features']:
            # Financial DNA
            financial_dna = self._extract_financial_dna(X)
            features.append(financial_dna)
            
            # Growth DNA
            growth_dna = self._extract_growth_dna(X)
            features.append(growth_dna)
            
            # Team DNA
            team_dna = self._extract_team_dna(X)
            features.append(team_dna)
            
            # Market DNA
            market_dna = self._extract_market_dna(X)
            features.append(market_dna)
        
        return np.hstack(features)
    
    def _calculate_pattern_similarity(self, X: np.ndarray, 
                                    pattern: Dict[str, np.ndarray]) -> np.ndarray:
        """Calculate similarity to a specific pattern"""
        # Mahalanobis-like distance
        diff = X - pattern['feature_means']
        normalized_diff = diff / (pattern['feature_stds'] + 1e-6)
        distance = np.sqrt(np.sum(normalized_diff ** 2, axis=1))
        
        # Convert to similarity (0-1)
        similarity = np.exp(-distance / 10)
        return similarity
    
    def _extract_financial_dna(self, X: np.ndarray) -> np.ndarray:
        """Extract financial health DNA"""
        # Assuming first 12 features are financial
        financial_features = X[:, :12]
        
        dna = np.zeros((X.shape[0], 5))
        dna[:, 0] = np.mean(financial_features, axis=1)  # Overall health
        dna[:, 1] = np.std(financial_features, axis=1)   # Volatility
        dna[:, 2] = np.max(financial_features, axis=1) - np.min(financial_features, axis=1)  # Range
        dna[:, 3] = np.percentile(financial_features, 75, axis=1)  # Upper quartile
        dna[:, 4] = self._calculate_trend(financial_features)  # Trend
        
        return dna
    
    def _extract_growth_dna(self, X: np.ndarray) -> np.ndarray:
        """Extract growth pattern DNA"""
        # Assuming features 12-24 are growth-related
        growth_features = X[:, 12:24] if X.shape[1] > 24 else X[:, :12]
        
        dna = np.zeros((X.shape[0], 4))
        dna[:, 0] = np.mean(growth_features, axis=1)  # Average growth
        dna[:, 1] = np.max(growth_features, axis=1)   # Peak growth
        dna[:, 2] = self._calculate_acceleration(growth_features)  # Acceleration
        dna[:, 3] = self._calculate_consistency(growth_features)   # Consistency
        
        return dna
    
    def _extract_team_dna(self, X: np.ndarray) -> np.ndarray:
        """Extract team strength DNA"""
        # Assuming features 24-35 are team-related
        start_idx = min(24, X.shape[1] - 11)
        team_features = X[:, start_idx:start_idx+11]
        
        dna = np.zeros((X.shape[0], 4))
        dna[:, 0] = np.mean(team_features, axis=1)  # Overall strength
        dna[:, 1] = np.max(team_features, axis=1)   # Star quality
        dna[:, 2] = np.std(team_features, axis=1)   # Diversity
        dna[:, 3] = np.sum(team_features > np.median(team_features), axis=1)  # Breadth
        
        return dna
    
    def _extract_market_dna(self, X: np.ndarray) -> np.ndarray:
        """Extract market position DNA"""
        # Assuming last 10 features are market-related
        market_features = X[:, -10:]
        
        dna = np.zeros((X.shape[0], 4))
        dna[:, 0] = np.mean(market_features, axis=1)  # Market strength
        dna[:, 1] = np.percentile(market_features, 90, axis=1)  # Top performance
        dna[:, 2] = self._calculate_market_fit(market_features)  # Market fit
        dna[:, 3] = self._calculate_competitive_advantage(market_features)  # Advantage
        
        return dna
    
    def _calculate_trend(self, features: np.ndarray) -> np.ndarray:
        """Calculate trend coefficient"""
        # Simple linear trend
        x = np.arange(features.shape[1])
        trends = np.zeros(features.shape[0])
        
        for i in range(features.shape[0]):
            coef = np.polyfit(x, features[i], 1)[0]
            trends[i] = coef
        
        return trends
    
    def _calculate_acceleration(self, features: np.ndarray) -> np.ndarray:
        """Calculate growth acceleration"""
        # Second derivative approximation
        if features.shape[1] < 3:
            return np.zeros(features.shape[0])
        
        diff1 = np.diff(features, axis=1)
        diff2 = np.diff(diff1, axis=1)
        return np.mean(diff2, axis=1)
    
    def _calculate_consistency(self, features: np.ndarray) -> np.ndarray:
        """Calculate growth consistency"""
        # Inverse of coefficient of variation
        means = np.mean(features, axis=1)
        stds = np.std(features, axis=1)
        return means / (stds + 1e-6)
    
    def _calculate_market_fit(self, features: np.ndarray) -> np.ndarray:
        """Calculate product-market fit score"""
        # Combination of retention and growth metrics
        return np.mean(features[:, :5], axis=1) * np.mean(features[:, 5:], axis=1)
    
    def _calculate_competitive_advantage(self, features: np.ndarray) -> np.ndarray:
        """Calculate competitive advantage score"""
        # How much better than median
        medians = np.median(features, axis=0)
        advantages = features - medians
        return np.mean(advantages, axis=1)
    
    def _calculate_pattern_weights(self, X: np.ndarray, y: np.ndarray):
        """Calculate optimal weights for pattern models"""
        # Cross-validation to find best weights
        from sklearn.model_selection import cross_val_predict
        
        predictions = {}
        for name, model in self.pattern_models.items():
            pred_proba = cross_val_predict(
                model, X, y, cv=5, method='predict_proba'
            )[:, 1]
            predictions[name] = pred_proba
        
        # Find optimal weights using simple grid search
        best_score = 0
        best_weights = None
        
        for w1 in np.arange(0, 1.1, 0.1):
            for w2 in np.arange(0, 1.1 - w1, 0.1):
                w3 = 1 - w1 - w2
                
                ensemble_pred = (
                    w1 * predictions['gradient_boost'] +
                    w2 * predictions['xgboost'] +
                    w3 * predictions['catboost']
                )
                
                # Calculate AUC
                from sklearn.metrics import roc_auc_score
                score = roc_auc_score(y, ensemble_pred)
                
                if score > best_score:
                    best_score = score
                    best_weights = {'gradient_boost': w1, 'xgboost': w2, 'catboost': w3}
        
        self.pattern_weights = best_weights
        self.metadata['performance_metrics']['auc'] = best_score
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict success probability using DNA patterns"""
        # Convert to numpy
        X_np = X.values if isinstance(X, pd.DataFrame) else X
        
        # Transform features
        X_scaled = self.scaler.transform(X_np)
        X_pca = self.pca.transform(X_scaled)
        clusters = self.pattern_clusterer.predict(X_pca)
        
        # Create DNA features
        dna_features = self._create_dna_features(X_scaled, X_pca, clusters)
        
        # Get predictions from each model
        predictions = []
        weights = []
        
        for name, model in self.pattern_models.items():
            pred = model.predict_proba(dna_features)
            predictions.append(pred)
            weights.append(self.pattern_weights.get(name, 1/3))
        
        # Weighted ensemble
        ensemble_pred = np.zeros_like(predictions[0])
        for pred, weight in zip(predictions, weights):
            ensemble_pred += weight * pred
        
        return ensemble_pred
    
    def get_dna_signature(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Get detailed DNA signature for a startup"""
        X_np = X.values if isinstance(X, pd.DataFrame) else X
        
        # Get base transformations
        X_scaled = self.scaler.transform(X_np)
        X_pca = self.pca.transform(X_scaled)
        cluster = self.pattern_clusterer.predict(X_pca)[0]
        
        # Extract all DNA components
        financial_dna = self._extract_financial_dna(X_scaled)
        growth_dna = self._extract_growth_dna(X_scaled)
        team_dna = self._extract_team_dna(X_scaled)
        market_dna = self._extract_market_dna(X_scaled)
        
        # Pattern similarities
        success_sims = {}
        for pattern_id, pattern_data in self.success_patterns.items():
            sim = self._calculate_pattern_similarity(X_scaled, pattern_data)
            success_sims[f"pattern_{pattern_id}"] = float(sim[0])
        
        return {
            'primary_pattern': int(cluster),
            'financial_dna': financial_dna[0].tolist(),
            'growth_dna': growth_dna[0].tolist(),
            'team_dna': team_dna[0].tolist(),
            'market_dna': market_dna[0].tolist(),
            'success_pattern_match': success_sims,
            'dna_summary': self._generate_dna_summary(
                cluster, financial_dna[0], growth_dna[0], 
                team_dna[0], market_dna[0]
            )
        }
    
    def _generate_dna_summary(self, cluster: int, financial: np.ndarray,
                             growth: np.ndarray, team: np.ndarray, 
                             market: np.ndarray) -> str:
        """Generate human-readable DNA summary"""
        pattern_names = [
            "Hypergrowth Unicorn", "Steady SaaS", "Deep Tech Pioneer",
            "Market Disruptor", "Efficient Operator", "Network Effect Master",
            "Platform Builder", "Category Creator"
        ]
        
        pattern_name = pattern_names[cluster % len(pattern_names)]
        
        # Analyze strengths
        strengths = []
        if financial[0] > 0.7:
            strengths.append("strong financials")
        if growth[1] > 0.8:
            strengths.append("explosive growth")
        if team[1] > 0.75:
            strengths.append("star team")
        if market[3] > 0.7:
            strengths.append("competitive moat")
        
        summary = f"{pattern_name} pattern with {', '.join(strengths)}"
        return summary
    
    def _get_serializable_components(self) -> Dict[str, Any]:
        """Get components for serialization"""
        return {
            'scaler': self.scaler,
            'pca': self.pca,
            'pattern_clusterer': self.pattern_clusterer,
            'pattern_models': self.pattern_models,
            'success_patterns': self.success_patterns,
            'failure_patterns': self.failure_patterns,
            'pattern_weights': self.pattern_weights
        }
    
    def _load_components(self, components: Dict[str, Any]) -> None:
        """Load components from serialized data"""
        self.scaler = components['scaler']
        self.pca = components['pca']
        self.pattern_clusterer = components['pattern_clusterer']
        self.pattern_models = components['pattern_models']
        self.success_patterns = components['success_patterns']
        self.failure_patterns = components['failure_patterns']
        self.pattern_weights = components['pattern_weights']
```

---

## Step 2: Create Model Training Pipeline

### 2.1 Unified Training Script

Create `train_advanced_models.py`:

```python
#!/usr/bin/env python3
"""
Unified training script for all advanced models
Ensures consistency and proper serialization
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import time
from sklearn.model_selection import train_test_split
import json

# Import our model classes
from ml_core.models.dna_analyzer import DNAPatternAnalyzer
from ml_core.models.temporal_predictor import TemporalPredictor
from ml_core.models.industry_models import IndustrySpecificModel
from ml_core.models.hierarchical_ensemble import HierarchicalEnsemble

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_training_data():
    """Load and prepare training data"""
    logger.info("Loading training data...")
    
    # Load the 100k dataset
    data_path = Path("data/final_100k_dataset_45features.csv")
    df = pd.read_csv(data_path)
    
    # Prepare features and target
    target_col = 'success_outcome'
    feature_cols = [col for col in df.columns if col != target_col]
    
    X = df[feature_cols]
    y = df[target_col].values
    
    logger.info(f"Loaded {len(df)} samples with {len(feature_cols)} features")
    
    return X, y, feature_cols

def train_dna_analyzer(X_train, y_train, X_val, y_val):
    """Train DNA Pattern Analyzer"""
    logger.info("\n=== Training DNA Pattern Analyzer ===")
    
    config = {
        'n_patterns': 8,
        'n_components': 20,
        'use_deep_features': True,
        'ensemble_models': True
    }
    
    model = DNAPatternAnalyzer(config=config)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Evaluate
    from sklearn.metrics import roc_auc_score
    y_pred = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    
    logger.info(f"DNA Analyzer - AUC: {auc:.4f}, Training time: {training_time:.2f}s")
    
    # Save model
    model.save("models/advanced/dna_analyzer")
    
    return model, auc

def train_temporal_model(X_train, y_train, X_val, y_val):
    """Train Temporal Prediction Model"""
    logger.info("\n=== Training Temporal Prediction Model ===")
    
    config = {
        'use_lstm': True,
        'sequence_length': 12,
        'forecast_horizons': [3, 6, 12, 24]
    }
    
    model = TemporalPredictor(config=config)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Evaluate
    from sklearn.metrics import roc_auc_score
    y_pred = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    
    logger.info(f"Temporal Model - AUC: {auc:.4f}, Training time: {training_time:.2f}s")
    
    # Save model
    model.save("models/advanced/temporal_predictor")
    
    return model, auc

def train_industry_models(X_train, y_train, X_val, y_val):
    """Train Industry-Specific Models"""
    logger.info("\n=== Training Industry-Specific Models ===")
    
    config = {
        'industries': ['saas', 'fintech', 'healthtech', 'ecommerce', 'other'],
        'use_industry_features': True
    }
    
    model = IndustrySpecificModel(config=config)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Evaluate
    from sklearn.metrics import roc_auc_score
    y_pred = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    
    logger.info(f"Industry Models - AUC: {auc:.4f}, Training time: {training_time:.2f}s")
    
    # Save model
    model.save("models/advanced/industry_specific")
    
    return model, auc

def train_hierarchical_ensemble(X_train, y_train, X_val, y_val, 
                               base_models=None):
    """Train Hierarchical Ensemble"""
    logger.info("\n=== Training Hierarchical Ensemble ===")
    
    config = {
        'use_stacking': True,
        'meta_learner': 'neural_network',
        'calibrate_probabilities': True
    }
    
    model = HierarchicalEnsemble(config=config, base_models=base_models)
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # Evaluate
    from sklearn.metrics import roc_auc_score
    y_pred = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_pred)
    
    logger.info(f"Hierarchical Ensemble - AUC: {auc:.4f}, Training time: {training_time:.2f}s")
    
    # Save model
    model.save("models/advanced/hierarchical_ensemble")
    
    return model, auc

def main():
    """Main training pipeline"""
    logger.info("Starting advanced model training pipeline")
    
    # Load data
    X, y, feature_names = load_training_data()
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info(f"Train set: {len(X_train)}, Validation set: {len(X_val)}")
    
    # Train all models
    results = {}
    models = {}
    
    # DNA Analyzer
    dna_model, dna_auc = train_dna_analyzer(X_train, y_train, X_val, y_val)
    models['dna'] = dna_model
    results['dna_analyzer'] = {'auc': dna_auc}
    
    # Temporal Model
    temporal_model, temporal_auc = train_temporal_model(X_train, y_train, X_val, y_val)
    models['temporal'] = temporal_model
    results['temporal_predictor'] = {'auc': temporal_auc}
    
    # Industry Models
    industry_model, industry_auc = train_industry_models(X_train, y_train, X_val, y_val)
    models['industry'] = industry_model
    results['industry_specific'] = {'auc': industry_auc}
    
    # Hierarchical Ensemble (using other models)
    ensemble_model, ensemble_auc = train_hierarchical_ensemble(
        X_train, y_train, X_val, y_val, base_models=models
    )
    results['hierarchical_ensemble'] = {'auc': ensemble_auc}
    
    # Save results summary
    results_summary = {
        'training_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'dataset_size': len(X),
        'feature_count': len(feature_names),
        'models': results,
        'average_auc': np.mean([r['auc'] for r in results.values()])
    }
    
    with open('models/advanced/training_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    logger.info("\n=== Training Complete ===")
    logger.info(f"Average AUC: {results_summary['average_auc']:.4f}")
    for model_name, result in results.items():
        logger.info(f"{model_name}: {result['auc']:.4f}")

if __name__ == "__main__":
    main()
```

---

## Step 3: Update API Server

### 3.1 Create Advanced Model Loader

Create `ml_core/serving/model_loader.py`:

```python
"""
Robust model loading system with proper error handling
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import joblib

# Import all model classes
from ..models.dna_analyzer import DNAPatternAnalyzer
from ..models.temporal_predictor import TemporalPredictor
from ..models.industry_models import IndustrySpecificModel
from ..models.hierarchical_ensemble import HierarchicalEnsemble

logger = logging.getLogger(__name__)

class ModelLoader:
    """Handles loading of all model types"""
    
    # Model registry
    MODEL_CLASSES = {
        'DNAPatternAnalyzer': DNAPatternAnalyzer,
        'TemporalPredictor': TemporalPredictor,
        'IndustrySpecificModel': IndustrySpecificModel,
        'HierarchicalEnsemble': HierarchicalEnsemble
    }
    
    @classmethod
    def load_model(cls, model_path: Path) -> Optional[Any]:
        """Load a model with proper error handling"""
        try:
            if not model_path.exists():
                logger.error(f"Model path does not exist: {model_path}")
                return None
            
            # Try new format first
            if (model_path / 'model.pkl').exists():
                return cls._load_new_format(model_path)
            
            # Try legacy format
            pkl_files = list(model_path.glob('*.pkl'))
            if pkl_files:
                return cls._load_legacy_format(pkl_files[0])
            
            logger.error(f"No model files found in {model_path}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
            return None
    
    @classmethod
    def _load_new_format(cls, model_path: Path) -> Optional[Any]:
        """Load model in new standardized format"""
        try:
            model_data = joblib.load(model_path / 'model.pkl')
            model_type = model_data.get('model_type')
            
            if model_type not in cls.MODEL_CLASSES:
                logger.error(f"Unknown model type: {model_type}")
                return None
            
            model_class = cls.MODEL_CLASSES[model_type]
            return model_class.load(model_path)
            
        except Exception as e:
            logger.error(f"Error loading new format model: {e}")
            return None
    
    @classmethod
    def _load_legacy_format(cls, pkl_path: Path) -> Optional[Any]:
        """Load legacy format models with class injection"""
        try:
            # Inject model classes into global namespace for unpickling
            import sys
            module = sys.modules[__name__]
            
            for class_name, class_obj in cls.MODEL_CLASSES.items():
                setattr(module, class_name, class_obj)
            
            # Also try common variations
            setattr(module, 'OptimizedDNAPatternAnalyzer', DNAPatternAnalyzer)
            setattr(module, 'OptimizedTemporalModel', TemporalPredictor)
            setattr(module, 'OptimizedIndustryModel', IndustrySpecificModel)
            
            # Load model
            model = joblib.load(pkl_path)
            logger.info(f"Successfully loaded legacy model: {type(model).__name__}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading legacy model: {e}")
            return None

class AdvancedModelOrchestrator:
    """Orchestrates all advanced models for unified predictions"""
    
    def __init__(self):
        self.models = {}
        self.model_paths = {
            'dna_analyzer': Path('models/advanced/dna_analyzer'),
            'temporal_predictor': Path('models/advanced/temporal_predictor'),
            'industry_specific': Path('models/advanced/industry_specific'),
            'hierarchical_ensemble': Path('models/advanced/hierarchical_ensemble')
        }
        
    def load_all_models(self) -> Dict[str, bool]:
        """Load all advanced models"""
        results = {}
        
        for model_name, model_path in self.model_paths.items():
            logger.info(f"Loading {model_name}...")
            
            # Try multiple paths
            paths_to_try = [
                model_path,
                Path(f'models/{model_name}'),
                Path(f'models/{model_name}.pkl'),
                Path(f'models/hierarchical_45features/{model_name}.pkl')
            ]
            
            loaded = False
            for path in paths_to_try:
                model = ModelLoader.load_model(path)
                if model is not None:
                    self.models[model_name] = model
                    loaded = True
                    logger.info(f"✅ Loaded {model_name} from {path}")
                    break
            
            results[model_name] = loaded
            if not loaded:
                logger.warning(f"❌ Failed to load {model_name}")
        
        return results
    
    def predict(self, X) -> Dict[str, Any]:
        """Get predictions from all available models"""
        predictions = {}
        
        # DNA Analyzer
        if 'dna_analyzer' in self.models:
            try:
                dna_pred = self.models['dna_analyzer'].predict_proba(X)[:, 1]
                dna_signature = self.models['dna_analyzer'].get_dna_signature(X)
                predictions['dna'] = {
                    'probability': float(dna_pred[0]),
                    'signature': dna_signature
                }
            except Exception as e:
                logger.error(f"DNA prediction error: {e}")
        
        # Temporal Predictor
        if 'temporal_predictor' in self.models:
            try:
                temporal_pred = self.models['temporal_predictor'].predict_proba(X)[:, 1]
                temporal_analysis = self.models['temporal_predictor'].get_temporal_analysis(X)
                predictions['temporal'] = {
                    'probability': float(temporal_pred[0]),
                    'analysis': temporal_analysis
                }
            except Exception as e:
                logger.error(f"Temporal prediction error: {e}")
        
        # Industry Specific
        if 'industry_specific' in self.models:
            try:
                industry_pred = self.models['industry_specific'].predict_proba(X)[:, 1]
                industry_insights = self.models['industry_specific'].get_industry_insights(X)
                predictions['industry'] = {
                    'probability': float(industry_pred[0]),
                    'insights': industry_insights
                }
            except Exception as e:
                logger.error(f"Industry prediction error: {e}")
        
        # Hierarchical Ensemble
        if 'hierarchical_ensemble' in self.models:
            try:
                ensemble_pred = self.models['hierarchical_ensemble'].predict_proba(X)[:, 1]
                predictions['ensemble'] = {
                    'probability': float(ensemble_pred[0])
                }
            except Exception as e:
                logger.error(f"Ensemble prediction error: {e}")
        
        # Calculate weighted average if multiple models available
        if predictions:
            probs = [p['probability'] for p in predictions.values()]
            predictions['combined_probability'] = np.mean(probs)
            predictions['model_agreement'] = 1 - np.std(probs)
        
        return predictions
```

### 3.2 Update API Server

Update the `api_server.py` to use the new model loader:

```python
# Add at the top of api_server.py
from ml_core.serving.model_loader import AdvancedModelOrchestrator

# Replace the model loading section with:
# Initialize advanced model orchestrator
ADVANCED_ORCHESTRATOR = AdvancedModelOrchestrator()

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    logger.info("Initializing advanced models...")
    
    # Load all advanced models
    results = ADVANCED_ORCHESTRATOR.load_all_models()
    
    loaded_count = sum(results.values())
    total_count = len(results)
    
    logger.info(f"Loaded {loaded_count}/{total_count} advanced models")
    
    if loaded_count == 0:
        logger.warning("No advanced models loaded, falling back to base models")
    
    # Continue with existing model loading...
    load_models()

# Update prediction endpoint to use advanced models
@app.post("/predict_advanced")
async def predict_advanced(metrics: StartupMetrics):
    """Advanced prediction using all available models"""
    try:
        # Convert to DataFrame
        data = pd.DataFrame([metrics.dict()])
        
        # Get advanced predictions
        advanced_results = ADVANCED_ORCHESTRATOR.predict(data)
        
        # Combine with base predictions
        base_prediction = await predict(metrics)
        
        # Merge results
        response = {
            **base_prediction.dict(),
            'advanced_analysis': advanced_results,
            'model_version': '2.0-advanced'
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Advanced prediction error: {e}")
        # Fall back to base prediction
        return await predict(metrics)
```

---

## Step 4: Data Collection Strategy

### 4.1 Create Data Collection Framework

Create `data_collection/collectors/crunchbase_collector.py`:

```python
"""
Crunchbase data collector for real startup data
"""
import requests
import pandas as pd
from typing import List, Dict, Any
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CrunchbaseCollector:
    """Collects startup data from Crunchbase API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.crunchbase.com/v4"
        self.headers = {"X-cb-user-key": api_key}
        
    def collect_startups(self, min_funding: float = 1e6, 
                        limit: int = 1000) -> pd.DataFrame:
        """Collect startup data with outcomes"""
        
        startups = []
        
        # Search for funded companies
        search_url = f"{self.base_url}/searches/organizations"
        
        params = {
            "field_ids": [
                "identifier", "name", "founded_on", "closed_on",
                "num_funding_rounds", "total_funding_usd",
                "num_employees_enum", "revenue_range",
                "categories", "location", "short_description"
            ],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "total_funding_usd",
                    "operator_id": "gte",
                    "values": [min_funding]
                }
            ],
            "limit": min(limit, 1000)
        }
        
        try:
            response = requests.post(
                search_url, 
                json=params, 
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            entities = data.get('entities', [])
            
            for entity in entities:
                startup_data = self._extract_startup_features(entity)
                if startup_data:
                    startups.append(startup_data)
                    
                # Rate limiting
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Crunchbase API error: {e}")
        
        return pd.DataFrame(startups)
    
    def _extract_startup_features(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from Crunchbase entity"""
        properties = entity.get('properties', {})
        
        # Determine outcome
        closed_on = properties.get('closed_on')
        ipo_status = properties.get('ipo_status')
        acquired = properties.get('num_acquisitions', 0) > 0
        
        success = 0
        if ipo_status == 'public' or acquired:
            success = 1
        elif closed_on:
            success = 0
        else:
            # Still operating - exclude from training
            return None
        
        # Extract features
        features = {
            'company_name': properties.get('name'),
            'founded_year': self._extract_year(properties.get('founded_on')),
            'total_funding': properties.get('total_funding_usd', 0),
            'num_funding_rounds': properties.get('num_funding_rounds', 0),
            'employee_count': self._map_employee_range(
                properties.get('num_employees_enum')
            ),
            'revenue_range': self._map_revenue_range(
                properties.get('revenue_range')
            ),
            'industry': properties.get('categories', [{}])[0].get('name', 'Other'),
            'location': properties.get('location', {}).get('region', 'Unknown'),
            'success_outcome': success
        }
        
        return features
    
    def _extract_year(self, date_str: str) -> int:
        """Extract year from date string"""
        if not date_str:
            return 0
        try:
            return int(date_str[:4])
        except:
            return 0
    
    def _map_employee_range(self, range_str: str) -> int:
        """Map employee range to numeric value"""
        mapping = {
            'c_00001_00010': 5,
            'c_00011_00050': 30,
            'c_00051_00100': 75,
            'c_00101_00250': 175,
            'c_00251_00500': 375,
            'c_00501_01000': 750,
            'c_01001_05000': 3000,
            'c_05001_10000': 7500,
            'c_10001_max': 15000
        }
        return mapping.get(range_str, 50)
    
    def _map_revenue_range(self, range_str: str) -> float:
        """Map revenue range to numeric value"""
        mapping = {
            'r_00000000': 0,
            'r_00000001_00100000': 50000,
            'r_00100001_01000000': 500000,
            'r_01000001_10000000': 5000000,
            'r_10000001_50000000': 30000000,
            'r_50000001_100000000': 75000000,
            'r_100000001_500000000': 300000000,
            'r_500000001_1000000000': 750000000,
            'r_1000000001_max': 2000000000
        }
        return mapping.get(range_str, 1000000)
```

---

## Step 5: Testing and Validation

### 5.1 Create Comprehensive Test Suite

Create `tests/test_advanced_models.py`:

```python
"""
Comprehensive tests for advanced models
"""
import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from ml_core.models.dna_analyzer import DNAPatternAnalyzer
from ml_core.serving.model_loader import ModelLoader, AdvancedModelOrchestrator

class TestAdvancedModels:
    """Test suite for advanced models"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        np.random.seed(42)
        n_samples = 100
        n_features = 45
        
        X = pd.DataFrame(
            np.random.randn(n_samples, n_features),
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        y = np.random.randint(0, 2, n_samples)
        
        return X, y
    
    def test_dna_analyzer_training(self, sample_data):
        """Test DNA analyzer training"""
        X, y = sample_data
        
        model = DNAPatternAnalyzer()
        model.fit(X, y)
        
        # Check predictions
        probs = model.predict_proba(X)
        assert probs.shape == (len(X), 2)
        assert np.all((probs >= 0) & (probs <= 1))
        
        # Check DNA signature
        signature = model.get_dna_signature(X.iloc[:1])
        assert 'primary_pattern' in signature
        assert 'dna_summary' in signature
    
    def test_model_serialization(self, sample_data, tmp_path):
        """Test model save/load"""
        X, y = sample_data
        
        # Train and save
        model = DNAPatternAnalyzer()
        model.fit(X, y)
        model.save(tmp_path / 'test_model')
        
        # Load
        loaded_model = DNAPatternAnalyzer.load(tmp_path / 'test_model')
        
        # Compare predictions
        orig_probs = model.predict_proba(X)
        loaded_probs = loaded_model.predict_proba(X)
        
        np.testing.assert_allclose(orig_probs, loaded_probs)
    
    def test_model_loader(self):
        """Test model loader with various formats"""
        loader = ModelLoader()
        
        # Test with non-existent path
        model = loader.load_model(Path('non_existent'))
        assert model is None
        
        # Test with actual model path (if exists)
        model_path = Path('models/advanced/dna_analyzer')
        if model_path.exists():
            model = loader.load_model(model_path)
            assert model is not None
    
    def test_orchestrator(self, sample_data):
        """Test advanced model orchestrator"""
        X, y = sample_data
        
        orchestrator = AdvancedModelOrchestrator()
        results = orchestrator.load_all_models()
        
        # Check predictions (if any models loaded)
        if any(results.values()):
            predictions = orchestrator.predict(X.iloc[:1])
            assert 'combined_probability' in predictions
            assert 0 <= predictions['combined_probability'] <= 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## Implementation Timeline

### Week 1: Architecture Setup
- [ ] Create ml_core package structure
- [ ] Implement base model classes
- [ ] Create DNA Pattern Analyzer
- [ ] Set up model serialization

### Week 2: Model Implementation
- [ ] Implement Temporal Predictor
- [ ] Implement Industry Models
- [ ] Create Hierarchical Ensemble
- [ ] Build training pipeline

### Week 3: Integration
- [ ] Update API server
- [ ] Create model loader
- [ ] Test end-to-end flow
- [ ] Fix legacy model loading

### Week 4: Data & Optimization
- [ ] Set up data collectors
- [ ] Gather additional data
- [ ] Retrain all models
- [ ] Performance optimization

### Week 5: Production Deployment
- [ ] Deploy to staging
- [ ] Load testing
- [ ] Monitor performance
- [ ] Production rollout

---

## Success Criteria

1. **All advanced models loading successfully**
2. **Combined accuracy > 85% AUC**
3. **Inference latency < 200ms**
4. **Zero model loading failures**
5. **Comprehensive test coverage**
6. **Production-ready monitoring**

This implementation plan provides a robust, scalable solution that will transform FLASH into a truly billion-dollar grade product.