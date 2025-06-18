// Dynamic Scoring System - Extracts 20+ derived metrics from existing data
// This is where we turn raw data into strategic intelligence

interface CompanyMetrics {
  // Direct metrics from assessment
  revenue: number;
  burn: number;
  runway: number;
  cash: number;
  teamSize: number;
  fundingRaised: number;
  marketGrowth: number;
  marketShare: number;
  competitorCount: number;
  churn: number;
  nps: number;
  cac: number;
  ltv: number;
  productStage: string;
  fundingStage: string;
}

interface DerivedMetrics {
  // Efficiency Metrics
  burnMultiple: number;
  efficiencyRatio: number;
  capitalEfficiency: number;
  revenuePerEmployee: number;
  cashEfficiency: number;
  
  // Growth Metrics
  growthEfficiency: number;
  marketCapturePotential: number;
  velocityScore: number;
  scalabilityIndex: number;
  
  // Strategic Position Metrics
  competitiveIntensity: number;
  marketPositionStrength: number;
  defensibilityScore: number;
  strategicMomentum: number;
  
  // Risk Metrics
  runwayRisk: number;
  concentrationRisk: number;
  executionRisk: number;
  marketRisk: number;
  
  // Opportunity Metrics
  expansionPotential: number;
  improvementHeadroom: number;
  marketTimingScore: number;
  
  // Composite Scores
  overallStrength: number;
  strategicReadiness: number;
  investabilityScore: number;
}

interface IndustryBenchmarks {
  medianBurnMultiple: number;
  topQuartileEfficiency: number;
  medianChurn: number;
  goodLtvCacRatio: number;
  healthyGrowthRate: number;
}

export class DynamicScoringSystem {
  private industryBenchmarks: { [key: string]: IndustryBenchmarks } = {
    'saas': {
      medianBurnMultiple: 1.5,
      topQuartileEfficiency: 0.7,
      medianChurn: 5,
      goodLtvCacRatio: 3,
      healthyGrowthRate: 100
    },
    'marketplace': {
      medianBurnMultiple: 2.0,
      topQuartileEfficiency: 0.5,
      medianChurn: 8,
      goodLtvCacRatio: 2.5,
      healthyGrowthRate: 150
    },
    'fintech': {
      medianBurnMultiple: 2.5,
      topQuartileEfficiency: 0.4,
      medianChurn: 3,
      goodLtvCacRatio: 4,
      healthyGrowthRate: 80
    }
  };

  /**
   * Calculate all derived metrics from raw company data
   */
  calculateDerivedMetrics(metrics: CompanyMetrics, industry: string = 'saas'): DerivedMetrics {
    const benchmarks = this.industryBenchmarks[industry] || this.industryBenchmarks['saas'];
    
    return {
      // Efficiency Metrics
      burnMultiple: this.calculateBurnMultiple(metrics),
      efficiencyRatio: this.calculateEfficiencyRatio(metrics),
      capitalEfficiency: this.calculateCapitalEfficiency(metrics),
      revenuePerEmployee: metrics.revenue / Math.max(1, metrics.teamSize),
      cashEfficiency: this.calculateCashEfficiency(metrics),
      
      // Growth Metrics
      growthEfficiency: this.calculateGrowthEfficiency(metrics),
      marketCapturePotential: this.calculateMarketCapturePotential(metrics),
      velocityScore: this.calculateVelocityScore(metrics),
      scalabilityIndex: this.calculateScalabilityIndex(metrics),
      
      // Strategic Position Metrics
      competitiveIntensity: this.calculateCompetitiveIntensity(metrics),
      marketPositionStrength: this.calculateMarketPositionStrength(metrics),
      defensibilityScore: this.calculateDefensibilityScore(metrics),
      strategicMomentum: this.calculateStrategicMomentum(metrics),
      
      // Risk Metrics
      runwayRisk: this.calculateRunwayRisk(metrics),
      concentrationRisk: this.calculateConcentrationRisk(metrics),
      executionRisk: this.calculateExecutionRisk(metrics),
      marketRisk: this.calculateMarketRisk(metrics),
      
      // Opportunity Metrics
      expansionPotential: this.calculateExpansionPotential(metrics),
      improvementHeadroom: this.calculateImprovementHeadroom(metrics, benchmarks),
      marketTimingScore: this.calculateMarketTimingScore(metrics),
      
      // Composite Scores
      overallStrength: 0, // Calculated after all others
      strategicReadiness: 0, // Calculated after all others
      investabilityScore: 0 // Calculated after all others
    };
  }

  /**
   * Efficiency Metrics Calculations
   */
  private calculateBurnMultiple(m: CompanyMetrics): number {
    if (m.revenue === 0) return 10; // Pre-revenue companies get max burn multiple
    const newRevenue = m.revenue / 12; // Monthly new revenue estimate
    return Math.min(10, m.burn / Math.max(1, newRevenue));
  }

  private calculateEfficiencyRatio(m: CompanyMetrics): number {
    if (m.revenue === 0) return 0;
    return Math.min(1, m.revenue / (m.burn * 12));
  }

  private calculateCapitalEfficiency(m: CompanyMetrics): number {
    if (m.fundingRaised === 0) return 0;
    return m.revenue / m.fundingRaised;
  }

  private calculateCashEfficiency(m: CompanyMetrics): number {
    // How many months of runway per million raised
    const millionsRaised = m.fundingRaised / 1000000;
    if (millionsRaised === 0) return 0;
    return m.runway / millionsRaised;
  }

  /**
   * Growth Metrics Calculations
   */
  private calculateGrowthEfficiency(m: CompanyMetrics): number {
    // Growth rate relative to burn
    if (m.burn === 0) return 0;
    const monthlyGrowth = m.marketGrowth / 12;
    const growthPerBurnDollar = monthlyGrowth / m.burn;
    return Math.min(100, growthPerBurnDollar * 1000000); // Normalized score
  }

  private calculateMarketCapturePotential(m: CompanyMetrics): number {
    // Current share vs market growth vs competition
    const growthFactor = Math.min(2, m.marketGrowth / 20);
    const competitionFactor = Math.max(0.1, 1 - (m.competitorCount / 100));
    const shareFactor = Math.min(2, m.marketShare * 10);
    
    return (growthFactor * competitionFactor * shareFactor) * 25;
  }

  private calculateVelocityScore(m: CompanyMetrics): number {
    // Speed of progress relative to stage
    const stageMonths = {
      'pre-seed': 6,
      'seed': 12,
      'series-a': 24,
      'series-b': 36,
      'series-c': 48
    };
    
    const expectedMonths = stageMonths[m.fundingStage] || 24;
    const velocityMultiplier = m.revenue > 0 ? 2 : 1;
    
    return Math.min(100, (expectedMonths / m.runway) * 50 * velocityMultiplier);
  }

  private calculateScalabilityIndex(m: CompanyMetrics): number {
    // LTV/CAC * (1 - churn) * market growth factor
    const unitEconomics = m.ltv / Math.max(1, m.cac);
    const retentionFactor = 1 - (m.churn / 100);
    const growthFactor = m.marketGrowth / 100;
    
    return Math.min(100, unitEconomics * retentionFactor * growthFactor * 20);
  }

  /**
   * Strategic Position Metrics
   */
  private calculateCompetitiveIntensity(m: CompanyMetrics): number {
    // More competitors + lower market share = higher intensity
    const competitorPressure = Math.min(100, m.competitorCount * 2);
    const marketSharePressure = Math.max(0, 100 - (m.marketShare * 100));
    
    return (competitorPressure + marketSharePressure) / 2;
  }

  private calculateMarketPositionStrength(m: CompanyMetrics): number {
    // Market share * NPS * retention
    const shareFactor = Math.min(50, m.marketShare * 500);
    const satisfactionFactor = Math.min(30, m.nps / 3);
    const retentionFactor = Math.min(20, (100 - m.churn) / 5);
    
    return shareFactor + satisfactionFactor + retentionFactor;
  }

  private calculateDefensibilityScore(m: CompanyMetrics): number {
    // Based on switching costs, network effects, regulatory barriers
    let score = 20; // Base defensibility
    
    // Network effects proxy (if marketplace or high NPS)
    if (m.nps > 60) score += 20;
    
    // Switching cost proxy (low churn = high switching costs)
    if (m.churn < 3) score += 30;
    else if (m.churn < 5) score += 20;
    else if (m.churn < 10) score += 10;
    
    // Market position bonus
    if (m.marketShare > 0.1) score += 20;
    
    // Technology moat proxy (high LTV/CAC suggests differentiation)
    if (m.ltv / m.cac > 5) score += 10;
    
    return Math.min(100, score);
  }

  private calculateStrategicMomentum(m: CompanyMetrics): number {
    // Combination of growth, efficiency improvement, market timing
    const growthMomentum = Math.min(40, m.marketGrowth / 2.5);
    const efficiencyMomentum = m.revenue > 0 ? 20 : 0;
    const timingMomentum = m.marketGrowth > 20 ? 20 : 10;
    const executionMomentum = m.runway > 12 ? 20 : 10;
    
    return growthMomentum + efficiencyMomentum + timingMomentum + executionMomentum;
  }

  /**
   * Risk Metrics Calculations
   */
  private calculateRunwayRisk(m: CompanyMetrics): number {
    // Inverse of runway with adjustments
    if (m.runway >= 24) return 10;
    if (m.runway >= 18) return 20;
    if (m.runway >= 12) return 40;
    if (m.runway >= 9) return 60;
    if (m.runway >= 6) return 80;
    return 95;
  }

  private calculateConcentrationRisk(m: CompanyMetrics): number {
    // Customer concentration + revenue concentration
    let risk = 20; // Base risk
    
    // Single market risk
    if (m.competitorCount > 50) risk += 20;
    
    // Pre-revenue risk
    if (m.revenue === 0) risk += 30;
    
    // Small team risk
    if (m.teamSize < 5) risk += 20;
    
    // High burn risk
    if (m.burn > m.revenue / 6) risk += 10;
    
    return Math.min(100, risk);
  }

  private calculateExecutionRisk(m: CompanyMetrics): number {
    // Team size vs ambition, burn rate vs progress
    const teamRisk = m.teamSize < 10 ? 30 : m.teamSize > 50 ? 20 : 10;
    const burnRisk = this.calculateBurnMultiple(m) > 3 ? 30 : 10;
    const stageRisk = m.productStage === 'idea' ? 30 : m.productStage === 'mvp' ? 20 : 10;
    
    return Math.min(100, teamRisk + burnRisk + stageRisk);
  }

  private calculateMarketRisk(m: CompanyMetrics): number {
    // Market maturity, competition, timing
    let risk = 0;
    
    // Too early (market not ready)
    if (m.marketGrowth > 100) risk += 20;
    
    // Too late (market saturated)
    if (m.competitorCount > 100) risk += 30;
    if (m.marketGrowth < 10) risk += 20;
    
    // High competition
    if (m.competitorCount > 50) risk += 20;
    
    // Low differentiation (proxy via churn)
    if (m.churn > 10) risk += 10;
    
    return Math.min(100, risk);
  }

  /**
   * Opportunity Metrics
   */
  private calculateExpansionPotential(m: CompanyMetrics): number {
    // Market size - current capture
    const untappedMarket = Math.max(0, 100 - (m.marketShare * 100));
    const growthBonus = m.marketGrowth > 30 ? 20 : 10;
    const economicsBonus = m.ltv / m.cac > 3 ? 20 : 0;
    
    return Math.min(100, untappedMarket * 0.6 + growthBonus + economicsBonus);
  }

  private calculateImprovementHeadroom(m: CompanyMetrics, benchmarks: IndustryBenchmarks): number {
    // How much room for improvement vs benchmarks
    let headroom = 0;
    
    // Efficiency improvement potential
    if (m.burn / m.revenue > benchmarks.medianBurnMultiple) {
      headroom += 25;
    }
    
    // Churn improvement potential
    if (m.churn > benchmarks.medianChurn) {
      headroom += 25;
    }
    
    // Unit economics improvement
    if (m.ltv / m.cac < benchmarks.goodLtvCacRatio) {
      headroom += 25;
    }
    
    // Growth improvement
    if (m.marketGrowth < benchmarks.healthyGrowthRate) {
      headroom += 25;
    }
    
    return headroom;
  }

  private calculateMarketTimingScore(m: CompanyMetrics): number {
    // Goldilocks zone: not too early, not too late
    let score = 0;
    
    // Good growth rate (not too hot, not too cold)
    if (m.marketGrowth >= 20 && m.marketGrowth <= 50) score += 40;
    else if (m.marketGrowth >= 15 && m.marketGrowth <= 70) score += 20;
    
    // Moderate competition (market validated but not saturated)
    if (m.competitorCount >= 5 && m.competitorCount <= 30) score += 40;
    else if (m.competitorCount >= 3 && m.competitorCount <= 50) score += 20;
    
    // Good market share opportunity
    if (m.marketShare < 0.1 && m.marketShare > 0.001) score += 20;
    
    return score;
  }

  /**
   * Calculate composite scores based on all metrics
   */
  calculateCompositeScores(derived: DerivedMetrics): DerivedMetrics {
    // Overall Strength: Weighted combination of key metrics
    derived.overallStrength = (
      derived.marketPositionStrength * 0.25 +
      derived.defensibilityScore * 0.20 +
      derived.scalabilityIndex * 0.20 +
      (100 - derived.executionRisk) * 0.15 +
      derived.strategicMomentum * 0.20
    );
    
    // Strategic Readiness: Ready for next stage?
    derived.strategicReadiness = (
      (100 - derived.runwayRisk) * 0.30 +
      derived.marketTimingScore * 0.25 +
      derived.velocityScore * 0.25 +
      (100 - derived.executionRisk) * 0.20
    );
    
    // Investability Score: VC attractiveness
    derived.investabilityScore = (
      derived.scalabilityIndex * 0.30 +
      derived.marketCapturePotential * 0.25 +
      derived.defensibilityScore * 0.20 +
      (100 - derived.marketRisk) * 0.15 +
      derived.expansionPotential * 0.10
    );
    
    return derived;
  }

  /**
   * Generate strategic insights from derived metrics
   */
  generateMetricInsights(metrics: CompanyMetrics, derived: DerivedMetrics): string[] {
    const insights: string[] = [];
    
    // Efficiency insights
    if (derived.burnMultiple > 3) {
      insights.push(`Burn multiple of ${derived.burnMultiple.toFixed(1)}x indicates need for efficiency improvements`);
    } else if (derived.burnMultiple < 1.5) {
      insights.push(`Excellent burn multiple of ${derived.burnMultiple.toFixed(1)}x shows strong capital efficiency`);
    }
    
    // Growth insights
    if (derived.growthEfficiency > 70) {
      insights.push('High growth efficiency suggests effective go-to-market engine');
    }
    
    // Risk insights
    if (derived.runwayRisk > 60) {
      insights.push(`Critical: Only ${metrics.runway} months runway requires immediate action`);
    }
    
    // Opportunity insights
    if (derived.expansionPotential > 80) {
      insights.push(`Massive expansion potential with ${(100 - metrics.marketShare * 100).toFixed(1)}% of market untapped`);
    }
    
    // Strategic position insights
    if (derived.defensibilityScore > 70 && derived.marketPositionStrength > 60) {
      insights.push('Strong competitive moat and market position enable aggressive growth strategy');
    } else if (derived.defensibilityScore < 40) {
      insights.push('Low defensibility requires building stronger competitive advantages');
    }
    
    // Timing insights
    if (derived.marketTimingScore > 80) {
      insights.push('Optimal market timing window - accelerate to capture opportunity');
    }
    
    return insights;
  }
}

// Export singleton instance
export const dynamicScoring = new DynamicScoringSystem();