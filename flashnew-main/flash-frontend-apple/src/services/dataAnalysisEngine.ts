// Data-Driven Framework Analysis Engine
// Generates specific, quantified insights based on actual startup data

import { AssessmentData } from '../types/assessment';

export interface QuantifiedInsight {
  metric: string;
  currentValue: number;
  benchmark: number;
  gap: number;
  percentile?: number;
  trend?: 'improving' | 'stable' | 'declining';
  impact: 'critical' | 'high' | 'medium' | 'low';
}

export interface DataDrivenRecommendation {
  action: string;
  specificTarget: string;
  currentState: string;
  expectedImpact: string;
  timeframe: string;
  requiredInvestment?: number;
  roi?: number;
  confidenceLevel: number;
}

export interface FrameworkAnalysisResult {
  frameworkId: string;
  frameworkName: string;
  position: string;
  quantifiedPosition: {
    xValue: number;
    yValue: number;
    percentile?: number;
    quadrant?: string;
  };
  metrics: Record<string, any>;
  insights: string[];
  recommendations: DataDrivenRecommendation[];
  visualizationData: any;
}

// Industry benchmarks for different metrics
const INDUSTRY_BENCHMARKS = {
  seed: {
    burnMultiple: 0.5,
    runwayMonths: 18,
    monthlyGrowthRate: 15,
    grossMargin: 70,
    ltvCacRatio: 3,
    customerChurnRate: 5,
    marketShareGrowth: 2,
  },
  seriesA: {
    burnMultiple: 0.7,
    runwayMonths: 24,
    monthlyGrowthRate: 10,
    grossMargin: 75,
    ltvCacRatio: 3.5,
    customerChurnRate: 3,
    marketShareGrowth: 1.5,
  },
  seriesB: {
    burnMultiple: 0.8,
    runwayMonths: 36,
    monthlyGrowthRate: 7,
    grossMargin: 80,
    ltvCacRatio: 4,
    customerChurnRate: 2,
    marketShareGrowth: 1,
  }
};

export class DataAnalysisEngine {
  private assessmentData: AssessmentData;
  
  constructor(assessmentData: AssessmentData) {
    this.assessmentData = assessmentData;
  }

  // BCG Matrix Analysis with actual calculations
  analyzeBCGMatrix(): FrameworkAnalysisResult {
    const revenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const marketSize = Number(this.assessmentData.market?.tam) || 1;
    const marketGrowth = Number(this.assessmentData.market?.marketGrowthRate) || 0;
    const competitors = Number(this.assessmentData.market?.competitorCount) || 5;
    
    // Calculate actual relative market share
    const estimatedMarketShare = revenue / (marketSize * 0.01); // Assuming 1% of TAM is current market
    const avgCompetitorShare = (100 - estimatedMarketShare) / competitors;
    const relativeMarketShare = estimatedMarketShare / avgCompetitorShare;
    
    // Determine position with specific thresholds
    let quadrant = '';
    if (marketGrowth > 20 && relativeMarketShare > 1) {
      quadrant = 'Star';
    } else if (marketGrowth > 20 && relativeMarketShare <= 1) {
      quadrant = 'Question Mark';
    } else if (marketGrowth <= 20 && relativeMarketShare > 1) {
      quadrant = 'Cash Cow';
    } else {
      quadrant = 'Dog';
    }
    
    // Generate specific insights
    const insights: string[] = [];
    
    if (quadrant === 'Question Mark') {
      const shareNeeded = avgCompetitorShare - estimatedMarketShare;
      const revenueNeeded = shareNeeded * marketSize * 0.01;
      insights.push(`Need to capture additional ${shareNeeded.toFixed(1)}% market share (${this.formatCurrency(revenueNeeded)} in revenue) to become market leader`);
      
      const currentCAC = Number(this.assessmentData.market?.customerAcquisitionCost) || 100;
      const customersNeeded = revenueNeeded / (revenue / (Number(this.assessmentData.market?.customerCount) || 1));
      const investmentNeeded = customersNeeded * currentCAC;
      insights.push(`Requires ${this.formatCurrency(investmentNeeded)} investment in customer acquisition based on current CAC of ${this.formatCurrency(currentCAC)}`);
    }
    
    if (marketGrowth > 30) {
      insights.push(`Market growing at ${marketGrowth}% annually - ${(marketGrowth / 15).toFixed(1)}x faster than typical SaaS markets`);
    }
    
    // Generate data-driven recommendations
    const recommendations: DataDrivenRecommendation[] = [];
    
    if (quadrant === 'Question Mark') {
      const currentBurn = Number(this.assessmentData.capital?.monthlyBurn) || 0;
      const currentGrowth = Number(this.assessmentData.market?.userGrowthRate) || 0;
      const targetGrowth = marketGrowth * 1.5; // Need to grow faster than market
      
      recommendations.push({
        action: 'Accelerate customer acquisition',
        specificTarget: `Increase monthly growth rate from ${currentGrowth}% to ${targetGrowth.toFixed(1)}%`,
        currentState: `Current burn: ${this.formatCurrency(currentBurn)}/month achieving ${currentGrowth}% growth`,
        expectedImpact: `Achieve market leadership within ${Math.ceil(12 / (targetGrowth / 100))} months`,
        timeframe: '3-6 months',
        requiredInvestment: currentBurn * 2 * 6, // Double burn for 6 months
        roi: 3.5,
        confidenceLevel: 75
      });
    }
    
    return {
      frameworkId: 'bcg_matrix',
      frameworkName: 'BCG Growth-Share Matrix',
      position: quadrant,
      quantifiedPosition: {
        xValue: relativeMarketShare,
        yValue: marketGrowth,
        percentile: this.calculatePercentile('marketShare', estimatedMarketShare),
        quadrant
      },
      metrics: {
        relativeMarketShare: relativeMarketShare.toFixed(2),
        absoluteMarketShare: estimatedMarketShare.toFixed(2),
        marketGrowthRate: marketGrowth,
        currentRevenue: revenue,
        marketSize: marketSize
      },
      insights,
      recommendations,
      visualizationData: {
        x: relativeMarketShare,
        y: marketGrowth,
        quadrant,
        competitorPositions: this.generateCompetitorPositions(competitors, marketGrowth)
      }
    };
  }

  // Porter's Five Forces with quantified analysis
  analyzePortersFiveForces(): FrameworkAnalysisResult {
    const competitorCount = Number(this.assessmentData.market?.competitorCount) || 5;
    const marketGrowth = Number(this.assessmentData.market?.marketGrowthRate) || 15;
    const switchingCosts = Number(this.assessmentData.advantage?.switchingCosts) || 3;
    const customerConcentration = Number(this.assessmentData.market?.customerConcentration) || 20;
    const hasPatents = Number(this.assessmentData.advantage?.patentCount) > 0;
    const brandStrength = Number(this.assessmentData.advantage?.brandStrength) || 3;
    
    // Calculate force intensities based on actual data
    const forces = {
      competitive_rivalry: {
        score: this.calculateCompetitiveRivalry(competitorCount, marketGrowth),
        level: '',
        factors: []
      },
      buyer_power: {
        score: this.calculateBuyerPower(customerConcentration, switchingCosts),
        level: '',
        factors: []
      },
      supplier_power: {
        score: 0.3, // Low for most tech startups
        level: 'Low',
        factors: ['Multiple cloud providers', 'Open source alternatives']
      },
      threat_of_substitution: {
        score: this.calculateSubstitutionThreat(switchingCosts, brandStrength),
        level: '',
        factors: []
      },
      threat_of_new_entry: {
        score: this.calculateEntryThreat(hasPatents, marketGrowth),
        level: '',
        factors: []
      }
    };
    
    // Set levels based on scores
    Object.keys(forces).forEach(force => {
      const score = forces[force].score;
      forces[force].level = score > 0.7 ? 'High' : score > 0.4 ? 'Medium' : 'Low';
    });
    
    // Calculate specific factors
    if (competitorCount > 10) {
      forces.competitive_rivalry.factors.push(`${competitorCount} direct competitors - ${(competitorCount / 5).toFixed(1)}x industry average`);
    }
    
    if (customerConcentration > 30) {
      forces.buyer_power.factors.push(`Top 20% of customers represent ${customerConcentration}% of revenue - high concentration risk`);
    }
    
    // Generate quantified insights
    const insights: string[] = [];
    const overallAttractiveness = 1 - (Object.values(forces).reduce((sum, f) => sum + f.score, 0) / 5);
    
    insights.push(`Industry attractiveness score: ${(overallAttractiveness * 100).toFixed(0)}% (${overallAttractiveness > 0.6 ? 'Attractive' : overallAttractiveness > 0.4 ? 'Moderate' : 'Challenging'})`);
    
    if (forces.competitive_rivalry.score > 0.7) {
      const marketSharePerCompetitor = 100 / (competitorCount + 1);
      insights.push(`Average market share per competitor: ${marketSharePerCompetitor.toFixed(1)}% - fragmented market requiring differentiation`);
    }
    
    // Data-driven recommendations
    const recommendations: DataDrivenRecommendation[] = [];
    
    if (forces.buyer_power.score > 0.6) {
      const currentLTV = Number(this.assessmentData.market?.lifetimeValue) || 1000;
      const targetConcentration = 20;
      
      recommendations.push({
        action: 'Reduce customer concentration risk',
        specificTarget: `Reduce top 20% revenue concentration from ${customerConcentration}% to ${targetConcentration}%`,
        currentState: `Current largest customer represents ${(customerConcentration / 5).toFixed(1)}% of revenue`,
        expectedImpact: `Reduce revenue volatility by ${((customerConcentration - targetConcentration) / 2).toFixed(0)}%`,
        timeframe: '6-12 months',
        confidenceLevel: 80
      });
    }
    
    return {
      frameworkId: 'porters_five_forces',
      frameworkName: "Porter's Five Forces",
      position: `${overallAttractiveness > 0.6 ? 'Attractive' : overallAttractiveness > 0.4 ? 'Moderately Attractive' : 'Challenging'} Industry`,
      quantifiedPosition: {
        xValue: overallAttractiveness,
        yValue: 0,
        percentile: this.calculatePercentile('industryAttractiveness', overallAttractiveness * 100)
      },
      metrics: forces,
      insights,
      recommendations,
      visualizationData: forces
    };
  }

  // SWOT Analysis with quantified elements
  analyzeSWOT(): FrameworkAnalysisResult {
    const strengths: string[] = [];
    const weaknesses: string[] = [];
    const opportunities: string[] = [];
    const threats: string[] = [];
    
    // Analyze strengths with specific metrics
    const patentCount = Number(this.assessmentData.advantage?.patentCount) || 0;
    if (patentCount > 0) {
      strengths.push(`${patentCount} patents filed - potential licensing revenue of ${this.formatCurrency(patentCount * 50000)} annually`);
    }
    
    const techScore = Number(this.assessmentData.advantage?.techDifferentiation) || 3;
    if (techScore >= 4) {
      strengths.push(`Technical differentiation score ${techScore}/5 - top ${100 - this.calculatePercentile('techDifferentiation', techScore)}% of startups`);
    }
    
    const teamSize = Number(this.assessmentData.people?.teamSize) || 1;
    const avgExperience = Number(this.assessmentData.people?.avgExperience) || 0;
    if (avgExperience > 10) {
      strengths.push(`Team average ${avgExperience} years experience - ${(avgExperience / 5).toFixed(1)}x industry average for seed stage`);
    }
    
    // Analyze weaknesses with specific gaps
    const runway = Number(this.assessmentData.capital?.runwayMonths) || 0;
    const benchmarkRunway = INDUSTRY_BENCHMARKS[this.assessmentData.capital?.fundingStage || 'seed'].runwayMonths;
    if (runway < benchmarkRunway) {
      weaknesses.push(`${runway} months runway - ${benchmarkRunway - runway} months below recommended for ${this.assessmentData.capital?.fundingStage || 'seed'} stage`);
    }
    
    const burnMultiple = Number(this.assessmentData.capital?.burnMultiple) || 0;
    if (burnMultiple > 1) {
      const excessBurn = (burnMultiple - 0.7) * Number(this.assessmentData.capital?.monthlyBurn);
      weaknesses.push(`Burn multiple of ${burnMultiple.toFixed(1)} - spending ${this.formatCurrency(excessBurn)} monthly above efficient levels`);
    }
    
    // Analyze opportunities with market data
    const marketGrowth = Number(this.assessmentData.market?.marketGrowthRate) || 0;
    const tam = Number(this.assessmentData.market?.tam) || 0;
    if (marketGrowth > 25) {
      const marketIn3Years = tam * Math.pow(1 + marketGrowth / 100, 3);
      opportunities.push(`Market growing ${marketGrowth}% annually - TAM expanding from ${this.formatCurrency(tam)} to ${this.formatCurrency(marketIn3Years)} in 3 years`);
    }
    
    // Analyze threats with quantification
    const competitorCount = Number(this.assessmentData.market?.competitorCount) || 0;
    if (competitorCount > 10) {
      threats.push(`${competitorCount} competitors identified - top 3 control ${(competitorCount > 20 ? 60 : 40)}% of market`);
    }
    
    const cashOnHand = Number(this.assessmentData.capital?.cashOnHand) || 0;
    const monthlyBurn = Number(this.assessmentData.capital?.monthlyBurn) || 1;
    if (runway < 6) {
      const fundingNeeded = monthlyBurn * 18 - cashOnHand;
      threats.push(`Need to raise ${this.formatCurrency(fundingNeeded)} within ${runway} months to maintain operations`);
    }
    
    // Generate strategic recommendations
    const recommendations: DataDrivenRecommendation[] = [];
    
    // SO Strategy (Strengths + Opportunities)
    if (strengths.length > 0 && opportunities.length > 0) {
      recommendations.push({
        action: 'Leverage technical advantages for market expansion',
        specificTarget: `Capture ${(1 / (competitorCount + 1) * 2).toFixed(1)}% market share in growing ${marketGrowth}% market`,
        currentState: `Strong tech differentiation (${techScore}/5) in expanding market`,
        expectedImpact: `${this.formatCurrency(tam * 0.01 * (1 / (competitorCount + 1) * 2))} additional revenue`,
        timeframe: '12-18 months',
        roi: 4.2,
        confidenceLevel: 70
      });
    }
    
    return {
      frameworkId: 'swot_analysis',
      frameworkName: 'SWOT Analysis',
      position: this.calculateSWOTPosition(strengths.length, weaknesses.length, opportunities.length, threats.length),
      quantifiedPosition: {
        xValue: (strengths.length - weaknesses.length) / 5,
        yValue: (opportunities.length - threats.length) / 5
      },
      metrics: {
        strengthCount: strengths.length,
        weaknessCount: weaknesses.length,
        opportunityCount: opportunities.length,
        threatCount: threats.length,
        netPosition: (strengths.length + opportunities.length) - (weaknesses.length + threats.length)
      },
      insights: [
        ...strengths.slice(0, 2).map(s => `Strength: ${s}`),
        ...weaknesses.slice(0, 2).map(w => `Weakness: ${w}`),
        ...opportunities.slice(0, 2).map(o => `Opportunity: ${o}`),
        ...threats.slice(0, 2).map(t => `Threat: ${t}`)
      ],
      recommendations,
      visualizationData: {
        strengths,
        weaknesses,
        opportunities,
        threats
      }
    };
  }

  // Helper methods
  private calculateCompetitiveRivalry(competitorCount: number, marketGrowth: number): number {
    const competitorScore = Math.min(competitorCount / 20, 1); // Normalize to 0-1
    const growthScore = 1 - Math.min(marketGrowth / 50, 1); // Higher growth = lower rivalry
    return (competitorScore * 0.7 + growthScore * 0.3);
  }

  private calculateBuyerPower(customerConcentration: number, switchingCosts: number): number {
    const concentrationScore = customerConcentration / 100;
    const switchingScore = 1 - (switchingCosts - 1) / 4; // 1-5 scale inverted
    return (concentrationScore * 0.6 + switchingScore * 0.4);
  }

  private calculateSubstitutionThreat(switchingCosts: number, brandStrength: number): number {
    const switchingScore = 1 - (switchingCosts - 1) / 4;
    const brandScore = 1 - (brandStrength - 1) / 4;
    return (switchingScore * 0.5 + brandScore * 0.5);
  }

  private calculateEntryThreat(hasPatents: boolean, marketGrowth: number): number {
    const patentScore = hasPatents ? 0.3 : 0.7;
    const growthScore = Math.min(marketGrowth / 50, 1); // High growth attracts entrants
    return (patentScore * 0.4 + growthScore * 0.6);
  }

  private calculatePercentile(metric: string, value: number): number {
    // Simplified percentile calculation - in production, use actual distribution data
    const percentiles = {
      marketShare: { 50: 0.1, 75: 0.5, 90: 2, 95: 5 },
      techDifferentiation: { 50: 3, 75: 4, 90: 4.5, 95: 5 },
      industryAttractiveness: { 50: 50, 75: 65, 90: 75, 95: 85 }
    };
    
    const distribution = percentiles[metric] || percentiles.marketShare;
    
    if (value <= distribution[50]) return 50 - (distribution[50] - value) * 25 / distribution[50];
    if (value <= distribution[75]) return 50 + (value - distribution[50]) * 25 / (distribution[75] - distribution[50]);
    if (value <= distribution[90]) return 75 + (value - distribution[75]) * 15 / (distribution[90] - distribution[75]);
    if (value <= distribution[95]) return 90 + (value - distribution[90]) * 5 / (distribution[95] - distribution[90]);
    return 95;
  }

  private calculateSWOTPosition(s: number, w: number, o: number, t: number): string {
    const internal = s - w;
    const external = o - t;
    
    if (internal > 0 && external > 0) return "Strong Position - Aggressive Growth";
    if (internal > 0 && external <= 0) return "Defensive Position - Protect Strengths";
    if (internal <= 0 && external > 0) return "Turnaround Position - Fix Weaknesses";
    return "Survival Position - Major Changes Needed";
  }

  private generateCompetitorPositions(count: number, marketGrowth: number): any[] {
    // Generate realistic competitor positions for visualization
    const positions = [];
    for (let i = 0; i < Math.min(count, 5); i++) {
      positions.push({
        name: `Competitor ${i + 1}`,
        x: Math.random() * 2 + 0.1, // 0.1 to 2.1 relative market share
        y: marketGrowth + (Math.random() - 0.5) * 10, // +/- 5% from market growth
        size: Math.random() * 100 + 50 // Revenue proxy
      });
    }
    return positions;
  }

  private formatCurrency(value: number): string {
    if (value >= 1000000000) return `$${(value / 1000000000).toFixed(1)}B`;
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`;
    return `$${value.toFixed(0)}`;
  }

  // Ansoff Matrix Analysis
  analyzeAnsoffMatrix(): FrameworkAnalysisResult {
    const currentRevenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const customerCount = Number(this.assessmentData.market?.customerCount) || 0;
    const marketGrowth = Number(this.assessmentData.market?.marketGrowthRate) || 15;
    const productStage = this.assessmentData.advantage?.productStage || 'mvp';
    const tam = Number(this.assessmentData.market?.tam) || 0;
    const sam = Number(this.assessmentData.market?.sam) || 0;
    
    // Calculate growth potential for each strategy
    const strategies = {
      market_penetration: {
        potential: this.calculateMarketPenetrationPotential(),
        risk: 'Low',
        investment: currentRevenue * 0.2,
        timeframe: '6-12 months'
      },
      market_development: {
        potential: this.calculateMarketDevelopmentPotential(),
        risk: 'Medium',
        investment: currentRevenue * 0.5,
        timeframe: '12-18 months'
      },
      product_development: {
        potential: this.calculateProductDevelopmentPotential(),
        risk: 'Medium',
        investment: currentRevenue * 0.4,
        timeframe: '9-15 months'
      },
      diversification: {
        potential: tam * 0.001, // 0.1% of TAM for new market/product
        risk: 'High',
        investment: currentRevenue * 1.0,
        timeframe: '18-24 months'
      }
    };
    
    // Determine recommended strategy
    const recommendedStrategy = this.selectAnsoffStrategy(strategies);
    
    const insights: string[] = [];
    const avgRevPerCustomer = customerCount > 0 ? currentRevenue / customerCount : 1000;
    
    insights.push(`Current market penetration: ${((currentRevenue / sam) * 100).toFixed(2)}% of SAM`);
    insights.push(`Average revenue per customer: ${this.formatCurrency(avgRevPerCustomer)}`);
    
    const recommendations: DataDrivenRecommendation[] = [];
    
    if (recommendedStrategy === 'market_penetration') {
      const currentMarketShare = (currentRevenue / sam) * 100;
      const targetMarketShare = Math.min(currentMarketShare * 2, 10);
      const additionalRevenue = (targetMarketShare - currentMarketShare) / 100 * sam;
      
      recommendations.push({
        action: 'Focus on market penetration',
        specificTarget: `Increase market share from ${currentMarketShare.toFixed(1)}% to ${targetMarketShare.toFixed(1)}%`,
        currentState: `${customerCount} customers generating ${this.formatCurrency(currentRevenue)} ARR`,
        expectedImpact: `Additional ${this.formatCurrency(additionalRevenue)} in revenue`,
        timeframe: '6-12 months',
        requiredInvestment: strategies.market_penetration.investment,
        roi: additionalRevenue / strategies.market_penetration.investment,
        confidenceLevel: 85
      });
    }
    
    return {
      frameworkId: 'ansoff_matrix',
      frameworkName: 'Ansoff Growth Matrix',
      position: recommendedStrategy.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      quantifiedPosition: {
        xValue: productStage === 'launched' ? 1 : 0,
        yValue: currentRevenue > 0 ? 1 : 0
      },
      metrics: strategies,
      insights,
      recommendations,
      visualizationData: {
        currentFocus: recommendedStrategy,
        strategies
      }
    };
  }

  private calculateMarketPenetrationPotential(): number {
    const currentRevenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const sam = Number(this.assessmentData.market?.sam) || currentRevenue * 100;
    const currentPenetration = currentRevenue / sam;
    const maxRealisticPenetration = 0.1; // 10% of SAM
    
    return (maxRealisticPenetration - currentPenetration) * sam;
  }

  private calculateMarketDevelopmentPotential(): number {
    const currentRevenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const tam = Number(this.assessmentData.market?.tam) || 0;
    const sam = Number(this.assessmentData.market?.sam) || 0;
    const untappedMarket = tam - sam;
    
    return untappedMarket * 0.01; // 1% of untapped market
  }

  private calculateProductDevelopmentPotential(): number {
    const currentRevenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const customerCount = Number(this.assessmentData.market?.customerCount) || 1;
    const avgRevPerCustomer = currentRevenue / customerCount;
    
    // Assume 50% revenue increase per customer with new products
    return currentRevenue * 0.5;
  }

  private selectAnsoffStrategy(strategies: any): string {
    // Select strategy based on risk-adjusted returns
    let bestStrategy = 'market_penetration';
    let bestScore = 0;
    
    const riskMultipliers = { Low: 1, Medium: 0.7, High: 0.4 };
    
    Object.entries(strategies).forEach(([strategy, data]: [string, any]) => {
      const score = data.potential * riskMultipliers[data.risk] / data.investment;
      if (score > bestScore) {
        bestScore = score;
        bestStrategy = strategy;
      }
    });
    
    return bestStrategy;
  }

  // Blue Ocean Strategy Analysis
  analyzeBlueOcean(): FrameworkAnalysisResult {
    const competitorCount = Number(this.assessmentData.market?.competitorCount) || 5;
    const techDifferentiation = Number(this.assessmentData.advantage?.techDifferentiation) || 3;
    const brandStrength = Number(this.assessmentData.advantage?.brandStrength) || 3;
    const currentCAC = Number(this.assessmentData.market?.customerAcquisitionCost) || 100;
    const currentLTV = Number(this.assessmentData.market?.lifetimeValue) || 300;
    
    // Analyze current competitive factors
    const competitiveFactors = {
      price: { current: 5, industry: 5, target: 3 },
      features: { current: techDifferentiation, industry: 3, target: 5 },
      quality: { current: 4, industry: 4, target: 5 },
      service: { current: brandStrength, industry: 3, target: 5 },
      speed: { current: 4, industry: 3, target: 5 },
      customization: { current: 3, industry: 2, target: 4 }
    };
    
    // Calculate blue ocean opportunity score
    let differentiationScore = 0;
    let costReductionScore = 0;
    
    Object.values(competitiveFactors).forEach(factor => {
      if (factor.current > factor.industry) {
        differentiationScore += (factor.current - factor.industry);
      }
      if (factor.target < factor.current) {
        costReductionScore += (factor.current - factor.target);
      }
    });
    
    const blueOceanScore = (differentiationScore * 0.7 + costReductionScore * 0.3) / 6 * 100;
    
    const insights: string[] = [];
    insights.push(`Current differentiation score: ${differentiationScore}/18 - ${differentiationScore > 9 ? 'Strong' : 'Moderate'} differentiation`);
    insights.push(`Cost reduction potential: ${(costReductionScore / 18 * 100).toFixed(0)}% across value chain`);
    
    if (competitorCount > 10) {
      insights.push(`High competition (${competitorCount} players) makes blue ocean strategy valuable`);
    }
    
    const recommendations: DataDrivenRecommendation[] = [];
    
    // Calculate specific value innovation opportunities
    const featureGap = competitiveFactors.features.target - competitiveFactors.features.current;
    if (featureGap > 0) {
      const additionalLTV = currentLTV * 0.3; // 30% LTV increase from better features
      const investmentNeeded = Number(this.assessmentData.capital?.monthlyBurn) * 3; // 3 months of development
      
      recommendations.push({
        action: 'Create uncontested market space through value innovation',
        specificTarget: `Increase feature differentiation from ${competitiveFactors.features.current}/5 to ${competitiveFactors.features.target}/5`,
        currentState: `Current LTV ${this.formatCurrency(currentLTV)}, CAC ${this.formatCurrency(currentCAC)}`,
        expectedImpact: `Increase LTV by ${this.formatCurrency(additionalLTV)} while reducing CAC by 20%`,
        timeframe: '6-9 months',
        requiredInvestment: investmentNeeded,
        roi: (additionalLTV * Number(this.assessmentData.market?.customerCount)) / investmentNeeded,
        confidenceLevel: 70
      });
    }
    
    return {
      frameworkId: 'blue_ocean',
      frameworkName: 'Blue Ocean Strategy',
      position: blueOceanScore > 70 ? 'Blue Ocean Creator' : blueOceanScore > 40 ? 'Purple Ocean' : 'Red Ocean',
      quantifiedPosition: {
        xValue: differentiationScore,
        yValue: costReductionScore,
        percentile: this.calculatePercentile('blueOcean', blueOceanScore)
      },
      metrics: {
        competitiveFactors,
        blueOceanScore,
        differentiationScore,
        costReductionScore
      },
      insights,
      recommendations,
      visualizationData: {
        strategyCanvas: competitiveFactors,
        fourActions: {
          eliminate: ['Complex pricing tiers', 'Legacy features'],
          reduce: ['Customer support costs', 'Feature complexity'],
          raise: ['User experience', 'Integration capabilities'],
          create: ['AI-powered insights', 'Predictive analytics']
        }
      }
    };
  }

  // Value Chain Analysis
  analyzeValueChain(): FrameworkAnalysisResult {
    const revenue = Number(this.assessmentData.capital?.annualRevenueRunRate) || 0;
    const monthlyBurn = Number(this.assessmentData.capital?.monthlyBurn) || 0;
    const teamSize = Number(this.assessmentData.people?.teamSize) || 1;
    const grossMargin = Number(this.assessmentData.market?.grossMargin) || 70;
    
    // Estimate cost allocation across value chain
    const annualCosts = monthlyBurn * 12;
    const costPerEmployee = annualCosts / teamSize;
    
    const primaryActivities = {
      inbound_logistics: { 
        cost: annualCosts * 0.05, 
        value: revenue * 0.02,
        efficiency: 0
      },
      operations: { 
        cost: annualCosts * 0.25, 
        value: revenue * 0.35,
        efficiency: 0
      },
      outbound_logistics: { 
        cost: annualCosts * 0.05, 
        value: revenue * 0.02,
        efficiency: 0
      },
      marketing_sales: { 
        cost: annualCosts * 0.35, 
        value: revenue * 0.40,
        efficiency: 0
      },
      service: { 
        cost: annualCosts * 0.10, 
        value: revenue * 0.21,
        efficiency: 0
      }
    };
    
    const supportActivities = {
      infrastructure: { cost: annualCosts * 0.08, value: revenue * 0.05 },
      hr_management: { cost: annualCosts * 0.05, value: revenue * 0.03 },
      technology: { cost: annualCosts * 0.05, value: revenue * 0.08 },
      procurement: { cost: annualCosts * 0.02, value: revenue * 0.01 }
    };
    
    // Calculate efficiency for each activity
    Object.keys(primaryActivities).forEach(activity => {
      const act = primaryActivities[activity];
      act.efficiency = act.cost > 0 ? (act.value - act.cost) / act.cost : 0;
    });
    
    // Find bottlenecks and opportunities
    const insights: string[] = [];
    const worstPerformer = Object.entries(primaryActivities)
      .sort((a, b) => a[1].efficiency - b[1].efficiency)[0];
    
    insights.push(`${worstPerformer[0].replace('_', ' ')} has lowest efficiency at ${(worstPerformer[1].efficiency * 100).toFixed(0)}% ROI`);
    
    const marketingSalesEfficiency = primaryActivities.marketing_sales.efficiency;
    if (marketingSalesEfficiency < 1) {
      const currentCAC = Number(this.assessmentData.market?.customerAcquisitionCost) || 100;
      const targetCAC = currentCAC * 0.7;
      insights.push(`Marketing efficiency ${(marketingSalesEfficiency * 100).toFixed(0)}% - reduce CAC from ${this.formatCurrency(currentCAC)} to ${this.formatCurrency(targetCAC)}`);
    }
    
    const recommendations: DataDrivenRecommendation[] = [];
    
    // Specific value chain optimization
    const totalValueCreated = Object.values(primaryActivities).reduce((sum, act) => sum + act.value, 0);
    const totalCosts = annualCosts;
    const currentMargin = (totalValueCreated - totalCosts) / totalValueCreated * 100;
    
    recommendations.push({
      action: 'Optimize value chain for margin expansion',
      specificTarget: `Increase operating margin from ${currentMargin.toFixed(1)}% to ${(currentMargin + 10).toFixed(1)}%`,
      currentState: `Current: ${this.formatCurrency(totalValueCreated)} value, ${this.formatCurrency(totalCosts)} costs`,
      expectedImpact: `Additional ${this.formatCurrency(totalValueCreated * 0.1)} in annual profit`,
      timeframe: '6-12 months',
      requiredInvestment: monthlyBurn * 2,
      roi: (totalValueCreated * 0.1) / (monthlyBurn * 2),
      confidenceLevel: 75
    });
    
    return {
      frameworkId: 'value_chain',
      frameworkName: 'Value Chain Analysis',
      position: currentMargin > 20 ? 'Efficient' : currentMargin > 0 ? 'Developing' : 'Inefficient',
      quantifiedPosition: {
        xValue: currentMargin,
        yValue: grossMargin
      },
      metrics: {
        primaryActivities,
        supportActivities,
        totalValueCreated,
        totalCosts,
        operatingMargin: currentMargin
      },
      insights,
      recommendations,
      visualizationData: {
        activities: { ...primaryActivities, ...supportActivities },
        marginWaterfall: this.generateMarginWaterfall(primaryActivities, supportActivities)
      }
    };
  }

  private generateMarginWaterfall(primary: any, support: any): any[] {
    const waterfall = [];
    let runningTotal = 0;
    
    // Add revenue
    const revenue = Object.values(primary).reduce((sum: number, act: any) => sum + act.value, 0);
    waterfall.push({ name: 'Revenue', value: revenue, total: revenue });
    runningTotal = revenue;
    
    // Subtract costs
    Object.entries(primary).forEach(([name, data]: [string, any]) => {
      runningTotal -= data.cost;
      waterfall.push({ 
        name: name.replace('_', ' '), 
        value: -data.cost, 
        total: runningTotal 
      });
    });
    
    Object.entries(support).forEach(([name, data]: [string, any]) => {
      runningTotal -= data.cost;
      waterfall.push({ 
        name: name.replace('_', ' '), 
        value: -data.cost, 
        total: runningTotal 
      });
    });
    
    return waterfall;
  }

  // Additional framework analyses can be added here...
}

// Export main analysis function
export function analyzeFrameworks(assessmentData: AssessmentData, frameworkIds: string[]): FrameworkAnalysisResult[] {
  const engine = new DataAnalysisEngine(assessmentData);
  const results: FrameworkAnalysisResult[] = [];
  
  const analysisMap = {
    'bcg_matrix': () => engine.analyzeBCGMatrix(),
    'porters_five_forces': () => engine.analyzePortersFiveForces(),
    'swot_analysis': () => engine.analyzeSWOT(),
    'ansoff_matrix': () => engine.analyzeAnsoffMatrix(),
    'blue_ocean': () => engine.analyzeBlueOcean(),
    'value_chain': () => engine.analyzeValueChain()
  };
  
  frameworkIds.forEach(id => {
    if (analysisMap[id]) {
      try {
        results.push(analysisMap[id]());
      } catch (error) {
        console.error(`Error analyzing ${id}:`, error);
      }
    }
  });
  
  return results;
}