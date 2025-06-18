// Framework Analysis Engine
// Maps FLASH startup data to framework positions with PhD-level rigor

import { EnrichedAnalysisData, StartupData } from '../types';

export interface FrameworkPosition {
  position: string;
  coordinates?: { x: number; y: number };
  score?: number;
  quadrant?: string;
  classification?: string;
  percentile?: number;
  confidence: number;
}

export interface FrameworkInsight {
  title: string;
  description: string;
  importance: 'critical' | 'high' | 'medium' | 'low';
  dataPoints: string[];
  recommendation: string;
  timeframe: 'immediate' | 'short-term' | 'medium-term' | 'long-term';
}

export interface FrameworkAnalysis {
  frameworkId: string;
  frameworkName: string;
  position: FrameworkPosition;
  insights: FrameworkInsight[];
  visualizationData: any;
  actions: ActionItem[];
  risks?: Risk[];
  opportunities?: Opportunity[];
}

export interface ActionItem {
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  effort: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  timeframe: string;
  metrics: string[];
}

export interface Risk {
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  likelihood: 'very-likely' | 'likely' | 'possible' | 'unlikely';
  mitigation: string;
}

export interface Opportunity {
  title: string;
  description: string;
  potential: 'transformative' | 'significant' | 'moderate' | 'incremental';
  feasibility: 'easy' | 'moderate' | 'difficult' | 'very-difficult';
  requirements: string[];
}

// Convert FLASH data to framework-compatible format
function convertFlashData(analysisData: EnrichedAnalysisData): {
  marketShare: number;
  marketGrowthRate: number;
  revenue: number;
  profitMargin: number;
  customerBase: number;
  growthRate: number;
  competitorCount: number;
  burnRate: number;
  teamSize: number;
  fundingRaised: number;
  productStage: string;
  differentiationLevel: number;
  nps: number;
  brandStrength: number;
} {
  const data = analysisData.startupData;
  
  // Extract metrics from FLASH data
  const marketShare = estimateMarketShare(data);
  const marketGrowthRate = data.market_growth_rate_percent || 10;
  const revenue = data.annual_revenue_run_rate || 0;
  const profitMargin = calculateProfitMargin(data);
  const customerBase = data.customer_count || 0;
  const growthRate = data.revenue_growth_rate_percent || 0;
  const competitorCount = data.competitors_named_count || 5;
  const burnRate = data.monthly_burn_usd || 50000;
  const teamSize = data.team_size_full_time || 10;
  const fundingRaised = data.total_capital_raised_usd || 0;
  const productStage = data.product_stage || 'mvp';
  const differentiationLevel = data.tech_differentiation_score || 5;
  const nps = estimateNPS(data);
  const brandStrength = data.brand_strength_score || 5;

  return {
    marketShare,
    marketGrowthRate,
    revenue,
    profitMargin,
    customerBase,
    growthRate,
    competitorCount,
    burnRate,
    teamSize,
    fundingRaised,
    productStage,
    differentiationLevel,
    nps,
    brandStrength
  };
}

function estimateMarketShare(data: StartupData): number {
  // Estimate market share based on revenue and SAM
  if (data.annual_revenue_run_rate && data.sam_size_usd) {
    return Math.min(100, (data.annual_revenue_run_rate / data.sam_size_usd) * 100);
  }
  // Default to low market share for early-stage
  return data.funding_stage === 'pre_seed' ? 0.1 : 
         data.funding_stage === 'seed' ? 0.5 : 
         data.funding_stage === 'series_a' ? 2 : 5;
}

function calculateProfitMargin(data: StartupData): number {
  // Calculate profit margin from gross margin and burn
  const grossMargin = data.gross_margin_percent || 50;
  const burnMultiple = data.burn_multiple || 2;
  
  // Estimate profit margin (can be negative)
  return grossMargin - (burnMultiple * 20); // Simplified calculation
}

function estimateNPS(data: StartupData): number {
  // Estimate NPS from retention metrics
  const retention30d = data.product_retention_30d || 50;
  const retention90d = data.product_retention_90d || 30;
  
  // Higher retention correlates with higher NPS
  if (retention30d > 80 && retention90d > 60) return 70;
  if (retention30d > 60 && retention90d > 40) return 40;
  if (retention30d > 40 && retention90d > 20) return 10;
  return -20;
}

// BCG Matrix Analysis
function analyzeBCGMatrix(data: ReturnType<typeof convertFlashData>): FrameworkAnalysis {
  const { marketShare, marketGrowthRate, revenue, profitMargin } = data;
  
  // Calculate position
  let position: string;
  let quadrant: string;
  const x = marketShare / 10; // Normalize to 0-1
  const y = marketGrowthRate / 30; // Normalize to 0-1
  
  if (marketShare > 5 && marketGrowthRate > 10) {
    position = 'Star';
    quadrant = 'High Growth, High Share';
  } else if (marketShare > 5 && marketGrowthRate <= 10) {
    position = 'Cash Cow';
    quadrant = 'Low Growth, High Share';
  } else if (marketShare <= 5 && marketGrowthRate > 10) {
    position = 'Question Mark';
    quadrant = 'High Growth, Low Share';
  } else {
    position = 'Dog';
    quadrant = 'Low Growth, Low Share';
  }

  const insights: FrameworkInsight[] = [];
  const actions: ActionItem[] = [];

  switch (position) {
    case 'Star':
      insights.push({
        title: 'Market Leader in Growth Segment',
        description: 'You\'re well-positioned in a high-growth market with strong market share.',
        importance: 'high',
        dataPoints: [
          `Market share: ${marketShare.toFixed(1)}%`,
          `Market growth: ${marketGrowthRate.toFixed(1)}% annually`,
          `Revenue: $${(revenue/1000000).toFixed(1)}M`
        ],
        recommendation: 'Invest heavily to maintain position and transition to Cash Cow as market matures.',
        timeframe: 'medium-term'
      });
      actions.push({
        title: 'Scale Operations Aggressively',
        description: 'Double down on growth to maintain market leadership',
        priority: 'critical',
        effort: 'high',
        impact: 'high',
        timeframe: '6-12 months',
        metrics: ['Market share', 'Customer acquisition', 'Revenue growth']
      });
      break;

    case 'Question Mark':
      insights.push({
        title: 'High Potential, Low Position',
        description: 'Operating in attractive market but need to capture more share quickly.',
        importance: 'critical',
        dataPoints: [
          `Market share: ${marketShare.toFixed(1)}%`,
          `Market growth: ${marketGrowthRate.toFixed(1)}% annually`,
          `Burn rate: $${(data.burnRate/1000).toFixed(0)}k/month`
        ],
        recommendation: 'Make strategic decision: invest heavily to become Star or divest.',
        timeframe: 'immediate'
      });
      actions.push({
        title: 'Aggressive Market Share Capture',
        description: 'Launch targeted campaigns to rapidly increase market share',
        priority: 'critical',
        effort: 'high',
        impact: 'high',
        timeframe: '3-6 months',
        metrics: ['Market share growth', 'CAC', 'Conversion rate']
      });
      break;

    case 'Cash Cow':
      insights.push({
        title: 'Profit Generator',
        description: 'Strong position in mature market generating steady cash flow.',
        importance: 'high',
        dataPoints: [
          `Profit margin: ${profitMargin.toFixed(1)}%`,
          `Market share: ${marketShare.toFixed(1)}%`,
          `Customer base: ${data.customerBase.toLocaleString()}`
        ],
        recommendation: 'Maximize profitability while investing surplus in new growth areas.',
        timeframe: 'short-term'
      });
      break;

    case 'Dog':
      insights.push({
        title: 'Strategic Reassessment Needed',
        description: 'Low share in low-growth market requires pivot or exit strategy.',
        importance: 'critical',
        dataPoints: [
          `Market share: ${marketShare.toFixed(1)}%`,
          `Market growth: ${marketGrowthRate.toFixed(1)}% annually`,
          `Burn rate: $${(data.burnRate/1000).toFixed(0)}k/month`
        ],
        recommendation: 'Consider pivoting to new market or orderly exit.',
        timeframe: 'immediate'
      });
      break;
  }

  return {
    frameworkId: 'bcg_matrix',
    frameworkName: 'BCG Growth-Share Matrix',
    position: {
      position,
      coordinates: { x, y },
      quadrant,
      confidence: 0.75
    },
    insights,
    visualizationData: {
      type: 'matrix_2x2',
      x,
      y,
      position,
      axes: {
        x: { label: 'Relative Market Share', min: 0, max: 10 },
        y: { label: 'Market Growth Rate', min: 0, max: 30 }
      }
    },
    actions
  };
}

// SWOT Analysis
function analyzeSWOT(data: ReturnType<typeof convertFlashData>): FrameworkAnalysis {
  const strengths: string[] = [];
  const weaknesses: string[] = [];
  const opportunities: string[] = [];
  const threats: string[] = [];

  // Identify strengths
  if (data.nps > 50) strengths.push('High customer satisfaction');
  if (data.growthRate > 50) strengths.push('Rapid revenue growth');
  if (data.differentiationLevel > 7) strengths.push('Strong technical differentiation');
  if (data.teamSize > 20) strengths.push('Substantial team resources');
  if (data.fundingRaised > 5000000) strengths.push('Well-funded operations');

  // Identify weaknesses
  if (data.burnRate > data.revenue * 0.5) weaknesses.push('High burn rate relative to revenue');
  if (data.marketShare < 2) weaknesses.push('Low market share');
  if (data.profitMargin < -50) weaknesses.push('Significant losses');
  if (data.customerBase < 100) weaknesses.push('Limited customer base');

  // Identify opportunities
  if (data.marketGrowthRate > 20) opportunities.push('Rapidly growing market');
  if (data.competitorCount < 5) opportunities.push('Limited direct competition');
  if (data.productStage === 'live' || data.productStage === 'scaling') {
    opportunities.push('Product ready for scale');
  }

  // Identify threats
  if (data.competitorCount > 10) threats.push('Intense competition');
  if (data.marketGrowthRate < 5) threats.push('Slow market growth');
  if (data.burnRate > data.fundingRaised / 12) threats.push('Limited runway');

  const swotScore = (strengths.length * 2 + opportunities.length * 1.5) - 
                    (weaknesses.length * 1.5 + threats.length * 2);
  const position = swotScore > 5 ? 'Strong Position' :
                   swotScore > 0 ? 'Balanced Position' : 'Vulnerable Position';

  const insights: FrameworkInsight[] = [
    {
      title: 'Strategic Position Assessment',
      description: `${strengths.length} key strengths vs ${weaknesses.length} weaknesses identified.`,
      importance: 'high',
      dataPoints: [
        `Top strength: ${strengths[0] || 'None identified'}`,
        `Critical weakness: ${weaknesses[0] || 'None identified'}`,
        `SWOT balance score: ${swotScore.toFixed(1)}`
      ],
      recommendation: 'Leverage strengths to capture opportunities while addressing critical weaknesses.',
      timeframe: 'medium-term'
    }
  ];

  const actions: ActionItem[] = [];
  
  // SO Strategy (Strengths-Opportunities)
  if (strengths.length > 0 && opportunities.length > 0) {
    actions.push({
      title: 'Aggressive Growth Strategy',
      description: `Leverage ${strengths[0]} to capture ${opportunities[0]}`,
      priority: 'high',
      effort: 'high',
      impact: 'high',
      timeframe: '6-12 months',
      metrics: ['Market share growth', 'Revenue growth']
    });
  }

  // WO Strategy (Weaknesses-Opportunities)
  if (weaknesses.length > 0 && opportunities.length > 0) {
    actions.push({
      title: 'Improvement Strategy',
      description: `Address ${weaknesses[0]} to better capture market opportunities`,
      priority: 'high',
      effort: 'medium',
      impact: 'medium',
      timeframe: '3-6 months',
      metrics: ['Weakness KPI improvement', 'Opportunity capture rate']
    });
  }

  return {
    frameworkId: 'swot',
    frameworkName: 'SWOT Analysis',
    position: {
      position,
      score: swotScore,
      confidence: 0.70
    },
    insights,
    visualizationData: {
      type: 'quadrant',
      strengths,
      weaknesses,
      opportunities,
      threats
    },
    actions
  };
}

// Porter's Five Forces Analysis
function analyzePortersFiveForces(data: ReturnType<typeof convertFlashData>): FrameworkAnalysis {
  // Calculate each force (0-10 scale, higher = more challenging)
  const competitiveRivalry = Math.min(10, (data.competitorCount / 5) + (10 - data.differentiationLevel) * 0.3);
  const buyerPower = Math.min(10, 8 - data.brandStrength + (data.customerBase < 1000 ? 2 : 0));
  const supplierPower = 5; // Default middle value without specific data
  const threatOfSubstitutes = Math.min(10, 10 - data.differentiationLevel);
  const threatOfNewEntrants = Math.min(10, 7 - (data.fundingRaised > 10000000 ? 3 : 0));

  const forces = {
    competitive_rivalry: competitiveRivalry,
    buyer_power: buyerPower,
    supplier_power: supplierPower,
    threat_of_substitutes: threatOfSubstitutes,
    threat_of_new_entrants: threatOfNewEntrants
  };

  const averageForce = Object.values(forces).reduce((a, b) => a + b, 0) / 5;
  const position = averageForce > 7 ? 'Very Challenging' :
                   averageForce > 5 ? 'Challenging' :
                   averageForce > 3 ? 'Moderate' : 'Favorable';

  const insights: FrameworkInsight[] = [];
  
  if (competitiveRivalry > 7) {
    insights.push({
      title: 'Intense Competitive Rivalry',
      description: 'High competition threatens profitability and market position.',
      importance: 'critical',
      dataPoints: [
        `${data.competitorCount} active competitors`,
        `Differentiation score: ${data.differentiationLevel}/10`,
        `Market growth: ${data.marketGrowthRate.toFixed(1)}%`
      ],
      recommendation: 'Differentiate strongly or find niche markets.',
      timeframe: 'immediate'
    });
  }

  if (buyerPower > 6) {
    insights.push({
      title: 'Strong Buyer Power',
      description: 'Customers have significant negotiating leverage.',
      importance: 'high',
      dataPoints: [
        `Customer count: ${data.customerBase}`,
        `Brand strength: ${data.brandStrength}/10`,
        `NPS: ${data.nps}`
      ],
      recommendation: 'Increase switching costs and build customer loyalty.',
      timeframe: 'short-term'
    });
  }

  const actions: ActionItem[] = [];
  
  if (position === 'Very Challenging' || position === 'Challenging') {
    actions.push({
      title: 'Competitive Positioning Strategy',
      description: 'Develop unique value proposition to reduce competitive pressures',
      priority: 'critical',
      effort: 'high',
      impact: 'high',
      timeframe: '3-6 months',
      metrics: ['Differentiation score', 'Customer retention', 'Pricing power']
    });
  }

  return {
    frameworkId: 'porters_five_forces',
    frameworkName: "Porter's Five Forces",
    position: {
      position,
      score: averageForce,
      confidence: 0.65
    },
    insights,
    visualizationData: {
      type: 'spider',
      forces,
      maxValue: 10
    },
    actions
  };
}

// Main analysis function
export async function analyzeFramework(
  frameworkId: string, 
  analysisData: EnrichedAnalysisData
): Promise<FrameworkAnalysis | null> {
  try {
    const data = convertFlashData(analysisData);
    
    switch (frameworkId) {
      case 'bcg_matrix':
        return analyzeBCGMatrix(data);
      case 'swot':
        return analyzeSWOT(data);
      case 'porters_five_forces':
        return analyzePortersFiveForces(data);
      default:
        return null;
    }
  } catch (error) {
    console.error(`Error analyzing framework ${frameworkId}:`, error);
    return null;
  }
}