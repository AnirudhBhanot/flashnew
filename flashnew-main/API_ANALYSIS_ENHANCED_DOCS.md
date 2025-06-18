# Enhanced Analysis API Documentation

## Overview

The `/analyze` endpoint provides comprehensive, dynamic analysis of startup data based on real benchmarks from a dataset of 100,000+ startups. Unlike static analysis, this endpoint:

- Calculates real percentiles based on actual startup performance
- Provides personalized recommendations based on specific weaknesses
- Offers stage-specific and industry-specific insights
- Identifies success patterns and improvement opportunities
- Quantifies the impact of suggested improvements

## Endpoint Details

### URL
```
POST /analyze
```

### Authentication
Requires JWT token or API key

### Rate Limiting
10 requests per minute

### Request Format
Same as `/predict` endpoint - accepts all 45 startup features

### Response Format

```json
{
  "status": "success",
  "analysis": {
    "analysis_timestamp": "2024-01-15T10:30:00",
    "percentiles": {
      "revenue_growth_rate_percent": {
        "value": 180,
        "percentile": 75.3,
        "benchmark_median": 120,
        "benchmark_p75": 180,
        "benchmark_p90": 250
      },
      // ... other metrics
    },
    "recommendations": [
      {
        "category": "Financial Efficiency",
        "priority": "HIGH",
        "recommendation": "Improve burn efficiency",
        "specific_action": "Your burn multiple of 2.5 is in the bottom 40%. Focus on reducing costs or accelerating revenue growth.",
        "impact": "Could improve success probability by 15-20%",
        "benchmark": "Top quartile startups have burn multiple < 1.5"
      }
      // ... more recommendations
    ],
    "model_insights": {
      "model_weights": {
        "camp_evaluation": 0.50,
        "pattern_analysis": 0.20,
        "industry_specific": 0.20,
        "temporal_prediction": 0.10
      },
      "key_drivers": [
        {
          "model": "CAMP Evaluation",
          "weight": 0.50,
          "reason": "Early stage success heavily depends on team and market opportunity"
        }
      ],
      "confidence_factors": [
        "High data completeness (>90%) increases prediction accuracy",
        "Patent portfolio provides strong signal for tech differentiation"
      ]
    },
    "stage_insights": {
      "current_stage": "Series A",
      "stage_priorities": {
        "growth_metrics": 0.40,
        "unit_economics": 0.30,
        "market": 0.20,
        "team": 0.10
      },
      "success_factors": [
        "Predictable revenue growth",
        "Strong unit economics",
        "Scalable go-to-market strategy"
      ],
      "common_pitfalls": [
        "CAC payback period too long",
        "High customer churn",
        "Inability to scale efficiently"
      ],
      "stage_benchmarks": {
        "success_rate": 0.40,
        "team_size_full_time_median": 25,
        "runway_months_median": 24
      }
    },
    "industry_comparison": {
      "industry": "SaaS",
      "peer_performance": {
        "Revenue Growth": {
          "your_value": 180,
          "industry_median": 150,
          "performance": "above",
          "percentile_estimate": 75
        }
        // ... other metrics
      },
      "competitive_advantages": [
        "Revenue Growth above industry median",
        "Gross Margin above industry median"
      ],
      "improvement_areas": [
        "Burn Efficiency below industry median"
      ],
      "industry_specific_insights": {
        "key_metrics": ["MRR growth", "Net retention", "CAC payback"],
        "success_threshold": "Rule of 40 (growth + margin > 40%)"
      }
    },
    "pattern_insights": {
      "detected_patterns": [
        {
          "pattern": "B2B_SAAS_EFFICIENT",
          "confidence": 0.85,
          "description": "Efficient B2B SaaS growth pattern",
          "success_rate": 0.45
        }
      ],
      "pattern_recommendations": [
        {
          "pattern": "B2B_SAAS_EFFICIENT",
          "recommendation": "Focus on expanding within existing accounts"
        }
      ],
      "success_patterns": [
        {
          "pattern": "Strong expansion revenue",
          "insight": "NDR > 120% indicates excellent product-market fit and upsell capability"
        }
      ]
    },
    "improvement_opportunities": [
      {
        "metric": "burn_multiple",
        "current_value": 2.5,
        "current_percentile": 35,
        "target_value": 1.5,
        "target_percentile": 50,
        "estimated_success_lift": "+8.5%",
        "priority": "HIGH"
      }
      // ... other opportunities
    ],
    "benchmarks_used": {
      "total_startups": 100000,
      "industries_covered": ["SaaS", "E-commerce", "FinTech", "HealthTech", "AI/ML"],
      "stages_covered": ["Pre-seed", "Seed", "Series A", "Series B", "Series C+"]
    }
  },
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

## Key Features

### 1. Real Percentile Analysis
- Compares each metric against actual startup data
- Shows percentile ranking for key performance indicators
- Provides benchmark values (median, 75th, 90th percentile)

### 2. Personalized Recommendations
- Identifies specific weaknesses in the startup profile
- Prioritizes recommendations by potential impact
- Provides actionable steps with quantified benefits
- References industry benchmarks

### 3. Model Transparency
- Shows how different models contribute to the analysis
- Explains which factors drive the evaluation
- Lists confidence factors based on data quality

### 4. Stage-Specific Insights
- Tailored advice based on funding stage
- Stage-appropriate success factors
- Common pitfalls to avoid
- Relevant benchmarks for the stage

### 5. Industry Comparison
- Compares against industry-specific benchmarks
- Identifies competitive advantages
- Highlights areas needing improvement
- Provides industry-specific success criteria

### 6. Pattern Recognition
- Detects known success patterns
- Provides pattern-specific recommendations
- Shows historical success rates for patterns
- Identifies positive signals in the data

### 7. Improvement Roadmap
- Quantifies impact of improvements
- Prioritizes changes by potential benefit
- Sets realistic targets (50th percentile)
- Estimates success probability lift

## Use Cases

### For Investors
- Quickly assess startup performance vs. peers
- Identify key risks and opportunities
- Understand model reasoning
- Get data-driven improvement suggestions

### For Founders
- Benchmark against successful startups
- Get actionable improvement recommendations
- Understand investor evaluation criteria
- Prioritize areas for improvement

### For Accelerators
- Provide data-driven mentorship
- Track portfolio company progress
- Identify common weaknesses across cohort
- Customize support based on needs

## Integration Example

```python
import requests

# Prepare startup data
startup_data = {
    "funding_stage": "Series A",
    "sector": "SaaS",
    "revenue_growth_rate_percent": 150,
    "burn_multiple": 2.0,
    # ... all other required fields
}

# Make request
response = requests.post(
    "http://localhost:8001/analyze",
    json=startup_data,
    headers={"Authorization": "Bearer YOUR_JWT_TOKEN"}
)

if response.status_code == 200:
    analysis = response.json()["analysis"]
    
    # Extract key insights
    percentiles = analysis["percentiles"]
    recommendations = analysis["recommendations"]
    improvements = analysis["improvement_opportunities"]
    
    # Display top recommendations
    for rec in recommendations[:3]:
        print(f"[{rec['priority']}] {rec['recommendation']}")
        print(f"Action: {rec['specific_action']}")
        print(f"Impact: {rec['impact']}")
```

## Data Sources

The analysis is based on:
- 100,000+ real startup profiles
- Historical success/failure outcomes
- Industry-specific performance data
- Stage-specific benchmarks
- Pattern analysis from successful startups

## Limitations

1. **Data Recency**: Benchmarks are updated periodically but may not reflect very recent market changes
2. **Industry Coverage**: Some niche industries may have limited benchmark data
3. **Geographic Bias**: Dataset may have geographic biases based on data sources
4. **Survivorship Bias**: Successful startups are overrepresented in later stages

## Future Enhancements

1. **Real-time Benchmarks**: Live updates as new data becomes available
2. **Peer Group Analysis**: Compare against custom peer groups
3. **Trend Analysis**: Show how benchmarks change over time
4. **Scenario Planning**: What-if analysis for improvements
5. **Custom Recommendations**: Industry/stage specific action plans