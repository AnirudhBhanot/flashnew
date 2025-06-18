#!/usr/bin/env python3
"""
Test framework selection for FLASH itself
"""

import asyncio
import json
import sys
sys.path.insert(0, '/Users/sf/Desktop/FLASH')

from strategic_context_engine import StrategicContextEngine
from intelligent_framework_selector import IntelligentFrameworkSelector

async def test_flash_frameworks():
    """Test framework selection for FLASH platform"""
    
    context_engine = StrategicContextEngine()
    framework_selector = IntelligentFrameworkSelector()
    
    # FLASH platform data with competitive challenges
    flash_data = {
        "startup_name": "FLASH Platform",
        "sector": "ai_ml",
        "stage": "series_a",
        "revenue": 2000000,
        "growth_rate": 150,
        "burn_rate": 300000,
        "ltv_cac_ratio": 3.5,
        "competition_intensity": 4,
        "key_challenges": ["Market differentiation", "Competitive positioning", "Customer acquisition"]
    }
    
    print(f"Testing framework selection for FLASH Platform...")
    print(f"Sector: {flash_data['sector']}")
    print(f"Stage: {flash_data['stage']}")
    print(f"Challenges: {flash_data['key_challenges']}")
    
    context = await context_engine.build_company_context(flash_data)
    
    # Override challenges to ensure they're set
    context.key_challenges = flash_data['key_challenges']
    
    frameworks = await framework_selector.select_frameworks(context, max_frameworks=5)
    
    print(f"\n\nSelected {len(frameworks)} frameworks for FLASH:")
    for i, fw in enumerate(frameworks, 1):
        print(f"\n{i}. {fw.base_framework.name}")
        print(f"   ID: {fw.base_framework.id}")
        print(f"   Category: {fw.base_framework.category.value}")
        print(f"   Industry Variant: {fw.industry_variant}")
        
        # Check if industry-specific customizations exist
        if fw.customizations.get("industry_adjustments"):
            print(f"   Has Industry Customizations: Yes")
        
        # Show rationale if available
        if hasattr(fw, 'rationale'):
            print(f"   Why selected: {fw.rationale}")

if __name__ == "__main__":
    asyncio.run(test_flash_frameworks())