#!/usr/bin/env python3
"""
Integration guide for adding Michelin analysis to existing API server
"""

# Add this to your existing API server file (e.g., api_server_unified.py)

# 1. Import the Michelin router
from api_michelin_llm_analysis import michelin_router, shutdown_michelin_engine

# 2. Add the router to your FastAPI app
# Add this after other router includes
app.include_router(michelin_router)

# 3. Add cleanup handler for graceful shutdown
# Add this to your existing shutdown handler
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    # ... existing cleanup code ...
    
    # Add Michelin engine cleanup
    await shutdown_michelin_engine()
    
    logger.info("Michelin analysis engine shut down")

# Example of how to call the endpoint:
"""
POST /api/michelin/analyze

Request Body:
{
  "startup_data": {
    "company_name": "CloudSync AI",
    "sector": "SaaS",
    "funding_stage": "Series A",
    "annual_revenue_run_rate": 2400000,
    "revenue_growth_rate_percent": 180,
    "monthly_burn_usd": 150000,
    "runway_months": 18,
    "team_size_full_time": 25,
    "customer_count": 120,
    "net_dollar_retention_percent": 125,
    "burn_multiple": 0.75,
    "target_market": "Mid-market B2B companies",
    "key_competitors": ["Zapier", "Workato"],
    "unique_value_proposition": "AI-driven data mapping",
    "business_model": "Subscription SaaS"
  },
  "include_financial_projections": true,
  "analysis_depth": "comprehensive"
}

Response:
{
  "company_name": "CloudSync AI",
  "analysis_date": "2024-01-15T10:30:00",
  "executive_briefing": "CloudSync AI stands at a critical inflection point...",
  "phase1": {
    "executive_summary": "...",
    "bcg_matrix_analysis": {...},
    "porters_five_forces": {...},
    "swot_analysis": {...},
    "current_position_narrative": "..."
  },
  "phase2": {
    "strategic_options_overview": "...",
    "ansoff_matrix_analysis": {...},
    "blue_ocean_strategy": {...},
    "growth_scenarios": [...],
    "recommended_direction": "..."
  },
  "phase3": {
    "implementation_roadmap": "...",
    "balanced_scorecard": {...},
    "okr_framework": {...},
    "resource_requirements": {...},
    "risk_mitigation_plan": {...},
    "success_metrics": [...]
  },
  "key_recommendations": [...],
  "critical_success_factors": [...],
  "next_steps": [...]
}
"""

# Frontend integration example:
"""
// In your React/TypeScript frontend

async function getMichelinAnalysis(startupData: StartupData) {
  try {
    const response = await fetch('/api/michelin/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-api-key' // if using API key auth
      },
      body: JSON.stringify({
        startup_data: startupData,
        include_financial_projections: true,
        analysis_depth: 'comprehensive'
      })
    });
    
    if (!response.ok) {
      throw new Error('Analysis failed');
    }
    
    const analysis = await response.json();
    return analysis;
    
  } catch (error) {
    console.error('Michelin analysis error:', error);
    throw error;
  }
}
"""