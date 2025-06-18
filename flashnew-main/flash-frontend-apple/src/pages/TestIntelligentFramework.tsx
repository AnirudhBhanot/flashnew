import React, { useEffect } from 'react';
import StrategicFrameworkAnalysis from '../components/StrategicFrameworkAnalysis';
import useAssessmentStore from '../store/assessmentStore';
import styles from './TestIntelligentFramework.module.scss';

const TestIntelligentFramework: React.FC = () => {
  const { updateData } = useAssessmentStore();

  // Set test data
  const testData = {
    companyInfo: {
      companyName: 'TechVenture AI',
      website: 'https://techventure.ai',
      description: 'AI-powered B2B SaaS platform for sales automation'
    },
    capital: {
      totalRaised: 5000000,
      cashOnHand: 3000000,
      monthlyBurn: 250000,
      runwayMonths: 12,
      fundingStage: 'seed',
      primaryInvestor: 'tier_2',
      annualRevenue: 1200000,
      marketingSpend: 180000
    },
    advantage: {
      productStage: 'growth',
      proprietaryTech: true,
      patentsFiled: 3,
      monthlyActiveUsers: 500,
      churnRate: 4,
      npsScore: 52,
      networkEffects: true,
      switchingCosts: 'high',
      customHardware: false,
      exclusivePartnerships: true
    },
    market: {
      tam: 15000000000,
      sam: 2000000000,
      som: 20000000,
      marketGrowthRate: 28,
      competitorCount: 25,
      customerAcquisitionCost: 1200,
      lifetimeValue: 36000,
      businessModel: 'b2b',
      sector: 'saas',
      customerConcentration: 15,
      contractLength: 'annual',
      substituteThreat: 'medium',
      primarySubstitute: 'In-house development',
      secondaryMarket: 'Financial Services',
      regulatoryChanges: true
    },
    people: {
      fullTimeEmployees: 22,
      industryExperience: 12,
      keyHires: ['VP Sales', 'VP Engineering', 'Head of Customer Success']
    }
  };

  const testResults = {
    successProbability: 0.76,
    scores: {
      capital: 0.72,
      advantage: 0.81,
      market: 0.68,
      people: 0.74
    }
  };

  useEffect(() => {
    // Update store with test data
    updateData('companyInfo', testData.companyInfo);
    updateData('capital', testData.capital);
    updateData('advantage', testData.advantage);
    updateData('market', testData.market);
    updateData('people', testData.people);
    updateData('results', testResults);
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Intelligent Framework Analysis Test</h1>
        <p>Testing next-generation AI-powered strategic framework selection</p>
        
        <div className={styles.testInfo}>
          <div className={styles.infoCard}>
            <h3>Test Company Profile</h3>
            <ul>
              <li>Company: {testData.companyInfo.companyName}</li>
              <li>Stage: {testData.capital.fundingStage}</li>
              <li>Industry: B2B SaaS - Sales Automation</li>
              <li>Team Size: {testData.people.fullTimeEmployees}</li>
              <li>Runway: {testData.capital.runwayMonths} months</li>
              <li>Market Growth: {testData.market.marketGrowthRate}% CAGR</li>
            </ul>
          </div>
          
          <div className={styles.infoCard}>
            <h3>Key Features Being Tested</h3>
            <ul>
              <li>✅ ML-based framework scoring</li>
              <li>✅ Real-time market intelligence</li>
              <li>✅ Framework synergy optimization</li>
              <li>✅ Custom adaptations per company</li>
              <li>✅ Quick wins identification</li>
              <li>✅ Integrated implementation roadmap</li>
            </ul>
          </div>
        </div>
      </div>

      <div className={styles.content}>
        <StrategicFrameworkAnalysis />
      </div>
    </div>
  );
};

export default TestIntelligentFramework;