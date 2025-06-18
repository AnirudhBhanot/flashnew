/**
 * Configuration for the FLASH frontend
 */

export const API_CONFIG = {
  // API base URL - update this when deploying to production
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
  
  // API Key for authentication
  API_KEY: process.env.REACT_APP_API_KEY || 'test-api-key-123',
  
  // API endpoints
  ENDPOINTS: {
    PREDICT: '/predict',
    PREDICT_SIMPLE: '/predict_simple',
    PREDICT_ADVANCED: '/predict_advanced',
    PREDICT_ENHANCED: '/predict_enhanced',  // Pattern-enhanced prediction
    PATTERNS: '/patterns',
    PATTERN_DETAILS: '/patterns/{pattern_name}',
    ANALYZE_PATTERN: '/analyze_pattern',
    HEALTH: '/health',
    INVESTOR_PROFILES: '/investor_profiles'
  },
  
  // Default headers for all API requests
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.REACT_APP_API_KEY || 'test-api-key-123'
  }
};

// Helper function to build full API URLs
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.API_BASE_URL}${endpoint}`;
};