#!/usr/bin/env python3
"""
Analyze score distributions from different models in the FLASH system
"""

import json
import requests
import numpy as np
import pandas as pd
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns

# Test cases representing different startup profiles
test_cases = {
    "Strong Startup": {
        "funding_stage": "series_a",
        "monthly_burn_usd": 200000,
        "runway_months": 24,
        "revenue_usd": 500000,
        "revenue_growth_rate_percent": 40,
        "gross_margin_percent": 80,
        "customer_acquisition_cost_usd": 200,
        "lifetime_value_usd": 5000,
        "arr_usd": 6000000,
        "market_size_usd": 10000000000,
        "market_growth_rate_percent": 50,
        "product_stage": "growth",
        "team_size": 25,
        "founder_experience_years": 15,
        "technical_team_percent": 60,
        "sales_team_percent": 20,
        "customer_churn_rate_percent": 2,
        "nps_score": 80,
        "cash_balance_usd": 4800000,
        "industry": "SaaS",
        "location": "San Francisco"
    },
    "Average Startup": {
        "funding_stage": "seed",
        "monthly_burn_usd": 100000,
        "runway_months": 12,
        "revenue_usd": 50000,
        "revenue_growth_rate_percent": 20,
        "gross_margin_percent": 70,
        "customer_acquisition_cost_usd": 500,
        "lifetime_value_usd": 2000,
        "arr_usd": 600000,
        "market_size_usd": 1000000000,
        "market_growth_rate_percent": 25,
        "product_stage": "beta",
        "team_size": 8,
        "founder_experience_years": 10,
        "technical_team_percent": 50,
        "sales_team_percent": 25,
        "customer_churn_rate_percent": 5,
        "nps_score": 50,
        "cash_balance_usd": 1200000,
        "industry": "SaaS",
        "location": "San Francisco"
    },
    "Weak Startup": {
        "funding_stage": "pre_seed",
        "monthly_burn_usd": 50000,
        "runway_months": 6,
        "revenue_usd": 5000,
        "revenue_growth_rate_percent": 10,
        "gross_margin_percent": 50,
        "customer_acquisition_cost_usd": 1000,
        "lifetime_value_usd": 800,
        "arr_usd": 60000,
        "market_size_usd": 100000000,
        "market_growth_rate_percent": 10,
        "product_stage": "mvp",
        "team_size": 3,
        "founder_experience_years": 2,
        "technical_team_percent": 66,
        "sales_team_percent": 0,
        "customer_churn_rate_percent": 15,
        "nps_score": 20,
        "cash_balance_usd": 300000,
        "industry": "SaaS",
        "location": "Other"
    }
}

def test_api_endpoint(data: Dict) -> Dict:
    """Test the API endpoint and get detailed results"""
    # First try the advanced endpoint
    try:
        response = requests.post(
            "http://localhost:8001/predict_advanced",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Fallback to enhanced endpoint
    try:
        response = requests.post(
            "http://localhost:8001/predict_enhanced",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return None

def analyze_model_scores():
    """Analyze score distributions across different models"""
    results = []
    
    print("Testing different startup profiles...\n")
    
    for profile_name, data in test_cases.items():
        print(f"\n{profile_name}:")
        print("-" * 50)
        
        # Get prediction
        result = test_api_endpoint(data)
        
        if result:
            # Extract scores
            success_prob = result.get('success_probability', 0)
            camp_scores = result.get('camp_scores', {})
            model_predictions = result.get('model_predictions', {})
            model_consensus = result.get('model_consensus', 0)
            
            print(f"Overall Success Probability: {success_prob:.1%}")
            print(f"Verdict: {result.get('verdict', 'Unknown')}")
            print(f"Model Consensus: {model_consensus:.2f}")
            
            print("\nCAMP Scores:")
            for pillar, score in camp_scores.items():
                print(f"  {pillar.capitalize()}: {score:.1%}")
            
            if model_predictions:
                print("\nModel Predictions:")
                for model, pred in model_predictions.items():
                    print(f"  {model}: {pred:.1%}")
            
            # Calculate CAMP average
            camp_avg = np.mean(list(camp_scores.values())) if camp_scores else 0
            
            # Store results
            results.append({
                'profile': profile_name,
                'success_probability': success_prob,
                'camp_average': camp_avg,
                'capital_score': camp_scores.get('capital', 0),
                'advantage_score': camp_scores.get('advantage', 0),
                'market_score': camp_scores.get('market', 0),
                'people_score': camp_scores.get('people', 0),
                'verdict': result.get('verdict', 'Unknown'),
                **{f'model_{k}': v for k, v in model_predictions.items()}
            })
    
    # Create DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Generate visualizations
    if len(results) > 0:
        plt.figure(figsize=(15, 10))
        
        # Plot 1: CAMP scores vs Overall probability
        plt.subplot(2, 2, 1)
        x = np.arange(len(df))
        width = 0.15
        
        plt.bar(x - 2*width, df['capital_score'], width, label='Capital', color='gold')
        plt.bar(x - width, df['advantage_score'], width, label='Advantage', color='lightblue')
        plt.bar(x, df['market_score'], width, label='Market', color='lightgreen')
        plt.bar(x + width, df['people_score'], width, label='People', color='coral')
        plt.bar(x + 2*width, df['success_probability'], width, label='Overall', color='darkred', alpha=0.7)
        
        plt.xlabel('Startup Profile')
        plt.ylabel('Score')
        plt.title('CAMP Scores vs Overall Success Probability')
        plt.xticks(x, df['profile'])
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Model predictions distribution
        plt.subplot(2, 2, 2)
        model_cols = [col for col in df.columns if col.startswith('model_')]
        if model_cols:
            model_data = df[model_cols].values.T
            plt.boxplot(model_data, labels=[col.replace('model_', '') for col in model_cols])
            plt.xlabel('Model')
            plt.ylabel('Prediction')
            plt.title('Model Prediction Distribution')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        
        # Plot 3: CAMP average vs Success probability
        plt.subplot(2, 2, 3)
        plt.scatter(df['camp_average'], df['success_probability'], s=100)
        for i, txt in enumerate(df['profile']):
            plt.annotate(txt, (df['camp_average'].iloc[i], df['success_probability'].iloc[i]))
        plt.xlabel('CAMP Average Score')
        plt.ylabel('Overall Success Probability')
        plt.title('CAMP Average vs Success Probability')
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Score breakdown table
        plt.subplot(2, 2, 4)
        plt.axis('tight')
        plt.axis('off')
        
        # Create summary table
        summary_data = []
        for _, row in df.iterrows():
            summary_data.append([
                row['profile'],
                f"{row['camp_average']:.1%}",
                f"{row['success_probability']:.1%}",
                row['verdict']
            ])
        
        table = plt.table(cellText=summary_data,
                         colLabels=['Profile', 'CAMP Avg', 'Success Prob', 'Verdict'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        plt.title('Summary Table')
        
        plt.tight_layout()
        plt.savefig('model_score_distribution.png', dpi=150, bbox_inches='tight')
        print("\n\nVisualization saved as 'model_score_distribution.png'")
        
        # Print correlation analysis
        print("\n\nCorrelation Analysis:")
        print("-" * 50)
        if len(df) > 1:
            print(f"Correlation between CAMP average and success probability: {df['camp_average'].corr(df['success_probability']):.3f}")
            
            # Calculate gap
            df['gap'] = df['camp_average'] - df['success_probability']
            print(f"\nAverage gap between CAMP and success probability: {df['gap'].mean():.1%}")
            print(f"Max gap: {df['gap'].max():.1%}")
            print(f"Min gap: {df['gap'].min():.1%}")

if __name__ == "__main__":
    analyze_model_scores()