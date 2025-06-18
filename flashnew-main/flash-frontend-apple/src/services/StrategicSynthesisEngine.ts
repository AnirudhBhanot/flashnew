// Strategic Synthesis Engine - The brain that connects insights across frameworks
// This is where 1+1=5 happens in strategic analysis

import { frameworkIntelligence } from './FrameworkIntelligenceService';

interface FrameworkOutput {
  frameworkId: string;
  frameworkName: string;
  data: any;
  keyInsights: string[];
  recommendations: Array<{
    action: string;
    priority: string;
    impact: string;
  }>;
}

interface CrossFrameworkPattern {
  pattern: string;
  confidence: number;
  evidence: string[];
  implication: string;
  action: string;
}

interface StrategicCoherence {
  coherenceScore: number; // 0-100
  alignments: string[];
  conflicts: string[];
  resolution: string;
}

interface IntegratedStrategy {
  executiveSummary: string;
  strategicPosition: {
    current: string;
    desired: string;
    gap: string;
  };
  coreStrategy: {
    name: string;
    rationale: string;
    timeframe: string;
  };
  criticalActions: Array<{
    action: string;
    framework_support: string[];
    timeline: string;
    success_metric: string;
  }>;
  risks: Array<{
    risk: string;
    likelihood: 'high' | 'medium' | 'low';
    impact: 'high' | 'medium' | 'low';
    mitigation: string;
  }>;
  confidenceLevel: number;
}

export class StrategicSynthesisEngine {
  /**
   * Main synthesis function - turns multiple framework outputs into integrated strategy
   */
  synthesize(frameworkOutputs: FrameworkOutput[], companyData: any): IntegratedStrategy {
    // 1. Detect cross-framework patterns
    const patterns = this.detectCrossFrameworkPatterns(frameworkOutputs);
    
    // 2. Check strategic coherence
    const coherence = this.assessStrategicCoherence(frameworkOutputs);
    
    // 3. Identify strategic position
    const position = this.identifyStrategicPosition(frameworkOutputs, companyData);
    
    // 4. Determine core strategy
    const coreStrategy = this.determineCoreStrategy(patterns, position, companyData);
    
    // 5. Extract critical actions with framework support
    const criticalActions = this.extractCriticalActions(frameworkOutputs, coreStrategy);
    
    // 6. Identify and prioritize risks
    const risks = this.identifyIntegratedRisks(frameworkOutputs, patterns);
    
    // 7. Generate executive summary
    const executiveSummary = this.generateExecutiveSummary(
      position, coreStrategy, criticalActions, risks, companyData
    );
    
    return {
      executiveSummary,
      strategicPosition: position,
      coreStrategy,
      criticalActions: criticalActions.slice(0, 5), // Top 5 actions
      risks: risks.slice(0, 3), // Top 3 risks
      confidenceLevel: this.calculateConfidenceLevel(coherence, patterns)
    };
  }

  /**
   * Detect patterns across multiple frameworks
   */
  private detectCrossFrameworkPatterns(outputs: FrameworkOutput[]): CrossFrameworkPattern[] {
    const patterns: CrossFrameworkPattern[] = [];
    
    // Pattern 1: Market Position vs Capabilities
    const swot = outputs.find(o => o.frameworkId === 'swot_analysis');
    const bcg = outputs.find(o => o.frameworkId === 'bcg_matrix');
    
    if (swot && bcg) {
      const strongCapabilities = swot.data.strengths?.length > swot.data.weaknesses?.length;
      const questionMark = bcg.data.position === 'Question Mark';
      
      if (strongCapabilities && questionMark) {
        patterns.push({
          pattern: 'High Potential Challenger',
          confidence: 85,
          evidence: [
            'Strong internal capabilities (SWOT)',
            'Question Mark position indicates growth market (BCG)',
            'Favorable conditions for market share capture'
          ],
          implication: 'Company has capabilities to become market leader',
          action: 'Aggressive market penetration with 18-month timeline'
        });
      }
    }
    
    // Pattern 2: Competitive Dynamics vs Growth Strategy
    const porters = outputs.find(o => o.frameworkId === 'porters_five_forces');
    const ansoff = outputs.find(o => o.frameworkId === 'ansoff_matrix');
    
    if (porters && ansoff) {
      const highRivalry = porters.data.forces?.find(f => f.force.includes('Rivalry'))?.score > 3;
      const marketPenetration = ansoff.data.current_strategy === 'Market Penetration';
      
      if (highRivalry && marketPenetration) {
        patterns.push({
          pattern: 'Red Ocean Trap',
          confidence: 75,
          evidence: [
            'High competitive rivalry (Porter\'s)',
            'Focus on market penetration in crowded market (Ansoff)',
            'Risk of commoditization'
          ],
          implication: 'Current strategy leads to margin erosion',
          action: 'Pivot to product development or new market segments'
        });
      }
    }
    
    // Pattern 3: Value Chain vs Competitive Advantage
    const valueChain = outputs.find(o => o.frameworkId === 'value_chain');
    
    if (valueChain && swot) {
      const techStrength = valueChain.data.primary_activities?.find(
        a => a.activity.includes('Technology') || a.activity.includes('Product')
      )?.strength > 7;
      
      const marketWeakness = swot.data.weaknesses?.some(
        w => w.item.includes('market') || w.item.includes('sales')
      );
      
      if (techStrength && marketWeakness) {
        patterns.push({
          pattern: 'Technical Excellence, Commercial Gap',
          confidence: 80,
          evidence: [
            'Strong technology/product capabilities (Value Chain)',
            'Weak market presence (SWOT)',
            'Classic technical founder syndrome'
          ],
          implication: 'Great product struggling to find market',
          action: 'Hire commercial leadership and build go-to-market engine'
        });
      }
    }
    
    // Pattern 4: Financial Health vs Strategic Options
    const financialStrength = this.assessFinancialStrength(outputs);
    const growthAmbition = this.assessGrowthAmbition(outputs);
    
    if (financialStrength < 0.4 && growthAmbition > 0.7) {
      patterns.push({
        pattern: 'Ambition-Resource Mismatch',
        confidence: 90,
        evidence: [
          'Limited runway and high burn rate',
          'Aggressive growth strategies recommended',
          'Insufficient resources for execution'
        ],
        implication: 'Strategy-resource gap threatens viability',
        action: 'Either raise capital immediately or pivot to efficiency'
      });
    }
    
    return patterns;
  }

  /**
   * Assess strategic coherence across frameworks
   */
  private assessStrategicCoherence(outputs: FrameworkOutput[]): StrategicCoherence {
    const alignments: string[] = [];
    const conflicts: string[] = [];
    
    // Check if all frameworks point to same direction
    const growthSignals = outputs.filter(o => 
      o.keyInsights.some(i => i.includes('growth') || i.includes('expand'))
    ).length;
    
    const efficiencySignals = outputs.filter(o => 
      o.keyInsights.some(i => i.includes('efficiency') || i.includes('cost'))
    ).length;
    
    if (growthSignals > outputs.length * 0.7) {
      alignments.push('Strong consensus on growth strategy across frameworks');
    }
    
    if (efficiencySignals > outputs.length * 0.7) {
      alignments.push('Clear need for operational efficiency across analyses');
    }
    
    // Detect conflicts
    if (growthSignals > 2 && efficiencySignals > 2) {
      conflicts.push('Frameworks disagree on growth vs efficiency priority');
    }
    
    // Check timeline conflicts
    const shortTermActions = outputs.flatMap(o => 
      o.recommendations.filter(r => r.priority === 'immediate')
    ).length;
    
    if (shortTermActions > 10) {
      conflicts.push('Too many immediate priorities - need focus');
    }
    
    // Calculate coherence score
    const coherenceScore = Math.max(0, Math.min(100, 
      100 - (conflicts.length * 20) + (alignments.length * 15)
    ));
    
    const resolution = conflicts.length > 0
      ? 'Prioritize based on runway: efficiency first if <9 months, growth if >12 months'
      : 'Strong strategic alignment enables aggressive execution';
    
    return { coherenceScore, alignments, conflicts, resolution };
  }

  /**
   * Identify strategic position by synthesizing framework outputs
   */
  private identifyStrategicPosition(outputs: FrameworkOutput[], companyData: any): any {
    const swot = outputs.find(o => o.frameworkId === 'swot_analysis');
    const bcg = outputs.find(o => o.frameworkId === 'bcg_matrix');
    const porters = outputs.find(o => o.frameworkId === 'porters_five_forces');
    
    // Current position
    let current = 'Emerging player';
    if (bcg?.data.position) {
      const positionMap = {
        'Star': 'Market leader in high-growth segment',
        'Question Mark': 'High-potential challenger in growth market',
        'Cash Cow': 'Established player in mature market',
        'Dog': 'Struggling position requiring pivot'
      };
      current = positionMap[bcg.data.position] || current;
    }
    
    // Add nuance from other frameworks
    if (swot?.data.strengths?.length > swot?.data.weaknesses?.length) {
      current += ' with strong internal capabilities';
    }
    
    if (porters?.data.overall_attractiveness > 3) {
      current += ' in attractive industry';
    }
    
    // Desired position (based on opportunities and recommendations)
    const opportunities = outputs.flatMap(o => o.data.opportunities || []);
    const hasMarketOpportunity = opportunities.some(o => 
      o.value?.includes('B') || o.value?.includes('TAM')
    );
    
    const desired = hasMarketOpportunity
      ? 'Category leader capturing significant market share'
      : 'Profitable niche player with sustainable advantages';
    
    // Gap analysis
    const gap = this.calculateStrategicGap(current, desired, outputs);
    
    return { current, desired, gap };
  }

  /**
   * Determine core strategy based on patterns and position
   */
  private determineCoreStrategy(
    patterns: CrossFrameworkPattern[], 
    position: any, 
    companyData: any
  ): any {
    // Strategy selection logic based on patterns
    if (patterns.some(p => p.pattern === 'High Potential Challenger')) {
      return {
        name: 'Aggressive Market Capture',
        rationale: 'Strong capabilities + growth market = window of opportunity',
        timeframe: '18-24 months'
      };
    }
    
    if (patterns.some(p => p.pattern === 'Red Ocean Trap')) {
      return {
        name: 'Blue Ocean Pivot',
        rationale: 'Escape commoditization through innovation or new markets',
        timeframe: '12-18 months'
      };
    }
    
    if (patterns.some(p => p.pattern === 'Technical Excellence, Commercial Gap')) {
      return {
        name: 'Commercial Transformation',
        rationale: 'Unlock product value through go-to-market excellence',
        timeframe: '9-12 months'
      };
    }
    
    if (patterns.some(p => p.pattern === 'Ambition-Resource Mismatch')) {
      return {
        name: 'Efficient Growth',
        rationale: 'Balance growth ambitions with capital efficiency',
        timeframe: '6-9 months to profitability'
      };
    }
    
    // Default strategy based on stage
    if (companyData.capital?.fundingStage === 'seed') {
      return {
        name: 'Product-Market Fit Sprint',
        rationale: 'Focus on validation before scaling',
        timeframe: '6-9 months'
      };
    }
    
    return {
      name: 'Sustainable Growth',
      rationale: 'Balanced approach to growth and efficiency',
      timeframe: '12-24 months'
    };
  }

  /**
   * Extract critical actions with multi-framework support
   */
  private extractCriticalActions(outputs: FrameworkOutput[], coreStrategy: any): any[] {
    const allActions = outputs.flatMap(o => 
      o.recommendations.map(rec => ({
        ...rec,
        framework: o.frameworkName
      }))
    );
    
    // Group similar actions
    const actionGroups = new Map<string, any[]>();
    
    allActions.forEach(action => {
      const key = this.normalizeAction(action.action);
      if (!actionGroups.has(key)) {
        actionGroups.set(key, []);
      }
      actionGroups.get(key)!.push(action);
    });
    
    // Score actions based on multi-framework support
    const scoredActions = Array.from(actionGroups.entries()).map(([key, actions]) => {
      const frameworks = [...new Set(actions.map(a => a.framework))];
      const avgPriority = this.calculatePriorityScore(actions);
      const avgImpact = this.calculateImpactScore(actions);
      const strategicAlignment = this.assessStrategicAlignment(key, coreStrategy);
      
      const score = (frameworks.length * 30) + (avgPriority * 25) + 
                    (avgImpact * 25) + (strategicAlignment * 20);
      
      return {
        action: this.refineActionDescription(key, actions[0].action),
        framework_support: frameworks,
        timeline: this.determineTimeline(actions),
        success_metric: this.generateSuccessMetric(key),
        score
      };
    });
    
    // Sort by score and return top actions
    return scoredActions
      .sort((a, b) => b.score - a.score)
      .map(({ score, ...action }) => action);
  }

  /**
   * Identify integrated risks across frameworks
   */
  private identifyIntegratedRisks(
    outputs: FrameworkOutput[], 
    patterns: CrossFrameworkPattern[]
  ): any[] {
    const risks = [];
    
    // Extract risks from SWOT threats
    const swot = outputs.find(o => o.frameworkId === 'swot_analysis');
    if (swot?.data.threats) {
      swot.data.threats.forEach(threat => {
        risks.push({
          risk: threat.item,
          likelihood: threat.likelihood || 'medium',
          impact: 'high',
          mitigation: threat.mitigation,
          source: 'SWOT Analysis'
        });
      });
    }
    
    // Extract risks from Porter's high forces
    const porters = outputs.find(o => o.frameworkId === 'porters_five_forces');
    if (porters?.data.forces) {
      porters.data.forces
        .filter(force => force.score >= 4)
        .forEach(force => {
          risks.push({
            risk: `High ${force.force}`,
            likelihood: 'high',
            impact: force.score === 5 ? 'high' : 'medium',
            mitigation: force.strategic_response,
            source: "Porter's Five Forces"
          });
        });
    }
    
    // Add pattern-based risks
    patterns
      .filter(p => p.pattern.includes('Trap') || p.pattern.includes('Mismatch'))
      .forEach(pattern => {
        risks.push({
          risk: pattern.implication,
          likelihood: pattern.confidence > 80 ? 'high' : 'medium',
          impact: 'high',
          mitigation: pattern.action,
          source: 'Cross-Framework Analysis'
        });
      });
    
    // Score and prioritize risks
    return risks
      .map(risk => ({
        ...risk,
        score: this.calculateRiskScore(risk.likelihood, risk.impact)
      }))
      .sort((a, b) => b.score - a.score)
      .map(({ source, score, ...risk }) => risk);
  }

  /**
   * Generate executive summary narrative
   */
  private generateExecutiveSummary(
    position: any,
    coreStrategy: any,
    actions: any[],
    risks: any[],
    companyData: any
  ): string {
    const company = companyData.companyInfo?.companyName || 'The company';
    const runway = companyData.capital?.runwayMonths || 12;
    const stage = companyData.capital?.fundingStage || 'growth';
    
    const summary = `${company} is currently positioned as a ${position.current}. ` +
      `Our integrated analysis across multiple strategic frameworks reveals a clear path to ${position.desired}. ` +
      `\n\n` +
      `The recommended strategy is "${coreStrategy.name}" based on ${coreStrategy.rationale}. ` +
      `With ${runway} months of runway, the ${coreStrategy.timeframe} timeline aligns with financial constraints while maximizing opportunity capture. ` +
      `\n\n` +
      `Critical success factors include ${actions.slice(0, 3).map(a => a.action).join(', ')}. ` +
      `The primary risk is ${risks[0]?.risk || 'execution complexity'}, which can be mitigated through ${risks[0]?.mitigation || 'focused prioritization'}. ` +
      `\n\n` +
      `This strategy leverages the convergent insights from ${actions[0].framework_support.length} strategic frameworks, ` +
      `providing ${this.calculateConfidenceStatement(position, coreStrategy)} confidence in the recommended direction.`;
    
    return summary;
  }

  // Helper methods
  private assessFinancialStrength(outputs: FrameworkOutput[]): number {
    // Simple heuristic - would be more sophisticated in production
    const hasRunwayRisk = outputs.some(o => 
      o.keyInsights.some(i => i.includes('runway') && i.includes('risk'))
    );
    return hasRunwayRisk ? 0.3 : 0.7;
  }

  private assessGrowthAmbition(outputs: FrameworkOutput[]): number {
    const growthMentions = outputs.reduce((count, o) => 
      count + o.recommendations.filter(r => 
        r.action.includes('growth') || r.action.includes('expand')
      ).length, 0
    );
    return Math.min(1, growthMentions / 10);
  }

  private calculateStrategicGap(current: string, desired: string, outputs: FrameworkOutput[]): string {
    const gaps = [];
    
    if (current.includes('challenger') && desired.includes('leader')) {
      gaps.push('market share growth of 10-20x');
    }
    
    if (current.includes('struggling') && desired.includes('profitable')) {
      gaps.push('operational transformation and cost reduction');
    }
    
    if (!current.includes('strong') && desired.includes('sustainable')) {
      gaps.push('capability building and competitive moats');
    }
    
    return gaps.join(', ') || 'incremental improvements across all dimensions';
  }

  private normalizeAction(action: string): string {
    // Normalize similar actions for grouping
    const normalized = action.toLowerCase();
    
    if (normalized.includes('hire') && normalized.includes('sales')) {
      return 'hire_sales_leadership';
    }
    if (normalized.includes('reduce') && normalized.includes('burn')) {
      return 'optimize_burn_rate';
    }
    if (normalized.includes('expand') && normalized.includes('market')) {
      return 'market_expansion';
    }
    
    return normalized.replace(/[^a-z0-9]/g, '_').substring(0, 30);
  }

  private calculatePriorityScore(actions: any[]): number {
    const priorityMap = { immediate: 100, 'short-term': 70, 'medium-term': 40, 'long-term': 20 };
    const sum = actions.reduce((total, a) => 
      total + (priorityMap[a.priority] || 50), 0
    );
    return sum / actions.length;
  }

  private calculateImpactScore(actions: any[]): number {
    const impactMap = { high: 100, medium: 60, low: 30 };
    const sum = actions.reduce((total, a) => 
      total + (impactMap[a.impact] || 50), 0
    );
    return sum / actions.length;
  }

  private assessStrategicAlignment(action: string, coreStrategy: any): number {
    const strategyKeywords = coreStrategy.name.toLowerCase().split(' ');
    const actionWords = action.split('_');
    
    const matches = strategyKeywords.filter(keyword => 
      actionWords.some(word => word.includes(keyword) || keyword.includes(word))
    ).length;
    
    return (matches / strategyKeywords.length) * 100;
  }

  private refineActionDescription(key: string, originalAction: string): string {
    const refinements = {
      'hire_sales_leadership': 'Hire VP Sales with enterprise SaaS experience within 60 days',
      'optimize_burn_rate': 'Reduce burn rate by 30% through operational efficiency',
      'market_expansion': 'Launch into 2 adjacent market segments with proven playbook',
      'improve_retention': 'Implement customer success program to reduce churn below 5%',
      'product_development': 'Accelerate product roadmap to achieve feature parity'
    };
    
    return refinements[key] || originalAction;
  }

  private determineTimeline(actions: any[]): string {
    const hasImmediate = actions.some(a => a.priority === 'immediate');
    const hasShortTerm = actions.some(a => a.priority === 'short-term');
    
    if (hasImmediate) return '0-30 days';
    if (hasShortTerm) return '1-3 months';
    return '3-6 months';
  }

  private generateSuccessMetric(actionKey: string): string {
    const metrics = {
      'hire_sales_leadership': 'Pipeline growth of 3x within 90 days',
      'optimize_burn_rate': 'Burn multiple below 1.5x',
      'market_expansion': '20% of revenue from new segments',
      'improve_retention': 'Net Revenue Retention > 110%',
      'product_development': 'Feature adoption rate > 60%'
    };
    
    return metrics[actionKey] || 'Measurable improvement in KPIs';
  }

  private calculateRiskScore(likelihood: string, impact: string): number {
    const likelihoodScore = { high: 3, medium: 2, low: 1 };
    const impactScore = { high: 3, medium: 2, low: 1 };
    
    return (likelihoodScore[likelihood] || 2) * (impactScore[impact] || 2);
  }

  private calculateConfidenceLevel(coherence: StrategicCoherence, patterns: CrossFrameworkPattern[]): number {
    const baseConfidence = coherence.coherenceScore;
    const patternBonus = Math.min(20, patterns.length * 5);
    const highConfidencePatterns = patterns.filter(p => p.confidence > 80).length;
    const patternConfidenceBonus = highConfidencePatterns * 5;
    
    return Math.min(95, baseConfidence + patternBonus + patternConfidenceBonus);
  }

  private calculateConfidenceStatement(position: any, strategy: any): string {
    if (position.gap.includes('10-20x')) return 'moderate';
    if (strategy.timeframe.includes('6-9')) return 'high';
    return 'strong';
  }
}

// Export singleton instance
export const strategicSynthesis = new StrategicSynthesisEngine();