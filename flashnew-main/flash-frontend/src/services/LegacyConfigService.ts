/**
 * Service to fetch dynamic configuration from the API
 * Falls back to local constants if API is unavailable
 */

import { API_CONFIG } from '../config';
import * as constants from '../config/constants';

// Configuration API base URL - using the same port as main API
const CONFIG_API_URL = process.env.REACT_APP_CONFIG_API_URL || 'http://localhost:8001';

// Default headers including authentication
const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'X-API-Key': process.env.REACT_APP_API_KEY || 'test-api-key-123'
};

class ConfigService {
  private cache: Map<string, any> = new Map();
  private cacheExpiry: Map<string, number> = new Map();
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  /**
   * Make authenticated fetch request
   */
  private async fetchWithAuth(url: string): Promise<Response> {
    return fetch(url, {
      method: 'GET',
      headers: DEFAULT_HEADERS
    });
  }

  /**
   * Get stage weights from API or fallback to constants
   */
  async getStageWeights(): Promise<typeof constants.STAGE_WEIGHTS> {
    return this.getCachedOrFetch('stage_weights', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/stage-weights`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.STAGE_WEIGHTS;
    });
  }

  /**
   * Get model performance metrics from API or fallback to constants
   */
  async getModelPerformance(): Promise<typeof constants.MODEL_PERFORMANCE> {
    return this.getCachedOrFetch('model_performance', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/model-performance`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.MODEL_PERFORMANCE;
    });
  }

  /**
   * Get company examples from API or fallback to constants
   */
  async getCompanyExamples(): Promise<typeof constants.COMPANY_EXAMPLES> {
    return this.getCachedOrFetch('company_examples', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/company-examples`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.COMPANY_EXAMPLES;
    });
  }

  /**
   * Get success thresholds from API or fallback to constants
   */
  async getSuccessThresholds(): Promise<typeof constants.SUCCESS_THRESHOLDS> {
    return this.getCachedOrFetch('success_thresholds', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/success-thresholds`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.SUCCESS_THRESHOLDS;
    });
  }

  /**
   * Get model weights from API or fallback to constants
   */
  async getModelWeights(): Promise<typeof constants.MODEL_WEIGHTS> {
    return this.getCachedOrFetch('model_weights', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/model-weights`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.MODEL_WEIGHTS;
    });
  }

  /**
   * Get revenue benchmarks from API or fallback to constants
   */
  async getRevenueBenchmarks(): Promise<typeof constants.REVENUE_BENCHMARKS> {
    return this.getCachedOrFetch('revenue_benchmarks', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/revenue-benchmarks`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.REVENUE_BENCHMARKS;
    });
  }

  /**
   * Get company comparables from API or fallback to constants
   */
  async getCompanyComparables(): Promise<typeof constants.COMPANY_COMPARABLES> {
    return this.getCachedOrFetch('company_comparables', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/company-comparables`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.COMPANY_COMPARABLES;
    });
  }

  /**
   * Get display limits from API or fallback to constants
   */
  async getDisplayLimits(): Promise<typeof constants.DISPLAY_LIMITS> {
    return this.getCachedOrFetch('display_limits', async () => {
      try {
        const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/display-limits`);
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
      }
      return constants.DISPLAY_LIMITS;
    });
  }

  /**
   * Get all configuration in one call
   */
  async getAllConfig() {
    try {
      const response = await this.fetchWithAuth(`${CONFIG_API_URL}/config/all`);
      if (response.ok) {
        const data = await response.json();
        // Cache individual configs
        Object.entries(data).forEach(([key, value]) => {
          this.cache.set(key, value);
          this.cacheExpiry.set(key, Date.now() + this.CACHE_DURATION);
        });
        return data;
      }
    } catch (error) {
    }

    // Return all defaults
    return {
      stage_weights: constants.STAGE_WEIGHTS,
      model_performance: constants.MODEL_PERFORMANCE,
      company_examples: constants.COMPANY_EXAMPLES,
      success_thresholds: constants.SUCCESS_THRESHOLDS,
      model_weights: constants.MODEL_WEIGHTS,
      revenue_benchmarks: constants.REVENUE_BENCHMARKS,
      company_comparables: constants.COMPANY_COMPARABLES,
      display_limits: constants.DISPLAY_LIMITS
    };
  }

  /**
   * Clear the cache
   */
  clearCache() {
    this.cache.clear();
    this.cacheExpiry.clear();
  }

  /**
   * Get cached value or fetch from source
   */
  private async getCachedOrFetch<T>(
    key: string,
    fetcher: () => Promise<T>
  ): Promise<T> {
    // Check cache
    if (this.cache.has(key)) {
      const expiry = this.cacheExpiry.get(key) || 0;
      if (Date.now() < expiry) {
        return this.cache.get(key) as T;
      }
    }

    // Fetch fresh data
    const data = await fetcher();
    
    // Cache it
    this.cache.set(key, data);
    this.cacheExpiry.set(key, Date.now() + this.CACHE_DURATION);
    
    return data;
  }
}

// Export singleton instance
export const configService = new ConfigService();