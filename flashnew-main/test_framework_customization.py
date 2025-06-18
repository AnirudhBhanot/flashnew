#!/usr/bin/env python3
"""
Test to verify framework customization is working
"""

import asyncio
import json
from strategic_context_engine import StrategicContextEngine
from intelligent_framework_selector import IntelligentFrameworkSelector

async def test_framework_customization():
    """Test framework selection and customization"""
    
    # Initialize components
    context_engine = StrategicContextEngine()
    framework_selector = IntelligentFrameworkSelector()
    
    # Test data for different industries
    test_cases = [
        {
            "name": "SaaS B2B Company",
            "data": {
                "startup_name": "TestSaaS",
                "sector": "saas_b2b",
                "stage": "seed",
                "revenue": 1000000,
                "growth_rate": 100,
                "burn_rate": 150000,
                "ltv_cac_ratio": 3.0,
                "net_revenue_retention": 115
            }
        },
        {
            "name": "Marketplace Company", 
            "data": {
                "startup_name": "TestMarket",
                "sector": "marketplace",
                "stage": "series_a",
                "revenue": 5000000,
                "growth_rate": 150,
                "burn_rate": 500000,
                "gmv": 50000000,
                "take_rate": 0.15
            }
        },
        {
            "name": "FinTech Company",
            "data": {
                "startup_name": "TestFinTech",
                "sector": "fintech",
                "stage": "seed",
                "revenue": 2000000,
                "growth_rate": 80,
                "burn_rate": 300000,
                "transaction_volume": 100000000
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test_case['name']}")
        print(f"{'='*60}")
        
        # Build context
        context = await context_engine.build_company_context(test_case['data'])
        print(f"\nContext built for {context.industry} company at {context.stage} stage")
        
        # Select frameworks
        frameworks = await framework_selector.select_frameworks(context, max_frameworks=3)
        print(f"\nSelected {len(frameworks)} frameworks:")
        
        for i, framework in enumerate(frameworks, 1):
            print(f"\n{i}. {framework.base_framework.name}")
            print(f"   Base ID: {framework.base_framework.id}")
            print(f"   Industry Variant: {framework.industry_variant}")
            
            # Check for industry-specific customizations
            if framework.customizations.get("industry_adjustments"):
                print(f"   Industry Adjustments: {json.dumps(framework.customizations['industry_adjustments'], indent=6)}")
            
            # Check metrics
            print(f"   Specific Metrics: {framework.specific_metrics[:3] if len(framework.specific_metrics) > 3 else framework.specific_metrics}")
            
            # Check thresholds
            if framework.thresholds:
                print(f"   Thresholds: {json.dumps(dict(list(framework.thresholds.items())[:3]), indent=6)}")
                
        # Check if BCG Matrix has industry customization
        bcg_framework = next((f for f in frameworks if f.base_framework.id == "bcg_matrix"), None)
        if bcg_framework:
            print(f"\n--- BCG Matrix Customization Details ---")
            if test_case['data']['sector'] == 'saas_b2b':
                print("Expected: SaaS Growth-Share Matrix with NRR/ARR axes")
            elif test_case['data']['sector'] == 'marketplace':
                print("Expected: Marketplace Dynamics Matrix with Take Rate/GMV axes")
            elif test_case['data']['sector'] == 'fintech':
                print("Expected: FinTech Portfolio Matrix with Revenue per User axes")
            
            print(f"Actual customizations: {json.dumps(bcg_framework.customizations, indent=4)}")

if __name__ == "__main__":
    print("Testing Framework Customization...")
    print("This will verify if industry-specific variants are being applied\n")
    asyncio.run(test_framework_customization())