// Framework Intelligence Service - Manages 554 frameworks with intelligent selection
// This service acts as the brain for framework selection and application

interface FrameworkCategory {
  id: string;
  name: string;
  description: string;
  frameworks: string[];
}

interface FrameworkFamily {
  id: string;
  name: string;
  purpose: string;
  coreFrameworks: string[];
  relatedFrameworks: string[];
}

interface CompanyContext {
  stage: string;
  industry: string;
  primaryChallenge: string;
  metrics: {
    revenue: number;
    growth: number;
    burn: number;
    runway: number;
    marketShare: number;
    competitorCount: number;
    nps: number;
    churn: number;
  };
}

interface FrameworkRecommendation {
  frameworkId: string;
  frameworkName: string;
  relevanceScore: number;
  reason: string;
  category: string;
  synergyWith: string[];
}

export class FrameworkIntelligenceService {
  // Framework families for intelligent grouping
  private frameworkFamilies: FrameworkFamily[] = [
    {
      id: 'position-analysis',
      name: 'Position Analysis',
      purpose: 'Where are we now?',
      coreFrameworks: ['bcg_matrix', 'ge_mckinsey_matrix', 'adl_matrix'],
      relatedFrameworks: ['competitive_position_matrix', 'market_share_analysis']
    },
    {
      id: 'growth-strategy',
      name: 'Growth Strategy',
      purpose: 'Where should we go?',
      coreFrameworks: ['ansoff_matrix', 'product_market_fit', 'growth_share_matrix'],
      relatedFrameworks: ['market_expansion_framework', 'adjacent_growth']
    },
    {
      id: 'competitive-analysis',
      name: 'Competitive Analysis',
      purpose: 'How do we win?',
      coreFrameworks: ['porters_five_forces', 'vrio', 'resource_based_view'],
      relatedFrameworks: ['competitive_advantage_framework', 'blue_ocean_strategy']
    },
    {
      id: 'internal-assessment',
      name: 'Internal Assessment',
      purpose: 'What are our capabilities?',
      coreFrameworks: ['swot_analysis', 'value_chain', 'core_competencies'],
      relatedFrameworks: ['capability_maturity', 'organizational_dna']
    },
    {
      id: 'execution-frameworks',
      name: 'Execution Frameworks',
      purpose: 'How do we execute?',
      coreFrameworks: ['balanced_scorecard', 'okr', 'mckinsey_7s'],
      relatedFrameworks: ['strategy_map', 'hoshin_kanri']
    }
  ];

  // Core frameworks by company stage
  private stageFrameworks = {
    'pre-seed': ['lean_canvas', 'jobs_to_be_done', 'value_proposition_canvas', 'problem_solution_fit'],
    'seed': ['product_market_fit', 'swot_analysis', 'lean_startup', 'customer_development'],
    'series-a': ['swot_analysis', 'porters_five_forces', 'ansoff_matrix', 'unit_economics'],
    'series-b': ['bcg_matrix', 'value_chain', 'growth_share_matrix', 'market_expansion'],
    'series-c': ['mckinsey_7s', 'balanced_scorecard', 'blue_ocean_strategy', 'platform_strategy']
  };

  // Framework synergies (which frameworks work well together)
  private frameworkSynergies = {
    'swot_analysis': ['bcg_matrix', 'ansoff_matrix', 'porters_five_forces'],
    'bcg_matrix': ['ansoff_matrix', 'value_chain', 'porters_five_forces'],
    'porters_five_forces': ['value_chain', 'vrio', 'blue_ocean_strategy'],
    'ansoff_matrix': ['risk_matrix', 'capability_assessment', 'market_analysis'],
    'value_chain': ['vrio', 'core_competencies', 'activity_system_map']
  };

  /**
   * Intelligently select 5-8 frameworks from 554 based on company context
   */
  selectFrameworks(context: CompanyContext, maxFrameworks: number = 6): FrameworkRecommendation[] {
    const recommendations: FrameworkRecommendation[] = [];
    const scores: Map<string, number> = new Map();

    // 1. Score frameworks based on stage relevance
    this.scoreByStage(context.stage, scores);

    // 2. Score based on primary challenge
    this.scoreByChallenges(context, scores);

    // 3. Score based on data availability
    this.scoreByDataAvailability(context.metrics, scores);

    // 4. Apply synergy bonuses
    this.applySynergyBonuses(scores);

    // 5. Industry-specific adjustments
    this.adjustForIndustry(context.industry, scores);

    // 6. Select top frameworks with diversity
    return this.selectTopFrameworksWithDiversity(scores, maxFrameworks, context);
  }

  private scoreByStage(stage: string, scores: Map<string, number>): void {
    const stageFrameworks = this.stageFrameworks[stage] || this.stageFrameworks['seed'];
    
    stageFrameworks.forEach(framework => {
      scores.set(framework, (scores.get(framework) || 0) + 30);
    });

    // Add stage-appropriate analysis depth
    if (stage === 'pre-seed' || stage === 'seed') {
      scores.set('lean_canvas', (scores.get('lean_canvas') || 0) + 20);
      scores.set('problem_solution_fit', (scores.get('problem_solution_fit') || 0) + 15);
    } else if (stage === 'series-a' || stage === 'series-b') {
      scores.set('unit_economics', (scores.get('unit_economics') || 0) + 20);
      scores.set('cohort_analysis', (scores.get('cohort_analysis') || 0) + 15);
    }
  }

  private scoreByChallenges(context: CompanyContext, scores: Map<string, number>): void {
    const { metrics } = context;

    // High burn rate - need efficiency frameworks
    if (metrics.burn > metrics.revenue * 2) {
      scores.set('unit_economics', (scores.get('unit_economics') || 0) + 25);
      scores.set('value_chain', (scores.get('value_chain') || 0) + 20);
      scores.set('activity_based_costing', (scores.get('activity_based_costing') || 0) + 15);
    }

    // Low runway - need immediate action frameworks
    if (metrics.runway < 9) {
      scores.set('turnaround_strategy', (scores.get('turnaround_strategy') || 0) + 30);
      scores.set('cash_flow_management', (scores.get('cash_flow_management') || 0) + 25);
      scores.set('scenario_planning', (scores.get('scenario_planning') || 0) + 20);
    }

    // High competition - need differentiation frameworks
    if (metrics.competitorCount > 20) {
      scores.set('blue_ocean_strategy', (scores.get('blue_ocean_strategy') || 0) + 25);
      scores.set('differentiation_strategy', (scores.get('differentiation_strategy') || 0) + 20);
      scores.set('positioning_map', (scores.get('positioning_map') || 0) + 15);
    }

    // High churn - need retention frameworks
    if (metrics.churn > 5) {
      scores.set('customer_journey_map', (scores.get('customer_journey_map') || 0) + 25);
      scores.set('service_blueprint', (scores.get('service_blueprint') || 0) + 20);
      scores.set('nps_driver_analysis', (scores.get('nps_driver_analysis') || 0) + 15);
    }

    // Fast growth - need scaling frameworks
    if (metrics.growth > 100) {
      scores.set('scaling_framework', (scores.get('scaling_framework') || 0) + 25);
      scores.set('blitzscaling', (scores.get('blitzscaling') || 0) + 20);
      scores.set('growth_readiness', (scores.get('growth_readiness') || 0) + 15);
    }
  }

  private scoreByDataAvailability(metrics: any, scores: Map<string, number>): void {
    // If we have good financial data, enable financial frameworks
    if (metrics.revenue && metrics.burn && metrics.runway) {
      scores.set('financial_analysis', (scores.get('financial_analysis') || 0) + 10);
      scores.set('break_even_analysis', (scores.get('break_even_analysis') || 0) + 10);
    }

    // If we have market data, enable market frameworks
    if (metrics.marketShare && metrics.competitorCount) {
      scores.set('market_analysis', (scores.get('market_analysis') || 0) + 10);
      scores.set('competitive_analysis', (scores.get('competitive_analysis') || 0) + 10);
    }

    // Always boost fundamental frameworks
    scores.set('swot_analysis', (scores.get('swot_analysis') || 0) + 15);
    scores.set('porters_five_forces', (scores.get('porters_five_forces') || 0) + 10);
  }

  private applySynergyBonuses(scores: Map<string, number>): void {
    const currentFrameworks = Array.from(scores.keys());
    
    currentFrameworks.forEach(framework => {
      const synergies = this.frameworkSynergies[framework] || [];
      synergies.forEach(synergyFramework => {
        if (scores.has(synergyFramework)) {
          scores.set(synergyFramework, scores.get(synergyFramework)! + 5);
        }
      });
    });
  }

  private adjustForIndustry(industry: string, scores: Map<string, number>): void {
    const industryBoosts = {
      'saas': ['recurring_revenue_model', 'saas_metrics', 'rule_of_40'],
      'marketplace': ['network_effects', 'platform_strategy', 'two_sided_market'],
      'fintech': ['regulatory_analysis', 'risk_framework', 'compliance_matrix'],
      'healthtech': ['regulatory_analysis', 'stakeholder_map', 'clinical_validation'],
      'e-commerce': ['conversion_funnel', 'customer_acquisition', 'logistics_optimization'],
      'ai-ml': ['technology_readiness', 'ai_maturity', 'data_strategy']
    };

    const boosts = industryBoosts[industry] || [];
    boosts.forEach(framework => {
      scores.set(framework, (scores.get(framework) || 0) + 20);
    });
  }

  private selectTopFrameworksWithDiversity(
    scores: Map<string, number>, 
    maxFrameworks: number,
    context: CompanyContext
  ): FrameworkRecommendation[] {
    // Sort frameworks by score
    const sortedFrameworks = Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, maxFrameworks * 2); // Get more than we need for diversity

    const selected: FrameworkRecommendation[] = [];
    const selectedFamilies = new Set<string>();

    // Always include SWOT as baseline
    selected.push({
      frameworkId: 'swot_analysis',
      frameworkName: 'SWOT Analysis',
      relevanceScore: scores.get('swot_analysis') || 80,
      reason: 'Fundamental assessment of internal and external factors',
      category: 'internal-assessment',
      synergyWith: this.frameworkSynergies['swot_analysis'] || []
    });
    selectedFamilies.add('internal-assessment');

    // Select diverse frameworks
    for (const [framework, score] of sortedFrameworks) {
      if (selected.length >= maxFrameworks) break;
      if (framework === 'swot_analysis') continue;

      const family = this.getFrameworkFamily(framework);
      
      // Ensure diversity - don't pick too many from same family
      const familyCount = selected.filter(f => this.getFrameworkFamily(f.frameworkId) === family).length;
      if (familyCount < 2) {
        selected.push({
          frameworkId: framework,
          frameworkName: this.getFrameworkDisplayName(framework),
          relevanceScore: score,
          reason: this.getFrameworkReason(framework, context),
          category: family,
          synergyWith: this.frameworkSynergies[framework] || []
        });
      }
    }

    return selected;
  }

  private getFrameworkFamily(frameworkId: string): string {
    for (const family of this.frameworkFamilies) {
      if (family.coreFrameworks.includes(frameworkId) || 
          family.relatedFrameworks.includes(frameworkId)) {
        return family.id;
      }
    }
    return 'other';
  }

  private getFrameworkDisplayName(frameworkId: string): string {
    const nameMap = {
      'swot_analysis': 'SWOT Analysis',
      'bcg_matrix': 'BCG Growth-Share Matrix',
      'porters_five_forces': "Porter's Five Forces",
      'ansoff_matrix': 'Ansoff Growth Matrix',
      'value_chain': 'Value Chain Analysis',
      'lean_canvas': 'Lean Canvas',
      'jobs_to_be_done': 'Jobs to be Done',
      'product_market_fit': 'Product-Market Fit Canvas',
      'mckinsey_7s': 'McKinsey 7S Framework',
      'blue_ocean_strategy': 'Blue Ocean Strategy Canvas',
      'vrio': 'VRIO Framework',
      'balanced_scorecard': 'Balanced Scorecard',
      'unit_economics': 'Unit Economics Analysis'
    };
    
    return nameMap[frameworkId] || frameworkId.split('_').map(
      word => word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  }

  private getFrameworkReason(frameworkId: string, context: CompanyContext): string {
    const reasonMap = {
      'bcg_matrix': `With ${context.metrics.growth}% growth in a ${context.metrics.competitorCount}-player market, understanding your strategic position is critical`,
      'porters_five_forces': `${context.metrics.competitorCount} competitors and ${context.metrics.churn}% churn indicate need for competitive analysis`,
      'ansoff_matrix': `${context.metrics.runway} month runway requires clear growth strategy prioritization`,
      'value_chain': `Burn rate of $${context.metrics.burn} demands operational efficiency analysis`,
      'lean_canvas': `Early stage requires validation of problem-solution fit`,
      'unit_economics': `LTV/CAC and burn multiple analysis critical for sustainable growth`
    };
    
    return reasonMap[frameworkId] || `Relevant for ${context.stage} stage ${context.industry} companies`;
  }

  /**
   * Get framework combinations that work well together
   */
  getFrameworkSynergies(selectedFrameworks: string[]): Array<{
    framework1: string;
    framework2: string;
    synergyType: string;
    insight: string;
  }> {
    const synergies = [];
    
    for (let i = 0; i < selectedFrameworks.length; i++) {
      for (let j = i + 1; j < selectedFrameworks.length; j++) {
        const synergy = this.identifySynergy(selectedFrameworks[i], selectedFrameworks[j]);
        if (synergy) {
          synergies.push(synergy);
        }
      }
    }
    
    return synergies;
  }

  private identifySynergy(framework1: string, framework2: string): any {
    const synergyPatterns = {
      'swot_bcg': {
        condition: (f1: string, f2: string) => 
          (f1 === 'swot_analysis' && f2 === 'bcg_matrix') || 
          (f1 === 'bcg_matrix' && f2 === 'swot_analysis'),
        synergyType: 'Position Validation',
        insight: 'SWOT strengths/weaknesses explain BCG position; opportunities guide quadrant movement strategy'
      },
      'porter_ansoff': {
        condition: (f1: string, f2: string) => 
          (f1 === 'porters_five_forces' && f2 === 'ansoff_matrix') || 
          (f1 === 'ansoff_matrix' && f2 === 'porters_five_forces'),
        synergyType: 'Strategic Direction',
        insight: 'Industry forces determine viable growth strategies; high rivalry suggests product development over market development'
      },
      'value_chain_competitive': {
        condition: (f1: string, f2: string) => 
          (f1 === 'value_chain' && (f2.includes('competitive') || f2.includes('porter'))) ||
          ((f1.includes('competitive') || f1.includes('porter')) && f2 === 'value_chain'),
        synergyType: 'Competitive Advantage Source',
        insight: 'Value chain activities create competitive advantages; strong links defend against five forces'
      }
    };

    for (const [key, pattern] of Object.entries(synergyPatterns)) {
      if (pattern.condition(framework1, framework2)) {
        return {
          framework1: this.getFrameworkDisplayName(framework1),
          framework2: this.getFrameworkDisplayName(framework2),
          synergyType: pattern.synergyType,
          insight: pattern.insight
        };
      }
    }
    
    return null;
  }
}

// Export singleton instance
export const frameworkIntelligence = new FrameworkIntelligenceService();