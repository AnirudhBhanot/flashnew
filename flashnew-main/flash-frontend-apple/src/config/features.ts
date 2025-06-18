/**
 * Feature flags for the FLASH platform
 * These can be toggled to enable/disable features or switch between implementations
 */

export const featureFlags = {
  // Michelin Analysis approach
  // Set to 'enhanced' to use the McKinsey-grade analysis with context engine (NEW - BEST)
  // Set to 'decomposed' to use the reliable approach (stable)
  // Set to 'original' to use the JSON-based approach (prone to parsing errors)
  // Set to 'strategic' to use the redesigned approach with phase interconnection
  michelinAnalysisApproach: 'enhanced' as 'enhanced' | 'decomposed' | 'original' | 'strategic',
  
  // Enable detailed logging for Michelin analysis
  michelinAnalysisDebugMode: false,
  
  // Show comparison mode (allows switching between approaches in UI)
  michelinAnalysisComparisonMode: false,
};

// Helper function to get the Michelin API endpoint based on feature flag
export const getMichelinEndpoint = (phase: 1 | 2 | 3): string => {
  const baseUrl = 'http://localhost:8001/api/michelin';
  const approach = featureFlags.michelinAnalysisApproach;
  
  if (approach === 'enhanced') {
    return `${baseUrl}/enhanced/analyze/phase${phase}`;
  } else if (approach === 'decomposed') {
    return `${baseUrl}/decomposed/analyze/phase${phase}`;
  } else if (approach === 'strategic') {
    return `${baseUrl}/strategic/analyze/phase${phase}`;
  } else {
    return `${baseUrl}/analyze/phase${phase}`;
  }
};

// Helper to check if we're using the decomposed approach
export const isUsingDecomposedMichelin = (): boolean => {
  return featureFlags.michelinAnalysisApproach === 'decomposed';
};