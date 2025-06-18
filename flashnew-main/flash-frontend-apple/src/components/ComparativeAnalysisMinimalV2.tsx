import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './ComparativeAnalysisMinimal.module.scss';

interface ComparativeAnalysisMinimalProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  assessmentData: any;
  successProbability: number;
}

export const ComparativeAnalysisMinimalV2: React.FC<ComparativeAnalysisMinimalProps> = ({
  scores,
  assessmentData,
  successProbability
}) => {
  const [selectedMetric, setSelectedMetric] = useState<string>('overall');
  const [selectedComparison, setSelectedComparison] = useState<string>('industry');

  const getComparisonData = () => {
    const industry = assessmentData.companyInfo?.industry || 'saas';
    const stage = assessmentData.companyInfo?.stage || 'seed';

    const industryAverages: Record<string, any> = {
      saas: { name: 'SaaS Average', scores: { capital: 0.65, advantage: 0.60, market: 0.70, people: 0.68 }, probability: 0.62 },
      fintech: { name: 'FinTech Average', scores: { capital: 0.70, advantage: 0.65, market: 0.75, people: 0.72 }, probability: 0.68 },
      healthtech: { name: 'HealthTech Average', scores: { capital: 0.68, advantage: 0.72, market: 0.65, people: 0.70 }, probability: 0.64 },
      marketplace: { name: 'Marketplace Average', scores: { capital: 0.62, advantage: 0.58, market: 0.72, people: 0.65 }, probability: 0.60 }
    };

    const stageAverages: Record<string, any> = {
      pre_seed: { name: 'Pre-seed Average', scores: { capital: 0.45, advantage: 0.50, market: 0.60, people: 0.55 }, probability: 0.48 },
      seed: { name: 'Seed Average', scores: { capital: 0.55, advantage: 0.58, market: 0.65, people: 0.62 }, probability: 0.56 },
      series_a: { name: 'Series A Average', scores: { capital: 0.70, advantage: 0.68, market: 0.72, people: 0.75 }, probability: 0.68 },
      series_b: { name: 'Series B Average', scores: { capital: 0.78, advantage: 0.75, market: 0.78, people: 0.80 }, probability: 0.76 }
    };

    const yourStartup = {
      name: assessmentData.companyInfo?.companyName || 'Your Startup',
      scores,
      probability: successProbability
    };

    if (selectedComparison === 'industry') {
      return [yourStartup, industryAverages[industry] || industryAverages.saas];
    } else {
      return [yourStartup, stageAverages[stage] || stageAverages.seed];
    }
  };

  const comparisonData = getComparisonData();
  const metrics = ['overall', 'capital', 'advantage', 'market', 'people'];

  const getValue = (company: any, metric: string) => {
    return metric === 'overall' ? company.probability : company.scores[metric];
  };

  const getPercentileRank = (metric: string): number => {
    const yourScore = metric === 'overall' ? successProbability : scores[metric as keyof typeof scores];
    if (yourScore >= 0.80) return 90;
    if (yourScore >= 0.70) return 75;
    if (yourScore >= 0.60) return 60;
    if (yourScore >= 0.50) return 45;
    if (yourScore >= 0.40) return 30;
    return 20;
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Comparative Analysis</h3>
      <p className={styles.subtitle}>
        How you compare to other startups
      </p>

      {/* Comparison Toggle */}
      <div className={styles.toggleGroup}>
        <button
          className={`${styles.toggle} ${selectedComparison === 'industry' ? styles.active : ''}`}
          onClick={() => setSelectedComparison('industry')}
        >
          Industry
        </button>
        <button
          className={`${styles.toggle} ${selectedComparison === 'stage' ? styles.active : ''}`}
          onClick={() => setSelectedComparison('stage')}
        >
          Stage
        </button>
      </div>

      {/* Metric Selection */}
      <div className={styles.metricTabs}>
        {metrics.map(metric => (
          <button
            key={metric}
            className={`${styles.metricTab} ${selectedMetric === metric ? styles.active : ''}`}
            onClick={() => setSelectedMetric(metric)}
          >
            {metric.charAt(0).toUpperCase() + metric.slice(1)}
          </button>
        ))}
      </div>

      {/* Comparison Display */}
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedMetric + selectedComparison}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
          className={styles.comparison}
        >
          {/* Percentile */}
          <div className={styles.percentile}>
            <span className={styles.percentileValue}>
              {getPercentileRank(selectedMetric)}th
            </span>
            <span className={styles.percentileLabel}>percentile</span>
          </div>

          {/* Bar Comparison */}
          <div className={styles.bars}>
            {comparisonData.map((company, index) => {
              const value = getValue(company, selectedMetric);
              const percentage = Math.round(value * 100);
              
              return (
                <div key={index} className={styles.barItem}>
                  <div className={styles.barHeader}>
                    <span className={styles.barName}>{company.name}</span>
                    <span className={styles.barValue}>{percentage}%</span>
                  </div>
                  <div className={styles.barContainer}>
                    <motion.div
                      className={`${styles.barFill} ${index === 0 ? styles.primary : ''}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${percentage}%` }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Insight */}
          <p className={styles.insight}>
            {getPercentileRank(selectedMetric) >= 50 
              ? `Above average ${selectedMetric === 'overall' ? 'performance' : selectedMetric} compared to ${selectedComparison} peers`
              : `Below average ${selectedMetric === 'overall' ? 'performance' : selectedMetric} compared to ${selectedComparison} peers`
            }
          </p>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};