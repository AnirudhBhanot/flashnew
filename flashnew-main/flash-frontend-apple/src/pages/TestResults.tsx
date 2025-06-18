import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../store/assessmentStore';

const TestResults: React.FC = () => {
  const navigate = useNavigate();
  const { setResults, setData } = useAssessmentStore();

  useEffect(() => {
    // Set test assessment data
    const testData = {
      companyInfo: {
        companyName: 'Test Startup',
        stage: 'seed',
        industry: 'tech',
        sector: 'saas'
      },
      capital: {
        cashOnHand: 1000000,
        annualRevenueRunRate: 500000,
        runwayMonths: 12,
        revenueGrowthRate: 100
      },
      advantage: {
        competitiveAdvantage: 7
      },
      market: {
        marketSize: 1000000000
      },
      people: {
        teamSize: 10,
        foundersExperience: 5
      }
    };

    // Set test results
    const testResults = {
      successProbability: 0.65,
      confidence: 0.85,
      scores: {
        capital: 0.7,
        advantage: 0.65,
        market: 0.75,
        people: 0.6
      },
      insights: [
        'Strong market potential with growing demand',
        'Capital position provides adequate runway',
        'Team capabilities need strengthening'
      ],
      recommendations: [
        'Focus on hiring senior talent',
        'Accelerate product development',
        'Strengthen IP protection'
      ]
    };

    setData(testData);
    setResults(testResults);
    
    // Navigate to results
    navigate('/results');
  }, [navigate, setData, setResults]);

  return <div>Redirecting to results...</div>;
};

export default TestResults;