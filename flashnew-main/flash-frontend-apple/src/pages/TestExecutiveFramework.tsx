import React, { useEffect } from 'react';
import { ExecutiveFrameworkAnalysis } from '../components/ExecutiveFrameworkAnalysis';
import useAssessmentStore from '../store/assessmentStore';
import styles from './TestFramework.module.scss';

const TestExecutiveFramework: React.FC = () => {
  const setMockData = useAssessmentStore(state => state.setData);
  const setMockResults = useAssessmentStore(state => state.setResults);

  useEffect(() => {
    // Set mock assessment data for testing
    const mockAssessmentData = {
      companyInfo: {
        companyName: 'TechVision AI',
        foundingDate: '2021-01-15',
        headquarters: 'San Francisco, CA',
        website: 'www.techvision.ai'
      },
      capital: {
        totalRaised: 8500000,
        cashOnHand: 3200000,
        monthlyBurn: 280000,
        monthlyRevenue: 125000,
        runwayMonths: 11,
        fundingStage: 'series-a',
        primaryInvestor: 'tier_2',
        hasDebt: false,
        burnMultiple: 2.24,
        annualRevenueRunRate: 1500000
      },
      market: {
        sector: 'saas',
        businessModel: 'b2b',
        tam: 4500000000,
        sam: 850000000,
        som: 42000000,
        marketGrowthRate: 28,
        competitionIntensity: 4,
        competitorCount: 12,
        customerCount: 48,
        customerAcquisitionCost: 2800,
        lifetimeValue: 18500,
        customerConcentration: 15,
        userGrowthRate: 22,
        netDollarRetention: 118,
        productRetention30d: 88,
        productRetention90d: 76,
        dauMauRatio: 42,
        revenueGrowthRate: 180,
        grossMargin: 68,
        ltvCacRatio: 6.6,
        marketShare: 0.005
      },
      advantage: {
        productStage: 'growth',
        proprietaryTech: true,
        patentsFiled: 3,
        patentCount: 3,
        monthlyActiveUsers: 2800,
        networkEffects: true,
        hasDataMoat: true,
        regulatoryAdvantage: false,
        techDifferentiation: 4,
        switchingCosts: 4,
        brandStrength: 3,
        scalability: 4
      },
      people: {
        fullTimeEmployees: 28,
        founderCount: 3,
        teamSize: 28,
        avgExperience: 8,
        industryExperience: 12,
        domainExpertiseYears: 10,
        priorStartupCount: 2,
        priorExits: 1,
        boardAdvisorScore: 4,
        advisorCount: 5,
        teamDiversity: 35,
        keyPersonDependency: true
      }
    };

    const mockResults = {
      successProbability: 0.74,
      confidence: 'high',
      verdict: 'INVEST',
      riskLevel: 'moderate',
      scores: {
        capital: 3.8,
        advantage: 4.2,
        market: 4.5,
        people: 3.9
      },
      insights: [
        'Strong product-market fit with 118% net dollar retention',
        'Impressive LTV:CAC ratio of 6.6x indicates efficient growth',
        'Burn multiple of 2.24 needs optimization for sustainable growth',
        'Market opportunity of $4.5B with 28% CAGR presents significant upside',
        'Team expertise and prior exits provide execution capability'
      ],
      confidenceInterval: {
        lower: 0.68,
        upper: 0.80
      }
    };

    setMockData(mockAssessmentData);
    setMockResults(mockResults);
  }, [setMockData, setMockResults]);

  return (
    <div className={styles.testContainer}>
      <div className={styles.testHeader}>
        <h1>Executive Framework Analysis - Test View</h1>
        <p>
          This page demonstrates the Executive Framework Analysis component with mock data.
          The analysis quality matches reports from top-tier consulting firms.
        </p>
        <div className={styles.testInfo}>
          <span className={styles.badge}>Test Mode</span>
          <span className={styles.company}>TechVision AI - Series A SaaS</span>
        </div>
      </div>
      
      <ExecutiveFrameworkAnalysis />
    </div>
  );
};

export default TestExecutiveFramework;