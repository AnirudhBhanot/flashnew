import { apiRequest, predictAPI, getConfig } from '../apiClient';
import { API_CONFIG } from '../../config';

// Mock fetch
global.fetch = jest.fn();

describe('apiClient', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockClear();
  });

  describe('apiRequest', () => {
    it('should make a request with default headers', async () => {
      const mockResponse = new Response(JSON.stringify({ data: 'test' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
      (global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse);

      await apiRequest('/test');

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_CONFIG.API_BASE_URL}/test`,
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            'X-API-Key': expect.any(String)
          })
        })
      );
    });

    it('should handle absolute URLs', async () => {
      const mockResponse = new Response('{}', { status: 200 });
      (global.fetch as jest.Mock).mockResolvedValueOnce(mockResponse);

      await apiRequest('https://example.com/api');

      expect(global.fetch).toHaveBeenCalledWith(
        'https://example.com/api',
        expect.any(Object)
      );
    });
  });

  describe('predictAPI', () => {
    const mockStartupData = {
      funding_stage: 'seed',
      total_capital_raised_usd: 1000000,
      cash_on_hand_usd: 800000,
      monthly_burn_usd: 50000,
      annual_revenue_run_rate: 500000,
      revenue_growth_rate_percent: 20,
      gross_margin_percent: 70,
      ltv_cac_ratio: 3,
      investor_tier_primary: 'tier_1',
      has_debt: false,
      patent_count: 2,
      network_effects_present: true,
      has_data_moat: false,
      regulatory_advantage_present: false,
      tech_differentiation_score: 8,
      switching_cost_score: 7,
      brand_strength_score: 6,
      scalability_score: 9,
      product_stage: 'growth',
      product_retention_30d: 0.85,
      product_retention_90d: 0.75,
      sector: 'SaaS',
      tam_size_usd: 10000000000,
      sam_size_usd: 1000000000,
      som_size_usd: 100000000,
      market_growth_rate_percent: 15,
      customer_count: 100,
      customer_concentration_percent: 20,
      user_growth_rate_percent: 25,
      net_dollar_retention_percent: 110,
      competition_intensity: 7,
      competitors_named_count: 5,
      dau_mau_ratio: 0.6,
      founders_count: 2,
      team_size_full_time: 15,
      years_experience_avg: 10,
      domain_expertise_years_avg: 7,
      prior_startup_experience_count: 2,
      prior_successful_exits_count: 1,
      board_advisor_experience_score: 8,
      advisors_count: 4,
      team_diversity_percent: 40,
      key_person_dependency: false
    };

    it('should make a POST request to /predict endpoint', async () => {
      const mockResponse = {
        success_probability: 0.75,
        confidence_score: 0.85,
        verdict: 'PASS',
        risk_level: 'MEDIUM'
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce(
        new Response(JSON.stringify(mockResponse), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        })
      );

      const result = await predictAPI(mockStartupData);

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_CONFIG.API_BASE_URL}/predict`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(mockStartupData),
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          })
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('should throw an error for non-ok responses', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce(
        new Response(JSON.stringify({ detail: 'Invalid data' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        })
      );

      await expect(predictAPI(mockStartupData)).rejects.toThrow('Invalid data');
    });

    it('should throw generic error if no detail in error response', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce(
        new Response('{}', {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        })
      );

      await expect(predictAPI(mockStartupData)).rejects.toThrow('API Error: 500');
    });
  });

  describe('getConfig', () => {
    it('should fetch configuration for given type', async () => {
      const mockConfig = {
        fields: [
          { key: 'threshold', value: 0.5, type: 'number' }
        ],
        categories: ['general'],
        lastUpdated: '2024-01-01'
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce(
        new Response(JSON.stringify(mockConfig), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        })
      );

      const result = await getConfig('general');

      expect(global.fetch).toHaveBeenCalledWith(
        `${API_CONFIG.API_BASE_URL}/config/general`,
        expect.any(Object)
      );
      expect(result).toEqual(mockConfig);
    });

    it('should throw an error for failed config fetch', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce(
        new Response('Not found', { status: 404 })
      );

      await expect(getConfig('invalid')).rejects.toThrow('Failed to fetch invalid config');
    });
  });
});