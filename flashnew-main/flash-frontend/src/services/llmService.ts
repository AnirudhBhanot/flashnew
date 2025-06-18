/**
 * LLM Analysis Service
 * Handles all AI-powered dynamic analysis features
 */

import { apiRequest } from './apiClient';

export interface LLMRecommendation {
  title: string;
  why: string;
  how: string[];
  timeline: string;
  impact: string;
  camp_area: 'capital' | 'advantage' | 'market' | 'people';
}

export interface LLMRecommendationsResponse {
  recommendations: LLMRecommendation[];
  generated_at: string;
  model: string;
  type: 'ai_generated' | 'fallback';
  error?: string;
}

export interface WhatIfImprovement {
  id: string;
  description: string;
  camp_area?: string;
}

export interface WhatIfResult {
  new_probability: {
    value: number;
    lower: number;
    upper: number;
  };
  new_scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  score_changes: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  timeline: string;
  risks: string[];
  priority: string;
  reasoning: string;
  generated_at: string;
  type: string;
}

export interface MarketInsights {
  market_trends: string[];
  funding_climate: string;
  recent_exits: string[];
  opportunities: string[];
  competitors: string[];
  investment_thesis: string;
  generated_at: string;
  type: string;
}

export interface LLMServiceStatus {
  status: 'operational' | 'degraded' | 'offline';
  model?: string;
  cache_enabled?: boolean;
  error?: string;
  timestamp: string;
}

class LLMService {
  private baseURL = '/api/analysis';
  private statusCache: { status: LLMServiceStatus | null; timestamp: number } = {
    status: null,
    timestamp: 0
  };
  private STATUS_CACHE_TTL = 300000; // 5 minutes

  /**
   * Get dynamic AI-powered recommendations
   */
  async getRecommendations(
    startupData: any,
    scores: any,
    verdict?: string
  ): Promise<LLMRecommendationsResponse> {
    try {
      const response = await apiRequest(`${this.baseURL}/recommendations/dynamic`, {
        method: 'POST',
        body: JSON.stringify({
          startup_data: startupData,
          scores: scores,
          verdict: verdict
        })
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Failed to get LLM recommendations:', error);
      throw error;
    }
  }

  /**
   * Analyze what-if scenarios with AI
   */
  async analyzeWhatIf(
    startupData: any,
    currentScores: any,
    improvements: WhatIfImprovement[]
  ): Promise<WhatIfResult> {
    try {
      const response = await apiRequest(`${this.baseURL}/whatif/dynamic`, {
        method: 'POST',
        body: JSON.stringify({
          startup_data: startupData,
          current_scores: currentScores,
          improvements: improvements
        })
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Failed to analyze what-if scenario:', error);
      throw error;
    }
  }

  /**
   * Get market insights for the startup's industry
   */
  async getMarketInsights(startupData: any): Promise<MarketInsights> {
    try {
      const response = await apiRequest(`${this.baseURL}/insights/market`, {
        method: 'POST',
        body: JSON.stringify({
          startup_data: startupData
        })
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Failed to get market insights:', error);
      throw error;
    }
  }

  /**
   * Check if LLM service is available
   */
  async checkStatus(): Promise<LLMServiceStatus> {
    // Return cached status if still valid
    const now = Date.now();
    if (this.statusCache.status && now - this.statusCache.timestamp < this.STATUS_CACHE_TTL) {
      return this.statusCache.status;
    }

    try {
      const response = await apiRequest(`${this.baseURL}/status`, {
        method: 'GET'
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      this.statusCache = {
        status: data,
        timestamp: now
      };
      return data;
    } catch (error) {
      const offlineStatus: LLMServiceStatus = {
        status: 'offline',
        error: 'Service unavailable',
        timestamp: new Date().toISOString()
      };
      this.statusCache = {
        status: offlineStatus,
        timestamp: now
      };
      return offlineStatus;
    }
  }

  /**
   * Check if LLM features should be shown
   */
  async isAvailable(): Promise<boolean> {
    const status = await this.checkStatus();
    return status.status === 'operational';
  }

  /**
   * Helper to determine if we should use LLM or fallback
   */
  async shouldUseLLM(): Promise<boolean> {
    // Check feature flag from environment
    if (process.env.REACT_APP_DISABLE_LLM === 'true') {
      return false;
    }

    // Check service status
    return await this.isAvailable();
  }

  /**
   * Format recommendations for display
   */
  formatRecommendations(recommendations: LLMRecommendation[]): any[] {
    return recommendations.map((rec, index) => ({
      priority: this.getPriorityFromIndex(index),
      title: rec.title,
      description: rec.why,
      impact: this.parseImpact(rec.impact),
      timeline: rec.timeline,
      actions: rec.how,
      metrics: this.generateMetrics(rec),
      affects: [rec.camp_area],
      ai_generated: true
    }));
  }

  private getPriorityFromIndex(index: number): string {
    if (index === 0) return 'CRITICAL';
    if (index === 1) return 'HIGH';
    if (index === 2) return 'MEDIUM';
    return 'LOW';
  }

  private parseImpact(impact: string): number {
    // Extract number from impact string like "Increase Capital score by 10-15 points"
    const match = impact.match(/(\d+)/);
    return match ? parseInt(match[1]) : 5;
  }

  private generateMetrics(rec: LLMRecommendation): string[] {
    // Generate success metrics from recommendation
    return [
      `${rec.camp_area} score improvement`,
      'Implementation completion',
      'Timeline adherence'
    ];
  }
}

// Export singleton instance
export const llmService = new LLMService();