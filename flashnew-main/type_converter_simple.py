"""
Simple Type Converter for Frontend-Backend Data Alignment
Now that frontend sends complete data, we only need basic conversions
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TypeConverter:
    """Simple converter for frontend data to backend format"""
    
    # Boolean fields that need conversion
    BOOLEAN_FIELDS = {
        'has_debt',
        'network_effects_present', 
        'has_data_moat',
        'regulatory_advantage_present',
        'key_person_dependency'
    }
    
    # Fields to remove (frontend-only)
    FRONTEND_ONLY_FIELDS = {
        'startup_name',
        'hq_location', 
        'vertical'
    }
    
    @staticmethod
    def convert_frontend_to_backend(data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert frontend data to backend format"""
        converted = data.copy()
        
        # Convert booleans to integers
        for field in TypeConverter.BOOLEAN_FIELDS:
            if field in converted and converted[field] is not None:
                # Handle various boolean representations
                val = converted[field]
                if isinstance(val, bool):
                    converted[field] = 1 if val else 0
                elif isinstance(val, str):
                    converted[field] = 1 if val.lower() in ['true', '1', 'yes'] else 0
                elif isinstance(val, (int, float)):
                    converted[field] = 1 if val else 0
        
        # Remove frontend-only fields
        for field in TypeConverter.FRONTEND_ONLY_FIELDS:
            converted.pop(field, None)
        
        # Scale percentage fields that need different ranges
        if 'technology_score' in converted and converted['technology_score'] is not None:
            # Convert from 0-100 to 0-5 scale
            converted['technology_score'] = min(5, max(0, converted['technology_score'] / 20))
        
        if 'scalability_score' in converted and converted['scalability_score'] is not None:
            # Ensure it's an integer (1-5 scale)
            val = converted['scalability_score']
            if isinstance(val, float) and val < 1:
                # If it's 0-1 scale, convert to 1-5
                converted['scalability_score'] = int(val * 5) if val > 0 else 1
            else:
                converted['scalability_score'] = int(val)
        
        if 'investor_concentration' in converted and converted['investor_concentration'] is not None:
            # Convert from percentage to 0-1 scale
            if converted['investor_concentration'] > 1:
                converted['investor_concentration'] = converted['investor_concentration'] / 100
        
        # Add missing required fields with sensible defaults
        defaults = {
            'competition_score': 50,  # Medium competition
            'market_readiness_score': 70,  # Good market readiness
            'customer_retention_rate': 85,  # Good retention
            'operations_efficiency_score': 75,
            'user_engagement_score': 70,
            'nps_score': 30,  # Good NPS
            'traction_score': 65,
            'growth_efficiency_score': 70,
            'ltv_cac_ratio': 3.0,  # Healthy ratio
            'sales_cycle_days': 45,
            'gross_revenue_retention': 90,
            'logo_retention_rate': 85,
            'average_contract_value': 50000,
            'qualified_pipeline_value': 2000000
        }
        
        for field, default_value in defaults.items():
            if field not in converted:
                converted[field] = default_value
        
        # Handle competition_intensity conversion (number to string)
        if 'competition_intensity' in converted and converted['competition_intensity'] is not None:
            intensity_val = converted['competition_intensity']
            if isinstance(intensity_val, (int, float)):
                # Convert numeric values to string categories
                if intensity_val <= 2:
                    converted['competition_intensity'] = 'low'
                elif intensity_val <= 3:
                    converted['competition_intensity'] = 'medium'
                else:
                    converted['competition_intensity'] = 'high'
        
        # Ensure numeric fields are proper types
        for key, value in list(converted.items()):
            if value is not None and key not in ['funding_stage', 'investor_tier_primary', 'product_stage', 'sector', 'market_competition_level', 'competition_intensity']:
                try:
                    # Try to convert to float (works for both int and float)
                    converted[key] = float(value)
                except (ValueError, TypeError):
                    # Keep original value if conversion fails
                    pass
        
        # Log conversion summary
        logger.info(f"Converted {len(data)} fields to backend format")
        
        return converted