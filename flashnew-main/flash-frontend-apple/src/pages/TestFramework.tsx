import React, { useEffect } from 'react';
import StrategicFrameworkAnalysis from '../components/StrategicFrameworkAnalysis';
import useAssessmentStore from '../store/assessmentStore';

const TestFramework: React.FC = () => {
  const { updateData } = useAssessmentStore();

  useEffect(() => {
    // Set minimal test data to verify component works
    const testData = {
      companyInfo: {
        companyName: 'Test Company',
        website: 'https://test.com',
        description: 'Test description'
      },
      capital: {
        fundingStage: 'seed',
        totalRaised: 1000000,
        cashOnHand: 500000,
        monthlyBurn: 50000,
        runwayMonths: 10,
        annualRevenue: 600000
      },
      market: {
        sector: 'saas',
        tam: 10000000000,
        sam: 1000000000,
        som: 10000000,
        marketGrowthRate: 25,
        competitorCount: 20,
        customerAcquisitionCost: 1000,
        lifetimeValue: 10000
      },
      advantage: {
        productStage: 'mvp',
        npsScore: 45,
        churnRate: 6
      },
      people: {
        fullTimeEmployees: 15
      }
    };

    const testResults = {
      successProbability: 0.65,
      scores: {
        capital: 0.70,
        advantage: 0.68,
        market: 0.72,
        people: 0.64
      }
    };

    // Update store
    updateData('companyInfo', testData.companyInfo);
    updateData('capital', testData.capital);
    updateData('market', testData.market);
    updateData('advantage', testData.advantage);
    updateData('people', testData.people);
    updateData('results', testResults);
  }, [updateData]);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Framework Analysis Test</h1>
      <StrategicFrameworkAnalysis />
    </div>
  );
};

export default TestFramework;