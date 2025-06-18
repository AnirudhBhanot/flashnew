import React, { useState, useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { Button, Icon } from '../../design-system/components';
import { GaugeChart, RadarChart, ScoreBarChart } from '../../components/charts';
import { EnhancedInsights } from '../../components/EnhancedInsights';
import { EnhancedAnalysis } from '../../components/EnhancedAnalysis';
import { LLMRecommendations } from '../../components/LLMRecommendations';
import { DeepDiveAnalysis } from '../../components/DeepDiveAnalysis';
import { ComparativeAnalysis } from '../../components/ComparativeAnalysis';
import { WhatIfAnalysis } from '../../components/WhatIfAnalysis';
import { MarketInsights } from '../../components/MarketInsights';
import { CompetitorAnalysis } from '../../components/CompetitorAnalysis';
import styles from './Results.module.scss';

const Results: React.FC = () => {
  const navigate = useNavigate();
  const { results, resetAssessment, data } = useAssessmentStore();
  const [revealedSections, setRevealedSections] = useState<string[]>([]);
  const controls = useAnimation();

  useEffect(() => {
    // Animate score reveal
    const revealSequence = async () => {
      await controls.start({ opacity: 1, scale: 1 });
      
      // Reveal sections one by one
      const sections = ['overall', 'capital', 'advantage', 'market', 'people', 'insights', 'deepdive', 'comparative', 'enhanced', 'llm-recommendations', 'whatif', 'market-insights', 'competitor-analysis', 'recommendations'];
      for (const section of sections) {
        await new Promise(resolve => setTimeout(resolve, 300));
        setRevealedSections(prev => [...prev, section]);
      }
    };
    
    revealSequence();
  }, [controls]);

  if (!results) {
    navigate('/');
    return null;
  }

  const successProbability = Math.round((results.successProbability || 0) * 100);
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return styles.excellent;
    if (score >= 0.6) return styles.good;
    if (score >= 0.4) return styles.fair;
    return styles.poor;
  };
  
  const getVerdict = () => {
    if (successProbability >= 70) return 'PASS';
    if (successProbability >= 50) return 'CONDITIONAL PASS';
    return 'FAIL';
  };
  
  const getVerdictColor = () => {
    if (successProbability >= 70) return styles.pass;
    if (successProbability >= 50) return styles.conditional;
    return styles.fail;
  };

  const getConfidenceDescription = (confidence: string) => {
    switch (confidence) {
      case 'very high':
        return 'Our models have very high confidence in this assessment';
      case 'high':
        return 'Our models have high confidence in this assessment';
      case 'moderate':
        return 'Our models have moderate confidence in this assessment';
      case 'low':
        return 'Our models have lower confidence due to limited data';
      default:
        return 'Assessment confidence level';
    }
  };

  const handleNewAssessment = () => {
    resetAssessment();
    navigate('/');
  };

  const handleExport = () => {
    // Create a downloadable report
    const report = {
      assessmentDate: new Date().toISOString(),
      results,
      metadata: {
        platform: 'FLASH Assessment',
        version: '1.0.0',
      },
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `flash-assessment-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <Button 
          variant="text" 
          size="small" 
          icon={<Icon name="chevron.left" />} 
          iconPosition="left"
          onClick={() => navigate('/')}
        >
          Home
        </Button>
      </nav>

      <div className={styles.container}>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={controls}
          transition={{ duration: 0.5 }}
          className={styles.content}
        >
          <div className={styles.header}>
            <h1 className={styles.title}>Your Assessment Results</h1>
            <p className={styles.subtitle}>
              Based on our analysis of your startup's key metrics
            </p>
          </div>

          {/* Main Score Card */}
          {revealedSections.includes('overall') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.scoreCard}
            >
              <div className={styles.scoreGrid}>
                <div className={styles.overallScore}>
                  <GaugeChart 
                    value={results.successProbability || 0}
                    size={320}
                    label="Success Probability"
                  />
                  
                  <div className={styles.confidence}>
                    <span className={styles.confidenceLabel}>Confidence Level:</span>
                    <span className={styles.confidenceValue}>{results.confidence}</span>
                  </div>
                  <p className={styles.confidenceDescription}>
                    {getConfidenceDescription(results.confidence || '')}
                  </p>
                </div>
                
                <div className={styles.scoreDetails}>
                  <div className={styles.verdictSection}>
                    <h3>Assessment Verdict</h3>
                    <div className={`${styles.verdict} ${getVerdictColor()}`}>
                      {getVerdict()}
                    </div>
                  </div>
                  
                  <div className={styles.quickStats}>
                    <div className={styles.stat}>
                      <span className={styles.statLabel}>Risk Level</span>
                      <span className={styles.statValue}>{results.riskLevel || 'Moderate'}</span>
                    </div>
                    <div className={styles.stat}>
                      <span className={styles.statLabel}>Investment Stage</span>
                      <span className={styles.statValue}>{data.companyInfo?.stage || 'Pre-seed'}</span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* CAMP Scores with Charts */}
          <div className={styles.chartsContainer}>
            {/* Radar Chart */}
            {revealedSections.includes('capital') && results.scores && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className={styles.radarChartSection}
              >
                <h2 className={styles.sectionTitle}>CAMP Analysis</h2>
                <RadarChart
                  data={[
                    { axis: 'Capital', value: results.scores.capital || 0, fullName: 'Capital Efficiency' },
                    { axis: 'Advantage', value: results.scores.advantage || 0, fullName: 'Competitive Advantage' },
                    { axis: 'Market', value: results.scores.market || 0, fullName: 'Market Opportunity' },
                    { axis: 'People', value: results.scores.people || 0, fullName: 'Team & Leadership' }
                  ]}
                  size={400}
                />
              </motion.div>
            )}
            
            {/* Bar Chart */}
            {revealedSections.includes('market') && results.scores && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className={styles.barChartSection}
              >
                <h2 className={styles.sectionTitle}>Detailed Scores</h2>
                <ScoreBarChart
                  scores={[
                    {
                      name: 'Capital',
                      value: results.scores.capital || 0,
                      icon: 'building.2',
                      description: 'Financial health, runway, and burn efficiency'
                    },
                    {
                      name: 'Advantage',
                      value: results.scores.advantage || 0,
                      icon: 'sparkles',
                      description: 'Competitive moat and differentiation'
                    },
                    {
                      name: 'Market',
                      value: results.scores.market || 0,
                      icon: 'chart.line.uptrend',
                      description: 'TAM, growth rate, and market timing'
                    },
                    {
                      name: 'People',
                      value: results.scores.people || 0,
                      icon: 'brain',
                      description: 'Team experience and execution capability'
                    }
                  ]}
                />
              </motion.div>
            )}
          </div>

          {/* Enhanced Insights */}
          {revealedSections.includes('insights') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.insightsSection}
            >
              <EnhancedInsights 
                scores={results.scores}
                probability={results.successProbability || 0}
              />
            </motion.div>
          )}

          {/* Enhanced Analysis */}
          {revealedSections.includes('enhanced') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.enhancedSection}
            >
              <EnhancedAnalysis 
                assessmentData={data}
                basicResults={results}
              />
            </motion.div>
          )}

          {/* Deep Dive Analysis */}
          {revealedSections.includes('deepdive') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.deepDiveSection}
            >
              <DeepDiveAnalysis 
                scores={results.scores}
                assessmentData={data}
                insights={results.insights}
              />
            </motion.div>
          )}

          {/* Comparative Analysis */}
          {revealedSections.includes('comparative') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.comparativeSection}
            >
              <ComparativeAnalysis 
                scores={results.scores}
                assessmentData={data}
                successProbability={results.successProbability || 0}
              />
            </motion.div>
          )}

          {/* LLM Recommendations */}
          {revealedSections.includes('llm-recommendations') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.recommendationsSection}
            >
              <LLMRecommendations 
                assessmentData={data}
                basicResults={results}
              />
            </motion.div>
          )}

          {/* What-If Analysis */}
          {revealedSections.includes('whatif') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.whatIfSection}
            >
              <WhatIfAnalysis />
            </motion.div>
          )}

          {/* Market Insights */}
          {revealedSections.includes('market-insights') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.marketInsightsSection}
            >
              <MarketInsights />
            </motion.div>
          )}

          {/* Competitor Analysis */}
          {revealedSections.includes('competitor-analysis') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.competitorSection}
            >
              <CompetitorAnalysis />
            </motion.div>
          )}

          {/* Actions */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 2 }}
            className={styles.actions}
          >
            <Button
              variant="secondary"
              size="large"
              icon={<Icon name="arrow.down" />}
              onClick={handleExport}
            >
              Export Report
            </Button>
            <Button
              variant="primary"
              size="large"
              onClick={handleNewAssessment}
            >
              New Assessment
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Results;