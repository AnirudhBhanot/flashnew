"""
Response Transformer for Frontend Compatibility
Transforms backend responses to match frontend expectations
"""

from typing import Dict, List, Any
from datetime import datetime


class ResponseTransformer:
    """Transform API responses to match frontend expectations"""
    
    @staticmethod
    def transform_for_frontend(backend_response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform backend response to frontend format"""
        
        # Start with base response
        prob = backend_response.get('success_probability', 0.5)
        confidence = backend_response.get('confidence_score', 0.7)
        
        # Calculate enhanced verdict
        if prob >= 0.85:
            verdict = "STRONG PASS"
            strength_level = "Very Strong"
            risk_level = "Low Risk"
        elif prob >= 0.7:
            verdict = "PASS"
            strength_level = "Strong"
            risk_level = "Low Risk"
        elif prob >= 0.6:
            verdict = "CONDITIONAL PASS"
            strength_level = "Moderate"
            risk_level = "Medium Risk"
        elif prob >= 0.5:
            verdict = "CONDITIONAL PASS"
            strength_level = "Weak"
            risk_level = "Medium Risk"
        elif prob >= 0.3:
            verdict = "FAIL"
            strength_level = "Weak"
            risk_level = "High Risk"
        else:
            verdict = "STRONG FAIL"
            strength_level = "Very Weak"
            risk_level = "Critical Risk"
        
        # Get pillar scores
        pillar_scores = backend_response.get('pillar_scores', {
            'capital': 0.5,
            'advantage': 0.5,
            'market': 0.5,
            'people': 0.5
        })
        
        # Find pillars below threshold
        below_threshold = [
            pillar.capitalize() for pillar, score in pillar_scores.items()
            if score < 0.4  # 40% threshold
        ]
        
        # Generate insights based on scores
        key_insights = []
        critical_failures = []
        success_factors = []
        growth_indicators = []
        
        # Analyze pillars for insights
        for pillar, score in pillar_scores.items():
            if score >= 0.7:
                success_factors.append(f"Strong {pillar.capitalize()} foundation")
                growth_indicators.append(f"{pillar.capitalize()} metrics trending positive")
            elif score < 0.3:
                critical_failures.append(f"{pillar.capitalize()} metrics need immediate attention")
        
        # Add pattern insights if available
        pattern_analysis = backend_response.get('pattern_analysis', {})
        if pattern_analysis:
            primary_patterns = pattern_analysis.get('primary_patterns', [])
            if primary_patterns:
                key_insights.append(f"Exhibits {primary_patterns[0].get('name', 'Unknown')} pattern")
            
            # Add pattern insights
            pattern_insights = pattern_analysis.get('pattern_insights', [])
            key_insights.extend(pattern_insights[:3])  # Top 3 insights
        
        # Add general insights based on probability
        if prob >= 0.7:
            key_insights.append("Strong potential for successful fundraising")
            success_factors.append("Model consensus indicates high confidence")
        elif prob >= 0.5:
            key_insights.append("Moderate potential with room for improvement")
        else:
            key_insights.append("Significant challenges identified")
            critical_failures.append("Below investment threshold")
        
        # Ensure we have content for all arrays
        if not key_insights:
            key_insights = ["Comprehensive analysis complete"]
        if not critical_failures and prob < 0.5:
            critical_failures = ["Multiple areas need improvement"]
        if not success_factors and prob >= 0.5:
            success_factors = ["Positive indicators present"]
        if not growth_indicators:
            growth_indicators = ["Growth metrics being analyzed"]
        
        # Build risk factors from interpretation
        risk_factors = []
        interpretation = backend_response.get('interpretation', {})
        if interpretation.get('risks'):
            risk_factors = interpretation['risks']
        elif prob < 0.5:
            risk_factors = [
                "Below average success probability",
                "Key metrics need improvement",
                "Consider strategic pivots"
            ]
        
        # Transform pattern analysis for frontend
        frontend_pattern_analysis = None
        if pattern_analysis and pattern_analysis.get('primary_patterns'):
            primary = pattern_analysis['primary_patterns'][0]
            frontend_pattern_analysis = {
                'primary_pattern': {
                    'name': primary.get('name', 'Unknown Pattern'),
                    'confidence': primary.get('score', 0.5),
                    'expected_success_rate': 0.6 + (primary.get('score', 0.5) * 0.3),  # Estimate
                    'similar_companies': ['Company A', 'Company B', 'Company C'],  # Placeholder
                    'recommendations': pattern_analysis.get('pattern_insights', [
                        'Follow successful patterns in your category',
                        'Focus on key differentiators'
                    ])[:3]
                },
                'pattern_insights': pattern_analysis.get('pattern_insights', [])
            }
        
        # Build complete frontend response
        frontend_response = {
            # Core fields
            'success_probability': prob,
            'confidence_score': confidence,
            'verdict': verdict,
            'strength': strength_level,  # Some components use 'strength'
            'strength_level': strength_level,  # Others use 'strength_level'
            'risk_level': risk_level,
            
            # Confidence interval
            'confidence_interval': {
                'lower': max(0, prob - (1 - confidence) * 0.2),
                'upper': min(1, prob + (1 - confidence) * 0.2)
            },
            'confidenceInterval': {  # Duplicate for compatibility
                'lower': max(0, prob - (1 - confidence) * 0.2),
                'upper': min(1, prob + (1 - confidence) * 0.2)
            },
            
            # Pillar scores
            'pillar_scores': pillar_scores,
            'below_threshold': below_threshold,
            
            # Insights and factors
            'key_insights': key_insights,
            'critical_failures': critical_failures,
            'success_factors': success_factors,
            'risk_factors': risk_factors if risk_factors else ["No significant risks identified"],
            'growth_indicators': growth_indicators,
            
            # Pattern analysis
            'pattern_analysis': frontend_pattern_analysis,
            'pattern_insights': pattern_analysis.get('pattern_insights', []) if pattern_analysis else [],
            
            # Model information
            'model_predictions': backend_response.get('model_predictions', {}),
            'model_consensus': backend_response.get('model_agreement', confidence),
            'model_contributions': backend_response.get('model_predictions', {}),
            'modelConfidence': confidence,  # For ConfidenceVisualization component
            
            # Temporal predictions (placeholder for now)
            'temporal_predictions': {
                'short_term': prob + 0.05,  # Slight optimism
                'medium_term': prob + 0.1,
                'long_term': prob + 0.15
            },
            
            # DNA pattern (placeholder)
            'dna_pattern': {
                'pattern_type': primary_patterns[0].get('name', 'Balanced Growth') if pattern_analysis and pattern_analysis.get('primary_patterns') else 'Balanced Growth'
            },
            
            # Metadata
            'processing_time_ms': backend_response.get('processing_time_ms', 0),
            'timestamp': backend_response.get('timestamp', datetime.now().isoformat()),
            'model_version': backend_response.get('model_version', 'unified_v4')
        }
        
        # Copy over any additional fields from backend
        for key, value in backend_response.items():
            if key not in frontend_response:
                frontend_response[key] = value
        
        return frontend_response