"""
Comprehensive data validation for startup predictions
"""
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class DataValidator:
    """Comprehensive validation for startup data beyond basic type checking"""
    
    def __init__(self):
        self.validation_rules = self._define_validation_rules()
        self.cross_field_rules = self._define_cross_field_rules()
    
    def _define_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Define validation rules for each field"""
        return {
            # Capital metrics
            "total_capital_raised_usd": {
                "min": 0,
                "max": 10_000_000_000,  # $10B max
                "required": False,
                "type": "numeric"
            },
            "cash_on_hand_usd": {
                "min": 0,
                "max": 1_000_000_000,  # $1B max
                "required": False,
                "type": "numeric"
            },
            "monthly_burn_usd": {
                "min": 0,
                "max": 100_000_000,  # $100M/month max
                "required": False,
                "type": "numeric"
            },
            "runway_months": {
                "min": 0,
                "max": 120,  # 10 years max
                "required": False,
                "type": "numeric"
            },
            "burn_multiple": {
                "min": -10,
                "max": 100,
                "required": False,
                "type": "numeric"
            },
            
            # Market metrics
            "tam_size_usd": {
                "min": 0,  # Allow 0 for now, will validate in business logic
                "max": 10_000_000_000_000,  # $10T max
                "required": False,
                "type": "numeric"
            },
            "sam_size_usd": {
                "min": 100_000,  # $100K minimum
                "max": 1_000_000_000_000,  # $1T max
                "required": False,
                "type": "numeric"
            },
            "som_size_usd": {
                "min": 10_000,  # $10K minimum
                "max": 100_000_000_000,  # $100B max
                "required": False,
                "type": "numeric"
            },
            "market_growth_rate_percent": {
                "min": -50,
                "max": 500,
                "required": False,
                "type": "numeric"
            },
            
            # Team metrics
            "founders_count": {
                "min": 1,
                "max": 10,
                "required": False,
                "type": "numeric"
            },
            "team_size_full_time": {
                "min": 1,
                "max": 100000,
                "required": False,
                "type": "numeric"
            },
            "advisors_count": {
                "min": 0,
                "max": 50,
                "required": False,
                "type": "numeric"
            },
            "years_experience_avg": {
                "min": 0,
                "max": 50,
                "required": False,
                "type": "numeric"
            },
            "domain_expertise_years_avg": {
                "min": 0,
                "max": 50,
                "required": False,
                "type": "numeric"
            },
            
            # Growth metrics
            "customer_count": {
                "min": 0,
                "max": 1_000_000_000,  # 1B customers max
                "required": False,
                "type": "numeric"
            },
            "user_growth_rate_percent": {
                "min": -100,
                "max": 10000,  # 100x growth
                "required": False,
                "type": "numeric"
            },
            "revenue_growth_rate_percent": {
                "min": -100,
                "max": 10000,
                "required": False,
                "type": "numeric"
            },
            
            # Product metrics
            "product_retention_30d": {
                "min": 0,
                "max": 1,
                "required": False,
                "type": "numeric"
            },
            "product_retention_90d": {
                "min": 0,
                "max": 1,
                "required": False,
                "type": "numeric"
            },
            "dau_mau_ratio": {
                "min": 0,
                "max": 1,
                "required": False,
                "type": "numeric"
            },
            "ltv_cac_ratio": {
                "min": 0,
                "max": 100,
                "required": False,
                "type": "numeric"
            },
            
            # Score fields (1-5 scale)
            "tech_differentiation_score": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            "switching_cost_score": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            "brand_strength_score": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            "scalability_score": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            "board_advisor_experience_score": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            "competition_intensity": {
                "min": 1,
                "max": 5,
                "required": False,
                "type": "numeric",
                "integer": True
            },
            
            # Percentage fields (0-100)
            "customer_concentration_percent": {
                "min": 0,
                "max": 100,
                "required": False,
                "type": "numeric"
            },
            "team_diversity_percent": {
                "min": 0,
                "max": 100,
                "required": False,
                "type": "numeric"
            },
            "gross_margin_percent": {
                "min": -100,
                "max": 100,
                "required": False,
                "type": "numeric"
            },
            "net_dollar_retention_percent": {
                "min": 0,
                "max": 300,  # Can exceed 100%
                "required": False,
                "type": "numeric"
            },
            
            # Enum fields
            "funding_stage": {
                "values": ["pre_seed", "seed", "series_a", "series_b", "series_c", "growth"],
                "required": False,
                "type": "enum"
            },
            "product_stage": {
                "values": ["concept", "prototype", "mvp", "beta", "launched", "growth", "mature", "idea", "research", "development", "alpha", "live", "scaling"],
                "required": False,
                "type": "enum"
            },
            "sector": {
                "values": ["saas", "fintech", "healthtech", "edtech", "ecommerce", "marketplace", 
                          "deeptech", "consumer", "enterprise", "proptech", "biotech", "agtech",
                          "cleantech", "cybersecurity", "gaming", "logistics", "insurtech", 
                          "legaltech", "hrtech", "other", "healthcare", "ai-ml", "artificial-intelligence",
                          "machine-learning", "blockchain", "crypto", "real-estate", "transportation",
                          "clean-tech", "deep-tech", "deep_tech"],
                "required": False,
                "type": "enum"
            },
            "investor_tier_primary": {
                "values": ["tier_1", "tier_2", "tier_3", "angel", "none", "university", "corporate", "government"],
                "required": False,
                "type": "enum"
            }
        }
    
    def _define_cross_field_rules(self) -> List[Dict[str, Any]]:
        """Define validation rules that involve multiple fields"""
        return [
            {
                "name": "runway_consistency",
                "fields": ["cash_on_hand_usd", "monthly_burn_usd", "runway_months"],
                "validator": self._validate_runway_consistency
            },
            {
                "name": "market_size_hierarchy",
                "fields": ["tam_size_usd", "sam_size_usd", "som_size_usd"],
                "validator": self._validate_market_hierarchy
            },
            {
                "name": "retention_consistency",
                "fields": ["product_retention_30d", "product_retention_90d"],
                "validator": self._validate_retention_consistency
            },
            {
                "name": "team_experience_logic",
                "fields": ["years_experience_avg", "domain_expertise_years_avg"],
                "validator": self._validate_experience_logic
            },
            {
                "name": "funding_stage_capital_consistency",
                "fields": ["funding_stage", "total_capital_raised_usd"],
                "validator": self._validate_funding_capital_consistency
            },
            {
                "name": "ltv_cac_revenue_consistency",
                "fields": ["ltv_cac_ratio", "customer_acquisition_cost", "annual_revenue_run_rate"],
                "validator": self._validate_ltv_cac_consistency
            }
        ]
    
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validate startup data comprehensively
        
        Returns:
            - is_valid: Boolean indicating if data is valid
            - errors: List of error messages
            - cleaned_data: Cleaned and validated data
        """
        errors = []
        warnings = []
        cleaned_data = {}
        
        # 1. Field-level validation
        for field, value in data.items():
            if field not in self.validation_rules:
                # Unknown field - just pass through
                cleaned_data[field] = value
                continue
            
            rule = self.validation_rules[field]
            field_errors, cleaned_value = self._validate_field(field, value, rule)
            
            if field_errors:
                errors.extend(field_errors)
            else:
                cleaned_data[field] = cleaned_value
        
        # 2. Cross-field validation
        for rule in self.cross_field_rules:
            # Check if all required fields are present
            if all(field in cleaned_data for field in rule["fields"]):
                rule_errors, rule_warnings = rule["validator"](cleaned_data)
                errors.extend(rule_errors)
                warnings.extend(rule_warnings)
        
        # 3. Business logic validation
        business_errors = self._validate_business_logic(cleaned_data)
        errors.extend(business_errors)
        
        is_valid = len(errors) == 0
        
        # Log warnings (non-blocking)
        for warning in warnings:
            logger.warning(f"Validation warning: {warning}")
        
        return is_valid, errors, cleaned_data
    
    def _validate_field(self, field: str, value: Any, rule: Dict[str, Any]) -> Tuple[List[str], Any]:
        """Validate a single field"""
        errors = []
        cleaned_value = value
        
        # Check if field is required
        if rule.get("required", False) and (value is None or value == ""):
            errors.append(f"{field} is required")
            return errors, None
        
        # Skip validation if value is None and not required
        if value is None:
            return errors, None
        
        # Type validation
        if rule["type"] == "numeric":
            try:
                cleaned_value = float(value)
                
                # Range validation
                if "min" in rule and cleaned_value < rule["min"]:
                    errors.append(f"{field} must be >= {rule['min']} (got {cleaned_value})")
                
                if "max" in rule and cleaned_value > rule["max"]:
                    errors.append(f"{field} must be <= {rule['max']} (got {cleaned_value})")
                
                # Integer validation
                if rule.get("integer", False) and not cleaned_value.is_integer():
                    errors.append(f"{field} must be an integer (got {cleaned_value})")
                    
            except (ValueError, TypeError):
                errors.append(f"{field} must be a number (got {type(value).__name__})")
        
        elif rule["type"] == "enum":
            if value not in rule["values"]:
                errors.append(f"{field} must be one of {rule['values']} (got {value})")
        
        return errors, cleaned_value
    
    def _validate_runway_consistency(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate runway calculation consistency"""
        errors = []
        warnings = []
        
        cash = data.get("cash_on_hand_usd")
        burn = data.get("monthly_burn_usd")
        runway = data.get("runway_months")
        
        if cash is not None and burn is not None and burn > 0 and runway is not None:
            calculated_runway = cash / burn
            
            # Allow 20% tolerance
            if abs(calculated_runway - runway) > max(2, runway * 0.2):
                warnings.append(
                    f"Runway inconsistency: {runway} months reported, "
                    f"but {calculated_runway:.1f} months calculated from cash/burn"
                )
        
        return errors, warnings
    
    def _validate_market_hierarchy(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate TAM > SAM > SOM"""
        errors = []
        warnings = []
        
        tam = data.get("tam_size_usd")
        sam = data.get("sam_size_usd")
        som = data.get("som_size_usd")
        
        # Skip validation if TAM is 0 (user hasn't entered market data yet)
        if tam == 0:
            if sam != 0 or som != 0:
                warnings.append("TAM is 0 but SAM/SOM have values - please enter TAM first")
            return errors, warnings
        
        if tam is not None and sam is not None and sam > tam:
            errors.append(f"SAM (${sam:,.0f}) cannot be larger than TAM (${tam:,.0f})")
        
        if sam is not None and som is not None and som > sam:
            errors.append(f"SOM (${som:,.0f}) cannot be larger than SAM (${sam:,.0f})")
        
        if tam is not None and som is not None and som > tam:
            errors.append(f"SOM (${som:,.0f}) cannot be larger than TAM (${tam:,.0f})")
        
        return errors, warnings
    
    def _validate_retention_consistency(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate that 90d retention <= 30d retention"""
        errors = []
        warnings = []
        
        retention_30d = data.get("product_retention_30d")
        retention_90d = data.get("product_retention_90d")
        
        if retention_30d is not None and retention_90d is not None:
            if retention_90d > retention_30d:
                errors.append(
                    f"90-day retention ({retention_90d:.1%}) cannot be higher than "
                    f"30-day retention ({retention_30d:.1%})"
                )
        
        return errors, warnings
    
    def _validate_experience_logic(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate that domain expertise <= total experience"""
        errors = []
        warnings = []
        
        total_exp = data.get("years_experience_avg")
        domain_exp = data.get("domain_expertise_years_avg")
        
        if total_exp is not None and domain_exp is not None:
            if domain_exp > total_exp:
                warnings.append(
                    f"Domain expertise ({domain_exp} years) exceeds total experience "
                    f"({total_exp} years)"
                )
        
        return errors, warnings
    
    def _validate_funding_capital_consistency(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate funding stage matches capital raised"""
        errors = []
        warnings = []
        
        stage = data.get("funding_stage")
        capital = data.get("total_capital_raised_usd", 0)
        
        # Typical ranges by stage
        stage_ranges = {
            "pre_seed": (0, 1_000_000),
            "seed": (100_000, 5_000_000),
            "series_a": (2_000_000, 20_000_000),
            "series_b": (10_000_000, 50_000_000),
            "series_c": (30_000_000, 100_000_000),
            "growth": (50_000_000, float('inf'))
        }
        
        if stage in stage_ranges and capital > 0:
            min_cap, max_cap = stage_ranges[stage]
            if capital < min_cap * 0.5:  # Allow some flexibility
                warnings.append(
                    f"Capital raised (${capital:,.0f}) seems low for {stage} stage "
                    f"(typical: ${min_cap:,.0f}-${max_cap:,.0f})"
                )
            elif capital > max_cap * 2:  # Allow some flexibility
                warnings.append(
                    f"Capital raised (${capital:,.0f}) seems high for {stage} stage "
                    f"(typical: ${min_cap:,.0f}-${max_cap:,.0f})"
                )
        
        return errors, warnings
    
    def _validate_ltv_cac_consistency(self, data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate LTV/CAC ratio makes sense"""
        errors = []
        warnings = []
        
        ltv_cac = data.get("ltv_cac_ratio")
        
        if ltv_cac is not None:
            if ltv_cac < 0:
                errors.append("LTV/CAC ratio cannot be negative")
            elif ltv_cac < 1:
                warnings.append(
                    f"LTV/CAC ratio of {ltv_cac:.2f} indicates negative unit economics"
                )
            elif ltv_cac > 20:
                warnings.append(
                    f"LTV/CAC ratio of {ltv_cac:.2f} seems unusually high"
                )
        
        return errors, warnings
    
    def _validate_business_logic(self, data: Dict[str, Any]) -> List[str]:
        """Additional business logic validations"""
        errors = []
        
        # Check for suspicious combinations
        stage = data.get("funding_stage")
        product_stage = data.get("product_stage")
        
        # Series B+ should not be at concept/prototype stage
        if stage in ["series_b", "series_c", "growth"] and product_stage in ["concept", "prototype"]:
            errors.append(
                f"Unusual: {stage} company still at {product_stage} stage"
            )
        
        # Growth stage checks
        if stage == "growth":
            revenue = data.get("annual_revenue_run_rate", 0)
            if revenue < 10_000_000:  # $10M ARR
                errors.append(
                    f"Growth stage companies typically have >$10M ARR (reported: ${revenue:,.0f})"
                )
        
        # Team size checks
        team_size = data.get("team_size_full_time", 0)
        capital = data.get("total_capital_raised_usd", 0)
        
        if team_size > 0 and capital > 0:
            capital_per_employee = capital / team_size
            if capital_per_employee < 10_000:  # Less than $10K per employee
                errors.append(
                    f"Unusually low capital per employee: ${capital_per_employee:,.0f}"
                )
        
        return errors


# Global validator instance
data_validator = DataValidator()