
# Add to api_server.py or create new file

from fix_v2_enhanced_models import FixedV2Ensemble
from integrate_models_fixed import WorkingModelEnsemble

class CombinedEnsemble:
    """Combines hierarchical and fixed V2 models"""
    
    def __init__(self):
        self.hierarchical = WorkingModelEnsemble()
        self.v2_fixed = FixedV2Ensemble()
        
    def load_all_models(self):
        self.hierarchical.load_working_models()
        self.v2_fixed.load_and_fix_models()
        
    def predict(self, X):
        # Get hierarchical predictions
        hier_results = self.hierarchical.predict_with_all_models(X)
        
        # Get V2 stacking predictions
        v2_pred = self.v2_fixed.predict_with_stacking(X)
        
        # Combine with weights
        # Higher weight to V2 stacking if it has meta-models
        if self.v2_fixed.meta_models:
            weights = {
                'hierarchical': 0.4,
                'v2_stacking': 0.6
            }
        else:
            weights = {
                'hierarchical': 0.7,
                'v2_stacking': 0.3
            }
        
        final_pred = (
            hier_results['ensemble_prediction'] * weights['hierarchical'] +
            v2_pred * weights['v2_stacking']
        )
        
        return {
            'probability': float(final_pred),
            'confidence': (hier_results['confidence'] + 0.8) / 2,  # Adjust confidence
            'models_used': hier_results['models_used'] + len(self.v2_fixed.base_models)
        }
