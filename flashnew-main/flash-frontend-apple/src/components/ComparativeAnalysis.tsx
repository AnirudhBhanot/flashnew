import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../design-system/components/AnimatePresenceWrapper';
import { Icon, Button, Select } from '../design-system/components';
import { MultiSeriesRadarChart } from './charts/MultiSeriesRadarChart';
import { ScoreBarChart } from './charts';
import styles from './ComparativeAnalysis.module.scss';

interface ComparativeAnalysisProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  assessmentData: any;
  successProbability: number;
}

interface ComparisonData {
  name: string;
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  successProbability: number;
  stage: string;
  industry: string;
}

export const ComparativeAnalysis: React.FC<ComparativeAnalysisProps> = ({
  scores,
  assessmentData,
  successProbability
}) => {
  const [selectedComparison, setSelectedComparison] = useState<string>('industry');
  const [selectedMetric, setSelectedMetric] = useState<string>('overall');
  const [showDetails, setShowDetails] = useState(false);

  // Generate comparison data based on selection
  const getComparisonData = (): ComparisonData[] => {
    const industry = assessmentData.companyInfo?.industry || 'saas';
    const stage = assessmentData.companyInfo?.stage || 'seed';

    // Industry averages (simulated data - in production, this would come from API)
    const industryAverages: Record<string, ComparisonData> = {
      saas: {
        name: 'SaaS Industry Average',
        scores: { capital: 0.65, advantage: 0.60, market: 0.70, people: 0.68 },
        successProbability: 0.62,
        stage: 'all',
        industry: 'saas'
      },
      fintech: {
        name: 'FinTech Industry Average',
        scores: { capital: 0.70, advantage: 0.65, market: 0.75, people: 0.72 },
        successProbability: 0.68,
        stage: 'all',
        industry: 'fintech'
      },
      healthtech: {
        name: 'HealthTech Industry Average',
        scores: { capital: 0.68, advantage: 0.72, market: 0.65, people: 0.70 },
        successProbability: 0.64,
        stage: 'all',
        industry: 'healthtech'
      },
      marketplace: {
        name: 'Marketplace Average',
        scores: { capital: 0.62, advantage: 0.58, market: 0.72, people: 0.65 },
        successProbability: 0.60,
        stage: 'all',
        industry: 'marketplace'
      }
    };

    // Stage benchmarks
    const stageBenchmarks: Record<string, ComparisonData> = {
      pre_seed: {
        name: 'Pre-seed Average',
        scores: { capital: 0.45, advantage: 0.50, market: 0.60, people: 0.55 },
        successProbability: 0.48,
        stage: 'pre_seed',
        industry: 'all'
      },
      seed: {
        name: 'Seed Stage Average',
        scores: { capital: 0.55, advantage: 0.58, market: 0.65, people: 0.62 },
        successProbability: 0.56,
        stage: 'seed',
        industry: 'all'
      },
      series_a: {
        name: 'Series A Average',
        scores: { capital: 0.70, advantage: 0.68, market: 0.72, people: 0.75 },
        successProbability: 0.68,
        stage: 'series_a',
        industry: 'all'
      },
      series_b: {
        name: 'Series B Average',
        scores: { capital: 0.78, advantage: 0.75, market: 0.78, people: 0.80 },
        successProbability: 0.76,
        stage: 'series_b',
        industry: 'all'
      }
    };

    // Top performers
    const topPerformers: ComparisonData = {
      name: 'Top 10% Startups',
      scores: { capital: 0.85, advantage: 0.82, market: 0.88, people: 0.86 },
      successProbability: 0.84,
      stage: 'all',
      industry: 'all'
    };

    // Your startup
    const yourStartup: ComparisonData = {
      name: assessmentData.companyInfo?.companyName || 'Your Startup',
      scores,
      successProbability,
      stage,
      industry
    };

    switch (selectedComparison) {
      case 'industry':
        return [
          yourStartup,
          industryAverages[industry] || industryAverages.saas,
          topPerformers
        ];
      case 'stage':
        return [
          yourStartup,
          stageBenchmarks[stage] || stageBenchmarks.seed,
          topPerformers
        ];
      case 'all':
        return [
          yourStartup,
          industryAverages[industry] || industryAverages.saas,
          stageBenchmarks[stage] || stageBenchmarks.seed,
          topPerformers
        ];
      default:
        return [yourStartup];
    }
  };

  const comparisonData = getComparisonData();

  // Calculate percentile rankings
  const getPercentileRank = (metric: string): number => {
    const yourScore = metric === 'overall' ? successProbability : scores[metric as keyof typeof scores];
    
    // Simulated percentile calculation
    if (yourScore >= 0.80) return 90;
    if (yourScore >= 0.70) return 75;
    if (yourScore >= 0.60) return 60;
    if (yourScore >= 0.50) return 45;
    if (yourScore >= 0.40) return 30;
    return 20;
  };

  const getInsight = (metric: string): string => {
    const percentile = getPercentileRank(metric);
    const metricName = metric === 'overall' ? 'overall success probability' : `${metric} score`;
    
    if (percentile >= 75) {
      return `Your ${metricName} is in the top 25% of startups`;
    } else if (percentile >= 50) {
      return `Your ${metricName} is above average`;
    } else if (percentile >= 25) {
      return `Your ${metricName} is below average`;
    } else {
      return `Your ${metricName} needs improvement`;
    }
  };

  const metrics = [
    { id: 'overall', name: 'Overall Success', icon: 'star' },
    { id: 'capital', name: 'Capital', icon: 'building.2' },
    { id: 'advantage', name: 'Advantage', icon: 'sparkles' },
    { id: 'market', name: 'Market', icon: 'chart.line.uptrend' },
    { id: 'people', name: 'People', icon: 'brain' }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>
          <Icon name="chart.bar" size={24} />
          Comparative Analysis
        </h3>
        <p className={styles.subtitle}>
          See how you compare to other startups in your industry and stage
        </p>
      </div>

      {/* Comparison Controls */}
      <div className={styles.controls}>
        <Select
          label="Compare Against"
          value={selectedComparison}
          onChange={setSelectedComparison}
          options={[
            { value: 'industry', label: 'Industry Peers' },
            { value: 'stage', label: 'Stage Peers' },
            { value: 'all', label: 'All Benchmarks' }
          ]}
        />
        
        <Button
          variant={showDetails ? 'primary' : 'secondary'}
          size="small"
          onClick={() => setShowDetails(!showDetails)}
          icon={<Icon name={showDetails ? 'chevron.up' : 'chevron.down'} />}
        >
          {showDetails ? 'Hide' : 'Show'} Details
        </Button>
      </div>

      {/* Radar Chart Comparison */}
      <div className={styles.chartSection}>
        <div className={styles.radarChart}>
          <MultiSeriesRadarChart
            data={comparisonData.map(company => ({
              name: company.name,
              values: {
                Capital: company.scores.capital,
                Advantage: company.scores.advantage,
                Market: company.scores.market,
                People: company.scores.people
              }
            }))}
            size={400}
          />
        </div>
        
        <div className={styles.legend}>
          {comparisonData.map((company, index) => (
            <div key={company.name} className={styles.legendItem}>
              <div 
                className={styles.legendColor}
                style={{ backgroundColor: ['#007AFF', '#FF9500', '#34C759'][index] }}
              />
              <span className={styles.legendLabel}>{company.name}</span>
              <span className={styles.legendValue}>
                {Math.round(company.successProbability * 100)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Metric Tabs */}
      <div className={styles.metricTabs}>
        {metrics.map(metric => (
          <button
            key={metric.id}
            className={`${styles.metricTab} ${selectedMetric === metric.id ? styles.active : ''}`}
            onClick={() => setSelectedMetric(metric.id)}
          >
            <Icon name={metric.icon} size={20} />
            <span>{metric.name}</span>
          </button>
        ))}
      </div>

      {/* Detailed Comparison */}
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedMetric}
          className={styles.comparisonDetail}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {/* Percentile Rank */}
          <div className={styles.percentileSection}>
            <h4 className={styles.percentileTitle}>Your Percentile Rank</h4>
            <div className={styles.percentileValue}>
              {getPercentileRank(selectedMetric)}th
              <span className={styles.percentileLabel}>percentile</span>
            </div>
            <p className={styles.percentileInsight}>{getInsight(selectedMetric)}</p>
          </div>

          {/* Bar Comparison */}
          <div className={styles.barComparison}>
            {comparisonData.map((company, index) => {
              const value = selectedMetric === 'overall' 
                ? company.successProbability 
                : company.scores[selectedMetric as keyof typeof company.scores];
              
              return (
                <motion.div
                  key={company.name}
                  className={styles.barItem}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className={styles.barLabel}>
                    <span className={styles.barName}>{company.name}</span>
                    <span className={styles.barValue}>{Math.round(value * 100)}%</span>
                  </div>
                  <div className={styles.barContainer}>
                    <motion.div
                      className={styles.barFill}
                      initial={{ width: 0 }}
                      animate={{ width: `${value * 100}%` }}
                      transition={{ duration: 0.5, delay: 0.2 + index * 0.1 }}
                      style={{ 
                        backgroundColor: company.name.includes('Your') 
                          ? '#007AFF' 
                          : '#E5E5EA' 
                      }}
                    />
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Detailed Insights */}
          {showDetails && (
            <motion.div
              className={styles.insights}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
            >
              <h4 className={styles.insightsTitle}>Detailed Insights</h4>
              
              {selectedMetric === 'overall' && (
                <div className={styles.insightGrid}>
                  <div className={styles.insightCard}>
                    <Icon name="arrow.up.circle" size={24} />
                    <h5>Strengths</h5>
                    <p>Your strongest areas compared to peers</p>
                    <ul>
                      {Object.entries(scores)
                        .filter(([_, score]) => score > 0.7)
                        .map(([metric, score]) => (
                          <li key={metric}>
                            <strong>{metric}:</strong> {Math.round(score * 100)}%
                          </li>
                        ))
                      }
                    </ul>
                  </div>
                  
                  <div className={styles.insightCard}>
                    <Icon name="arrow.down.circle" size={24} />
                    <h5>Improvement Areas</h5>
                    <p>Areas where you lag behind peers</p>
                    <ul>
                      {Object.entries(scores)
                        .filter(([_, score]) => score < 0.6)
                        .map(([metric, score]) => (
                          <li key={metric}>
                            <strong>{metric}:</strong> {Math.round(score * 100)}%
                          </li>
                        ))
                      }
                    </ul>
                  </div>
                </div>
              )}

              {selectedMetric !== 'overall' && (
                <div className={styles.metricInsights}>
                  <p className={styles.metricDescription}>
                    {getMetricDescription(selectedMetric)}
                  </p>
                  
                  <div className={styles.benchmarkList}>
                    <h5>Key Benchmarks</h5>
                    {getMetricBenchmarks(selectedMetric).map((benchmark, index) => (
                      <div key={index} className={styles.benchmarkItem}>
                        <span className={styles.benchmarkLabel}>{benchmark.label}</span>
                        <span className={styles.benchmarkValue}>{benchmark.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );

  function getMetricDescription(metric: string): string {
    const descriptions: Record<string, string> = {
      capital: 'Capital efficiency measures how well you utilize funding, manage burn rate, and generate revenue. Top performers maintain 18+ months runway with strong unit economics.',
      advantage: 'Competitive advantage reflects your moat strength, differentiation, and defensibility. Leaders have multiple barriers to entry and proprietary advantages.',
      market: 'Market opportunity combines TAM size, growth rate, and your positioning. Winners target large, growing markets with clear go-to-market strategies.',
      people: 'Team strength evaluates founder experience, key hires, and execution capability. Successful startups have experienced, complementary teams.'
    };
    return descriptions[metric] || '';
  }

  function getMetricBenchmarks(metric: string): { label: string; value: string }[] {
    const benchmarks: Record<string, { label: string; value: string }[]> = {
      capital: [
        { label: 'Typical Runway', value: '12-18 months' },
        { label: 'Burn Multiple', value: '<2x' },
        { label: 'Gross Margin Target', value: '>60%' }
      ],
      advantage: [
        { label: 'Patents Filed', value: '2-5' },
        { label: 'Key Differentiators', value: '3+' },
        { label: 'Switching Cost', value: 'High' }
      ],
      market: [
        { label: 'TAM Minimum', value: '$1B+' },
        { label: 'Growth Rate', value: '>20% YoY' },
        { label: 'CAC Payback', value: '<12 months' }
      ],
      people: [
        { label: 'Technical Founders', value: '1-2' },
        { label: 'Prior Exits', value: '1+' },
        { label: 'Key Hires', value: '5+' }
      ]
    };
    return benchmarks[metric] || [];
  }
};