import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styles from './WhatIfAnalysisMinimal.module.scss';

interface Scenario {
  id: string;
  name: string;
  description: string;
  metrics: {
    revenue: string;
    runway: string;
    team: string;
    market: string;
  };
  impact: number;
  probability: number;
}

export const WhatIfAnalysisMinimalV2: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState<string>('current');

  const scenarios: Scenario[] = [
    {
      id: 'current',
      name: 'Current State',
      description: 'Your startup as it is today',
      metrics: {
        revenue: '$50K MRR',
        runway: '12 months',
        team: '5 people',
        market: '2.5% share'
      },
      impact: 0,
      probability: 65
    },
    {
      id: 'funding',
      name: 'Series A Funding',
      description: 'Successfully raise $5M Series A',
      metrics: {
        revenue: '$50K MRR',
        runway: '24 months',
        team: '15 people',
        market: '2.5% share'
      },
      impact: 15,
      probability: 80
    },
    {
      id: 'growth',
      name: '3x Revenue Growth',
      description: 'Triple your current revenue',
      metrics: {
        revenue: '$150K MRR',
        runway: '18 months',
        team: '8 people',
        market: '5% share'
      },
      impact: 12,
      probability: 77
    },
    {
      id: 'team',
      name: 'Key Hire',
      description: 'Hire experienced CTO/CPO',
      metrics: {
        revenue: '$50K MRR',
        runway: '10 months',
        team: '6 people',
        market: '2.5% share'
      },
      impact: 8,
      probability: 73
    },
    {
      id: 'pivot',
      name: 'Market Pivot',
      description: 'Pivot to adjacent market',
      metrics: {
        revenue: '$20K MRR',
        runway: '8 months',
        team: '5 people',
        market: '0.5% share'
      },
      impact: -10,
      probability: 55
    }
  ];

  const currentScenario = scenarios.find(s => s.id === selectedScenario) || scenarios[0];
  const baseScenario = scenarios[0];

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>What-If Analysis</h3>
      <p className={styles.subtitle}>
        Explore how different scenarios affect your success probability
      </p>

      {/* Scenario Selection */}
      <div className={styles.scenarios}>
        {scenarios.map(scenario => (
          <button
            key={scenario.id}
            className={`${styles.scenarioButton} ${selectedScenario === scenario.id ? styles.active : ''}`}
            onClick={() => setSelectedScenario(scenario.id)}
          >
            <span className={styles.scenarioName}>{scenario.name}</span>
            <span className={styles.scenarioImpact}>
              {scenario.impact > 0 && '+'}
              {scenario.impact !== 0 && `${scenario.impact}%`}
            </span>
          </button>
        ))}
      </div>

      {/* Selected Scenario Details */}
      <motion.div
        key={selectedScenario}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={styles.scenarioDetail}
      >
        <p className={styles.scenarioDescription}>
          {currentScenario.description}
        </p>

        {/* Metrics Comparison */}
        <div className={styles.metrics}>
          {Object.entries(currentScenario.metrics).map(([key, value]) => (
            <div key={key} className={styles.metric}>
              <span className={styles.metricLabel}>
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </span>
              <span className={styles.metricValue}>{value}</span>
            </div>
          ))}
        </div>

        {/* Probability Visualization */}
        <div className={styles.probabilitySection}>
          <div className={styles.probabilityHeader}>
            <span className={styles.probabilityLabel}>Success Probability</span>
            <span className={styles.probabilityValue}>{currentScenario.probability}%</span>
          </div>
          
          <div className={styles.probabilityBar}>
            <motion.div
              className={styles.probabilityFill}
              initial={{ width: 0 }}
              animate={{ width: `${currentScenario.probability}%` }}
              transition={{ duration: 0.5 }}
            />
            {selectedScenario !== 'current' && (
              <div 
                className={styles.baselineMark} 
                style={{ left: `${baseScenario.probability}%` }}
              >
                <span className={styles.baselineLabel}>Current: {baseScenario.probability}%</span>
              </div>
            )}
          </div>
        </div>

        {/* Impact Analysis */}
        {selectedScenario !== 'current' && (
          <div className={styles.impact}>
            <h4 className={styles.impactTitle}>Impact Analysis</h4>
            <div className={styles.impactItems}>
              <div className={styles.impactItem}>
                <span className={styles.impactLabel}>Probability Change</span>
                <span className={`${styles.impactValue} ${currentScenario.impact > 0 ? styles.positive : styles.negative}`}>
                  {currentScenario.impact > 0 && '+'}
                  {currentScenario.impact}%
                </span>
              </div>
              <div className={styles.impactItem}>
                <span className={styles.impactLabel}>Risk Level</span>
                <span className={styles.impactValue}>
                  {Math.abs(currentScenario.impact) > 10 ? 'High' : 'Medium'}
                </span>
              </div>
              <div className={styles.impactItem}>
                <span className={styles.impactLabel}>Timeframe</span>
                <span className={styles.impactValue}>
                  {currentScenario.id === 'funding' ? '3-6 months' : 
                   currentScenario.id === 'growth' ? '6-12 months' :
                   currentScenario.id === 'team' ? '1-3 months' :
                   '3-6 months'}
                </span>
              </div>
            </div>
          </div>
        )}
      </motion.div>

      {/* Recommendations */}
      <div className={styles.recommendations}>
        <h4 className={styles.recommendationsTitle}>Key Insights</h4>
        <ul className={styles.recommendationsList}>
          <li>Series A funding provides the highest probability boost (+15%)</li>
          <li>Revenue growth has strong positive impact with lower risk</li>
          <li>Market pivots carry significant risk and should be carefully considered</li>
        </ul>
      </div>
    </div>
  );
};