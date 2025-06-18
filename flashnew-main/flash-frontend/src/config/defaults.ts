/**
 * Default Configuration Values
 * These serve as the baseline configuration for FLASH
 */

import { IConfiguration } from './types';

export const defaultConfiguration: IConfiguration = {
  version: '1.0.0',
  environment: (process.env.NODE_ENV || 'development') as any,
  
  features: {
    llmRecommendations: true,
    industryBenchmarks: true,
    whatIfAnalysis: true,
    exportPDF: true,
    advancedMetrics: false,
    adminPanel: false,
    debugMode: process.env.NODE_ENV === 'development',
  },
  
  thresholds: {
    success: {
      probability: {
        excellent: 0.75,
        good: 0.65,
        fair: 0.55,
        poor: 0.45,
        byStage: {
          'pre_seed': {
            excellent: 0.70,
            good: 0.60,
            fair: 0.50,
            poor: 0.40,
          },
          'seed': {
            excellent: 0.72,
            good: 0.62,
            fair: 0.52,
            poor: 0.42,
          },
          'series_a': {
            excellent: 0.80,
            good: 0.70,
            fair: 0.60,
            poor: 0.50,
          },
          'series_b': {
            excellent: 0.85,
            good: 0.75,
            fair: 0.65,
            poor: 0.55,
          },
        },
        bySector: {
          'saas': {
            excellent: 0.77,
            good: 0.67,
            fair: 0.57,
            poor: 0.47,
          },
          'deeptech': {
            excellent: 0.70,
            good: 0.60,
            fair: 0.50,
            poor: 0.40,
          },
          'marketplace': {
            excellent: 0.73,
            good: 0.63,
            fair: 0.53,
            poor: 0.43,
          },
        },
      },
      improvements: {
        maxImprovement: 0.15,
        perActionImprovement: 0.02,
        milestoneActions: [3, 5, 10],
        algorithm: 'logarithmic',
        calculateImprovement: (current: number, actions: number) => {
          // Logarithmic improvement with diminishing returns
          const baseImprovement = Math.log(actions + 1) * 0.05;
          const maxPossible = 1 - current; // Can't exceed 100%
          const improvement = Math.min(baseImprovement, maxPossible * 0.5, 0.15);
          return improvement;
        },
      },
      confidence: {
        veryHigh: 0.85,
        high: 0.70,
        moderate: 0.50,
        low: 0.30,
      },
    },
    
    risk: {
      runway: {
        critical: 3,
        warning: 6,
        safe: 12,
        comfortable: 18,
        byStage: {
          'pre_seed': {
            critical: 2,
            warning: 4,
            safe: 8,
            comfortable: 12,
          },
          'seed': {
            critical: 3,
            warning: 6,
            safe: 12,
            comfortable: 18,
          },
          'series_a': {
            critical: 6,
            warning: 9,
            safe: 15,
            comfortable: 24,
          },
        },
      },
      burnMultiple: {
        excellent: 1.5,
        good: 2.0,
        warning: 2.5,
        critical: 3.0,
        byStage: {
          'pre_seed': {
            excellent: 2.0,
            good: 3.0,
            warning: 4.0,
            critical: 5.0,
          },
          'seed': {
            excellent: 1.8,
            good: 2.5,
            warning: 3.0,
            critical: 4.0,
          },
          'series_a': {
            excellent: 1.5,
            good: 2.0,
            warning: 2.5,
            critical: 3.0,
          },
          'growth': {
            excellent: 1.2,
            good: 1.5,
            warning: 2.0,
            critical: 2.5,
          },
        },
      },
      concentration: {
        low: 0.15,
        medium: 0.30,
        high: 0.50,
        extreme: 0.70,
      },
      churn: {
        excellent: 0.02,
        good: 0.05,
        warning: 0.10,
        critical: 0.20,
      },
    },
    
    performance: {
      revenue: {
        growth: {
          hypergrowth: 3.0,  // 300% YoY
          high: 2.0,         // 200% YoY
          moderate: 1.0,     // 100% YoY
          low: 0.5,          // 50% YoY
          byStage: {
            'pre_seed': {
              hypergrowth: 5.0,  // 500% (from small base)
              high: 3.0,
              moderate: 1.5,
              low: 0.5,
            },
            'seed': {
              hypergrowth: 4.0,
              high: 2.5,
              moderate: 1.5,
              low: 0.75,
            },
            'series_a': {
              hypergrowth: 3.0,
              high: 2.0,
              moderate: 1.0,
              low: 0.5,
            },
            'series_b': {
              hypergrowth: 2.0,
              high: 1.5,
              moderate: 0.8,
              low: 0.4,
            },
          },
        },
      },
      ltv_cac: {
        excellent: 3.0,
        good: 2.0,
        fair: 1.5,
        poor: 1.0,
        bySector: {
          'saas': {
            excellent: 3.5,
            good: 2.5,
            fair: 1.8,
            poor: 1.2,
          },
          'marketplace': {
            excellent: 2.5,
            good: 1.8,
            fair: 1.3,
            poor: 0.8,
          },
          'ecommerce': {
            excellent: 2.0,
            good: 1.5,
            fair: 1.2,
            poor: 0.8,
          },
        },
      },
      grossMargin: {
        excellent: 0.80,
        good: 0.70,
        fair: 0.60,
        poor: 0.50,
        bySector: {
          'saas': {
            excellent: 0.85,
            good: 0.75,
            fair: 0.65,
            poor: 0.55,
          },
          'marketplace': {
            excellent: 0.30,  // Take rate
            good: 0.20,
            fair: 0.15,
            poor: 0.10,
          },
          'ecommerce': {
            excellent: 0.50,
            good: 0.40,
            fair: 0.30,
            poor: 0.20,
          },
          'fintech': {
            excellent: 0.70,
            good: 0.60,
            fair: 0.50,
            poor: 0.40,
          },
        },
      },
    },
    
    metrics: {
      team: {
        size: {
          minimum: 2,
          optimal: 15,
          maximum: 50,
          byStage: {
            'pre_seed': {
              minimum: 1,
              optimal: 3,
              maximum: 5,
            },
            'seed': {
              minimum: 3,
              optimal: 8,
              maximum: 15,
            },
            'series_a': {
              minimum: 10,
              optimal: 25,
              maximum: 50,
            },
            'series_b': {
              minimum: 25,
              optimal: 60,
              maximum: 120,
            },
          },
        },
        experience: {
          junior: 2,
          mid: 5,
          senior: 10,
          expert: 15,
        },
        diversity: {
          low: 0.20,
          moderate: 0.40,
          high: 0.60,
          excellent: 0.80,
        },
      },
      market: {
        tam: {
          small: 1_000_000_000,      // $1B
          medium: 10_000_000_000,    // $10B
          large: 50_000_000_000,     // $50B
          huge: 100_000_000_000,     // $100B+
        },
        competition: {
          low: 1,
          medium: 2,
          high: 3,
          extreme: 4,
        },
        growth: {
          declining: -0.05,  // -5% YoY
          stable: 0.05,      // 5% YoY
          growing: 0.15,     // 15% YoY
          explosive: 0.30,   // 30%+ YoY
        },
      },
      product: {
        nps: {
          poor: 0,
          fair: 20,
          good: 50,
          excellent: 70,
        },
        retention: {
          poor: 0.70,
          fair: 0.80,
          good: 0.90,
          excellent: 0.95,
        },
      },
    },
  },
  
  defaults: {
    confidence: 0.50,
    probability: 0.50,
    runway: 12,
    burnMultiple: 2.0,
    teamSize: 10,
    experience: 5,
    grossMargin: 0.70,
    ltvCac: 3.0,
    churnRate: 0.05,
    nps: 50,
  },
  
  ui: {
    animation: {
      enabled: true,
      duration: {
        fast: 200,
        normal: 400,
        slow: 600,
      },
      delay: {
        short: 50,
        medium: 100,
        long: 200,
      },
      type: 'spring',
      easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
      reducedMotion: false,
      springConfig: {
        stiffness: 100,
        damping: 15,
        mass: 1,
      },
    },
    charts: {
      radar: {
        radius: 120,
        levels: 5,
        pointRadius: 6,
        labelOffset: 1.25,
        strokeWidth: 3,
        responsive: true,
      },
      colors: {
        success: '#00C851',
        warning: '#FF8800',
        danger: '#FF4444',
        info: '#33B5E5',
        neutral: '#78909C',
        gradients: true,
        opacity: {
          fill: 0.2,
          stroke: 0.8,
          hover: 0.9,
        },
      },
    },
    colors: {
      brand: {
        primary: '#007AFF',
        secondary: '#5856D6',
        accent: '#FF9500',
      },
      semantic: {
        success: '#00C851',
        warning: '#FF8800',
        danger: '#FF4444',
        info: '#33B5E5',
      },
      chart: {
        series: ['#007AFF', '#5856D6', '#FF9500', '#00C851', '#FF3B30'],
        background: 'rgba(255, 255, 255, 0.02)',
        grid: 'rgba(255, 255, 255, 0.1)',
      },
      text: {
        primary: '#FFFFFF',
        secondary: 'rgba(255, 255, 255, 0.7)',
        disabled: 'rgba(255, 255, 255, 0.3)',
        inverse: '#000000',
      },
      background: {
        primary: '#0A0A0C',
        secondary: '#1A1A1F',
        elevated: '#2A2A2F',
        overlay: 'rgba(0, 0, 0, 0.8)',
      },
    },
    layout: {
      maxWidth: 1200,
      spacing: {
        xs: 4,
        sm: 8,
        md: 16,
        lg: 24,
        xl: 32,
      },
      borderRadius: {
        sm: 4,
        md: 8,
        lg: 12,
        full: 9999,
      },
      breakpoints: {
        mobile: 480,
        tablet: 768,
        desktop: 1024,
        wide: 1440,
      },
    },
    numbers: {
      percentageDecimals: 0,
      currencyDecimals: 0,
      scoreDecimals: 1,
      locale: 'en-US',
      currency: 'USD',
    },
    display: {
      emojis: {
        excellent: '🚀',
        good: '✅',
        fair: '⚡',
        poor: '⚠️'
      },
      limits: {
        strengths: 3,
        risks: 3,
        recommendations: 5,
        patterns: 4
      }
    },
  },
  
  business: {
    scoring: {
      algorithm: 'hybrid',
      weights: {
        camp: {
          capital: 0.25,
          advantage: 0.25,
          market: 0.25,
          people: 0.25,
        },
        models: {
          dna: 0.25,
          temporal: 0.25,
          industry: 0.25,
          ensemble: 0.25,
        },
      },
      adjustments: {
        stageMultipliers: {
          'pre_seed': 0.8,
          'seed': 0.9,
          'series_a': 1.0,
          'series_b': 1.1,
          'growth': 1.2,
        },
        sectorMultipliers: {
          'deeptech': 0.9,
          'saas': 1.1,
          'marketplace': 1.0,
          'fintech': 1.05,
          'healthtech': 0.95,
        },
      },
    },
    validation: {
      required: [
        'funding_stage',
        'sector',
        'team_size_full_time',
        'total_capital_raised_usd',
      ],
      ranges: {
        'team_size_full_time': { min: 1, max: 10000 },
        'total_capital_raised_usd': { min: 0, max: 10_000_000_000 },
        'annual_revenue_run_rate': { min: 0, max: 10_000_000_000 },
        'runway_months': { min: 0, max: 120 },
        'burn_multiple': { min: 0, max: 100 },
        'ltv_cac_ratio': { min: 0, max: 100 },
        'gross_margin_percent': { min: -100, max: 100 },
        'revenue_growth_rate_percent': { min: -100, max: 10000 },
      },
      patterns: {},
      custom: {},
    },
    calculation: {
      burnRate: (raised: number, runway: number) => {
        if (runway <= 0) return 0;
        return raised / runway;
      },
      ltvCac: (ltv: number, cac: number) => {
        if (cac <= 0) return 0;
        return ltv / cac;
      },
      growthRate: (current: number, previous: number) => {
        if (previous <= 0) return current > 0 ? 1 : 0;
        return (current - previous) / previous;
      },
      marketShare: (revenue: number, tam: number) => {
        if (tam <= 0) return 0;
        return revenue / tam;
      },
    },
    stageWeights: {
      pre_seed: {
        people: 0.40,
        advantage: 0.30,
        market: 0.20,
        capital: 0.10
      },
      seed: {
        people: 0.30,
        advantage: 0.30,
        market: 0.25,
        capital: 0.15
      },
      series_a: {
        market: 0.30,
        people: 0.25,
        advantage: 0.25,
        capital: 0.20
      },
      series_b: {
        market: 0.35,
        capital: 0.25,
        advantage: 0.20,
        people: 0.20
      },
      series_c: {
        capital: 0.35,
        market: 0.30,
        people: 0.20,
        advantage: 0.15
      },
      growth: {
        capital: 0.35,
        market: 0.30,
        people: 0.20,
        advantage: 0.15
      }
    },
    analysis: {
      modelWeights: {
        base: 0.35,
        patterns: 0.25,
        stage: 0.15,
        industry: 0.15,
        camp: 0.10
      },
      successFactors: 45,
      patternCount: 10
    },
    benchmarks: {
      revenue: {
        'pre_seed': { p25: 0, p50: 10000, p75: 50000 },
        'seed': { p25: 50000, p50: 250000, p75: 1000000 },
        'series_a': { p25: 1000000, p50: 3000000, p75: 10000000 },
      },
      growth: {
        'pre_seed': { p25: 0, p50: 50, p75: 200 },
        'seed': { p25: 50, p50: 100, p75: 300 },
        'series_a': { p25: 100, p50: 150, p75: 200 },
      }
    }
  },
  
  messages: {
    success: {
      excellent: 'Exceptional opportunity with strong fundamentals across all dimensions',
      good: 'Promising opportunity with solid metrics and growth potential',
      fair: 'Moderate opportunity with areas for improvement',
      poor: 'Significant improvements needed across multiple areas',
    },
    risk: {
      low: 'Well-managed risk profile with strong mitigation strategies',
      medium: 'Moderate risk levels requiring ongoing monitoring',
      high: 'Elevated risk factors requiring immediate attention',
      critical: 'Critical risk levels threatening business viability',
    },
    improvements: {
      available: 'By implementing these recommendations, you could improve your success score by up to {amount} percentage points.',
      completed: 'Great progress! You\'ve completed {count} improvement actions.',
      milestone: 'Milestone achieved! You\'re {count} actions away from the next level.',
    },
    errors: {
      validation: 'Please check your input values and try again.',
      network: 'Unable to connect to the server. Please check your connection.',
      calculation: 'An error occurred during calculation. Please try again.',
      generic: 'Something went wrong. Please try again later.',
    },
    recommendations: {
      capital: [
        'Reduce burn rate by focusing on essential expenses',
        'Improve unit economics through pricing optimization',
        'Extend runway through revenue growth or funding',
        'Track and optimize customer acquisition costs'
      ],
      advantage: [
        'Strengthen IP protection through patents or trade secrets',
        'Build deeper technical moats in your product',
        'Create switching costs for customers',
        'Develop unique data assets or algorithms'
      ],
      market: [
        'Validate market size with customer research',
        'Expand to adjacent market segments',
        'Accelerate go-to-market strategies',
        'Build strategic partnerships for distribution'
      ],
      people: [
        'Hire senior talent in key positions',
        'Build advisory board with industry experts',
        'Implement employee retention programs',
        'Invest in team training and development'
      ]
    },
  },
  
  experimental: {
    enableMLWhatIf: true,
    enableStreaming: false,
    enableWebSockets: false,
    enableOfflineMode: false,
    enableBetaFeatures: false,
    experiments: {},
  },
};