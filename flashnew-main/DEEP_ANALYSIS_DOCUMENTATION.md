# Deep Framework Analysis System Documentation

## Overview

The Deep Framework Analysis system provides Michelin-style strategic analysis by combining strategic frameworks with DeepSeek AI to generate detailed, actionable insights for startups. This system goes beyond basic framework positioning to provide comprehensive implementation plans, success metrics, and industry benchmarks.

## Key Features

### 1. **Enhanced Framework Analysis**
- Detailed situation analysis with peer comparisons
- Strategic implications and growth options
- Comprehensive implementation roadmaps
- Success metrics with industry benchmarks
- Risk assessment and mitigation strategies
- Expected outcomes with confidence intervals

### 2. **Multi-Framework Integration**
- Analyze multiple frameworks simultaneously
- Identify patterns across different strategic lenses
- Resolve contradictions between frameworks
- Surface hidden opportunities
- Create unified action plans

### 3. **Customizable Analysis Depth**
- **Quick**: 5-10 minute analysis for rapid insights
- **Standard**: 10-15 minute balanced analysis
- **Comprehensive**: 15-20 minute detailed consulting-grade analysis

## API Endpoints

### 1. Deep Framework Analysis
```
POST /api/frameworks/deep-analysis
```

Performs comprehensive strategic analysis using selected frameworks.

**Request Body:**
```json
{
  "startup_data": {
    "startup_name": "TechVenture AI",
    "sector": "SaaS",
    "funding_stage": "Series A",
    "annual_revenue_usd": 2400000,
    "revenue_growth_rate_percent": 150,
    "monthly_burn_usd": 180000,
    "runway_months": 14,
    "team_size_full_time": 25,
    "tam_size_usd": 5000000000,
    // ... other startup metrics
  },
  "framework_ids": ["bcg_matrix", "ansoff_matrix", "porters_five_forces"],
  "analysis_depth": "comprehensive",
  "include_implementation_plan": true,
  "include_metrics": true,
  "include_benchmarks": true
}
```

**Response:**
```json
{
  "startup_name": "TechVenture AI",
  "analysis_date": "2024-01-15T10:30:00Z",
  "executive_summary": "Detailed executive summary...",
  "framework_analyses": [
    {
      "framework_id": "bcg_matrix",
      "framework_name": "BCG Growth-Share Matrix",
      "category": "Strategic",
      "position": "Star",
      "score": 0.78,
      "detailed_analysis": {
        "situation_deep_dive": {
          "position_interpretation": "As a Star, TechVenture AI combines high market growth with strong market share...",
          "driving_factors": [
            {
              "factor": "150% revenue growth",
              "impact": "High",
              "evidence": "3x industry average for Series A SaaS"
            }
          ],
          "peer_comparison": "Top quartile compared to Series A SaaS companies",
          "unique_aspects": ["Strong product-market fit", "Efficient growth engine"],
          "critical_gaps": ["International expansion", "Enterprise features"]
        },
        "strategic_implications": {
          "time_horizon_impact": {
            "next_6_months": "Focus on maintaining growth momentum",
            "6_12_months": "Prepare for Series B with unit economics improvement",
            "12_24_months": "Establish market leadership position"
          },
          "strategic_options": [
            {
              "option": "Aggressive market expansion",
              "description": "Double down on growth in current market",
              "feasibility": "High",
              "resource_requirements": "$3M funding, 15 hires",
              "expected_roi": "3x revenue in 18 months"
            }
          ],
          "recommended_direction": {
            "primary_strategy": "Invest heavily to maintain Star position",
            "rationale": "Market window is open, competitors are emerging",
            "success_factors": ["Maintain product velocity", "Scale sales team"]
          }
        }
      },
      "implementation_plan": {
        "phase1": {
          "timeline": "0-3 months",
          "objectives": ["Scale sales team", "Launch v2.0"],
          "critical_actions": [
            {
              "action": "Hire 5 enterprise sales reps",
              "owner": "VP Sales",
              "deadline": "Week 4"
            }
          ],
          "resource_needs": {
            "budget": "$500k",
            "headcount": 8,
            "tools": ["Salesforce", "Gong.io"]
          },
          "success_criteria": ["10 enterprise pilots", "Sales pipeline >$5M"],
          "potential_blockers": ["Talent availability", "Product readiness"]
        }
      },
      "success_metrics": [
        {
          "metric": "Monthly Recurring Revenue",
          "current_value": "$200k",
          "target_6m": "$400k",
          "target_12m": "$800k",
          "target_18m": "$1.5M",
          "measurement_method": "Stripe dashboard",
          "owner": "CFO",
          "type": "Lagging"
        }
      ],
      "industry_benchmarks": {
        "peer_performance": {
          "revenue_growth": "50-70% for Series A SaaS",
          "burn_multiple": "1.5-2.0x typical",
          "team_size": "20-30 average",
          "time_to_next_round": "12-18 months"
        },
        "best_in_class": {
          "revenue_growth": ">200% (Zoom, Slack at this stage)",
          "efficiency_metrics": "Burn multiple <1.5x",
          "key_differentiators": ["Product-led growth", "Viral coefficient >1"]
        }
      },
      "strategic_recommendations": [
        "Double sales team within 90 days to capture market opportunity",
        "Launch enterprise tier with 3x pricing by Q2",
        "Establish partnerships with 2 major SIs within 6 months"
      ],
      "risk_factors": [
        {
          "risk": "Competitor raises mega-round",
          "probability": "Medium",
          "impact": "High",
          "mitigation": "Accelerate customer acquisition, build moat features",
          "trigger_point": "If competitor raises >$50M"
        }
      ],
      "expected_outcomes": {
        "6_months": {
          "revenue": "$2.4M ARR",
          "team_size": 40,
          "market_position": "Top 3 in category",
          "key_milestones": ["100 enterprise customers", "SOC2 compliance"],
          "confidence": "70-80%"
        }
      }
    }
    // ... additional framework analyses
  ],
  "integrated_insights": {
    "cross_framework_patterns": [
      "All frameworks indicate strong growth position but execution risk",
      "Consistent theme of needing to build competitive moats"
    ],
    "strategic_tensions": [
      {
        "tension": "Growth vs. Efficiency trade-off",
        "resolution": "Maintain growth focus for next 6 months, then optimize"
      }
    ],
    "hidden_opportunities": [
      "Platform play potential identified across multiple frameworks",
      "International expansion earlier than typical"
    ],
    "critical_decisions": [
      {
        "decision": "Growth strategy: PLG vs. Enterprise sales",
        "timeline": "Next 30 days",
        "criteria": "CAC payback, market feedback, competitive dynamics"
      }
    ]
  },
  "prioritized_actions": [
    {
      "action": "Scale enterprise sales team from 3 to 10 reps",
      "priority": 1,
      "impact": "High",
      "effort": "Medium",
      "timeline": "3 months",
      "owner": "VP Sales",
      "dependencies": ["Sales playbook completion"],
      "success_metrics": ["Pipeline growth 3x", "Win rate >25%"]
    }
  ],
  "implementation_roadmap": {
    "immediate": {
      "timeline": "Next 30 days",
      "focus": "Foundation building",
      "key_initiatives": ["Hire sales leadership", "Launch customer success"],
      "quick_wins": ["Automate onboarding", "Launch referral program"]
    },
    "short_term": {
      "timeline": "30-90 days",
      "focus": "Scaling core operations",
      "key_initiatives": ["Double sales team", "Launch enterprise features"],
      "critical_milestones": ["$300k MRR", "50 enterprise leads"]
    },
    "medium_term": {
      "timeline": "3-9 months",
      "focus": "Market leadership",
      "key_initiatives": ["International expansion", "Platform APIs"],
      "scaling_priorities": ["Tier 1 support", "Partner channel"]
    }
  },
  "success_probability": 72,
  "success_drivers": [
    "Strong product-market fit validated by 125% NDR",
    "Experienced team with prior successful exits",
    "Large and growing TAM with clear customer pain"
  ],
  "key_risks": [
    {
      "risk": "Sales execution at scale",
      "probability": "Medium",
      "impact": "High",
      "mitigation": "Hire experienced VP Sales from similar company",
      "early_warning": "Sales cycle lengthening beyond 45 days"
    }
  ],
  "monitoring_plan": {
    "weekly_metrics": ["New ARR", "Sales pipeline", "Product usage", "Burn rate"],
    "monthly_reviews": ["Unit economics", "Competitive win/loss"],
    "quarterly_assessments": ["Market position", "Strategic progress"],
    "decision_triggers": [
      {
        "condition": "If burn multiple exceeds 2.5x",
        "action": "Implement efficiency measures"
      }
    ],
    "feedback_mechanisms": ["Customer advisory board", "Investor updates"]
  }
}
```

### 2. Quick Framework Insights
```
POST /api/frameworks/quick-insights/{framework_id}
```

Get rapid strategic insights for a single framework.

### 3. Analysis Templates
```
GET /api/frameworks/analysis-templates
```

Retrieve pre-configured analysis templates for common scenarios.

## Integration Guide

### Backend Integration

1. **Install Dependencies**
```bash
pip install aiohttp tenacity
```

2. **Configure API Key**
Set the DeepSeek API key in your environment or configuration:
```python
DEEPSEEK_API_KEY = "sk-f68b7148243e4663a31386a5ea6093cf"
```

3. **Import and Use**
```python
from api_framework_deep_analysis import deep_analysis_router
app.include_router(deep_analysis_router)
```

### Frontend Integration

1. **Install Axios**
```bash
npm install axios
```

2. **Create Service Class**
```typescript
class DeepAnalysisService {
  async performDeepAnalysis(request: DeepAnalysisRequest): Promise<DeepAnalysisResponse> {
    const response = await axios.post('/api/frameworks/deep-analysis', request);
    return response.data;
  }
}
```

3. **Implement UI Component**
See `frontend_deep_analysis_integration.tsx` for a complete React component example.

## Use Cases

### 1. **Investment Due Diligence**
- Analyze potential investments using multiple strategic frameworks
- Get detailed risk assessments and growth projections
- Compare against industry benchmarks

### 2. **Strategic Planning**
- Annual planning sessions with comprehensive framework analysis
- Identify strategic options and trade-offs
- Create detailed implementation roadmaps

### 3. **Board Presentations**
- Generate executive-level strategic summaries
- Provide data-driven recommendations
- Show clear action plans with metrics

### 4. **Competitive Analysis**
- Use Porter's Five Forces for detailed competitive landscape
- Identify differentiation opportunities
- Plan competitive responses

## Best Practices

1. **Framework Selection**
   - Use 3-5 frameworks for comprehensive analysis
   - Mix strategic, operational, and market frameworks
   - Consider startup stage when selecting frameworks

2. **Analysis Depth**
   - Use "quick" for regular monitoring
   - Use "standard" for monthly reviews
   - Use "comprehensive" for major decisions

3. **Data Quality**
   - Provide complete and accurate startup data
   - Update data regularly for trend analysis
   - Include both quantitative and qualitative inputs

4. **Action Planning**
   - Focus on top 5 prioritized actions
   - Assign clear ownership and deadlines
   - Set up monitoring systems immediately

## Performance Considerations

- **API Response Time**: 
  - Quick analysis: 10-30 seconds
  - Standard analysis: 30-60 seconds
  - Comprehensive analysis: 60-120 seconds

- **Rate Limits**:
  - 10 requests per minute per API key
  - 100 requests per hour per API key

- **Caching**:
  - Results are cached for 1 hour
  - Force refresh with `force_refresh: true` parameter

## Error Handling

Common error responses:
- `400`: Invalid request parameters
- `401`: Invalid API key
- `429`: Rate limit exceeded
- `500`: Server error (retry with exponential backoff)

## Support

For issues or questions:
1. Check the API logs for detailed error messages
2. Verify your API key is valid and has sufficient credits
3. Ensure all required startup data fields are provided
4. Contact support with request ID for investigation