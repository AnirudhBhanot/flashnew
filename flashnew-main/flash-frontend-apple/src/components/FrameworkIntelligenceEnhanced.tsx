import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '../design-system/components';
import useAssessmentStore from '../store/assessmentStore';
import styles from './FrameworkIntelligence.module.scss';

interface IntelligentFrameworkRecommendation {
  framework_id: string;
  framework_name: string;
  category: string;
  relevance_score: number;
  why_selected: string;
  expected_impact: string;
  implementation_priority: number;
  time_to_value: string;
  specific_benefits: string[];
  implementation_tips: string[];
  success_metrics: string[];
  risk_factors: string[];
}

interface FrameworkAnalysisResponse {
  recommendations: IntelligentFrameworkRecommendation[];
  situation_analysis: string;
  strategic_priorities: string[];
  implementation_roadmap: {
    phase_1: {
      name: string;
      frameworks: string[];
      objectives: string[];
      expected_outcomes: string[];
    };
    phase_2: {
      name: string;
      frameworks: string[];
      objectives: string[];
      expected_outcomes: string[];
    };
    phase_3: {
      name: string;
      frameworks: string[];
      objectives: string[];
      expected_outcomes: string[];
    };
  };
  success_factors: string[];
  total_frameworks_analyzed: number;
  selection_rationale: string;
}

interface FrameworkInsight {
  framework: string;
  category: string;
  analysis: string;
  key_findings: string[];
  action_items: string[];
  expected_impact: string;
  implementation_timeline: string;
}

const FrameworkIntelligenceEnhanced: React.FC = () => {
  const { data: assessmentData } = useAssessmentStore();
  const [activeTab, setActiveTab] = useState<'recommendations' | 'analysis' | 'roadmap'>('recommendations');
  const [frameworkAnalysis, setFrameworkAnalysis] = useState<FrameworkAnalysisResponse | null>(null);
  const [frameworkInsights, setFrameworkInsights] = useState<FrameworkInsight[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFramework, setSelectedFramework] = useState<IntelligentFrameworkRecommendation | null>(null);
  const [expandedPhase, setExpandedPhase] = useState<string | null>('phase_1');

  const buildStartupData = () => {
    const companyInfo = assessmentData?.companyInfo || {};
    const capital = assessmentData?.capital || {};
    const people = assessmentData?.people || {};
    const market = assessmentData?.market || {};
    const advantage = assessmentData?.advantage || {};

    return {
      // Company basics
      company_name: companyInfo.companyName || 'Unnamed Company',
      company_stage: mapCompanyStage(companyInfo.stage),
      funding_stage: companyInfo.stage || 'seed',
      industry: companyInfo.industry || 'technology',
      sector: companyInfo.sector,
      
      // Team and resources
      team_size_full_time: people.teamSize || 10,
      technical_team_percent: people.technicalTeamPercent || 50,
      founders_experience_years: people.foundersExperience || 5,
      
      // Financial metrics
      annual_revenue_run_rate: capital.annualRevenueRunRate || 0,
      revenue_growth_rate_percent: capital.revenueGrowthRate || 0,
      monthly_burn_usd: capital.monthlyBurnRate || 50000,
      runway_months: capital.runwayMonths || 12,
      burn_multiple: capital.burnMultiple || 1.5,
      
      // Business metrics
      customer_count: market.customerCount || 0,
      customer_acquisition_cost_usd: market.customerAcquisitionCost || 1000,
      customer_lifetime_value_usd: market.customerLifetimeValue || 5000,
      net_dollar_retention_percent: market.netDollarRetention || 100,
      
      // Challenges and goals
      primary_challenges: determineChallenges(),
      goals: determineGoals(),
      pain_points: determinePainPoints(),
      
      // Additional context
      business_model: companyInfo.businessModel || 'B2B SaaS',
      target_market: market.targetMarket || 'SMB',
      competitive_landscape: advantage.competitiveLandscape || 'Moderately competitive',
      unique_value_proposition: advantage.uniqueValueProposition || ''
    };
  };

  const mapCompanyStage = (stage?: string): string => {
    const stageMap: Record<string, string> = {
      'idea': 'pre-seed',
      'pre-seed': 'pre-seed',
      'seed': 'seed',
      'series-a': 'series-a',
      'series-b': 'series-b',
      'series-c': 'series-c',
      'growth': 'series-b',
      'mature': 'series-c'
    };
    return stageMap[stage?.toLowerCase() || ''] || 'seed';
  };

  const determineChallenges = (): string[] => {
    const challenges: string[] = [];
    const capital = assessmentData?.capital || {};
    const market = assessmentData?.market || {};
    const people = assessmentData?.people || {};
    
    if (capital.runwayMonths && capital.runwayMonths < 6) {
      challenges.push('Fundraising urgency');
    }
    
    if (capital.annualRevenueRunRate === 0) {
      challenges.push('Finding product-market fit');
    } else if (capital.revenueGrowthRate && capital.revenueGrowthRate < 50) {
      challenges.push('Accelerating revenue growth');
    }
    
    if (market.customerCount && market.customerCount < 10) {
      challenges.push('Customer acquisition');
    }
    
    if (people.teamSize && people.teamSize < 5) {
      challenges.push('Team building');
    }
    
    if (market.customerAcquisitionCost && market.customerLifetimeValue) {
      const ltv_cac = market.customerLifetimeValue / market.customerAcquisitionCost;
      if (ltv_cac < 3) {
        challenges.push('Unit economics optimization');
      }
    }
    
    // Add some defaults if no specific challenges identified
    if (challenges.length === 0) {
      challenges.push('Scaling operations', 'Building competitive advantage');
    }
    
    return challenges;
  };

  const determineGoals = (): string[] => {
    const goals: string[] = [];
    const stage = assessmentData?.companyInfo?.stage;
    
    switch (stage) {
      case 'pre-seed':
      case 'seed':
        goals.push('Achieve product-market fit', 'Build MVP', 'Validate business model');
        break;
      case 'series-a':
        goals.push('Scale revenue to $1M ARR', 'Build repeatable sales process', 'Expand team');
        break;
      case 'series-b':
      case 'growth':
        goals.push('Expand to new markets', 'Optimize unit economics', 'Build market leadership');
        break;
      default:
        goals.push('Increase revenue growth', 'Improve operational efficiency', 'Build sustainable advantage');
    }
    
    return goals;
  };

  const determinePainPoints = (): string[] => {
    const painPoints: string[] = [];
    const capital = assessmentData?.capital || {};
    const market = assessmentData?.market || {};
    
    if (capital.burnMultiple && capital.burnMultiple > 2) {
      painPoints.push('High burn rate relative to growth');
    }
    
    if (market.netDollarRetention && market.netDollarRetention < 100) {
      painPoints.push('Customer churn issues');
    }
    
    if (capital.cashOnHand && capital.monthlyBurnRate) {
      const runway = capital.cashOnHand / capital.monthlyBurnRate;
      if (runway < 12) {
        painPoints.push('Limited runway');
      }
    }
    
    return painPoints;
  };

  const fetchIntelligentRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const startupData = buildStartupData();
      
      // Call the new intelligent recommendation endpoint
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/recommend`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(startupData)
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch intelligent framework recommendations');
      }

      const data: FrameworkAnalysisResponse = await response.json();
      setFrameworkAnalysis(data);
      
      // If analysis tab is active, also fetch framework insights
      if (activeTab === 'analysis') {
        await fetchFrameworkInsights(startupData);
      }
    } catch (err) {
      console.error('Framework recommendation error:', err);
      setError('Failed to load framework recommendations. Please try again.');
      
      // Set fallback data for demo purposes
      setFrameworkAnalysis(getFallbackAnalysis());
    } finally {
      setIsLoading(false);
    }
  };

  const fetchFrameworkInsights = async (startupData: any) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/analyze-with-frameworks`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(startupData)
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch framework insights');
      }

      const data = await response.json();
      setFrameworkInsights(data.framework_insights || []);
    } catch (err) {
      console.error('Framework insights error:', err);
      // Use insights from recommendations as fallback
      if (frameworkAnalysis) {
        const fallbackInsights = frameworkAnalysis.recommendations.slice(0, 5).map(rec => ({
          framework: rec.framework_name,
          category: rec.category,
          analysis: rec.why_selected,
          key_findings: rec.specific_benefits,
          action_items: rec.implementation_tips,
          expected_impact: rec.expected_impact,
          implementation_timeline: rec.time_to_value
        }));
        setFrameworkInsights(fallbackInsights);
      }
    }
  };

  const getFallbackAnalysis = (): FrameworkAnalysisResponse => {
    return {
      recommendations: [
        {
          framework_id: "lean_startup",
          framework_name: "Lean Startup",
          category: "Innovation",
          relevance_score: 0.95,
          why_selected: "Critical for validating product-market fit with limited resources",
          expected_impact: "High - Critical for addressing your primary challenges",
          implementation_priority: 1,
          time_to_value: "2-4 weeks",
          specific_benefits: [
            "Reduce waste through validated learning",
            "Faster time to market with MVP approach",
            "Data-driven decision making"
          ],
          implementation_tips: [
            "Start with customer interviews to validate assumptions",
            "Build a minimal viable product focusing on core value",
            "Implement analytics to track key metrics"
          ],
          success_metrics: [
            "Time to first customer feedback < 2 weeks",
            "Number of validated hypotheses per month",
            "Customer engagement metrics"
          ],
          risk_factors: [
            "Requires discipline to avoid feature creep",
            "May strain limited team resources"
          ]
        },
        {
          framework_id: "aarrr_metrics",
          framework_name: "AARRR (Pirate) Metrics",
          category: "Growth",
          relevance_score: 0.92,
          why_selected: "Essential for measuring and optimizing your growth funnel",
          expected_impact: "High - Critical for addressing your primary challenges",
          implementation_priority: 2,
          time_to_value: "1-3 months",
          specific_benefits: [
            "Clear visibility into growth funnel performance",
            "Identify and fix conversion bottlenecks",
            "Accelerate revenue growth through systematic approach"
          ],
          implementation_tips: [
            "Set up comprehensive analytics tracking",
            "Define clear metrics for each funnel stage",
            "Create weekly review cadence"
          ],
          success_metrics: [
            "Funnel visibility > 90%",
            "Weekly metric reviews implemented",
            "Conversion rate improvements"
          ],
          risk_factors: [
            "Requires analytics infrastructure investment",
            "May require technical expertise"
          ]
        }
      ],
      situation_analysis: "Based on analysis of your seed stage technology company with 10 employees:\n\nKey Findings:\n- Current challenges: Finding product-market fit, Customer acquisition, Unit economics optimization\n- Recommended focus areas: Innovation, Growth, Customer, Financial\n- Implementation approach: Phased with Intermediate complexity\n\nYour startup would benefit most from frameworks that address finding product-market fit while building foundations for sustainable growth.",
      strategic_priorities: [
        "Validate product-market fit through systematic experimentation",
        "Build repeatable customer acquisition engine",
        "Establish data-driven culture and decision making"
      ],
      implementation_roadmap: {
        phase_1: {
          name: "Foundation (0-3 months)",
          frameworks: ["Lean Startup", "AARRR Metrics"],
          objectives: [
            "Establish core measurement systems",
            "Address most critical pain points",
            "Quick wins for team morale"
          ],
          expected_outcomes: [
            "Improved visibility into key metrics",
            "Initial process improvements",
            "Team alignment on priorities"
          ]
        },
        phase_2: {
          name: "Growth (3-6 months)",
          frameworks: ["Jobs to be Done", "Growth Loops"],
          objectives: [
            "Scale successful initiatives",
            "Optimize core operations",
            "Build competitive advantages"
          ],
          expected_outcomes: [
            "Accelerated growth metrics",
            "Improved operational efficiency",
            "Stronger market position"
          ]
        },
        phase_3: {
          name: "Excellence (6-12 months)",
          frameworks: ["Blue Ocean Strategy", "OKR Framework"],
          objectives: [
            "Achieve operational excellence",
            "Develop innovation capabilities",
            "Prepare for next growth stage"
          ],
          expected_outcomes: [
            "Industry-leading performance",
            "Sustainable competitive advantages",
            "Platform for future expansion"
          ]
        }
      },
      success_factors: [
        "Executive commitment to framework implementation",
        "Dedicated resources for change management",
        "Regular progress tracking and adaptation",
        "Focus on quick wins while building long-term capabilities",
        "Cross-functional collaboration and buy-in"
      ],
      total_frameworks_analyzed: 554,
      selection_rationale: "Frameworks selected based on seed stage needs, technology industry best practices, and your specific challenges"
    };
  };

  useEffect(() => {
    if (!frameworkAnalysis) {
      fetchIntelligentRecommendations();
    } else if (activeTab === 'analysis' && frameworkInsights.length === 0) {
      fetchFrameworkInsights(buildStartupData());
    }
  }, [activeTab]);

  const getImpactColor = (impact: string): string => {
    if (impact.toLowerCase().includes('high')) return '#34c759';
    if (impact.toLowerCase().includes('medium')) return '#007aff';
    return '#8e8e93';
  };

  const getPriorityLabel = (priority: number): string => {
    if (priority <= 3) return 'Immediate';
    if (priority <= 7) return 'Short-term';
    return 'Long-term';
  };

  const getPriorityColor = (priority: number): string => {
    if (priority <= 3) return '#ff3b30';
    if (priority <= 7) return '#ff9500';
    return '#007aff';
  };

  const getCategoryIcon = (category: string): string => {
    const iconMap: Record<string, string> = {
      'Strategy': 'target',
      'Innovation': 'lightbulb',
      'Growth': 'chart.line.uptrend.xyaxis',
      'Financial': 'dollarsign.circle',
      'Operations': 'gearshape.2',
      'Marketing': 'megaphone',
      'Product': 'cube',
      'Leadership': 'person.2',
      'Organizational': 'building.2',
      'Customer': 'person.crop.circle',
      'Technology': 'cpu',
      'Analytics': 'chart.bar.xaxis',
      'Sales': 'cart',
      'Quality': 'checkmark.seal',
      'Risk': 'exclamationmark.shield',
      'Change': 'arrow.triangle.2.circlepath',
      'Digital': 'network',
      'Startup': 'rocket'
    };
    return iconMap[category] || 'square.grid.2x2';
  };

  return (
    <div className={styles.container}>
      <div className={styles.mainCard}>
        <div className={styles.header}>
          <h2 className={styles.title}>Intelligent Framework Selection</h2>
          <p className={styles.subtitle}>
            AI-powered analysis of your startup's specific situation to recommend the most relevant frameworks from our database of 554 business methodologies
          </p>
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${activeTab === 'recommendations' ? styles.active : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            <Icon name="wand.and.stars" size={16} />
            Smart Recommendations
          </button>
          <button
            className={`${styles.tab} ${activeTab === 'analysis' ? styles.active : ''}`}
            onClick={() => setActiveTab('analysis')}
          >
            <Icon name="doc.text.magnifyingglass" size={16} />
            Framework Analysis
          </button>
          <button
            className={`${styles.tab} ${activeTab === 'roadmap' ? styles.active : ''}`}
            onClick={() => setActiveTab('roadmap')}
          >
            <Icon name="map" size={16} />
            Implementation Roadmap
          </button>
        </div>

        <div className={styles.content}>
          {isLoading && (
            <div className={styles.loading}>
              <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
              <p>Analyzing your startup's situation and selecting optimal frameworks...</p>
            </div>
          )}

          {error && (
            <div className={styles.error}>
              <Icon name="exclamationmark.triangle" size={24} />
              <p>{error}</p>
              <button onClick={fetchIntelligentRecommendations} className={styles.retryButton}>
                Try Again
              </button>
            </div>
          )}

          {!isLoading && !error && frameworkAnalysis && (
            <>
              {activeTab === 'recommendations' && (
                <div className={styles.recommendationsSection}>
                  {/* Situation Analysis Card */}
                  <motion.div 
                    className={styles.analysisCard}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    <h3>Situation Analysis</h3>
                    <p className={styles.analysisText}>{frameworkAnalysis.situation_analysis}</p>
                    
                    <div className={styles.priorities}>
                      <h4>Strategic Priorities</h4>
                      <ol>
                        {frameworkAnalysis.strategic_priorities.map((priority, idx) => (
                          <li key={idx}>{priority}</li>
                        ))}
                      </ol>
                    </div>
                    
                    <div className={styles.stats}>
                      <div className={styles.stat}>
                        <span className={styles.statValue}>{frameworkAnalysis.total_frameworks_analyzed}</span>
                        <span className={styles.statLabel}>Frameworks Analyzed</span>
                      </div>
                      <div className={styles.stat}>
                        <span className={styles.statValue}>{frameworkAnalysis.recommendations.length}</span>
                        <span className={styles.statLabel}>Selected for You</span>
                      </div>
                    </div>
                  </motion.div>

                  {/* Framework Recommendations */}
                  <div className={styles.recommendationsGrid}>
                    {frameworkAnalysis.recommendations.map((framework, index) => (
                      <motion.div
                        key={framework.framework_id}
                        className={styles.frameworkCard}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 + index * 0.05 }}
                        onClick={() => setSelectedFramework(framework)}
                        whileHover={{ scale: 1.02 }}
                      >
                        <div className={styles.frameworkHeader}>
                          <div className={styles.frameworkInfo}>
                            <Icon name={getCategoryIcon(framework.category)} size={24} />
                            <div>
                              <h3 className={styles.frameworkName}>{framework.framework_name}</h3>
                              <div className={styles.frameworkMeta}>
                                <span className={styles.frameworkCategory}>{framework.category}</span>
                                <span 
                                  className={styles.priority}
                                  style={{ color: getPriorityColor(framework.implementation_priority) }}
                                >
                                  {getPriorityLabel(framework.implementation_priority)}
                                </span>
                                <span className={styles.time}>
                                  <Icon name="clock" size={14} />
                                  {framework.time_to_value}
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className={styles.frameworkScore}>
                            {Math.round(framework.relevance_score * 100)}%
                            <span className={styles.scoreLabel}>Match</span>
                          </div>
                        </div>
                        
                        <div className={styles.whySelected}>
                          <Icon name="lightbulb" size={16} />
                          <p>{framework.why_selected}</p>
                        </div>
                        
                        <div className={styles.impact} style={{ color: getImpactColor(framework.expected_impact) }}>
                          <Icon name="bolt.fill" size={16} />
                          <span>{framework.expected_impact}</span>
                        </div>
                        
                        <div className={styles.benefits}>
                          <h4>Key Benefits</h4>
                          <ul>
                            {framework.specific_benefits.slice(0, 3).map((benefit, idx) => (
                              <li key={idx}>
                                <Icon name="checkmark.circle.fill" size={14} />
                                {benefit}
                              </li>
                            ))}
                          </ul>
                        </div>

                        {framework.risk_factors.length > 0 && (
                          <div className={styles.risks}>
                            <Icon name="info.circle" size={14} />
                            <span>{framework.risk_factors[0]}</span>
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'analysis' && (
                <div className={styles.analysisSection}>
                  <motion.div 
                    className={styles.analysisIntro}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    <h3>Framework-Based Analysis</h3>
                    <p>Deep insights from applying selected frameworks to your specific situation</p>
                  </motion.div>

                  {frameworkInsights.map((insight, index) => (
                    <motion.div
                      key={index}
                      className={styles.insightCard}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className={styles.insightHeader}>
                        <div className={styles.insightInfo}>
                          <Icon name={getCategoryIcon(insight.category)} size={20} />
                          <h3>{insight.framework}</h3>
                          <span className={styles.insightCategory}>{insight.category}</span>
                        </div>
                        <div className={styles.timeline}>
                          <Icon name="calendar" size={16} />
                          {insight.implementation_timeline}
                        </div>
                      </div>

                      <p className={styles.insightAnalysis}>{insight.analysis}</p>

                      <div className={styles.insightContent}>
                        <div className={styles.findings}>
                          <h4>Key Findings</h4>
                          <ul>
                            {insight.key_findings.map((finding, idx) => (
                              <li key={idx}>{finding}</li>
                            ))}
                          </ul>
                        </div>

                        <div className={styles.actions}>
                          <h4>Action Items</h4>
                          <ol>
                            {insight.action_items.map((action, idx) => (
                              <li key={idx}>{action}</li>
                            ))}
                          </ol>
                        </div>
                      </div>

                      <div className={styles.expectedImpact}>
                        <Icon name="target" size={16} />
                        <span>Expected Impact: {insight.expected_impact}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}

              {activeTab === 'roadmap' && frameworkAnalysis.implementation_roadmap && (
                <div className={styles.roadmapSection}>
                  <motion.div 
                    className={styles.roadmapIntro}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    <h3>Phased Implementation Plan</h3>
                    <p>A structured approach to implementing recommended frameworks for maximum impact</p>
                    
                    <div className={styles.successFactors}>
                      <h4>Success Factors</h4>
                      <div className={styles.factorsGrid}>
                        {frameworkAnalysis.success_factors.map((factor, idx) => (
                          <div key={idx} className={styles.factor}>
                            <Icon name="checkmark.seal.fill" size={16} />
                            <span>{factor}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>

                  <div className={styles.phases}>
                    {Object.entries(frameworkAnalysis.implementation_roadmap).map(([phaseKey, phase], index) => (
                      <motion.div
                        key={phaseKey}
                        className={`${styles.phaseCard} ${expandedPhase === phaseKey ? styles.expanded : ''}`}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <div 
                          className={styles.phaseHeader}
                          onClick={() => setExpandedPhase(expandedPhase === phaseKey ? null : phaseKey)}
                        >
                          <div className={styles.phaseInfo}>
                            <div className={styles.phaseNumber}>{index + 1}</div>
                            <div>
                              <h3>{phase.name}</h3>
                              <div className={styles.frameworkCount}>
                                {phase.frameworks.length} frameworks
                              </div>
                            </div>
                          </div>
                          <Icon 
                            name={expandedPhase === phaseKey ? "chevron.up" : "chevron.down"} 
                            size={20} 
                          />
                        </div>

                        <AnimatePresence>
                          {expandedPhase === phaseKey && (
                            <motion.div
                              className={styles.phaseContent}
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.3 }}
                            >
                              <div className={styles.frameworks}>
                                <h4>Frameworks to Implement</h4>
                                <div className={styles.frameworkTags}>
                                  {phase.frameworks.map((fw, idx) => (
                                    <span key={idx} className={styles.frameworkTag}>
                                      {fw}
                                    </span>
                                  ))}
                                </div>
                              </div>

                              <div className={styles.objectives}>
                                <h4>Phase Objectives</h4>
                                <ul>
                                  {phase.objectives.map((obj, idx) => (
                                    <li key={idx}>
                                      <Icon name="target" size={14} />
                                      {obj}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              <div className={styles.outcomes}>
                                <h4>Expected Outcomes</h4>
                                <ul>
                                  {phase.expected_outcomes.map((outcome, idx) => (
                                    <li key={idx}>
                                      <Icon name="star" size={14} />
                                      {outcome}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Framework Detail Modal */}
        <AnimatePresence>
          {selectedFramework && (
            <motion.div
              className={styles.modal}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedFramework(null)}
            >
              <motion.div
                className={styles.modalContent}
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
              >
                <div className={styles.modalHeader}>
                  <div>
                    <h3>{selectedFramework.framework_name}</h3>
                    <div className={styles.modalMeta}>
                      <span className={styles.category}>{selectedFramework.category}</span>
                      <span className={styles.relevance}>
                        {Math.round(selectedFramework.relevance_score * 100)}% relevance
                      </span>
                    </div>
                  </div>
                  <button onClick={() => setSelectedFramework(null)}>
                    <Icon name="xmark" size={20} />
                  </button>
                </div>
                
                <div className={styles.modalBody}>
                  <div className={styles.modalSection}>
                    <h4>Why This Framework?</h4>
                    <p>{selectedFramework.why_selected}</p>
                  </div>

                  <div className={styles.modalSection}>
                    <h4>Expected Impact</h4>
                    <p className={styles.impact} style={{ color: getImpactColor(selectedFramework.expected_impact) }}>
                      <Icon name="bolt.fill" size={16} />
                      {selectedFramework.expected_impact}
                    </p>
                  </div>
                  
                  <div className={styles.modalSection}>
                    <h4>Implementation Steps</h4>
                    <ol>
                      {selectedFramework.implementation_tips.map((tip, idx) => (
                        <li key={idx}>{tip}</li>
                      ))}
                    </ol>
                  </div>

                  <div className={styles.modalSection}>
                    <h4>Success Metrics</h4>
                    <ul className={styles.metricsList}>
                      {selectedFramework.success_metrics.map((metric, idx) => (
                        <li key={idx}>
                          <Icon name="chart.bar" size={14} />
                          {metric}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {selectedFramework.risk_factors.length > 0 && (
                    <div className={styles.modalSection}>
                      <h4>Risk Factors</h4>
                      <ul className={styles.risksList}>
                        {selectedFramework.risk_factors.map((risk, idx) => (
                          <li key={idx}>
                            <Icon name="exclamationmark.triangle" size={14} />
                            {risk}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  <div className={styles.modalActions}>
                    <button className={styles.primaryButton}>
                      <Icon name="book" size={16} />
                      View Full Implementation Guide
                    </button>
                    <button className={styles.secondaryButton}>
                      <Icon name="square.and.arrow.down" size={16} />
                      Download Framework Template
                    </button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export { FrameworkIntelligenceEnhanced };