#!/usr/bin/env python3
"""
Clustering-based feature engineering to identify startup archetypes
Expected to improve AUC from 77.7% to 80-81%
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class StartupArchetypeClusterer:
    def __init__(self, n_archetypes=8):
        self.n_archetypes = n_archetypes
        self.scaler = StandardScaler()
        self.success_clusterer = None
        self.failure_clusterer = None
        self.pca = None
        self.archetype_profiles = {}
        
    def prepare_clustering_features(self, df):
        """Select and prepare features for clustering"""
        
        # Key features that define startup archetypes
        clustering_features = [
            # Growth profile
            'revenue_growth_rate_percent',
            'user_growth_rate_percent',
            'monthly_revenue_growth_rate',
            
            # Efficiency profile
            'burn_multiple',
            'gross_margin_percent',
            'ltv_cac_ratio',
            'revenue_per_employee',
            
            # Scale profile
            'annual_revenue_run_rate',
            'customer_count',
            'team_size_full_time',
            
            # Capital profile
            'total_capital_raised_usd',
            'runway_months',
            'burn_months_remaining',
            
            # Product profile
            'product_retention_90d',
            'net_dollar_retention_percent',
            'dau_mau_ratio',
            
            # Market profile
            'market_growth_rate_percent',
            'competition_intensity',
            'customer_concentration_percent',
            
            # Team profile
            'prior_successful_exits_count',
            'domain_expertise_years_avg',
            'founder_ownership_percentage'
        ]
        
        # Filter to available features
        available_features = [f for f in clustering_features if f in df.columns]
        print(f"Using {len(available_features)} features for clustering")
        
        # Extract and handle missing values
        X = df[available_features].copy()
        X = X.fillna(X.median())
        
        return X, available_features
    
    def identify_archetypes(self, df):
        """Identify startup archetypes through clustering"""
        
        print("Identifying startup archetypes...")
        
        # Prepare features
        X, feature_names = self.prepare_clustering_features(df)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Separate successful and failed startups
        successful_mask = df['success'] == 1
        X_success = X_scaled[successful_mask]
        X_failure = X_scaled[~successful_mask]
        
        # Cluster successful startups to find winning archetypes
        print(f"\nClustering {len(X_success)} successful startups...")
        self.success_clusterer = KMeans(
            n_clusters=self.n_archetypes,
            random_state=42,
            n_init=10
        )
        success_labels = self.success_clusterer.fit_predict(X_success)
        
        # Cluster failed startups to find failure patterns
        print(f"Clustering {len(X_failure)} failed startups...")
        self.failure_clusterer = KMeans(
            n_clusters=self.n_archetypes,
            random_state=42,
            n_init=10
        )
        failure_labels = self.failure_clusterer.fit_predict(X_failure)
        
        # Analyze archetypes
        self._analyze_archetypes(
            X[successful_mask], 
            success_labels, 
            feature_names, 
            'success'
        )
        
        self._analyze_archetypes(
            X[~successful_mask], 
            failure_labels, 
            feature_names, 
            'failure'
        )
        
        # Apply PCA for visualization
        self.pca = PCA(n_components=2, random_state=42)
        X_pca = self.pca.fit_transform(X_scaled)
        
        return X_scaled, X_pca
    
    def _analyze_archetypes(self, X, labels, feature_names, archetype_type):
        """Analyze and name archetypes based on their characteristics"""
        
        print(f"\nAnalyzing {archetype_type} archetypes:")
        
        for i in range(self.n_archetypes):
            cluster_mask = labels == i
            cluster_data = X[cluster_mask]
            
            if len(cluster_data) == 0:
                continue
                
            # Calculate cluster profile
            profile = cluster_data.mean(axis=0)
            
            # Identify defining characteristics
            top_features_idx = np.argsort(np.abs(profile - X.mean(axis=0)))[-5:]
            
            # Create archetype description
            archetype_name = self._name_archetype(profile, feature_names, archetype_type, i)
            
            self.archetype_profiles[f"{archetype_type}_{i}"] = {
                'name': archetype_name,
                'size': len(cluster_data),
                'profile': profile,
                'defining_features': [feature_names[idx] for idx in top_features_idx]
            }
            
            print(f"  Archetype {i}: {archetype_name} (n={len(cluster_data)})")
    
    def _name_archetype(self, profile, feature_names, archetype_type, cluster_id):
        """Generate descriptive names for archetypes based on their profiles"""
        
        # Create feature lookup
        feature_dict = dict(zip(feature_names, profile))
        
        if archetype_type == 'success':
            # Success archetypes
            if (feature_dict.get('revenue_growth_rate_percent', 0) > 200 and 
                feature_dict.get('burn_multiple', 999) > 3):
                return "Blitzscaler"
            elif (feature_dict.get('gross_margin_percent', 0) > 70 and 
                  feature_dict.get('burn_multiple', 999) < 2):
                return "Efficient SaaS"
            elif feature_dict.get('product_retention_90d', 0) > 85:
                return "Product-Market Fit Star"
            elif feature_dict.get('prior_successful_exits_count', 0) > 1:
                return "Serial Entrepreneur"
            elif feature_dict.get('revenue_per_employee', 0) > 200000:
                return "High Productivity"
            elif feature_dict.get('net_dollar_retention_percent', 0) > 120:
                return "Expansion Machine"
            elif feature_dict.get('runway_months', 0) > 24:
                return "Well Capitalized"
            else:
                return f"Success Type {cluster_id}"
        else:
            # Failure archetypes
            if feature_dict.get('burn_multiple', 0) > 5:
                return "Cash Burner"
            elif feature_dict.get('customer_concentration_percent', 0) > 50:
                return "Customer Risk"
            elif feature_dict.get('runway_months', 999) < 6:
                return "Running on Fumes"
            elif feature_dict.get('product_retention_90d', 100) < 50:
                return "Poor Retention"
            elif feature_dict.get('revenue_growth_rate_percent', 999) < 50:
                return "Slow Growth"
            elif feature_dict.get('competition_intensity', 0) > 0.8:
                return "Fierce Competition"
            elif feature_dict.get('gross_margin_percent', 100) < 40:
                return "Low Margin"
            else:
                return f"Failure Type {cluster_id}"
    
    def create_cluster_features(self, df, X_scaled):
        """Create new features based on clustering"""
        
        print("\nCreating cluster-based features...")
        
        new_features = pd.DataFrame(index=df.index)
        
        # 1. Distance to each success archetype
        success_distances = self.success_clusterer.transform(X_scaled)
        for i in range(self.n_archetypes):
            archetype_name = self.archetype_profiles.get(f'success_{i}', {}).get('name', f'success_{i}')
            new_features[f'dist_to_{archetype_name.lower().replace(" ", "_")}'] = success_distances[:, i]
        
        # 2. Distance to nearest success archetype
        new_features['dist_to_nearest_success'] = success_distances.min(axis=1)
        
        # 3. Distance to each failure archetype
        failure_distances = self.failure_clusterer.transform(X_scaled)
        for i in range(self.n_archetypes):
            archetype_name = self.archetype_profiles.get(f'failure_{i}', {}).get('name', f'failure_{i}')
            new_features[f'dist_to_{archetype_name.lower().replace(" ", "_")}'] = failure_distances[:, i]
        
        # 4. Distance to nearest failure archetype
        new_features['dist_to_nearest_failure'] = failure_distances.min(axis=1)
        
        # 5. Success-failure distance ratio
        new_features['success_failure_ratio'] = (
            new_features['dist_to_nearest_failure'] / 
            (new_features['dist_to_nearest_success'] + 1e-6)
        )
        
        # 6. Archetype membership probabilities (softmax of negative distances)
        success_probs = np.exp(-success_distances) / np.exp(-success_distances).sum(axis=1, keepdims=True)
        new_features['max_success_archetype_prob'] = success_probs.max(axis=1)
        
        failure_probs = np.exp(-failure_distances) / np.exp(-failure_distances).sum(axis=1, keepdims=True)
        new_features['max_failure_archetype_prob'] = failure_probs.max(axis=1)
        
        # 7. Archetype uncertainty (entropy)
        success_entropy = -np.sum(success_probs * np.log(success_probs + 1e-6), axis=1)
        new_features['success_archetype_entropy'] = success_entropy
        
        # 8. Most likely success archetype (one-hot encoded)
        most_likely_success = np.argmax(success_probs, axis=1)
        for i in range(self.n_archetypes):
            archetype_name = self.archetype_profiles.get(f'success_{i}', {}).get('name', f'success_{i}')
            new_features[f'is_{archetype_name.lower().replace(" ", "_")}'] = (most_likely_success == i).astype(int)
        
        # 9. Transition risk score
        # Companies that are closer to failure patterns than success patterns
        new_features['transition_risk'] = (
            new_features['dist_to_nearest_success'] - 
            new_features['dist_to_nearest_failure']
        )
        
        # 10. Archetype stability score
        # How clearly a company belongs to one archetype vs being between archetypes
        new_features['archetype_clarity'] = (
            new_features['max_success_archetype_prob'] - 
            new_features['success_archetype_entropy'] / np.log(self.n_archetypes)
        )
        
        print(f"Created {len(new_features.columns)} cluster-based features")
        
        return new_features
    
    def visualize_clusters(self, X_pca, df, save_path='cluster_visualization.png'):
        """Visualize clusters in 2D PCA space"""
        
        plt.figure(figsize=(12, 5))
        
        # Plot 1: All startups colored by success
        plt.subplot(1, 2, 1)
        colors = ['red' if s == 0 else 'green' for s in df['success']]
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=colors, alpha=0.5, s=10)
        plt.title('Startups by Success (Red=Failed, Green=Success)')
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        
        # Plot 2: Success cluster centers
        plt.subplot(1, 2, 2)
        success_mask = df['success'] == 1
        X_pca_success = X_pca[success_mask]
        
        # Transform cluster centers to PCA space
        centers_scaled = self.success_clusterer.cluster_centers_
        centers_pca = self.pca.transform(centers_scaled)
        
        plt.scatter(X_pca_success[:, 0], X_pca_success[:, 1], 
                   c='lightgreen', alpha=0.3, s=10, label='Successful Startups')
        plt.scatter(centers_pca[:, 0], centers_pca[:, 1], 
                   c='darkgreen', s=200, marker='*', edgecolors='black', 
                   label='Success Archetypes')
        
        # Add archetype labels
        for i, (x, y) in enumerate(centers_pca):
            name = self.archetype_profiles.get(f'success_{i}', {}).get('name', f'Type {i}')
            plt.annotate(name, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.title('Success Archetypes')
        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
        
        print(f"Cluster visualization saved to {save_path}")

def main():
    print("="*60)
    print("Startup Archetype Clustering")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/final_100k_dataset_75features.csv')
    print(f"Loaded {len(df)} startups")
    
    # Initialize clusterer
    clusterer = StartupArchetypeClusterer(n_archetypes=8)
    
    # Identify archetypes
    X_scaled, X_pca = clusterer.identify_archetypes(df)
    
    # Create cluster features
    cluster_features = clusterer.create_cluster_features(df, X_scaled)
    
    # Combine with original data
    df_enhanced = pd.concat([df, cluster_features], axis=1)
    
    # Save enhanced dataset
    output_path = 'data/final_100k_dataset_with_clusters.csv'
    df_enhanced.to_csv(output_path, index=False)
    print(f"\nSaved enhanced dataset to {output_path}")
    
    # Visualize clusters
    clusterer.visualize_clusters(X_pca, df)
    
    # Print summary statistics
    print("\n" + "="*60)
    print("Clustering Summary")
    print("="*60)
    
    print("\nSuccess Archetypes:")
    for key, profile in clusterer.archetype_profiles.items():
        if key.startswith('success_'):
            print(f"  {profile['name']}: {profile['size']} startups")
            print(f"    Key features: {', '.join(profile['defining_features'][:3])}")
    
    print("\nFailure Archetypes:")
    for key, profile in clusterer.archetype_profiles.items():
        if key.startswith('failure_'):
            print(f"  {profile['name']}: {profile['size']} startups")
            print(f"    Key features: {', '.join(profile['defining_features'][:3])}")
    
    print(f"\nTotal new features created: {len(cluster_features.columns)}")
    print("="*60)

if __name__ == "__main__":
    main()