#!/usr/bin/env python3
"""
Pattern System Integration Wrapper
Handles pattern classification with proper feature alignment
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PatternSystemWrapper:
    """Wrapper for pattern system with feature alignment"""
    
    def __init__(self, pattern_classifier):
        self.pattern_classifier = pattern_classifier
        self.patterns_loaded = False
        self._load_patterns()
    
    def _load_patterns(self):
        """Load and validate patterns"""
        try:
            self.patterns = self.pattern_classifier.list_patterns()
            self.patterns_loaded = True
            logger.info(f"Loaded {len(self.patterns)} patterns")
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")
            self.patterns = []
    
    def predict(self, features: Dict) -> Dict:
        """Predict with proper error handling"""
        if not self.patterns_loaded:
            return {
                'pattern_score': 0.5,
                'primary_patterns': [],
                'all_patterns': [],
                'error': 'Pattern system not loaded'
            }
        
        try:
            # Ensure all required features are present
            for feature in ['funding_stage', 'sector', 'product_stage']:
                if feature not in features:
                    features[feature] = 'unknown'
            
            # Get pattern predictions
            result = self.pattern_classifier.predict(features)
            
            # Ensure proper response format
            response = {
                'pattern_score': result.get('pattern_score', 0.5),
                'primary_patterns': result.get('primary_patterns', []),
                'secondary_patterns': result.get('secondary_patterns', []),
                'all_patterns': result.get('all_patterns', []),
                'category_scores': result.get('category_scores', {}),
                'pattern_insights': result.get('pattern_insights', [])
            }
            
            # Add pattern recommendations
            response['recommendations'] = self._generate_recommendations(result)
            
            return response
            
        except Exception as e:
            logger.error(f"Pattern prediction failed: {e}")
            return {
                'pattern_score': 0.5,
                'primary_patterns': [],
                'all_patterns': [],
                'error': str(e)
            }
    
    def _generate_recommendations(self, pattern_result: Dict) -> List[str]:
        """Generate recommendations based on patterns"""
        recommendations = []
        
        primary_patterns = pattern_result.get('primary_patterns', [])
        if not primary_patterns:
            return ["Focus on establishing clearer strategic patterns"]
        
        # Get top pattern
        top_pattern = primary_patterns[0]
        pattern_name = top_pattern.get('pattern', '')
        confidence = top_pattern.get('confidence', 0)
        
        if confidence > 0.8:
            recommendations.append(f"Strong {pattern_name} pattern - double down on this strategy")
        elif confidence > 0.6:
            recommendations.append(f"Emerging {pattern_name} pattern - reinforce key elements")
        else:
            recommendations.append(f"Weak {pattern_name} signals - consider strategic pivots")
        
        # Add category-specific recommendations
        category_scores = pattern_result.get('category_scores', {})
        if category_scores:
            top_category = max(category_scores.items(), key=lambda x: x[1])
            if top_category[1] > 0.7:
                recommendations.append(f"Excel in {top_category[0].replace('_', ' ')} - leverage this strength")
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def get_pattern_details(self, pattern_name: str) -> Dict:
        """Get details for a specific pattern"""
        try:
            # This would call the pattern classifier's method
            if hasattr(self.pattern_classifier, 'get_pattern_details'):
                return self.pattern_classifier.get_pattern_details(pattern_name)
            else:
                # Fallback implementation
                return {
                    'name': pattern_name,
                    'description': f'Pattern {pattern_name}',
                    'success_rate': 0.65,
                    'key_metrics': []
                }
        except Exception as e:
            logger.error(f"Failed to get pattern details: {e}")
            return {}
