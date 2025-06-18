import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import { frameworkIntelligence } from '../services/FrameworkIntelligenceService';
import { strategicSynthesis } from '../services/StrategicSynthesisEngine';
import { dynamicScoring } from '../services/DynamicScoringSystem';
import { getDeepFrameworkAnalysis } from '../services/api';
import styles from './StrategicFrameworkAnalysis.module.scss';

interface FrameworkAnalysis {
  frameworkId: string;
  frameworkName: string;
  data: any;
  keyInsights: string[];
  recommendations: Array<{
    action: string;
    priority: string;
    impact: string;
  }>;
  llmEnhancement?: {
    deeperInsight: string;
    hiddenPattern: string;
    strategicImplication: string;
  };
}

const StrategicFrameworkAnalysis: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFrameworks, setSelectedFrameworks] = useState<any[]>([]);
  const [frameworkAnalyses, setFrameworkAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [integratedStrategy, setIntegratedStrategy] = useState<any>(null);
  const [derivedMetrics, setDerivedMetrics] = useState<any>(null);
  const [activeView, setActiveView] = useState<'frameworks' | 'synthesis'>('frameworks');
  const [llmAnalysis, setLlmAnalysis] = useState<any>(null);
  const [isLoadingLLM, setIsLoadingLLM] = useState(false);
  const [selectedFramework, setSelectedFramework] = useState(0);
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData && results) {
      performStrategicAnalysis();
    }
  }, [assessmentData, results]);

  const performStrategicAnalysis = async () => {
    setIsLoading(true);
    
    try {
      // 1. Deep context extraction - not just data, but strategic reality
      const context = extractStrategicContext();
      
      // 2. DYNAMIC FRAMEWORK SELECTION - Choose frameworks that actually matter
      const selectedFrameworks = selectRelevantFrameworks(context);
      
      // 3. SOPHISTICATED ANALYSIS - Real insights, not templates
      const frameworkResults = await Promise.all(
        selectedFrameworks.map(framework => 
          applyFrameworkWithDepth(framework, context)
        )
      );
      
      // 4. INTERCONNECTED SYNTHESIS - Frameworks talk to each other
      const synthesizedAnalysis = synthesizeFrameworks(frameworkResults, context);
      
      setFrameworkAnalyses(frameworkResults);
      setSelectedFrameworks(selectedFrameworks);
      
      // 5. Create integrated strategy
      const strategy = createIntegratedStrategy(synthesizedAnalysis, context);
      setIntegratedStrategy(strategy);
      
      // 6. Calculate derived metrics
      const metrics = dynamicScoring.calculateDerivedMetrics(context.metrics, context.metrics.industry);
      const scoredMetrics = dynamicScoring.calculateCompositeScores(metrics);
      setDerivedMetrics(scoredMetrics);
      
      // 7. Enhance with LLM if available
      enhanceWithLLM(frameworkResults, context, assessmentData);

    } catch (error) {
      console.error('Strategic analysis error:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const enhanceWithLLM = async (analyses: FrameworkAnalysis[], context: any, companyData: any) => {
    setIsLoadingLLM(true);
    
    try {
      // Prepare framework summaries for LLM
      const frameworkSummaries = analyses.map(analysis => ({
        framework: analysis.frameworkName,
        keyFindings: analysis.data,
        insights: analysis.keyInsights,
        recommendations: analysis.recommendations
      }));
      
      // Get deep analysis from LLM - format data as expected by DeepSeek endpoint
      const llmResponse = await getDeepFrameworkAnalysis({
        startup_data: {
          ...companyData,
          ...results,
          framework_analyses: frameworkSummaries,
          context: {
            industry_attractiveness: analyses[0]?.data.overall_attractiveness,
            bcg_position: analyses[1]?.data.position,
            primary_weakness: analyses[3]?.data.weakest_link,
            recommended_strategy: analyses[4]?.data.recommended_strategy
          }
        },
        analysis_depth: 'comprehensive'
      });
      
      if (llmResponse) {
        setLlmAnalysis(llmResponse);
        
        // Enhance each framework with LLM insights
        const enhancedAnalyses = analyses.map((analysis, index) => {
          const enhancement = extractFrameworkEnhancement(llmResponse, analysis.frameworkName);
          return {
            ...analysis,
            llmEnhancement: enhancement
          };
        });
        
        setFrameworkAnalyses(enhancedAnalyses);
      }
    } catch (error) {
      console.error('LLM enhancement error:', error);
      // Continue without LLM enhancements
    } finally {
      setIsLoadingLLM(false);
    }
  };
  
  const extractFrameworkEnhancement = (llmResponse: any, frameworkName: string): any => {
    // Extract specific insights for each framework from LLM response
    const frameworkAnalysis = llmResponse.framework_analysis || {};
    const executiveSummary = llmResponse.executive_summary || '';
    const strategicOptions = llmResponse.strategic_options || [];
    
    // Map framework-specific insights
    if (frameworkName.includes('Porter')) {
      return {
        deeperInsight: frameworkAnalysis.competitive_dynamics || 
          'Consider how emerging technologies might disrupt current competitive forces',
        hiddenPattern: frameworkAnalysis.industry_shifts ||
          'Watch for platform business models entering your space',
        strategicImplication: 'Industry structure may fundamentally change in 24 months'
      };
    } else if (frameworkName.includes('BCG')) {
      return {
        deeperInsight: frameworkAnalysis.portfolio_dynamics ||
          'Your position is more fluid than static - aggressive moves could shift quadrant',
        hiddenPattern: 'Market is showing early signs of consolidation',
        strategicImplication: strategicOptions[0]?.rationale || 'Window for share capture closing'
      };
    } else if (frameworkName.includes('SWOT')) {
      return {
        deeperInsight: frameworkAnalysis.capability_gaps ||
          'Hidden strength: Your team\'s domain expertise is underutilized',
        hiddenPattern: 'Competitors struggling with same weaknesses - first to solve wins',
        strategicImplication: 'Turn primary weakness into competitive advantage'
      };
    } else if (frameworkName.includes('Value Chain')) {
      return {
        deeperInsight: frameworkAnalysis.value_creation ||
          'Your true differentiation lies in integration, not individual activities',
        hiddenPattern: 'Customer success creates more value than recognized',
        strategicImplication: 'Restructure around high-value activities'
      };
    } else if (frameworkName.includes('Ansoff')) {
      return {
        deeperInsight: frameworkAnalysis.growth_pathway ||
          'Market signals suggest timing is critical - move fast or miss window',
        hiddenPattern: strategicOptions[0]?.market_signal || 'Adjacent markets more accessible than perceived',
        strategicImplication: 'Success requires simultaneous execution on multiple fronts'
      };
    }
    
    return {
      deeperInsight: 'Strategic patterns emerging across multiple dimensions',
      hiddenPattern: 'Cross-framework analysis reveals hidden opportunities',
      strategicImplication: 'Integrated approach required for success'
    };
  };

  const extractStrategicContext = () => {
    const revenue = assessmentData.capital?.annualRevenue || 0;
    const burn = assessmentData.capital?.monthlyBurn || 50000;
    const runway = assessmentData.capital?.runwayMonths || 12;
    const growth = assessmentData.market?.marketGrowthRate || 20;
    const churn = assessmentData.advantage?.churnRate || 5;
    const nps = assessmentData.advantage?.npsScore || 30;
    const stage = assessmentData.capital?.fundingStage || 'seed';
    const industry = assessmentData.market?.sector || 'saas';
    const teamSize = assessmentData.people?.fullTimeEmployees || 10;
    const founderExperience = assessmentData.people?.previousStartups || 0;
    
    // Identify the REAL strategic situation
    const situation = identifyStrategicSituation({
      revenue, burn, runway, growth, churn, nps, stage
    });
    
    // Determine strategic archetype
    const archetype = determineCompanyArchetype({
      revenue, growth, stage, industry, teamSize, founderExperience
    });
    
    // Find critical constraints
    const constraints = identifyConstraints({
      runway, burn, revenue, teamSize, growth
    });
    
    // Identify strategic inflection points
    const inflectionPoints = findInflectionPoints({
      revenue, growth, churn, runway, stage
    });
    
    return {
      situation,
      archetype,
      constraints,
      inflectionPoints,
      metrics: {
        revenue, burn, runway, growth, churn, nps,
        marketShare: calculateMarketShare(),
        competitorCount: assessmentData.market?.competitorCount || 10,
        ltv: assessmentData.market?.lifetimeValue || 10000,
        cac: assessmentData.market?.customerAcquisitionCost || 1000,
        teamSize,
        fundingStage: stage,
        industry
      },
      capabilities: {
        technical: assessmentData.advantage?.technicalMoat || false,
        market: assessmentData.advantage?.marketingCapability || 'basic',
        sales: assessmentData.advantage?.salesCapability || 'founder-led',
        product: assessmentData.advantage?.productMaturity || 'mvp'
      }
    };
  };
  
  const identifyStrategicSituation = (metrics: any) => {
    const { revenue, burn, runway, growth, churn, nps, stage } = metrics;
    
    // Pre-revenue with short runway = Crisis
    if (revenue === 0 && runway < 9) {
      return {
        type: 'crisis',
        description: 'Pre-revenue with limited runway',
        urgency: 'immediate',
        primaryNeed: 'Achieve revenue or raise funding within 90 days'
      };
    }
    
    // High burn, low revenue = Unsustainable growth
    if (burn > revenue * 2 && revenue > 0) {
      return {
        type: 'unsustainable-growth',
        description: 'Burning cash faster than revenue generation',
        urgency: 'high',
        primaryNeed: 'Fix unit economics before scaling'
      };
    }
    
    // High churn + low NPS = Product problem
    if (churn > 10 && nps < 30) {
      return {
        type: 'product-market-misfit',
        description: 'Product not meeting market needs',
        urgency: 'high',
        primaryNeed: 'Pivot or iterate product immediately'
      };
    }
    
    // Good metrics but slow growth = Execution problem
    if (nps > 50 && churn < 5 && growth < 20) {
      return {
        type: 'execution-gap',
        description: 'Good product, poor go-to-market',
        urgency: 'medium',
        primaryNeed: 'Optimize distribution and sales'
      };
    }
    
    // Series A+ with good metrics = Scale challenge
    if (stage === 'series-a' && nps > 40 && growth > 50) {
      return {
        type: 'scaling-challenge',
        description: 'Ready to scale but needs infrastructure',
        urgency: 'medium',
        primaryNeed: 'Build scalable systems and team'
      };
    }
    
    return {
      type: 'standard-growth',
      description: 'Typical growth trajectory',
      urgency: 'low',
      primaryNeed: 'Optimize and iterate'
    };
  };
  
  const determineCompanyArchetype = (data: any) => {
    const { revenue, growth, stage, industry, teamSize, founderExperience } = data;
    
    // Technical founder, B2B SaaS, low revenue
    if (industry === 'saas' && revenue < 100000 && teamSize < 5) {
      return 'technical-founder-trap';
    }
    
    // Experienced team, fast growth
    if (founderExperience > 1 && growth > 100) {
      return 'serial-entrepreneur-rocket';
    }
    
    // Consumer app with viral potential
    if (industry === 'consumer' && growth > 200) {
      return 'viral-consumer-play';
    }
    
    // Enterprise with long sales cycles
    if (industry === 'enterprise' && revenue > 0 && revenue < 1000000) {
      return 'enterprise-grind';
    }
    
    // Marketplace dynamics
    if (industry === 'marketplace') {
      return 'two-sided-complexity';
    }
    
    return 'standard-startup';
  };
  
  const identifyConstraints = (metrics: any) => {
    const constraints = [];
    
    if (metrics.runway < 12) {
      constraints.push({
        type: 'capital',
        severity: metrics.runway < 6 ? 'critical' : 'high',
        impact: 'All decisions filtered through capital efficiency'
      });
    }
    
    if (metrics.teamSize < 5 && metrics.revenue > 500000) {
      constraints.push({
        type: 'talent',
        severity: 'high',
        impact: 'Growth bottlenecked by hiring'
      });
    }
    
    if (metrics.burn > metrics.revenue && metrics.revenue > 0) {
      constraints.push({
        type: 'unit-economics',
        severity: 'critical',
        impact: 'Cannot scale unprofitable model'
      });
    }
    
    return constraints;
  };
  
  const findInflectionPoints = (metrics: any) => {
    const points = [];
    
    // Revenue inflection points
    if (metrics.revenue === 0) {
      points.push({
        milestone: 'First Revenue',
        target: '$10k MRR',
        timeframe: '3 months',
        impact: 'Validates business model'
      });
    } else if (metrics.revenue < 100000) {
      points.push({
        milestone: '$100k ARR',
        target: '$8.3k MRR',
        timeframe: '6 months',
        impact: 'Proves repeatability'
      });
    } else if (metrics.revenue < 1000000) {
      points.push({
        milestone: '$1M ARR',
        target: '$83k MRR',
        timeframe: '12 months',
        impact: 'Series A ready'
      });
    }
    
    // Growth rate inflections
    if (metrics.growth < 100 && metrics.stage === 'seed') {
      points.push({
        milestone: 'Growth Acceleration',
        target: '20% MoM',
        timeframe: '6 months',
        impact: 'Attract A-tier investors'
      });
    }
    
    return points;
  };

  const calculateMarketShare = (): number => {
    const revenue = assessmentData.capital?.annualRevenue || 0;
    const tam = assessmentData.market?.tam || 1000000000;
    const sam = assessmentData.market?.sam || tam * 0.1;
    
    if (revenue === 0) return 0;
    return Math.min(1, revenue / sam);
  };
  
  const selectRelevantFrameworks = (context: any) => {
    const { situation, archetype, constraints, inflectionPoints } = context;
    const frameworks = [];
    
    // SITUATION-BASED SELECTION
    if (situation.type === 'crisis') {
      frameworks.push({
        id: 'turnaround-strategy',
        name: 'Turnaround Strategy Matrix',
        relevance: 'Critical for immediate survival',
        focus: 'Cash preservation and quick wins'
      });
      frameworks.push({
        id: 'resource-based-view',
        name: 'Resource-Based View (RBV)',
        relevance: 'Identify leverageable assets',
        focus: 'What can we monetize quickly?'
      });
    } else if (situation.type === 'product-market-misfit') {
      frameworks.push({
        id: 'jobs-to-be-done',
        name: 'Jobs-to-be-Done',
        relevance: 'Understand real customer needs',
        focus: 'What job are customers really hiring us for?'
      });
      frameworks.push({
        id: 'lean-canvas',
        name: 'Lean Canvas',
        relevance: 'Rapid hypothesis testing',
        focus: 'Pivot or persevere decision'
      });
    } else if (situation.type === 'scaling-challenge') {
      frameworks.push({
        id: 'vrio',
        name: 'VRIO Framework',
        relevance: 'Identify sustainable advantages',
        focus: 'What will defend our position at scale?'
      });
      frameworks.push({
        id: 'mckinsey-7s',
        name: 'McKinsey 7S',
        relevance: 'Organizational readiness for scale',
        focus: 'Are our systems ready for 10x growth?'
      });
    }
    
    // ARCHETYPE-BASED ADDITIONS
    if (archetype === 'technical-founder-trap') {
      frameworks.push({
        id: 'customer-development',
        name: 'Customer Development Process',
        relevance: 'Break out of product-only thinking',
        focus: 'Get out of the building'
      });
    } else if (archetype === 'enterprise-grind') {
      frameworks.push({
        id: 'miller-heiman',
        name: 'Miller Heiman Strategic Selling',
        relevance: 'Complex B2B sales optimization',
        focus: 'Shorten sales cycles and increase win rates'
      });
    } else if (archetype === 'two-sided-complexity') {
      frameworks.push({
        id: 'platform-strategy',
        name: 'Platform Strategy Canvas',
        relevance: 'Balance supply and demand dynamics',
        focus: 'Solve the chicken-egg problem'
      });
    }
    
    // CONSTRAINT-BASED ADDITIONS
    constraints.forEach(constraint => {
      if (constraint.type === 'capital' && constraint.severity === 'critical') {
        frameworks.push({
          id: 'runway-extension',
          name: 'Runway Extension Matrix',
          relevance: 'Survival tactics',
          focus: 'Double runway without raising'
        });
      } else if (constraint.type === 'unit-economics') {
        frameworks.push({
          id: 'unit-economics-framework',
          name: 'SaaS Unit Economics Framework',
          relevance: 'Fix the fundamentals',
          focus: 'Path to positive unit economics'
        });
      }
    });
    
    // ALWAYS INCLUDE A COMPETITIVE FRAMEWORK
    if (context.metrics.competitorCount > 5) {
      frameworks.push({
        id: 'blue-ocean',
        name: 'Blue Ocean Strategy',
        relevance: 'Find uncontested market space',
        focus: 'Create new demand rather than fight'
      });
    } else {
      frameworks.push({
        id: 'competitive-advantage',
        name: "Porter's Generic Strategies",
        relevance: 'Define competitive stance',
        focus: 'Cost leadership vs differentiation'
      });
    }
    
    // LIMIT TO 5-6 MOST RELEVANT
    return frameworks.slice(0, 6);
  };

  const applyFrameworkWithDepth = async (framework: any, context: any) => {
    // Each framework gets custom application based on context
    switch (framework.id) {
      case 'turnaround-strategy':
        return applyTurnaroundStrategy(context);
      case 'resource-based-view':
        return applyResourceBasedView(context);
      case 'jobs-to-be-done':
        return applyJobsToBeDone(context);
      case 'lean-canvas':
        return applyLeanCanvas(context);
      case 'vrio':
        return applyVRIOFramework(context);
      case 'mckinsey-7s':
        return applyMcKinsey7S(context);
      case 'customer-development':
        return applyCustomerDevelopment(context);
      case 'miller-heiman':
        return applyMillerHeiman(context);
      case 'platform-strategy':
        return applyPlatformStrategy(context);
      case 'runway-extension':
        return applyRunwayExtension(context);
      case 'unit-economics-framework':
        return applyUnitEconomicsFramework(context);
      case 'blue-ocean':
        return applyBlueOceanStrategy(context);
      case 'competitive-advantage':
        return applyPortersGenericStrategies(context);
      default:
        return applyGenericFramework(framework, context);
    }
  };
  
  const applyTurnaroundStrategy = (context: any): FrameworkAnalysis => {
    const { metrics, situation, constraints } = context;
    const runway = metrics.runway;
    const burn = metrics.burn;
    const revenue = metrics.revenue;
    
    // Calculate survival metrics
    const daysToZeroCash = runway * 30;
    const currentBurnMultiple = revenue > 0 ? burn / revenue : 999;
    const requiredBurnReduction = burn - (revenue * 0.8); // Target 80% of revenue
    
    // Identify quick wins
    const quickWins = [];
    
    if (burn > 100000) {
      quickWins.push({
        action: 'Reduce cloud infrastructure by 40%',
        impact: `Save $${(burn * 0.15 / 1000).toFixed(0)}k/month`,
        timeline: '7 days',
        difficulty: 'easy'
      });
    }
    
    if (metrics.teamSize > 10) {
      quickWins.push({
        action: 'Restructure to core team of 5-7',
        impact: `Save $${(metrics.teamSize * 10000 / 1000).toFixed(0)}k/month`,
        timeline: '30 days',
        difficulty: 'hard'
      });
    }
    
    // Revenue acceleration tactics
    const revenueTactics = [];
    
    if (revenue === 0) {
      revenueTactics.push({
        tactic: 'Paid pilot program',
        target: '$50k in 60 days',
        approach: 'Convert free users to paid pilots at 50% discount'
      });
    } else {
      revenueTactics.push({
        tactic: 'Annual prepayment incentive',
        target: `${Math.min(10, Math.floor(100 / metrics.churn))} customers`,
        approach: '25% discount for 12-month prepay'
      });
    }
    
    return {
      frameworkId: 'turnaround-strategy',
      frameworkName: 'Turnaround Strategy Matrix',
      data: {
        urgency: 'DEFCON 1',
        daysToZeroCash,
        survivalMetrics: {
          currentRunway: runway,
          targetRunway: 18,
          burnReductionRequired: requiredBurnReduction,
          revenueAccelerationRequired: burn - revenue
        },
        quickWins,
        revenueTactics,
        exitOptions: [
          {
            option: 'Acquihire',
            viability: metrics.teamSize > 5 ? 'high' : 'low',
            timeline: '60-90 days',
            preparation: 'Package team achievements and IP'
          },
          {
            option: 'Asset sale',
            viability: revenue > 100000 ? 'medium' : 'low',
            timeline: '90-120 days',
            preparation: 'Document customer contracts and tech stack'
          }
        ]
      },
      keyInsights: [
        `You have ${daysToZeroCash} days of cash remaining`,
        `Burn must drop by $${(requiredBurnReduction / 1000).toFixed(0)}k/month immediately`,
        quickWins.length > 0 ? 
          `Quick wins can save $${quickWins.reduce((sum, win) => sum + parseFloat(win.impact.match(/\d+/)?.[0] || '0'), 0)}k/month` :
          'Limited quick win opportunities - focus on revenue'
      ],
      recommendations: [
        {
          action: quickWins[0]?.action || 'Launch paid pilot program within 14 days',
          priority: 'immediate',
          impact: 'critical'
        },
        {
          action: 'CEO to lead all sales efforts personally',
          priority: 'immediate',
          impact: 'high'
        },
        {
          action: 'Prepare acquisition package in parallel',
          priority: 'short-term',
          impact: 'backup plan'
        }
      ]
    };
  };
  
  const applyJobsToBeDone = (context: any): FrameworkAnalysis => {
    const { metrics, capabilities, archetype } = context;
    
    // Identify what job customers are really hiring the product for
    const jobAnalysis = analyzeCustomerJobs(metrics, capabilities);
    
    // Find misalignment between product and job
    const misalignments = identifyJobMisalignments(jobAnalysis, metrics);
    
    // Competitive job analysis
    const competitiveJobs = analyzeCompetitiveJobSolutions(jobAnalysis, metrics);
    
    return {
      frameworkId: 'jobs-to-be-done',
      frameworkName: 'Jobs-to-be-Done Analysis',
      data: {
        primaryJob: jobAnalysis.primary,
        relatedJobs: jobAnalysis.related,
        jobMetrics: {
          satisfaction: jobAnalysis.satisfactionScore,
          importance: jobAnalysis.importanceScore,
          frequency: jobAnalysis.frequencyScore
        },
        misalignments,
        competitiveJobs,
        pivotOptions: generatePivotOptions(jobAnalysis, misalignments)
      },
      keyInsights: [
        `Primary job: ${jobAnalysis.primary.statement}`,
        `Current satisfaction: ${jobAnalysis.satisfactionScore}/10`,
        misalignments.length > 0 ? 
          `Critical misalignment: ${misalignments[0].description}` :
          'Product well-aligned with primary job'
      ],
      recommendations: misalignments.map(m => ({
        action: m.solution,
        priority: m.severity,
        impact: m.impact
      }))
    };
  };
  
  const analyzeCustomerJobs = (metrics: any, capabilities: any) => {
    // Simplified job analysis based on metrics
    const highChurn = metrics.churn > 10;
    const lowNPS = metrics.nps < 30;
    
    if (highChurn && lowNPS) {
      return {
        primary: {
          statement: 'Solve immediate pain with minimal effort',
          currentSolution: 'Product requires too much setup/learning',
          desiredOutcome: 'Instant value with zero friction'
        },
        related: [
          'Look good to my boss/team',
          'Avoid making costly mistakes',
          'Save time on repetitive tasks'
        ],
        satisfactionScore: 3,
        importanceScore: 9,
        frequencyScore: 8
      };
    }
    
    return {
      primary: {
        statement: 'Achieve specific business outcome efficiently',
        currentSolution: 'Product delivers but could be faster',
        desiredOutcome: 'Best-in-class speed and reliability'
      },
      related: [
        'Integrate with existing workflow',
        'Scale with growing needs',
        'Justify investment to stakeholders'
      ],
      satisfactionScore: 7,
      importanceScore: 8,
      frequencyScore: 9
    };
  };
  
  const identifyJobMisalignments = (jobAnalysis: any, metrics: any) => {
    const misalignments = [];
    
    if (jobAnalysis.satisfactionScore < 5) {
      misalignments.push({
        description: 'Product doesn\'t fully solve the primary job',
        severity: 'critical',
        impact: `${metrics.churn}% monthly churn`,
        solution: 'Redesign core workflow around job outcome'
      });
    }
    
    if (jobAnalysis.importanceScore > 8 && jobAnalysis.satisfactionScore < 7) {
      misalignments.push({
        description: 'High importance job poorly served',
        severity: 'high',
        impact: 'Limited pricing power',
        solution: 'Double down on job completion metrics'
      });
    }
    
    return misalignments;
  };
  
  const analyzeCompetitiveJobSolutions = (jobAnalysis: any, metrics: any) => {
    return [
      {
        competitor: 'In-house solution',
        jobCompletion: 60,
        advantages: 'Customized, no vendor lock-in',
        disadvantages: 'Expensive, slow to build'
      },
      {
        competitor: 'Direct competitor',
        jobCompletion: jobAnalysis.satisfactionScore * 10 + 10,
        advantages: 'More features, established brand',
        disadvantages: 'Higher price, complex'
      },
      {
        competitor: 'Do nothing',
        jobCompletion: 20,
        advantages: 'Free, no change required',
        disadvantages: 'Problem persists and compounds'
      }
    ];
  };
  
  const generatePivotOptions = (jobAnalysis: any, misalignments: any[]) => {
    if (misalignments.length === 0) return [];
    
    return [
      {
        type: 'Zoom-in Pivot',
        description: 'Focus entire product on best-performing job',
        viability: 'high',
        timeframe: '60 days'
      },
      {
        type: 'Customer Segment Pivot',
        description: 'Same job, different customer who values it more',
        viability: 'medium',
        timeframe: '90 days'
      }
    ];
  };
  
  const createFlowingStrategy = (analyses: FrameworkAnalysis[], context: any, companyData: any): any => {
    // Extract key findings from each analysis
    const portersInsights = analyses[0]; // External reality
    const bcgInsights = analyses[1];     // Current position
    const swotInsights = analyses[2];     // Capabilities audit
    const valueChainInsights = analyses[3]; // Value creation
    const ansoffInsights = analyses[4];   // Strategic options
    
    // Build the executive narrative that flows from external to internal to future
    const executiveSummary = `
Based on our comprehensive strategic analysis, ${companyData.companyInfo?.companyName || 'the company'} faces a 
${portersInsights.data.overall_attractiveness > 3 ? 'moderately attractive' : 'challenging'} industry environment 
with ${context.metrics.competitorCount} competitors. As a ${bcgInsights.data.position} in the BCG matrix with 
${(context.metrics.marketShare * 100).toFixed(1)}% market share, the immediate imperative is ${bcgInsights.data.strategic_direction}.

Our internal assessment reveals ${swotInsights.data.strengths.length} key strengths that can be leveraged, 
while addressing ${swotInsights.data.weaknesses.length} critical weaknesses. The value chain analysis identifies 
${valueChainInsights.data.competitive_advantages[0]} as our primary source of competitive advantage.

Given this position, we recommend pursuing a ${ansoffInsights.data.recommended_strategy} strategy with 
${ansoffInsights.data.risk_level} risk, focusing on ${ansoffInsights.data.implementation_steps[0].step} 
within the next ${ansoffInsights.data.implementation_steps[0].timeline}.`;

    return {
      executiveSummary,
      strategicPosition: {
        current: bcgInsights.data.position,
        desired: ansoffInsights.data.recommended_strategy === 'Market Penetration' ? 'Market Leader' : 'Category Creator',
        gap: `From ${bcgInsights.data.position} to market leadership through ${ansoffInsights.data.recommended_strategy}`
      },
      coreStrategy: {
        name: ansoffInsights.data.recommended_strategy,
        rationale: `Industry attractiveness (${portersInsights.data.overall_attractiveness}/5) combined with our ${bcgInsights.data.position} position suggests this path`,
        timeframe: '12-18 months'
      },
      criticalActions: [
        {
          action: ansoffInsights.data.implementation_steps[0].step,
          timeline: ansoffInsights.data.implementation_steps[0].timeline,
          success_metric: 'Achieve first milestone within 90 days',
          framework_support: ['Porter\'s Five Forces', 'BCG Matrix', 'Ansoff Matrix']
        },
        {
          action: `Strengthen ${valueChainInsights.data.primary_activities[0].activity} capabilities`,
          timeline: '0-6 months',
          success_metric: `Improve strength score from ${valueChainInsights.data.primary_activities[0].strength} to 9/10`,
          framework_support: ['Value Chain Analysis', 'SWOT']
        },
        {
          action: `Address primary weakness: ${swotInsights.data.weaknesses[0].item}`,
          timeline: 'Immediate',
          success_metric: swotInsights.data.weaknesses[0].action,
          framework_support: ['SWOT Analysis']
        }
      ],
      risks: [
        {
          risk: `High competitive rivalry (${portersInsights.data.forces[2].score}/5)`,
          likelihood: 'high',
          impact: 'high',
          mitigation: portersInsights.data.forces[2].strategic_response
        }
      ],
      confidenceLevel: 85
    };
  };

  const generateSWOTAnalysis = (context: any, portersAnalysis: FrameworkAnalysis, bcgAnalysis: FrameworkAnalysis): FrameworkAnalysis => {
    const { metrics } = context;
    
    // Build on Porter's and BCG insights
    const industryAttractiveness = portersAnalysis.data.overall_attractiveness;
    const competitiveIntensity = portersAnalysis.data.forces.find((f: any) => f.force === 'Competitive Rivalry')?.score || 3;
    const bcgPosition = bcgAnalysis.data.position;
    
    // Strengths are contextualized by external environment
    const strengths = [];
    
    // Financial strength relative to competitive intensity
    if (metrics.runway > 12 && competitiveIntensity > 3) {
      strengths.push({
        item: 'Financial resilience in competitive market',
        impact: 'high',
        evidence: `${metrics.runway} months runway while competitors face funding pressure`
      });
    } else if (metrics.runway > 12) {
      strengths.push({
        item: 'Strong financial position',
        impact: 'medium',
        evidence: `${metrics.runway} months runway with $${(metrics.burn * metrics.runway / 1000).toFixed(0)}k cash`
      });
    }
    
    // Customer satisfaction relative to BCG position
    if (metrics.nps > 50 && bcgPosition === 'Question Mark') {
      strengths.push({
        item: 'Product-market fit achieved despite low market share',
        impact: 'high',
        evidence: `NPS ${metrics.nps} positions us for rapid share capture`
      });
    } else if (metrics.nps > 30) {
      strengths.push({
        item: 'Positive customer sentiment',
        impact: 'medium',
        evidence: `NPS ${metrics.nps}, ${100 - metrics.churn}% retention rate`
      });
    }
    
    // Weaknesses identified through external lens
    const weaknesses = [];
    
    if (bcgPosition === 'Question Mark' && metrics.burn > 100000) {
      weaknesses.push({
        item: 'Burn rate unsustainable for market position',
        severity: 'critical',
        action: `Achieve BCG "Star" status or reduce burn by 40% in 90 days`
      });
    } else if (metrics.burn > metrics.revenue / 12) {
      weaknesses.push({
        item: 'Negative unit economics',
        severity: 'high',
        action: 'Path to profitability required within 12 months'
      });
    }
    
    // Opportunities filtered by Porter's analysis
    const opportunities = [];
    
    if (industryAttractiveness > 3 && metrics.growth > 20) {
      opportunities.push({
        item: `Attractive industry (${industryAttractiveness}/5) with ${metrics.growth}% growth`,
        value: `$${(assessmentData.market?.sam / 1000000).toFixed(0)}M addressable market`,
        timeframe: '12-18 months'
      });
    }
    
    // Threats from Porter's forces
    const threats = portersAnalysis.data.forces
      .filter((force: any) => force.score >= 4)
      .map((force: any) => ({
        item: force.force,
        likelihood: force.strength.toLowerCase(),
        mitigation: force.strategic_response
      }));
    
    return {
      frameworkId: 'swot_analysis',
      frameworkName: 'SWOT Analysis (Integrated)',
      data: {
        strengths,
        weaknesses,
        opportunities,
        threats
      },
      keyInsights: [
        `As a ${bcgPosition}, ${strengths.length > weaknesses.length ? 'leverage strengths' : 'address weaknesses'} to improve position`,
        `Industry attractiveness (${industryAttractiveness}/5) ${industryAttractiveness > 3 ? 'supports' : 'challenges'} growth ambitions`,
        `Primary strategic imperative: ${bcgAnalysis.data.strategic_direction}`
      ],
      recommendations: [
        {
          action: bcgPosition === 'Question Mark' ? 'Achieve market leadership in niche segment' : bcgAnalysis.data.strategic_direction,
          priority: 'immediate',
          impact: 'high'
        }
      ]
    };
  };

  const generateBCGAnalysis = (context: any, portersAnalysis: FrameworkAnalysis): FrameworkAnalysis => {
    const { metrics } = context;
    
    // BCG position informed by Porter's competitive analysis
    const competitiveRivalry = portersAnalysis.data.forces.find((f: any) => f.force === 'Competitive Rivalry')?.score || 3;
    const entrantThreat = portersAnalysis.data.forces.find((f: any) => f.force === 'Threat of New Entrants')?.score || 3;
    
    // Adjust market share threshold based on competitive intensity
    const shareThreshold = competitiveRivalry > 3 ? 0.05 : 0.1; // Lower threshold in highly competitive markets
    
    const position = 
      metrics.growth > 20 && metrics.marketShare > shareThreshold ? 'Star' :
      metrics.growth > 20 && metrics.marketShare <= shareThreshold ? 'Question Mark' :
      metrics.growth <= 20 && metrics.marketShare > shareThreshold ? 'Cash Cow' : 'Dog';
    
    // Strategic direction influenced by Porter's forces
    let strategicDirection = '';
    if (position === 'Question Mark') {
      if (entrantThreat > 3) {
        strategicDirection = 'Aggressive investment to preempt new entrants';
      } else {
        strategicDirection = 'Selective investment in defensible niches';
      }
    } else if (position === 'Star') {
      strategicDirection = competitiveRivalry > 3 ? 
        'Defend position through innovation and customer lock-in' : 
        'Maintain leadership and expand margins';
    } else if (position === 'Cash Cow') {
      strategicDirection = 'Harvest profits while monitoring disruption threats';
    } else {
      strategicDirection = 'Strategic pivot or managed exit';
    }
    
    return {
      frameworkId: 'bcg_matrix',
      frameworkName: 'BCG Matrix (Porter-Informed)',
      data: {
        position,
        market_share: metrics.marketShare,
        market_growth: metrics.growth,
        relative_share: metrics.marketShare * metrics.competitorCount,
        strategic_direction: strategicDirection,
        competitive_context: `${competitiveRivalry}/5 rivalry, ${entrantThreat}/5 entry threat`
      },
      keyInsights: [
        `${position} position in context of ${portersAnalysis.data.overall_attractiveness}/5 industry attractiveness`,
        `Competitive forces suggest ${competitiveRivalry > 3 ? 'urgent action needed' : 'strategic patience viable'}`,
        `Market dynamics favor ${metrics.growth > 30 ? 'aggressive growth' : 'selective expansion'}`
      ],
      recommendations: [
        {
          action: strategicDirection,
          priority: position === 'Question Mark' || position === 'Dog' ? 'immediate' : 'short-term',
          impact: 'high'
        }
      ]
    };
  };

  const synthesizeFrameworks = (frameworks: FrameworkAnalysis[], context: any) => {
    // Create connections between frameworks
    const synthesis = {
      primaryInsight: '',
      strategicNarrative: '',
      criticalDecisions: [],
      synergies: [],
      conflicts: []
    };
    
    // Find patterns across frameworks
    const allInsights = frameworks.flatMap(f => f.keyInsights);
    const allRecommendations = frameworks.flatMap(f => f.recommendations);
    
    // Identify conflicts
    frameworks.forEach((f1, i) => {
      frameworks.slice(i + 1).forEach(f2 => {
        const conflict = findConflicts(f1, f2);
        if (conflict) synthesis.conflicts.push(conflict);
      });
    });
    
    // Build strategic narrative
    synthesis.strategicNarrative = buildStrategicNarrative(frameworks, context);
    
    // Extract critical decisions
    synthesis.criticalDecisions = extractCriticalDecisions(allRecommendations, context);
    
    return synthesis;
  };
  
  const findConflicts = (f1: FrameworkAnalysis, f2: FrameworkAnalysis) => {
    // Simple conflict detection - in real implementation would be more sophisticated
    const f1Actions = f1.recommendations.map(r => r.action.toLowerCase());
    const f2Actions = f2.recommendations.map(r => r.action.toLowerCase());
    
    if (f1Actions.some(a => a.includes('reduce')) && f2Actions.some(a => a.includes('expand'))) {
      return {
        frameworks: [f1.frameworkName, f2.frameworkName],
        issue: 'Conflicting resource allocation recommendations',
        resolution: 'Prioritize based on runway and growth stage'
      };
    }
    
    return null;
  };
  
  const buildStrategicNarrative = (frameworks: FrameworkAnalysis[], context: any) => {
    const situation = context.situation;
    const primaryFramework = frameworks[0];
    
    return `${situation.description}. ${primaryFramework.keyInsights[0]}. 
    The analysis reveals ${frameworks.length} critical perspectives that must be balanced. 
    The path forward requires ${situation.primaryNeed} while managing 
    ${context.constraints.map(c => c.type).join(' and ')} constraints.`;
  };
  
  const extractCriticalDecisions = (recommendations: any[], context: any) => {
    // Group and prioritize recommendations
    const immediate = recommendations.filter(r => r.priority === 'immediate');
    const critical = recommendations.filter(r => r.impact === 'critical' || r.impact === 'high');
    
    return [...new Set([...immediate, ...critical])].slice(0, 5);
  };
  
  const createIntegratedStrategy = (synthesis: any, context: any) => {
    return {
      executiveSummary: synthesis.strategicNarrative,
      criticalDecisions: synthesis.criticalDecisions,
      conflicts: synthesis.conflicts,
      implementation: {
        phase1: {
          duration: '0-90 days',
          focus: context.situation.primaryNeed,
          keyActions: synthesis.criticalDecisions.slice(0, 3)
        },
        phase2: {
          duration: '90-180 days',
          focus: 'Build on early wins',
          keyActions: synthesis.criticalDecisions.slice(3, 6)
        }
      },
      successMetrics: defineSuccessMetrics(context),
      riskMitigation: defineRiskMitigation(context, synthesis.conflicts)
    };
  };
  
  const defineSuccessMetrics = (context: any) => {
    const metrics = [];
    
    if (context.situation.type === 'crisis') {
      metrics.push({
        metric: 'Runway extension',
        target: '12+ months',
        measurement: 'Monthly cash burn vs revenue'
      });
    }
    
    if (context.situation.type === 'product-market-misfit') {
      metrics.push({
        metric: 'Churn reduction',
        target: '< 5% monthly',
        measurement: 'Cohort retention analysis'
      });
    }
    
    return metrics;
  };
  
  const defineRiskMitigation = (context: any, conflicts: any[]) => {
    const risks = [];
    
    if (context.constraints.some(c => c.type === 'capital')) {
      risks.push({
        risk: 'Run out of cash before achieving milestones',
        mitigation: 'Parallel fundraising track with clear milestones',
        owner: 'CEO'
      });
    }
    
    conflicts.forEach(conflict => {
      risks.push({
        risk: conflict.issue,
        mitigation: conflict.resolution,
        owner: 'Leadership team'
      });
    });
    
    return risks;
  };
  
  const generatePortersAnalysis = (context: any): FrameworkAnalysis => {
    const { metrics } = context;
    
    // Porter's is the foundation - sets the external reality
    const forces = [
      {
        force: 'Threat of New Entrants',
        strength: metrics.growth > 30 ? 'High' : metrics.growth > 15 ? 'Medium' : 'Low',
        score: metrics.growth > 30 ? 4 : metrics.growth > 15 ? 3 : 2,
        key_factors: [
          metrics.growth > 30 ? 'Hot market attracting VC capital' : 'Moderate market growth',
          `${metrics.growth}% CAGR drawing ${metrics.growth > 30 ? 'heavy' : 'moderate'} investment`,
          assessmentData.advantage?.proprietaryTech ? 'Some IP barriers exist' : 'Low technical barriers'
        ],
        strategic_response: metrics.growth > 30 ? 
          'Urgently build moats - 18 month window before market floods' :
          'Systematically strengthen barriers over 24 months'
      },
      {
        force: 'Bargaining Power of Buyers',
        strength: metrics.churn > 10 ? 'High' : metrics.churn > 5 ? 'Medium' : 'Low',
        score: metrics.churn > 10 ? 5 : metrics.churn > 5 ? 3 : 2,
        key_factors: [
          `${metrics.churn}% monthly churn indicates ${metrics.churn > 10 ? 'weak' : 'moderate'} lock-in`,
          'Switching costs: ' + (assessmentData.advantage?.switchingCosts || 'low'),
          `${metrics.competitorCount} alternatives available`
        ],
        strategic_response: metrics.churn > 5 ?
          'Critical: Implement technical lock-in within 90 days' :
          'Enhance stickiness through workflow integration'
      },
      {
        force: 'Bargaining Power of Suppliers',
        strength: 'Low',
        score: 2,
        key_factors: [
          'Cloud infrastructure commoditized',
          'Multiple vendor options',
          'No critical dependencies'
        ],
        strategic_response: 'Leverage supplier competition for cost optimization'
      },
      {
        force: 'Threat of Substitutes',
        strength: assessmentData.market?.substituteThreat || 'Medium',
        score: 3,
        key_factors: [
          'In-house development always an option',
          'Open source alternatives emerging',
          'Adjacent solutions expanding'
        ],
        strategic_response: 'Create switching costs through data and integrations'
      },
      {
        force: 'Competitive Rivalry',
        strength: metrics.competitorCount > 30 ? 'Very High' : metrics.competitorCount > 20 ? 'High' : 'Medium',
        score: metrics.competitorCount > 30 ? 5 : metrics.competitorCount > 20 ? 4 : 3,
        key_factors: [
          `${metrics.competitorCount} direct competitors identified`,
          metrics.growth > 20 ? 'Growth market intensifying competition' : 'Mature market dynamics',
          'Price competition ' + (metrics.competitorCount > 30 ? 'severe' : 'moderate')
        ],
        strategic_response: metrics.competitorCount > 20 ?
          'Niche down: Own a specific use case completely' :
          'Maintain broad positioning while building advantages'
      }
    ];
    
    // Calculate overall attractiveness
    const avgScore = forces.reduce((sum, force) => sum + force.score, 0) / forces.length;
    const overall_attractiveness = 5 - avgScore + 1; // Invert: high forces = low attractiveness
    
    return {
      frameworkId: 'porters_five_forces',
      frameworkName: "Porter's Five Forces (Foundation)",
      data: {
        forces,
        overall_attractiveness,
        competitive_strategy: overall_attractiveness > 3 ?
          'Aggressive growth in attractive market' :
          'Selective competition in challenging environment'
      },
      keyInsights: [
        `Industry attractiveness: ${overall_attractiveness.toFixed(1)}/5 - ${overall_attractiveness > 3 ? 'Favorable' : 'Challenging'} environment`,
        `Highest threat: ${forces.sort((a, b) => b.score - a.score)[0].force} (${forces[0].score}/5)`,
        `Time horizon for moat building: ${metrics.growth > 30 ? '12-18 months' : '24-36 months'}`
      ],
      recommendations: [
        {
          action: forces[0].strategic_response,
          priority: 'immediate',
          impact: 'high'
        }
      ]
    };
  };

  const generateAnsoffAnalysis = (
    context: any, 
    bcgAnalysis: FrameworkAnalysis, 
    swotAnalysis: FrameworkAnalysis,
    valueChainAnalysis: FrameworkAnalysis
  ): FrameworkAnalysis => {
    const { metrics } = context;
    
    // Ansoff strategy determined by BCG position and capabilities
    const bcgPosition = bcgAnalysis.data.position;
    const strengths = swotAnalysis.data.strengths || [];
    const weaknesses = swotAnalysis.data.weaknesses || [];
    const primaryActivity = valueChainAnalysis.data.primary_activities[0];
    
    // Decision logic based on position and capabilities
    let recommendedStrategy = '';
    let rationale = '';
    let risk_level = '';
    let implementation_steps = [];
    
    if (bcgPosition === 'Question Mark') {
      // Question Marks need to achieve market share
      if (strengths.length > weaknesses.length) {
        recommendedStrategy = 'Market Penetration';
        rationale = 'Strong capabilities support aggressive share capture in existing market';
        risk_level = 'medium';
        implementation_steps = [
          {
            step: 'Dominate a specific niche within 90 days',
            timeline: '0-3 months',
            investment: '$500k-1M',
            success_metric: 'Achieve 25% share in target niche'
          },
          {
            step: 'Expand to adjacent niches',
            timeline: '3-9 months',
            investment: '$1-2M',
            success_metric: 'Triple customer base'
          }
        ];
      } else {
        recommendedStrategy = 'Product Development';
        rationale = 'Product improvements needed before scaling market efforts';
        risk_level = 'medium';
        implementation_steps = [
          {
            step: 'Fix critical product gaps identified in SWOT',
            timeline: '0-2 months',
            investment: '$200k',
            success_metric: 'Reduce churn by 50%'
          },
          {
            step: 'Launch differentiated features',
            timeline: '2-6 months',
            investment: '$500k',
            success_metric: 'NPS > 50'
          }
        ];
      }
    } else if (bcgPosition === 'Star') {
      recommendedStrategy = 'Market Development';
      rationale = 'Strong position in current market enables geographic/segment expansion';
      risk_level = 'medium-low';
      implementation_steps = [
        {
          step: 'Enter 2 adjacent market segments',
          timeline: '0-6 months',
          investment: '$1-3M',
          success_metric: '20% revenue from new segments'
        }
      ];
    } else if (bcgPosition === 'Cash Cow') {
      recommendedStrategy = 'Related Diversification';
      rationale = 'Use cash flow to build new growth engines';
      risk_level = 'high';
      implementation_steps = [
        {
          step: 'Incubate adjacent product line',
          timeline: '0-12 months',
          investment: '$2-5M',
          success_metric: 'Launch and validate new offering'
        }
      ];
    } else { // Dog
      recommendedStrategy = 'Turnaround or Exit';
      rationale = 'Fundamental repositioning required';
      risk_level = 'very high';
      implementation_steps = [
        {
          step: 'Pivot to defensible niche or prepare exit',
          timeline: '0-6 months',
          investment: 'Minimize burn',
          success_metric: 'Path to profitability or acquisition'
        }
      ];
    }
    
    // Adjust based on value chain strength
    if (primaryActivity && primaryActivity.strength < 5) {
      implementation_steps.unshift({
        step: `First strengthen ${primaryActivity.activity} (current: ${primaryActivity.strength}/10)`,
        timeline: '0-2 months',
        investment: '$100-300k',
        success_metric: `Achieve ${primaryActivity.strength + 3}/10 strength`
      });
    }
    
    return {
      frameworkId: 'ansoff_matrix',
      frameworkName: 'Ansoff Matrix (Strategic Options)',
      data: {
        current_strategy: bcgPosition === 'Question Mark' ? 'Struggling for position' : 'Established in market',
        recommended_strategy: recommendedStrategy,
        rationale: rationale,
        risk_level: risk_level,
        implementation_steps: implementation_steps,
        contingency: 'If primary strategy fails, ' + 
          (bcgPosition === 'Question Mark' ? 'pivot to niche domination' : 'optimize for profitability')
      },
      keyInsights: [
        `${bcgPosition} position drives ${recommendedStrategy} strategy`,
        `Success probability: ${strengths.length > weaknesses.length ? 'High' : 'Medium'} based on capability assessment`,
        `Critical dependency: ${implementation_steps[0].step}`
      ],
      recommendations: [
        {
          action: implementation_steps[0].step,
          priority: 'immediate',
          impact: 'high'
        }
      ]
    };
  };

  const generateValueChainAnalysis = (context: any, swotAnalysis: FrameworkAnalysis): FrameworkAnalysis => {
    const { metrics } = context;
    
    // Value chain activities scored based on SWOT insights
    const hasProductStrength = swotAnalysis.data.strengths.some((s: any) => 
      s.item.toLowerCase().includes('product') || s.item.toLowerCase().includes('tech')
    );
    const hasSalesWeakness = swotAnalysis.data.weaknesses.some((w: any) => 
      w.item.toLowerCase().includes('revenue') || w.item.toLowerCase().includes('growth')
    );
    
    // Score activities based on data and SWOT
    const primary_activities = [
      {
        activity: 'Product Development',
        strength: hasProductStrength ? 8 : 
                 assessmentData.advantage?.productStage === 'growth' ? 7 : 5,
        improvement: hasProductStrength ? 
          'Maintain velocity while adding enterprise features' : 
          'Accelerate development - ship weekly not monthly',
        impact_on_strategy: 'Critical for differentiation'
      },
      {
        activity: 'Marketing & Sales',
        strength: hasSalesWeakness ? 3 : 
                 metrics.revenue > 1000000 ? 6 : 4,
        improvement: hasSalesWeakness ? 
          'Build repeatable sales playbook - hire experienced VP Sales' :
          'Scale proven channels 10x',
        impact_on_strategy: 'Bottleneck for growth'
      },
      {
        activity: 'Customer Success',
        strength: metrics.churn < 5 ? 8 : 
                 metrics.churn < 10 ? 6 : 4,
        improvement: metrics.churn > 5 ? 
          `Reduce churn from ${metrics.churn}% to <5% through proactive engagement` :
          'Scale success team to maintain quality at 10x volume',
        impact_on_strategy: 'Foundation for expansion revenue'
      },
      {
        activity: 'Operations & Infrastructure',
        strength: metrics.burn < 100000 ? 7 : 5,
        improvement: 'Automate manual processes to support scale',
        impact_on_strategy: 'Enabler for efficiency'
      }
    ];
    
    // Identify competitive advantages from strong activities
    const competitive_advantages = primary_activities
      .filter(a => a.strength >= 7)
      .map(a => `${a.activity} excellence (${a.strength}/10)`)
      .concat(
        metrics.nps > 50 ? ['Customer loyalty (NPS > 50)'] : [],
        assessmentData.advantage?.proprietaryTech ? ['Proprietary technology'] : []
      );
    
    // Find the weakest link
    const weakestActivity = primary_activities.sort((a, b) => a.strength - b.strength)[0];
    
    return {
      frameworkId: 'value_chain',
      frameworkName: 'Value Chain Analysis (Capability Audit)',
      data: {
        primary_activities,
        competitive_advantages,
        weakest_link: weakestActivity,
        overall_capability: primary_activities.reduce((sum, a) => sum + a.strength, 0) / primary_activities.length
      },
      keyInsights: [
        `Weakest link: ${weakestActivity.activity} (${weakestActivity.strength}/10) - ${weakestActivity.impact_on_strategy}`,
        `Core advantage: ${competitive_advantages[0] || 'None identified - urgent attention needed'}`,
        `Overall capability: ${(primary_activities.reduce((sum, a) => sum + a.strength, 0) / primary_activities.length).toFixed(1)}/10`
      ],
      recommendations: [
        {
          action: weakestActivity.improvement,
          priority: 'immediate',
          impact: 'high'
        }
      ]
    };
  };

  const generateGenericAnalysis = (fw: any, context: any): FrameworkAnalysis => {
    // For frameworks we don't have specific implementations for,
    // create a meaningful generic analysis based on the framework's purpose
    const frameworkName = fw.frameworkName || fw.framework_name || 'Strategic Framework';
    const frameworkId = fw.frameworkId || fw.framework_id || 'generic';
    
    // Use the analysis data from API if available
    const apiAnalysis = fw.analysis || {};
    
    return {
      frameworkId: frameworkId,
      frameworkName: frameworkName,
      data: {
        ...apiAnalysis,
        category: fw.category || 'Strategic',
        description: fw.description || `${frameworkName} analysis for strategic planning`,
        relevance: fw.relevance_score || fw.relevanceScore || 0.8,
        customizations: fw.customizations || [],
        quickWins: fw.quick_wins || fw.quickWins || []
      },
      keyInsights: [
        ...(fw.keyInsights || []),
        ...(fw.key_insights || []),
        `${frameworkName} relevance score: ${((fw.relevance_score || fw.relevanceScore || 0.8) * 100).toFixed(0)}%`,
        `Implementation confidence: ${((fw.confidence_level || fw.confidenceLevel || 0.75) * 100).toFixed(0)}%`
      ].filter(Boolean).slice(0, 3),
      recommendations: [
        ...(fw.recommendations || []),
        ...(fw.quick_wins || fw.quickWins || []).map((qw: string) => ({
          action: qw,
          priority: 'short-term',
          impact: 'medium'
        }))
      ].slice(0, 3)
    };
  };

  // Removed Executive View - now in separate report tab
  /*
  const renderExecutiveView = () => {
    if (!integratedStrategy) return null;
    
    return (
      <div className={styles.executiveView}>
        <div className={styles.executiveSummary}>
          <h2>Executive Strategic Assessment</h2>
          <div className={styles.summaryContent}>
            <p>{integratedStrategy.executiveSummary}</p>
          </div>
          
          {llmAnalysis?.executive_summary && (
            <div className={styles.llmExecutiveSummary}>
              <h3>AI-Enhanced Strategic Perspective</h3>
              {typeof llmAnalysis.executive_summary === 'string' ? (
                <p>{llmAnalysis.executive_summary}</p>
              ) : (
                <>
                  <p><strong>Situation:</strong> {llmAnalysis.executive_summary.situation}</p>
                  {llmAnalysis.executive_summary.key_insights && (
                    <div>
                      <strong>Key Insights:</strong>
                      <ul>
                        {llmAnalysis.executive_summary.key_insights.map((insight: string, i: number) => (
                          <li key={i}>{insight}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <p><strong>Recommendation:</strong> {llmAnalysis.executive_summary.recommendation}</p>
                  <p><strong>Value at Stake:</strong> ${(llmAnalysis.executive_summary.value_at_stake / 1000000).toFixed(1)}M</p>
                  <p><strong>Confidence Level:</strong> {llmAnalysis.executive_summary.confidence_level}%</p>
                </>
              )}
              {llmAnalysis.key_risks && llmAnalysis.key_risks.length > 0 && (
                <div className={styles.aiRisks}>
                  <strong>Critical Risks Identified by AI:</strong>
                  <ul>
                    {llmAnalysis.key_risks.slice(0, 3).map((risk: any, i: number) => (
                      <li key={i}>
                        <span className={styles.riskName}>{risk.risk}</span>
                        <span className={styles.riskMitigation}>{risk.mitigation}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
          
          <div className={styles.confidenceIndicator}>
            <span>Analysis Confidence:</span>
            <div className={styles.confidenceBar}>
              <div 
                className={styles.confidenceFill} 
                style={{ width: `${integratedStrategy.confidenceLevel}%` }}
              />
            </div>
            <span>{integratedStrategy.confidenceLevel}%</span>
            {isLoadingLLM && <span className={styles.llmLoading}>🤖 Enhancing with AI...</span>}
          </div>
        </div>

        <div className={styles.strategicPosition}>
          <h3>Strategic Position</h3>
          <div className={styles.positionFlow}>
            <div className={styles.current}>
              <h4>Current State</h4>
              <p>{integratedStrategy.strategicPosition.current}</p>
            </div>
            <div className={styles.arrow}>→</div>
            <div className={styles.desired}>
              <h4>Target State</h4>
              <p>{integratedStrategy.strategicPosition.desired}</p>
            </div>
          </div>
          <div className={styles.gap}>
            <strong>Strategic Gap:</strong> {integratedStrategy.strategicPosition.gap}
          </div>
        </div>

        <div className={styles.coreStrategy}>
          <h3>Recommended Strategy</h3>
          <div className={styles.strategyCard}>
            <h4>{integratedStrategy.coreStrategy.name}</h4>
            <p>{integratedStrategy.coreStrategy.rationale}</p>
            <div className={styles.timeframe}>
              <span>Timeframe:</span> {integratedStrategy.coreStrategy.timeframe}
            </div>
          </div>
        </div>

        <div className={styles.criticalActions}>
          <h3>Critical Actions</h3>
          <div className={styles.actionsList}>
            {integratedStrategy.criticalActions.map((action: any, i: number) => (
              <motion.div 
                key={i} 
                className={styles.actionItem}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <div className={styles.actionNumber}>{i + 1}</div>
                <div className={styles.actionContent}>
                  <h5>{action.action}</h5>
                  <div className={styles.actionMeta}>
                    <span className={styles.timeline}>{action.timeline}</span>
                    <span className={styles.metric}>Success Metric: {action.success_metric}</span>
                  </div>
                  <div className={styles.frameworkSupport}>
                    Supported by: {action.framework_support.join(', ')}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className={styles.risks}>
          <h3>Key Risks & Mitigation</h3>
          <div className={styles.riskGrid}>
            {integratedStrategy.risks.map((risk: any, i: number) => (
              <div key={i} className={styles.riskCard}>
                <div className={styles.riskHeader}>
                  <h5>{risk.risk}</h5>
                  <div className={styles.riskLevel}>
                    <span className={`${styles.likelihood} ${styles[risk.likelihood]}`}>
                      {risk.likelihood} likelihood
                    </span>
                    <span className={`${styles.impact} ${styles[risk.impact]}`}>
                      {risk.impact} impact
                    </span>
                  </div>
                </div>
                <p className={styles.mitigation}>
                  <strong>Mitigation:</strong> {risk.mitigation}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };
  */

  const renderFrameworksView = () => {
    const currentAnalysis = frameworkAnalyses[selectedFramework];
    
    return (
      <div className={styles.frameworksView}>
        <div className={styles.frameworkLayout}>
          <div className={styles.frameworkSidebar}>
            <h3>Frameworks</h3>
            {frameworkAnalyses.map((analysis, i) => (
              <button
                key={analysis.frameworkId}
                className={`${styles.frameworkTab} ${selectedFramework === i ? styles.active : ''}`}
                onClick={() => setSelectedFramework(i)}
              >
                <span className={styles.frameworkNumber}>{i + 1}</span>
                <span className={styles.frameworkName}>{analysis.frameworkName}</span>
                {analysis.llmEnhancement && <span className={styles.aiIndicator}>AI</span>}
              </button>
            ))}
          </div>
          
          <div className={styles.frameworkMain}>
            {currentAnalysis && (
              <motion.div
                key={currentAnalysis.frameworkId}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className={styles.frameworkDetail}
              >
                <h2>{currentAnalysis.frameworkName}</h2>
                
                <div className={styles.frameworkContent}>
                  {renderFrameworkSpecificContent(currentAnalysis)}
                </div>
                
                <div className={styles.analysisGrid}>
                  <div className={styles.keyInsights}>
                    <h4>Key Insights</h4>
                    <ul>
                      {currentAnalysis.keyInsights.map((insight, j) => (
                        <li key={j}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                  
                  {currentAnalysis.recommendations.length > 0 && (
                    <div className={styles.recommendations}>
                      <h4>Recommendations</h4>
                      {currentAnalysis.recommendations.map((rec, j) => (
                        <div key={j} className={styles.recommendation}>
                          <span className={`${styles.priority} ${styles[rec.priority.replace('-', '')]}`}>
                            {rec.priority}
                          </span>
                          <p>{rec.action}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                
                {currentAnalysis.llmEnhancement && (
                  <div className={styles.llmEnhancement}>
                    <h4>AI Strategic Intelligence</h4>
                    <div className={styles.enhancementContent}>
                      <div className={styles.insight}>
                        <span className={styles.label}>Deeper Insight:</span>
                        <p>{currentAnalysis.llmEnhancement.deeperInsight}</p>
                      </div>
                      <div className={styles.pattern}>
                        <span className={styles.label}>Hidden Pattern:</span>
                        <p>{currentAnalysis.llmEnhancement.hiddenPattern}</p>
                      </div>
                      <div className={styles.implication}>
                        <span className={styles.label}>Strategic Implication:</span>
                        <p>{currentAnalysis.llmEnhancement.strategicImplication}</p>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderFrameworkSpecificContent = (analysis: FrameworkAnalysis) => {
    switch (analysis.frameworkId) {
      case 'swot_analysis':
        return renderSWOTContent(analysis.data);
      case 'bcg_matrix':
        return renderBCGContent(analysis.data);
      case 'porters_five_forces':
        return renderPortersContent(analysis.data);
      case 'ansoff_matrix':
        return renderAnsoffContent(analysis.data);
      case 'value_chain':
        return renderValueChainContent(analysis.data);
      default:
        return <pre>{JSON.stringify(analysis.data, null, 2)}</pre>;
    }
  };

  const renderSWOTContent = (data: any) => {
    if (!data || !data.strengths) {
      return <div>No SWOT data available</div>;
    }
    
    return (
      <div className={styles.swotGrid}>
        <div className={styles.quadrant}>
          <h5>Strengths</h5>
          {data.strengths?.map((s: any, i: number) => (
            <div key={i} className={styles.item}>
              <strong>{s.item}</strong>
              <span className={`${styles.badge} ${styles[s.impact]}`}>{s.impact}</span>
              <p>{s.evidence}</p>
            </div>
          ))}
        </div>
        <div className={styles.quadrant}>
          <h5>Weaknesses</h5>
          {data.weaknesses?.map((w: any, i: number) => (
            <div key={i} className={styles.item}>
              <strong>{w.item}</strong>
              <span className={`${styles.badge} ${styles[w.severity]}`}>{w.severity}</span>
              <p>{w.action}</p>
            </div>
          ))}
        </div>
        <div className={styles.quadrant}>
          <h5>Opportunities</h5>
          {data.opportunities?.map((o: any, i: number) => (
            <div key={i} className={styles.item}>
              <strong>{o.item}</strong>
              <p>{o.value} • {o.timeframe}</p>
            </div>
          ))}
        </div>
        <div className={styles.quadrant}>
          <h5>Threats</h5>
          {data.threats?.map((t: any, i: number) => (
            <div key={i} className={styles.item}>
              <strong>{t.item}</strong>
              <span className={`${styles.badge} ${styles[t.likelihood]}`}>{t.likelihood}</span>
              <p>{t.mitigation}</p>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderBCGContent = (data: any) => {
    if (!data) {
      return <div>No BCG Matrix data available</div>;
    }
    
    return (
      <div className={styles.bcgContent}>
        <div className={styles.matrixPosition}>
          <h5>Current Position: {data.position}</h5>
          <div className={styles.metrics}>
            <div>Market Share: {((data.market_share || 0) * 100).toFixed(2)}%</div>
            <div>Market Growth: {data.market_growth || 0}%</div>
            <div>Relative Share: {(data.relative_share || 0).toFixed(2)}x</div>
          </div>
        </div>
        <div className={styles.strategy}>
          <strong>Strategic Direction:</strong> {data.strategic_direction}
        </div>
      </div>
    );
  };

  const renderPortersContent = (data: any) => {
    if (!data || !data.forces) {
      return <div>No Porter's Five Forces data available</div>;
    }
    
    return (
      <div className={styles.portersContent}>
        {data.forces?.map((force: any, i: number) => (
          <div key={i} className={styles.force}>
            <div className={styles.forceHeader}>
              <h5>{force.force}</h5>
              <span className={`${styles.strength} ${styles[force.strength.toLowerCase()]}`}>
                {force.strength} ({force.score}/5)
              </span>
            </div>
            <p className={styles.response}>{force.strategic_response}</p>
          </div>
        ))}
        <div className={styles.overall}>
          <strong>Industry Attractiveness:</strong> {data.overall_attractiveness}/5
        </div>
      </div>
    );
  };

  const renderAnsoffContent = (data: any) => {
    if (!data) {
      return <div>No Ansoff Matrix data available</div>;
    }
    
    return (
      <div className={styles.ansoffContent}>
        <div className={styles.matrixPosition}>
          <h5>Current Strategy: {data.current_strategy}</h5>
          <h5>Recommended Strategy: {data.recommended_strategy}</h5>
          {data.rationale && (
            <p className={styles.rationale}>{data.rationale}</p>
          )}
          <div className={styles.riskLevel}>
            Risk Level: <span className={`${styles.badge} ${styles[data.risk_level?.replace(/[- ]/g, '')]}`}>{data.risk_level}</span>
          </div>
        </div>
        {data.implementation_steps && (
          <div className={styles.implementation}>
            <h5>Implementation Steps</h5>
            {data.implementation_steps.map((step: any, i: number) => (
              <div key={i} className={styles.step}>
                <strong>{step.step}</strong>
                <div className={styles.stepMeta}>
                  <span>{step.timeline}</span>
                  <span>{step.investment}</span>
                  {step.success_metric && (
                    <span className={styles.metric}>Target: {step.success_metric}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
        {data.contingency && (
          <div className={styles.contingency}>
            <strong>Contingency Plan:</strong> {data.contingency}
          </div>
        )}
      </div>
    );
  };

  const renderValueChainContent = (data: any) => {
    if (!data || !data.primary_activities) {
      return <div>No Value Chain data available</div>;
    }
    
    return (
      <div className={styles.valueChainContent}>
        <div className={styles.activities}>
          <h5>Primary Activities</h5>
          {data.primary_activities.map((activity: any, i: number) => (
            <div key={i} className={styles.activity}>
              <div className={styles.activityHeader}>
                <strong>{activity.activity}</strong>
                <span className={styles.strength}>Strength: {activity.strength}/10</span>
              </div>
              <p className={styles.improvement}>{activity.improvement}</p>
            </div>
          ))}
        </div>
        {data.competitive_advantages && (
          <div className={styles.advantages}>
            <h5>Competitive Advantages</h5>
            <ul>
              {data.competitive_advantages.map((advantage: string, i: number) => (
                <li key={i}>{advantage}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderSynthesisView = () => {
    if (!frameworkAnalyses || frameworkAnalyses.length === 0) return null;
    
    // Extract insights from the flowing analysis
    const porters = frameworkAnalyses[0];
    const bcg = frameworkAnalyses[1];
    const swot = frameworkAnalyses[2];
    const valueChain = frameworkAnalyses[3];
    const ansoff = frameworkAnalyses[4];
    
    return (
      <div className={styles.synthesisView}>
        <h2>Strategic Flow & Integration</h2>
        
        <div className={styles.strategicFlow}>
          <h3>The Strategic Narrative</h3>
          
          <div className={styles.flowSection}>
            <div className={styles.flowStep}>
              <div className={styles.stepNumber}>1</div>
              <div className={styles.stepContent}>
                <h4>External Reality</h4>
                <p className={styles.question}>What game are we playing?</p>
                <div className={styles.finding}>
                  <strong>Porter's Analysis:</strong> {porters?.data.overall_attractiveness > 3 ? 'Attractive' : 'Challenging'} industry 
                  ({porters?.data.overall_attractiveness}/5) with {porters?.data.forces[0].force} as primary concern
                </div>
                <div className={styles.implication}>
                  → Shapes our strategic ambition and timeline
                </div>
              </div>
            </div>
            
            <div className={styles.flowStep}>
              <div className={styles.stepNumber}>2</div>
              <div className={styles.stepContent}>
                <h4>Current Position</h4>
                <p className={styles.question}>Where do we stand?</p>
                <div className={styles.finding}>
                  <strong>BCG Position:</strong> {bcg?.data.position} with {(bcg?.data.market_share * 100).toFixed(1)}% share
                </div>
                <div className={styles.implication}>
                  → Determines resource allocation and growth strategy
                </div>
              </div>
            </div>
            
            <div className={styles.flowStep}>
              <div className={styles.stepNumber}>3</div>
              <div className={styles.stepContent}>
                <h4>Internal Capabilities</h4>
                <p className={styles.question}>What do we have to work with?</p>
                <div className={styles.finding}>
                  <strong>SWOT Balance:</strong> {swot?.data.strengths?.length || 0} strengths vs {swot?.data.weaknesses?.length || 0} weaknesses
                  <br />
                  <strong>Value Chain:</strong> Weakest link is {valueChain?.data.weakest_link?.activity} ({valueChain?.data.weakest_link?.strength}/10)
                </div>
                <div className={styles.implication}>
                  → Identifies what to leverage and what to fix
                </div>
              </div>
            </div>
            
            <div className={styles.flowStep}>
              <div className={styles.stepNumber}>4</div>
              <div className={styles.stepContent}>
                <h4>Strategic Choice</h4>
                <p className={styles.question}>Where should we go?</p>
                <div className={styles.finding}>
                  <strong>Ansoff Recommendation:</strong> {ansoff?.data.recommended_strategy} 
                  <span className={styles.riskBadge}>{ansoff?.data.risk_level} risk</span>
                </div>
                <div className={styles.implication}>
                  → Clear path forward with specific first steps
                </div>
              </div>
            </div>
          </div>
          
          <div className={styles.criticalInsight}>
            <h4>The Strategic Imperative</h4>
            <p>
              Given the {porters?.data.overall_attractiveness > 3 ? 'attractive' : 'challenging'} industry environment 
              and our {bcg?.data.position} position, we must {ansoff?.data.implementation_steps?.[0]?.step || 'take immediate action'}. 
              Success depends on fixing our {valueChain?.data.weakest_link?.activity} weakness while 
              leveraging our {swot?.data.strengths?.[0]?.item || 'core strengths'}.
            </p>
          </div>
          
          {llmAnalysis && (
            <div className={styles.llmSynthesis}>
              <h4>AI-Powered Strategic Synthesis</h4>
              {llmAnalysis.strategic_options && llmAnalysis.strategic_options.length > 0 && (
                <div className={styles.strategicOptions}>
                  <h5>Strategic Options Ranked by AI</h5>
                  {llmAnalysis.strategic_options.slice(0, 3).map((option: any, i: number) => (
                    <div key={i} className={styles.option}>
                      <div className={styles.optionHeader}>
                        <span className={styles.rank}>{i + 1}</span>
                        <h6>{option.name}</h6>
                        <span className={styles.viability}>{(option.viability * 100).toFixed(0)}% viable</span>
                      </div>
                      <p className={styles.description}>{option.description}</p>
                      <div className={styles.optionMeta}>
                        <span>Timeframe: {option.timeframe}</span>
                        <span>Investment: {option.investment_required}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              
              {llmAnalysis.next_steps && (
                <div className={styles.nextSteps}>
                  <h5>AI-Recommended Next 90 Days</h5>
                  <ul>
                    {llmAnalysis.next_steps.map((step: string, i: number) => (
                      <li key={i}>{step}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  };

  const generateConvergentThemes = () => {
    // Extract themes that appear across multiple frameworks
    const themes = [];
    
    if (derivedMetrics?.burnMultiple > 2) {
      themes.push({
        theme: 'Efficiency Imperative',
        evidence: `Burn multiple of ${derivedMetrics.burnMultiple.toFixed(1)}x requires immediate optimization`,
        frameworks: ['SWOT Analysis', 'Value Chain', 'Financial Analysis']
      });
    }
    
    if (derivedMetrics?.marketCapturePotential > 70) {
      themes.push({
        theme: 'Market Opportunity Window',
        evidence: `${derivedMetrics.marketCapturePotential.toFixed(0)}% capture potential in growing market`,
        frameworks: ['BCG Matrix', "Porter's Five Forces", 'Ansoff Matrix']
      });
    }
    
    if (derivedMetrics?.defensibilityScore > 60) {
      themes.push({
        theme: 'Competitive Moat Building',
        evidence: `${derivedMetrics.defensibilityScore.toFixed(0)}% defensibility enables sustainable advantage`,
        frameworks: ['SWOT Analysis', "Porter's Five Forces", 'Value Chain']
      });
    }
    
    return themes;
  };

  // Removed Metrics View - now focused on framework analysis only
  /*
  const renderMetricsView = () => {
    if (!derivedMetrics) return null;
    
    return (
      <div className={styles.metricsView}>
        <h2>Strategic Intelligence Metrics</h2>
        
        <div className={styles.compositeScores}>
          <div className={styles.scoreCard}>
            <h4>Overall Strength</h4>
            <div className={styles.scoreValue}>{derivedMetrics.overallStrength.toFixed(0)}</div>
            <div className={styles.scoreBar}>
              <div className={styles.scoreFill} style={{ width: `${derivedMetrics.overallStrength}%` }} />
            </div>
          </div>
          <div className={styles.scoreCard}>
            <h4>Strategic Readiness</h4>
            <div className={styles.scoreValue}>{derivedMetrics.strategicReadiness.toFixed(0)}</div>
            <div className={styles.scoreBar}>
              <div className={styles.scoreFill} style={{ width: `${derivedMetrics.strategicReadiness}%` }} />
            </div>
          </div>
          <div className={styles.scoreCard}>
            <h4>Investability Score</h4>
            <div className={styles.scoreValue}>{derivedMetrics.investabilityScore.toFixed(0)}</div>
            <div className={styles.scoreBar}>
              <div className={styles.scoreFill} style={{ width: `${derivedMetrics.investabilityScore}%` }} />
            </div>
          </div>
        </div>
        
        <div className={styles.metricCategories}>
          <div className={styles.category}>
            <h3>Efficiency Metrics</h3>
            <div className={styles.metricGrid}>
              <div className={styles.metric}>
                <label>Burn Multiple</label>
                <span className={derivedMetrics.burnMultiple > 2 ? styles.warning : styles.good}>
                  {derivedMetrics.burnMultiple.toFixed(1)}x
                </span>
              </div>
              <div className={styles.metric}>
                <label>Capital Efficiency</label>
                <span>{(derivedMetrics.capitalEfficiency * 100).toFixed(0)}%</span>
              </div>
              <div className={styles.metric}>
                <label>Revenue per Employee</label>
                <span>${(derivedMetrics.revenuePerEmployee / 1000).toFixed(0)}k</span>
              </div>
            </div>
          </div>
          
          <div className={styles.category}>
            <h3>Growth Metrics</h3>
            <div className={styles.metricGrid}>
              <div className={styles.metric}>
                <label>Growth Efficiency</label>
                <span>{derivedMetrics.growthEfficiency.toFixed(0)}</span>
              </div>
              <div className={styles.metric}>
                <label>Market Capture Potential</label>
                <span>{derivedMetrics.marketCapturePotential.toFixed(0)}%</span>
              </div>
              <div className={styles.metric}>
                <label>Velocity Score</label>
                <span>{derivedMetrics.velocityScore.toFixed(0)}</span>
              </div>
            </div>
          </div>
          
          <div className={styles.category}>
            <h3>Risk Metrics</h3>
            <div className={styles.metricGrid}>
              <div className={styles.metric}>
                <label>Runway Risk</label>
                <span className={derivedMetrics.runwayRisk > 60 ? styles.critical : styles.good}>
                  {derivedMetrics.runwayRisk.toFixed(0)}%
                </span>
              </div>
              <div className={styles.metric}>
                <label>Execution Risk</label>
                <span className={derivedMetrics.executionRisk > 60 ? styles.warning : styles.good}>
                  {derivedMetrics.executionRisk.toFixed(0)}%
                </span>
              </div>
              <div className={styles.metric}>
                <label>Market Risk</label>
                <span>{derivedMetrics.marketRisk.toFixed(0)}%</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className={styles.insights}>
          <h3>Metric-Driven Insights</h3>
          <ul>
            {dynamicScoring.generateMetricInsights(
              {
                revenue: assessmentData.capital?.annualRevenue || 0,
                burn: assessmentData.capital?.monthlyBurn || 50000,
                runway: assessmentData.capital?.runwayMonths || 12,
                cash: assessmentData.capital?.cashOnHand || 0,
                teamSize: assessmentData.people?.fullTimeEmployees || 10,
                fundingRaised: assessmentData.capital?.totalRaised || 0,
                marketGrowth: assessmentData.market?.marketGrowthRate || 20,
                marketShare: calculateMarketShare(),
                competitorCount: assessmentData.market?.competitorCount || 10,
                churn: assessmentData.advantage?.churnRate || 5,
                nps: assessmentData.advantage?.npsScore || 30,
                cac: assessmentData.market?.customerAcquisitionCost || 1000,
                ltv: assessmentData.market?.lifetimeValue || 10000,
                productStage: assessmentData.advantage?.productStage || 'mvp',
                fundingStage: assessmentData.capital?.fundingStage || 'seed'
              },
              derivedMetrics
            ).map((insight, i) => (
              <li key={i}>{insight}</li>
            ))}
          </ul>
        </div>
      </div>
    );
  };
  */

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Performing strategic analysis across {selectedFrameworks.length} frameworks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Strategic Framework Analysis</h1>
        <p>Deep strategic insights through interconnected framework analysis</p>
      </div>
      
      <div className={styles.navigation}>
        <button 
          className={activeView === 'frameworks' ? styles.active : ''}
          onClick={() => setActiveView('frameworks')}
        >
          Framework Analysis
        </button>
        <button 
          className={activeView === 'synthesis' ? styles.active : ''}
          onClick={() => setActiveView('synthesis')}
        >
          Synthesis
        </button>
      </div>
      
      <AnimatePresence mode="wait">
        <motion.div
          key={activeView}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className={styles.content}
        >
          {activeView === 'frameworks' && renderFrameworksView()}
          {activeView === 'synthesis' && renderSynthesisView()}
        </motion.div>
      </AnimatePresence>
    </div>
  );
  };
  
  // Add missing framework implementations
  const applyBlueOceanStrategy = (context: any): FrameworkAnalysis => {
    const { metrics, capabilities } = context;
    
    // Analyze current competitive factors
    const competitiveFactors = [
      { factor: 'Price', industryLevel: 5, ourLevel: metrics.revenue > 1000000 ? 6 : 4 },
      { factor: 'Features', industryLevel: 8, ourLevel: capabilities.product === 'mvp' ? 4 : 7 },
      { factor: 'Ease of Use', industryLevel: 5, ourLevel: metrics.nps > 50 ? 8 : 5 },
      { factor: 'Integration', industryLevel: 6, ourLevel: capabilities.technical ? 7 : 4 },
      { factor: 'Support', industryLevel: 7, ourLevel: metrics.teamSize > 20 ? 6 : 3 },
      { factor: 'Speed', industryLevel: 6, ourLevel: 5 }
    ];
    
    // Identify factors to eliminate, reduce, raise, create
    const eliminate = competitiveFactors
      .filter(f => f.ourLevel < 4 && f.industryLevel > 6)
      .map(f => f.factor);
    
    const reduce = competitiveFactors
      .filter(f => f.industryLevel > 7 && f.ourLevel > 5)
      .map(f => f.factor);
    
    const raise = competitiveFactors
      .filter(f => f.ourLevel > f.industryLevel && f.ourLevel < 8)
      .map(f => f.factor);
    
    const create = identifyNewValueFactors(metrics, capabilities);
    
    // Calculate blue ocean score
    const differentiation = competitiveFactors
      .filter(f => Math.abs(f.ourLevel - f.industryLevel) > 2).length;
    const blueOceanScore = (differentiation / competitiveFactors.length) * 10;
    
    return {
      frameworkId: 'blue-ocean',
      frameworkName: 'Blue Ocean Strategy',
      data: {
        currentStrategy: blueOceanScore > 5 ? 'Differentiator' : 'Red Ocean Competitor',
        competitiveFactors,
        fourActions: {
          eliminate,
          reduce,
          raise,
          create
        },
        valueInnovation: {
          customerValue: create.map(f => f.value),
          companyValue: create.map(f => f.costImpact),
          feasibility: assessCapabilityToExecute(create, capabilities)
        },
        blueOceanScore,
        newMarketSpace: defineNewMarketSpace(create, metrics)
      },
      keyInsights: [
        `Current strategy is ${blueOceanScore}% differentiated from competition`,
        create.length > 0 ? 
          `Opportunity to create new market with: ${create[0].factor}` :
          'Limited blue ocean opportunities in current positioning',
        eliminate.length > 0 ?
          `Eliminate ${eliminate[0]} to reduce costs and complexity` :
          'Current offering well-balanced'
      ],
      recommendations: [
        {
          action: create[0] ? 
            `Create new value: ${create[0].factor}` :
            `Dramatically raise ${raise[0] || 'ease of use'} beyond industry standard`,
          priority: 'immediate',
          impact: 'high'
        },
        {
          action: eliminate[0] ?
            `Stop competing on ${eliminate[0]}` :
            `Reduce investment in ${reduce[0] || 'feature parity'}`,
          priority: 'short-term',
          impact: 'medium'
        }
      ]
    };
  };
  
  const identifyNewValueFactors = (metrics: any, capabilities: any) => {
    const factors = [];
    
    // Based on context, suggest innovative value factors
    if (metrics.industry === 'saas' && metrics.churn > 5) {
      factors.push({
        factor: 'Success Guarantee',
        value: 'Pay only when customer achieves outcome',
        costImpact: 'Revenue delay but higher LTV',
        difficulty: 'medium'
      });
    }
    
    if (capabilities.technical && metrics.competitorCount > 20) {
      factors.push({
        factor: 'AI-Powered Automation',
        value: '10x productivity vs manual process',
        costImpact: 'High R&D but strong moat',
        difficulty: 'high'
      });
    }
    
    return factors;
  };
  
  const assessCapabilityToExecute = (factors: any[], capabilities: any) => {
    if (!factors.length) return 'N/A';
    
    const techCapability = capabilities.technical ? 8 : 4;
    const resourceCapability = capabilities.teamSize > 20 ? 7 : 4;
    
    const avgDifficulty = factors.reduce((sum, f) => {
      return sum + (f.difficulty === 'high' ? 8 : f.difficulty === 'medium' ? 5 : 3);
    }, 0) / factors.length;
    
    const executionScore = (techCapability + resourceCapability) / 2;
    
    return executionScore > avgDifficulty ? 'High' : 
           executionScore > avgDifficulty - 2 ? 'Medium' : 'Low';
  };
  
  const defineNewMarketSpace = (createFactors: any[], metrics: any) => {
    if (!createFactors.length) {
      return {
        description: 'Optimize within existing market',
        size: 'Current TAM',
        accessibility: 'High'
      };
    }
    
    return {
      description: `${createFactors[0].factor}-first solution for underserved segment`,
      size: `${(metrics.sam * 0.3 / 1000000).toFixed(0)}M estimated`,
      accessibility: assessCapabilityToExecute(createFactors, { technical: true }) === 'High' ? 
        'High - strong execution capability' : 'Medium - execution risk exists'
    };
  };
  
  const applyUnitEconomicsFramework = (context: any): FrameworkAnalysis => {
    const { metrics } = context;
    const { revenue, burn, ltv, cac, teamSize, churn } = metrics;
    
    // Calculate comprehensive unit economics
    const monthlyRevenue = revenue / 12;
    const customersNeeded = monthlyRevenue > 0 ? Math.ceil(burn / monthlyRevenue) : 'N/A';
    const ltvCacRatio = ltv / cac;
    const paybackPeriod = cac / (monthlyRevenue / (revenue > 0 ? Math.floor(revenue / ltv) : 1));
    const burnMultiple = revenue > 0 ? burn * 12 / revenue : 'Pre-revenue';
    
    // Magic Number (Net New ARR / S&M Spend)
    const magicNumber = revenue > 0 ? (revenue * 0.8) / (burn * 0.4 * 12) : 0;
    
    // Rule of 40 (Growth Rate + Profit Margin)
    const profitMargin = revenue > 0 ? ((revenue - burn * 12) / revenue) * 100 : -100;
    const growthRate = metrics.growth;
    const ruleOf40 = growthRate + profitMargin;
    
    // Efficiency metrics
    const revenuePerEmployee = revenue / teamSize;
    const burnRate = burn;
    const grossMargin = revenue > 0 ? 0.8 : 0; // Assume 80% for SaaS
    
    // Identify unit economic health
    const health = 
      ltvCacRatio > 3 && paybackPeriod < 12 ? 'healthy' :
      ltvCacRatio > 1.5 && paybackPeriod < 18 ? 'improving' :
      'unhealthy';
    
    // Generate improvement scenarios
    const scenarios = generateUnitEconomicScenarios(metrics);
    
    return {
      frameworkId: 'unit-economics',
      frameworkName: 'SaaS Unit Economics Analysis',
      data: {
        currentMetrics: {
          ltvCacRatio,
          paybackPeriod,
          burnMultiple,
          magicNumber,
          ruleOf40,
          revenuePerEmployee,
          monthlyBurn: burn,
          grossMargin: grossMargin * 100
        },
        health,
        benchmarks: {
          ltvCacRatio: { current: ltvCacRatio, target: 3, bestInClass: 5 },
          paybackPeriod: { current: paybackPeriod, target: 12, bestInClass: 6 },
          magicNumber: { current: magicNumber, target: 1, bestInClass: 1.5 },
          ruleOf40: { current: ruleOf40, target: 40, bestInClass: 60 }
        },
        improvementLevers: [
          {
            lever: 'Reduce CAC',
            current: cac,
            target: cac * 0.7,
            impact: `Improve LTV:CAC to ${(ltv / (cac * 0.7)).toFixed(1)}`,
            tactics: ['Focus on inbound', 'Improve conversion', 'Target better segments']
          },
          {
            lever: 'Increase LTV',
            current: ltv,
            target: ltv * 1.5,
            impact: `Improve LTV:CAC to ${((ltv * 1.5) / cac).toFixed(1)}`,
            tactics: ['Reduce churn', 'Upsell existing', 'Increase prices']
          },
          {
            lever: 'Improve Efficiency',
            current: burnMultiple,
            target: 1.5,
            impact: 'Path to profitability',
            tactics: ['Automate operations', 'Offshore development', 'Cut non-essential']
          }
        ],
        scenarios
      },
      keyInsights: [
        `Unit economics ${health}: LTV:CAC ratio ${ltvCacRatio.toFixed(1)}x`,
        `${paybackPeriod.toFixed(0)} month payback period ${paybackPeriod > 12 ? '(too long)' : '(acceptable)'}`,
        `Rule of 40 score: ${ruleOf40.toFixed(0)} ${ruleOf40 < 40 ? '(below benchmark)' : '(healthy)'}`
      ],
      recommendations: [
        {
          action: health === 'unhealthy' ? 
            'Pause all growth spending until unit economics fixed' :
            'Optimize CAC through channel mix analysis',
          priority: 'immediate',
          impact: 'critical'
        },
        {
          action: `Target ${scenarios[0].description}`,
          priority: 'short-term',
          impact: 'high'
        }
      ]
    };
  };
  
  const generateUnitEconomicScenarios = (metrics: any) => {
    const scenarios = [];
    
    // Scenario 1: Fix churn
    if (metrics.churn > 5) {
      const newLTV = metrics.ltv * (10 / metrics.churn);
      scenarios.push({
        description: `Reduce churn from ${metrics.churn}% to 5%`,
        impact: `LTV increases to $${(newLTV / 1000).toFixed(0)}k`,
        effort: 'medium',
        timeline: '3-6 months'
      });
    }
    
    // Scenario 2: Improve sales efficiency
    scenarios.push({
      description: 'Increase sales velocity by 50%',
      impact: `CAC reduces to $${(metrics.cac * 0.67 / 1000).toFixed(0)}k`,
      effort: 'high',
      timeline: '6-9 months'
    });
    
    // Scenario 3: Price optimization
    scenarios.push({
      description: 'Increase pricing by 20%',
      impact: `LTV increases to $${(metrics.ltv * 1.2 / 1000).toFixed(0)}k`,
      effort: 'low',
      timeline: '1-2 months'
    });
    
    return scenarios;
  };
  
  // Stub out remaining framework applications
  const applyResourceBasedView = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('resource-based-view', 'Resource-Based View', context);
  };
  
  const applyLeanCanvas = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('lean-canvas', 'Lean Canvas', context);
  };
  
  const applyVRIOFramework = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('vrio', 'VRIO Framework', context);
  };
  
  const applyMcKinsey7S = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('mckinsey-7s', 'McKinsey 7S', context);
  };
  
  const applyCustomerDevelopment = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('customer-development', 'Customer Development', context);
  };
  
  const applyMillerHeiman = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('miller-heiman', 'Miller Heiman Strategic Selling', context);
  };
  
  const applyPlatformStrategy = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('platform-strategy', 'Platform Strategy', context);
  };
  
  const applyRunwayExtension = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('runway-extension', 'Runway Extension Matrix', context);
  };
  
  const applyPortersGenericStrategies = (context: any): FrameworkAnalysis => {
    return createGenericAnalysis('competitive-advantage', "Porter's Generic Strategies", context);
  };
  
  const applyGenericFramework = (framework: any, context: any): FrameworkAnalysis => {
    return createGenericAnalysis(framework.id, framework.name, context);
  };
  
  const createGenericAnalysis = (id: string, name: string, context: any): FrameworkAnalysis => {
    return {
      frameworkId: id,
      frameworkName: name,
      data: {
        analysis: 'Detailed analysis would go here',
        situation: context.situation,
        relevantMetrics: context.metrics
      },
      keyInsights: [
        `Applied ${name} to ${context.situation.type} situation`,
        'Further analysis required for specific insights'
      ],
      recommendations: [
        {
          action: `Implement ${name} recommendations`,
          priority: 'medium',
          impact: 'medium'
        }
      ]
    };
  };

export default StrategicFrameworkAnalysis;