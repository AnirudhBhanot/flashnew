// Michelin Analysis View - Displays comprehensive strategic analysis
// Renders the full Michelin-style report with interactive sections

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  Target, 
  TrendingUp, 
  Users, 
  Map, 
  AlertTriangle,
  CheckCircle,
  ChevronRight,
  Download,
  Briefcase,
  Globe,
  Shield,
  Zap,
  Clock,
  BarChart3
} from 'lucide-react';
import { EnrichedAnalysisData } from '../../../types';
import { generateMichelinAnalysis, MichelinAnalysis } from '../../../services/strategicAnalysisEngine';
import './MichelinAnalysisView.css';

interface MichelinAnalysisViewProps {
  analysisData: EnrichedAnalysisData;
}

type SectionId = 'executive' | 'situation' | 'imperatives' | 'readiness' | 'roadmap' | 'risks' | 'recommendations';

const MichelinAnalysisView: React.FC<MichelinAnalysisViewProps> = ({ analysisData }) => {
  const [analysis, setAnalysis] = useState<MichelinAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<SectionId>('executive');
  const [expandedPhase, setExpandedPhase] = useState<number | null>(null);

  useEffect(() => {
    generateAnalysis();
  }, [analysisData]);

  const generateAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await generateMichelinAnalysis(analysisData);
      setAnalysis(result);
    } catch (err) {
      setError('Failed to generate strategic analysis');
      console.error('Michelin analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const sections: Array<{ id: SectionId; title: string; icon: any; description: string }> = [
    { id: 'executive', title: 'Executive Summary', icon: FileText, description: 'Strategic overview and key insights' },
    { id: 'situation', title: 'Situation Analysis', icon: Globe, description: 'Where are we now?' },
    { id: 'imperatives', title: 'Strategic Imperatives', icon: Target, description: 'Where do we need to go?' },
    { id: 'readiness', title: 'Organizational Readiness', icon: Users, description: '7S assessment and change readiness' },
    { id: 'roadmap', title: 'Transformation Roadmap', icon: Map, description: 'How do we get there?' },
    { id: 'risks', title: 'Risk Assessment', icon: Shield, description: 'What could go wrong?' },
    { id: 'recommendations', title: 'Board Recommendations', icon: Briefcase, description: 'Synthesis and next steps' }
  ];

  if (loading) {
    return (
      <div className="michelin-loading">
        <div className="loading-spinner" />
        <h3>Generating Strategic Analysis</h3>
        <p>Analyzing your startup through multiple strategic frameworks...</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="michelin-error">
        <AlertTriangle size={48} />
        <h3>Analysis Generation Failed</h3>
        <p>{error || 'Unable to generate analysis'}</p>
        <button onClick={generateAnalysis}>Retry</button>
      </div>
    );
  }

  return (
    <div className="michelin-analysis-container">
      {/* Header */}
      <div className="michelin-header">
        <div className="header-content">
          <h1>Strategic Analysis Report</h1>
          <p className="subtitle">Comprehensive Michelin-style strategic assessment</p>
        </div>
        <button className="download-button">
          <Download size={16} />
          Export PDF
        </button>
      </div>

      {/* Navigation */}
      <div className="michelin-navigation">
        {sections.map(section => (
          <button
            key={section.id}
            className={`nav-button ${activeSection === section.id ? 'active' : ''}`}
            onClick={() => setActiveSection(section.id)}
          >
            <section.icon size={20} />
            <div className="nav-text">
              <span className="nav-title">{section.title}</span>
              <span className="nav-description">{section.description}</span>
            </div>
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="michelin-content">
        <AnimatePresence mode="wait">
          {activeSection === 'executive' && (
            <motion.div
              key="executive"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <ExecutiveSummarySection summary={analysis.executiveSummary} />
            </motion.div>
          )}

          {activeSection === 'situation' && (
            <motion.div
              key="situation"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <SituationAnalysisSection situation={analysis.situationAnalysis} />
            </motion.div>
          )}

          {activeSection === 'imperatives' && (
            <motion.div
              key="imperatives"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <StrategicImperativesSection imperatives={analysis.strategicImperatives} />
            </motion.div>
          )}

          {activeSection === 'readiness' && (
            <motion.div
              key="readiness"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <OrganizationalReadinessSection readiness={analysis.organizationalReadiness} />
            </motion.div>
          )}

          {activeSection === 'roadmap' && (
            <motion.div
              key="roadmap"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <TransformationRoadmapSection 
                roadmap={analysis.transformationRoadmap}
                expandedPhase={expandedPhase}
                setExpandedPhase={setExpandedPhase}
              />
            </motion.div>
          )}

          {activeSection === 'risks' && (
            <motion.div
              key="risks"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <RiskAssessmentSection risks={analysis.riskAssessment} />
            </motion.div>
          )}

          {activeSection === 'recommendations' && (
            <motion.div
              key="recommendations"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="section-content"
            >
              <RecommendationsSection recommendations={analysis.synthesisRecommendations} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// Executive Summary Section
const ExecutiveSummarySection: React.FC<{ summary: any }> = ({ summary }) => (
  <div className="executive-summary">
    <div className="headline-box">
      <h2>{summary.headline}</h2>
      <div className={`urgency-badge ${summary.urgencyLevel}`}>
        <Clock size={16} />
        {summary.urgencyLevel.replace('-', ' ')} action required
      </div>
    </div>

    <div className="summary-grid">
      <div className="summary-card">
        <h3>Current Position</h3>
        <p>{summary.currentPosition}</p>
      </div>
      <div className="summary-card">
        <h3>Critical Challenge</h3>
        <p>{summary.criticalChallenge}</p>
      </div>
      <div className="summary-card">
        <h3>Strategic Opportunity</h3>
        <p>{summary.strategicOpportunity}</p>
      </div>
    </div>

    {summary.transformationRequired && (
      <div className="transformation-alert">
        <AlertTriangle />
        <div>
          <h4>Transformation Required</h4>
          <p>Your current trajectory requires fundamental strategic and organizational transformation to succeed.</p>
        </div>
      </div>
    )}
  </div>
);

// Situation Analysis Section
const SituationAnalysisSection: React.FC<{ situation: any }> = ({ situation }) => (
  <div className="situation-analysis">
    <div className="current-state">
      <h2>Where Are We Now?</h2>
      <div className="state-grid">
        <div className="state-card">
          <BarChart3 className="card-icon" />
          <h4>Market Position</h4>
          <p>{situation.whereAreWeNow.marketPosition}</p>
        </div>
        <div className="state-card">
          <Target className="card-icon" />
          <h4>Competitive Dynamics</h4>
          <p>{situation.whereAreWeNow.competitiveDynamics}</p>
        </div>
        <div className="state-card">
          <Zap className="card-icon" />
          <h4>Internal Capabilities</h4>
          <p>{situation.whereAreWeNow.internalCapabilities}</p>
        </div>
        <div className="state-card">
          <TrendingUp className="card-icon" />
          <h4>Financial Health</h4>
          <p>{situation.whereAreWeNow.financialHealth}</p>
        </div>
      </div>
    </div>

    <div className="analysis-sections">
      <div className="analysis-column">
        <h3>External Analysis</h3>
        <div className="analysis-group">
          <h4>Market Trends</h4>
          <ul>
            {situation.externalAnalysis.marketTrends.map((trend: string, i: number) => (
              <li key={i}>{trend}</li>
            ))}
          </ul>
        </div>
        <div className="analysis-group">
          <h4>Disruptive Threats</h4>
          <ul>
            {situation.externalAnalysis.disruptiveThreats.map((threat: string, i: number) => (
              <li key={i} className="threat">{threat}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="analysis-column">
        <h3>Internal Analysis</h3>
        <div className="analysis-group">
          <h4>Core Strengths</h4>
          <ul>
            {situation.internalAnalysis.coreStrengths.map((strength: string, i: number) => (
              <li key={i} className="strength">{strength}</li>
            ))}
          </ul>
        </div>
        <div className="analysis-group">
          <h4>Critical Weaknesses</h4>
          <ul>
            {situation.internalAnalysis.criticalWeaknesses.map((weakness: string, i: number) => (
              <li key={i} className="weakness">{weakness}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>

    <div className="swot-synthesis">
      <h3>SWOT Synthesis</h3>
      <div className="swot-grid">
        <div className="swot-quadrant strengths">
          <h4>Strengths</h4>
          {situation.swotSynthesis.strengths.map((item: string, i: number) => (
            <span key={i}>{item}</span>
          ))}
        </div>
        <div className="swot-quadrant weaknesses">
          <h4>Weaknesses</h4>
          {situation.swotSynthesis.weaknesses.map((item: string, i: number) => (
            <span key={i}>{item}</span>
          ))}
        </div>
        <div className="swot-quadrant opportunities">
          <h4>Opportunities</h4>
          {situation.swotSynthesis.opportunities.map((item: string, i: number) => (
            <span key={i}>{item}</span>
          ))}
        </div>
        <div className="swot-quadrant threats">
          <h4>Threats</h4>
          {situation.swotSynthesis.threats.map((item: string, i: number) => (
            <span key={i}>{item}</span>
          ))}
        </div>
      </div>
    </div>
  </div>
);

// Strategic Imperatives Section
const StrategicImperativesSection: React.FC<{ imperatives: any }> = ({ imperatives }) => (
  <div className="strategic-imperatives">
    <div className="vision-statement">
      <h2>Strategic Vision</h2>
      <p className="vision-text">{imperatives.visionStatement}</p>
    </div>

    <div className="strategic-choices">
      <h3>Key Strategic Choices</h3>
      {imperatives.strategicChoices.map((choice: any, i: number) => (
        <div key={i} className="choice-card">
          <div className="choice-header">
            <span className="choice-number">{i + 1}</span>
            <h4>{choice.choice}</h4>
          </div>
          <p className="rationale">{choice.rationale}</p>
          <div className="tradeoffs">
            <h5>Trade-offs:</h5>
            <ul>
              {choice.tradeoffs.map((tradeoff: string, j: number) => (
                <li key={j}>{tradeoff}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}
    </div>

    <div className="growth-strategy">
      <h3>Growth Strategy</h3>
      <div className="strategy-grid">
        <div className="strategy-item">
          <h4>Approach</h4>
          <p>{imperatives.growthStrategy.approach}</p>
        </div>
        <div className="strategy-item">
          <h4>Value Proposition</h4>
          <p>{imperatives.growthStrategy.valueProposition}</p>
        </div>
        <div className="strategy-item">
          <h4>Competitive Moat</h4>
          <p>{imperatives.growthStrategy.competitiveMoat}</p>
        </div>
        <div className="strategy-item">
          <h4>Target Markets</h4>
          <ul>
            {imperatives.growthStrategy.targetMarkets.map((market: string, i: number) => (
              <li key={i}>{market}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  </div>
);

// Organizational Readiness Section
const OrganizationalReadinessSection: React.FC<{ readiness: any }> = ({ readiness }) => (
  <div className="organizational-readiness">
    <div className="readiness-header">
      <h2>7S Organizational Assessment</h2>
      <div className="readiness-score">
        <span className="score-label">Change Readiness</span>
        <span className="score-value">{readiness.changeReadiness.score}/10</span>
      </div>
    </div>

    <div className="seven-s-grid">
      {Object.entries(readiness.sevenSAssessment).map(([element, assessment]: [string, any]) => (
        <div key={element} className="seven-s-card">
          <h4>{element.charAt(0).toUpperCase() + element.slice(1)}</h4>
          <div className="assessment-row">
            <span className="label">Current:</span>
            <span className="value">{assessment.current}</span>
          </div>
          <div className="assessment-row">
            <span className="label">Required:</span>
            <span className="value required">{assessment.required}</span>
          </div>
          <div className="gap-analysis">
            <strong>Gap:</strong> {assessment.gap}
          </div>
        </div>
      ))}
    </div>

    <div className="readiness-insights">
      <div className="insight-column">
        <h3>Change Strengths</h3>
        <ul>
          {readiness.changeReadiness.strengths.map((strength: string, i: number) => (
            <li key={i} className="positive">{strength}</li>
          ))}
        </ul>
      </div>
      <div className="insight-column">
        <h3>Change Barriers</h3>
        <ul>
          {readiness.changeReadiness.barriers.map((barrier: string, i: number) => (
            <li key={i} className="negative">{barrier}</li>
          ))}
        </ul>
      </div>
    </div>
  </div>
);

// Transformation Roadmap Section
const TransformationRoadmapSection: React.FC<{ 
  roadmap: any; 
  expandedPhase: number | null;
  setExpandedPhase: (phase: number | null) => void;
}> = ({ roadmap, expandedPhase, setExpandedPhase }) => (
  <div className="transformation-roadmap">
    <h2>Transformation Roadmap</h2>
    
    <div className="quick-wins">
      <h3>Quick Wins (30-60 Days)</h3>
      <div className="quick-wins-grid">
        {roadmap.quickWins.map((win: any, i: number) => (
          <div key={i} className="quick-win-card">
            <Zap className="win-icon" />
            <h4>{win.action}</h4>
            <p>{win.impact}</p>
            <div className="win-meta">
              <span>{win.timeframe}</span>
              <span>{win.owner}</span>
            </div>
          </div>
        ))}
      </div>
    </div>

    <div className="transformation-phases">
      <h3>Transformation Phases</h3>
      {roadmap.phases.map((phase: any) => (
        <div 
          key={phase.phase} 
          className={`phase-card ${expandedPhase === phase.phase ? 'expanded' : ''}`}
        >
          <div 
            className="phase-header"
            onClick={() => setExpandedPhase(expandedPhase === phase.phase ? null : phase.phase)}
          >
            <div className="phase-info">
              <span className="phase-number">Phase {phase.phase}</span>
              <h4>{phase.name}</h4>
              <span className="phase-duration">{phase.duration}</span>
            </div>
            <ChevronRight className={`expand-icon ${expandedPhase === phase.phase ? 'expanded' : ''}`} />
          </div>
          
          {expandedPhase === phase.phase && (
            <div className="phase-details">
              <div className="objectives">
                <h5>Objectives</h5>
                <ul>
                  {phase.objectives.map((obj: string, i: number) => (
                    <li key={i}>{obj}</li>
                  ))}
                </ul>
              </div>
              
              <div className="initiatives">
                <h5>Key Initiatives</h5>
                {phase.keyInitiatives.map((initiative: any, i: number) => (
                  <div key={i} className="initiative">
                    <h6>{initiative.initiative}</h6>
                    <div className="initiative-meta">
                      <span>Owner: {initiative.owner}</span>
                      <span>Resources: {initiative.resources}</span>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="milestones">
                <h5>Milestones</h5>
                <ul>
                  {phase.milestones.map((milestone: string, i: number) => (
                    <li key={i}>{milestone}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);

// Risk Assessment Section
const RiskAssessmentSection: React.FC<{ risks: any }> = ({ risks }) => {
  const getRiskIcon = (probability: string, impact: string) => {
    if (impact === 'critical' || (impact === 'major' && probability === 'high')) {
      return { icon: AlertTriangle, color: 'critical' };
    }
    if (impact === 'major' || probability === 'high') {
      return { icon: AlertTriangle, color: 'high' };
    }
    return { icon: Shield, color: 'medium' };
  };

  return (
    <div className="risk-assessment">
      <h2>Risk Assessment</h2>
      
      <div className="risk-categories">
        <div className="risk-category">
          <h3>Strategic Risks</h3>
          {risks.strategicRisks.map((risk: any, i: number) => {
            const { icon: Icon, color } = getRiskIcon(risk.probability, risk.impact);
            return (
              <div key={i} className={`risk-card ${color}`}>
                <Icon className="risk-icon" />
                <div className="risk-content">
                  <h4>{risk.risk}</h4>
                  <div className="risk-meta">
                    <span className="probability">Probability: {risk.probability}</span>
                    <span className="impact">Impact: {risk.impact}</span>
                  </div>
                  <p className="mitigation"><strong>Mitigation:</strong> {risk.mitigation}</p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="risk-category">
          <h3>Execution Risks</h3>
          {risks.executionRisks.map((risk: any, i: number) => {
            const { icon: Icon, color } = getRiskIcon(risk.probability, risk.impact);
            return (
              <div key={i} className={`risk-card ${color}`}>
                <Icon className="risk-icon" />
                <div className="risk-content">
                  <h4>{risk.risk}</h4>
                  <div className="risk-meta">
                    <span className="probability">Probability: {risk.probability}</span>
                    <span className="impact">Impact: {risk.impact}</span>
                  </div>
                  <p className="mitigation"><strong>Mitigation:</strong> {risk.mitigation}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mitigation-plan">
        <h3>Risk Mitigation Plan</h3>
        <div className="mitigation-grid">
          <div className="mitigation-section">
            <h4>Preventive Measures</h4>
            <ul>
              {risks.riskMitigationPlan.preventiveMeasures.map((measure: string, i: number) => (
                <li key={i}>{measure}</li>
              ))}
            </ul>
          </div>
          <div className="mitigation-section">
            <h4>Contingency Plans</h4>
            <ul>
              {risks.riskMitigationPlan.contingencyPlans.map((plan: string, i: number) => (
                <li key={i}>{plan}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Board Recommendations Section
const RecommendationsSection: React.FC<{ recommendations: any }> = ({ recommendations }) => (
  <div className="board-recommendations">
    <div className="board-summary">
      <h2>Board Recommendation</h2>
      <p className="recommendation-text">{recommendations.boardRecommendation}</p>
    </div>

    <div className="priority-actions">
      <h3>Priority Actions</h3>
      {recommendations.priorityActions.map((action: any, i: number) => (
        <div key={i} className="action-card">
          <div className="action-header">
            <span className="action-number">{i + 1}</span>
            <h4>{action.action}</h4>
            <span className="timeline">{action.timeline}</span>
          </div>
          <p className="rationale"><strong>Rationale:</strong> {action.rationale}</p>
          <p className="outcome"><strong>Expected Outcome:</strong> {action.expectedOutcome}</p>
        </div>
      ))}
    </div>

    <div className="success-metrics">
      <h3>Success Metrics</h3>
      <div className="metrics-table">
        <div className="metrics-header">
          <span>Metric</span>
          <span>Current</span>
          <span>Target</span>
          <span>Timeframe</span>
        </div>
        {recommendations.successMetrics.map((metric: any, i: number) => (
          <div key={i} className="metric-row">
            <span>{metric.metric}</span>
            <span className="current">{metric.current}</span>
            <span className="target">{metric.target}</span>
            <span>{metric.timeframe}</span>
          </div>
        ))}
      </div>
    </div>

    <div className="implementation-guidance">
      <h3>Implementation Guidance</h3>
      <div className="guidance-grid">
        <div className="guidance-item">
          <h4>Communication Strategy</h4>
          <p>{recommendations.implementationGuidance.communicationStrategy}</p>
        </div>
        <div className="guidance-item">
          <h4>Change Management</h4>
          <p>{recommendations.implementationGuidance.changeManagementApproach}</p>
        </div>
        <div className="guidance-item">
          <h4>Governance</h4>
          <p>{recommendations.implementationGuidance.governanceStructure}</p>
        </div>
      </div>
    </div>
  </div>
);

export default MichelinAnalysisView;