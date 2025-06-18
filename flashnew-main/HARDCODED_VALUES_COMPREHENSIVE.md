# Comprehensive List of Hardcoded Values in FLASH Frontend Components

## Overview
This document lists all hardcoded values found in the flash-frontend v3 components that should be made dynamic or configurable.

---

## 1. AnalysisResults.tsx

### Hardcoded Percentages & Scores
- **Line 69-74**: Success probability thresholds
  ```typescript
  if (probability >= 0.75) return { text: 'STRONG INVESTMENT OPPORTUNITY', emoji: '🚀', class: 'strong-yes' };
  if (probability >= 0.65) return { text: 'PROMISING OPPORTUNITY', emoji: '✨', class: 'yes' };
  if (probability >= 0.55) return { text: 'PROCEED WITH CONDITIONS', emoji: '📊', class: 'conditional' };
  if (probability >= 0.45) return { text: 'NEEDS IMPROVEMENT', emoji: '🔧', class: 'needs-work' };
  ```

- **Line 77-81**: Color thresholds for success scores
  ```typescript
  if (probability >= 0.7) return '#00c851';
  if (probability >= 0.55) return '#33b5e5';
  if (probability >= 0.45) return '#ff8800';
  return '#ff4444';
  ```

- **Line 276**: Success factors count
  ```typescript
  <p className="subtitle">Comprehensive analysis based on 45 success factors</p>
  ```

- **Line 322**: Confidence level thresholds
  ```typescript
  <span className="value">{confidenceScore >= 0.8 ? 'High' : confidenceScore >= 0.6 ? 'Moderate' : 'Low'}</span>
  ```

- **Line 354-374**: Score range descriptions and percentages
  ```typescript
  <div className="range poor" data-range="0-45%">
  <div className="range fair" data-range="45-55%">
  <div className="range good" data-range="55-65%">
  <div className="range excellent" data-range="65-75%">
  <div className="range exceptional" data-range="75-100%">
  ```

### Hardcoded Model Weights
- **Line 432-451**: Model weight percentages
  ```typescript
  <span className="weight-value">35%</span> // Base Analysis
  <span className="weight-value">25%</span> // Pattern Detection
  <span className="weight-value">15%</span> // Stage Factors
  <span className="weight-value">15%</span> // Industry Specific
  <span className="weight-value">10%</span> // CAMP Framework
  ```

### Hardcoded Industry Benchmarks
- **Line 1518-1526**: Revenue growth benchmarks by stage
  ```typescript
  p25: data.funding_stage === 'Pre-seed' ? '0%' : data.funding_stage === 'Seed' ? '50%' : '100%',
  p50: data.funding_stage === 'Pre-seed' ? '0%' : data.funding_stage === 'Seed' ? '150%' : '200%',
  p75: data.funding_stage === 'Pre-seed' ? '100%' : data.funding_stage === 'Seed' ? '300%' : '400%',
  ```

- **Line 1532-1539**: Burn multiple benchmarks
  ```typescript
  p25: '3.0x',
  p50: '2.0x',
  p75: '1.2x',
  ```

### Hardcoded Thresholds
- **Line 1283**: Runway months threshold
  ```typescript
  value: `${data.runway_months || 12} months`,
  ```

- **Line 1404**: Revenue growth threshold
  ```typescript
  if (data.revenue_growth_rate_percent > 150) {
  ```

- **Line 1410**: Burn multiple threshold
  ```typescript
  if (data.burn_multiple < 1.5) {
  ```

---

## 2. HybridResults.tsx

### Model Analysis
- **Line 221**: Model count
  ```typescript
  <p className="section-description">
    Your startup was evaluated by 29 specialized models across 5 categories
  </p>
  ```

### Model Category Weights
- **Line 249-253**: Category percentages
  ```typescript
  <li><strong>Base Models (35%):</strong> Foundation models using contractual architecture</li>
  <li><strong>Pattern Models (25%):</strong> Specialized models for startup archetypes</li>
  <li><strong>Stage Models (15%):</strong> Funding stage-specific evaluation</li>
  <li><strong>Industry Models (15%):</strong> Vertical-specific insights</li>
  <li><strong>CAMP Models (10%):</strong> Framework refinement models</li>
  ```

### CAMP Score Thresholds
- **Line 365**: CAMP improvement threshold
  ```typescript
  if ((score as number) < 0.6) {
  ```

---

## 3. WorldClassResults.tsx

### Hardcoded Model Count & Features
- **Line 14**: Import specific model counts from constants but still references them

### Default Values
- **Line 145**: Default runway
  ```typescript
  data.runway_months || 12
  ```

### Industry/Company Examples
- Uses imported constants but could be more dynamic

---

## 4. AnalysisOrb.tsx

### Hardcoded Company Examples
- **Line 59**: Company references in DNA analysis
  ```typescript
  similar: ['Stripe at Series A', 'Airbnb at Series B'],
  ```

### Score Thresholds
- **Line 212-217**: Color thresholds
  ```typescript
  if (score >= 0.8) return '#00ff88';
  if (score >= 0.6) return '#ffbb00';
  if (score >= 0.4) return '#ff8800';
  return '#ff0055';
  ```

---

## 5. DataCollectionCAMP.tsx

### Field Configuration
- **Line 88-138**: All field configurations with hardcoded min/max values, placeholders, and defaults
  ```typescript
  revenue_growth_rate_percent: { label: 'Revenue Growth Rate (%)', type: 'number', placeholder: '100', min: -100, max: 1000 },
  gross_margin_percent: { label: 'Gross Margin (%)', type: 'number', placeholder: '70', min: -100, max: 100 },
  ltv_cac_ratio: { label: 'LTV/CAC Ratio', type: 'number', placeholder: '3', min: 0, max: 100, step: 0.1 },
  ```

### Default Values
- **Line 240-254**: Required defaults
  ```typescript
  revenue_growth_rate_percent: 0,
  ltv_cac_ratio: 0,
  customer_concentration_percent: 20,
  team_diversity_percent: 40,
  runway_months: 12,
  burn_multiple: 2
  ```

---

## 6. InvestmentMemo.tsx

### Valuation Multiples
- **Line 30-35**: Revenue multiples based on growth
  ```typescript
  let multiple = 5; // Base multiple
  if (growthRate > 200) multiple = 10;
  else if (growthRate > 150) multiple = 8;
  else if (growthRate > 100) multiple = 6;
  ```

### Company Comparables
- **Line 75-87**: Hardcoded company examples
  ```typescript
  'SaaS': {
    'Series A': ['Slack at Series A ($340M → $28B)', 'Zoom at Series A ($30M → $100B)'],
    'Series B': ['Datadog at Series B ($94M → $40B)', 'Monday.com at Series B ($84M → $7B)']
  },
  'AI/ML': {
    'Series A': ['Hugging Face at Series A ($40M → $2B)', 'Scale AI at Series A ($100M → $7B)'],
    'Series B': ['Anthropic at Series B ($124M → $5B)', 'Cohere at Series B ($125M → $2B)']
  }
  ```

### Benchmarks & Thresholds
- **Line 100-126**: Performance benchmarks
  ```typescript
  benchmark: data.revenue_growth_rate_percent > 150 ? 'Top 10%' : 'Top 25%',
  good: data.revenue_growth_rate_percent > 100
  ```

### Stage Weightings
- **Line 210-237**: Stage-specific weightings
  ```typescript
  'Pre-seed': [
    { label: 'People & Team', weight: 40 },
    { label: 'Market Opportunity', weight: 30 },
    { label: 'Product Vision', weight: 20 },
    { label: 'Capital Efficiency', weight: 10 }
  ],
  ```

---

## 7. ModelContributions.tsx

### Training Time
- **Line 190**: Hardcoded training time
  ```typescript
  <span>Optimized Training: 56 seconds</span>
  ```

### Model Dataset Size
- Relies on constants but displays as "100k Real Startups"

---

## 8. PatternAnalysis.tsx

### Pattern Success Rates
- Pattern descriptions and expected success rates should be dynamic

---

## 9. assessment/SuccessContext.tsx

### Success Comparisons
- **Line 57-92**: Hardcoded company comparisons and percentages
  ```typescript
  if (probability >= 0.80) {
    return {
      comparison: 'Top 5% of startups',
      similar: ['Stripe at Series A', 'Airbnb at Series B'],
      likelihood: 'Very likely to achieve 10x+ returns',
      timeframe: '3-5 years to major exit'
    };
  }
  ```

### Exit Timeframes
- **Line 61, 68, 75, 82**: Hardcoded exit timeframes
  ```typescript
  timeframe: '3-5 years to major exit'
  timeframe: '4-6 years to exit'
  timeframe: '5-7 years to exit'
  timeframe: '7+ years to potential exit'
  ```

---

## 10. assessment/BusinessInsights.tsx

### Business Language Translations
- Multiple hardcoded thresholds and descriptions throughout the translation logic

---

## 11. assessment/InvestmentReadiness.tsx

### Readiness Thresholds
- Various hardcoded thresholds for determining investment readiness

---

## 12. WeightageExplanation.tsx

### Stage Weights (if not using imported constants)
- May contain hardcoded stage weightings

---

## 13. Array Slicing & Display Limits

### AnalysisOrb.tsx
- **Line 305**: Key insights display limit
  ```typescript
  data.key_insights.slice(0, 3).map((insight: string, i: number) =>
  ```

### InvestmentMemo.tsx
- **Line 149, 171, 190**: Limits for strengths, risks, and steps
  ```typescript
  return strengths.slice(0, 3);
  return risks.slice(0, 3);
  return steps.slice(0, 3);
  ```

### WorldClassResults.tsx
- **Line 289**: Similar companies display limit
  ```typescript
  data.pattern_analysis.primary_pattern.similar_companies.slice(0, 3)
  ```
- **Line 299**: Recommendations display limit
  ```typescript
  data.pattern_analysis.primary_pattern.recommendations.slice(0, 2)
  ```

### BusinessInsights.tsx
- **Line 139**: Total insights limit
  ```typescript
  ].slice(0, 6); // Top 6 insights
  ```

---

## 14. Hardcoded Timeframes

### AdvancedAnalysisModal.tsx
- **Line 97, 104**: Prediction timeframes
  ```typescript
  <h4>Short Term (0-6 months)</h4>
  <h4>Medium Term (6-18 months)</h4>
  ```

### AnalysisOrb.tsx
- **Line 261, 267, 273**: Temporal prediction periods
  ```typescript
  <span className="temporal-label">6 months:</span>
  <span className="temporal-label">12 months:</span>
  <span className="temporal-label">18+ months:</span>
  ```

### AnalysisResults.tsx
- **Line 1224**: Profitability timeframe
  ```typescript
  'Clear path to profitability within 24-36 months'
  ```
- **Line 1636, 1652, 1674, 1696**: Action plan timelines
  ```typescript
  timeline: '90 days',
  timeline: '30 days',
  timeline: '60 days',
  ```

### DataCollectionCAMP.tsx
- **Line 110-111**: Retention period definitions
  ```typescript
  product_retention_30d: { label: '30-Day Retention (%)', ...
  product_retention_90d: { label: '90-Day Retention (%)', ...
  ```

### InvestmentMemo.tsx
- **Line 178, 184**: Improvement timeframes
  ```typescript
  steps.push('Optimize burn rate to reach <1.5x within 6 months');
  steps.push('Extend runway to 18-24 months');
  ```

### FullAnalysisView.tsx
- **Line 258, 282**: Milestone timelines
  ```typescript
  <span className="timeline">0-3 months</span>
  <span className="timeline">3-6 months</span>
  ```

---

## 15. Field Counts & Validation

### DataCollectionCAMP.tsx
- **Line 204, 207**: Field completion tracking
  ```typescript
  console.log(`Fields filled: ${filledFields.length}/${allFields.length}`);
  alert(`Please complete all fields. Currently ${filledFields.length}/${allFields.length} fields are filled.`);
  ```

---

## 16. Hardcoded Industries & Sectors

### AnalysisResults.tsx
- **Line 659**: Default industry
  ```typescript
  <h2>Industry Benchmarks: {data.industry || 'SaaS'}</h2>
  ```

### DataCollectionCAMP.tsx
- **Line 114**: Industry placeholder
  ```typescript
  sector: { label: 'Industry Sector', type: 'text', placeholder: 'SaaS, Fintech, etc.', helper: 'Primary industry vertical' },
  ```

### InvestmentMemo.tsx
- **Line 72**: Default sector
  ```typescript
  const sector = data.sector || 'SaaS';
  ```
- **Line 76-86**: Hardcoded company comparables by sector
  ```typescript
  'SaaS': {
    'Series A': ['Slack at Series A ($340M → $28B)', 'Zoom at Series A ($30M → $100B)'],
    'Series B': ['Datadog at Series B ($94M → $40B)', 'Monday.com at Series B ($84M → $7B)']
  },
  'AI/ML': {
    'Series A': ['Hugging Face at Series A ($40M → $2B)', 'Scale AI at Series A ($100M → $7B)'],
    'Series B': ['Anthropic at Series B ($124M → $5B)', 'Cohere at Series B ($125M → $2B)']
  }
  ```

---

## 17. Investor Tiers

### DataCollectionCAMP.tsx
- **Line 97**: Investor tier options
  ```typescript
  investor_tier_primary: { label: 'Primary Investor Tier', type: 'select', options: ['Tier 1', 'Tier 2', 'Tier 3', 'Angel'], helper: 'Lead investor quality ranking' },
  ```

### AnalysisPage.tsx & HybridAnalysisPage.tsx
- Investor tier mapping logic with hardcoded tiers

---

## Summary of Key Hardcoded Categories

### 1. **Numeric Thresholds**
   - Success probability ranges (0.45, 0.55, 0.65, 0.75)
   - Confidence scores (0.6, 0.8)
   - Burn multiples (1.5, 2.0, 2.5, 3.0)
   - Growth rates (50%, 100%, 150%, 200%)
   - Retention rates (30d, 90d)
   - LTV/CAC ratios (3:1)

### 2. **Timeframes**
   - Exit timelines (3-5, 4-6, 5-7, 7+ years)
   - Runway periods (12, 18, 24 months)
   - Action plan durations (30, 60, 90 days)
   - Prediction horizons (6, 12, 18 months)

### 3. **Company References**
   - Specific company examples (Stripe, Airbnb, Slack, etc.)
   - Historical valuations and exits
   - Success story comparisons

### 4. **Model & Analysis**
   - Model counts (29 specialized models)
   - Success factors (45 factors)
   - Model weights (10%, 15%, 25%, 35%)
   - Training metrics (56 seconds, 100k dataset)

### 5. **Display Limits**
   - Insights shown (3, 6 items)
   - Recommendations (2-3 items)
   - Company examples (3 items)

### 6. **Business Rules**
   - Valuation multiples (5x-10x based on growth)
   - Stage-specific weightings
   - Industry categories
   - Investor tier classifications

---

## Recommendations

1. **Create a centralized configuration service** that fetches these values from the backend
2. **Use environment variables** for values that change between deployments
3. **Implement a feature flag system** for A/B testing different thresholds
4. **Create admin interfaces** to update benchmarks and thresholds without code changes
5. **Version the configuration** to track changes over time
6. **Cache configuration** with appropriate TTL to reduce API calls
7. **Provide fallback values** when API is unavailable
8. **Document all configurable values** and their business impact

## Priority Items to Fix

### High Priority (Business Impact)
1. Success probability thresholds and verdict mappings
2. Model weights and category percentages  
3. Revenue multiples and valuation logic
4. Company comparables and examples
5. Benchmark values (burn multiple, growth rates, etc.)

### Medium Priority (User Experience)
1. Color schemes and visual thresholds
2. Progress indicators and timeframes
3. Default field values in forms
4. Score range descriptions

### Low Priority (Cosmetic)
1. Icon mappings
2. Text descriptions
3. UI animation timings
4. Helper text