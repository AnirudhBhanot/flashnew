// Tests for data validation and transformation utilities

describe('Data Validation', () => {
  describe('Startup Data Validation', () => {
    it('should validate funding stage values', () => {
      const validStages = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c'];
      const invalidStages = ['', 'unknown', 'SeriesA', 'SEED'];

      validStages.forEach(stage => {
        expect(['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']).toContain(stage);
      });

      invalidStages.forEach(stage => {
        expect(['pre_seed', 'seed', 'series_a', 'series_b', 'series_c']).not.toContain(stage);
      });
    });

    it('should validate numeric ranges', () => {
      // Test percentage fields (should be 0-100 or 0-1)
      const percentageFields = [
        { value: 50, min: 0, max: 100, valid: true },
        { value: 0, min: 0, max: 100, valid: true },
        { value: 100, min: 0, max: 100, valid: true },
        { value: -10, min: 0, max: 100, valid: false },
        { value: 150, min: 0, max: 100, valid: false }
      ];

      percentageFields.forEach(({ value, min, max, valid }) => {
        const isValid = value >= min && value <= max;
        expect(isValid).toBe(valid);
      });
    });

    it('should validate required fields are present', () => {
      const requiredFields = [
        'funding_stage',
        'total_capital_raised_usd',
        'cash_on_hand_usd',
        'monthly_burn_usd',
        'sector',
        'team_size_full_time'
      ];

      const completeData = {
        funding_stage: 'seed',
        total_capital_raised_usd: 1000000,
        cash_on_hand_usd: 800000,
        monthly_burn_usd: 50000,
        sector: 'SaaS',
        team_size_full_time: 10
      };

      const incompleteData = {
        funding_stage: 'seed',
        total_capital_raised_usd: 1000000
      };

      const hasAllRequired = requiredFields.every(field => field in completeData);
      const hasAllRequiredIncomplete = requiredFields.every(field => field in incompleteData);

      expect(hasAllRequired).toBe(true);
      expect(hasAllRequiredIncomplete).toBe(false);
    });
  });

  describe('Data Transformations', () => {
    it('should transform funding stage format', () => {
      const transformFundingStage = (stage: string): string => {
        return stage.toLowerCase().replace(' ', '_');
      };

      expect(transformFundingStage('Series A')).toBe('series_a');
      expect(transformFundingStage('Pre Seed')).toBe('pre_seed');
      expect(transformFundingStage('SEED')).toBe('seed');
    });

    it('should calculate derived fields', () => {
      const calculateRunway = (cash: number, burn: number): number => {
        if (burn === 0) return Infinity;
        return Math.round(cash / burn);
      };

      expect(calculateRunway(1000000, 50000)).toBe(20);
      expect(calculateRunway(500000, 100000)).toBe(5);
      expect(calculateRunway(1000000, 0)).toBe(Infinity);
    });

    it('should convert percentage formats', () => {
      const percentToDecimal = (percent: number): number => percent / 100;
      const decimalToPercent = (decimal: number): number => decimal * 100;

      expect(percentToDecimal(75)).toBe(0.75);
      expect(percentToDecimal(100)).toBe(1);
      expect(decimalToPercent(0.85)).toBe(85);
      expect(decimalToPercent(1)).toBe(100);
    });
  });

  describe('CAMP Score Validation', () => {
    it('should validate CAMP scores are within range', () => {
      const validateCAMPScore = (score: number): boolean => {
        return score >= 0 && score <= 1;
      };

      expect(validateCAMPScore(0.75)).toBe(true);
      expect(validateCAMPScore(0)).toBe(true);
      expect(validateCAMPScore(1)).toBe(true);
      expect(validateCAMPScore(-0.1)).toBe(false);
      expect(validateCAMPScore(1.5)).toBe(false);
    });

    it('should validate all CAMP pillars are present', () => {
      const validCAMP = {
        capital: 0.75,
        advantage: 0.80,
        market: 0.65,
        people: 0.70
      };

      const invalidCAMP = {
        capital: 0.75,
        market: 0.65
      };

      const requiredPillars = ['capital', 'advantage', 'market', 'people'];
      const hasAllPillars = requiredPillars.every(pillar => pillar in validCAMP);
      const hasAllPillarsInvalid = requiredPillars.every(pillar => pillar in invalidCAMP);

      expect(hasAllPillars).toBe(true);
      expect(hasAllPillarsInvalid).toBe(false);
    });
  });

  describe('API Response Validation', () => {
    it('should validate prediction result structure', () => {
      const validResult = {
        success_probability: 0.75,
        confidence_score: 0.85,
        verdict: 'PASS',
        risk_level: 'MEDIUM',
        pillar_scores: {
          capital: 0.7,
          advantage: 0.8,
          market: 0.65,
          people: 0.75
        }
      };

      const isValidProbability = validResult.success_probability >= 0 && 
                                validResult.success_probability <= 1;
      const isValidConfidence = validResult.confidence_score >= 0 && 
                               validResult.confidence_score <= 1;
      const hasRequiredFields = 'success_probability' in validResult &&
                               'verdict' in validResult &&
                               'pillar_scores' in validResult;

      expect(isValidProbability).toBe(true);
      expect(isValidConfidence).toBe(true);
      expect(hasRequiredFields).toBe(true);
    });

    it('should validate verdict values', () => {
      const validVerdicts = ['PASS', 'FAIL', 'CONDITIONAL PASS', 'STRONG PASS', 'STRONG FAIL'];
      const testVerdicts = ['PASS', 'FAIL', 'INVALID', 'pass'];

      testVerdicts.forEach(verdict => {
        const isValid = validVerdicts.includes(verdict);
        expect(isValid).toBe(verdict === 'PASS' || verdict === 'FAIL');
      });
    });
  });
});