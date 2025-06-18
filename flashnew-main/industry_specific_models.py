#!/usr/bin/env python3
"""
Industry-Specific Models for FLASH Platform
Sector-based prediction with industry benchmarks and insights
"""
import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
import json
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class IndustryConfig:
    """Configuration for industry-specific models"""
    industries: List[str] = None
    industry_features: Dict[str, List[str]] = None
    industry_benchmarks: Dict[str, Dict[str, float]] = None
    
    def __post_init__(self):
        if self.industries is None:
            self.industries = [
                'SaaS', 'FinTech', 'HealthTech', 'E-commerce', 
                'AI/ML', 'BioTech', 'EdTech', 'CleanTech'
            ]
            
        if self.industry_features is None:
            self.industry_features = {
                'SaaS': [
                    'net_dollar_retention_percent',
                    'ltv_cac_ratio',
                    'gross_margin_percent',
                    'burn_multiple',
                    'annual_revenue_run_rate',
                    'customer_concentration_percent'
                ],
                'FinTech': [
                    'regulatory_advantage_present',
                    'has_data_moat',
                    'customer_count',
                    'brand_strength_score',
                    'gross_margin_percent',
                    'switching_cost_score'
                ],
                'HealthTech': [
                    'patent_count',
                    'regulatory_advantage_present',
                    'years_experience_avg',
                    'advisors_count',
                    'board_advisor_experience_score',
                    'tech_differentiation_score'
                ],
                'E-commerce': [
                    'gross_margin_percent',
                    'ltv_cac_ratio',
                    'customer_concentration_percent',
                    'scalability_score',
                    'brand_strength_score',
                    'user_growth_rate_percent'
                ],
                'AI/ML': [
                    'tech_differentiation_score',
                    'patent_count',
                    'has_data_moat',
                    'team_size_full_time',
                    'years_experience_avg',
                    'scalability_score'
                ],
                'BioTech': [
                    'patent_count',
                    'regulatory_advantage_present',
                    'years_experience_avg',
                    'board_advisor_experience_score',
                    'cash_on_hand_usd',
                    'runway_months'
                ],
                'EdTech': [
                    'user_growth_rate_percent',
                    'product_retention_30d',
                    'dau_mau_ratio',
                    'scalability_score',
                    'net_dollar_retention_percent',
                    'customer_count'
                ],
                'CleanTech': [
                    'patent_count',
                    'tech_differentiation_score',
                    'regulatory_advantage_present',
                    'market_growth_rate_percent',
                    'tam_size_usd',
                    'board_advisor_experience_score'
                ]
            }
            
        if self.industry_benchmarks is None:
            self.industry_benchmarks = {
                'SaaS': {
                    'gross_margin': 70,
                    'net_retention': 110,
                    'ltv_cac': 3.0,
                    'growth_rate': 100
                },
                'FinTech': {
                    'gross_margin': 50,
                    'customer_growth': 150,
                    'regulatory_score': 4.0,
                    'retention_30d': 0.8
                },
                'HealthTech': {
                    'patent_count': 5,
                    'experience_years': 15,
                    'regulatory_score': 4.5,
                    'runway_months': 24
                },
                'E-commerce': {
                    'gross_margin': 40,
                    'ltv_cac': 2.5,
                    'growth_rate': 150,
                    'retention_30d': 0.6
                },
                'AI/ML': {
                    'tech_score': 4.5,
                    'patent_count': 3,
                    'team_size': 20,
                    'experience_years': 10
                },
                'BioTech': {
                    'patent_count': 10,
                    'runway_months': 36,
                    'experience_years': 20,
                    'regulatory_score': 4.0
                },
                'EdTech': {
                    'retention_30d': 0.7,
                    'dau_mau': 0.4,
                    'growth_rate': 200,
                    'net_retention': 105
                },
                'CleanTech': {
                    'patent_count': 8,
                    'tech_score': 4.0,
                    'market_growth': 30,
                    'experience_years': 15
                }
            }


class IndustrySpecificModel:
    """
    Industry-specific prediction model with sector expertise
    Provides benchmarking and industry-tailored insights
    """
    
    def __init__(self, config: Optional[IndustryConfig] = None):
        self.config = config or IndustryConfig()
        self.models = {}
        self.general_model = None
        self.is_loaded = False
        self.industry_classifier = IndustryClassifier()
        
    def load(self, model_path: Union[str, Path]) -> bool:
        """
        Load industry-specific models from disk
        
        Args:
            model_path: Path to model directory
            
        Returns:
            bool: True if successful
        """
        try:
            model_path = Path(model_path)
            
            # Try to load the complete industry model
            industry_file = model_path / 'industry_specific_model.pkl'
            if industry_file.exists():
                logger.info(f"Loading industry model from {industry_file}")
                loaded_model = joblib.load(industry_file)
                
                # Extract industry models if they exist
                if hasattr(loaded_model, 'industry_models'):
                    self.models = loaded_model.industry_models
                    if hasattr(loaded_model, 'general_model'):
                        self.general_model = loaded_model.general_model
                    logger.info(f"Loaded {len(self.models)} industry models")
                else:
                    # Use as general model for all industries
                    self.general_model = loaded_model
                    logger.info("Using single model for all industries")
            else:
                # Try to load individual industry models
                loaded_count = 0
                for industry in self.config.industries:
                    industry_key = industry.lower().replace('/', '_')
                    model_file = model_path / f'{industry_key}_model.pkl'
                    
                    if model_file.exists():
                        self.models[industry] = joblib.load(model_file)
                        loaded_count += 1
                        logger.info(f"Loaded {industry} model")
                
                # Load general model for other industries
                general_file = model_path / 'general_industry_model.pkl'
                if general_file.exists():
                    self.general_model = joblib.load(general_file)
                    logger.info("Loaded general industry model")
                    
                if loaded_count == 0 and self.general_model is None:
                    logger.error("No industry models found")
                    return False
                    
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading industry models: {str(e)}")
            return False
    
    def predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Make industry-specific predictions
        
        Args:
            features: DataFrame with startup features
            
        Returns:
            Dictionary with predictions and analysis
        """
        if not self.is_loaded:
            logger.warning("Industry models not loaded, returning default predictions")
            return self._get_default_predictions(features)
        
        try:
            # Determine industry
            industry = self._get_industry(features)
            
            # Get prediction
            prediction_result = self._predict_for_industry(features, industry)
            
            # Benchmark analysis
            benchmark_analysis = self._benchmark_against_industry(features, industry)
            
            # Generate insights
            insights = self._generate_industry_insights(
                features, industry, prediction_result, benchmark_analysis
            )
            
            # Industry-specific recommendations
            recommendations = self._generate_recommendations(
                industry, prediction_result['probability'], benchmark_analysis
            )
            
            return {
                'prediction': prediction_result['prediction'],
                'probability': prediction_result['probability'],
                'industry': industry,
                'industry_confidence': prediction_result.get('confidence', 0.8),
                'benchmark_analysis': benchmark_analysis,
                'insights': insights,
                'recommendations': recommendations,
                'peer_comparison': self._get_peer_comparison(features, industry)
            }
            
        except Exception as e:
            logger.error(f"Error in industry prediction: {str(e)}")
            return self._get_default_predictions(features)
    
    def _get_industry(self, features: pd.DataFrame) -> str:
        """Determine the industry/sector of the startup"""
        if 'sector' in features.columns:
            sector = features['sector'].iloc[0]
            
            # Map sector to standard industry
            sector_mapping = {
                'saas': 'SaaS',
                'fintech': 'FinTech',
                'healthcare': 'HealthTech',
                'healthtech': 'HealthTech',
                'ecommerce': 'E-commerce',
                'e-commerce': 'E-commerce',
                'ai': 'AI/ML',
                'ml': 'AI/ML',
                'biotech': 'BioTech',
                'edtech': 'EdTech',
                'cleantech': 'CleanTech',
                'enterprise': 'SaaS',
                'consumer': 'E-commerce'
            }
            
            normalized = sector.lower().replace('-', '').replace(' ', '')
            if normalized in sector_mapping:
                return sector_mapping[normalized]
            
            # Use classifier if mapping not found
            return self.industry_classifier.classify(features)
        else:
            # Use feature-based classification
            return self.industry_classifier.classify(features)
    
    def _predict_for_industry(self, features: pd.DataFrame, 
                             industry: str) -> Dict[str, Any]:
        """Make prediction using industry-specific model"""
        # Get industry-specific features
        industry_features = self.config.industry_features.get(industry, [])
        available_features = [f for f in industry_features if f in features.columns]
        
        if industry in self.models:
            # Use industry-specific model
            model = self.models[industry]
            if available_features:
                model_features = features[available_features]
            else:
                model_features = features
                
            try:
                probability = model.predict_proba(model_features)[0, 1]
                prediction = int(probability >= 0.5)
                confidence = 0.9  # High confidence with specific model
            except Exception as e:
                logger.error(f"Error with {industry} model: {e}")
                probability = 0.5
                prediction = 0
                confidence = 0.5
        else:
            # Use general model
            if self.general_model is not None:
                try:
                    probability = self.general_model.predict_proba(features)[0, 1]
                    prediction = int(probability >= 0.5)
                    confidence = 0.7  # Lower confidence with general model
                except:
                    probability = 0.5
                    prediction = 0
                    confidence = 0.5
            else:
                probability = 0.5
                prediction = 0
                confidence = 0.3
        
        return {
            'prediction': prediction,
            'probability': float(probability),
            'confidence': confidence
        }
    
    def _benchmark_against_industry(self, features: pd.DataFrame, 
                                   industry: str) -> Dict[str, Any]:
        """Benchmark startup against industry standards"""
        benchmarks = self.config.industry_benchmarks.get(industry, {})
        analysis = {
            'overall_score': 0,
            'metrics': {},
            'strengths': [],
            'weaknesses': []
        }
        
        scores = []
        
        # Gross margin benchmark
        if 'gross_margin' in benchmarks and 'gross_margin_percent' in features.columns:
            actual = features['gross_margin_percent'].iloc[0]
            benchmark = benchmarks['gross_margin']
            score = min(actual / benchmark, 2.0) if benchmark > 0 else 1.0
            scores.append(score)
            
            analysis['metrics']['gross_margin'] = {
                'actual': actual,
                'benchmark': benchmark,
                'score': score
            }
            
            if score >= 1.2:
                analysis['strengths'].append(f"Gross margin {actual}% exceeds industry average")
            elif score < 0.8:
                analysis['weaknesses'].append(f"Gross margin below industry standard")
        
        # Growth rate benchmark
        growth_keys = ['growth_rate', 'customer_growth']
        for key in growth_keys:
            if key in benchmarks:
                if key == 'growth_rate' and 'revenue_growth_rate_percent' in features.columns:
                    actual = features['revenue_growth_rate_percent'].iloc[0]
                elif key == 'customer_growth' and 'user_growth_rate_percent' in features.columns:
                    actual = features['user_growth_rate_percent'].iloc[0]
                else:
                    continue
                    
                benchmark = benchmarks[key]
                score = min(actual / benchmark, 2.0) if benchmark > 0 else 1.0
                scores.append(score)
                
                analysis['metrics'][key] = {
                    'actual': actual,
                    'benchmark': benchmark,
                    'score': score
                }
                
                if score >= 1.5:
                    analysis['strengths'].append(f"Exceptional growth rate: {actual}%")
                elif score < 0.5:
                    analysis['weaknesses'].append(f"Growth rate significantly below industry")
        
        # LTV/CAC benchmark
        if 'ltv_cac' in benchmarks and 'ltv_cac_ratio' in features.columns:
            actual = features['ltv_cac_ratio'].iloc[0]
            benchmark = benchmarks['ltv_cac']
            score = min(actual / benchmark, 2.0) if benchmark > 0 else 1.0
            scores.append(score)
            
            analysis['metrics']['ltv_cac'] = {
                'actual': actual,
                'benchmark': benchmark,
                'score': score
            }
            
            if score >= 1.0:
                analysis['strengths'].append(f"Strong unit economics (LTV/CAC: {actual:.1f})")
            elif score < 0.7:
                analysis['weaknesses'].append("Unit economics need improvement")
        
        # Calculate overall score
        if scores:
            analysis['overall_score'] = np.mean(scores)
        else:
            analysis['overall_score'] = 0.5
        
        # Industry percentile
        analysis['industry_percentile'] = self._calculate_percentile(
            analysis['overall_score']
        )
        
        return analysis
    
    def _calculate_percentile(self, score: float) -> int:
        """Convert score to industry percentile"""
        # Simple mapping - in production would use actual distribution
        if score >= 1.5:
            return 90
        elif score >= 1.2:
            return 75
        elif score >= 1.0:
            return 60
        elif score >= 0.8:
            return 40
        elif score >= 0.6:
            return 25
        else:
            return 10
    
    def _generate_industry_insights(self, features: pd.DataFrame, industry: str,
                                   prediction: Dict[str, Any],
                                   benchmark: Dict[str, Any]) -> List[str]:
        """Generate industry-specific insights"""
        insights = []
        
        # Industry identification
        insights.append(f"Classified as {industry} startup")
        
        # Performance insights
        percentile = benchmark['industry_percentile']
        if percentile >= 75:
            insights.append(f"Top quartile performance in {industry} sector")
        elif percentile >= 50:
            insights.append(f"Above average for {industry} startups")
        elif percentile < 25:
            insights.append(f"Below average for {industry} sector")
        
        # Industry-specific insights
        industry_insights = {
            'SaaS': self._get_saas_insights,
            'FinTech': self._get_fintech_insights,
            'HealthTech': self._get_healthtech_insights,
            'E-commerce': self._get_ecommerce_insights,
            'AI/ML': self._get_aiml_insights
        }
        
        if industry in industry_insights:
            insights.extend(industry_insights[industry](features, benchmark))
        
        # Strengths and weaknesses
        if benchmark['strengths']:
            insights.append(f"Key strengths: {', '.join(benchmark['strengths'][:2])}")
        
        if benchmark['weaknesses']:
            insights.append(f"Areas for improvement: {', '.join(benchmark['weaknesses'][:2])}")
        
        return insights
    
    def _get_saas_insights(self, features: pd.DataFrame, 
                          benchmark: Dict[str, Any]) -> List[str]:
        """SaaS-specific insights"""
        insights = []
        
        if 'net_dollar_retention_percent' in features.columns:
            ndr = features['net_dollar_retention_percent'].iloc[0]
            if ndr > 120:
                insights.append("Excellent net dollar retention indicates strong product-market fit")
            elif ndr < 100:
                insights.append("Net dollar retention below 100% - focus on reducing churn")
        
        if 'burn_multiple' in features.columns:
            burn = features['burn_multiple'].iloc[0]
            if burn < 1:
                insights.append("Efficient growth with burn multiple < 1")
            elif burn > 3:
                insights.append("High burn multiple - optimize CAC and sales efficiency")
        
        return insights
    
    def _get_fintech_insights(self, features: pd.DataFrame,
                             benchmark: Dict[str, Any]) -> List[str]:
        """FinTech-specific insights"""
        insights = []
        
        if 'regulatory_advantage_present' in features.columns:
            if features['regulatory_advantage_present'].iloc[0]:
                insights.append("Regulatory moat provides competitive advantage")
        
        if 'has_data_moat' in features.columns:
            if features['has_data_moat'].iloc[0]:
                insights.append("Data network effects strengthen market position")
        
        return insights
    
    def _get_healthtech_insights(self, features: pd.DataFrame,
                                benchmark: Dict[str, Any]) -> List[str]:
        """HealthTech-specific insights"""
        insights = []
        
        if 'patent_count' in features.columns:
            patents = features['patent_count'].iloc[0]
            if patents > 5:
                insights.append(f"Strong IP portfolio with {patents} patents")
        
        if 'regulatory_advantage_present' in features.columns:
            if features['regulatory_advantage_present'].iloc[0]:
                insights.append("FDA/regulatory approvals create barriers to entry")
        
        return insights
    
    def _get_ecommerce_insights(self, features: pd.DataFrame,
                               benchmark: Dict[str, Any]) -> List[str]:
        """E-commerce-specific insights"""
        insights = []
        
        if 'gross_margin_percent' in features.columns:
            margin = features['gross_margin_percent'].iloc[0]
            if margin > 50:
                insights.append("Above-average margins for e-commerce")
            elif margin < 30:
                insights.append("Margins below e-commerce standards - explore pricing/COGS")
        
        if 'customer_concentration_percent' in features.columns:
            concentration = features['customer_concentration_percent'].iloc[0]
            if concentration < 20:
                insights.append("Well-diversified customer base reduces risk")
        
        return insights
    
    def _get_aiml_insights(self, features: pd.DataFrame,
                          benchmark: Dict[str, Any]) -> List[str]:
        """AI/ML-specific insights"""
        insights = []
        
        if 'tech_differentiation_score' in features.columns:
            tech_score = features['tech_differentiation_score'].iloc[0]
            if tech_score >= 4.5:
                insights.append("Cutting-edge technology provides strong differentiation")
        
        if 'has_data_moat' in features.columns:
            if features['has_data_moat'].iloc[0]:
                insights.append("Proprietary dataset creates defensible position")
        
        return insights
    
    def _generate_recommendations(self, industry: str, probability: float,
                                 benchmark: Dict[str, Any]) -> List[str]:
        """Generate industry-specific recommendations"""
        recommendations = []
        
        # General recommendations based on performance
        if probability < 0.5:
            recommendations.append(f"Focus on {industry} best practices to improve success odds")
        
        if benchmark['overall_score'] < 0.8:
            recommendations.append("Benchmark against top-performing peers in your sector")
        
        # Industry-specific recommendations
        industry_recs = {
            'SaaS': [
                "Target 120%+ net dollar retention",
                "Optimize CAC payback to <12 months",
                "Build predictable revenue growth"
            ],
            'FinTech': [
                "Ensure regulatory compliance roadmap",
                "Focus on trust and security features",
                "Build network effects into product"
            ],
            'HealthTech': [
                "Develop clear regulatory strategy",
                "Build clinical validation evidence",
                "Establish KOL relationships"
            ],
            'E-commerce': [
                "Improve gross margins through optimization",
                "Diversify customer acquisition channels",
                "Build brand loyalty programs"
            ],
            'AI/ML': [
                "Protect IP through patents",
                "Build proprietary datasets",
                "Demonstrate clear ROI for customers"
            ]
        }
        
        if industry in industry_recs and probability < 0.7:
            recommendations.extend(industry_recs[industry][:2])
        
        # Weakness-specific recommendations
        for weakness in benchmark['weaknesses'][:2]:
            if 'margin' in weakness.lower():
                recommendations.append("Analyze pricing strategy and cost structure")
            elif 'growth' in weakness.lower():
                recommendations.append("Develop growth acceleration plan")
            elif 'unit economics' in weakness.lower():
                recommendations.append("Focus on improving LTV/CAC ratio")
        
        return recommendations[:5]  # Limit to top 5
    
    def _get_peer_comparison(self, features: pd.DataFrame, 
                            industry: str) -> Dict[str, Any]:
        """Compare against industry peers"""
        # In production, this would query a database of peer companies
        # For now, return synthetic comparison
        
        return {
            'peer_group_size': np.random.randint(50, 200),
            'percentile_rank': np.random.randint(25, 75),
            'top_performers': [
                f"Top {industry} Startup A",
                f"Top {industry} Startup B"
            ],
            'comparison_metrics': {
                'growth_rate': 'Above peer median',
                'efficiency': 'Below peer median',
                'team_quality': 'At peer median'
            }
        }
    
    def _get_default_predictions(self, features: pd.DataFrame) -> Dict[str, Any]:
        """Return default predictions when models not loaded"""
        return {
            'prediction': 0,
            'probability': 0.5,
            'industry': 'Unknown',
            'industry_confidence': 0.0,
            'benchmark_analysis': {
                'overall_score': 0.5,
                'metrics': {},
                'strengths': [],
                'weaknesses': []
            },
            'insights': ["Industry models not available"],
            'recommendations': ["Load industry models for sector-specific analysis"],
            'peer_comparison': {
                'peer_group_size': 0,
                'percentile_rank': 50,
                'top_performers': [],
                'comparison_metrics': {}
            }
        }


class IndustryClassifier:
    """Classify startups into industries based on features"""
    
    def classify(self, features: pd.DataFrame) -> str:
        """
        Classify startup into industry based on features
        
        Args:
            features: Startup features
            
        Returns:
            Industry classification
        """
        # Simple rule-based classification
        # In production, this would use a trained classifier
        
        # Check for strong indicators
        if 'sector' in features.columns:
            return self._normalize_sector(features['sector'].iloc[0])
        
        # Feature-based classification
        scores = {}
        
        # SaaS indicators
        saas_score = 0
        if 'net_dollar_retention_percent' in features.columns:
            if features['net_dollar_retention_percent'].iloc[0] > 100:
                saas_score += 1
        if 'burn_multiple' in features.columns:
            saas_score += 0.5
        scores['SaaS'] = saas_score
        
        # FinTech indicators
        fintech_score = 0
        if 'regulatory_advantage_present' in features.columns:
            if features['regulatory_advantage_present'].iloc[0]:
                fintech_score += 1
        scores['FinTech'] = fintech_score
        
        # HealthTech indicators
        health_score = 0
        if 'patent_count' in features.columns:
            if features['patent_count'].iloc[0] > 5:
                health_score += 0.5
        scores['HealthTech'] = health_score
        
        # E-commerce indicators
        ecom_score = 0
        if 'customer_concentration_percent' in features.columns:
            ecom_score += 0.5
        scores['E-commerce'] = ecom_score
        
        # Return highest scoring industry
        if scores:
            return max(scores, key=scores.get)
        else:
            return 'SaaS'  # Default
    
    def _normalize_sector(self, sector: str) -> str:
        """Normalize sector name to standard industry"""
        sector_lower = sector.lower()
        
        if 'saas' in sector_lower or 'software' in sector_lower:
            return 'SaaS'
        elif 'fin' in sector_lower:
            return 'FinTech'
        elif 'health' in sector_lower or 'med' in sector_lower:
            return 'HealthTech'
        elif 'commerce' in sector_lower or 'retail' in sector_lower:
            return 'E-commerce'
        elif 'ai' in sector_lower or 'ml' in sector_lower:
            return 'AI/ML'
        elif 'bio' in sector_lower:
            return 'BioTech'
        elif 'ed' in sector_lower:
            return 'EdTech'
        elif 'clean' in sector_lower or 'energy' in sector_lower:
            return 'CleanTech'
        else:
            return 'SaaS'  # Default