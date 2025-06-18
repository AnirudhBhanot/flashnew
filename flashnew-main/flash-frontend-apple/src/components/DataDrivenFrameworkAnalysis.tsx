import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import { Icon } from '../design-system/components';
import { analyzeFrameworks, FrameworkAnalysisResult, DataDrivenRecommendation } from '../services/dataAnalysisEngine';
import styles from './DataDrivenFrameworkAnalysis.module.scss';

// Enhanced BCG Matrix Visualization with actual data points
const BCGMatrixVisualization: React.FC<{ data: FrameworkAnalysisResult }> = ({ data }) => {
  const { xValue, yValue, quadrant } = data.quantifiedPosition;
  const metrics = data.metrics;
  
  // Calculate position with actual relative market share (log scale)
  const logX = Math.log10(Math.max(0.01, xValue));
  const xPos = Math.min(95, Math.max(5, 50 + (logX * 25)));
  const yPos = Math.min(95, Math.max(5, (yValue / 40) * 90 + 5));
  
  return (
    <div className={styles.bcgMatrix}>
      <div className={styles.matrixGrid}>
        <div className={styles.quadrant} data-quadrant="star">
          <span>Star</span>
          <p>High Growth, High Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="question">
          <span>Question Mark</span>
          <p>High Growth, Low Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="cash-cow">
          <span>Cash Cow</span>
          <p>Low Growth, High Share</p>
        </div>
        <div className={styles.quadrant} data-quadrant="dog">
          <span>Dog</span>
          <p>Low Growth, Low Share</p>
        </div>
        
        {/* Your position with actual metrics */}
        <motion.div 
          className={styles.position}
          initial={{ scale: 0 }}
          animate={{ 
            scale: 1,
            left: `${xPos}%`,
            bottom: `${yPos}%`
          }}
          transition={{ type: "spring", stiffness: 100 }}
        >
          <div className={styles.positionDot} />
          <span className={styles.positionLabel}>
            You
            <span className={styles.positionMetrics}>
              {metrics.absoluteMarketShare}% share
              <br />
              {metrics.marketGrowthRate}% growth
            </span>
          </span>
        </motion.div>
        
        {/* Competitor positions */}
        {data.visualizationData.competitorPositions?.map((competitor, idx) => (
          <div
            key={idx}
            className={styles.competitor}
            style={{
              left: `${Math.min(95, Math.max(5, 50 + (Math.log10(competitor.x) * 25)))}%`,
              bottom: `${Math.min(95, Math.max(5, (competitor.y / 40) * 90 + 5))}%`,
              transform: `scale(${0.5 + competitor.size / 200})`
            }}
          >
            <div className={styles.competitorDot} />
            <span className={styles.competitorLabel}>{competitor.name}</span>
          </div>
        ))}
      </div>
      
      <div className={styles.axisLabels}>
        <span className={styles.xLabel}>
          Relative Market Share →
          <span className={styles.axisScale}>0.1x &nbsp;&nbsp;&nbsp; 1x &nbsp;&nbsp;&nbsp; 10x</span>
        </span>
        <span className={styles.yLabel}>
          Market Growth Rate →
          <span className={styles.axisScale}>0% &nbsp; 20% &nbsp; 40%</span>
        </span>
      </div>
      
      {/* Key metrics display */}
      <div className={styles.metricsPanel}>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Your Market Share</span>
          <span className={styles.metricValue}>{metrics.absoluteMarketShare}%</span>
        </div>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Relative Share</span>
          <span className={styles.metricValue}>{metrics.relativeMarketShare}x</span>
        </div>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Market Size</span>
          <span className={styles.metricValue}>${(metrics.marketSize / 1000000000).toFixed(1)}B</span>
        </div>
      </div>
    </div>
  );
};

// Enhanced Porter's Five Forces with quantified scores
const FiveForcesVisualization: React.FC<{ data: FrameworkAnalysisResult }> = ({ data }) => {
  const forces = data.metrics;
  const overallScore = data.quantifiedPosition.xValue;
  
  return (
    <div className={styles.fiveForces}>
      <div className={styles.forcesCenter}>
        <h4>Industry Attractiveness</h4>
        <div className={styles.attractivenessScore}>
          <div className={styles.scoreValue}>{(overallScore * 100).toFixed(0)}%</div>
          <div className={styles.scoreLabel}>{data.position}</div>
        </div>
        <div className={styles.percentile}>
          Top {100 - (data.quantifiedPosition.percentile || 50)}% of industries
        </div>
      </div>
      
      {Object.entries(forces).map(([force, details]: any) => (
        <div key={force} className={`${styles.force} ${styles[force]}`}>
          <h5>{force.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h5>
          <div className={styles.forceLevel} data-level={details.level?.toLowerCase()}>
            {details.level}
          </div>
          <div className={styles.forceScore}>
            <div 
              className={styles.scoreBar}
              style={{ width: `${(1 - details.score) * 100}%` }}
            />
            <span className={styles.scoreText}>{(details.score * 100).toFixed(0)}%</span>
          </div>
          {details.factors && details.factors.length > 0 && (
            <ul className={styles.forceFactors}>
              {details.factors.map((factor: string, i: number) => (
                <li key={i}>{factor}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
};

// Enhanced SWOT Matrix with quantified elements
const SWOTVisualization: React.FC<{ data: FrameworkAnalysisResult }> = ({ data }) => {
  const swot = data.visualizationData;
  const metrics = data.metrics;
  
  return (
    <div className={styles.swotContainer}>
      <div className={styles.swotMatrix}>
        <div className={styles.swotQuadrant} data-type="strengths">
          <h5>Strengths ({metrics.strengthCount})</h5>
          <ul>
            {swot.strengths?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
        <div className={styles.swotQuadrant} data-type="weaknesses">
          <h5>Weaknesses ({metrics.weaknessCount})</h5>
          <ul>
            {swot.weaknesses?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
        <div className={styles.swotQuadrant} data-type="opportunities">
          <h5>Opportunities ({metrics.opportunityCount})</h5>
          <ul>
            {swot.opportunities?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
        <div className={styles.swotQuadrant} data-type="threats">
          <h5>Threats ({metrics.threatCount})</h5>
          <ul>
            {swot.threats?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className={styles.swotSummary}>
        <h4>Strategic Position</h4>
        <div className={styles.positionIndicator}>
          <div className={styles.netPosition}>
            Net Position Score: <strong>{metrics.netPosition > 0 ? '+' : ''}{metrics.netPosition}</strong>
          </div>
          <p>{data.position}</p>
        </div>
      </div>
    </div>
  );
};

// Data-driven recommendation card
const RecommendationCard: React.FC<{ recommendation: DataDrivenRecommendation }> = ({ recommendation }) => {
  return (
    <div className={styles.recommendationCard}>
      <div className={styles.recommendationHeader}>
        <h4>{recommendation.action}</h4>
        <div className={styles.confidence}>
          <Icon name="chart.bar.fill" size={16} />
          {recommendation.confidenceLevel}% confidence
        </div>
      </div>
      
      <div className={styles.recommendationBody}>
        <div className={styles.targetSection}>
          <h5>Specific Target</h5>
          <p>{recommendation.specificTarget}</p>
        </div>
        
        <div className={styles.currentSection}>
          <h5>Current State</h5>
          <p>{recommendation.currentState}</p>
        </div>
        
        <div className={styles.impactSection}>
          <h5>Expected Impact</h5>
          <p>{recommendation.expectedImpact}</p>
        </div>
        
        <div className={styles.metricsRow}>
          <div className={styles.metric}>
            <Icon name="clock" size={16} />
            <span>{recommendation.timeframe}</span>
          </div>
          {recommendation.requiredInvestment && (
            <div className={styles.metric}>
              <Icon name="dollarsign.circle" size={16} />
              <span>${(recommendation.requiredInvestment / 1000).toFixed(0)}K investment</span>
            </div>
          )}
          {recommendation.roi && (
            <div className={styles.metric}>
              <Icon name="arrow.up.right.circle" size={16} />
              <span>{recommendation.roi.toFixed(1)}x ROI</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export const DataDrivenFrameworkAnalysis: React.FC = () => {
  const [activePhase, setActivePhase] = useState<'situation' | 'strategy' | 'execution'>('situation');
  const [analyses, setAnalyses] = useState<Record<string, FrameworkAnalysisResult[]>>({
    situation: [],
    strategy: [],
    execution: []
  });
  const [isLoading, setIsLoading] = useState(true);
  
  const assessmentData = useAssessmentStore(state => state.data);

  useEffect(() => {
    if (assessmentData) {
      loadAnalyses();
    }
  }, [assessmentData]);

  const loadAnalyses = async () => {
    setIsLoading(true);
    
    // Define frameworks for each phase
    const phaseFrameworks = {
      situation: ['bcg_matrix', 'porters_five_forces', 'swot_analysis'],
      strategy: ['ansoff_matrix', 'blue_ocean', 'value_chain'],
      execution: ['lean_canvas', 'balanced_scorecard', 'okr_framework']
    };

    try {
      // Analyze frameworks for each phase using the data-driven engine
      const newAnalyses: Record<string, FrameworkAnalysisResult[]> = {
        situation: [],
        strategy: [],
        execution: []
      };
      
      // Analyze situation phase
      newAnalyses.situation = analyzeFrameworks(assessmentData, phaseFrameworks.situation);
      
      // Analyze strategy phase
      newAnalyses.strategy = analyzeFrameworks(assessmentData, phaseFrameworks.strategy);
      
      // For execution phase, we'll use the existing frameworks for now
      // In a full implementation, you'd add more framework analyses to the engine
      newAnalyses.execution = [];
      
      setAnalyses(newAnalyses);
    } catch (error) {
      console.error('Error loading analyses:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getVisualization = (analysis: FrameworkAnalysisResult) => {
    switch (analysis.frameworkId) {
      case 'bcg_matrix':
        return <BCGMatrixVisualization data={analysis} />;
      case 'porters_five_forces':
        return <FiveForcesVisualization data={analysis} />;
      case 'swot_analysis':
        return <SWOTVisualization data={analysis} />;
      default:
        return null;
    }
  };

  const renderPhaseContent = () => {
    const phaseData = analyses[activePhase] || [];
    
    if (isLoading) {
      return (
        <div className={styles.loading}>
          <Icon name="arrow.trianglehead.clockwise" size={32} />
          <p>Analyzing your business with real data...</p>
        </div>
      );
    }

    return (
      <div className={styles.phaseContent}>
        <div className={styles.phaseHeader}>
          <h2>
            {activePhase === 'situation' && 'Where Are We Now?'}
            {activePhase === 'strategy' && 'Where Should We Go?'}
            {activePhase === 'execution' && 'How to Get There?'}
          </h2>
          <p>
            {activePhase === 'situation' && 'Data-driven analysis of your current position'}
            {activePhase === 'strategy' && 'Quantified strategic options based on your metrics'}
            {activePhase === 'execution' && 'Specific implementation plans with measurable targets'}
          </p>
        </div>

        <div className={styles.frameworkAnalyses}>
          {phaseData.map((analysis: FrameworkAnalysisResult, index: number) => (
            <motion.div
              key={analysis.frameworkId}
              className={styles.frameworkSection}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <div className={styles.frameworkHeader}>
                <h3>{analysis.frameworkName}</h3>
                <div className={styles.position}>
                  <Icon name="location.fill" size={16} />
                  <span>{analysis.position}</span>
                  {analysis.quantifiedPosition.percentile && (
                    <span className={styles.percentile}>
                      (Top {100 - analysis.quantifiedPosition.percentile}%)
                    </span>
                  )}
                </div>
              </div>

              {/* Framework Visualization */}
              {getVisualization(analysis) && (
                <div className={styles.visualization}>
                  {getVisualization(analysis)}
                </div>
              )}

              {/* Quantified Insights */}
              <div className={styles.insights}>
                <h4>Data-Driven Insights</h4>
                <ul>
                  {analysis.insights.map((insight: string, i: number) => (
                    <li key={i}>
                      <Icon name="lightbulb.fill" size={16} />
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Specific Recommendations */}
              <div className={styles.recommendations}>
                <h4>Actionable Recommendations</h4>
                <div className={styles.recommendationsList}>
                  {analysis.recommendations.map((rec: DataDrivenRecommendation, i: number) => (
                    <RecommendationCard key={i} recommendation={rec} />
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Phase Summary with Metrics */}
        {phaseData.length > 0 && (
          <div className={styles.phaseSummary}>
            <h3>
              {activePhase === 'situation' && 'Situation Summary'}
              {activePhase === 'strategy' && 'Strategic Direction'}
              {activePhase === 'execution' && 'Implementation Priorities'}
            </h3>
            <div className={styles.summaryContent}>
              <div className={styles.keyMetrics}>
                <h4>Key Performance Indicators</h4>
                <div className={styles.metricsGrid}>
                  {activePhase === 'situation' && (
                    <>
                      <div className={styles.kpi}>
                        <span className={styles.kpiLabel}>Market Position</span>
                        <span className={styles.kpiValue}>{phaseData[0]?.position || 'Analyzing...'}</span>
                      </div>
                      <div className={styles.kpi}>
                        <span className={styles.kpiLabel}>Industry Attractiveness</span>
                        <span className={styles.kpiValue}>
                          {phaseData[1]?.quantifiedPosition?.xValue 
                            ? `${(phaseData[1].quantifiedPosition.xValue * 100).toFixed(0)}%` 
                            : 'Analyzing...'}
                        </span>
                      </div>
                      <div className={styles.kpi}>
                        <span className={styles.kpiLabel}>Strategic Health</span>
                        <span className={styles.kpiValue}>
                          {phaseData[2]?.metrics?.netPosition !== undefined
                            ? `${phaseData[2].metrics.netPosition > 0 ? '+' : ''}${phaseData[2].metrics.netPosition}`
                            : 'Analyzing...'}
                        </span>
                      </div>
                    </>
                  )}
                </div>
              </div>
              
              <div className={styles.priorityActions}>
                <h4>Top 3 Priority Actions</h4>
                <ol>
                  {phaseData
                    .flatMap(analysis => analysis.recommendations)
                    .sort((a, b) => (b.roi || 0) - (a.roi || 0))
                    .slice(0, 3)
                    .map((rec, i) => (
                      <li key={i}>
                        <strong>{rec.action}</strong>
                        <br />
                        Target: {rec.specificTarget}
                        <br />
                        Expected ROI: {rec.roi ? `${rec.roi.toFixed(1)}x` : 'TBD'}
                      </li>
                    ))}
                </ol>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={styles.container}>
      {/* Phase Navigation */}
      <div className={styles.phaseNav}>
        <button
          className={`${styles.phaseButton} ${activePhase === 'situation' ? styles.active : ''}`}
          onClick={() => setActivePhase('situation')}
        >
          <span className={styles.number}>1</span>
          <div className={styles.phaseInfo}>
            <h4>Where Are We Now?</h4>
            <p>Data-Driven Situation Analysis</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'strategy' ? styles.active : ''}`}
          onClick={() => setActivePhase('strategy')}
        >
          <span className={styles.number}>2</span>
          <div className={styles.phaseInfo}>
            <h4>Where Should We Go?</h4>
            <p>Quantified Strategic Options</p>
          </div>
        </button>
        
        <div className={styles.phaseSeparator} />
        
        <button
          className={`${styles.phaseButton} ${activePhase === 'execution' ? styles.active : ''}`}
          onClick={() => setActivePhase('execution')}
        >
          <span className={styles.number}>3</span>
          <div className={styles.phaseInfo}>
            <h4>How to Get There?</h4>
            <p>Specific Implementation Plan</p>
          </div>
        </button>
      </div>

      {/* Phase Content */}
      {renderPhaseContent()}
    </div>
  );
};