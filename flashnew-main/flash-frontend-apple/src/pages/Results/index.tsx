import React, { useState, useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { Button, Icon } from '../../design-system/components';
import { GaugeChart, RadarChart, ScoreBarChart } from '../../components/charts';
import { EnhancedInsightsMinimalV2 } from '../../components/EnhancedInsightsMinimalV2';
import { LLMRecommendationsMinimalV2 } from '../../components/LLMRecommendationsMinimalV2';
import { DeepDiveAnalysisMinimalV2 } from '../../components/DeepDiveAnalysisMinimalV2';
import { CAMPAnalysisMinimalV2 } from '../../components/CAMPAnalysisMinimalV2';
import { SuccessScoreMinimal } from '../../components/SuccessScoreMinimal';
import { RadarChartMinimal } from '../../components/charts/RadarChartMinimal';
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
      const sections = ['overall', 'capital', 'advantage', 'market', 'people', 'insights', 'deepdive', 'llm-recommendations', 'recommendations'];
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
          {/* Main Score Card */}
          {revealedSections.includes('overall') && (
            <SuccessScoreMinimal 
              score={results.successProbability || 0}
              confidence={results.confidence}
              companyName={data.companyInfo?.companyName || 'Your Startup'}
            />
          )}

          {/* CAMP Framework Analysis */}
          {revealedSections.includes('capital') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.campSection}
            >
              <h2 className={styles.sectionTitle}>CAMP Framework Analysis</h2>
              <CAMPAnalysisMinimalV2 scores={results.scores} />
            </motion.div>
          )}

          {/* Enhanced Insights */}
          {revealedSections.includes('insights') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.insightsSection}
            >
              <EnhancedInsightsMinimalV2 
                scores={results.scores}
                probability={results.successProbability || 0}
              />
            </motion.div>
          )}

          {/* Enhanced Analysis - Removed duplicate as components are integrated above */}

          {/* Deep Dive Analysis */}
          {revealedSections.includes('deepdive') && results.scores && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.deepDiveSection}
            >
              <DeepDiveAnalysisMinimalV2 
                scores={results.scores}
                assessmentData={data}
                insights={results.insights}
              />
            </motion.div>
          )}

          {/* FLASH Intelligence (formerly LLM Recommendations) */}
          {revealedSections.includes('llm-recommendations') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={styles.recommendationsSection}
            >
              <LLMRecommendationsMinimalV2 
                assessmentData={data}
                basicResults={results}
              />
            </motion.div>
          )}

          {/* Actions */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 2 }}
            className={styles.actions}
          >
            <button
              className={styles.actionButton}
              onClick={handleExport}
            >
              Export Report
            </button>
            <button
              className={`${styles.actionButton} ${styles.primary}`}
              onClick={handleNewAssessment}
            >
              New Assessment
            </button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Results;