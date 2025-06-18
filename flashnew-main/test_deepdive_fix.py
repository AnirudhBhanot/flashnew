#!/usr/bin/env python3
import asyncio
import os
import sys
import json
from llm_analysis import LLMAnalysisEngine

async def test_competitive_analysis():
    # Initialize the engine
    engine = LLMAnalysisEngine()
    
    # This is the actual data that's being sent from the frontend
    context = {
        "porters_five_forces": {
            "supplier_power": {
                "rating": "Medium",
                "factors": ["Limited suppliers"],
                "score": 6.5
            },
            "buyer_power": {
                "rating": "High", 
                "factors": ["Many alternatives"],
                "score": 7.8
            },
            "competitive_rivalry": {
                "rating": "High",
                "factors": ["Many competitors"],
                "score": 8.2
            },
            "threat_of_substitution": {
                "rating": "Medium",
                "factors": ["Some alternatives"],
                "score": 5.5
            },
            "threat_of_new_entry": {
                "rating": "Low",
                "factors": ["High barriers"],
                "score": 3.2
            }
        },
        "internal_audit": {
            "strengths": ["Strong team"],
            "weaknesses": ["Limited marketing"],
            "opportunities": ["Growing market"],
            "threats": ["Economic uncertainty"]
        }
    }
    
    print("Testing analyze_competitive_position with actual data...")
    print(f"Context: {json.dumps(context, indent=2)}")
    print("\n" + "="*50 + "\n")
    
    try:
        result = await engine.analyze_competitive_position(context)
        print("✓ Success! Got result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    await engine.close()

if __name__ == "__main__":
    # Set up logging to see debug messages
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    asyncio.run(test_competitive_analysis())