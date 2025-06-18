"""
Configuration Service for FLASH Platform
Provides dynamic configuration to frontend to eliminate hardcoded values
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum
import os
from datetime import datetime


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class ConfigService:
    """Centralized configuration service for all frontend values"""
    
    def __init__(self, environment: Optional[str] = None):
        self.environment = Environment(environment or os.getenv("ENVIRONMENT", "development"))
        self._config_cache = {}
        self._last_update = datetime.now()
    
    def get_business_logic_config(self) -> Dict[str, Any]:
        """Get all business logic thresholds and rules"""
        return {
            "score_thresholds": {
                "very_high": 0.8,
                "high": 0.7,
                "medium": 0.5,
                "low": 0.3,
                "very_low": 0.0
            },
            "risk_thresholds": {
                "runway_months_critical": 6,
                "runway_months_warning": 12,
                "burn_multiple_high": 2,
                "burn_multiple_critical": 3,
                "revenue_concentration_high": 0.3,
                "revenue_concentration_critical": 0.5,
                "churn_rate_high": 0.1,
                "churn_rate_critical": 0.15
            },
            "risk_indicator_positions": {
                "low": 12.5,
                "medium": 37.5,
                "high": 62.5,
                "critical": 87.5
            },
            "investment_thresholds": {
                "capital": 0.65,
                "advantage": 0.70,
                "market": 0.65,
                "people": 0.70
            },
            "consensus_thresholds": {
                "very_high": 0.8,
                "high": 0.6,
                "moderate": 0.4,
                "low": 0.0
            },
            "confidence_interval": {
                "default_lower_bound": 0.15,
                "default_upper_bound": 0.15
            },
            "verdict_config": {
                "STRONG PASS": {
                    "icon": "🚀",
                    "className": "verdict-strong-pass",
                    "threshold": 0.85
                },
                "PASS": {
                    "icon": "✅",
                    "className": "verdict-pass",
                    "threshold": 0.70
                },
                "CONDITIONAL PASS": {
                    "icon": "⚡",
                    "className": "verdict-conditional",
                    "threshold": 0.55
                },
                "FAIL": {
                    "icon": "⚠️",
                    "className": "verdict-fail",
                    "threshold": 0.40
                },
                "STRONG FAIL": {
                    "icon": "🔴",
                    "className": "verdict-strong-fail",
                    "threshold": 0.0
                }
            }
        }
    
    def get_model_performance_config(self) -> Dict[str, Any]:
        """Get model performance metrics and configuration"""
        return {
            "dna_analyzer": {
                "name": "DNA Pattern Analyzer",
                "accuracy": 0.730,
                "description": "Analyzes startup DNA patterns and growth genes"
            },
            "temporal_predictor": {
                "name": "Temporal Predictor",
                "accuracy": 0.734,
                "description": "Forecasts based on time-series patterns"
            },
            "industry_model": {
                "name": "Industry Specialist",
                "accuracy": 0.718,
                "description": "Industry-specific success patterns"
            },
            "ensemble_model": {
                "name": "Core Ensemble",
                "accuracy": 0.724,
                "description": "Core CAMP framework analysis"
            },
            "pattern_matcher": {
                "name": "Stage Hierarchical",
                "accuracy": 0.725,
                "description": "Stage-specific success factors"
            },
            "meta_learner": {
                "name": "Meta Pipeline",
                "accuracy": 0.727,
                "description": "Optimized meta-learning pipeline"
            },
            "overall_accuracy": 0.727,
            "dataset_size": "100,000",
            "last_updated": "2025-06-03"
        }
    
    def get_stage_weights_config(self) -> Dict[str, Any]:
        """Get stage-specific CAMP weights"""
        return {
            "pre_seed": {
                "capital": 0.20,
                "advantage": 0.20,
                "market": 0.20,
                "people": 0.40
            },
            "seed": {
                "capital": 0.25,
                "advantage": 0.25,
                "market": 0.25,
                "people": 0.25
            },
            "series_a": {
                "capital": 0.25,
                "advantage": 0.25,
                "market": 0.30,
                "people": 0.20
            },
            "series_b": {
                "capital": 0.40,
                "advantage": 0.25,
                "market": 0.20,
                "people": 0.15
            },
            "series_c": {
                "capital": 0.45,
                "advantage": 0.20,
                "market": 0.20,
                "people": 0.15
            }
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI-specific configuration (colors, animations, etc.)"""
        return {
            "colors": {
                "primary": "#007AFF",
                "success": "#00C851",
                "warning": "#FF8800",
                "danger": "#FF4444",
                "info": "#33B5E5",
                "dark": "#0A0A0C",
                "light": "#1A1A1F",
                "pattern_categories": {
                    "efficient_growth": "#00C851",
                    "high_burn_growth": "#FF8800",
                    "technical_innovation": "#33B5E5",
                    "market_driven": "#AA66CC",
                    "bootstrap_profitable": "#00C851",
                    "struggling_pivot": "#FF4444",
                    "vertical_specific": "#FFBB33"
                }
            },
            "animations": {
                "duration_fast": 0.2,
                "duration_normal": 0.6,
                "duration_slow": 1.0,
                "spring_stiffness": 200,
                "spring_damping": 20
            },
            "loading": {
                "min_duration": 3000,
                "max_duration": 8000,
                "messages": [
                    "Analyzing startup DNA patterns...",
                    "Running advanced ML models...",
                    "Evaluating CAMP framework metrics...",
                    "Processing temporal predictions...",
                    "Comparing with successful patterns...",
                    "Calculating risk assessments...",
                    "Finalizing investment analysis..."
                ]
            }
        }
    
    def get_test_data_config(self) -> Dict[str, Any]:
        """Get test data ranges and examples"""
        return {
            "ranges": {
                "revenue": {"min": 10000, "max": 10000000},
                "burn_rate": {"min": 50000, "max": 2000000},
                "runway_months": {"min": 3, "max": 36},
                "team_size": {"min": 2, "max": 200},
                "customer_count": {"min": 10, "max": 10000},
                "growth_rate": {"min": 0.05, "max": 0.5},
                "market_size": {"min": 100000000, "max": 50000000000}
            },
            "company_examples": {
                "saas": ["Slack", "Zoom", "Datadog", "Snowflake", "MongoDB"],
                "fintech": ["Stripe", "Square", "Plaid", "Robinhood", "Chime"],
                "healthtech": ["Oscar Health", "Ro", "Hims", "Forward", "One Medical"],
                "ecommerce": ["Warby Parker", "Allbirds", "Glossier", "Away", "Casper"],
                "marketplaces": ["Airbnb", "DoorDash", "Instacart", "Rover", "StockX"]
            },
            "sample_startups": {
                "high_potential": {
                    "name": "TechVenture AI",
                    "stage": "series_a",
                    "revenue": 2000000,
                    "growth_rate": 0.3,
                    "burn_rate": 500000,
                    "runway_months": 18
                },
                "moderate_potential": {
                    "name": "MarketFlow",
                    "stage": "seed",
                    "revenue": 500000,
                    "growth_rate": 0.15,
                    "burn_rate": 200000,
                    "runway_months": 12
                },
                "low_potential": {
                    "name": "LocalBiz",
                    "stage": "pre_seed",
                    "revenue": 50000,
                    "growth_rate": 0.05,
                    "burn_rate": 100000,
                    "runway_months": 6
                }
            }
        }
    
    def get_time_periods_config(self) -> Dict[str, Any]:
        """Get time period definitions"""
        return {
            "short_term_months": 12,
            "medium_term_months": 24,
            "long_term_months": 36,
            "analysis_window_months": 48
        }
    
    def get_default_values_config(self) -> Dict[str, Any]:
        """Get default values for missing data"""
        return {
            "success_probability": 0.5,
            "confidence_score": 0.7,
            "funding_stage": "seed",
            "revenue": 100000,
            "burn_rate": 100000,
            "runway_months": 12,
            "team_size": 5,
            "growth_rate": 0.1
        }
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration in one call"""
        return {
            "business_logic": self.get_business_logic_config(),
            "model_performance": self.get_model_performance_config(),
            "stage_weights": self.get_stage_weights_config(),
            "ui": self.get_ui_config(),
            "test_data": self.get_test_data_config(),
            "time_periods": self.get_time_periods_config(),
            "default_values": self.get_default_values_config(),
            "environment": self.environment.value,
            "last_updated": self._last_update.isoformat()
        }
    
    def get_config_by_category(self, category: str) -> Optional[Dict[str, Any]]:
        """Get configuration by specific category"""
        category_map = {
            "business_logic": self.get_business_logic_config,
            "model_performance": self.get_model_performance_config,
            "stage_weights": self.get_stage_weights_config,
            "ui": self.get_ui_config,
            "test_data": self.get_test_data_config,
            "time_periods": self.get_time_periods_config,
            "default_values": self.get_default_values_config
        }
        
        getter = category_map.get(category)
        return getter() if getter else None


# Singleton instance
config_service = ConfigService()