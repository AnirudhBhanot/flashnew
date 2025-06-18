import React from 'react';
import { FrameworkIntelligenceEnhanced } from '../components/FrameworkIntelligenceEnhanced';
import useAssessmentStore from '../store/assessmentStore';
import styles from './Landing/Landing.module.scss';

const TestFrameworkIntelligence: React.FC = () => {
  const { setData } = useAssessmentStore();

  // Set some test data
  React.useEffect(() => {
    setData({
      companyInfo: {
        companyName: 'Test Startup',
        stage: 'seed',
        industry: 'SaaS',
        sector: 'B2B',
        businessModel: 'B2B SaaS',
        foundedDate: new Date('2022-01-01'),
        location: 'San Francisco, CA'
      },
      capital: {
        totalCapitalRaised: 2000000,
        cashOnHand: 1500000,
        monthlyBurnRate: 150000,
        runwayMonths: 10,
        annualRevenueRunRate: 500000,
        revenueGrowthRate: 50,
        burnMultiple: 3.6
      },
      people: {
        teamSize: 12,
        technicalTeamPercent: 60,
        foundersExperience: 8,
        foundersCount: 2,
        advisorsCount: 3,
        boardMembersCount: 2
      },
      market: {
        tamSize: 5000000000,
        samSize: 500000000,
        somSize: 50000000,
        customerCount: 25,
        customerAcquisitionCost: 2000,
        customerLifetimeValue: 8000,
        netDollarRetention: 95,
        targetMarket: 'SMB Software Companies',
        marketGrowthRate: 25
      },
      advantage: {
        competitiveLandscape: 'Moderately competitive with 3-5 major players',
        uniqueValueProposition: 'AI-powered business intelligence for SMBs',
        intellectualProperty: 2,
        networkEffects: true,
        technicalMoat: true
      }
    });
  }, [setData]);

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className={styles.header}>
          <h1>Framework Intelligence Test</h1>
          <p>Testing intelligent framework selection based on startup context</p>
        </div>
        
        <div style={{ marginTop: '2rem' }}>
          <FrameworkIntelligenceEnhanced />
        </div>
      </div>
    </div>
  );
};

export default TestFrameworkIntelligence;