/**
 * Industry-specific benchmarks by sector and stage
 * Based on real market data and industry research
 */

export interface Benchmark {
  metric: string;
  description: string;
  p25: string;
  p50: string;
  p75: string;
  unit?: string;
}

export interface SectorBenchmarks {
  [sector: string]: {
    [stage: string]: {
      revenue_growth: Benchmark;
      burn_multiple: Benchmark;
      team_size: Benchmark;
      ltv_cac: Benchmark;
      gross_margin: Benchmark;
      runway_months: Benchmark;
    }
  }
}

export const INDUSTRY_BENCHMARKS: SectorBenchmarks = {
  saas: {
    pre_seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for SaaS pre-seed',
        p25: '0%',
        p50: '50%',
        p75: '200%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '5.0x',
        p50: '3.0x',
        p75: '2.0x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '2',
        p50: '3',
        p75: '5',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '0.5:1',
        p50: '1.0:1',
        p75: '2.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '60%',
        p50: '70%',
        p75: '80%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '6',
        p50: '12',
        p75: '18',
        unit: 'months'
      }
    },
    seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for SaaS seed',
        p25: '100%',
        p50: '200%',
        p75: '400%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '3.5x',
        p50: '2.5x',
        p75: '1.5x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '5',
        p50: '10',
        p75: '20',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.5:1',
        p50: '3.0:1',
        p75: '5.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '65%',
        p50: '75%',
        p75: '85%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '24',
        unit: 'months'
      }
    },
    series_a: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for SaaS Series A',
        p25: '80%',
        p50: '150%',
        p75: '300%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '3.0x',
        p50: '2.0x',
        p75: '1.2x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '20',
        p50: '40',
        p75: '80',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '2.0:1',
        p50: '3.5:1',
        p75: '6.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '70%',
        p50: '78%',
        p75: '85%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '24',
        unit: 'months'
      }
    }
  },
  
  fintech: {
    pre_seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for FinTech pre-seed',
        p25: '0%',
        p50: '0%',
        p75: '100%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '8.0x',
        p50: '5.0x',
        p75: '3.0x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '3',
        p50: '5',
        p75: '8',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '0.3:1',
        p50: '0.8:1',
        p75: '1.5:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '40%',
        p50: '55%',
        p75: '70%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '9',
        p50: '15',
        p75: '24',
        unit: 'months'
      }
    },
    seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for FinTech seed',
        p25: '50%',
        p50: '150%',
        p75: '350%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '4.0x',
        p50: '2.8x',
        p75: '1.8x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '8',
        p50: '15',
        p75: '30',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.2:1',
        p50: '2.5:1',
        p75: '4.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '50%',
        p50: '65%',
        p75: '75%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '24',
        unit: 'months'
      }
    },
    series_a: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for FinTech Series A',
        p25: '60%',
        p50: '120%',
        p75: '250%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '3.5x',
        p50: '2.3x',
        p75: '1.4x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '30',
        p50: '60',
        p75: '120',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.8:1',
        p50: '3.0:1',
        p75: '5.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '60%',
        p50: '70%',
        p75: '80%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '15',
        p50: '20',
        p75: '30',
        unit: 'months'
      }
    }
  },

  marketplace: {
    pre_seed: {
      revenue_growth: {
        metric: 'Revenue Growth (GMV)',
        description: 'YoY GMV growth for marketplace pre-seed',
        p25: '0%',
        p50: '100%',
        p75: '300%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '6.0x',
        p50: '4.0x',
        p75: '2.5x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '2',
        p50: '4',
        p75: '7',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '0.8:1',
        p50: '1.5:1',
        p75: '2.5:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Take Rate',
        description: 'Marketplace commission rate',
        p25: '10%',
        p50: '15%',
        p75: '20%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '8',
        p50: '14',
        p75: '20',
        unit: 'months'
      }
    },
    seed: {
      revenue_growth: {
        metric: 'Revenue Growth (GMV)',
        description: 'YoY GMV growth for marketplace seed',
        p25: '150%',
        p50: '300%',
        p75: '600%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '4.5x',
        p50: '3.0x',
        p75: '2.0x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '8',
        p50: '15',
        p75: '25',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.2:1',
        p50: '2.0:1',
        p75: '3.5:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Take Rate',
        description: 'Marketplace commission rate',
        p25: '12%',
        p50: '18%',
        p75: '25%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '16',
        p75: '24',
        unit: 'months'
      }
    },
    series_a: {
      revenue_growth: {
        metric: 'Revenue Growth (GMV)',
        description: 'YoY GMV growth for marketplace Series A',
        p25: '100%',
        p50: '200%',
        p75: '400%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '3.8x',
        p50: '2.5x',
        p75: '1.6x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '25',
        p50: '50',
        p75: '100',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.5:1',
        p50: '2.5:1',
        p75: '4.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Take Rate',
        description: 'Marketplace commission rate',
        p25: '15%',
        p50: '20%',
        p75: '28%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '24',
        unit: 'months'
      }
    }
  },

  healthtech: {
    pre_seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for HealthTech pre-seed',
        p25: '0%',
        p50: '0%',
        p75: '50%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '10.0x',
        p50: '6.0x',
        p75: '3.5x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '3',
        p50: '5',
        p75: '10',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '0.2:1',
        p50: '0.5:1',
        p75: '1.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '30%',
        p50: '50%',
        p75: '70%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '30',
        unit: 'months'
      }
    },
    seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for HealthTech seed',
        p25: '50%',
        p50: '120%',
        p75: '250%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '5.0x',
        p50: '3.5x',
        p75: '2.2x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '10',
        p50: '20',
        p75: '40',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.0:1',
        p50: '2.0:1',
        p75: '3.5:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '45%',
        p50: '60%',
        p75: '75%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '15',
        p50: '20',
        p75: '30',
        unit: 'months'
      }
    },
    series_a: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth for HealthTech Series A',
        p25: '70%',
        p50: '130%',
        p75: '220%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '4.0x',
        p50: '2.7x',
        p75: '1.8x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '35',
        p50: '70',
        p75: '150',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.5:1',
        p50: '2.8:1',
        p75: '4.5:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '55%',
        p50: '68%',
        p75: '80%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '15',
        p50: '22',
        p75: '36',
        unit: 'months'
      }
    }
  },

  // Default benchmarks for other sectors
  default: {
    pre_seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth',
        p25: '0%',
        p50: '25%',
        p75: '150%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '7.0x',
        p50: '4.0x',
        p75: '2.5x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '2',
        p50: '4',
        p75: '8',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '0.5:1',
        p50: '1.0:1',
        p75: '2.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '40%',
        p50: '60%',
        p75: '75%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '9',
        p50: '15',
        p75: '24',
        unit: 'months'
      }
    },
    seed: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth',
        p25: '75%',
        p50: '175%',
        p75: '350%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '4.0x',
        p50: '2.7x',
        p75: '1.7x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '7',
        p50: '12',
        p75: '25',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.3:1',
        p50: '2.5:1',
        p75: '4.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '50%',
        p50: '65%',
        p75: '80%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '24',
        unit: 'months'
      }
    },
    series_a: {
      revenue_growth: {
        metric: 'Revenue Growth',
        description: 'YoY revenue growth',
        p25: '70%',
        p50: '140%',
        p75: '280%',
        unit: 'percent'
      },
      burn_multiple: {
        metric: 'Burn Multiple',
        description: 'Efficiency of growth spending',
        p25: '3.3x',
        p50: '2.2x',
        p75: '1.5x',
        unit: 'multiple'
      },
      team_size: {
        metric: 'Team Size',
        description: 'Full-time employees',
        p25: '25',
        p50: '50',
        p75: '100',
        unit: 'people'
      },
      ltv_cac: {
        metric: 'LTV/CAC Ratio',
        description: 'Customer lifetime value vs acquisition cost',
        p25: '1.8:1',
        p50: '3.0:1',
        p75: '5.0:1',
        unit: 'ratio'
      },
      gross_margin: {
        metric: 'Gross Margin',
        description: 'Revenue after direct costs',
        p25: '60%',
        p50: '72%',
        p75: '82%',
        unit: 'percent'
      },
      runway_months: {
        metric: 'Runway',
        description: 'Months of cash remaining',
        p25: '12',
        p50: '18',
        p75: '27',
        unit: 'months'
      }
    }
  }
};

/**
 * Calculate percentile based on actual value and benchmarks
 */
export function calculatePercentile(
  value: number,
  p25: number,
  p50: number,
  p75: number,
  inverse: boolean = false
): number {
  // For metrics where lower is better (like burn multiple)
  if (inverse) {
    if (value >= p25) return 15;
    if (value >= p50) return 35;
    if (value >= p75) return 60;
    return 85;
  }
  
  // For metrics where higher is better
  if (value <= p25) return 15;
  if (value <= p50) return 35;
  if (value <= p75) return 60;
  return 85;
}

/**
 * Get benchmarks for a specific sector and stage
 */
export function getBenchmarksForSectorStage(
  sector: string,
  stage: string
): typeof INDUSTRY_BENCHMARKS.default.pre_seed {
  const normalizedSector = sector?.toLowerCase() || 'default';
  const normalizedStage = stage?.toLowerCase().replace(/[\s-]/g, '_') || 'seed';
  
  // Try to find exact match
  if (INDUSTRY_BENCHMARKS[normalizedSector]?.[normalizedStage]) {
    return INDUSTRY_BENCHMARKS[normalizedSector][normalizedStage];
  }
  
  // Fall back to default benchmarks for the stage
  if (INDUSTRY_BENCHMARKS.default[normalizedStage]) {
    return INDUSTRY_BENCHMARKS.default[normalizedStage];
  }
  
  // Ultimate fallback
  return INDUSTRY_BENCHMARKS.default.seed;
}

/**
 * Extract numeric value from benchmark string
 */
export function extractBenchmarkValue(benchmark: string): number {
  // Remove percentage signs, 'x' for multiples, and ratio formatting
  const cleaned = benchmark.replace(/[%x:]/g, '').trim();
  const value = parseFloat(cleaned);
  return isNaN(value) ? 0 : value;
}