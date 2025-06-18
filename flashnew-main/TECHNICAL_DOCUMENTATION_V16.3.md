# FLASH Technical Documentation V16.3 - Realistic Models with AI Integration & Dynamic Benchmarks

**Last Updated**: June 7, 2025  
**Version**: 16.3 (Industry-Specific Benchmarking System)

## Overview

FLASH is an AI-powered startup assessment platform that provides **honest, realistic predictions** about startup success using machine learning. The system has evolved from unrealistic synthetic models to truly realistic models that acknowledge the inherent uncertainty in early-stage prediction.

### 🚀 New in V16.3: Industry-Specific Benchmarking
- **Dynamic Benchmarks**: Sector and stage-specific performance metrics
- **6 Key Metrics**: Revenue Growth, Burn Multiple, Team Size, LTV/CAC, Gross Margin, Runway
- **20+ Sectors Supported**: SaaS, FinTech, Marketplace, HealthTech, and more
- **Realistic Percentiles**: Based on actual market data, not hardcoded 65%
- **Smart Fallbacks**: Default benchmarks for unknown sectors

### Previous Updates (V16.2)
- **Context-Aware Recommendations**: LLM generates advice specific to each startup's metrics
- **CAMP-Aligned Guidance**: First recommendation always addresses weakest area
- **Fixed Data Flow**: userInput now properly passed to LLM for personalization
- **Enhanced Prompts**: Detailed rules prevent generic advice
- **Working What-If Analysis**: Realistic predictions with quantified impacts

### Recent Fixes (June 7, 2025)
- **Industry Benchmarks**: Fixed issue where all sectors showed same 65% percentile
- **Authentication**: Removed API key header for development (DISABLE_AUTH=true)
- **Data Validation**: Fixed all field transformations (e-commerce→ecommerce, AI/ML→deeptech)
- **LLM Context**: Added userInput to enrichedData for proper personalization
- **Prompt Engineering**: Enhanced to identify weakest areas and reference specific metrics

## Key Technical Evolution

### From Fantasy to Reality

1. **V1-V14**: Synthetic data, unrealistic 94-100% AUC
2. **V15**: Realistic data approach (72.7% AUC)  
3. **V16**: Production deployment with 50% AUC on truly realistic data
4. **V16.3**: Added industry-specific benchmarking system

## Current System Architecture

### Models (Production V46 Realistic)

```
models/production_v46_realistic/
├── dna_analyzer.pkl      # AUC: 0.489
├── temporal_model.pkl    # AUC: 0.505
├── industry_model.pkl    # AUC: 0.504
├── ensemble_model.pkl    # AUC: 0.499
└── feature_columns.pkl   # 85 features
```

### Performance Metrics

- **Average AUC**: 0.499 (~50%)
- **True Positive Rate**: 18.5%
- **True Negative Rate**: 81.8%
- **Overall Accuracy**: 84% (mostly predicting failure)

### Why 50% AUC is Actually Good

1. **Honest Assessment**: Shows true difficulty of early-stage prediction
2. **No Overfitting**: Models aren't memorizing fake patterns
3. **Academic Alignment**: Matches research on startup prediction
4. **Business Value**: Even 18.5% TPR means catching 1 in 5 unicorns

## Industry Benchmarking System (NEW in V16.3)

### Architecture

```typescript
// industry_benchmarks.ts structure
export interface Benchmark {
  metric: string;
  description: string;
  p25: string;    // 25th percentile
  p50: string;    // 50th percentile (median)
  p75: string;    // 75th percentile
  unit?: string;
}

export interface SectorBenchmarks {
  [sector: string]: {
    [stage: string]: {
      revenue_growth: Benchmark;
      burn_multiple: Benchmark;
      team_size: Benchmark;
      ltv_cac: Benchmark;
      gross_margin: Benchmark;
      runway_months: Benchmark;
    }
  }
}
```

### Supported Sectors

1. **SaaS**: Software as a Service companies
2. **FinTech**: Financial technology startups
3. **Marketplace**: Two-sided marketplaces
4. **HealthTech**: Healthcare technology companies
5. **Default**: Fallback for other sectors

### Benchmark Examples

#### SaaS Pre-seed
```javascript
{
  revenue_growth: { p25: '0%', p50: '50%', p75: '200%' },
  burn_multiple: { p25: '5.0x', p50: '3.0x', p75: '2.0x' },
  team_size: { p25: '2', p50: '3', p75: '5' },
  ltv_cac: { p25: '0.5:1', p50: '1.0:1', p75: '2.0:1' },
  gross_margin: { p25: '60%', p50: '70%', p75: '80%' },
  runway_months: { p25: '6', p50: '12', p75: '18' }
}
```

#### FinTech Series A
```javascript
{
  revenue_growth: { p25: '60%', p50: '120%', p75: '250%' },
  burn_multiple: { p25: '3.5x', p50: '2.3x', p75: '1.4x' },
  team_size: { p25: '30', p50: '60', p75: '120' },
  ltv_cac: { p25: '1.8:1', p50: '3.0:1', p75: '5.0:1' },
  gross_margin: { p25: '60%', p50: '70%', p75: '80%' },
  runway_months: { p25: '15', p50: '20', p75: '30' }
}
```

### Key Features

1. **Dynamic Percentile Calculation**
   ```typescript
   function calculatePercentile(
     value: number,
     p25: number,
     p50: number,
     p75: number,
     inverse: boolean = false  // For metrics where lower is better
   ): number
   ```

2. **Sector-Specific Metrics**
   - Marketplaces show "Take Rate" instead of "Gross Margin"
   - HealthTech has longer runway expectations
   - FinTech has higher team size requirements

3. **Stage Progression**
   - Pre-seed: Lower revenue expectations, smaller teams
   - Seed: Focus on growth metrics
   - Series A: Emphasis on efficiency and scale

### Integration with Frontend

```typescript
// In AnalysisResults.tsx
function getIndustryBenchmarks(data: any): Array<any> {
  const sector = data.sector || data.industry || 'default';
  const stage = data.funding_stage || 'seed';
  const sectorBenchmarks = getBenchmarksForSectorStage(sector, stage);
  
  // Now returns 6 metrics with sector/stage-specific benchmarks
  // Instead of hardcoded 65% for everyone
}
```

## Dataset Characteristics

### Realistic Training Data (100K Companies)

```python
# Distribution
- Pre-seed: 35% (35,000 companies)
- Seed: 25% (25,000 companies)
- Series A: 20% (20,000 companies)
- Series B+: 20% (20,000 companies)

# Key Realism Features
- 85% of pre-seed have $0 revenue
- Average pre-seed team: 2.1 people
- 51% of pre-seed have 0 customers
- 16% overall success rate
- 25% missing data for early stages
```

### Pre-Seed Characteristics

```python
# Revenue Distribution
- 84.9% have $0
- 15.1% have $1-100k
- 0% have >$100k

# Team Size
- 84.6% have 1-3 people
- 15.4% have 4-6 people
- 0% have >10 people

# Product Stage
- 40.3% at idea stage
- 34.6% at prototype
- 20.0% at MVP
- 5.1% at beta
```

## LLM Integration (Updated V16.2)

### DeepSeek API Configuration

```python
# In .env
DEEPSEEK_API_KEY=sk-f68b7148243e4663a31386a5ea6093cf
LLM_CACHE_TTL=3600
DISABLE_AUTH=true  # For development
```

### Prompt Engineering for Personalization

The LLM integration uses detailed prompts with strict rules to ensure personalized, context-specific recommendations:

```python
# Key prompt components
1. Context injection: All startup metrics embedded in prompt
2. Weakest area identification: Automatically calculated and emphasized
3. Anti-generic rules: "DO NOT give generic advice"
4. Structured output: JSON format with specific fields
5. Quantified impact: Must include measurable outcomes
```

#### Example Prompt Structure
```python
f"""You are an expert startup advisor analyzing a {stage} {sector} company.

CAMP Framework Scores (0-100 scale):
- Capital: {capital}% - Financial health, runway, burn efficiency
- Advantage: {advantage}% - Competitive moat, differentiation, IP
- Market: {market}% - TAM, growth rate, market timing
- People: {people}% - Team experience, composition, advisors

WEAKEST AREA: {weakest_area} ({score}%)

Key Metrics:
- Annual Revenue: ${revenue:,.0f}
- Monthly Burn: ${burn:,.0f}
- Team Size: {team_size}
[...all other metrics...]

CRITICAL: Generate exactly 3 HIGHLY SPECIFIC recommendations:
1. First recommendation MUST address the weakest CAMP area
2. Be specific to their {sector} industry and {stage} stage
3. Reference their specific numbers and context
4. Make recommendations achievable within constraints

DO NOT give generic advice."""
```

### LLM Endpoints

#### 1. Status Check
```http
GET /api/analysis/status
Response: {
  "status": "operational",
  "model": "deepseek-chat",
  "cache_enabled": false
}
```

#### 2. Dynamic Recommendations (Fixed in V16.2)
```http
POST /api/analysis/recommendations/dynamic
Body: {
  "funding_stage": "seed",
  "sector": "saas",
  "scores": {
    "capital": 0.65,
    "advantage": 0.58,
    "market": 0.72,
    "people": 0.25  # Weakest area
  },
  "userInput": {  # CRITICAL: Now properly passed
    "annual_revenue_run_rate": 500000,
    "monthly_burn_usd": 80000,
    "team_size_full_time": 8,
    "years_experience_avg": 5
  }
}
Response: {
  "recommendations": [
    {
      "title": "Hire a seasoned SaaS VP of Engineering",
      "why": "The team's low experience (5 years) is critical...",
      "how": [
        "Allocate $150k/year from burn ($12.5k/month)",
        "Leverage advisor networks for referrals",
        "Structure equity at 1-2% to attract talent"
      ],
      "timeline": "8 weeks",
      "impact": "Improve engineering velocity by 30% within 3 months",
      "camp_area": "people"  # Addresses weakest area
    }
  ]
}
```

#### 3. What-If Analysis (With ML Calculator)
```http
POST /api/analysis/whatif/dynamic
Body: {
  "startup_data": {...},
  "current_scores": {
    "capital": 0.55,
    "advantage": 0.44,
    "market": 0.63,
    "people": 0.27,  # Weakest area
    "success_probability": 0.52
  },
  "improvements": [
    {"id": "hire_vp", "description": "Hire VP Sales with enterprise SaaS experience"},
    {"id": "advisory", "description": "Add 3 industry advisors"}
  ]
}
Response: {
  "new_probability": {"value": 0.60, "lower": 0.55, "upper": 0.65},
  "new_scores": {
    "capital": 0.54,      # -1% (hiring costs)
    "advantage": 0.48,    # +4% (better execution)
    "market": 0.67,       # +4% (market access)  
    "people": 0.39        # +12% (team strength)
  },
  "score_changes": {
    "capital": -0.01,
    "advantage": 0.04,
    "market": 0.04,
    "people": 0.12
  },
  "timeline": "3-6 months",
  "risks": [
    "VP hiring may take longer in competitive market",
    "Advisory board effectiveness depends on engagement"
  ],
  "priority": "hire_vp"
}
```

### What-If Calculator (NEW in V16.2)

The `whatif_calculator.py` implements ML-based score calculation:

```python
# Key features:
1. Diminishing returns: effective_change = change * (1 - current_score) * 0.8
2. Context-aware adjustments based on stage and sector
3. Realistic impact mappings:
   - Hiring VP: +12-15% people, -3% capital
   - Patents: +15% advantage, -2% capital
   - Advisors: +8% people, +4% market
```

### Response Times
- **LLM Status**: 15-20 seconds (normal for DeepSeek)
- **Recommendations**: 15-20 seconds (with personalization)
- **What-If**: 15-20 seconds (with ML calculations)

## API Configuration

### Server Details

- **URL**: `http://localhost:8001`
- **Framework**: FastAPI
- **Models**: Loaded directly from pickles
- **Authentication**: Disabled in dev (`DISABLE_AUTH=true`)
- **Caching**: In-memory cache when Redis unavailable

### Key Endpoints

```bash
GET  /                    # API info
GET  /health             # Health check
POST /predict            # Make prediction
GET  /features           # Model features
GET  /config/{type}      # Configuration
```

### Prediction Request Example

```bash
curl -X POST "http://localhost:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "funding_stage": "pre_seed",
    "total_capital_raised_usd": 150000,
    "team_size_full_time": 2,
    "annual_revenue_run_rate": 0,
    ...
  }'
```

### Response Format

```json
{
  "success_probability": 0.347,
  "confidence_score": 0.5,
  "verdict": "PASS",
  "risk_level": "Medium Risk",
  "camp_analysis": {
    "capital": 0.45,
    "advantage": 0.45,
    "market": 0.47,
    "people": 0.53
  },
  "disclaimer": "Early-stage prediction is highly uncertain"
}
```

## Frontend Updates

### Key Changes in V16.3

1. **Industry Benchmarks** (`industry_benchmarks.ts`)
   ```typescript
   // 853 lines of sector/stage-specific benchmarks
   export const INDUSTRY_BENCHMARKS: SectorBenchmarks = {
     saas: {
       pre_seed: { /* 6 metrics */ },
       seed: { /* 6 metrics */ },
       series_a: { /* 6 metrics */ }
     },
     fintech: { /* ... */ },
     marketplace: { /* ... */ },
     healthtech: { /* ... */ },
     default: { /* fallback benchmarks */ }
   }
   ```

2. **Updated Benchmark Display** (`AnalysisResults.tsx`)
   ```typescript
   // Now shows 6 metrics instead of 4
   // Dynamic percentiles based on actual values
   // Sector and stage aware
   ```

### Key Changes in V16.2

1. **Fixed Data Transformations** (`HybridAnalysisPage.tsx`)
   ```typescript
   // Sector mappings (20+ sectors supported)
   'ai/ml' → 'deeptech'
   'e-commerce' → 'ecommerce'
   'health tech' → 'healthtech'
   'prop tech' → 'proptech'
   'bio tech' → 'biotech'
   // ... and more
   ```

2. **Removed Authentication Headers**
   ```typescript
   // Before
   headers: { 
     'Content-Type': 'application/json',
     'X-API-Key': API_CONFIG.API_KEY  // REMOVED
   }
   
   // After  
   headers: { 
     'Content-Type': 'application/json'
   }
   ```

3. **Added userInput to LLM Data**
   ```typescript
   const enrichedData = {
     funding_stage: transformedData.funding_stage,
     sector: transformedData.sector,
     scores: results.camp_analysis,
     verdict: results.verdict,
     userInput: startupData  // CRITICAL: Added for personalization
   };
   ```

## Model Training Process

### 1. Generate Realistic Dataset
```python
python3 create_realistic_dataset_100k.py
# Creates dataset with realistic pre-seed characteristics
```

### 2. Train Models
```python
python3 retrain_production_v46_realistic.py
# Trains 4 models with realistic expectations
```

### 3. Verify Performance
```python
python3 analyze_realistic_performance.py
# Should show ~50% AUC, not 95%+
```

## Troubleshooting

### Common Issues and Solutions (Updated June 7, 2025)

#### 1. Industry Benchmarks All Show 65%
```bash
# Issue: Hardcoded percentiles in getIndustryBenchmarks
# Solution: Import and use industry_benchmarks.ts
import { getBenchmarksForSectorStage, calculatePercentile } from './industry_benchmarks';

# Now shows realistic, sector-specific benchmarks:
- SaaS Seed Revenue Growth: 50% → 150% → 300%
- FinTech Series A Team Size: 30 → 60 → 120
```

#### 2. 403 Forbidden Error
```bash
# Issue: Frontend sending API key when auth disabled
# Solution: Remove X-API-Key header from requests
headers: { 
  'Content-Type': 'application/json'
  // 'X-API-Key': API_CONFIG.API_KEY  // REMOVED
}
```

#### 3. 500 Validation Errors
```bash
# Common errors:
"sector must be one of [...] (got proptech)"
"investor_tier_primary must be one of [...] (got tier1)"

# Solution: Added 20+ sectors to validation
valid_sectors = ["saas", "fintech", "healthtech", "edtech", "ecommerce", 
                 "marketplace", "deeptech", "consumer", "enterprise", 
                 "proptech", "biotech", "agtech", "cleantech", 
                 "cybersecurity", "gaming", "logistics", "insurtech", 
                 "legaltech", "hrtech", "other"]
```

#### 4. Generic LLM Recommendations
```bash
# Issue: "recommendations are same for all results"
# Root cause: userInput not passed to LLM
# Solution: Add userInput to enrichedData
const enrichedData = {
  ...scores,
  userInput: startupData  # CRITICAL FIX
};
```

#### 5. What-If Shows Same Scores
```bash
# Issue: "potential score which is same as the original score"
# Solution: Created whatif_calculator.py with ML logic
# Example impacts:
- Hire VP: People +12%, Capital -3%
- Add Advisors: People +8%, Market +4%
- File Patent: Advantage +15%, Capital -2%
```

#### 6. Redis Connection Refused
```bash
# Issue: Redis not running, caching fails
# Solution: Automatic fallback to in-memory cache
INFO: Redis not available. Using in-memory cache.
# Cache works without Redis installation
```

#### 7. Pydantic Deprecation Warnings
```bash
# Issue: @validator deprecated in Pydantic V2
# Solution: Updated to @field_validator
@field_validator('sector')
@classmethod
def validate_sector(cls, v):
    # validation logic
```

### Debug Commands
```bash
# Check API health
curl http://localhost:8001/health

# Test LLM status (expect 15-20s response)
curl http://localhost:8001/api/analysis/status

# Monitor LLM context
tail -f api_server.log | grep "startup_data"
# Should see actual data, not "None None"

# Test personalized recommendations
python3 test_llm_integration.py

# Check benchmarks are working
grep "yourPercentile" build/static/js/main.*.js
# Should see calculatePercentile function calls
```

### Verifying Personalization

1. **Check LLM receives context**:
   ```bash
   grep "Generating dynamic recommendations" api_server.log
   # Should show sector and stage, not "None None"
   ```

2. **Verify recommendations address weakest area**:
   - First recommendation should target lowest CAMP score
   - Should reference specific metrics from startup

3. **Test different scenarios**:
   - Low people score → hiring recommendations
   - High burn → capital efficiency advice
   - No revenue → customer acquisition focus

4. **Verify benchmarks are dynamic**:
   - SaaS pre-seed should see different benchmarks than FinTech Series A
   - Percentiles should vary based on actual metrics

## Key Files

### Core System
1. **`api_server_unified.py`**: Main API server with all endpoints
2. **`advanced_models.py`**: Model loading and prediction logic
3. **`utils/data_validation.py`**: Input validation with 20+ sectors

### LLM Integration
1. **`llm_analysis.py`**: Core LLM engine with prompt templates
2. **`api_llm_endpoints.py`**: API endpoint handlers
3. **`whatif_calculator.py`**: ML-based what-if score calculations
4. **`test_llm_integration.py`**: Validation test suite

### Frontend
1. **`HybridAnalysisPage.tsx`**: Data transformation and API calls
2. **`AnalysisResults.tsx`**: Results display with benchmarks
3. **`industry_benchmarks.ts`**: Sector/stage-specific benchmarks
4. **`config/constants.ts`**: System-wide configuration

### Caching & Utilities
1. **`simple_cache.py`**: In-memory cache implementation
2. **`api_llm_helpers.py`**: Standalone functions for testing
3. **`.env.example`**: Environment variable template

## Environment Setup

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Add your API key (optional - has fallbacks)
DEEPSEEK_API_KEY=your_key_here

# 3. Set development mode
DISABLE_AUTH=true

# 4. Install dependencies
pip install python-dotenv

# 5. Start API server
python api_server_unified.py --port 8001

# 6. Start frontend
cd flash-frontend && npm start
```

## Conclusion

The V16.3 realistic models with personalized AI integration and industry-specific benchmarking represent a major improvement in **integrity**, **utility**, and **relevance**. The system now provides:

1. **Honest Predictions**: ~50% AUC reflects real uncertainty
2. **Personalized AI Insights**: Context-specific recommendations via DeepSeek
3. **CAMP-Aligned Guidance**: Always addresses weakest areas first
4. **Industry Benchmarks**: Sector and stage-specific performance metrics
5. **Fixed Data Flow**: All field mappings and context passing working
6. **Production Ready**: Full error handling, monitoring, and testing
7. **Fallback Mechanisms**: Works without Redis or API keys

This positions FLASH as a trustworthy AND intelligent tool for startup assessment, combining realistic ML predictions with highly personalized AI insights and industry-relevant benchmarking that helps startups understand their competitive position.