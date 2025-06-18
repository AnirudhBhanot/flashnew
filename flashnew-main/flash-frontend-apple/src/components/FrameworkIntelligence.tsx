import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '../design-system/components';
import useAssessmentStore from '../store/assessmentStore';
import styles from './FrameworkIntelligence.module.scss';
// Error recovery utilities
const retryWithBackoff = async (
  fn: () => Promise<any>,
  maxRetries: number = 3,
  initialDelay: number = 1000
) => {
  let lastError;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (i < maxRetries - 1) {
        const delay = initialDelay * Math.pow(2, i);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
};

// Enhanced cache management
const frameworkCache = {
  set: (key: string, data: any, ttl: number = 3600000) => {
    const item = {
      data,
      timestamp: Date.now(),
      ttl
    };
    localStorage.setItem(`framework_cache_${key}`, JSON.stringify(item));
  },
  
  get: (key: string) => {
    const item = localStorage.getItem(`framework_cache_${key}`);
    if (!item) return null;
    
    const parsed = JSON.parse(item);
    const age = Date.now() - parsed.timestamp;
    
    if (age > parsed.ttl) {
      localStorage.removeItem(`framework_cache_${key}`);
      return null;
    }
    
    return parsed.data;
  },
  
  clear: () => {
    Object.keys(localStorage)
      .filter(key => key.startsWith('framework_cache_'))
      .forEach(key => localStorage.removeItem(key));
  }
};


interface Framework {
  framework_name: string;
  score: number;
  category: string;
  complexity: string;
  time_to_implement: string;
  description: string;
  why_recommended: string;
  key_benefits: string[];
  implementation_tips: string[];
}

interface Phase {
  phase: number;
  duration: string;
  frameworks: string[];
  objectives: string[];
  success_metrics: string[];
  dependencies: string[];
}

interface FrameworkCombination {
  frameworks: string[];
  synergy_score: number;
  combined_benefit: string;
  implementation_order: string[];
  estimated_impact: string;
}

const FrameworkIntelligence: React.FC = () => {
  const { data: assessmentData } = useAssessmentStore();
  const [activeTab, setActiveTab] = useState<'recommendations' | 'roadmap' | 'combinations'>('recommendations');
  const [recommendations, setRecommendations] = useState<Framework[]>([]);
  const [roadmap, setRoadmap] = useState<Phase[]>([]);
  const [combinations, setCombinations] = useState<FrameworkCombination[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFramework, setSelectedFramework] = useState<Framework | null>(null);

  const getContext = () => {
    return {
      company_stage: assessmentData?.companyInfo?.stage || 'seed',
      industry: assessmentData?.companyInfo?.industry || 'tech',
      primary_challenge: determinePrimaryChallenge(),
      team_size: assessmentData?.people?.teamSize || 10,
      resources: determineResources(),
      timeline: '6-12 months',
      goals: determineGoals(),
      current_frameworks: []
    };
  };

  const determinePrimaryChallenge = () => {
    // Analyze assessment data to determine primary challenge
    const revenue = assessmentData?.capital?.annualRevenueRunRate || 0;
    const growth = assessmentData?.capital?.revenueGrowthRate || 0;
    const runway = assessmentData?.capital?.runwayMonths || 0;
    
    if (revenue === 0) return 'finding_product_market_fit';
    if (runway < 6) return 'fundraising';
    if (growth < 50) return 'accelerating_growth';
    return 'scaling_operations';
  };

  const determineResources = () => {
    const capital = assessmentData?.capital?.cashOnHand || 0;
    const teamSize = assessmentData?.people?.teamSize || 0;
    
    if (capital < 500000 || teamSize < 10) return 'limited';
    if (capital < 5000000 || teamSize < 50) return 'moderate';
    return 'abundant';
  };

  const determineGoals = () => {
    const goals = [];
    const revenue = assessmentData?.capital?.annualRevenueRunRate || 0;
    const growth = assessmentData?.capital?.revenueGrowthRate || 0;
    
    if (revenue === 0) goals.push('achieve_product_market_fit');
    if (growth < 100) goals.push('increase_revenue_growth');
    goals.push('improve_operational_efficiency');
    goals.push('build_competitive_advantage');
    
    return goals;
  };

  
  const getContextualFallback = () => {
    const context = getContext();
    const fallbacks = [];
    
    // Industry-specific recommendations
    if (context.industry?.toLowerCase().includes('tech') || context.industry?.toLowerCase().includes('saas')) {
      fallbacks.push({
        framework_name: "Lean Startup",
        score: 0.95,
        category: "Innovation",
        complexity: "Intermediate",
        time_to_implement: "2-3 months",
        description: "Build-Measure-Learn feedback loop for rapid validation",
        why_recommended: "Perfect for tech companies iterating quickly",
        key_benefits: ["Rapid validation", "Reduced waste", "Customer feedback"],
        implementation_tips: ["Start with MVP", "Define metrics", "Weekly iterations"]
      });
    }
    
    // Stage-specific recommendations
    if (context.company_stage === 'seed' || context.company_stage === 'pre_seed') {
      fallbacks.push({
        framework_name: "Customer Development",
        score: 0.92,
        category: "Product",
        complexity: "Basic",
        time_to_implement: "1-2 months",
        description: "Systematic approach to understanding customer needs",
        why_recommended: "Critical for early-stage validation",
        key_benefits: ["Customer insights", "Problem validation", "Solution fit"],
        implementation_tips: ["Interview 100 customers", "Document learnings", "Pivot if needed"]
      });
    }
    
    // Challenge-specific recommendations
    if (context.primary_challenge?.includes('scaling')) {
      fallbacks.push({
        framework_name: "Scaling Up (Rockefeller Habits)",
        score: 0.90,
        category: "Strategy",
        complexity: "Advanced",
        time_to_implement: "3-6 months",
        description: "Comprehensive framework for scaling businesses",
        why_recommended: "Proven system for companies ready to scale",
        key_benefits: ["Systematic growth", "Team alignment", "Execution rhythm"],
        implementation_tips: ["Start with One-Page Plan", "Daily huddles", "Quarterly themes"]
      });
    }
    
    // Always include some general frameworks
    fallbacks.push(
      {
        framework_name: "OKR Framework",
        score: 0.88,
        category: "Strategy",
        complexity: "Intermediate",
        time_to_implement: "1-2 months",
        description: "Objectives and Key Results for goal alignment",
        why_recommended: "Universal framework for any growth stage",
        key_benefits: ["Clear goals", "Measurable results", "Team alignment"],
        implementation_tips: ["Start at company level", "Cascade to teams", "Quarterly cycles"]
      },
      {
        framework_name: "SWOT Analysis",
        score: 0.85,
        category: "Strategy",
        complexity: "Basic",
        time_to_implement: "1 week",
        description: "Strategic assessment of position and opportunities",
        why_recommended: "Quick wins for strategic clarity",
        key_benefits: ["Situational awareness", "Opportunity identification", "Risk assessment"],
        implementation_tips: ["Workshop format", "Include all stakeholders", "Update quarterly"]
      }
    );
    
    return fallbacks.slice(0, 8);
  };

  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    
    // Check cache first
    const cacheKey = JSON.stringify(getContext());
    const cached = frameworkCache.get(cacheKey);
    if (cached) {
      setRecommendations(cached.recommendations);
      setIsLoading(false);
      return;
    }
    
    try {
      const fetchWithRetry = async () => {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/recommend`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(getContext())
          }
        );

        if (!response.ok) {
          throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        return response.json();
      };
      
      const data = await retryWithBackoff(fetchWithRetry);
      setRecommendations(data.recommendations);
      
      // Cache successful response
      frameworkCache.set(cacheKey, data);
      
    } catch (err: any) {
      console.error('Framework recommendation error:', err);
      
      // Try to provide more specific error messages
      if (err.message.includes('fetch')) {
        setError('Unable to connect to the framework service. Please check your connection.');
      } else if (err.message.includes('timeout')) {
        setError('Request timed out. The server might be busy.');
      } else {
        setError(`Failed to load recommendations: ${err.message}`);
      }
      
      
      // Enhanced fallback data based on context
      const contextualFallback = getContextualFallback();
      setRecommendations(contextualFallback);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchRoadmap = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/roadmap`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(getContext())
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch implementation roadmap');
      }

      const data = await response.json();
      setRoadmap(data.roadmap);
    } catch (err) {
      console.error('Roadmap fetch error:', err);
      setError('Failed to load implementation roadmap');
      
      // Set fallback roadmap
      setRoadmap([
        {
          phase: 1,
          duration: "1-2 months",
          frameworks: ["Lean Startup", "AARRR Metrics"],
          objectives: ["Establish baseline metrics", "Launch MVP"],
          success_metrics: ["User engagement", "Conversion rate"],
          dependencies: []
        },
        {
          phase: 2,
          duration: "2-3 months",
          frameworks: ["Jobs to be Done", "Customer Journey Mapping"],
          objectives: ["Deep customer understanding", "Optimize experience"],
          success_metrics: ["NPS score", "Retention rate"],
          dependencies: ["Phase 1 completion"]
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCombinations = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/combinations`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(getContext())
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch framework combinations');
      }

      const data = await response.json();
      setCombinations(data.combinations);
    } catch (err) {
      console.error('Combinations fetch error:', err);
      setError('Failed to load framework combinations');
      
      // Set fallback combinations
      setCombinations([
        {
          frameworks: ["Lean Startup", "Design Thinking", "AARRR Metrics"],
          synergy_score: 0.95,
          combined_benefit: "Complete innovation-to-growth pipeline",
          implementation_order: ["Design Thinking", "Lean Startup", "AARRR Metrics"],
          estimated_impact: "3x faster product-market fit"
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'recommendations' && recommendations.length === 0) {
      fetchRecommendations();
    } else if (activeTab === 'roadmap' && roadmap.length === 0) {
      fetchRoadmap();
    } else if (activeTab === 'combinations' && combinations.length === 0) {
      fetchCombinations();
    }
  }, [activeTab]);

  const getComplexityLabel = (complexity: number | string): string => {
    if (typeof complexity === 'string') return complexity;
    const labels: Record<number, string> = {
      1: 'Basic',
      2: 'Intermediate',
      3: 'Advanced',
      4: 'Expert'
    };
    return labels[complexity] || 'Unknown';
  };

  const getComplexityColor = (complexity: number | string) => {
    const label = getComplexityLabel(complexity);
    switch (label) {
      case 'Basic': return '#34c759';
      case 'Intermediate': return '#007aff';
      case 'Advanced': return '#ff9500';
      case 'Expert': return '#af52de';
      default: return '#8e8e93';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Strategy': return 'target';
      case 'Innovation': return 'lightbulb';
      case 'Growth': return 'chart.line.uptrend.xyaxis';
      case 'Financial': return 'dollarsign.circle';
      case 'Operations': return 'gearshape.2';
      case 'Marketing': return 'megaphone';
      case 'Product': return 'cube';
      case 'Leadership': return 'person.2';
      case 'Organizational': return 'building.2';
      default: return 'square.grid.2x2';
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.mainCard}>
        <div className={styles.header}>
          <h2 className={styles.title}>Framework Intelligence Engine</h2>
          <p className={styles.subtitle}>
            AI-powered framework recommendations from our library of 554 business frameworks
          </p>
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${activeTab === 'recommendations' ? styles.active : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            <Icon name="wand.and.stars" size={16} />
            Recommendations
          </button>
          <button
            className={`${styles.tab} ${activeTab === 'roadmap' ? styles.active : ''}`}
            onClick={() => setActiveTab('roadmap')}
          >
            <Icon name="map" size={16} />
            Implementation Roadmap
          </button>
          <button
            className={`${styles.tab} ${activeTab === 'combinations' ? styles.active : ''}`}
            onClick={() => setActiveTab('combinations')}
          >
            <Icon name="link" size={16} />
            Framework Combinations
          </button>
        </div>

        <div className={styles.content}>
          {isLoading && (
            <div className={styles.loading}>
              <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
              <p>Analyzing your context and finding the best frameworks...</p>
            </div>
          )}

          {error && (
            <div className={styles.errorContainer}>
              <div className={styles.error}>
                <Icon name="exclamationmark.triangle" size={24} />
                <p>{error}</p>
              </div>
              <div className={styles.errorActions}>
                <button 
                  onClick={() => {
                    setError(null);
                    fetchRecommendations();
                  }}
                  className={styles.retryButton}
                >
                  <Icon name="arrow.clockwise" size={16} />
                  Try Again
                </button>
                <button 
                  onClick={() => {
                    setError(null);
                    const fallback = getContextualFallback();
                    setRecommendations(fallback);
                  }}
                  className={styles.fallbackButton}
                >
                  <Icon name="doc.text" size={16} />
                  Use Offline Mode
                </button>
              </div>
            </div>
          )}

          {!isLoading && !error && (
            <>
              {activeTab === 'recommendations' && (
                <div className={styles.recommendationsGrid}>
                  {recommendations.map((framework, index) => (
                    <motion.div
                      key={framework.framework_name}
                      className={styles.frameworkCard}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
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
                                className={styles.complexity}
                                style={{ color: getComplexityColor(framework.complexity) }}
                              >
                                {getComplexityLabel(framework.complexity)}
                              </span>
                              <span className={styles.time}>
                                <Icon name="clock" size={14} />
                                {framework.time_to_implement}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className={styles.frameworkScore}>
                          {Math.round(framework.score * 100)}%
                        </div>
                      </div>
                      
                      <p className={styles.frameworkDescription}>{framework.description}</p>
                      
                      <div className={styles.whyRecommended}>
                        <Icon name="lightbulb" size={16} />
                        <p>{framework.why_recommended}</p>
                      </div>
                      
                      <div className={styles.benefits}>
                        <h4>Key Benefits</h4>
                        <ul>
                          {framework.key_benefits.map((benefit, idx) => (
                            <li key={idx}>
                              <Icon name="checkmark.circle.fill" size={14} />
                              {benefit}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}

              {activeTab === 'roadmap' && (
                <div className={styles.roadmapPhases}>
                  {roadmap.map((phase, index) => (
                    <motion.div
                      key={phase.phase}
                      className={styles.phaseCard}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className={styles.phaseHeader}>
                        <div className={styles.phaseNumber}>Phase {phase.phase}</div>
                        <div className={styles.phaseDuration}>
                          <Icon name="calendar" size={16} />
                          {phase.duration}
                        </div>
                      </div>
                      
                      <div className={styles.phaseContent}>
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
                          <h4>Objectives</h4>
                          <ul>
                            {phase.objectives.map((obj, idx) => (
                              <li key={idx}>{obj}</li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className={styles.metrics}>
                          <h4>Success Metrics</h4>
                          <ul>
                            {phase.success_metrics.map((metric, idx) => (
                              <li key={idx}>
                                <Icon name="chart.bar" size={14} />
                                {metric}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}

              {activeTab === 'combinations' && (
                <div className={styles.combinationsGrid}>
                  {combinations.map((combo, index) => (
                    <motion.div
                      key={index}
                      className={styles.combinationCard}
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className={styles.synergyScore}>
                        <div className={styles.synergyValue}>
                          {Math.round(combo.synergy_score * 100)}%
                        </div>
                        <div className={styles.synergyLabel}>Synergy</div>
                      </div>
                      
                      <div className={styles.combinationContent}>
                        <div className={styles.frameworkList}>
                          {combo.frameworks.map((fw, idx) => (
                            <React.Fragment key={idx}>
                              <span className={styles.framework}>{fw}</span>
                              {idx < combo.frameworks.length - 1 && (
                                <Icon name="plus" size={16} />
                              )}
                            </React.Fragment>
                          ))}
                        </div>
                        
                        <div className={styles.benefit}>
                          <Icon name="sparkles" size={16} />
                          <p>{combo.combined_benefit}</p>
                        </div>
                        
                        <div className={styles.implementation}>
                          <h4>Implementation Order</h4>
                          <div className={styles.order}>
                            {combo.implementation_order.map((fw, idx) => (
                              <React.Fragment key={idx}>
                                <span className={styles.step}>
                                  <span className={styles.stepNumber}>{idx + 1}</span>
                                  {fw}
                                </span>
                                {idx < combo.implementation_order.length - 1 && (
                                  <Icon name="arrow.right" size={14} />
                                )}
                              </React.Fragment>
                            ))}
                          </div>
                        </div>
                        
                        <div className={styles.impact}>
                          <Icon name="bolt.fill" size={16} />
                          <strong>Estimated Impact:</strong> {combo.estimated_impact}
                        </div>
                      </div>
                    </motion.div>
                  ))}
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
                  <h3>{selectedFramework.framework_name}</h3>
                  <button onClick={() => setSelectedFramework(null)}>
                    <Icon name="xmark" size={20} />
                  </button>
                </div>
                
                <div className={styles.modalBody}>
                  <div className={styles.modalSection}>
                    <h4>Implementation Tips</h4>
                    <ol>
                      {selectedFramework.implementation_tips.map((tip, idx) => (
                        <li key={idx}>{tip}</li>
                      ))}
                    </ol>
                  </div>
                  
                  <div className={styles.modalSection}>
                    <h4>Why This Framework?</h4>
                    <p>{selectedFramework.why_recommended}</p>
                  </div>
                  
                  <div className={styles.modalActions}>
                    <button className={styles.primaryButton}>
                      <Icon name="book" size={16} />
                      View Full Guide
                    </button>
                    <button className={styles.secondaryButton}>
                      <Icon name="square.and.arrow.down" size={16} />
                      Download Template
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

export { FrameworkIntelligence };