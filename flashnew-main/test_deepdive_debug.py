#!/usr/bin/env python3
import asyncio
import os
from llm_analysis import LLMAnalysisEngine

async def test_competitive_analysis():
    # Initialize the engine
    engine = LLMAnalysisEngine()
    
    context = {
        "analysis_type": "competitive_position",
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
    
    try:
        result = await engine.analyze_competitive_position(context)
        print("Success! Result type:", result.get("type"))
        print("Overall rating:", result.get("position_assessment", {}).get("overall_rating"))
    except Exception as e:
        print(f"Error: {e}")
    
    await engine.close()

if __name__ == "__main__":
    asyncio.run(test_competitive_analysis())