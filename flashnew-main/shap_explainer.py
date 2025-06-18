#!/usr/bin/env python3
"""
SHAP Explainability Module for FLASH 2.0
Provides interpretable AI insights for startup predictions
Works with the actual model architecture used in production
"""

import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Dict, List, Tuple, Optional, Any
import joblib
from pathlib import Path
import seaborn as sns
import logging
from datetime import datetime

# Configure matplotlib for better quality
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 6)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FLASHExplainer:
    """SHAP-based explainability for FLASH predictions"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models = {}
        self.explainers = {}
        self.feature_names = self._get_feature_names()
        self._load_models()
        
    def _get_feature_names(self) -> List[str]:
        """Get the 45 feature names used in the actual models"""
        return [
            # Capital features (12)
            'funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd',
            'monthly_burn_usd', 'runway_months', 'annual_revenue_run_rate',
            'revenue_growth_rate_percent', 'gross_margin_percent', 'burn_multiple',
            'ltv_cac_ratio', 'investor_tier_primary', 'has_debt',
            
            # Advantage features (11)
            'patent_count', 'network_effects_present', 'has_data_moat',
            'regulatory_advantage_present', 'tech_differentiation_score',
            'switching_cost_score', 'brand_strength_score', 'scalability_score',
            'product_stage', 'product_retention_30d', 'product_retention_90d',
            
            # Market features (12)
            'sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
            'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
            'user_growth_rate_percent', 'net_dollar_retention_percent',
            'competition_intensity', 'competitors_named_count', 'dau_mau_ratio',
            
            # People features (10)
            'founders_count', 'team_size_full_time', 'years_experience_avg',
            'domain_expertise_years_avg', 'prior_startup_experience_count',
            'prior_successful_exits_count', 'board_advisor_experience_score',
            'advisors_count', 'team_diversity_percent', 'key_person_dependency'
        ]
        
    def _load_models(self) -> bool:
        """Load models based on available model types"""
        try:
            # Try to load hierarchical models (most recent architecture)
            hierarchical_path = self.models_dir / 'hierarchical_45features'
            if hierarchical_path.exists():
                logger.info("Loading hierarchical models...")
                
                # Stage hierarchical model
                try:
                    self.models['stage_hierarchical'] = joblib.load(
                        hierarchical_path / 'stage_hierarchical_model.pkl'
                    )
                    logger.info("✅ Loaded stage hierarchical model")
                except Exception as e:
                    logger.warning(f"Could not load stage hierarchical: {e}")
                
                # Temporal hierarchical model
                try:
                    self.models['temporal_hierarchical'] = joblib.load(
                        hierarchical_path / 'temporal_hierarchical_model.pkl'
                    )
                    logger.info("✅ Loaded temporal hierarchical model")
                except Exception as e:
                    logger.warning(f"Could not load temporal hierarchical: {e}")
                
                # DNA pattern model
                try:
                    self.models['dna_pattern'] = joblib.load(
                        hierarchical_path / 'dna_pattern_model.pkl'
                    )
                    logger.info("✅ Loaded DNA pattern model")
                except Exception as e:
                    logger.warning(f"Could not load DNA pattern model: {e}")
                    
                # Hierarchical meta ensemble
                try:
                    self.models['hierarchical_meta'] = joblib.load(
                        hierarchical_path / 'hierarchical_meta_ensemble.pkl'
                    )
                    logger.info("✅ Loaded hierarchical meta ensemble")
                except Exception as e:
                    logger.warning(f"Could not load hierarchical meta: {e}")
            
            # Try to load production ensemble
            try:
                self.models['production_ensemble'] = joblib.load(
                    self.models_dir / 'final_production_ensemble.pkl'
                )
                logger.info("✅ Loaded production ensemble")
            except Exception as e:
                logger.warning(f"Could not load production ensemble: {e}")
            
            # Try to load v2 enhanced models
            v2_path = self.models_dir / 'v2_enhanced'
            if v2_path.exists():
                try:
                    self.models['v2_enhanced'] = joblib.load(
                        v2_path / 'meta_catboost_meta.cbm'
                    )
                    logger.info("✅ Loaded v2 enhanced model")
                except Exception as e:
                    logger.warning(f"Could not load v2 enhanced: {e}")
            
            # Create explainers for loaded models
            self._create_explainers()
            
            logger.info(f"Successfully loaded {len(self.models)} models")
            return len(self.models) > 0
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False
    
    def _create_explainers(self):
        """Create SHAP explainers for each loaded model"""
        for name, model in self.models.items():
            try:
                # For ensemble models, we need the base estimator
                if hasattr(model, 'estimators_'):
                    # Use the first estimator for explanation
                    base_model = model.estimators_[0]
                    self.explainers[name] = shap.TreeExplainer(base_model)
                elif hasattr(model, 'model'):
                    # Some models wrap the actual model
                    self.explainers[name] = shap.TreeExplainer(model.model)
                else:
                    # Direct model
                    self.explainers[name] = shap.TreeExplainer(model)
                logger.info(f"Created explainer for {name}")
            except Exception as e:
                logger.warning(f"Could not create explainer for {name}: {e}")
                # Fallback to KernelExplainer for non-tree models
                try:
                    background = shap.sample(pd.DataFrame(
                        np.zeros((100, len(self.feature_names))),
                        columns=self.feature_names
                    ), 100)
                    self.explainers[name] = shap.KernelExplainer(
                        model.predict_proba if hasattr(model, 'predict_proba') else model.predict,
                        background
                    )
                    logger.info(f"Created kernel explainer for {name}")
                except Exception as e2:
                    logger.error(f"Could not create any explainer for {name}: {e2}")
    
    def explain_prediction(self, features: pd.DataFrame, 
                         model_name: Optional[str] = None,
                         include_plots: bool = True) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for a prediction
        
        Args:
            features: DataFrame with startup features
            model_name: Specific model to use (None = use best available)
            include_plots: Whether to generate visualization plots
            
        Returns:
            Dict with explanations, predictions, and insights
        """
        if not self.models:
            return {
                'error': 'No models loaded',
                'predictions': {},
                'explanations': {},
                'insights': {}
            }
        
        # Ensure features are in correct order
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        
        # Reorder columns to match expected feature order
        features = features[self.feature_names]
        
        # Get predictions from each model
        predictions = {}
        explanations = {}
        
        # If specific model requested
        if model_name and model_name in self.models:
            models_to_use = {model_name: self.models[model_name]}
        else:
            models_to_use = self.models
        
        for name, model in models_to_use.items():
            try:
                # Get prediction
                if hasattr(model, 'predict_proba'):
                    pred = model.predict_proba(features)[0, 1]
                else:
                    pred = model.predict(features)[0]
                predictions[name] = float(pred)
                
                # Get SHAP values if explainer exists
                if name in self.explainers:
                    shap_values = self.explainers[name].shap_values(features)
                    if isinstance(shap_values, list):
                        shap_values = shap_values[1]  # For binary classification
                    
                    explanations[name] = {
                        'prediction': float(pred),
                        'shap_values': shap_values[0].tolist() if hasattr(shap_values[0], 'tolist') else shap_values[0],
                        'feature_names': self.feature_names,
                        'feature_values': features.iloc[0].tolist()
                    }
                else:
                    explanations[name] = {
                        'prediction': float(pred),
                        'error': 'No explainer available for this model'
                    }
                    
            except Exception as e:
                logger.error(f"Error explaining {name}: {e}")
                predictions[name] = 0.5
                explanations[name] = {'error': str(e)}
        
        # Calculate ensemble prediction
        if predictions:
            ensemble_pred = np.mean(list(predictions.values()))
        else:
            ensemble_pred = 0.5
        
        # Generate plots if requested
        plots = {}
        if include_plots and explanations:
            plots = self._generate_plots(explanations, ensemble_pred)
        
        # Generate insights
        insights = self._generate_insights(explanations, predictions)
        
        return {
            'ensemble_prediction': float(ensemble_pred),
            'model_predictions': predictions,
            'explanations': explanations,
            'plots': plots,
            'insights': insights,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_plots(self, explanations: Dict, ensemble_pred: float) -> Dict[str, str]:
        """Generate visualization plots"""
        plots = {}
        
        # 1. Model consensus plot
        if len(explanations) > 1:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            model_names = []
            predictions = []
            
            for model_name, exp in explanations.items():
                if 'prediction' in exp and not exp.get('error'):
                    model_names.append(model_name.replace('_', ' ').title())
                    predictions.append(exp['prediction'])
            
            if predictions:
                # Create bar chart
                y_pos = np.arange(len(predictions))
                colors = ['#2ecc71' if p > 0.5 else '#e74c3c' for p in predictions]
                
                bars = ax.barh(y_pos, predictions, color=colors)
                ax.set_yticks(y_pos)
                ax.set_yticklabels(model_names)
                ax.set_xlabel('Success Probability')
                ax.set_title('Model Predictions Consensus')
                ax.set_xlim(0, 1)
                
                # Add ensemble line
                ax.axvline(x=ensemble_pred, color='blue', linestyle='--', 
                          linewidth=2, label=f'Ensemble: {ensemble_pred:.2%}')
                ax.axvline(x=0.5, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
                
                # Add value labels
                for i, (bar, pred) in enumerate(zip(bars, predictions)):
                    ax.text(pred + 0.01, bar.get_y() + bar.get_height()/2,
                           f'{pred:.1%}', va='center', fontsize=9)
                
                ax.legend()
                plt.tight_layout()
                plots['model_consensus'] = self._fig_to_base64(fig)
                plt.close(fig)
        
        # 2. Feature importance plot (from best available model)
        best_model_name = None
        best_explanation = None
        
        # Find best model with SHAP values
        for name, exp in explanations.items():
            if 'shap_values' in exp and not exp.get('error'):
                best_model_name = name
                best_explanation = exp
                break
        
        if best_explanation:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            shap_values = np.array(best_explanation['shap_values'])
            feature_names = best_explanation['feature_names']
            feature_values = best_explanation['feature_values']
            
            # Get top 20 features by absolute impact
            abs_shap = np.abs(shap_values)
            top_idx = np.argsort(abs_shap)[-20:][::-1]
            
            # Create horizontal bar chart
            y_pos = np.arange(len(top_idx))
            impacts = [shap_values[i] for i in top_idx]
            colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in impacts]
            
            bars = ax.barh(y_pos, impacts, color=colors)
            
            # Set labels with feature values
            labels = []
            for i in top_idx:
                feat_name = feature_names[i].replace('_', ' ').title()
                feat_val = feature_values[i]
                if isinstance(feat_val, (int, float)):
                    labels.append(f"{feat_name}\n({feat_val:.2f})")
                else:
                    labels.append(f"{feat_name}\n({feat_val})")
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=9)
            ax.set_xlabel('Impact on Success Probability')
            ax.set_title(f'Top 20 Feature Contributions ({best_model_name.replace("_", " ").title()})')
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
            
            # Add value labels
            for bar, impact in zip(bars, impacts):
                width = bar.get_width()
                ax.text(width + 0.001 if width > 0 else width - 0.001, 
                       bar.get_y() + bar.get_height()/2,
                       f'{impact:.3f}', 
                       ha='left' if width > 0 else 'right', 
                       va='center', fontsize=8)
            
            plt.tight_layout()
            plots['feature_importance'] = self._fig_to_base64(fig)
            plt.close(fig)
        
        # 3. CAMP category breakdown if we have the data
        if best_explanation and 'feature_names' in best_explanation:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Calculate CAMP category impacts
            camp_impacts = {
                'Capital': 0,
                'Advantage': 0,
                'Market': 0,
                'People': 0
            }
            
            shap_values = best_explanation['shap_values']
            
            # Map features to categories
            capital_features = ['funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd',
                              'monthly_burn_usd', 'runway_months', 'annual_revenue_run_rate',
                              'revenue_growth_rate_percent', 'gross_margin_percent', 'burn_multiple',
                              'ltv_cac_ratio', 'investor_tier_primary', 'has_debt']
            
            advantage_features = ['patent_count', 'network_effects_present', 'has_data_moat',
                                'regulatory_advantage_present', 'tech_differentiation_score',
                                'switching_cost_score', 'brand_strength_score', 'scalability_score',
                                'product_stage', 'product_retention_30d', 'product_retention_90d']
            
            market_features = ['sector', 'tam_size_usd', 'sam_size_usd', 'som_size_usd',
                             'market_growth_rate_percent', 'customer_count', 'customer_concentration_percent',
                             'user_growth_rate_percent', 'net_dollar_retention_percent',
                             'competition_intensity', 'competitors_named_count', 'dau_mau_ratio']
            
            people_features = ['founders_count', 'team_size_full_time', 'years_experience_avg',
                             'domain_expertise_years_avg', 'prior_startup_experience_count',
                             'prior_successful_exits_count', 'board_advisor_experience_score',
                             'advisors_count', 'team_diversity_percent', 'key_person_dependency']
            
            # Sum SHAP values by category
            for i, feat in enumerate(self.feature_names):
                if feat in capital_features:
                    camp_impacts['Capital'] += shap_values[i]
                elif feat in advantage_features:
                    camp_impacts['Advantage'] += shap_values[i]
                elif feat in market_features:
                    camp_impacts['Market'] += shap_values[i]
                elif feat in people_features:
                    camp_impacts['People'] += shap_values[i]
            
            # Create bar chart
            categories = list(camp_impacts.keys())
            impacts = list(camp_impacts.values())
            colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in impacts]
            
            bars = ax.bar(categories, impacts, color=colors)
            ax.set_ylabel('Impact on Success Probability')
            ax.set_title('CAMP Category Contributions')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., 
                       height + 0.001 if height > 0 else height - 0.001,
                       f'{height:.3f}', ha='center', 
                       va='bottom' if height > 0 else 'top')
            
            plt.tight_layout()
            plots['camp_breakdown'] = self._fig_to_base64(fig)
            plt.close(fig)
        
        return plots
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        return f"data:image/png;base64,{image_base64}"
    
    def _generate_insights(self, explanations: Dict, predictions: Dict) -> Dict[str, List[str]]:
        """Generate human-readable insights from explanations"""
        insights = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'key_drivers': [],
            'model_agreement': []
        }
        
        # Analyze model agreement
        if len(predictions) > 1:
            pred_values = list(predictions.values())
            std_dev = np.std(pred_values)
            mean_pred = np.mean(pred_values)
            
            if std_dev < 0.05:
                insights['model_agreement'].append(
                    f"Strong consensus across models (std: {std_dev:.3f})"
                )
            elif std_dev < 0.1:
                insights['model_agreement'].append(
                    f"Moderate agreement across models (std: {std_dev:.3f})"
                )
            else:
                insights['model_agreement'].append(
                    f"Models show divergent predictions (std: {std_dev:.3f})"
                )
            
            # Find outlier predictions
            for model, pred in predictions.items():
                if abs(pred - mean_pred) > 2 * std_dev:
                    insights['model_agreement'].append(
                        f"{model} shows significantly different prediction: {pred:.2%}"
                    )
        
        # Find best explanation with SHAP values
        best_explanation = None
        for exp in explanations.values():
            if 'shap_values' in exp and not exp.get('error'):
                best_explanation = exp
                break
        
        if best_explanation:
            shap_values = np.array(best_explanation['shap_values'])
            feature_names = best_explanation['feature_names']
            feature_values = best_explanation['feature_values']
            
            # Top 3 positive impacts
            pos_idx = np.where(shap_values > 0.01)[0]
            if len(pos_idx) > 0:
                top_pos = pos_idx[np.argsort(shap_values[pos_idx])[-3:]][::-1]
                for idx in top_pos:
                    feat_name = feature_names[idx].replace('_', ' ').title()
                    insights['strengths'].append(
                        f"{feat_name}: {feature_values[idx]:.2f} (impact: +{shap_values[idx]:.3f})"
                    )
            
            # Top 3 negative impacts
            neg_idx = np.where(shap_values < -0.01)[0]
            if len(neg_idx) > 0:
                top_neg = neg_idx[np.argsort(shap_values[neg_idx])[:3]]
                for idx in top_neg:
                    feat_name = feature_names[idx].replace('_', ' ').title()
                    insights['weaknesses'].append(
                        f"{feat_name}: {feature_values[idx]:.2f} (impact: {shap_values[idx]:.3f})"
                    )
            
            # Key drivers (top 5 by absolute impact)
            abs_impact = np.abs(shap_values)
            top_drivers = np.argsort(abs_impact)[-5:][::-1]
            
            for idx in top_drivers:
                feat_name = feature_names[idx].replace('_', ' ').title()
                direction = "increasing" if shap_values[idx] > 0 else "decreasing"
                insights['key_drivers'].append(
                    f"{feat_name} is {direction} success probability by {abs(shap_values[idx]):.3f}"
                )
        
        # Generate opportunities based on overall prediction
        mean_pred = np.mean(list(predictions.values())) if predictions else 0.5
        
        if mean_pred > 0.7:
            insights['opportunities'].extend([
                "High success probability - consider aggressive growth strategies",
                "Strong fundamentals suggest readiness for scaling",
                "Focus on maintaining current strengths while expanding"
            ])
        elif mean_pred > 0.5:
            insights['opportunities'].extend([
                "Moderate success probability - focus on strengthening weak areas",
                "Consider targeted improvements in lowest-scoring metrics",
                "Potential for significant improvement with focused effort"
            ])
        else:
            insights['opportunities'].extend([
                "Low success probability - consider fundamental changes",
                "Focus on addressing critical weaknesses before scaling",
                "May benefit from pivot or strategic repositioning"
            ])
        
        return insights
    
    def generate_report_data(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Generate complete report data for comprehensive analysis"""
        # Get full explanation
        explanation = self.explain_prediction(features, include_plots=True)
        
        # Add summary statistics
        summary = {
            'final_prediction': explanation['ensemble_prediction'],
            'model_count': len(explanation['model_predictions']),
            'prediction_range': {
                'min': min(explanation['model_predictions'].values()) if explanation['model_predictions'] else 0,
                'max': max(explanation['model_predictions'].values()) if explanation['model_predictions'] else 0,
                'std': np.std(list(explanation['model_predictions'].values())) if explanation['model_predictions'] else 0
            },
            'confidence_level': 'High' if explanation['model_predictions'] and 
                              np.std(list(explanation['model_predictions'].values())) < 0.05 else 'Medium',
            'top_positive_factors': [],
            'top_negative_factors': [],
            'improvement_areas': []
        }
        
        # Extract top factors from insights
        if 'strengths' in explanation['insights']:
            summary['top_positive_factors'] = explanation['insights']['strengths'][:3]
        
        if 'weaknesses' in explanation['insights']:
            summary['top_negative_factors'] = explanation['insights']['weaknesses'][:3]
        
        # Identify improvement areas
        if explanation['ensemble_prediction'] < 0.7:
            summary['improvement_areas'] = [
                "Focus on improving weakest metrics identified above",
                "Consider strategic changes to business model",
                "Strengthen team or market positioning"
            ]
        
        return {
            'summary': summary,
            'detailed_explanation': explanation,
            'timestamp': datetime.now().isoformat(),
            'model_version': '2.0',
            'feature_count': len(self.feature_names)
        }


if __name__ == "__main__":
    # Test the updated explainer
    explainer = FLASHExplainer()
    
    # Sample features matching the 45 features used in actual models
    test_features = {
        # Capital features
        'funding_stage': 'series_a',
        'total_capital_raised_usd': 5000000,
        'cash_on_hand_usd': 3000000,
        'monthly_burn_usd': 150000,
        'runway_months': 20,
        'annual_revenue_run_rate': 1200000,
        'revenue_growth_rate_percent': 150,
        'gross_margin_percent': 65,
        'burn_multiple': 1.5,
        'ltv_cac_ratio': 3.0,
        'investor_tier_primary': 'tier_2',
        'has_debt': 0,
        
        # Advantage features
        'patent_count': 2,
        'network_effects_present': 1,
        'has_data_moat': 1,
        'regulatory_advantage_present': 0,
        'tech_differentiation_score': 4,
        'switching_cost_score': 3,
        'brand_strength_score': 3,
        'scalability_score': 4,
        'product_stage': 'growth',
        'product_retention_30d': 0.75,
        'product_retention_90d': 0.65,
        
        # Market features
        'sector': 'SaaS',
        'tam_size_usd': 50000000000,
        'sam_size_usd': 5000000000,
        'som_size_usd': 500000000,
        'market_growth_rate_percent': 25,
        'customer_count': 100,
        'customer_concentration_percent': 15,
        'user_growth_rate_percent': 200,
        'net_dollar_retention_percent': 110,
        'competition_intensity': 3,
        'competitors_named_count': 10,
        'dau_mau_ratio': 0.4,
        
        # People features
        'founders_count': 2,
        'team_size_full_time': 25,
        'years_experience_avg': 12,
        'domain_expertise_years_avg': 8,
        'prior_startup_experience_count': 2,
        'prior_successful_exits_count': 1,
        'board_advisor_experience_score': 4,
        'advisors_count': 4,
        'team_diversity_percent': 40,
        'key_person_dependency': 0
    }
    
    # Convert to DataFrame
    test_df = pd.DataFrame([test_features])
    
    # Generate explanation
    result = explainer.explain_prediction(test_df)
    
    if 'error' not in result:
        print("✅ Explanation generated successfully!")
        print(f"\nEnsemble prediction: {result['ensemble_prediction']:.2%}")
        
        print("\nModel predictions:")
        for model, pred in result['model_predictions'].items():
            print(f"  - {model}: {pred:.2%}")
        
        print("\nKey insights:")
        for category, items in result['insights'].items():
            if items:
                print(f"\n{category.upper()}:")
                for item in items[:3]:  # Show top 3 items
                    print(f"  - {item}")
        
        print("\nGenerated plots:")
        for plot_name in result['plots'].keys():
            print(f"  - {plot_name}")
    else:
        print(f"❌ Error: {result['error']}")