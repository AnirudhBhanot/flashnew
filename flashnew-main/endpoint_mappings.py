
# Add these endpoint mappings to api_server_working.py

@app.route("/predict_simple", methods=["POST"])
async def predict_simple(request: Request):
    """Alias for /predict endpoint for frontend compatibility"""
    return await predict(request)

@app.route("/predict_advanced", methods=["POST"])
async def predict_advanced(request: Request):
    """Alias for /predict_enhanced endpoint for frontend compatibility"""
    return await predict_enhanced(request)

@app.route("/investor_profiles", methods=["GET"])
async def investor_profiles():
    """Return investor profile templates"""
    profiles = {
        "conservative": {
            "name": "Conservative Investor",
            "risk_tolerance": "low",
            "preferred_stages": ["series_b", "series_c"],
            "preferred_metrics": {
                "burn_multiple": {"max": 1.5},
                "runway_months": {"min": 18},
                "gross_margin_percent": {"min": 70}
            }
        },
        "aggressive": {
            "name": "Aggressive Growth Investor",
            "risk_tolerance": "high",
            "preferred_stages": ["seed", "series_a"],
            "preferred_metrics": {
                "revenue_growth_rate_percent": {"min": 100},
                "user_growth_rate_percent": {"min": 50}
            }
        },
        "balanced": {
            "name": "Balanced Investor",
            "risk_tolerance": "medium",
            "preferred_stages": ["series_a", "series_b"],
            "preferred_metrics": {
                "burn_multiple": {"max": 2.0},
                "ltv_cac_ratio": {"min": 3.0}
            }
        }
    }
    return {"profiles": profiles}
