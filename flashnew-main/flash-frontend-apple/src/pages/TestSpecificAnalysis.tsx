import React, { useState } from 'react';
import { getExecutiveFrameworkAnalysis } from '../services/api';
import styles from './TestSpecificAnalysis.module.scss';

const TestSpecificAnalysis: React.FC = () => {
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testData = {
    capital: {
      totalRaised: 3000000,
      cashOnHand: 3000000,
      monthlyBurn: 200000,
      runway: 15,
      annualRevenueRunRate: 1800000,
      revenue: 1800000,  // Add revenue field
      fundingStage: 'seed'
    },
    market: {
      sector: 'fintech',
      tam: 85000000000,
      sam: 8500000000,
      som: 85000000,
      marketGrowthRate: 45,
      customerCount: 150,
      competitionIntensity: 4,
      userGrowthRate: 25,
      grossMargin: 75,
      ltvCacRatio: 3.2,
      customerConcentration: 35
    },
    people: {
      teamSize: 18,
      founderCount: 2
    },
    advantage: {
      productStage: 'scaling',
      switchingCosts: 3
    }
  };

  const runAnalysis = async () => {
    setLoading(true);
    try {
      const result = await getExecutiveFrameworkAnalysis(testData);
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className={styles.container}>
      <h1>Test Specific Framework Analysis</h1>
      
      <button onClick={runAnalysis} disabled={loading}>
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </button>

      {analysis && (
        <div className={styles.results}>
          <h2>Executive Summary</h2>
          <div className={styles.section}>
            <h3>Situation</h3>
            <p>{analysis.executiveSummary?.situation}</p>
            
            <h3>Key Insights</h3>
            <ul>
              {analysis.executiveSummary?.keyInsights?.map((insight: string, i: number) => (
                <li key={i}>{insight}</li>
              ))}
            </ul>
            
            <h3>Recommendation</h3>
            <p>{analysis.executiveSummary?.recommendation}</p>
            
            <div className={styles.metrics}>
              <div>Value at Stake: ${(analysis.executiveSummary?.valueAtStake / 1e6)?.toFixed(0)}M</div>
              <div>Confidence: {analysis.executiveSummary?.confidenceLevel}%</div>
            </div>
          </div>

          <h2>Strategic Options</h2>
          {analysis.strategicOptions?.map((option: any, i: number) => (
            <div key={i} className={styles.option}>
              <h3>{option.title}</h3>
              <p>{option.description}</p>
              <div className={styles.metrics}>
                <span>NPV: ${(option.npv / 1e6).toFixed(1)}M</span>
                <span>IRR: {option.irr}%</span>
                <span>Payback: {option.paybackPeriod?.toFixed(1)} years</span>
              </div>
            </div>
          ))}

          <h2>Implementation Roadmap</h2>
          {analysis.implementationRoadmap?.map((phase: any, i: number) => (
            <div key={i} className={styles.phase}>
              <h3>{phase.phase}</h3>
              <h4>Initiatives:</h4>
              <ul>
                {phase.initiatives?.map((init: string, j: number) => (
                  <li key={j}>{init}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TestSpecificAnalysis;