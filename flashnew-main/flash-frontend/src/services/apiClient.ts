/**
 * Centralized API client with authentication
 */

import { API_CONFIG } from '../config';
import { StartupData } from '../types';
import { ApiPredictionResult, ConfigResponse } from '../types/api.types';

// Default headers including authentication
const defaultHeaders = {
  'Content-Type': 'application/json',
  'X-API-Key': process.env.REACT_APP_API_KEY || 'test-api-key-123'
};

/**
 * Make an authenticated API request
 */
export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const url = endpoint.startsWith('http') 
    ? endpoint 
    : `${API_CONFIG.API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  });

  return response;
}

/**
 * Make a prediction request
 */
export async function predictAPI(data: StartupData): Promise<ApiPredictionResult> {
  const response = await apiRequest('/predict', {
    method: 'POST',
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

/**
 * Get configuration data
 */
export async function getConfig(configType: string): Promise<ConfigResponse> {
  const response = await apiRequest(`/config/${configType}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch ${configType} config`);
  }

  return response.json();
}