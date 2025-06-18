import React, { useEffect } from 'react';
import useAssessmentStore from '../store/assessmentStore';
import { StrategicFrameworkReport } from '../components/StrategicFrameworkReport';
import styles from './TestFramework.module.scss';

const TestStrategicFramework: React.FC = () => {
  const updateData = useAssessmentStore(state => state.updateData);
  const setResults = useAssessmentStore(state => state.setResults);

  useEffect(() => {
    // Set test data for demonstration
    const testData = {
      companyInfo: {
        companyName: 'TechVision AI',
        website: 'https://techvision.ai',
        foundedDate: '2022-01-15',
        headquarters: 'San Francisco, CA'
      },
      capital: {
        fundingStage: 'series-a',
        totalRaised: '8500000',
        cashOnHand: '2800000',
        monthlyBurn: '200000',
        runwayMonths: '14',
        annualRevenue: '1800000',
        primaryInvestor: 'tier_1',
        marketingSpend: '18'
      },
      advantage: {
        productStage: 'growth',
        proprietaryTech: true,
        patentsFiled: '3',
        networkEffects: false,
        monthlyActiveUsers: '15000',
        churnRate: '2.1',
        npsScore: '68',
        switchingCosts: 'medium'
      },
      market: {
        sector: 'saas',
        tam: '45000000000',
        sam: '5000000000',
        som: '40000000',
        marketGrowthRate: '28',
        competitorCount: '15',
        customerConcentration: '35',
        contractLength: 'annual',
        customerAcquisitionCost: '2500',
        businessModel: 'b2b',
        substituteThreat: 'high',
        primarySubstitute: 'in-house development'
      },
      people: {
        fullTimeEmployees: '25',
        industryExperience: '12',
        keyHires: ['CTO', 'VP Sales', 'VP Marketing']
      }
    };

    const testResults = {
      successProbability: 0.68,
      confidence: 'high',
      scores: {
        capital: 0.65,
        advantage: 0.72,
        market: 0.58,
        people: 0.74
      }
    };

    // Update each section separately
    updateData('companyInfo', testData.companyInfo);
    updateData('capital', testData.capital);
    updateData('advantage', testData.advantage);
    updateData('market', testData.market);
    updateData('people', testData.people);
    
    setResults(testResults);
  }, [updateData, setResults]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Strategic Framework Analysis Test</h1>
        <p>Testing the enhanced professional framework analysis</p>
      </div>
      
      <div className={styles.content}>
        <StrategicFrameworkReport />
      </div>
    </div>
  );
};

export default TestStrategicFramework;