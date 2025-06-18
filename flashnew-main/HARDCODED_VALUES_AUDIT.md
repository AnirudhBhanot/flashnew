# Hardcoded Values Audit - FLASH Frontend

**Date**: June 7, 2025  
**Status**: Audit Complete

## Summary

Found multiple hardcoded values throughout the frontend that should be made configurable. While the industry benchmarks issue has been fixed, there are still many other hardcoded values that limit flexibility.

## Critical Hardcoded Values to Fix

### 1. Success Score Improvements (AnalysisResults.tsx)
```typescript
// Line 1201: Hardcoded 15% improvement cap
formatPercentage(Math.min(successProbability + 0.15, 0.85))

// Line 1205: Hardcoded text
"you could improve your success score by up to 15 percentage points"

// Line 1313: Hardcoded 2% per action
+{Math.floor(completedActions.size * 2)}%

// Line 1317: Hardcoded 3 actions milestone
{Math.max(0, 3 - completedActions.size)}
```
**Impact**: Users see fixed improvement potential regardless of their situation

### 2. Success Probability Thresholds (Multiple Files)
```typescript
// AnalysisResults.tsx Line 487:
successProbability >= 0.65 ? "strong fundamentals" : ...

// DynamicPredictionDisplay.tsx Lines 36-39:
if (probability >= 0.7) return '#00C851';
if (probability >= 0.5) return '#FF8800';
if (probability >= 0.3) return '#FF8800';

// HybridResults.tsx Line 382:
score >= 0.6 ? recommendations : null
```
**Impact**: Fixed thresholds don't adapt to different industries or stages

### 3. Default Fallback Values
```typescript
// HybridResults.tsx Line 116:
confidence={data.confidence_score || 0.85}

// Multiple files:
|| 0.5  // Default probability
|| 12   // Default runway months
|| 2    // Default burn multiple
|| 10   // Default team size
```
**Impact**: May show misleading defaults when data is missing

### 4. Business Metric Thresholds
```typescript
// AnalysisResults.tsx:
burn_multiple < 2 ? 'Efficient' : 'Watch burn'         // Line 713
competition_intensity > 3 ? 'High' : 'Moderate'        // Line 733
tam_size_usd > 50000000000 ? 'Large' : 'Niche'       // Line 737
team_size_full_time > 20 ? 'Good' : 'Needed'         // Line 757
years_experience_avg > 10 ? 'Experienced' : 'Growing' // Line 761
```
**Impact**: Same thresholds for all stages/sectors isn't realistic

### 5. Chart and Visual Constants
```typescript
// CAMPRadarChart.tsx:
const radius = 120;        // Line 33
const levels = 5;          // Line 34
r="6"                     // Line 189 (circle radius)
calculatePoint(1.25, i)   // Line 201 (label position)

// Score color offsets:
score >= threshold + 0.2  // Line 95
score >= threshold - 0.1  // Line 97
```
**Impact**: Fixed visualizations can't adapt to different screen sizes

### 6. Animation Timings
```typescript
// Throughout components:
transition: { duration: 0.6 }
transition: { delay: 0.2 }
transition: { type: "spring", stiffness: 100 }
setTimeout(() => {...}, 100)
```
**Impact**: Can't optimize for performance or accessibility needs

### 7. API Configuration
```typescript
// config.ts:
API_BASE_URL: 'http://localhost:8001'  // Line 7
REQUEST_TIMEOUT: 30000                  // Line 14 (30 seconds)
RETRY_ATTEMPTS: 3                       // Line 17
RETRY_DELAY: 1000                      // Line 18
```
**Impact**: Hardcoded timeouts may not suit all environments

## Recommendations

### 1. Create Configuration Service
```typescript
interface DynamicConfig {
  thresholds: {
    successProbability: {
      excellent: number;
      good: number;
      fair: number;
      poor: number;
    };
    improvements: {
      maxImprovement: number;
      perActionImprovement: number;
      milestoneActions: number;
    };
    metrics: {
      burnMultiple: { efficient: number; warning: number };
      teamSize: { [stage: string]: { good: number } };
      experience: { senior: number };
      tamSize: { large: number };
      competitionIntensity: { high: number };
    };
  };
  defaults: {
    confidence: number;
    probability: number;
    runwayMonths: number;
    burnMultiple: number;
    teamSize: number;
  };
  ui: {
    animation: {
      duration: number;
      delay: number;
      springStiffness: number;
    };
    chart: {
      radius: number;
      levels: number;
      pointRadius: number;
      labelOffset: number;
    };
  };
}
```

### 2. Environment-Based Configuration
```bash
# .env
REACT_APP_MAX_IMPROVEMENT=0.15
REACT_APP_PER_ACTION_IMPROVEMENT=0.02
REACT_APP_MILESTONE_ACTIONS=3
REACT_APP_DEFAULT_CONFIDENCE=0.85
```

### 3. Stage/Sector Aware Thresholds
Instead of:
```typescript
team_size_full_time > 20 ? 'Good' : 'Needed'
```

Use:
```typescript
team_size_full_time > getTeamSizeThreshold(stage, sector) ? 'Good' : 'Needed'
```

### 4. Dynamic Visual Scaling
```typescript
const chartConfig = useChartConfig(); // Hook that considers screen size
const radius = chartConfig.radius;
const levels = chartConfig.levels;
```

### 5. Accessibility Settings
```typescript
const animationSpeed = useAccessibilitySettings().reduceMotion ? 0 : 0.6;
```

## Priority Order

1. **High Priority**: Business logic thresholds (success probabilities, improvements)
2. **Medium Priority**: Default values and metric thresholds
3. **Low Priority**: Visual constants and animation timings

## Next Steps

1. Create a `ConfigProvider` component to wrap the app
2. Move all thresholds to a configuration file
3. Implement environment variable support for key values
4. Add admin UI to modify thresholds without deployment
5. Consider A/B testing framework for threshold experiments

## Files Most Affected

1. `AnalysisResults.tsx` - 20+ hardcoded values
2. `DynamicPredictionDisplay.tsx` - Color thresholds
3. `HybridResults.tsx` - Default values
4. `CAMPRadarChart.tsx` - Visual constants
5. `constants.ts` - Central configuration (partially done)

## Conclusion

While the constants.ts file provides some centralization, many components still have inline hardcoded values. Moving these to a proper configuration system would make the application more maintainable and flexible for different use cases.