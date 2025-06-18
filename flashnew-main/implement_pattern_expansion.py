#!/usr/bin/env python3
"""
Pattern Expansion Implementation - Phase 1
Analyze the current dataset to discover and validate new patterns
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import existing definitions
from api_server import ALL_FEATURES, CAPITAL_FEATURES, ADVANTAGE_FEATURES, MARKET_FEATURES, PEOPLE_FEATURES


class PatternExpansionAnalyzer:
    """Analyze startup data to discover and validate new patterns"""
    
    def __init__(self):
        self.data = None
        self.pattern_assignments = None
        self.new_patterns = {}
        self.pattern_stats = {}
        
    def load_data(self, data_path='data/final_100k_dataset_45features.csv'):
        """Load and preprocess the dataset"""
        logger.info(f"Loading data from {data_path}")
        self.data = pd.read_csv(data_path)
        
        # Encode categorical variables
        categorical_mappings = {
            'funding_stage': {'pre_seed': 0, 'seed': 1, 'series_a': 2, 'series_b': 3, 'series_c': 4, 'growth': 5},
            'product_stage': {'concept': 0, 'mvp': 1, 'beta': 2, 'launch': 3, 'growth': 4, 'mature': 5}
        }
        
        for col, mapping in categorical_mappings.items():
            if col in self.data.columns:
                self.data[col] = self.data[col].map(mapping).fillna(0)
        
        # Handle other categorical columns
        for col in ['sector', 'investor_tier_primary']:
            if col in self.data.columns:
                self.data[col] = pd.Categorical(self.data[col]).codes
        
        # Convert boolean columns
        bool_columns = ['has_debt', 'network_effects_present', 'has_data_moat', 
                       'regulatory_advantage_present', 'key_person_dependency']
        for col in bool_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(int)
        
        logger.info(f"Data loaded: {self.data.shape}")
        return self.data
    
    def analyze_current_patterns(self):
        """Analyze distribution and coverage of current patterns"""
        logger.info("Analyzing current pattern coverage...")
        
        # Load current pattern assignments if they exist
        pattern_results = {
            'total_startups': len(self.data),
            'success_rate': self.data['success'].mean()
        }
        
        # Analyze by funding stage
        stage_dist = self.data['funding_stage'].value_counts()
        logger.info(f"Funding stage distribution:\n{stage_dist}")
        
        # Analyze by success patterns
        success_by_stage = self.data.groupby('funding_stage')['success'].agg(['mean', 'count'])
        logger.info(f"Success by stage:\n{success_by_stage}")
        
        return pattern_results
    
    def discover_industry_patterns(self):
        """Discover patterns within industry verticals"""
        logger.info("Discovering industry-specific patterns...")
        
        # Get unique sectors
        sectors = self.data['sector'].unique()
        industry_patterns = {}
        
        for sector in sectors:
            if sector >= 0:  # Valid sector
                sector_data = self.data[self.data['sector'] == sector]
                
                if len(sector_data) >= 500:  # Minimum sample size
                    # Analyze characteristics
                    sector_profile = {
                        'count': len(sector_data),
                        'success_rate': sector_data['success'].mean(),
                        'avg_funding': sector_data['total_capital_raised_usd'].mean(),
                        'avg_team_size': sector_data['team_size_full_time'].mean(),
                        'avg_growth': sector_data['revenue_growth_rate_percent'].mean(),
                        'characteristics': self._extract_sector_characteristics(sector_data)
                    }
                    
                    # Sub-cluster within sector
                    if len(sector_data) >= 1000:
                        subclusters = self._find_subclusters(sector_data)
                        sector_profile['subclusters'] = subclusters
                    
                    industry_patterns[f'sector_{sector}'] = sector_profile
        
        return industry_patterns
    
    def discover_growth_patterns(self):
        """Discover patterns based on growth dynamics"""
        logger.info("Discovering growth-based patterns...")
        
        # Define growth features
        growth_features = [
            'revenue_growth_rate_percent',
            'user_growth_rate_percent',
            'customer_count',
            'net_dollar_retention_percent',
            'burn_multiple'
        ]
        
        # Filter to companies with growth data
        growth_data = self.data[growth_features].dropna()
        
        # Standardize features
        scaler = StandardScaler()
        growth_scaled = scaler.fit_transform(growth_data)
        
        # Try different numbers of clusters
        best_k = self._find_optimal_clusters(growth_scaled, min_k=5, max_k=12)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=best_k, random_state=42)
        growth_clusters = kmeans.fit_predict(growth_scaled)
        
        # Analyze each cluster
        growth_patterns = {}
        for i in range(best_k):
            cluster_mask = growth_clusters == i
            cluster_data = self.data.loc[growth_data.index[cluster_mask]]
            
            pattern_name = self._name_growth_pattern(cluster_data, growth_features)
            growth_patterns[pattern_name] = {
                'size': len(cluster_data),
                'success_rate': cluster_data['success'].mean(),
                'profile': cluster_data[growth_features].mean().to_dict(),
                'characteristics': self._extract_growth_characteristics(cluster_data)
            }
        
        return growth_patterns
    
    def discover_business_model_patterns(self):
        """Discover patterns based on business model characteristics"""
        logger.info("Discovering business model patterns...")
        
        # Business model indicators
        bm_features = [
            'annual_revenue_run_rate',
            'gross_margin_percent',
            'ltv_cac_ratio',
            'burn_multiple',
            'customer_concentration_percent',
            'net_dollar_retention_percent',
            'product_retention_30d'
        ]
        
        # Create business model profiles
        bm_patterns = {}
        
        # SaaS indicators
        saas_mask = (
            (self.data['net_dollar_retention_percent'] > 100) & 
            (self.data['gross_margin_percent'] > 60) &
            (self.data['ltv_cac_ratio'] > 2)
        )
        
        # Marketplace indicators  
        marketplace_mask = (
            (self.data['network_effects_present'] == 1) &
            (self.data['customer_concentration_percent'] < 20) &
            (self.data['gross_margin_percent'] < 40)
        )
        
        # Hardware indicators
        hardware_mask = (
            (self.data['gross_margin_percent'] < 50) &
            (self.data['patent_count'] > 0) &
            (self.data['tech_differentiation_score'] > 3)
        )
        
        # Analyze each business model
        for name, mask in [
            ('PURE_SAAS', saas_mask),
            ('MARKETPLACE_PLATFORM', marketplace_mask),
            ('HARDWARE_PRODUCT', hardware_mask)
        ]:
            if mask.sum() >= 100:
                pattern_data = self.data[mask]
                bm_patterns[name] = {
                    'size': len(pattern_data),
                    'success_rate': pattern_data['success'].mean(),
                    'profile': pattern_data[bm_features].mean().to_dict()
                }
        
        return bm_patterns
    
    def discover_technology_patterns(self):
        """Discover patterns based on technology depth"""
        logger.info("Discovering technology-based patterns...")
        
        tech_features = [
            'patent_count',
            'tech_differentiation_score',
            'regulatory_advantage_present',
            'has_data_moat',
            'network_effects_present',
            'scalability_score'
        ]
        
        # High-tech indicators
        patterns = {}
        
        # AI/ML pattern
        ai_mask = (
            (self.data['tech_differentiation_score'] >= 4) &
            (self.data['has_data_moat'] == 1)
        )
        
        # Biotech pattern
        biotech_mask = (
            (self.data['regulatory_advantage_present'] == 1) &
            (self.data['patent_count'] > 5) &
            (self.data['runway_months'] > 24)
        )
        
        # Platform pattern
        platform_mask = (
            (self.data['network_effects_present'] == 1) &
            (self.data['scalability_score'] >= 4) &
            (self.data['tech_differentiation_score'] >= 3)
        )
        
        for name, mask in [
            ('AI_ML_FOCUSED', ai_mask),
            ('BIOTECH_DEEP', biotech_mask),
            ('PLATFORM_TECH', platform_mask)
        ]:
            if mask.sum() >= 100:
                pattern_data = self.data[mask]
                patterns[name] = {
                    'size': len(pattern_data),
                    'success_rate': pattern_data['success'].mean(),
                    'requirements': self._extract_pattern_requirements(pattern_data, tech_features)
                }
        
        return patterns
    
    def _find_optimal_clusters(self, data, min_k=3, max_k=10):
        """Find optimal number of clusters using silhouette score"""
        scores = []
        
        for k in range(min_k, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(data)
            score = silhouette_score(data, labels)
            scores.append(score)
            logger.info(f"K={k}, silhouette score: {score:.3f}")
        
        best_k = min_k + np.argmax(scores)
        return best_k
    
    def _find_subclusters(self, sector_data):
        """Find subclusters within a sector"""
        features = sector_data[ALL_FEATURES].fillna(0)
        
        # Scale features
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)
        
        # Use DBSCAN for density-based clustering
        dbscan = DBSCAN(eps=0.5, min_samples=50)
        clusters = dbscan.fit_predict(scaled)
        
        subclusters = {}
        for label in set(clusters):
            if label >= 0:  # Ignore noise points
                mask = clusters == label
                subcluster_data = sector_data.iloc[mask]
                
                if len(subcluster_data) >= 100:
                    subclusters[f'subcluster_{label}'] = {
                        'size': len(subcluster_data),
                        'success_rate': subcluster_data['success'].mean()
                    }
        
        return subclusters
    
    def _extract_sector_characteristics(self, sector_data):
        """Extract key characteristics of a sector"""
        chars = {
            'typical_funding_stage': sector_data['funding_stage'].mode().values[0] if len(sector_data) > 0 else None,
            'avg_team_size': sector_data['team_size_full_time'].mean(),
            'burn_characteristics': 'high' if sector_data['burn_multiple'].mean() > 3 else 'moderate',
            'growth_profile': 'high' if sector_data['revenue_growth_rate_percent'].mean() > 100 else 'steady'
        }
        return chars
    
    def _extract_growth_characteristics(self, cluster_data):
        """Extract growth pattern characteristics"""
        return {
            'growth_type': self._classify_growth_type(cluster_data),
            'efficiency': 'efficient' if cluster_data['burn_multiple'].mean() < 2 else 'burn-heavy',
            'retention': 'strong' if cluster_data['net_dollar_retention_percent'].mean() > 110 else 'weak'
        }
    
    def _name_growth_pattern(self, cluster_data, features):
        """Generate descriptive name for growth pattern"""
        growth = cluster_data['revenue_growth_rate_percent'].mean()
        burn = cluster_data['burn_multiple'].mean()
        
        if growth > 200 and burn > 5:
            return "HYPERGROWTH_HIGH_BURN"
        elif growth > 100 and burn < 2:
            return "EFFICIENT_GROWTH"
        elif growth < 50 and burn < 1:
            return "STEADY_PROFITABLE"
        elif growth < 20:
            return "LOW_GROWTH"
        else:
            return f"GROWTH_PATTERN_{int(growth)}_{int(burn)}"
    
    def _classify_growth_type(self, data):
        """Classify the type of growth"""
        user_growth = data['user_growth_rate_percent'].mean()
        revenue_growth = data['revenue_growth_rate_percent'].mean()
        
        if user_growth > revenue_growth * 1.5:
            return "user-led"
        elif revenue_growth > user_growth * 1.5:
            return "revenue-led"
        else:
            return "balanced"
    
    def _extract_pattern_requirements(self, pattern_data, features):
        """Extract requirements for a pattern"""
        reqs = {}
        for feature in features:
            if feature in pattern_data.columns:
                values = pattern_data[feature]
                reqs[feature] = {
                    'min': values.quantile(0.25),
                    'median': values.median(),
                    'max': values.quantile(0.75)
                }
        return reqs
    
    def generate_pattern_report(self, output_path='pattern_expansion_analysis.json'):
        """Generate comprehensive pattern analysis report"""
        logger.info("Generating pattern expansion report...")
        
        # Run all analyses
        current = self.analyze_current_patterns()
        industry = self.discover_industry_patterns()
        growth = self.discover_growth_patterns()
        business_model = self.discover_business_model_patterns()
        technology = self.discover_technology_patterns()
        
        # Compile report
        report = {
            'analysis_date': pd.Timestamp.now().isoformat(),
            'dataset_stats': current,
            'discovered_patterns': {
                'industry_specific': len(industry),
                'growth_based': len(growth),
                'business_model': len(business_model),
                'technology_based': len(technology)
            },
            'total_new_patterns': len(industry) + len(growth) + len(business_model) + len(technology),
            'patterns': {
                'industry': industry,
                'growth': growth,
                'business_model': business_model,
                'technology': technology
            },
            'recommendations': self._generate_recommendations(industry, growth, business_model, technology)
        }
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Report saved to {output_path}")
        return report
    
    def _generate_recommendations(self, industry, growth, bm, tech):
        """Generate recommendations for pattern expansion"""
        recs = []
        
        # Check coverage
        total_patterns = len(industry) + len(growth) + len(bm) + len(tech)
        
        if total_patterns < 30:
            recs.append("Need more granular patterns - current discovery found only {} patterns".format(total_patterns))
        
        # Check distribution
        if len(industry) < 8:
            recs.append("Industry vertical patterns are underdeveloped - expand sector-specific patterns")
        
        if len(growth) < 5:
            recs.append("Growth dynamics need more nuance - consider user acquisition patterns")
        
        # Success rate variance
        all_success_rates = []
        for patterns in [industry, growth, bm, tech]:
            for p in patterns.values():
                if 'success_rate' in p:
                    all_success_rates.append(p['success_rate'])
        
        if all_success_rates:
            variance = np.var(all_success_rates)
            if variance < 0.01:
                recs.append("Patterns are not discriminative enough - success rates too similar")
        
        return recs


def main():
    """Run pattern expansion analysis"""
    analyzer = PatternExpansionAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Generate comprehensive report
    report = analyzer.generate_pattern_report()
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Pattern Expansion Analysis Complete")
    logger.info(f"Total new patterns discovered: {report['total_new_patterns']}")
    logger.info("Pattern breakdown:")
    for category, count in report['discovered_patterns'].items():
        logger.info(f"  - {category}: {count} patterns")
    
    logger.info("\nRecommendations:")
    for rec in report['recommendations']:
        logger.info(f"  • {rec}")


if __name__ == "__main__":
    main()