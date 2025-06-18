# Configuration System Implementation Guide

**Version**: 1.0  
**Date**: June 7, 2025  
**Status**: Ready for Implementation

## Overview

This guide provides step-by-step instructions for implementing the enterprise-grade configuration system in the FLASH frontend. The system eliminates hardcoded values and provides dynamic, context-aware configuration management.

## Implementation Steps

### Step 1: Install Dependencies

```bash
cd flash-frontend
npm install lodash @types/lodash
```

### Step 2: Add Configuration Files

The following files have been created and are ready to use:

1. **Type Definitions** (`src/config/types.ts`)
   - Comprehensive TypeScript interfaces for all configuration
   - Type guards and utility types
   - Context interfaces for stage/sector overrides

2. **Default Configuration** (`src/config/defaults.ts`)
   - Complete default values for all configuration
   - Stage and sector-specific overrides
   - Custom calculation functions

3. **Configuration Context** (`src/providers/ConfigContext.ts`)
   - React context interface
   - Methods for getting/setting configuration

4. **Configuration Provider** (`src/providers/ConfigProvider.tsx`)
   - Main provider component
   - Configuration loading and caching
   - Environment variable merging

5. **Configuration Hooks** (`src/hooks/useConfiguration.ts`)
   - `useConfiguration` - Main configuration access
   - `useSuccessThresholds` - Success probability thresholds
   - `useImprovementCalculator` - Dynamic improvement calculations
   - `useAnimationConfig` - Animation settings
   - `useNumberFormatter` - Number formatting
   - `useMetricThreshold` - Business metric thresholds

6. **Environment Template** (`.env.example`)
   - Template for environment variables
   - All configurable values documented

### Step 3: Update App Entry Point

Update `src/AppV3.tsx`:

```typescript
import React from 'react';
import { ConfigProvider } from './providers/ConfigProvider';
import { BrowserRouter as Router } from 'react-router-dom';
// ... other imports

function AppV3() {
  return (
    <ConfigProvider>
      <Router>
        {/* Your existing app content */}
      </Router>
    </ConfigProvider>
  );
}

export default AppV3;
```

### Step 4: Migrate Components

Follow the example in `MIGRATION_EXAMPLE_ANALYSISRESULTS.tsx` to migrate components:

#### Before:
```typescript
// Hardcoded values
successProbability >= 0.65 ? "strong" : "weak"
formatPercentage = (value) => `${(value * 100).toFixed(0)}%`
burn_multiple < 2 ? 'Efficient' : 'High'
improvement = actions * 0.02 // Fixed calculation
```

#### After:
```typescript
// Configuration-based
const successThresholds = useSuccessThresholds(stage, sector);
const { formatPercentage } = useNumberFormatter();
const burnThresholds = useMetricThreshold('burn', stage, sector);
const improvement = improvementCalculator(actions);

// Usage
successThresholds.getLevel(probability) // Returns 'excellent', 'good', etc.
formatPercentage(value) // Uses configured decimal places
data.burn_multiple < burnThresholds.good ? 'Efficient' : 'High'
```

### Step 5: Key Migration Patterns

#### 1. Success Probability Thresholds
```typescript
// Old
if (probability >= 0.7) return 'excellent';
if (probability >= 0.5) return 'good';

// New
const thresholds = useSuccessThresholds(stage, sector);
const level = thresholds.getLevel(probability);
const color = thresholds.getColor(probability);
const message = thresholds.getMessage(probability);
```

#### 2. Default Values
```typescript
// Old
const confidence = data.confidence_score || 0.85;

// New
const defaults = useDefaults();
const confidence = data.confidence_score || defaults.confidence;
```

#### 3. Animation Durations
```typescript
// Old
transition: { duration: 0.6 }

// New
const animation = useAnimationConfig();
transition: { duration: animation.getDuration() / 1000 }
```

#### 4. Business Metrics
```typescript
// Old
team_size > 20 ? 'Good' : 'Needed'

// New
const teamThresholds = useMetricThreshold('team.size', stage, sector);
team_size > teamThresholds.optimal ? 'Good' : 'Needed'
```

#### 5. Feature Flags
```typescript
// Old
<button onClick={exportPDF}>Export</button>

// New
const { isFeatureEnabled } = useConfiguration();
{isFeatureEnabled('exportPDF') && (
  <button onClick={exportPDF}>Export</button>
)}
```

### Step 6: Environment Variables

1. Copy `.env.example` to `.env`
2. Update values as needed
3. Restart development server

Example:
```bash
cp .env.example .env
# Edit .env with your values
npm start
```

### Step 7: Testing Configuration Changes

1. **Runtime Updates**: Configuration can be updated without restarting:
```typescript
const { update } = useConfiguration();
await update('thresholds.success.probability.good', 0.70);
```

2. **Bulk Updates**:
```typescript
const { bulkUpdate } = useConfiguration();
await bulkUpdate({
  'thresholds.success.probability.good': 0.70,
  'thresholds.success.probability.excellent': 0.80
});
```

3. **Reset to Defaults**:
```typescript
const { reset } = useConfiguration();
await reset(); // Reset all
await reset('thresholds.success'); // Reset specific path
```

## Components to Migrate

Priority order for migration:

### High Priority (Business Logic)
1. `AnalysisResults.tsx` - Success thresholds, improvements
2. `DynamicPredictionDisplay.tsx` - Color thresholds
3. `HybridResults.tsx` - Default values
4. `CAMPRadarChart.tsx` - Visual constants
5. `DataCollectionCAMP.tsx` - Validation thresholds

### Medium Priority (UI/UX)
1. `AnalysisOrb.tsx` - Animation settings
2. `ConfidenceVisualization.tsx` - Chart settings
3. `InvestmentMemo.tsx` - Export settings
4. `WeightageExplanation.tsx` - Display settings

### Low Priority (Styling)
1. CSS files - Convert pixel values to configuration
2. Animation timings - Use animation config
3. Color values - Use color configuration

## Advanced Features

### 1. A/B Testing

```typescript
// In configuration
experiments: {
  'new-thresholds': {
    enabled: true,
    rolloutPercentage: 50,
    variants: [
      { id: 'control', weight: 0.5, config: { /* current */ } },
      { id: 'treatment', weight: 0.5, config: { /* new thresholds */ } }
    ]
  }
}
```

### 2. Stage-Specific Overrides

```typescript
// Configuration automatically handles stage overrides
const threshold = useMetricThreshold('burn', 'pre_seed');
// Returns pre-seed specific burn thresholds
```

### 3. Sector-Specific Overrides

```typescript
// Sector overrides take precedence
const threshold = useMetricThreshold('ltv_cac', 'series_a', 'saas');
// Returns SaaS-specific LTV/CAC thresholds for Series A
```

### 4. Performance Monitoring

```typescript
// Subscribe to configuration changes
useConfigSubscription((config, changes) => {
  console.log('Configuration updated:', changes);
  // Track which thresholds are used most
});
```

## Benefits Achieved

1. **No More Hardcoded Values**
   - All business logic configurable
   - Easy updates without deployment

2. **Context-Aware Configuration**
   - Stage-specific thresholds
   - Sector-specific thresholds
   - User preference support

3. **Type Safety**
   - Full TypeScript support
   - Compile-time checking
   - IntelliSense for all config

4. **Performance Optimized**
   - Memoized calculations
   - Cached values
   - Minimal re-renders

5. **Developer Experience**
   - Simple hook-based API
   - Clear migration path
   - Comprehensive documentation

## Troubleshooting

### Configuration Not Loading
```typescript
// Check console for errors
// Verify ConfigProvider wraps your app
// Check localStorage for cached config
localStorage.getItem('flash_config_cache')
```

### Environment Variables Not Working
```bash
# Ensure variables start with REACT_APP_
# Restart dev server after changes
# Check process.env in browser console
console.log(process.env.REACT_APP_SUCCESS_GOOD)
```

### Type Errors
```typescript
// Import types from config/types
import { IConfiguration } from '../config/types';

// Use type guards
if (isConfiguration(obj)) {
  // obj is IConfiguration
}
```

## Next Steps

1. Start with high-priority components
2. Test each migration thoroughly
3. Monitor for performance impacts
4. Gather team feedback
5. Plan production rollout

## Support

For questions or issues:
1. Check the `CONFIGURATION_SYSTEM_PLAN.md` for architecture details
2. Review type definitions in `src/config/types.ts`
3. Look at migration example in `MIGRATION_EXAMPLE_ANALYSISRESULTS.tsx`

The configuration system is now ready for implementation. Start with one component, test thoroughly, then proceed with the full migration.