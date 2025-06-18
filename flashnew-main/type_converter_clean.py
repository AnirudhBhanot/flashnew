"""
Type Converter for Frontend-Backend Data Alignment
Handles all necessary conversions for the unified system
"""

from typing import Dict, Any
import logging
from financial_calculator import FinancialCalculator
from feature_defaults import FeatureDefaults
from feature_config import ALL_FEATURES

logger = logging.getLogger(__name__)


class TypeConverter:
    """Convert frontend data types to backend expectations"""
    
    # Boolean fields that need conversion
    BOOLEAN_FIELDS = {
        'has_debt',
        'network_effects_present', 
        'has_data_moat',
        'regulatory_advantage_present',
        'key_person_dependency',
        'has_patents',
        'has_lead_investor',
        'has_notable_investors'
    }
    
    # Fields that might be missing and need defaults
    OPTIONAL_FIELDS = {
        'runway_months': 12.0,
        'burn_multiple': 2.0,
        'patent_count': 0,
        'debt_to_equity': 0.0
    }
    
    @staticmethod
    def convert_frontend_to_backend(data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert frontend data to backend format"""
        converted = data.copy()
        
        # Convert booleans to integers
        for field in TypeConverter.BOOLEAN_FIELDS:
            if field in converted:
                # Handle various boolean representations
                value = converted[field]
                if isinstance(value, bool):
                    converted[field] = 1 if value else 0
                elif isinstance(value, str):
                    converted[field] = 1 if value.lower() in ['true', 'yes', '1'] else 0
                elif value is None:
                    converted[field] = 0
        
        # Add defaults for optional fields
        for field, default in TypeConverter.OPTIONAL_FIELDS.items():
            if field not in converted or converted[field] is None:
                converted[field] = default
        
        # Remove frontend-only fields
        frontend_only = ['startup_name', 'hq_location', 'vertical']
        for field in frontend_only:
            converted.pop(field, None)
        
        # Ensure numeric fields are proper types
        numeric_fields = [
            'founding_year', 'team_size', 'num_funding_rounds',
            'time_to_market', 'product_launch_months', 'patent_count'
        ]
        for field in numeric_fields:
            if field in converted and converted[field] is not None:
                try:
                    converted[field] = int(converted[field])
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert {field} to int: {converted[field]}")
        
        # Ensure float fields
        float_fields = [
            'total_funding', 'burn_rate', 'revenue_growth_rate',
            'customer_retention_rate', 'tam_size', 'sam_percentage',
            'market_share', 'market_growth_rate', 'employees_from_top_companies',
            'technical_team_percentage', 'investor_concentration',
            'r_and_d_intensity', 'viral_coefficient', 'customer_acquisition_cost',
            'ltv_cac_ratio', 'runway_months', 'burn_multiple', 'debt_to_equity'
        ]
        for field in float_fields:
            if field in converted and converted[field] is not None:
                try:
                    converted[field] = float(converted[field])
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert {field} to float: {converted[field]}")
        
        # Ensure string fields are strings
        string_fields = ['investor_tier_primary', 'funding_stage']
        for field in string_fields:
            if field in converted and converted[field] is not None:
                converted[field] = str(converted[field])
        
        # Handle special conversions
        if 'investor_tier_primary' in converted:
            # Convert frontend format to backend
            tier_map = {
                'tier_1': 'tier_1',
                'tier_2': 'tier_2', 
                'tier_3': 'tier_3',
                'none': 'unknown',
                'angel': 'angel'
            }
            value = converted['investor_tier_primary'].lower()
            converted['investor_tier_primary'] = tier_map.get(value, value)
        
        if 'funding_stage' in converted:
            # Ensure lowercase with underscores
            converted['funding_stage'] = converted['funding_stage'].lower().replace(' ', '_')
        
        # Apply financial calculations
        converted = FinancialCalculator.apply_calculated_metrics(converted)
        
        # Apply smart defaults for missing features
        converted = FeatureDefaults.apply_defaults(converted)
        
        # Remove any extra fields that models don't expect
        expected_features = set(ALL_FEATURES)
        extra_fields = set(converted.keys()) - expected_features
        
        # Keep only expected features
        cleaned_data = {k: v for k, v in converted.items() if k in expected_features}
        
        if extra_fields:
            logger.info(f"Removed extra fields not expected by models: {extra_fields}")
        
        return cleaned_data