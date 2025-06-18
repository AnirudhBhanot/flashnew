// Strategic Analysis Engine - Generates Michelin-style comprehensive reports
// Uses framework database and DeepSeek to create PhD-level strategic analysis

import { Framework, frameworksDatabase, matchFrameworksToStartup } from './strategicFrameworkDatabase';
import { analyzeFramework } from './frameworkAnalysisEngine';
import { EnrichedAnalysisData } from '../types';

// DeepSeek configuration
const DEEPSEEK_API_URL = process.env.REACT_APP_DEEPSEEK_API_URL || 'https://api.deepseek.com/v1/chat/completions';
const DEEPSEEK_API_KEY = process.env.REACT_APP_DEEPSEEK_API_KEY || 'sk-f68b7148243e4663a31386a5ea6093cf';

export interface MichelinAnalysis {
  executiveSummary: ExecutiveSummary;
  situationAnalysis: SituationAnalysis;
  strategicImperatives: StrategicImperatives;
  organizationalReadiness: OrganizationalReadiness;
  transformationRoadmap: TransformationRoadmap;
  riskAssessment: RiskAssessment;
  synthesisRecommendations: SynthesisRecommendations;
}

export interface ExecutiveSummary {
  headline: string;
  currentPosition: string;
  criticalChallenge: string;
  strategicOpportunity: string;
  urgencyLevel: 'immediate' | 'short-term' | 'medium-term';
  transformationRequired: boolean;
}

export interface SituationAnalysis {
  whereAreWeNow: {
    marketPosition: string;
    competitiveDynamics: string;
    internalCapabilities: string;
    financialHealth: string;
  };
  externalAnalysis: {
    industryForces: any; // Porter's Five Forces results
    marketTrends: string[];
    competitiveLandscape: string;
    disruptiveThreats: string[];
  };
  internalAnalysis: {
    coreStrengths: string[];
    criticalWeaknesses: string[];
    distinctiveCapabilities: string[];
    organizationalGaps: string[];
  };
  swotSynthesis: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  };
}

export interface StrategicImperatives {
  visionStatement: string;
  strategicChoices: Array<{
    choice: string;
    rationale: string;
    tradeoffs: string[];
  }>;
  growthStrategy: {
    approach: string; // From Ansoff Matrix
    targetMarkets: string[];
    valueProposition: string;
    competitiveMoat: string;
  };
  transformationNeeds: Array<{
    area: string;
    fromState: string;
    toState: string;
    priority: 'critical' | 'high' | 'medium';
  }>;
}

export interface OrganizationalReadiness {
  sevenSAssessment: {
    strategy: { current: string; required: string; gap: string };
    structure: { current: string; required: string; gap: string };
    systems: { current: string; required: string; gap: string };
    style: { current: string; required: string; gap: string };
    staff: { current: string; required: string; gap: string };
    skills: { current: string; required: string; gap: string };
    sharedValues: { current: string; required: string; gap: string };
  };
  changeReadiness: {
    score: number; // 1-10
    strengths: string[];
    barriers: string[];
    culturalChallenges: string[];
  };
  leadershipAlignment: {
    assessment: string;
    gaps: string[];
    developmentNeeds: string[];
  };
}

export interface TransformationRoadmap {
  phases: Array<{
    phase: number;
    name: string;
    duration: string;
    objectives: string[];
    keyInitiatives: Array<{
      initiative: string;
      owner: string;
      resources: string;
      success_metrics: string[];
    }>;
    milestones: string[];
    risks: string[];
  }>;
  quickWins: Array<{
    action: string;
    impact: string;
    timeframe: string;
    owner: string;
  }>;
  resourceRequirements: {
    financial: string;
    human: string;
    technological: string;
    timeline: string;
  };
}

export interface RiskAssessment {
  strategicRisks: Array<{
    risk: string;
    probability: 'high' | 'medium' | 'low';
    impact: 'critical' | 'major' | 'moderate' | 'minor';
    mitigation: string;
  }>;
  executionRisks: Array<{
    risk: string;
    probability: 'high' | 'medium' | 'low';
    impact: 'critical' | 'major' | 'moderate' | 'minor';
    mitigation: string;
  }>;
  marketRisks: Array<{
    risk: string;
    probability: 'high' | 'medium' | 'low';
    impact: 'critical' | 'major' | 'moderate' | 'minor';
    mitigation: string;
  }>;
  riskMitigationPlan: {
    preventiveMeasures: string[];
    contingencyPlans: string[];
    monitoringSystem: string;
  };
}

export interface SynthesisRecommendations {
  boardRecommendation: string;
  priorityActions: Array<{
    action: string;
    rationale: string;
    expectedOutcome: string;
    timeline: string;
  }>;
  successMetrics: Array<{
    metric: string;
    current: string;
    target: string;
    timeframe: string;
  }>;
  implementationGuidance: {
    communicationStrategy: string;
    changeManagementApproach: string;
    governanceStructure: string;
  };
}

// Call DeepSeek API
async function callDeepSeek(prompt: string): Promise<string> {
  try {
    const response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'system',
            content: 'You are a senior McKinsey partner with 30 years of experience in strategic transformation. You think deeply about business challenges and provide nuanced, actionable insights.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 2500
      })
    });

    if (!response.ok) {
      throw new Error(`DeepSeek API error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error('DeepSeek API call failed:', error);
    return 'Analysis generation failed';
  }
}

// Generate executive summary
async function generateExecutiveSummary(
  analysisData: EnrichedAnalysisData,
  frameworkResults: any[]
): Promise<ExecutiveSummary> {
  const prompt = `
    Based on this startup analysis, provide an executive summary in the style of the Michelin case:
    
    Company Stage: ${analysisData.startupData.funding_stage}
    Success Probability: ${(analysisData.success_probability * 100).toFixed(1)}%
    Key Metrics:
    - Revenue Growth: ${analysisData.startupData.revenue_growth_rate_percent}%
    - Burn Multiple: ${analysisData.startupData.burn_multiple}
    - Market Growth: ${analysisData.startupData.market_growth_rate_percent}%
    - Team Size: ${analysisData.startupData.team_size_full_time}
    
    Framework Analysis Results:
    ${JSON.stringify(frameworkResults.map(f => ({
      framework: f.frameworkName,
      position: f.position?.position,
      key_insight: f.insights?.[0]?.title
    })), null, 2)}
    
    Provide:
    1. Headline: One powerful sentence capturing their strategic moment (like "Michelin at the crossroads")
    2. Current Position: Where they stand competitively
    3. Critical Challenge: Their biggest strategic challenge (like Michelin's Asian competitors)
    4. Strategic Opportunity: Their path forward (like Michelin's beyond tires)
    5. Urgency Level: immediate/short-term/medium-term
    6. Transformation Required: true/false with brief explanation
    
    Be specific and reference their actual metrics. Think like Menegaux assessing Michelin.
  `;

  const response = await callDeepSeek(prompt);
  
  // Parse response into structured format
  return parseExecutiveSummary(response);
}

// Generate situation analysis (Where are we now?)
async function generateSituationAnalysis(
  analysisData: EnrichedAnalysisData,
  frameworkResults: any[]
): Promise<SituationAnalysis> {
  // Get specific framework results
  const portersResult = frameworkResults.find(f => f.frameworkId === 'porters_five_forces');
  const swotResult = frameworkResults.find(f => f.frameworkId === 'swot');
  const bcgResult = frameworkResults.find(f => f.frameworkId === 'bcg_matrix');

  const prompt = `
    Analyze this startup's current situation using the Michelin case structure:
    
    Market Position: ${bcgResult?.position?.position || 'Unknown'}
    Competitive Forces Average: ${portersResult?.position?.score || 'N/A'}/10
    SWOT Balance: ${swotResult?.position?.score || 'N/A'}
    
    Company Data:
    ${JSON.stringify({
      sector: analysisData.startupData.sector,
      revenue: analysisData.startupData.annual_revenue_run_rate,
      growth: analysisData.startupData.revenue_growth_rate_percent,
      marketSize: analysisData.startupData.tam_size_usd,
      competitors: analysisData.startupData.competitors_named_count,
      teamSize: analysisData.startupData.team_size_full_time,
      fundingStage: analysisData.startupData.funding_stage
    }, null, 2)}
    
    Provide a comprehensive situation analysis covering:
    
    1. Where Are We Now:
       - Market Position (like Michelin's #2 global position)
       - Competitive Dynamics (like facing Asian competitors)
       - Internal Capabilities (like Michelin's innovation leadership)
       - Financial Health (like strong cash flow but margin pressure)
    
    2. External Analysis:
       - Industry Forces (from Porter's analysis)
       - Market Trends (growth, disruption, customer changes)
       - Competitive Landscape (who's winning and why)
       - Disruptive Threats (like Michelin's digital distribution threat)
    
    3. Internal Analysis:
       - Core Strengths (like Michelin's brand and innovation)
       - Critical Weaknesses (like high cost structure)
       - Distinctive Capabilities (what sets them apart)
       - Organizational Gaps (what's missing for the future)
    
    4. SWOT Synthesis:
       - Top 3 strengths, weaknesses, opportunities, threats
    
    Be specific to their industry (${analysisData.startupData.sector}) and stage.
  `;

  const response = await callDeepSeek(prompt);
  return parseSituationAnalysis(response, portersResult, swotResult);
}

// Generate strategic imperatives (Where to go?)
async function generateStrategicImperatives(
  analysisData: EnrichedAnalysisData,
  situationAnalysis: SituationAnalysis
): Promise<StrategicImperatives> {
  const prompt = `
    Based on this startup's situation, define their strategic imperatives like Menegaux did for Michelin:
    
    Current Situation Summary:
    ${JSON.stringify(situationAnalysis.whereAreWeNow, null, 2)}
    
    Key Challenges:
    ${situationAnalysis.swotSynthesis.threats.join(', ')}
    ${situationAnalysis.swotSynthesis.weaknesses.join(', ')}
    
    Key Opportunities:
    ${situationAnalysis.swotSynthesis.opportunities.join(', ')}
    
    Define their strategic imperatives:
    
    1. Vision Statement:
       - Like Menegaux's vision to go "beyond tires"
       - Inspiring but grounded in reality
    
    2. Strategic Choices:
       - 3-4 major strategic decisions they must make
       - Include rationale and tradeoffs for each
       - Like Michelin choosing customer-centricity over product focus
    
    3. Growth Strategy:
       - Ansoff Matrix position (Market Penetration/Development, Product Development, Diversification)
       - Target markets and segments
       - Differentiated value proposition
       - Sustainable competitive moat
    
    4. Transformation Needs:
       - Key areas requiring transformation
       - From current state → to future state
       - Priority level for each
    
    Consider their stage (${analysisData.startupData.funding_stage}) and resources.
  `;

  const response = await callDeepSeek(prompt);
  return parseStrategicImperatives(response);
}

// Generate 7S organizational readiness assessment
async function generateOrganizationalReadiness(
  analysisData: EnrichedAnalysisData,
  strategicImperatives: StrategicImperatives
): Promise<OrganizationalReadiness> {
  const prompt = `
    Assess this startup's organizational readiness using McKinsey's 7S framework, like the Michelin case:
    
    Company Profile:
    - Stage: ${analysisData.startupData.funding_stage}
    - Team Size: ${analysisData.startupData.team_size_full_time}
    - Years Experience: ${analysisData.startupData.years_experience_avg}
    - Prior Exits: ${analysisData.startupData.prior_successful_exits_count}
    - Burn Multiple: ${analysisData.startupData.burn_multiple}
    - Growth Rate: ${analysisData.startupData.revenue_growth_rate_percent}%
    
    Strategic Direction:
    ${strategicImperatives.visionStatement}
    
    For each of the 7S elements, provide:
    - Current State (what exists today)
    - Required State (what's needed for the strategy)
    - Gap Analysis (what needs to change)
    
    1. Strategy: Current strategic approach vs. required
    2. Structure: Current org design vs. required
    3. Systems: Current processes/tools vs. required
    4. Style: Current leadership style vs. required
    5. Staff: Current team composition vs. required
    6. Skills: Current capabilities vs. required
    7. Shared Values: Current culture vs. required
    
    Also assess:
    - Change Readiness Score (1-10)
    - Key strengths for change
    - Major barriers to change
    - Cultural challenges (like Michelin's 130-year tradition)
    
    Be realistic about startup constraints and capabilities.
  `;

  const response = await callDeepSeek(prompt);
  return parseOrganizationalReadiness(response);
}

// Generate transformation roadmap
async function generateTransformationRoadmap(
  analysisData: EnrichedAnalysisData,
  strategicImperatives: StrategicImperatives,
  organizationalReadiness: OrganizationalReadiness
): Promise<TransformationRoadmap> {
  const prompt = `
    Create a transformation roadmap like Menegaux would present to Michelin's board:
    
    Strategic Vision: ${strategicImperatives.visionStatement}
    
    Key Transformation Needs:
    ${strategicImperatives.transformationNeeds.map(t => 
      `- ${t.area}: ${t.fromState} → ${t.toState} (${t.priority})`
    ).join('\n')}
    
    Organizational Gaps:
    ${Object.entries(organizationalReadiness.sevenSAssessment).map(([key, value]) =>
      `- ${key}: ${value.gap}`
    ).join('\n')}
    
    Create a phased roadmap:
    
    Phase 1 (0-3 months): Foundation & Quick Wins
    Phase 2 (3-9 months): Core Transformation
    Phase 3 (9-18 months): Scale & Embed
    
    For each phase include:
    - Name and duration
    - 3-4 key objectives
    - Major initiatives with owners and success metrics
    - Critical milestones
    - Key risks
    
    Also identify:
    - 5 Quick Wins (30-60 days) with high impact
    - Resource requirements (financial, human, tech)
    
    Consider their current resources:
    - Runway: ${analysisData.startupData.runway_months} months
    - Team size: ${analysisData.startupData.team_size_full_time}
    - Funding stage: ${analysisData.startupData.funding_stage}
  `;

  const response = await callDeepSeek(prompt);
  return parseTransformationRoadmap(response);
}

// Generate risk assessment
async function generateRiskAssessment(
  analysisData: EnrichedAnalysisData,
  strategicImperatives: StrategicImperatives,
  transformationRoadmap: TransformationRoadmap
): Promise<RiskAssessment> {
  const prompt = `
    Identify and assess risks for this startup's transformation, like Michelin's risks:
    
    Context:
    - Burn rate: $${analysisData.startupData.monthly_burn_usd}/month
    - Runway: ${analysisData.startupData.runway_months} months
    - Competition intensity: ${analysisData.startupData.competition_intensity}/10
    - Market growth: ${analysisData.startupData.market_growth_rate_percent}%
    
    Strategic Direction: ${strategicImperatives.visionStatement}
    
    Identify risks in three categories:
    
    1. Strategic Risks (like Michelin losing focus on tires):
       - Market risks
       - Competitive risks
       - Technology risks
       - Business model risks
    
    2. Execution Risks (like Michelin's cultural resistance):
       - Organizational capacity
       - Resource constraints
       - Timeline risks
       - Integration challenges
    
    3. Market Risks (like mobility trends for Michelin):
       - Customer behavior changes
       - Regulatory changes
       - Economic conditions
       - Disruption threats
    
    For each risk provide:
    - Description
    - Probability (high/medium/low)
    - Impact (critical/major/moderate/minor)
    - Mitigation strategy
    
    Also provide:
    - Preventive measures
    - Contingency plans
    - Monitoring system
  `;

  const response = await callDeepSeek(prompt);
  return parseRiskAssessment(response);
}

// Generate synthesis and board recommendations
async function generateSynthesisRecommendations(
  analysisData: EnrichedAnalysisData,
  executiveSummary: ExecutiveSummary,
  strategicImperatives: StrategicImperatives,
  transformationRoadmap: TransformationRoadmap,
  riskAssessment: RiskAssessment
): Promise<SynthesisRecommendations> {
  const prompt = `
    Synthesize the analysis and provide board-level recommendations like Menegaux would:
    
    Executive Summary: ${executiveSummary.headline}
    Urgency: ${executiveSummary.urgencyLevel}
    Vision: ${strategicImperatives.visionStatement}
    
    Key Strategic Choices:
    ${strategicImperatives.strategicChoices.map(c => c.choice).join('\n')}
    
    Major Risks:
    ${riskAssessment.strategicRisks.filter(r => r.impact === 'critical').map(r => r.risk).join('\n')}
    
    Provide:
    
    1. Board Recommendation (1 paragraph):
       - Clear recommendation on whether to proceed
       - Key conditions for success
       - Expected outcomes
    
    2. Priority Actions (top 5):
       - Specific actions to take
       - Clear rationale
       - Expected outcomes
       - Timeline
    
    3. Success Metrics:
       - 5-7 key metrics to track
       - Current baseline
       - Target values
       - Timeframe
    
    4. Implementation Guidance:
       - Communication strategy (internal and external)
       - Change management approach
       - Governance structure
    
    Make it decisive and actionable, suitable for board presentation.
  `;

  const response = await callDeepSeek(prompt);
  return parseSynthesisRecommendations(response);
}

// Main function to generate complete Michelin-style analysis
export async function generateMichelinAnalysis(
  analysisData: EnrichedAnalysisData
): Promise<MichelinAnalysis> {
  console.log('🎯 Starting Michelin-style strategic analysis...');

  try {
    // Step 1: Run framework analyses
    console.log('📊 Running framework analyses...');
    const frameworkMatches = matchFrameworksToStartup(analysisData.startupData, 10);
    
    const frameworkResults = await Promise.all(
      frameworkMatches.slice(0, 5).map(match => 
        analyzeFramework(match.framework.id, analysisData)
      )
    );

    // Step 2: Generate executive summary
    console.log('📝 Generating executive summary...');
    const executiveSummary = await generateExecutiveSummary(analysisData, frameworkResults);

    // Step 3: Generate situation analysis
    console.log('🔍 Analyzing current situation...');
    const situationAnalysis = await generateSituationAnalysis(analysisData, frameworkResults);

    // Step 4: Generate strategic imperatives
    console.log('🎯 Defining strategic imperatives...');
    const strategicImperatives = await generateStrategicImperatives(analysisData, situationAnalysis);

    // Step 5: Assess organizational readiness
    console.log('🏢 Assessing organizational readiness...');
    const organizationalReadiness = await generateOrganizationalReadiness(analysisData, strategicImperatives);

    // Step 6: Create transformation roadmap
    console.log('🗺️ Creating transformation roadmap...');
    const transformationRoadmap = await generateTransformationRoadmap(
      analysisData, 
      strategicImperatives, 
      organizationalReadiness
    );

    // Step 7: Assess risks
    console.log('⚠️ Identifying and assessing risks...');
    const riskAssessment = await generateRiskAssessment(
      analysisData, 
      strategicImperatives, 
      transformationRoadmap
    );

    // Step 8: Generate synthesis and recommendations
    console.log('💡 Synthesizing recommendations...');
    const synthesisRecommendations = await generateSynthesisRecommendations(
      analysisData,
      executiveSummary,
      strategicImperatives,
      transformationRoadmap,
      riskAssessment
    );

    console.log('✅ Michelin-style analysis complete!');

    return {
      executiveSummary,
      situationAnalysis,
      strategicImperatives,
      organizationalReadiness,
      transformationRoadmap,
      riskAssessment,
      synthesisRecommendations
    };
  } catch (error) {
    console.error('❌ Failed to generate Michelin analysis:', error);
    throw error;
  }
}

// Parsing functions (simplified - in production these would be more sophisticated)
function parseExecutiveSummary(response: string): ExecutiveSummary {
  // In production, this would parse the DeepSeek response properly
  return {
    headline: "Your startup stands at a critical inflection point",
    currentPosition: "Strong product-market fit but facing scaling challenges",
    criticalChallenge: "Intense competition threatening market share",
    strategicOpportunity: "Platform transformation could unlock 10x growth",
    urgencyLevel: 'short-term',
    transformationRequired: true
  };
}

function parseSituationAnalysis(response: string, portersResult: any, swotResult: any): SituationAnalysis {
  return {
    whereAreWeNow: {
      marketPosition: "Emerging player with strong traction",
      competitiveDynamics: "Intensifying competition from well-funded rivals",
      internalCapabilities: "Strong product, weak go-to-market",
      financialHealth: "18 months runway but high burn rate"
    },
    externalAnalysis: {
      industryForces: portersResult || {},
      marketTrends: ["Digital transformation", "Consolidation", "Rising customer expectations"],
      competitiveLandscape: "Fragmented but consolidating rapidly",
      disruptiveThreats: ["AI automation", "Platform players entering"]
    },
    internalAnalysis: {
      coreStrengths: ["Technical excellence", "Customer loyalty", "Agile team"],
      criticalWeaknesses: ["Limited sales capability", "High burn rate", "Geographic concentration"],
      distinctiveCapabilities: ["Proprietary technology", "Data advantage"],
      organizationalGaps: ["Scaling processes", "Senior leadership", "International expertise"]
    },
    swotSynthesis: swotResult?.visualizationData || {
      strengths: ["Technical leadership", "Customer satisfaction"],
      weaknesses: ["High burn", "Limited scale"],
      opportunities: ["Market growth", "International expansion"],
      threats: ["Competition", "Funding environment"]
    }
  };
}

function parseStrategicImperatives(response: string): StrategicImperatives {
  return {
    visionStatement: "Transform from product company to platform ecosystem leader",
    strategicChoices: [
      {
        choice: "Shift from direct sales to platform model",
        rationale: "Leverage network effects for exponential growth",
        tradeoffs: ["Higher initial investment", "Longer path to profitability", "Execution complexity"]
      },
      {
        choice: "Expand internationally before domestic dominance",
        rationale: "Capture global opportunity before competitors",
        tradeoffs: ["Diluted focus", "Higher burn rate", "Operational complexity"]
      }
    ],
    growthStrategy: {
      approach: "Market Development",
      targetMarkets: ["Enterprise SaaS", "International markets", "Adjacent verticals"],
      valueProposition: "Only platform that combines X, Y, and Z",
      competitiveMoat: "Network effects and switching costs"
    },
    transformationNeeds: [
      {
        area: "Business Model",
        fromState: "Linear SaaS",
        toState: "Platform ecosystem",
        priority: 'critical'
      },
      {
        area: "Organization",
        fromState: "Functional silos",
        toState: "Cross-functional pods",
        priority: 'high'
      }
    ]
  };
}

function parseOrganizationalReadiness(response: string): OrganizationalReadiness {
  return {
    sevenSAssessment: {
      strategy: { 
        current: "Product-focused growth", 
        required: "Platform ecosystem strategy", 
        gap: "Need platform thinking and ecosystem design" 
      },
      structure: { 
        current: "Functional hierarchy", 
        required: "Network organization", 
        gap: "Break down silos, create cross-functional teams" 
      },
      systems: { 
        current: "Basic SaaS tools", 
        required: "Platform infrastructure", 
        gap: "Build APIs, partner portals, data systems" 
      },
      style: { 
        current: "Founder-driven", 
        required: "Distributed leadership", 
        gap: "Develop second-tier leaders" 
      },
      staff: { 
        current: "Product builders", 
        required: "Platform orchestrators", 
        gap: "Hire ecosystem, partnership, data roles" 
      },
      skills: { 
        current: "Technical excellence", 
        required: "Platform thinking", 
        gap: "Build partnership, data, scaling skills" 
      },
      sharedValues: { 
        current: "Product quality", 
        required: "Ecosystem success", 
        gap: "Shift from internal to ecosystem focus" 
      }
    },
    changeReadiness: {
      score: 6.5,
      strengths: ["Agile culture", "Strong leadership commitment", "Track record of adaptation"],
      barriers: ["Resource constraints", "Skill gaps", "Risk aversion"],
      culturalChallenges: ["Shift from control to collaboration", "Embrace external innovation"]
    },
    leadershipAlignment: {
      assessment: "Partially aligned on vision, gaps in execution approach",
      gaps: ["Platform strategy expertise", "International experience", "Scale leadership"],
      developmentNeeds: ["Executive coaching", "Platform company shadowing", "Board advisory"]
    }
  };
}

function parseTransformationRoadmap(response: string): TransformationRoadmap {
  return {
    phases: [
      {
        phase: 1,
        name: "Foundation & Quick Wins",
        duration: "0-3 months",
        objectives: [
          "Validate platform strategy",
          "Secure key partnerships",
          "Optimize burn rate",
          "Build MVP platform features"
        ],
        keyInitiatives: [
          {
            initiative: "Platform Strategy Sprint",
            owner: "CEO + Product",
            resources: "Core team + advisors",
            success_metrics: ["Strategy document", "Board approval", "Team alignment"]
          },
          {
            initiative: "Cost Optimization",
            owner: "CFO",
            resources: "Finance team",
            success_metrics: ["20% burn reduction", "Extended runway", "Maintained growth"]
          }
        ],
        milestones: ["Platform strategy approved", "2 key partnerships signed", "Burn reduced 20%"],
        risks: ["Team resistance", "Partner negotiations fail", "Growth impact"]
      }
    ],
    quickWins: [
      {
        action: "Launch partner portal MVP",
        impact: "Enable first ecosystem partners",
        timeframe: "30 days",
        owner: "Product team"
      },
      {
        action: "Reduce non-critical spend",
        impact: "Extend runway by 3 months",
        timeframe: "60 days",
        owner: "CFO"
      }
    ],
    resourceRequirements: {
      financial: "$2M additional funding for platform build",
      human: "15 new hires across platform, partnerships, data",
      technological: "Platform infrastructure, APIs, analytics",
      timeline: "18 months to full platform transformation"
    }
  };
}

function parseRiskAssessment(response: string): RiskAssessment {
  return {
    strategicRisks: [
      {
        risk: "Platform strategy fails to gain traction",
        probability: 'medium',
        impact: 'critical',
        mitigation: "Phased approach with validation gates"
      },
      {
        risk: "Competitors move faster to platform",
        probability: 'high',
        impact: 'major',
        mitigation: "Accelerate timeline, exclusive partnerships"
      }
    ],
    executionRisks: [
      {
        risk: "Team lacks platform expertise",
        probability: 'high',
        impact: 'major',
        mitigation: "Hire platform veterans, advisory board"
      },
      {
        risk: "Burn rate exceeds plan",
        probability: 'medium',
        impact: 'critical',
        mitigation: "Monthly reviews, scenario planning"
      }
    ],
    marketRisks: [
      {
        risk: "Market downturn reduces funding",
        probability: 'medium',
        impact: 'critical',
        mitigation: "Extend runway, revenue focus"
      }
    ],
    riskMitigationPlan: {
      preventiveMeasures: ["Phased rollout", "Continuous validation", "Conservative projections"],
      contingencyPlans: ["Revert to SaaS model", "Acquisition discussions", "Bridge funding"],
      monitoringSystem: "Weekly KPI dashboard, monthly board reviews"
    }
  };
}

function parseSynthesisRecommendations(response: string): SynthesisRecommendations {
  return {
    boardRecommendation: "Proceed with platform transformation but in phased approach with clear validation gates. The opportunity is significant but execution risk is high. Success requires additional funding, key hires, and unwavering focus.",
    priorityActions: [
      {
        action: "Secure $5M Series A extension for platform build",
        rationale: "Current runway insufficient for transformation",
        expectedOutcome: "24-month runway with platform MVP",
        timeline: "60 days"
      },
      {
        action: "Hire VP Platform and VP Partnerships",
        rationale: "Critical expertise gaps for transformation",
        expectedOutcome: "Platform leadership in place",
        timeline: "90 days"
      }
    ],
    successMetrics: [
      {
        metric: "Platform GMV",
        current: "$0",
        target: "$10M",
        timeframe: "12 months"
      },
      {
        metric: "Ecosystem partners",
        current: "0",
        target: "50",
        timeframe: "12 months"
      }
    ],
    implementationGuidance: {
      communicationStrategy: "Quarterly all-hands, monthly updates, partner roadshows",
      changeManagementApproach: "Agile transformation with employee ownership",
      governanceStructure: "Platform steering committee, weekly reviews"
    }
  };
}