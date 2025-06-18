// Strategic Intelligence Component
// PhD-level framework analysis applied to actual startup data

import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Target, 
  TrendingUp, 
  Shield, 
  Users, 
  AlertCircle,
  ChevronRight,
  Brain,
  Lightbulb,
  BarChart3,
  Layers
} from 'lucide-react';
import { EnrichedAnalysisData } from '../../../types.js';
import { analyzeFramework, FrameworkAnalysis } from '../../../services/frameworkAnalysisEngine';
import { FrameworkVisualization } from './FrameworkVisualization';
import './StrategicIntelligence.css';

interface StrategicIntelligenceProps {
  analysisData: EnrichedAnalysisData;
}

interface FrameworkResult extends FrameworkAnalysis {
  loading?: boolean;
  error?: string;
}

const CORE_FRAMEWORKS = [
  {
    id: 'bcg_matrix',
    name: 'BCG Growth-Share Matrix',
    description: 'Portfolio analysis positioning',
    icon: Target,
    color: '#007AFF'
  },
  {
    id: 'swot',
    name: 'SWOT Analysis',
    description: 'Strengths, Weaknesses, Opportunities, Threats',
    icon: Shield,
    color: '#34C759'
  },
  {
    id: 'porters_five_forces',
    name: "Porter's Five Forces",
    description: 'Industry competitive analysis',
    icon: BarChart3,
    color: '#FF3B30'
  }
];

const StrategicIntelligence: React.FC<StrategicIntelligenceProps> = ({ analysisData }) => {
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);
  const [showSynthesis, setShowSynthesis] = useState(false);
  const [frameworkResults, setFrameworkResults] = useState<Record<string, FrameworkResult>>({});

  // Auto-analyze top frameworks on mount
  useEffect(() => {
    CORE_FRAMEWORKS.forEach(framework => {
      analyzeFrameworkAsync(framework.id);
    });
  }, [analysisData]);

  const analyzeFrameworkAsync = async (frameworkId: string) => {
    setFrameworkResults(prev => ({
      ...prev,
      [frameworkId]: { ...prev[frameworkId], loading: true }
    }));

    try {
      const result = await analyzeFramework(frameworkId, analysisData);
      if (result) {
        setFrameworkResults(prev => ({
          ...prev,
          [frameworkId]: { ...result, loading: false }
        }));
      }
    } catch (error) {
      setFrameworkResults(prev => ({
        ...prev,
        [frameworkId]: { 
          ...prev[frameworkId], 
          loading: false, 
          error: 'Analysis failed' 
        }
      }));
    }
  };

  // Generate cross-framework synthesis
  const synthesis = useMemo(() => {
    const completedAnalyses = Object.values(frameworkResults).filter(
      r => !r.loading && !r.error && r.position
    );

    if (completedAnalyses.length < 2) return null;

    // Find consensus themes
    const allInsights = completedAnalyses.flatMap(a => a.insights || []);
    const criticalInsights = allInsights.filter(i => i.importance === 'critical');
    const highInsights = allInsights.filter(i => i.importance === 'high');

    // Extract common patterns
    const patterns = {
      strengths: [] as string[],
      weaknesses: [] as string[],
      opportunities: [] as string[],
      threats: [] as string[]
    };

    // Analyze BCG position
    const bcgAnalysis = frameworkResults['bcg_matrix'];
    if (bcgAnalysis?.position?.position) {
      const position = bcgAnalysis.position.position;
      if (position === 'Star') {
        patterns.strengths.push('Market leadership in growth segment');
      } else if (position === 'Question Mark') {
        patterns.opportunities.push('High growth market potential');
        patterns.weaknesses.push('Low market share needs improvement');
      }
    }

    // Analyze SWOT
    const swotAnalysis = frameworkResults['swot'];
    if (swotAnalysis?.visualizationData) {
      const { strengths, weaknesses, opportunities, threats } = swotAnalysis.visualizationData;
      patterns.strengths.push(...(strengths || []));
      patterns.weaknesses.push(...(weaknesses || []));
      patterns.opportunities.push(...(opportunities || []));
      patterns.threats.push(...(threats || []));
    }

    // Key recommendations
    const recommendations = criticalInsights
      .map(i => i.recommendation)
      .filter((r, i, arr) => arr.indexOf(r) === i) // Unique
      .slice(0, 3);

    return {
      consensusPosition: determineConsensusPosition(completedAnalyses),
      keyPatterns: patterns,
      criticalActions: recommendations,
      confidence: calculateSynthesisConfidence(completedAnalyses)
    };
  }, [frameworkResults]);

  const determineConsensusPosition = (analyses: FrameworkAnalysis[]): string => {
    const positions = analyses.map(a => a.position?.position).filter(Boolean);
    // Simple consensus logic - would be more sophisticated in production
    if (positions.includes('Question Mark') && positions.includes('Challenging')) {
      return 'Growth Opportunity with Challenges';
    }
    if (positions.includes('Star')) {
      return 'Strong Market Position';
    }
    return 'Strategic Pivot Needed';
  };

  const calculateSynthesisConfidence = (analyses: FrameworkAnalysis[]): number => {
    const confidences = analyses
      .map(a => a.position?.confidence || 0)
      .filter(c => c > 0);
    return confidences.reduce((a, b) => a + b, 0) / confidences.length;
  };

  return (
    <div className="strategic-intelligence">
      <div className="si-header">
        <div className="si-title-section">
          <Brain className="si-icon" />
          <div>
            <h2>Strategic Intelligence</h2>
            <p>AI-powered framework analysis of your startup position</p>
          </div>
        </div>
        <button 
          className={`si-synthesis-toggle ${showSynthesis ? 'active' : ''}`}
          onClick={() => setShowSynthesis(!showSynthesis)}
        >
          <Layers size={16} />
          {showSynthesis ? 'Individual Analysis' : 'Cross-Framework Synthesis'}
        </button>
      </div>

      <AnimatePresence mode="wait">
        {!showSynthesis ? (
          <motion.div
            key="frameworks"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="si-frameworks-grid"
          >
            {CORE_FRAMEWORKS.map(framework => {
              const result = frameworkResults[framework.id];
              const isAnalyzed = result && !result.loading && !result.error;
              const position = result?.position?.position;
              const keyInsight = result?.insights?.[0];

              return (
                <motion.div
                  key={framework.id}
                  className={`si-framework-card ${selectedFramework === framework.id ? 'selected' : ''}`}
                  onClick={() => setSelectedFramework(
                    selectedFramework === framework.id ? null : framework.id
                  )}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="si-card-header">
                    <div 
                      className="si-card-icon"
                      style={{ backgroundColor: `${framework.color}20`, color: framework.color }}
                    >
                      <framework.icon size={24} />
                    </div>
                    <div className="si-card-title">
                      <h3>{framework.name}</h3>
                      <p>{framework.description}</p>
                    </div>
                    {isAnalyzed && (
                      <div className="si-card-badge">Analyzed</div>
                    )}
                  </div>

                  {isAnalyzed && (
                    <div className="si-card-content">
                      <div className="si-position">
                        <span className="si-position-label">Position:</span>
                        <span className="si-position-value">{position}</span>
                      </div>
                      {keyInsight && (
                        <div className="si-insight">
                          <Lightbulb size={14} />
                          <span>{keyInsight.title}</span>
                        </div>
                      )}
                      {keyInsight?.importance === 'critical' && (
                        <div className="si-urgency critical">
                          <AlertCircle size={14} />
                          <span>Critical Action Required</span>
                        </div>
                      )}
                    </div>
                  )}

                  {result?.loading && (
                    <div className="si-card-loading">
                      <div className="si-spinner" />
                      <span>Analyzing...</span>
                    </div>
                  )}

                  <ChevronRight className="si-card-arrow" />
                </motion.div>
              );
            })}
          </motion.div>
        ) : (
          <motion.div
            key="synthesis"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="si-synthesis"
          >
            {synthesis ? (
              <>
                <div className="si-synthesis-header">
                  <h3>Cross-Framework Strategic Synthesis</h3>
                  <div className="si-confidence">
                    Confidence: {(synthesis.confidence * 100).toFixed(0)}%
                  </div>
                </div>

                <div className="si-consensus-position">
                  <h4>Consensus Strategic Position</h4>
                  <div className="si-position-box">
                    {synthesis.consensusPosition}
                  </div>
                </div>

                <div className="si-patterns-grid">
                  <div className="si-pattern-section strengths">
                    <h4>Key Strengths</h4>
                    <ul>
                      {synthesis.keyPatterns.strengths.slice(0, 3).map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="si-pattern-section opportunities">
                    <h4>Opportunities</h4>
                    <ul>
                      {synthesis.keyPatterns.opportunities.slice(0, 3).map((o, i) => (
                        <li key={i}>{o}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="si-critical-actions">
                  <h4>Critical Strategic Actions</h4>
                  {synthesis.criticalActions.map((action, i) => (
                    <div key={i} className="si-action-item">
                      <div className="si-action-number">{i + 1}</div>
                      <div className="si-action-text">{action}</div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="si-synthesis-loading">
                <p>Analyzing frameworks to generate synthesis...</p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Framework Detail Modal */}
      <AnimatePresence>
        {selectedFramework && frameworkResults[selectedFramework] && (
          <motion.div
            className="si-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedFramework(null)}
          >
            <motion.div
              className="si-modal"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={e => e.stopPropagation()}
            >
              <div className="si-modal-header">
                <h3>{frameworkResults[selectedFramework].frameworkName}</h3>
                <button onClick={() => setSelectedFramework(null)}>×</button>
              </div>
              
              <div className="si-modal-content">
                <FrameworkVisualization 
                  framework={selectedFramework}
                  analysis={frameworkResults[selectedFramework]}
                />
                
                <div className="si-insights-section">
                  <h4>Strategic Insights</h4>
                  {frameworkResults[selectedFramework].insights?.map((insight, i) => (
                    <div key={i} className={`si-insight-card ${insight.importance}`}>
                      <h5>{insight.title}</h5>
                      <p>{insight.description}</p>
                      <div className="si-insight-data">
                        {insight.dataPoints.map((point, j) => (
                          <span key={j}>{point}</span>
                        ))}
                      </div>
                      <div className="si-recommendation">
                        <strong>Recommendation:</strong> {insight.recommendation}
                      </div>
                    </div>
                  ))}
                </div>

                {frameworkResults[selectedFramework].actions && (
                  <div className="si-actions-section">
                    <h4>Recommended Actions</h4>
                    {frameworkResults[selectedFramework].actions.map((action, i) => (
                      <div key={i} className="si-action-card">
                        <div className="si-action-header">
                          <h5>{action.title}</h5>
                          <div className={`si-priority ${action.priority}`}>
                            {action.priority}
                          </div>
                        </div>
                        <p>{action.description}</p>
                        <div className="si-action-meta">
                          <span>Effort: {action.effort}</span>
                          <span>Impact: {action.impact}</span>
                          <span>Timeframe: {action.timeframe}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default StrategicIntelligence;