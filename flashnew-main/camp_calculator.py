#!/usr/bin/env python3
"""
CAMP Score Calculator - Research-based framework
Separate from ML predictions to maintain credibility
"""

import numpy as np
from typing import Dict, Any, Tuple
from feature_config import (
    CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, 
    PEOPLE_FEATURES, PRODUCT_FEATURES, STAGE_WEIGHTS
)

class CAMPCalculator:
    """Calculate CAMP scores based on research, not ML feature importance"""
    
    def __init__(self):
        # Research-based stage weights
        self.stage_weights = STAGE_WEIGHTS
        
        # Feature normalization rules
        self.normalization_rules = {
            'monetary': {
                'features': [
                    'total_capital_raised_usd', 'cash_on_hand_usd', 'monthly_burn_usd',
                    'tam_size_usd', 'sam_size_usd', 'som_size_usd', 'annual_revenue_run_rate'
                ],
                'method': 'log_scale',
                'range': (1000, 1e9)  # $1K to $1B
            },
            'percentage': {
                'features': [
                    'market_growth_rate_percent', 'user_growth_rate_percent',
                    'revenue_growth_rate_percent', 'gross_margin_percent',
                    'net_dollar_retention_percent', 'customer_concentration_percent',
                    'team_diversity_percent'
                ],
                'method': 'linear',
                'range': (-100, 200)
            },
            'score': {
                'features': [
                    'tech_differentiation_score', 'switching_cost_score',
                    'brand_strength_score', 'scalability_score',
                    'board_advisor_experience_score', 'competition_intensity'
                ],
                'method': 'linear',
                'range': (1, 5)
            },
            'ratio': {
                'features': ['ltv_cac_ratio', 'burn_multiple', 'dau_mau_ratio'],
                'method': 'custom'
            },
            'retention': {
                'features': ['product_retention_30d', 'product_retention_90d'],
                'method': 'linear',
                'range': (0, 100)
            }
        }
    
    def calculate_camp_scores(self, features: Dict[str, Any], funding_stage: str) -> Dict[str, float]:
        """
        Calculate CAMP scores using research-based weights
        
        Args:
            features: Startup features
            funding_stage: Current funding stage
            
        Returns:
            Dictionary with camp scores and analysis
        """
        # Normalize features first
        normalized = self._normalize_features(features)
        
        # Calculate raw scores for each pillar
        raw_scores = {
            'capital': self._calculate_pillar_score(normalized, CAPITAL_FEATURES),
            'advantage': self._calculate_pillar_score(normalized, ADVANTAGE_FEATURES),
            'market': self._calculate_pillar_score(normalized, MARKET_FEATURES),
            'people': self._calculate_pillar_score(normalized, PEOPLE_FEATURES)
        }
        
        # Get stage-specific weights
        stage_key = funding_stage.lower().replace('-', '_')
        if stage_key not in self.stage_weights:
            stage_key = 'seed'  # Default to seed if unknown
        
        weights = self.stage_weights[stage_key]
        
        # Calculate weighted scores
        weighted_scores = {}
        total_weighted = 0
        
        for pillar, raw_score in raw_scores.items():
            weight = weights.get(pillar, 0.25)
            weighted_score = raw_score * weight
            weighted_scores[pillar] = weighted_score
            total_weighted += weighted_score
        
        # Return comprehensive results
        return {
            'raw_scores': raw_scores,
            'stage_weights': weights,
            'weighted_scores': weighted_scores,
            'overall_score': total_weighted,
            'funding_stage': funding_stage,
            'stage_focus': self._get_stage_focus(weights)
        }
    
    def _normalize_features(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Normalize all features to 0-1 scale"""
        normalized = {}
        
        for feature, value in features.items():
            if value is None:
                normalized[feature] = 0.5  # Default for missing
                continue
            
            # Find normalization rule
            norm_method = None
            for rule_name, rule in self.normalization_rules.items():
                if feature in rule['features']:
                    norm_method = rule['method']
                    norm_range = rule.get('range', (0, 1))
                    break
            
            if norm_method == 'log_scale':
                # Logarithmic scaling for monetary values
                if value > 0:
                    normalized[feature] = np.clip(
                        np.log10(value + 1) / np.log10(norm_range[1] + 1), 0, 1
                    )
                else:
                    normalized[feature] = 0
            
            elif norm_method == 'linear':
                # Linear scaling
                min_val, max_val = norm_range
                normalized[feature] = np.clip(
                    (value - min_val) / (max_val - min_val), 0, 1
                )
            
            elif norm_method == 'custom':
                # Custom handling for specific features
                if feature == 'ltv_cac_ratio':
                    normalized[feature] = np.clip(value / 5, 0, 1)  # 5+ is excellent
                elif feature == 'burn_multiple':
                    normalized[feature] = np.clip(1 - (value / 10), 0, 1)  # Lower is better
                elif feature == 'dau_mau_ratio':
                    normalized[feature] = np.clip(value, 0, 1)  # Already 0-1
                else:
                    normalized[feature] = 0.5
            
            else:
                # Default: assume boolean or already normalized
                try:
                    # Handle boolean features
                    if isinstance(value, bool):
                        normalized[feature] = 1.0 if value else 0.0
                    elif feature in ['has_debt', 'network_effects_present', 'has_data_moat', 
                                     'regulatory_advantage_present', 'key_person_dependency']:
                        # These are boolean features
                        normalized[feature] = 1.0 if value else 0.0
                    else:
                        # Try to convert to float and clip to 0-1
                        normalized[feature] = np.clip(float(value), 0, 1)
                except:
                    normalized[feature] = 0.5
        
        return normalized
    
    def _calculate_pillar_score(self, normalized: Dict[str, float], pillar_features: list) -> float:
        """Calculate average score for a CAMP pillar"""
        scores = []
        for feature in pillar_features:
            if feature in normalized:
                # Ensure value is between 0 and 1
                value = normalized[feature]
                if isinstance(value, (int, float)):
                    value = np.clip(value, 0, 1)
                else:
                    value = 0.5
                scores.append(value)
        
        return np.mean(scores) if scores else 0.5
    
    def _get_stage_focus(self, weights: Dict[str, float]) -> str:
        """Determine primary focus for the stage"""
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_weights[0][0]
        
        focus_descriptions = {
            'people': "Team and execution capability",
            'advantage': "Product differentiation and moats",
            'market': "Market opportunity and traction",
            'capital': "Financial efficiency and scalability"
        }
        
        return focus_descriptions.get(primary, "Balanced approach")

# Global instance
camp_calculator = CAMPCalculator()

def calculate_camp_scores(features: Dict[str, Any], funding_stage: str = 'seed') -> Dict[str, float]:
    """Main function to calculate CAMP scores"""
    return camp_calculator.calculate_camp_scores(features, funding_stage)
