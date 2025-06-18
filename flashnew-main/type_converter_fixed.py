#!/usr/bin/env python3
"""
Fixed Type Converter - Maps frontend fields to canonical 45 features correctly
"""

import logging
from typing import Dict, Any
from feature_config import ALL_FEATURES

logger = logging.getLogger(__name__)


class TypeConverterFixed:
    """Fixed type converter with proper field mapping"""
    
    def __init__(self):
        # Map frontend field names to canonical feature names
        self.field_mapping = {
            # Direct mappings (same name)
            'total_capital_raised_usd': 'total_capital_raised_usd',
            'cash_on_hand_usd': 'cash_on_hand_usd',
            'monthly_burn_usd': 'monthly_burn_usd',
            'runway_months': 'runway_months',
            'burn_multiple': 'burn_multiple',
            'investor_tier_primary': 'investor_tier_primary',
            'has_debt': 'has_debt',
            
            'patent_count': 'patent_count',
            'network_effects_present': 'network_effects_present',
            'has_data_moat': 'has_data_moat',
            'regulatory_advantage_present': 'regulatory_advantage_present',
            'tech_differentiation_score': 'tech_differentiation_score',
            'switching_cost_score': 'switching_cost_score',
            'brand_strength_score': 'brand_strength_score',
            'scalability_score': 'scalability_score',
            
            'sector': 'sector',
            'tam_size_usd': 'tam_size_usd',
            'sam_size_usd': 'sam_size_usd',
            'som_size_usd': 'som_size_usd',
            'market_growth_rate_percent': 'market_growth_rate_percent',
            'customer_count': 'customer_count',
            'customer_concentration_percent': 'customer_concentration_percent',
            'user_growth_rate_percent': 'user_growth_rate_percent',
            'net_dollar_retention_percent': 'net_dollar_retention_percent',
            'competition_intensity': 'competition_intensity',
            'competitors_named_count': 'competitors_named_count',
            
            'founders_count': 'founders_count',
            'team_size_full_time': 'team_size_full_time',
            'years_experience_avg': 'years_experience_avg',
            'domain_expertise_years_avg': 'domain_expertise_years_avg',
            'prior_startup_experience_count': 'prior_startup_experience_count',
            'prior_successful_exits_count': 'prior_successful_exits_count',
            'board_advisor_experience_score': 'board_advisor_experience_score',
            'advisors_count': 'advisors_count',
            'team_diversity_percent': 'team_diversity_percent',
            'key_person_dependency': 'key_person_dependency',
            
            'product_stage': 'product_stage',
            'product_retention_30d': 'product_retention_30d',
            'product_retention_90d': 'product_retention_90d',
            'dau_mau_ratio': 'dau_mau_ratio',
            'annual_revenue_run_rate': 'annual_revenue_run_rate',
            'revenue_growth_rate_percent': 'revenue_growth_rate_percent',
            'gross_margin_percent': 'gross_margin_percent',
            'ltv_cac_ratio': 'ltv_cac_ratio',
            'funding_stage': 'funding_stage',
            
            # Alternative names from frontend
            'proprietary_tech': 'has_data_moat',  # Map to similar concept
            'switching_costs_high': 'switching_cost_score',  # Convert to score
            'technical_moat_score': 'tech_differentiation_score',
            'competitive_intensity_score': 'competition_intensity',
            'previous_startup_experience': 'prior_startup_experience_count',
            'ltv_to_cac_ratio': 'ltv_cac_ratio',
            'founders_experience_score': 'years_experience_avg',  # Map to years
            'team_domain_expertise_score': 'domain_expertise_years_avg',  # Map to years
            'board_strength_score': 'board_advisor_experience_score',
            'advisors_score': 'advisors_count',  # Map score to count
            'diversity_score': 'team_diversity_percent',  # Map score to percent
            'mrr_usd': 'annual_revenue_run_rate',  # Convert MRR to ARR
            'active_users': 'customer_count',  # Map users to customers
        }
        
        # Default values for missing features
        self.defaults = {
            'sector': 0,
            'investor_tier_primary': 0,
            'product_stage': 0,
            'funding_stage': 0,
            'has_debt': 0,
            'has_data_moat': 0,
            'network_effects_present': 0,
            'regulatory_advantage_present': 0,
            'key_person_dependency': 0,
            'som_size_usd': 0,  # Often missing
            'net_dollar_retention_percent': 100,  # Default to 100%
            'dau_mau_ratio': 0.1,  # Default engagement
            'product_retention_30d': 50,
            'product_retention_90d': 30,
        }
    
    def convert_frontend_to_backend(self, frontend_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert frontend data to canonical 45 features"""
        backend_data = {}
        
        # Initialize all features with defaults
        for feature in ALL_FEATURES:
            backend_data[feature] = self.defaults.get(feature, 0)
        
        # Map frontend fields to backend
        for frontend_field, value in frontend_data.items():
            if value is None:
                continue
                
            # Get canonical field name
            canonical_field = self.field_mapping.get(frontend_field)
            
            if canonical_field and canonical_field in ALL_FEATURES:
                # Special conversions
                if frontend_field == 'proprietary_tech' and isinstance(value, bool):
                    backend_data[canonical_field] = 1 if value else 0
                elif frontend_field == 'switching_costs_high' and isinstance(value, bool):
                    backend_data[canonical_field] = 5 if value else 2  # High or low score
                elif frontend_field == 'founders_experience_score':
                    backend_data[canonical_field] = value * 3  # Convert 1-5 to years (3-15)
                elif frontend_field == 'team_domain_expertise_score':
                    backend_data[canonical_field] = value * 2.5  # Convert 1-5 to years (2.5-12.5)
                elif frontend_field == 'advisors_score':
                    backend_data[canonical_field] = value * 2  # Convert 1-5 to count (2-10)
                elif frontend_field == 'diversity_score':
                    backend_data[canonical_field] = value * 20  # Convert 1-5 to percent (20-100)
                elif frontend_field == 'mrr_usd':
                    backend_data['annual_revenue_run_rate'] = value * 12  # MRR to ARR
                elif frontend_field == 'previous_startup_experience':
                    backend_data[canonical_field] = value  # Direct mapping
                else:
                    # Direct value assignment
                    backend_data[canonical_field] = value
        
        # Calculate SOM if missing but SAM exists
        if backend_data['som_size_usd'] == 0 and backend_data['sam_size_usd'] > 0:
            backend_data['som_size_usd'] = backend_data['sam_size_usd'] * 0.1  # 10% of SAM
        
        # Ensure boolean fields are 0/1
        boolean_fields = ['has_debt', 'has_data_moat', 'network_effects_present', 
                         'regulatory_advantage_present', 'key_person_dependency']
        for field in boolean_fields:
            if field in backend_data:
                backend_data[field] = 1 if backend_data[field] else 0
        
        # Log conversion
        logger.info(f"Converted {len(frontend_data)} frontend fields to {len(backend_data)} canonical features")
        
        # Count non-zero values
        non_zero = sum(1 for v in backend_data.values() if v != 0)
        logger.info(f"Non-zero features: {non_zero}/{len(ALL_FEATURES)}")
        
        return backend_data


if __name__ == "__main__":
    # Test the converter
    converter = TypeConverterFixed()
    
    test_data = {
        'total_capital_raised_usd': 1000000,
        'runway_months': 18,
        'proprietary_tech': True,
        'founders_experience_score': 4,
        'mrr_usd': 50000,
        'extra_field': 'ignored'
    }
    
    result = converter.convert_frontend_to_backend(test_data)
    print(f"Converted {len(result)} features")
    print("Sample conversions:")
    print(f"  MRR $50k → ARR: ${result.get('annual_revenue_run_rate', 0):,}")
    print(f"  Founders score 4 → Years: {result.get('years_experience_avg', 0)}")
    print(f"  Has data moat: {result.get('has_data_moat', 0)}")