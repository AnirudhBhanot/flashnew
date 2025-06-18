import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Icon } from '../../../design-system/components';
import { RadarChart } from '../../../components/charts';
import styles from './index.module.scss';

interface PhaseData {
  phase1: {
    externalScore: number;
    internalScore: number;
    keyThreats: string[];
    keyStrengths: string[];
  };
  phase2: {
    visionGap: number;
    primaryStrategy: string;
    resourceAllocation: { [key: string]: number };
  };
  phase3: {
    alignmentScores: { [key: string]: number };
    topGaps: string[];
  };
  phase4: {
    bestCaseProb: number;
    baseCaseProb: number;
    worstCaseProb: number;
    topRisks: string[];
  };
}

interface Priority {
  id: string;
  title: string;
  impact: 'High' | 'Medium' | 'Low';
  effort: 'High' | 'Medium' | 'Low';
  timeframe: string;
  phase: string;
  description: string;
}

const Synthesis: React.FC = () => {
  const navigate = useNavigate();
  const [phaseData, setPhaseData] = useState<PhaseData | null>(null);
  const [priorities, setPriorities] = useState<Priority[]>([]);
  const [readinessScore, setReadinessScore] = useState(0);

  useEffect(() => {
    loadAllPhaseData();
  }, []);

  const loadAllPhaseData = () => {
    // Load data from all phases
    const phase1External = localStorage.getItem('externalRealityData');
    const phase1Internal = localStorage.getItem('internalAuditData');
    const phase2Vision = localStorage.getItem('visionRealityGapData');
    const phase2Ansoff = localStorage.getItem('ansoffMatrixData');
    const phase3SevenS = localStorage.getItem('sevenSFrameworkData');
    const phase4Scenario = localStorage.getItem('scenarioPlanningData');

    // Process Phase 1 data
    let externalScore = 0;
    let internalScore = 0;
    let keyThreats: string[] = [];
    let keyStrengths: string[] = [];

    if (phase1External) {
      const external = JSON.parse(phase1External);
      const forces = ['industryRivalry', 'customerPower', 'supplierPower', 'substituteThreat', 'newEntrants'];
      const totalScore = forces.reduce((sum, force) => sum + (external[force]?.score || 3), 0);
      externalScore = 100 - (totalScore / 25) * 100; // Convert threat level to opportunity score
      
      // Identify key threats
      forces.forEach(force => {
        if (external[force]?.score >= 4) {
          keyThreats.push(force.replace(/([A-Z])/g, ' $1').trim());
        }
      });
    }

    if (phase1Internal) {
      const internal = JSON.parse(phase1Internal);
      internalScore = internal.overallScore || 0;
      
      // Identify key strengths
      if (internal.capital > 70) keyStrengths.push('Strong Capital Position');
      if (internal.advantage > 70) keyStrengths.push('Competitive Advantage');
      if (internal.market > 70) keyStrengths.push('Market Position');
      if (internal.people > 70) keyStrengths.push('Strong Team');
    }

    // Process Phase 2 data
    let visionGap = 0;
    let primaryStrategy = '';
    let resourceAllocation: { [key: string]: number } = {};

    if (phase2Vision) {
      const vision = JSON.parse(phase2Vision);
      visionGap = vision.overallGap || 0;
    }

    if (phase2Ansoff) {
      const ansoff = JSON.parse(phase2Ansoff);
      resourceAllocation = {
        'Market Penetration': ansoff.marketPenetration?.resourceAllocation || 0,
        'Product Development': ansoff.productDevelopment?.resourceAllocation || 0,
        'Market Development': ansoff.marketDevelopment?.resourceAllocation || 0,
        'Diversification': ansoff.diversification?.resourceAllocation || 0
      };
      
      // Find primary strategy
      const maxAllocation = Math.max(...Object.values(resourceAllocation));
      primaryStrategy = Object.keys(resourceAllocation).find(key => resourceAllocation[key] === maxAllocation) || '';
    }

    // Process Phase 3 data
    let alignmentScores: { [key: string]: number } = {};
    let topGaps: string[] = [];

    if (phase3SevenS) {
      const sevenS = JSON.parse(phase3SevenS);
      const dimensions = ['strategy', 'structure', 'systems', 'sharedValues', 'style', 'staff', 'skills'];
      
      dimensions.forEach(dim => {
        alignmentScores[dim] = sevenS[dim]?.current || 0;
        const gap = (sevenS[dim]?.desired || 5) - (sevenS[dim]?.current || 0);
        if (gap >= 2) {
          topGaps.push(dim.charAt(0).toUpperCase() + dim.slice(1));
        }
      });
    }

    // Process Phase 4 data
    let bestCaseProb = 0;
    let baseCaseProb = 0;
    let worstCaseProb = 0;
    let topRisks: string[] = [];

    if (phase4Scenario) {
      const scenario = JSON.parse(phase4Scenario);
      if (scenario.scenarios) {
        scenario.scenarios.forEach((s: any) => {
          if (s.name === 'Best Case') bestCaseProb = s.probability || 0;
          if (s.name === 'Base Case') baseCaseProb = s.probability || 0;
          if (s.name === 'Worst Case') worstCaseProb = s.probability || 0;
        });
      }
      
      if (scenario.contingencyPlans) {
        topRisks = scenario.contingencyPlans.slice(0, 3).map((plan: any) => plan.trigger);
      }
    }

    const data: PhaseData = {
      phase1: { externalScore, internalScore, keyThreats, keyStrengths },
      phase2: { visionGap, primaryStrategy, resourceAllocation },
      phase3: { alignmentScores, topGaps },
      phase4: { bestCaseProb, baseCaseProb, worstCaseProb, topRisks }
    };

    setPhaseData(data);
    calculateReadinessScore(data);
    generatePriorities(data);
  };

  const calculateReadinessScore = (data: PhaseData) => {
    let score = 0;
    let weights = 0;

    // Phase 1 contribution (25%)
    score += (data.phase1.externalScore * 0.125);
    score += (data.phase1.internalScore * 0.125);
    weights += 25;

    // Phase 2 contribution (25%)
    score += ((100 - data.phase2.visionGap) * 0.25);
    weights += 25;

    // Phase 3 contribution (25%)
    const avgAlignment = Object.values(data.phase3.alignmentScores).reduce((a, b) => a + b, 0) / 
                        Object.values(data.phase3.alignmentScores).length;
    score += (avgAlignment * 20 * 0.25); // Convert 1-5 scale to percentage
    weights += 25;

    // Phase 4 contribution (25%)
    const riskAdjustedScore = (data.phase4.bestCaseProb * 100 + data.phase4.baseCaseProb * 70 + 
                              data.phase4.worstCaseProb * 30) / 100;
    score += (riskAdjustedScore * 0.25);
    weights += 25;

    setReadinessScore(Math.round(score));
  };

  const generatePriorities = (data: PhaseData) => {
    const priorities: Priority[] = [];

    // Phase 1 priorities
    if (data.phase1.externalScore < 50) {
      priorities.push({
        id: 'p1-1',
        title: 'Address High External Threats',
        impact: 'High',
        effort: 'High',
        timeframe: '3-6 months',
        phase: 'Phase 1',
        description: `Focus on mitigating: ${data.phase1.keyThreats.join(', ')}`
      });
    }

    if (data.phase1.internalScore < 60) {
      priorities.push({
        id: 'p1-2',
        title: 'Strengthen Internal Capabilities',
        impact: 'High',
        effort: 'Medium',
        timeframe: '2-4 months',
        phase: 'Phase 1',
        description: 'Improve CAMP scores, especially in weak areas'
      });
    }

    // Phase 2 priorities
    if (data.phase2.visionGap > 30) {
      priorities.push({
        id: 'p2-1',
        title: 'Bridge Vision-Reality Gap',
        impact: 'High',
        effort: 'High',
        timeframe: '6-12 months',
        phase: 'Phase 2',
        description: 'Align resources and capabilities with strategic vision'
      });
    }

    // Phase 3 priorities
    data.phase3.topGaps.forEach((gap, index) => {
      priorities.push({
        id: `p3-${index}`,
        title: `Improve ${gap} Alignment`,
        impact: index === 0 ? 'High' : 'Medium',
        effort: 'Medium',
        timeframe: '2-3 months',
        phase: 'Phase 3',
        description: `Address organizational misalignment in ${gap}`
      });
    });

    // Phase 4 priorities
    if (data.phase4.worstCaseProb > 30) {
      priorities.push({
        id: 'p4-1',
        title: 'Implement Risk Mitigation',
        impact: 'High',
        effort: 'High',
        timeframe: '1-2 months',
        phase: 'Phase 4',
        description: 'Activate contingency plans for high-probability risks'
      });
    }

    // Sort by impact and effort
    priorities.sort((a, b) => {
      const impactScore = { High: 3, Medium: 2, Low: 1 };
      const effortScore = { Low: 3, Medium: 2, High: 1 };
      const aScore = impactScore[a.impact] * effortScore[a.effort];
      const bScore = impactScore[b.impact] * effortScore[b.effort];
      return bScore - aScore;
    });

    setPriorities(priorities.slice(0, 5)); // Top 5 priorities
  };

  const getReadinessLevel = () => {
    if (readinessScore >= 80) return { level: 'Excellent', color: '#34c759' };
    if (readinessScore >= 60) return { level: 'Good', color: '#1d1d1f' };
    if (readinessScore >= 40) return { level: 'Fair', color: '#ff9500' };
    return { level: 'Needs Work', color: '#ff3b30' };
  };

  const getRadarData = () => {
    if (!phaseData) return null;

    return [{
      name: 'Strategic Readiness',
      values: {
        'External Environment': phaseData.phase1.externalScore,
        'Internal Capabilities': phaseData.phase1.internalScore,
        'Vision Alignment': 100 - phaseData.phase2.visionGap,
        'Organizational Readiness': Object.values(phaseData.phase3.alignmentScores)
          .reduce((a, b) => a + b, 0) / Object.values(phaseData.phase3.alignmentScores).length * 20,
        'Risk Management': (phaseData.phase4.bestCaseProb * 100 + phaseData.phase4.baseCaseProb * 70) / 100
      }
    }];
  };

  const handlePrint = () => {
    window.print();
  };

  if (!phaseData) {
    return (
      <div className={styles.loading}>
        <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
        <p>Synthesizing insights...</p>
      </div>
    );
  }

  const readinessLevel = getReadinessLevel();

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <motion.button
          className={styles.backButton}
          onClick={() => navigate('/deep-dive')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="arrow.left" size={20} />
          Back to Deep Dive
        </motion.button>
        
        <h1>Strategic Synthesis</h1>
        <p>Your comprehensive strategic roadmap based on deep dive analysis</p>
      </div>

      {/* Executive Summary */}
      <div className={styles.executiveSummary}>
        <div className={styles.summaryHeader}>
          <h2>Executive Summary</h2>
          <button onClick={handlePrint} className={styles.printButton}>
            <Icon name="printer" size={20} />
            Print Report
          </button>
        </div>

        <div className={styles.readinessCard}>
          <div className={styles.readinessScore}>
            <motion.div
              className={styles.scoreCircle}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', duration: 0.6 }}
            >
              <svg viewBox="0 0 200 200">
                <circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke="#f5f5f7"
                  strokeWidth="10"
                />
                <motion.circle
                  cx="100"
                  cy="100"
                  r="90"
                  fill="none"
                  stroke={readinessLevel.color}
                  strokeWidth="10"
                  strokeLinecap="round"
                  strokeDasharray={`${readinessScore * 5.65} 565`}
                  transform="rotate(-90 100 100)"
                  initial={{ strokeDasharray: '0 565' }}
                  animate={{ strokeDasharray: `${readinessScore * 5.65} 565` }}
                  transition={{ duration: 1, delay: 0.5 }}
                />
              </svg>
              <div className={styles.scoreText}>
                <span className={styles.scoreNumber}>{readinessScore}</span>
                <span className={styles.scoreLabel}>Strategic Readiness</span>
              </div>
            </motion.div>
          </div>
          
          <div className={styles.readinessDetails}>
            <h3>Overall Assessment: <span className={styles.readinessLevelText}>{readinessLevel.level}</span></h3>
            <p>
              Based on comprehensive analysis across all four phases, your organization shows 
              {readinessScore >= 60 ? ' strong' : ' developing'} strategic readiness with 
              {priorities.filter(p => p.impact === 'High').length} high-impact priorities to address.
            </p>
          </div>
        </div>
      </div>

      {/* Visual Dashboard */}
      <div className={styles.dashboard}>
        <h2>Strategic Dashboard</h2>
        
        <div className={styles.dashboardGrid}>
          <div className={styles.radarSection}>
            <h3>Multi-Dimensional Assessment</h3>
            {getRadarData() && <RadarChart data={getRadarData()!} size={300} />}
          </div>
          
          <div className={styles.metricsGrid}>
            <div className={styles.metricCard}>
              <Icon name="shield" size={24} />
              <h4>External Position</h4>
              <p className={styles.metricValue}>{phaseData.phase1.externalScore}%</p>
              <span className={styles.metricLabel}>Market Opportunity</span>
            </div>
            
            <div className={styles.metricCard}>
              <Icon name="building" size={24} />
              <h4>Internal Strength</h4>
              <p className={styles.metricValue}>{phaseData.phase1.internalScore}%</p>
              <span className={styles.metricLabel}>CAMP Score</span>
            </div>
            
            <div className={styles.metricCard}>
              <Icon name="target" size={24} />
              <h4>Vision Gap</h4>
              <p className={styles.metricValue}>{phaseData.phase2.visionGap}%</p>
              <span className={styles.metricLabel}>Reality Distance</span>
            </div>
            
            <div className={styles.metricCard}>
              <Icon name="chart.pie" size={24} />
              <h4>Success Probability</h4>
              <p className={styles.metricValue}>{phaseData.phase4.baseCaseProb}%</p>
              <span className={styles.metricLabel}>Base Case</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top Priorities */}
      <div className={styles.priorities}>
        <h2>Strategic Priorities</h2>
        <p className={styles.subtitle}>Top 5 actions ranked by impact and feasibility</p>
        
        <div className={styles.priorityList}>
          {priorities.map((priority, index) => (
            <motion.div
              key={priority.id}
              className={styles.priorityCard}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className={styles.priorityRank}>#{index + 1}</div>
              
              <div className={styles.priorityContent}>
                <h3>{priority.title}</h3>
                <p>{priority.description}</p>
                
                <div className={styles.priorityMeta}>
                  <span className={`${styles.tag} ${styles[`impact${priority.impact}`]}`}>
                    Impact: {priority.impact}
                  </span>
                  <span className={`${styles.tag} ${styles[`effort${priority.effort}`]}`}>
                    Effort: {priority.effort}
                  </span>
                  <span className={styles.timeframe}>
                    <Icon name="clock" size={14} />
                    {priority.timeframe}
                  </span>
                  <span className={styles.phase}>{priority.phase}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Implementation Roadmap */}
      <div className={styles.roadmap}>
        <h2>Implementation Roadmap</h2>
        
        <div className={styles.timeline}>
          <div className={styles.timelineHeader}>
            <span>Immediate (0-3 months)</span>
            <span>Short-term (3-6 months)</span>
            <span>Medium-term (6-12 months)</span>
          </div>
          
          <div className={styles.timelineContent}>
            <div className={styles.timelinePhase}>
              <h4>Quick Wins</h4>
              <ul>
                {priorities
                  .filter(p => p.timeframe.includes('1-') || p.timeframe.includes('2-'))
                  .map(p => <li key={p.id}>{p.title}</li>)}
              </ul>
            </div>
            
            <div className={styles.timelinePhase}>
              <h4>Build Momentum</h4>
              <ul>
                {priorities
                  .filter(p => p.timeframe.includes('3-') || p.timeframe.includes('4-'))
                  .map(p => <li key={p.id}>{p.title}</li>)}
              </ul>
            </div>
            
            <div className={styles.timelinePhase}>
              <h4>Strategic Transformation</h4>
              <ul>
                {priorities
                  .filter(p => p.timeframe.includes('6-') || p.timeframe.includes('12'))
                  .map(p => <li key={p.id}>{p.title}</li>)}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Success Metrics */}
      <div className={styles.metrics}>
        <h2>Success Metrics & KPIs</h2>
        
        <div className={styles.kpiGrid}>
          <div className={styles.kpiCard}>
            <h4>Financial KPIs</h4>
            <ul>
              <li>Monthly burn rate reduction: 20%</li>
              <li>Revenue growth: {phaseData.phase4.baseCaseProb > 50 ? '150%' : '100%'} YoY</li>
              <li>Gross margin improvement: 10pp</li>
            </ul>
          </div>
          
          <div className={styles.kpiCard}>
            <h4>Operational KPIs</h4>
            <ul>
              <li>Customer acquisition cost: -30%</li>
              <li>Time to market: -25%</li>
              <li>Employee productivity: +40%</li>
            </ul>
          </div>
          
          <div className={styles.kpiCard}>
            <h4>Strategic KPIs</h4>
            <ul>
              <li>Market share: +{phaseData.phase2.primaryStrategy === 'Market Penetration' ? '5%' : '3%'}</li>
              <li>NPS score: 70+</li>
              <li>Team alignment: 90%</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className={styles.navigation}>
        <motion.button
          className={styles.navButton}
          onClick={() => navigate('/deep-dive/phase4')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="arrow.left" size={16} />
          Back to Phase 4
        </motion.button>
        
        <motion.button
          className={styles.completeButton}
          onClick={() => {
            // Dispatch synthesis completion event
            window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
              detail: { phaseId: 'synthesis' } 
            }));
            // Navigate to results
            navigate('/results');
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Icon name="checkmark.circle.fill" size={16} />
          Complete Deep Dive
        </motion.button>
      </div>
    </div>
  );
};

export default Synthesis;