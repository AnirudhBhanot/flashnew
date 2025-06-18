import React from 'react';
import { StrategicFrameworkReport } from '../components/StrategicFrameworkReport';
import useAssessmentStore from '../store/assessmentStore';
import styles from './TestFramework.module.scss';

const TestStrategicFrameworkSimple: React.FC = () => {
  // Direct store access
  const store = useAssessmentStore();
  
  // Set data directly (only if not already set)
  if (!store.data.companyInfo?.companyName) {
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

    // Update store
    store.updateData('companyInfo', testData.companyInfo);
    store.updateData('capital', testData.capital);
    store.updateData('advantage', testData.advantage);
    store.updateData('market', testData.market);
    store.updateData('people', testData.people);
    store.setResults(testResults);
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Strategic Framework Analysis Test</h1>
        <p>Professional business intelligence framework analysis</p>
      </div>
      
      <div className={styles.content}>
        <StrategicFrameworkReport />
      </div>
    </div>
  );
};

export default TestStrategicFrameworkSimple;