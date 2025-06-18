#!/usr/bin/env python3
"""
Week 1: Analyze Pattern Distribution in 100k Dataset
Discover natural patterns based on CAMP scores and success outcomes
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PatternDistributionAnalyzer:
    """Analyze the 100k dataset to discover natural startup patterns"""
    
    def __init__(self, data_path: str = "data/final_100k_dataset_45features.csv"):
        self.data_path = data_path
        self.df = None
        self.camp_scores = None
        self.patterns = {}
        self.pattern_stats = {}
        self.capital_features = []
        self.advantage_features = []
        self.market_features = []
        self.people_features = []
        
    def load_data(self):
        """Load the dataset"""
        logger.info(f"Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} samples with {len(self.df.columns)} features")
        
        # Identify CAMP features based on actual dataset
        # Capital features
        self.capital_features = [col for col in self.df.columns if any(
            x in col.lower() for x in ['funding', 'capital', 'burn', 'revenue', 'runway', 'cash', 'ltv_cac', 'margin', 'debt']
        ) and col not in ['startup_id', 'startup_name']]
        
        # Advantage features
        self.advantage_features = [col for col in self.df.columns if any(
            x in col.lower() for x in ['patent', 'differentiation', 'moat', 'retention', 'proprietary', 'regulatory', 'network_effect', 'viral']
        ) and col not in ['startup_id', 'startup_name']]
        
        # Market features
        self.market_features = [col for col in self.df.columns if any(
            x in col.lower() for x in ['market', 'tam', 'growth_rate', 'customer', 'competition', 'scalability', 'nps', 'churn']
        ) and col not in ['startup_id', 'startup_name']]
        
        # People features
        self.people_features = [col for col in self.df.columns if any(
            x in col.lower() for x in ['founder', 'team', 'experience', 'advisor', 'diversity', 'employee', 'ai_team', 'full_time']
        ) and col not in ['startup_id', 'startup_name']]
        
        logger.info(f"CAMP features - C:{len(self.capital_features)}, "
                   f"A:{len(self.advantage_features)}, M:{len(self.market_features)}, "
                   f"P:{len(self.people_features)}")
        
    def calculate_camp_scores(self):
        """Calculate CAMP scores for each startup"""
        logger.info("Calculating CAMP scores...")
        
        # Make sure features are identified
        if not self.capital_features:
            self.load_data()
        
        # Normalize features
        scaler = StandardScaler()
        
        # Calculate scores (0-100 scale)
        self.camp_scores = pd.DataFrame()
        
        # Capital score
        if self.capital_features:
            capital_data = self.df[self.capital_features].fillna(0)
            capital_scaled = scaler.fit_transform(capital_data)
            self.camp_scores['capital_score'] = (capital_scaled.mean(axis=1) + 2) * 25  # Scale to 0-100
        else:
            self.camp_scores['capital_score'] = 50  # Default score
        
        # Advantage score
        if self.advantage_features:
            advantage_data = self.df[self.advantage_features].fillna(0)
            advantage_scaled = scaler.fit_transform(advantage_data)
            self.camp_scores['advantage_score'] = (advantage_scaled.mean(axis=1) + 2) * 25
        else:
            self.camp_scores['advantage_score'] = 50
        
        # Market score
        if self.market_features:
            market_data = self.df[self.market_features].fillna(0)
            market_scaled = scaler.fit_transform(market_data)
            self.camp_scores['market_score'] = (market_scaled.mean(axis=1) + 2) * 25
        else:
            self.camp_scores['market_score'] = 50
        
        # People score
        if self.people_features:
            people_data = self.df[self.people_features].fillna(0)
            people_scaled = scaler.fit_transform(people_data)
            self.camp_scores['people_score'] = (people_scaled.mean(axis=1) + 2) * 25
        else:
            self.camp_scores['people_score'] = 50
        
        # Clip to 0-100 range
        self.camp_scores = self.camp_scores.clip(0, 100)
        
        # Add metadata
        self.camp_scores['success_outcome'] = self.df.get('success', 0)
        self.camp_scores['funding_stage'] = self.df.get('funding_stage', 'unknown')
        self.camp_scores['industry'] = self.df.get('industry', 'other')
        
        logger.info("CAMP scores calculated")
        
    def discover_patterns_with_clustering(self, n_clusters_range=(20, 60)):
        """Use clustering to discover natural patterns"""
        logger.info("Discovering patterns using clustering...")
        
        # Prepare data for clustering
        X = self.camp_scores[['capital_score', 'advantage_score', 
                              'market_score', 'people_score']].values
        
        # Find optimal number of clusters
        inertias = []
        silhouette_scores = []
        
        for n_clusters in range(n_clusters_range[0], n_clusters_range[1], 5):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            inertias.append(kmeans.inertia_)
            
            # Calculate average cluster size
            cluster_sizes = Counter(labels)
            min_size = min(cluster_sizes.values())
            
            logger.info(f"n_clusters={n_clusters}, min_cluster_size={min_size}")
            
            # Skip if any cluster is too small
            if min_size < 500:
                silhouette_scores.append(0)
            else:
                from sklearn.metrics import silhouette_score
                score = silhouette_score(X, labels, sample_size=10000)
                silhouette_scores.append(score)
        
        # Select optimal number based on silhouette score
        optimal_idx = np.argmax(silhouette_scores)
        optimal_n = list(range(n_clusters_range[0], n_clusters_range[1], 5))[optimal_idx]
        
        logger.info(f"Optimal number of clusters: {optimal_n}")
        
        # Final clustering
        self.kmeans = KMeans(n_clusters=optimal_n, random_state=42, n_init=20)
        self.camp_scores['cluster'] = self.kmeans.fit_predict(X)
        
        # Analyze each cluster
        self._analyze_clusters()
        
    def _analyze_clusters(self):
        """Analyze characteristics of each cluster"""
        logger.info("Analyzing cluster characteristics...")
        
        for cluster_id in sorted(self.camp_scores['cluster'].unique()):
            cluster_data = self.camp_scores[self.camp_scores['cluster'] == cluster_id]
            
            # Basic stats
            cluster_size = len(cluster_data)
            success_rate = cluster_data['success_outcome'].mean()
            
            # CAMP profile
            camp_means = {
                'capital': cluster_data['capital_score'].mean(),
                'advantage': cluster_data['advantage_score'].mean(),
                'market': cluster_data['market_score'].mean(),
                'people': cluster_data['people_score'].mean()
            }
            
            # Industry distribution
            industry_dist = cluster_data['industry'].value_counts().head(3).to_dict()
            
            # Stage distribution
            stage_dist = cluster_data['funding_stage'].value_counts().head(3).to_dict()
            
            # Generate pattern name
            pattern_name = self._generate_pattern_name(camp_means, success_rate, industry_dist)
            
            self.patterns[cluster_id] = {
                'name': pattern_name,
                'size': cluster_size,
                'success_rate': success_rate,
                'camp_profile': camp_means,
                'top_industries': industry_dist,
                'top_stages': stage_dist,
                'cluster_id': cluster_id
            }
            
            logger.info(f"Cluster {cluster_id}: {pattern_name} "
                       f"(n={cluster_size}, success={success_rate:.2%})")
    
    def _generate_pattern_name(self, camp_means, success_rate, industry_dist):
        """Generate meaningful pattern name based on characteristics"""
        # Identify dominant CAMP dimension
        camp_sorted = sorted(camp_means.items(), key=lambda x: x[1], reverse=True)
        dominant_camp = camp_sorted[0][0].upper()
        
        # Success level
        if success_rate > 0.7:
            success_level = "HIGH_PERFORMING"
        elif success_rate > 0.5:
            success_level = "MODERATE"
        else:
            success_level = "STRUGGLING"
        
        # Industry focus
        top_industry = list(industry_dist.keys())[0] if industry_dist else "GENERAL"
        
        # Efficiency indicator
        if camp_means['capital'] > 70:
            efficiency = "EFFICIENT"
        elif camp_means['capital'] < 40:
            efficiency = "CAPITAL_INTENSIVE"
        else:
            efficiency = "BALANCED"
        
        return f"{success_level}_{dominant_camp}_{efficiency}_{top_industry.upper()}"
    
    def identify_top_patterns(self, coverage_target=0.8):
        """Identify top patterns that cover X% of data"""
        logger.info(f"Identifying patterns covering {coverage_target*100}% of data...")
        
        # Sort patterns by size
        sorted_patterns = sorted(self.patterns.items(), 
                               key=lambda x: x[1]['size'], 
                               reverse=True)
        
        total_samples = len(self.camp_scores)
        covered_samples = 0
        top_patterns = []
        
        for cluster_id, pattern_info in sorted_patterns:
            top_patterns.append((cluster_id, pattern_info))
            covered_samples += pattern_info['size']
            
            if covered_samples / total_samples >= coverage_target:
                break
        
        logger.info(f"Top {len(top_patterns)} patterns cover "
                   f"{covered_samples/total_samples:.1%} of data")
        
        return top_patterns
    
    def export_pattern_definitions(self):
        """Export pattern definitions for implementation"""
        output = {
            'discovery_metadata': {
                'total_samples': len(self.camp_scores),
                'n_patterns_discovered': len(self.patterns),
                'clustering_method': 'kmeans_camp_scores'
            },
            'patterns': {}
        }
        
        # Get top patterns covering 80% of data
        top_patterns = self.identify_top_patterns(0.8)
        
        for cluster_id, pattern_info in top_patterns:
            output['patterns'][pattern_info['name']] = {
                'cluster_id': cluster_id,
                'sample_count': pattern_info['size'],
                'success_rate': round(pattern_info['success_rate'], 3),
                'camp_thresholds': {
                    'capital': f">{pattern_info['camp_profile']['capital']-10}",
                    'advantage': f">{pattern_info['camp_profile']['advantage']-10}",
                    'market': f">{pattern_info['camp_profile']['market']-10}",
                    'people': f">{pattern_info['camp_profile']['people']-10}"
                },
                'typical_industries': pattern_info['top_industries'],
                'typical_stages': pattern_info['top_stages'],
                'centroid': {
                    'capital': round(pattern_info['camp_profile']['capital'], 1),
                    'advantage': round(pattern_info['camp_profile']['advantage'], 1),
                    'market': round(pattern_info['camp_profile']['market'], 1),
                    'people': round(pattern_info['camp_profile']['people'], 1)
                }
            }
        
        # Save to file
        output_path = Path('ml_core/discovered_patterns.json')
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Exported pattern definitions to {output_path}")
        
        return output
    
    def visualize_patterns(self):
        """Create visualizations of discovered patterns"""
        logger.info("Creating pattern visualizations...")
        
        # Create output directory
        viz_dir = Path('pattern_analysis_visualizations')
        viz_dir.mkdir(exist_ok=True)
        
        # 1. CAMP score distribution by pattern
        plt.figure(figsize=(15, 10))
        
        top_patterns = self.identify_top_patterns(0.8)
        pattern_camps = []
        
        for cluster_id, pattern_info in top_patterns[:20]:  # Top 20 patterns
            pattern_camps.append({
                'Pattern': pattern_info['name'][:30],  # Truncate long names
                'Capital': pattern_info['camp_profile']['capital'],
                'Advantage': pattern_info['camp_profile']['advantage'],
                'Market': pattern_info['camp_profile']['market'],
                'People': pattern_info['camp_profile']['people'],
                'Success Rate': pattern_info['success_rate'] * 100
            })
        
        camp_df = pd.DataFrame(pattern_camps)
        
        # Heatmap of CAMP scores
        plt.subplot(2, 2, 1)
        sns.heatmap(camp_df[['Capital', 'Advantage', 'Market', 'People']].T,
                    xticklabels=camp_df['Pattern'],
                    cmap='RdYlGn', center=50, annot=True, fmt='.0f')
        plt.title('CAMP Profiles by Pattern')
        plt.xticks(rotation=45, ha='right')
        
        # Success rates
        plt.subplot(2, 2, 2)
        bars = plt.bar(range(len(camp_df)), camp_df['Success Rate'])
        plt.xticks(range(len(camp_df)), camp_df['Pattern'], rotation=45, ha='right')
        plt.ylabel('Success Rate (%)')
        plt.title('Success Rates by Pattern')
        
        # Color bars by success rate
        for i, bar in enumerate(bars):
            if camp_df.iloc[i]['Success Rate'] > 70:
                bar.set_color('green')
            elif camp_df.iloc[i]['Success Rate'] > 50:
                bar.set_color('orange')
            else:
                bar.set_color('red')
        
        # Pattern sizes
        plt.subplot(2, 2, 3)
        sizes = [self.patterns[cluster_id]['size'] for cluster_id, _ in top_patterns[:20]]
        plt.bar(range(len(sizes)), sizes)
        plt.xticks(range(len(sizes)), [p[1]['name'][:20] for p in top_patterns[:20]], 
                   rotation=45, ha='right')
        plt.ylabel('Number of Startups')
        plt.title('Pattern Sizes')
        
        # 2D visualization of patterns
        plt.subplot(2, 2, 4)
        # Use PCA for 2D visualization
        X = self.camp_scores[['capital_score', 'advantage_score', 
                              'market_score', 'people_score']].values
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        
        # Plot clusters
        scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], 
                            c=self.camp_scores['cluster'], 
                            cmap='tab20', alpha=0.6, s=1)
        
        # Add cluster centers
        centers_2d = pca.transform(self.kmeans.cluster_centers_)
        plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
                   c='red', marker='x', s=200, linewidths=3)
        
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        plt.title('Pattern Clusters in 2D')
        
        plt.tight_layout()
        plt.savefig(viz_dir / 'pattern_analysis_overview.png', dpi=300)
        plt.close()
        
        logger.info(f"Saved visualizations to {viz_dir}")
    
    def generate_pattern_report(self):
        """Generate comprehensive pattern analysis report"""
        report = []
        report.append("# Pattern Discovery Report\n")
        report.append(f"Total samples analyzed: {len(self.camp_scores):,}\n")
        report.append(f"Patterns discovered: {len(self.patterns)}\n\n")
        
        # Top patterns
        report.append("## Top 20 Patterns (by size)\n")
        top_patterns = self.identify_top_patterns(0.9)
        
        for i, (cluster_id, pattern) in enumerate(top_patterns[:20]):
            report.append(f"\n### {i+1}. {pattern['name']}")
            report.append(f"- **Size**: {pattern['size']:,} startups "
                         f"({pattern['size']/len(self.camp_scores)*100:.1f}%)")
            report.append(f"- **Success Rate**: {pattern['success_rate']:.1%}")
            report.append(f"- **CAMP Profile**: C:{pattern['camp_profile']['capital']:.0f}, "
                         f"A:{pattern['camp_profile']['advantage']:.0f}, "
                         f"M:{pattern['camp_profile']['market']:.0f}, "
                         f"P:{pattern['camp_profile']['people']:.0f}")
            report.append(f"- **Top Industries**: {', '.join(pattern['top_industries'].keys())}")
            report.append(f"- **Top Stages**: {', '.join(pattern['top_stages'].keys())}")
            report.append("")
        
        # Statistical summary
        report.append("\n## Statistical Summary\n")
        
        success_rates = [p['success_rate'] for p in self.patterns.values()]
        sizes = [p['size'] for p in self.patterns.values()]
        
        report.append(f"- Average pattern success rate: {np.mean(success_rates):.1%}")
        report.append(f"- Success rate range: {min(success_rates):.1%} - {max(success_rates):.1%}")
        report.append(f"- Average pattern size: {np.mean(sizes):.0f}")
        report.append(f"- Size range: {min(sizes)} - {max(sizes)}")
        report.append(f"- Patterns with >1000 samples: "
                     f"{sum(1 for s in sizes if s > 1000)}")
        report.append(f"- Patterns with >70% success: "
                     f"{sum(1 for sr in success_rates if sr > 0.7)}")
        
        # Save report
        report_path = Path('pattern_discovery_report.md')
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        logger.info(f"Generated pattern report: {report_path}")

def main():
    """Run complete pattern analysis"""
    analyzer = PatternDistributionAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Calculate CAMP scores
    analyzer.calculate_camp_scores()
    
    # Discover patterns
    analyzer.discover_patterns_with_clustering(n_clusters_range=(30, 60))
    
    # Export pattern definitions
    pattern_defs = analyzer.export_pattern_definitions()
    
    # Visualize patterns
    analyzer.visualize_patterns()
    
    # Generate report
    analyzer.generate_pattern_report()
    
    # Print summary
    print(f"\nPattern Discovery Complete!")
    print(f"Discovered {len(analyzer.patterns)} patterns")
    print(f"Top patterns covering 80% of data: {len(analyzer.identify_top_patterns(0.8))}")
    print(f"Pattern definitions exported to: ml_core/discovered_patterns.json")
    print(f"Visualizations saved to: pattern_analysis_visualizations/")
    print(f"Report saved to: pattern_discovery_report.md")

if __name__ == "__main__":
    main()