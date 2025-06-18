# Michelin Strategic Analysis - Technical Documentation

## Overview
The Michelin Strategic Analysis is a comprehensive three-phase business analysis system inspired by Michelin-star restaurant evaluations. It provides deep strategic insights for startups using AI-powered analysis through the DeepSeek API.

## Architecture

### Three Implementation Approaches

#### 1. Original Approach (`api_michelin_llm_analysis.py`)
- **Endpoint**: `/api/michelin/analyze/phase{1,2,3}`
- **Method**: Generates complex nested JSON in single API call
- **Issues**: Prone to JSON parsing errors, timeouts with complex structures
- **Status**: Legacy, not recommended

#### 2. Decomposed Approach (`api_michelin_decomposed.py`) - RECOMMENDED
- **Endpoint**: `/api/michelin/decomposed/analyze/phase{1,2,3}`
- **Method**: Breaks analysis into focused components
- **Benefits**: Reliable, graceful fallbacks, no JSON parsing issues
- **Performance**: ~40s per phase
- **Key Features**:
  - Simple focused prompts for each component
  - Parallel API calls where possible
  - Intelligent fallbacks based on startup metrics
  - Frontend-compatible data structures

#### 3. Strategic Approach (`api_michelin_strategic.py`)
- **Endpoint**: `/api/michelin/strategic/analyze/phase{1,2,3}`
- **Method**: Intelligent phase interconnection with context
- **Benefits**: Deeper insights, strategic coherence across phases
- **Performance**: Phase 1 (~40s), Phase 2 (~35s), Phase 3 (~10s)
- **Key Features**:
  - `StrategicContext` class maintains insights
  - Each phase builds on previous analysis
  - Programmatic structure generation
  - True McKinsey-style strategic thinking

## Phase Structure

### Phase 1: Situational Analysis (Where Are We?)
- **Executive Summary**: 2-paragraph strategic overview
- **BCG Matrix Analysis**: Position (Star/Cash Cow/Question Mark/Dog) with implications
- **Porter's Five Forces**: Industry competitive dynamics
- **SWOT Analysis**: With strategic priorities
- **Current Position Narrative**: Executive briefing

### Phase 2: Strategic Options (Where Could We Go?)
- **Strategic Options Overview**: Three paths with recommendations
- **Ansoff Matrix Analysis**: Growth strategy selection
- **Blue Ocean Strategy**: ERRC grid (Eliminate/Reduce/Raise/Create)
- **Growth Scenarios**: Conservative/Base/Aggressive with probabilities
- **Recommended Direction**: Primary strategic focus

### Phase 3: Implementation Roadmap (How Do We Get There?)
- **Implementation Roadmap**: 90-day detailed plan
- **Balanced Scorecard**: Four perspectives with KPIs
- **OKR Framework**: Quarterly objectives and key results
- **Resource Requirements**: Financial, human, tech needs
- **Risk Mitigation Plan**: Key risks and mitigation strategies
- **Success Metrics**: Measurable outcomes with timeframes

## API Contract

### Request Structure
```typescript
// Phase 1 Request
{
  startup_data: StartupData,
  include_financial_projections?: boolean,
  analysis_depth?: 'basic' | 'comprehensive'
}

// Phase 2 Request
{
  startup_data: StartupData,
  phase1_results: Phase1Analysis
}

// Phase 3 Request
{
  startup_data: StartupData,
  phase1_results: Phase1Analysis,
  phase2_results: Phase2Analysis
}
```

### Response Structure
```typescript
// Phase Response
{
  startup_name: string,
  analysis_date: string,
  phase1?: Phase1Analysis,  // Only in Phase 1 response
  phase2?: Phase2Analysis,  // Only in Phase 2 response
  phase3?: Phase3Analysis,  // Only in Phase 3 response
  executive_briefing?: string,
  key_recommendations?: string[],
  critical_success_factors?: string[],
  next_steps?: Array<{title: string, description: string, priority: string}>
}
```

## Strategic Context (Strategic Approach Only)

The `StrategicContext` class maintains evolving insights:

```python
class StrategicContext:
    insights = {
        "core_challenge": str,           # Primary challenge to address
        "competitive_position": str,      # BCG position
        "key_advantages": List[str],      # Top 2 strengths
        "critical_constraints": List[str], # Major limitations
        "strategic_imperatives": List[str], # Must-do actions
        "strategic_focus": str,           # Chosen Ansoff strategy
        "chosen_path": str,               # Selected growth scenario
        "key_metrics": {                  # Calculated metrics
            "ltv_cac_ratio": float,
            "burn_multiple": float,
            "market_position": str
        }
    }
```

## Frontend Integration

### Feature Flag Configuration
```typescript
// config/features.ts
export const featureFlags = {
  michelinAnalysisApproach: 'decomposed' as 'decomposed' | 'original' | 'strategic',
  michelinAnalysisDebugMode: false,
  michelinAnalysisComparisonMode: false,
};
```

### Endpoint Selection
```typescript
export const getMichelinEndpoint = (phase: 1 | 2 | 3): string => {
  const baseUrl = 'http://localhost:8001/api/michelin';
  const approach = featureFlags.michelinAnalysisApproach;
  
  if (approach === 'decomposed') {
    return `${baseUrl}/decomposed/analyze/phase${phase}`;
  } else if (approach === 'strategic') {
    return `${baseUrl}/strategic/analyze/phase${phase}`;
  } else {
    return `${baseUrl}/analyze/phase${phase}`;
  }
};
```

## Implementation Details

### Decomposed Approach Methods
- `get_bcg_position()`: Simple BCG quadrant determination
- `get_bcg_implications()`: Strategic implications of position
- `get_porter_force()`: Individual force analysis
- `get_swot_items()`: Focused SWOT component generation
- `get_strategic_priorities()`: Priority generation with fallbacks
- `get_ansoff_strategy()`: Growth strategy selection
- `get_blue_ocean_items()`: ERRC grid components

### Strategic Approach Enhancements
- Context-aware prompt generation
- Phase interconnection logic
- Insight extraction and accumulation
- Strategic coherence validation
- Programmatic structure building

## Error Handling

### Common Issues and Solutions

1. **JSON Parsing Errors**
   - Original: Regex syntax errors, malformed JSON
   - Solution: Decomposed approach with simple text responses

2. **Timeout Issues**
   - Original: 60s→120s timeouts still failing
   - Solution: Phase-by-phase loading, focused prompts

3. **Data Structure Mismatches**
   - Original: Frontend expects different fields
   - Solution: Programmatic structure generation

4. **Router Conflicts**
   - Original: Multiple routers with same prefix
   - Solution: Unique prefixes for each approach

## Performance Optimization

### Decomposed Approach
- Parallel API calls for independent components
- Caching of intermediate results
- Fallback chains for reliability
- Average 40s per phase

### Strategic Approach
- Context reuse across phases
- Intelligent prompt construction
- Reduced token usage through focused questions
- Phase 3 optimization through context

## Testing

### Test Files
- `test_frontend_ready.py`: Validates frontend compatibility
- `test_strategic_michelin.py`: End-to-end strategic testing
- `test_decomposed.py`: Component-level testing

### Key Test Cases
1. Frontend field validation
2. Phase interconnection
3. Fallback behavior
4. Error recovery
5. Performance benchmarks

## Deployment Considerations

### Environment Variables
```bash
DEEPSEEK_API_KEY="sk-f68b7148243e4663a31386a5ea6093cf"
DEEPSEEK_API_URL="https://api.deepseek.com/v1/chat/completions"
```

### API Server Registration
```python
# api_server_unified.py
app.include_router(decomposed_router)  # Recommended
app.include_router(strategic_router)   # Advanced
app.include_router(michelin_router)    # Legacy
```

### Monitoring
- Request duration logging
- Error rate tracking
- DeepSeek API usage
- Fallback activation rates

## Migration Guide

### From Original to Decomposed
1. Update feature flag: `michelinAnalysisApproach: 'decomposed'`
2. No frontend changes required
3. Monitor for improved reliability

### From Decomposed to Strategic
1. Update feature flag: `michelinAnalysisApproach: 'strategic'`
2. Verify phase interconnection
3. Monitor for deeper insights

## Future Enhancements

1. **Caching Strategy**
   - Redis integration for phase results
   - Context persistence across sessions

2. **Advanced Analytics**
   - Industry-specific insights
   - Competitive benchmarking
   - Trend analysis integration

3. **UI Enhancements**
   - Real-time progress indicators
   - Interactive strategy selection
   - Comparative analysis views

## Troubleshooting

### Common Issues

1. **"Analysis in progress - data processing error occurred"**
   - Check for router conflicts
   - Verify API endpoints
   - Check server logs for details

2. **Frontend displays empty sections**
   - Verify data structure alignment
   - Check for missing required fields
   - Enable debug mode for details

3. **Timeout errors**
   - Switch to decomposed approach
   - Check DeepSeek API status
   - Monitor server resources

### Debug Mode
Enable in `config/features.ts`:
```typescript
michelinAnalysisDebugMode: true
```

This logs all API requests/responses to console.

## API Usage Examples

### Phase 1 Request
```bash
curl -X POST http://localhost:8001/api/michelin/decomposed/analyze/phase1 \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {
      "startup_name": "TestCo",
      "sector": "technology",
      "funding_stage": "seed",
      "annual_revenue_usd": 100000,
      ...
    }
  }'
```

### Phase 2 Request (with Phase 1 results)
```bash
curl -X POST http://localhost:8001/api/michelin/decomposed/analyze/phase2 \
  -H "Content-Type: application/json" \
  -d '{
    "startup_data": {...},
    "phase1_results": {...}
  }'
```

## Conclusion

The Michelin Strategic Analysis system provides flexible, reliable, and intelligent business analysis for startups. The three-tier approach allows teams to choose between reliability (decomposed), intelligence (strategic), or legacy compatibility (original) based on their needs.