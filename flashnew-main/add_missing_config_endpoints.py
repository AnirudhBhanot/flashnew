#!/usr/bin/env python3
"""
Add missing config endpoints to the API
"""

# Add these endpoints to api_server_unified.py after the existing config endpoints

@app.get("/config/success-thresholds")
async def get_success_thresholds():
    """Get success probability thresholds"""
    return {
        "strong_pass": 0.75,
        "pass": 0.60,
        "conditional_pass": 0.40,
        "fail": 0.20,
        "strong_fail": 0.0
    }

@app.get("/config/model-weights")
async def get_model_weights():
    """Get model ensemble weights"""
    return {
        "dna_analyzer": 0.25,
        "temporal_model": 0.25,
        "industry_model": 0.25,
        "ensemble_model": 0.25
    }

@app.get("/config/revenue-benchmarks")
async def get_revenue_benchmarks():
    """Get revenue benchmarks by stage"""
    return {
        "pre_seed": {
            "min": 0,
            "target": 10000,
            "excellent": 50000
        },
        "seed": {
            "min": 10000,
            "target": 100000,
            "excellent": 500000
        },
        "series_a": {
            "min": 100000,
            "target": 1000000,
            "excellent": 3000000
        },
        "series_b": {
            "min": 1000000,
            "target": 5000000,
            "excellent": 10000000
        }
    }

@app.get("/config/company-comparables")
async def get_company_comparables():
    """Get comparable company data"""
    return {
        "unicorns": [
            {"name": "Stripe", "valuation": 95000000000, "category": "Fintech"},
            {"name": "SpaceX", "valuation": 150000000000, "category": "Aerospace"},
            {"name": "Databricks", "valuation": 43000000000, "category": "Data/AI"}
        ],
        "decacorns": [
            {"name": "ByteDance", "valuation": 225000000000, "category": "Social"},
            {"name": "Ant Group", "valuation": 150000000000, "category": "Fintech"}
        ]
    }

@app.get("/config/display-limits")
async def get_display_limits():
    """Get UI display limits"""
    return {
        "max_chart_points": 100,
        "max_table_rows": 50,
        "animation_duration_ms": 500,
        "decimal_places": 2
    }

print("""
To add these endpoints:
1. Copy the code above
2. Add it to api_server_unified.py after the existing config endpoints
3. The API will then have all required config endpoints
""")