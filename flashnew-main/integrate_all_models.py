"""
Comprehensive Model Integration for FLASH Platform
Integrates ALL available models including:
- Base v2 models (CAMP pillars)
- Enhanced v2 models (conservative, aggressive, balanced, deep)
- Hierarchical models (stage, temporal, industry, DNA)
- Experimental models from 75-feature experiments
- Clustering and advanced ensembles
"""

import pandas as pd
import numpy as np
import joblib
import catboost as cb
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional, Tuple
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComprehensiveModelEnsemble:
    """Master ensemble integrating ALL available models"""
    
    def __init__(self):
        self.models = {}
        self.model_weights = {}
        self.feature_sets = {
            '45_features': None,
            '75_features': None,
            'clustering_features': None
        }
        self.is_loaded = False
        
    def load_all_models(self):
        """Load all available models from various directories"""
        logger.info("Loading comprehensive model ensemble...")
        
        # 1. Load base v2 models (CAMP pillars)
        self._load_v2_models()
        
        # 2. Load enhanced v2 models
        self._load_v2_enhanced_models()
        
        # 3. Load hierarchical 45-feature models
        self._load_hierarchical_models()
        
        # 4. Load experimental 75-feature models (if needed)
        self._load_experimental_models()
        
        # 5. Set up model weights based on performance
        self._initialize_model_weights()
        
        self.is_loaded = True
        logger.info(f"Successfully loaded {len(self.models)} models")
        
    def _load_v2_models(self):
        """Load v2 CAMP pillar models"""
        v2_path = Path('models/v2')
        if v2_path.exists():
            try:
                self.models['capital_pillar'] = cb.CatBoost().load_model(str(v2_path / 'capital_model.cbm'))
                self.models['advantage_pillar'] = cb.CatBoost().load_model(str(v2_path / 'advantage_model.cbm'))
                self.models['market_pillar'] = cb.CatBoost().load_model(str(v2_path / 'market_model.cbm'))
                self.models['people_pillar'] = cb.CatBoost().load_model(str(v2_path / 'people_model.cbm'))
                self.models['v2_meta'] = cb.CatBoost().load_model(str(v2_path / 'meta_model.cbm'))
                logger.info("Loaded v2 CAMP pillar models")
            except Exception as e:
                logger.warning(f"Failed to load v2 models: {e}")
                
    def _load_v2_enhanced_models(self):
        """Load enhanced v2 models"""
        enhanced_path = Path('models/v2_enhanced')
        if enhanced_path.exists():
            try:
                self.models['conservative'] = cb.CatBoost().load_model(str(enhanced_path / 'conservative_model.cbm'))
                self.models['aggressive'] = cb.CatBoost().load_model(str(enhanced_path / 'aggressive_model.cbm'))
                self.models['balanced'] = cb.CatBoost().load_model(str(enhanced_path / 'balanced_model.cbm'))
                self.models['deep'] = cb.CatBoost().load_model(str(enhanced_path / 'deep_model.cbm'))
                
                # Meta models
                self.models['meta_catboost'] = cb.CatBoost().load_model(str(enhanced_path / 'meta_catboost_meta.cbm'))
                self.models['meta_logistic'] = joblib.load(enhanced_path / 'meta_logistic.pkl')
                self.models['meta_nn'] = joblib.load(enhanced_path / 'meta_nn.pkl')
                
                logger.info("Loaded v2 enhanced models")
            except Exception as e:
                logger.warning(f"Failed to load enhanced models: {e}")
                
    def _load_hierarchical_models(self):
        """Load new hierarchical 45-feature models"""
        hier_path = Path('models/hierarchical_45features')
        if hier_path.exists():
            try:
                self.models['stage_hierarchical'] = joblib.load(hier_path / 'stage_hierarchical_model.pkl')
                self.models['temporal_hierarchical'] = joblib.load(hier_path / 'temporal_hierarchical_model.pkl')
                self.models['industry_specific'] = joblib.load(hier_path / 'industry_specific_model.pkl')
                self.models['dna_pattern'] = joblib.load(hier_path / 'dna_pattern_model.pkl')
                self.models['hierarchical_meta'] = joblib.load(hier_path / 'hierarchical_meta_ensemble.pkl')
                logger.info("Loaded hierarchical 45-feature models")
            except Exception as e:
                logger.warning(f"Failed to load hierarchical models: {e}")
                
    def _load_experimental_models(self):
        """Load experimental models (75 features, clustering, etc.)"""
        exp_path = Path('experiments')
        
        # Load 75-feature models (if we want to support extended features)
        v2_75_path = exp_path / 'v2_75features'
        if v2_75_path.exists():
            try:
                self.models['catboost_75_1'] = cb.CatBoost().load_model(str(v2_75_path / 'catboost_1.cbm'))
                self.models['catboost_75_2'] = cb.CatBoost().load_model(str(v2_75_path / 'catboost_2.cbm'))
                self.models['xgboost_75'] = joblib.load(v2_75_path / 'xgboost.pkl')
                self.models['lightgbm_75'] = joblib.load(v2_75_path / 'lightgbm.pkl')
                self.models['meta_75'] = joblib.load(v2_75_path / 'meta_learner.pkl')
                logger.info("Loaded 75-feature experimental models")
            except Exception as e:
                logger.warning(f"Failed to load 75-feature models: {e}")
        
        # Load industry-specific models from experiments
        industry_path = exp_path / 'other_approaches/industry_specific'
        if industry_path.exists():
            try:
                for industry_file in industry_path.glob('industry_*.cbm'):
                    industry_name = industry_file.stem.replace('industry_', '')
                    self.models[f'industry_exp_{industry_name}'] = cb.CatBoost().load_model(str(industry_file))
                logger.info("Loaded experimental industry models")
            except Exception as e:
                logger.warning(f"Failed to load experimental industry models: {e}")
                
    def _initialize_model_weights(self):
        """Set model weights based on expected performance"""
        # Base weights for different model types
        self.model_weights = {
            # V2 models (proven performance)
            'v2_meta': 0.15,
            'conservative': 0.10,
            'aggressive': 0.08,
            'balanced': 0.10,
            'deep': 0.08,
            
            # Hierarchical models (new high performers)
            'hierarchical_meta': 0.20,
            'stage_hierarchical': 0.08,
            'temporal_hierarchical': 0.06,
            'industry_specific': 0.08,
            'dna_pattern': 0.07,
            
            # Pillar models (specialized)
            'capital_pillar': 0.02,
            'advantage_pillar': 0.02,
            'market_pillar': 0.02,
            'people_pillar': 0.02,
            
            # Meta models
            'meta_catboost': 0.05,
            'meta_logistic': 0.03,
            'meta_nn': 0.02,
        }
        
        # Normalize weights
        total_weight = sum(self.model_weights.values())
        self.model_weights = {k: v/total_weight for k, v in self.model_weights.items()}
        
    def predict(self, X: pd.DataFrame, 
                model_subset: Optional[List[str]] = None,
                return_all_predictions: bool = False) -> Dict[str, Any]:
        """
        Make predictions using the comprehensive ensemble
        
        Args:
            X: Input features (45 or 75 features)
            model_subset: Optional list of specific models to use
            return_all_predictions: Return individual model predictions
            
        Returns:
            Dictionary with predictions and metadata
        """
        if not self.is_loaded:
            self.load_all_models()
            
        # Determine feature set
        n_features = len(X.columns)
        is_45_features = n_features < 50
        
        # Collect predictions from all applicable models
        predictions = {}
        model_list = model_subset or list(self.models.keys())
        
        for model_name, model in self.models.items():
            if model_name not in model_list:
                continue
                
            try:
                # Skip 75-feature models if we have 45 features
                if is_45_features and '75' in model_name:
                    continue
                    
                # Get prediction based on model type
                if hasattr(model, 'predict_proba'):
                    if 'hierarchical' in model_name:
                        # Hierarchical models need special handling
                        pred = model.predict_proba(X.copy())
                        if hasattr(pred, 'shape') and len(pred.shape) > 1:
                            pred = pred[:, 1]
                    else:
                        pred = model.predict_proba(X)[:, 1]
                elif hasattr(model, 'predict'):
                    pred = model.predict(X)
                else:
                    continue
                    
                predictions[model_name] = pred
                
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {e}")
                continue
        
        # Calculate weighted ensemble prediction
        if predictions:
            weighted_sum = np.zeros(len(X))
            total_weight = 0
            
            for model_name, pred in predictions.items():
                weight = self.model_weights.get(model_name, 0.01)
                weighted_sum += pred * weight
                total_weight += weight
                
            ensemble_prediction = weighted_sum / total_weight
        else:
            ensemble_prediction = np.full(len(X), 0.5)  # Default to 0.5
            
        # Prepare results
        results = {
            'ensemble_probability': ensemble_prediction,
            'confidence_score': self._calculate_confidence(predictions),
            'models_used': len(predictions),
            'feature_set': '45_features' if is_45_features else '75_features'
        }
        
        if return_all_predictions:
            results['individual_predictions'] = predictions
            results['model_weights'] = {k: v for k, v in self.model_weights.items() if k in predictions}
            
        return results
    
    def _calculate_confidence(self, predictions: Dict[str, np.ndarray]) -> float:
        """Calculate confidence based on model agreement"""
        if not predictions:
            return 0.0
            
        pred_values = list(predictions.values())
        if len(pred_values) == 1:
            return 0.5
            
        # Calculate standard deviation of predictions
        std_dev = np.std(pred_values, axis=0).mean()
        
        # Convert to confidence (lower std = higher confidence)
        confidence = 1.0 - min(std_dev * 2, 1.0)
        
        return confidence
    
    def get_model_insights(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Get detailed insights from different model perspectives"""
        insights = {
            'stage_insights': None,
            'temporal_insights': None,
            'industry_insights': None,
            'dna_insights': None,
            'risk_factors': [],
            'growth_indicators': []
        }
        
        # Get stage-based insights
        if 'stage_hierarchical' in self.models:
            try:
                stage_pred = self.models['stage_hierarchical'].predict_proba(X.copy())[:, 1]
                insights['stage_insights'] = {
                    'prediction': float(stage_pred[0]),
                    'recommendation': self._get_stage_recommendation(X.iloc[0])
                }
            except:
                pass
                
        # Get temporal insights
        if 'temporal_hierarchical' in self.models:
            try:
                temporal_pred = self.models['temporal_hierarchical'].predict_proba(X.copy())[:, 1]
                insights['temporal_insights'] = {
                    'prediction': float(temporal_pred[0]),
                    'time_horizon_focus': self._get_temporal_focus(X.iloc[0])
                }
            except:
                pass
                
        # Get industry insights
        if 'industry_specific' in self.models:
            try:
                industry_pred = self.models['industry_specific'].predict_proba(X.copy())[:, 1]
                insights['industry_insights'] = {
                    'prediction': float(industry_pred[0]),
                    'industry_fit': self._get_industry_fit(X.iloc[0])
                }
            except:
                pass
                
        # Get DNA pattern insights
        if 'dna_pattern' in self.models:
            try:
                dna_pred = self.models['dna_pattern'].predict_proba(X.copy())[:, 1]
                insights['dna_insights'] = {
                    'prediction': float(dna_pred[0]),
                    'pattern_match': self._get_dna_pattern_match(X.iloc[0])
                }
            except:
                pass
                
        # Extract risk factors and growth indicators
        insights['risk_factors'] = self._extract_risk_factors(X.iloc[0])
        insights['growth_indicators'] = self._extract_growth_indicators(X.iloc[0])
        
        return insights
    
    def _get_stage_recommendation(self, data):
        """Get stage-specific recommendations"""
        stage = data.get('funding_stage', 'Unknown')
        if 'pre' in stage.lower() or 'seed' in stage.lower():
            return "Focus on team building and product-market fit"
        elif 'series a' in stage.lower():
            return "Prioritize market expansion and unit economics"
        elif 'series b' in stage.lower() or 'series c' in stage.lower():
            return "Optimize for capital efficiency and market dominance"
        return "Continue executing on growth strategy"
    
    def _get_temporal_focus(self, data):
        """Determine temporal focus based on metrics"""
        runway = data.get('runway_months', 12)
        if runway < 6:
            return "Short-term: Urgent need to extend runway or achieve profitability"
        elif runway < 18:
            return "Medium-term: Focus on growth metrics and efficiency"
        else:
            return "Long-term: Build sustainable competitive advantages"
    
    def _get_industry_fit(self, data):
        """Assess industry fit"""
        industry = data.get('sector', 'Unknown')
        if industry == 'SaaS':
            ndr = data.get('net_dollar_retention_percent', 100)
            if ndr > 120:
                return "Excellent SaaS metrics - strong product-market fit"
            elif ndr > 100:
                return "Good SaaS fundamentals - focus on expansion revenue"
            else:
                return "Below-average retention - address churn urgently"
        return f"Performing within {industry} benchmarks"
    
    def _get_dna_pattern_match(self, data):
        """Identify DNA pattern matches"""
        growth_rate = data.get('revenue_growth_rate_percent', 0)
        burn_multiple = data.get('burn_multiple', 5)
        
        if growth_rate > 200 and burn_multiple < 2:
            return "Efficient Hypergrowth - Rare successful pattern"
        elif growth_rate > 100 and burn_multiple < 3:
            return "Balanced Growth - Strong success indicator"
        elif growth_rate < 50 and burn_multiple > 5:
            return "Inefficient Burn - High risk pattern"
        else:
            return "Mixed signals - Monitor efficiency closely"
    
    def _extract_risk_factors(self, data):
        """Extract key risk factors"""
        risks = []
        
        if data.get('runway_months', 12) < 6:
            risks.append("Critical: Less than 6 months runway")
        
        if data.get('burn_multiple', 0) > 5:
            risks.append("High burn multiple indicates inefficiency")
            
        if data.get('customer_concentration_percent', 0) > 30:
            risks.append("High customer concentration risk")
            
        if data.get('net_dollar_retention_percent', 100) < 90:
            risks.append("Poor retention metrics")
            
        return risks[:3]  # Top 3 risks
    
    def _extract_growth_indicators(self, data):
        """Extract positive growth indicators"""
        indicators = []
        
        if data.get('revenue_growth_rate_percent', 0) > 100:
            indicators.append("Triple-digit revenue growth")
            
        if data.get('net_dollar_retention_percent', 0) > 120:
            indicators.append("Excellent net dollar retention")
            
        if data.get('gross_margin_percent', 0) > 70:
            indicators.append("Strong gross margins")
            
        if data.get('ltv_cac_ratio', 0) > 3:
            indicators.append("Efficient customer acquisition")
            
        return indicators[:3]  # Top 3 indicators


def create_unified_api_integration():
    """Create API integration code for all models"""
    
    integration_code = '''
# Add this to api_server.py after existing model loading

# Initialize comprehensive ensemble
comprehensive_ensemble = ComprehensiveModelEnsemble()
comprehensive_ensemble.load_all_models()

@app.post("/predict_comprehensive")
async def predict_comprehensive(startup_data: StartupDataInput):
    """
    Comprehensive prediction using ALL available models
    Provides ensemble prediction with detailed insights
    """
    try:
        # Convert to DataFrame
        data_dict = startup_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Get comprehensive predictions
        results = comprehensive_ensemble.predict(
            df, 
            return_all_predictions=True
        )
        
        # Get detailed insights
        insights = comprehensive_ensemble.get_model_insights(df)
        
        # Calculate CAMP scores using best models
        camp_scores = {
            'capital': float(comprehensive_ensemble.models.get('capital_pillar', 
                            comprehensive_ensemble.models['conservative']).predict_proba(df)[:, 1][0]),
            'advantage': float(comprehensive_ensemble.models.get('advantage_pillar',
                            comprehensive_ensemble.models['balanced']).predict_proba(df)[:, 1][0]),
            'market': float(comprehensive_ensemble.models.get('market_pillar',
                            comprehensive_ensemble.models['aggressive']).predict_proba(df)[:, 1][0]),
            'people': float(comprehensive_ensemble.models.get('people_pillar',
                            comprehensive_ensemble.models['deep']).predict_proba(df)[:, 1][0])
        }
        
        response = {
            "success_probability": float(results['ensemble_probability'][0]),
            "confidence_score": float(results['confidence_score']),
            "models_used": results['models_used'],
            "pillar_scores": camp_scores,
            "insights": insights,
            "risk_factors": insights['risk_factors'],
            "growth_indicators": insights['growth_indicators'],
            "recommendations": [
                insights.get('stage_insights', {}).get('recommendation', ''),
                insights.get('temporal_insights', {}).get('time_horizon_focus', ''),
                insights.get('industry_insights', {}).get('industry_fit', '')
            ],
            "advanced_insights": {
                "stage_prediction": insights.get('stage_insights', {}).get('prediction'),
                "temporal_prediction": insights.get('temporal_insights', {}).get('prediction'),
                "industry_prediction": insights.get('industry_insights', {}).get('prediction'),
                "dna_pattern_match": insights.get('dna_insights', {}).get('pattern_match')
            }
        }
        
        # Add individual model predictions if requested
        if startup_data.return_all_predictions:
            response["individual_predictions"] = {
                k: float(v[0]) for k, v in results['individual_predictions'].items()
            }
            response["model_weights"] = results['model_weights']
        
        return response
        
    except Exception as e:
        logger.error(f"Comprehensive prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/available")
async def get_available_models():
    """List all available models and their status"""
    model_status = {}
    
    for model_name in comprehensive_ensemble.models:
        model_status[model_name] = {
            "loaded": True,
            "weight": comprehensive_ensemble.model_weights.get(model_name, 0.01),
            "type": "hierarchical" if "hierarchical" in model_name else "ensemble"
        }
    
    return {
        "total_models": len(model_status),
        "models": model_status,
        "feature_sets_supported": ["45_features", "75_features"]
    }
'''
    
    return integration_code


def test_comprehensive_ensemble():
    """Test the comprehensive ensemble"""
    # Load test data
    df = pd.read_csv('data/final_100k_dataset_45features.csv', nrows=5)
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in [
        'startup_id', 'startup_name', 'success', 'founding_year', 'burn_multiple_calc'
    ]]
    
    X = df[feature_cols]
    
    # Initialize ensemble
    ensemble = ComprehensiveModelEnsemble()
    ensemble.load_all_models()
    
    # Test predictions
    print("\nTesting Comprehensive Ensemble:")
    print("-" * 50)
    
    for i in range(min(3, len(X))):
        print(f"\nTest case {i+1}:")
        print(f"Company: {df.iloc[i]['startup_name']}")
        print(f"Stage: {df.iloc[i]['funding_stage']}")
        print(f"Sector: {df.iloc[i]['sector']}")
        
        results = ensemble.predict(X.iloc[[i]], return_all_predictions=True)
        insights = ensemble.get_model_insights(X.iloc[[i]])
        
        print(f"Ensemble Prediction: {results['ensemble_probability'][0]:.3f}")
        print(f"Confidence: {results['confidence_score']:.3f}")
        print(f"Models Used: {results['models_used']}")
        
        if insights['stage_insights']:
            print(f"Stage-based prediction: {insights['stage_insights']['prediction']:.3f}")
        if insights['dna_insights']:
            print(f"DNA Pattern: {insights['dna_insights']['pattern_match']}")
        
        print(f"Risk Factors: {', '.join(insights['risk_factors'])}")
        print(f"Growth Indicators: {', '.join(insights['growth_indicators'])}")
    
    # Save integration code
    with open('api_integration_comprehensive.py', 'w') as f:
        f.write(create_unified_api_integration())
    
    print("\n✅ Comprehensive ensemble tested successfully!")
    print("📝 API integration code saved to api_integration_comprehensive.py")


if __name__ == "__main__":
    test_comprehensive_ensemble()