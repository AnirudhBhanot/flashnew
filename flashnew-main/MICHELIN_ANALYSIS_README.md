# Michelin Strategic Analysis API

## Overview

The Michelin Strategic Analysis API provides McKinsey/BCG-style strategic consulting analysis for startups using the Michelin 2018 case study framework. It leverages DeepSeek LLM to generate rich, narrative insights across three strategic phases.

## Features

### Three-Phase Strategic Analysis

#### Phase 1: Where Are We Now?
- **BCG Matrix Analysis**: Positions the company as Star, Cash Cow, Question Mark, or Dog
- **Porter's Five Forces**: Comprehensive competitive analysis
- **SWOT Analysis**: Detailed strengths, weaknesses, opportunities, and threats
- **Current Position Narrative**: Executive summary of the company's current state

#### Phase 2: Where Should We Go?
- **Ansoff Matrix Analysis**: Growth strategies across all four quadrants
- **Blue Ocean Strategy**: Identifies uncontested market opportunities
- **Growth Scenarios**: Conservative, Moderate, and Aggressive paths
- **Strategic Recommendation**: Clear direction with supporting rationale

#### Phase 3: How to Get There?
- **Balanced Scorecard**: KPIs across Financial, Customer, Internal Process, and Learning perspectives
- **OKR Framework**: Quarterly objectives and key results for execution
- **Resource Requirements**: Human, financial, technology, and partnership needs
- **Risk Mitigation Plan**: Top risks with mitigation strategies
- **Success Metrics**: Leading and lagging indicators

## API Endpoints

### POST `/api/michelin/analyze`
Performs comprehensive strategic analysis on startup data.

**Request Body:**
```json
{
  "startup_data": {
    "company_name": "string",
    "sector": "string",
    "funding_stage": "string",
    "annual_revenue_run_rate": 0,
    "revenue_growth_rate_percent": 0,
    "monthly_burn_usd": 0,
    "runway_months": 0,
    "team_size_full_time": 0,
    "customer_count": 0,
    "net_dollar_retention_percent": 0,
    "burn_multiple": 0,
    "target_market": "string (optional)",
    "key_competitors": ["string"] (optional),
    "unique_value_proposition": "string (optional)",
    "business_model": "string (optional)",
    "key_partnerships": ["string"] (optional),
    "technology_stack": ["string"] (optional)
  },
  "include_financial_projections": true,
  "analysis_depth": "comprehensive"
}
```

**Response:**
```json
{
  "company_name": "string",
  "analysis_date": "ISO 8601 datetime",
  "executive_briefing": "3-4 paragraph executive summary",
  "phase1": {
    "executive_summary": "string",
    "bcg_matrix_analysis": {},
    "porters_five_forces": {},
    "swot_analysis": {},
    "current_position_narrative": "string"
  },
  "phase2": {
    "strategic_options_overview": "string",
    "ansoff_matrix_analysis": {},
    "blue_ocean_strategy": {},
    "growth_scenarios": [],
    "recommended_direction": "string"
  },
  "phase3": {
    "implementation_roadmap": "string",
    "balanced_scorecard": {},
    "okr_framework": {},
    "resource_requirements": {},
    "risk_mitigation_plan": {},
    "success_metrics": []
  },
  "key_recommendations": ["string"],
  "critical_success_factors": ["string"],
  "next_steps": [
    {
      "timeline": "30 days",
      "actions": ["string"]
    }
  ]
}
```

### GET `/api/michelin/status`
Check service health and availability.

## Integration Guide

### 1. Add to Existing API Server

```python
# In your api_server.py
from api_michelin_llm_analysis import michelin_router, shutdown_michelin_engine

# Add router
app.include_router(michelin_router)

# Add shutdown handler
@app.on_event("shutdown")
async def shutdown_event():
    await shutdown_michelin_engine()
```

### 2. Environment Setup

The API uses the DeepSeek API key configured in the file:
```
DEEPSEEK_API_KEY=sk-f68b7148243e4663a31386a5ea6093cf
```

### 3. Frontend Integration

```typescript
interface MichelinAnalysis {
  company_name: string;
  analysis_date: string;
  executive_briefing: string;
  phase1: Phase1Analysis;
  phase2: Phase2Analysis;
  phase3: Phase3Analysis;
  key_recommendations: string[];
  critical_success_factors: string[];
  next_steps: NextStep[];
}

async function getMichelinAnalysis(startupData: StartupData): Promise<MichelinAnalysis> {
  const response = await fetch('/api/michelin/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey // if using API key auth
    },
    body: JSON.stringify({
      startup_data: startupData,
      analysis_depth: 'comprehensive'
    })
  });
  
  if (!response.ok) {
    throw new Error('Analysis failed');
  }
  
  return response.json();
}
```

## Testing

Run the test script to verify the integration:

```bash
python test_michelin_analysis.py
```

This will:
1. Create a sample startup profile
2. Run the full three-phase analysis
3. Display key results in the console
4. Save complete analysis to a JSON file

## Key Features

### Rich Narrative Output
- Each framework produces 2-3 paragraphs of contextual insight
- Analysis reads like a professional consulting report
- Connects frameworks to specific startup metrics

### Strategic Depth
- Goes beyond simple scores to provide actionable insights
- Considers industry context and competitive dynamics
- Provides specific, measurable recommendations

### Implementation Focus
- Quarterly OKRs for execution
- Resource planning and budgeting
- Risk assessment and mitigation strategies

## Example Use Cases

1. **Fundraising Preparation**: Generate comprehensive strategic analysis for investor decks
2. **Board Presentations**: Create executive-level strategic reports
3. **Strategic Planning**: Develop data-driven growth strategies
4. **Competitive Analysis**: Understand market position and opportunities

## Performance Considerations

- Analysis typically takes 20-30 seconds due to multiple LLM calls
- Results are comprehensive (typically 5,000-10,000 words)
- Consider caching results for repeated analysis of the same company

## Error Handling

The API includes comprehensive error handling:
- Retry logic for transient API failures
- Graceful fallback for parsing errors
- Detailed error messages for debugging

## Future Enhancements

1. **Caching Layer**: Redis-based caching for faster repeated analysis
2. **Batch Analysis**: Analyze multiple startups in parallel
3. **Industry Templates**: Pre-configured analysis for specific sectors
4. **Visual Reports**: PDF generation with charts and visualizations
5. **Comparative Analysis**: Compare multiple companies or scenarios