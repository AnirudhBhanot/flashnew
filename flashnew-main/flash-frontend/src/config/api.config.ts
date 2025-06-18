/**
 * API Configuration
 * Centralized configuration for all API-related settings
 */

export const API_CONFIG = {
  // Base URL for the API
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
  
  // API Key for authentication
  API_KEY: process.env.REACT_APP_API_KEY || 'test-api-key-123',
  
  // Request timeout in milliseconds
  REQUEST_TIMEOUT: 30000,
  
  // Retry configuration
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
  
  // Default headers for all requests
  DEFAULT_HEADERS: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.REACT_APP_API_KEY || 'test-api-key-123'
  }
};

// Endpoint paths
export const API_ENDPOINTS = {
  // Main endpoints
  PREDICT: '/predict',
  HEALTH: '/health',
  FEATURES: '/features',
  
  // Config endpoints
  CONFIG: {
    STAGE_WEIGHTS: '/config/stage-weights',
    MODEL_PERFORMANCE: '/config/model-performance',
    COMPANY_EXAMPLES: '/config/company-examples',
    SUCCESS_THRESHOLDS: '/config/success-thresholds',
    MODEL_WEIGHTS: '/config/model-weights',
    REVENUE_BENCHMARKS: '/config/revenue-benchmarks',
    COMPANY_COMPARABLES: '/config/company-comparables',
    DISPLAY_LIMITS: '/config/display-limits',
    ALL: '/config/all'
  }
};