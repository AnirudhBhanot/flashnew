import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '../design-system/components';
import { FrameworkImplementation } from './FrameworkImplementation';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicIntelligence.module.scss';

interface FrameworkRecommendation {
  framework_id: string;
  framework_name: string;
  score: number;
  category: string;
  complexity: string;
  time_to_implement: string;
  description: string;
  why_recommended: string;
  key_benefits: string[];
  // Analysis preview
  position?: string;
  key_insight?: string;
  urgency?: 'high' | 'medium' | 'low';
}

interface FrameworkAnalysisPreview {
  framework_id: string;
  position: string;
  score?: number;
  key_insight: string;
  urgency: 'high' | 'medium' | 'low';
  top_action: string;
}

const FRAMEWORK_METADATA = {
  lean_startup: {
    icon: 'arrow.triangle.2.circlepath',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  bcg_matrix: {
    icon: 'square.grid.2x2',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  porters_five_forces: {
    icon: 'shield.lefthalf.filled',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  swot_analysis: {
    icon: 'square.split.2x2',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  value_chain: {
    icon: 'link',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  },
  business_model_canvas: {
    icon: 'rectangle.grid.3x2',
    gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)'
  },
  blue_ocean_strategy: {
    icon: 'water.waves',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  ansoff_matrix: {
    icon: 'arrow.up.right.square',
    gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
  },
  pestel_analysis: {
    icon: 'globe',
    gradient: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)'
  },
  jobs_to_be_done: {
    icon: 'person.fill.checkmark',
    gradient: 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)'
  }
};

export const StrategicIntelligence: React.FC = () => {
  const [recommendations, setRecommendations] = useState<FrameworkRecommendation[]>([]);
  const [analysisResults, setAnalysisResults] = useState<Map<string, FrameworkAnalysisPreview>>(new Map());
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [autoAnalyzing, setAutoAnalyzing] = useState(false);
  const [viewMode, setViewMode] = useState<'where-now' | 'where-go' | 'how-get-there'>('where-now');
  const assessmentData = useAssessmentStore(state => state.data);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Generate mock recommendations with preview data
      const mockRecommendations: FrameworkRecommendation[] = [
        {
          framework_id: 'bcg_matrix',
          framework_name: 'BCG Growth-Share Matrix',
          score: 0.95,
          category: 'Strategy',
          complexity: 'Intermediate',
          time_to_implement: '1-2 hours',
          description: 'Position your product portfolio based on market growth and share',
          why_recommended: 'Your high growth market (18% YoY) but low market share (3.2%) indicates critical strategic decisions needed',
          key_benefits: ['Clear strategic position', 'Investment prioritization', 'Portfolio decisions'],
          position: 'Question Mark',
          key_insight: 'High growth opportunity but requires significant investment to capture market share',
          urgency: 'high'
        },
        {
          framework_id: 'porters_five_forces',
          framework_name: "Porter's Five Forces",
          score: 0.88,
          category: 'Strategy',
          complexity: 'Advanced',
          time_to_implement: '2-3 hours',
          description: 'Analyze competitive forces shaping your industry',
          why_recommended: 'Multiple well-funded competitors and low barriers to entry threaten your position',
          key_benefits: ['Industry attractiveness', 'Competitive dynamics', 'Strategic positioning'],
          position: 'Moderate Attractiveness',
          key_insight: 'High competitive rivalry (4.2/5) suggests need for strong differentiation',
          urgency: 'high'
        },
        {
          framework_id: 'blue_ocean_strategy',
          framework_name: 'Blue Ocean Strategy',
          score: 0.82,
          category: 'Innovation',
          complexity: 'Advanced',
          time_to_implement: '3-4 hours',
          description: 'Find uncontested market spaces for growth',
          why_recommended: 'Current red ocean competition suggests exploring adjacent markets',
          key_benefits: ['Market creation', 'Competition irrelevance', 'Value innovation'],
          position: 'Red Ocean',
          key_insight: '3 untapped market segments identified with 2x pricing potential',
          urgency: 'medium'
        },
        {
          framework_id: 'lean_startup',
          framework_name: 'Lean Startup',
          score: 0.78,
          category: 'Innovation',
          complexity: 'Basic',
          time_to_implement: '2-4 weeks per cycle',
          description: 'Rapid experimentation and validated learning',
          why_recommended: 'Early stage requires rapid iteration and market validation',
          key_benefits: ['Faster learning', 'Reduced waste', 'Market validation'],
          position: 'Build-Measure-Learn',
          key_insight: 'Current burn rate allows 8-10 experiment cycles before funding needed',
          urgency: 'medium'
        },
        {
          framework_id: 'swot_analysis',
          framework_name: 'SWOT Analysis',
          score: 0.75,
          category: 'Strategy',
          complexity: 'Basic',
          time_to_implement: '1-2 hours',
          description: 'Comprehensive view of internal and external factors',
          why_recommended: 'Baseline strategic assessment for funding and planning',
          key_benefits: ['Holistic view', 'Quick assessment', 'Strategic clarity'],
          position: 'Growth Stage',
          key_insight: 'Strong tech capabilities offset by weak market presence',
          urgency: 'low'
        }
      ];

      setRecommendations(mockRecommendations);
      
      // Auto-analyze top 3 frameworks
      setTimeout(() => {
        autoAnalyzeTopFrameworks(mockRecommendations.slice(0, 3));
      }, 500);
      
    } catch (error) {
      console.error('Error loading recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const autoAnalyzeTopFrameworks = async (topFrameworks: FrameworkRecommendation[]) => {
    setAutoAnalyzing(true);
    
    for (const framework of topFrameworks) {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const preview: FrameworkAnalysisPreview = {
        framework_id: framework.framework_id,
        position: framework.position || 'Analyzing...',
        score: framework.score,
        key_insight: framework.key_insight || 'Analysis in progress...',
        urgency: framework.urgency || 'medium',
        top_action: getTopAction(framework.framework_id)
      };
      
      setAnalysisResults(prev => new Map(prev).set(framework.framework_id, preview));
    }
    
    setAutoAnalyzing(false);
  };

  const getTopAction = (frameworkId: string): string => {
    const actions: Record<string, string> = {
      bcg_matrix: 'Double marketing budget to capture market share',
      porters_five_forces: 'Build switching costs through proprietary integrations',
      blue_ocean_strategy: 'Validate untapped segment with 50 customers',
      lean_startup: 'Launch MVP for highest-risk assumption within 2 weeks',
      swot_analysis: 'Leverage technical strengths for market expansion'
    };
    return actions[frameworkId] || 'Review detailed analysis for actions';
  };

  const getSynthesisInsights = () => {
    const analyzed = Array.from(analysisResults.values());
    if (analyzed.length < 3) return null;

    const highUrgency = analyzed.filter(a => a.urgency === 'high').length;
    const consensus = analyzed.filter(a => 
      a.key_insight.includes('market share') || 
      a.key_insight.includes('competition')
    ).length;

    return {
      overallAssessment: highUrgency >= 2 ? 'Critical Strategic Juncture' : 'Strategic Optimization Needed',
      consensusTheme: consensus >= 2 ? 'Market Position & Competition' : 'Mixed Strategic Signals',
      urgencyLevel: highUrgency >= 2 ? 'high' : 'medium',
      keyPattern: 'Multiple frameworks indicate need for aggressive market share capture',
      synthesizedAction: 'Focus 70% of resources on customer acquisition in next 6 months'
    };
  };

  const getFrameworkIcon = (frameworkId: string) => {
    return FRAMEWORK_METADATA[frameworkId]?.icon || 'square.grid.2x2';
  };

  const getFrameworkGradient = (frameworkId: string) => {
    return FRAMEWORK_METADATA[frameworkId]?.gradient || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h2>Strategic Intelligence Engine</h2>
          <p className={styles.subtitle}>
            AI-powered framework analysis tailored to your startup's specific situation
          </p>
        </div>
        
        <div className={styles.controls}>
          <button
            className={`${styles.viewToggle} ${viewMode === 'where-now' ? styles.active : ''}`}
            onClick={() => setViewMode('where-now')}
          >
            <Icon name="location.circle" size={16} />
            Where Are We Now?
          </button>
          <button
            className={`${styles.viewToggle} ${viewMode === 'where-go' ? styles.active : ''}`}
            onClick={() => setViewMode('where-go')}
          >
            <Icon name="target" size={16} />
            Where Should We Go?
          </button>
          <button
            className={`${styles.viewToggle} ${viewMode === 'how-get-there' ? styles.active : ''}`}
            onClick={() => setViewMode('how-get-there')}
          >
            <Icon name="map" size={16} />
            How to Get There?
          </button>
        </div>
      </div>

      {autoAnalyzing && (
        <motion.div 
          className={styles.autoAnalyzing}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Icon name="wand.and.stars" size={20} />
          <span>Auto-analyzing top frameworks for immediate insights...</span>
        </motion.div>
      )}

      {isLoading ? (
        <div className={styles.loading}>
          <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
          <p>Analyzing your strategic position...</p>
        </div>
      ) : (
        <AnimatePresence mode="wait">
          {viewMode === 'grid' ? (
            <motion.div 
              key="grid"
              className={styles.frameworkGrid}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {recommendations.map((framework, index) => {
                const analysis = analysisResults.get(framework.framework_id);
                const hasAnalysis = !!analysis;
                
                return (
                  <motion.div
                    key={framework.framework_id}
                    className={`${styles.frameworkCard} ${hasAnalysis ? styles.analyzed : ''}`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => setSelectedFramework(framework.framework_id)}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div 
                      className={styles.cardHeader}
                      style={{ background: getFrameworkGradient(framework.framework_id) }}
                    >
                      <Icon name={getFrameworkIcon(framework.framework_id)} size={24} />
                      <div className={styles.matchScore}>
                        <span className={styles.scoreValue}>{Math.round(framework.score * 100)}%</span>
                        <span className={styles.scoreLabel}>Match</span>
                      </div>
                    </div>
                    
                    <div className={styles.cardContent}>
                      <h3>{framework.framework_name}</h3>
                      
                      {hasAnalysis ? (
                        <motion.div 
                          className={styles.analysisPreview}
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                        >
                          <div className={styles.position}>
                            <Icon name="location.fill" size={16} />
                            <span>Your Position: <strong>{analysis.position}</strong></span>
                          </div>
                          
                          <div className={styles.insight}>
                            <p>{analysis.key_insight}</p>
                          </div>
                          
                          <div className={styles.urgencyBadge} style={{ 
                            backgroundColor: getUrgencyColor(analysis.urgency) 
                          }}>
                            {analysis.urgency} priority
                          </div>
                          
                          <div className={styles.topAction}>
                            <Icon name="bolt.fill" size={14} />
                            <span>{analysis.top_action}</span>
                          </div>
                        </motion.div>
                      ) : (
                        <div className={styles.description}>
                          <p>{framework.why_recommended}</p>
                        </div>
                      )}
                      
                      <button className={styles.analyzeButton}>
                        {hasAnalysis ? 'View Full Analysis' : 'Analyze Now'}
                        <Icon name="arrow.right" size={16} />
                      </button>
                    </div>
                    
                    {index < 3 && (
                      <div className={styles.topFrameworkBadge}>
                        <Icon name="star.fill" size={12} />
                        Top Match
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </motion.div>
          ) : (
            <motion.div
              key="synthesis"
              className={styles.synthesisView}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {getSynthesisInsights() ? (
                <div className={styles.synthesisContent}>
                  <div className={styles.synthesisHeader}>
                    <Icon name="brain" size={48} />
                    <h3>{getSynthesisInsights()!.overallAssessment}</h3>
                    <p>Based on analysis across {analysisResults.size} strategic frameworks</p>
                  </div>
                  
                  <div className={styles.synthesisGrid}>
                    <div className={styles.synthesisCard}>
                      <h4>Consensus Theme</h4>
                      <p>{getSynthesisInsights()!.consensusTheme}</p>
                    </div>
                    
                    <div className={styles.synthesisCard}>
                      <h4>Key Pattern</h4>
                      <p>{getSynthesisInsights()!.keyPattern}</p>
                    </div>
                    
                    <div className={styles.synthesisCard}>
                      <h4>Unified Action</h4>
                      <p>{getSynthesisInsights()!.synthesizedAction}</p>
                    </div>
                  </div>
                  
                  <div className={styles.frameworkComparison}>
                    <h4>Framework Positions</h4>
                    <div className={styles.comparisonGrid}>
                      {Array.from(analysisResults.entries()).map(([id, analysis]) => {
                        const framework = recommendations.find(r => r.framework_id === id);
                        if (!framework) return null;
                        
                        return (
                          <div key={id} className={styles.comparisonItem}>
                            <Icon name={getFrameworkIcon(id)} size={20} />
                            <div>
                              <strong>{framework.framework_name}</strong>
                              <p>{analysis.position}</p>
                            </div>
                            <div 
                              className={styles.urgencyDot} 
                              style={{ backgroundColor: getUrgencyColor(analysis.urgency) }}
                            />
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              ) : (
                <div className={styles.synthesisEmpty}>
                  <Icon name="hourglass" size={48} />
                  <p>Analyzing frameworks to generate synthesis...</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      )}

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
              <FrameworkImplementation 
                frameworkId={selectedFramework}
                onClose={() => setSelectedFramework(null)}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default StrategicIntelligence;