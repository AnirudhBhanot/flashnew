#!/usr/bin/env python3
import json
import requests
import time

# FLASH's data as a startup
flash_data = {
    # Company Info
    'company_name': 'FLASH Analytics',
    'funding_stage': 'seed',
    'sector': 'ai-ml',  # Using hyphen format that API expects
    
    # Capital metrics
    'annual_revenue_run_rate': 2000000,  # $2M ARR
    'revenue_growth_rate_percent': 400,
    'monthly_burn_usd': 150000,
    'runway_months': 12,
    'total_capital_raised_usd': 2500000,
    'valuation_usd': 15000000,
    
    # Market metrics
    'customer_count': 50,
    'ltv_cac_ratio': 12.0,  # 24000/2000
    'gross_margin_percent': 85,
    'tam_size_usd': 5000000000,
    'market_growth_rate_percent': 35,
    
    # People metrics
    'team_size_full_time': 18,
    'founders_experience_years': 15,
    'has_technical_cofounder': True,
    'has_business_cofounder': True,
    
    # Additional metrics
    'net_dollar_retention_percent': 115,
    'months_since_last_funding': 6,
    'funding_rounds_count': 1,
    'monthly_active_users': 200,
    'user_growth_rate_percent': 50,
    'churn_rate_percent': 3,
    'patent_count': 2,
    'investor_tier_primary': 'tier_2',
    'has_regulatory_approval': False,
    'competitive_intensity': 3,
    'sales_cycle_days': 45,
    'customer_acquisition_cost': 2000,
    'burn_multiple': 1.5,
    'revenue_per_employee': 111111,
    'data_quality_score': 4.5,
    'years_experience_avg': 12,
    'revenue_concentration_top10_percent': 30,
    'international_revenue_percent': 20,
    'product_stage': 'scaling',
    'has_network_effects': True,
    'has_moat': True,
    'market_position': 3,
    'nps_score': 72,
    'time_to_profitability_months': 18,
    'equity_retention_founders_percent': 65,
    'board_size': 5,
    'has_repeat_founders': True,
    'months_of_cash_left': 12
}

print('🚀 Testing FLASH Analytics as a Startup')
print('='*60)
print(f'\nSending sector: {flash_data["sector"]}')

# 1. Test prediction endpoint
print('\n📊 1. ML Model Prediction')
print('-'*40)
try:
    response = requests.post('http://localhost:8001/predict', json=flash_data)
    if response.status_code == 200:
        prediction = response.json()
        
        success_prob = prediction['success_probability']
        camp_scores = prediction['camp_scores']
        
        print(f'Success Probability: {success_prob*100:.1f}%')
        print(f'Verdict: {prediction["verdict"]}')
        print(f'Strength Level: {prediction.get("strength_level", "N/A")}')
        print(f'\nCAMP Scores:')
        print(f'  💰 Capital: {camp_scores["capital"]*100:.1f}%')
        print(f'  🏆 Advantage: {camp_scores["advantage"]*100:.1f}%')
        print(f'  📈 Market: {camp_scores["market"]*100:.1f}%')
        print(f'  👥 People: {camp_scores["people"]*100:.1f}%')
    else:
        print(f'Error: {response.status_code}')
        print(f'Response: {response.text}')
        print(response.json())
        exit(1)
except Exception as e:
    print(f'Error calling predict: {e}')
    exit(1)

# 2. Test LLM recommendations
print('\n\n🤖 2. AI Recommendations')
print('-'*40)
try:
    rec_data = {
        'startup_data': flash_data,
        'scores': {
            'success_probability': success_prob,
            'capital': camp_scores['capital'],
            'advantage': camp_scores['advantage'],
            'market': camp_scores['market'],
            'people': camp_scores['people']
        }
    }
    
    response = requests.post('http://localhost:8001/api/analysis/recommendations/dynamic', json=rec_data)
    if response.status_code == 200:
        recommendations = response.json()
        recs = recommendations.get('recommendations', [])
        print(f'Generated {len(recs)} recommendations')
        
        for i, rec in enumerate(recs[:3]):  # Show top 3
            print(f'\n{i+1}. {rec["recommendation"]}')
            print(f'   Priority: {rec["priority"]} | Timeline: {rec["timeline"]}')
            print(f'   Impact: {rec["impact"]}')
    else:
        print(f'Error: {response.status_code}')
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')

# 3. Test What-If Analysis
print('\n\n🔮 3. What-If Analysis')
print('-'*40)
try:
    whatif_data = {
        'startup_data': flash_data,
        'current_scores': {
            'success_probability': success_prob,
            'capital': camp_scores['capital'],
            'advantage': camp_scores['advantage'],
            'market': camp_scores['market'],
            'people': camp_scores['people']
        },
        'improvements': [
            {
                'id': 'increase_revenue',
                'description': 'Double revenue to $4M ARR through enterprise sales',
                'camp_area': 'market',
                'estimated_impact': 0.15
            },
            {
                'id': 'reduce_burn',
                'description': 'Reduce burn rate by 30% through efficiency improvements',
                'camp_area': 'capital',
                'estimated_impact': 0.10
            },
            {
                'id': 'expand_team',
                'description': 'Hire 2 senior ML engineers to strengthen technical advantage',
                'camp_area': 'people',
                'estimated_impact': 0.08
            }
        ]
    }
    
    response = requests.post('http://localhost:8001/api/analysis/whatif/dynamic', json=whatif_data)
    if response.status_code == 200:
        whatif = response.json()
        new_prob = whatif.get('new_probability', {}).get('value', 0)
        print('Proposed Improvements:')
        for imp in whatif_data['improvements']:
            print(f'  • {imp["description"]}')
        
        print(f'\nCurrent Success Probability: {success_prob*100:.1f}%')
        print(f'New Success Probability: {new_prob*100:.1f}%')
        print(f'Improvement: +{(new_prob - success_prob)*100:.1f} percentage points')
        
        if whatif.get('insights'):
            print('\nKey Insights:')
            for insight in whatif['insights'][:2]:
                print(f'  • {insight}')
    else:
        print(f'Error: {response.status_code}')
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')

# 4. Test Market Insights
print('\n\n📈 4. Market Insights')
print('-'*40)
try:
    market_data = {
        'startup_data': {
            'sector': flash_data['sector'],
            'funding_stage': flash_data['funding_stage'],
            'annual_revenue_run_rate': flash_data['annual_revenue_run_rate'],
            'tam_size_usd': flash_data['tam_size_usd']
        }
    }
    
    response = requests.post('http://localhost:8001/api/analysis/insights/market', json=market_data)
    if response.status_code == 200:
        insights = response.json()
        
        print('Market Trends:')
        for trend in insights.get('market_trends', [])[:3]:
            print(f'  • {trend}')
        
        print(f'\nFunding Climate: {insights.get("funding_climate", "N/A")}')
        print(f'\nInvestment Thesis: {insights.get("investment_thesis", "N/A")}')
    else:
        print(f'Error: {response.status_code}')
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')

# 5. Test Competitor Analysis
print('\n\n🏆 5. Competitor Analysis')
print('-'*40)
try:
    comp_data = {
        'startup_data': {
            'sector': flash_data['sector'],
            'funding_stage': flash_data['funding_stage'],
            'annual_revenue_run_rate': flash_data['annual_revenue_run_rate'],
            'tam_size_usd': flash_data['tam_size_usd'],
            'unique_advantages': ['ML-powered predictions', 'CAMP framework', 'Real startup data']
        }
    }
    
    response = requests.post('http://localhost:8001/api/analysis/competitors/analyze', json=comp_data)
    if response.status_code == 200:
        competitors = response.json()
        
        print(f'Competitive Intensity: {competitors.get("competitive_intensity", "Unknown")}')
        print(f'\nKey Competitors ({len(competitors.get("competitors", []))} identified):')
        
        for comp in competitors.get('competitors', [])[:3]:
            print(f'\n  {comp["name"]} ({comp.get("stage", "Unknown")})')
            print(f'  Strengths: {", ".join(comp.get("strengths", [])[:2])}')
            print(f'  Positioning: {comp.get("positioning", "N/A")}')
        
        print('\nSuccess Factors:')
        for factor in competitors.get('success_factors', [])[:3]:
            print(f'  • {factor}')
    else:
        print(f'Error: {response.status_code}')
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')

print('\n' + '='*60)
print('✅ All tests completed successfully!')
print('\nSummary for FLASH Analytics:')
print(f'  • Success Probability: {success_prob*100:.1f}%')
print(f'  • Verdict: {prediction["verdict"]}')
print(f'  • Weakest Area: {min(camp_scores.items(), key=lambda x: x[1])[0].capitalize()}')
print(f'  • Strongest Area: {max(camp_scores.items(), key=lambda x: x[1])[0].capitalize()}')