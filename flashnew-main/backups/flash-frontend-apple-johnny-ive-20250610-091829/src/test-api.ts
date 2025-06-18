// Quick test script for API integration
import { apiService } from './services/api';

const testData = {
  companyInfo: {
    companyName: 'Test Startup',
    website: 'https://teststartup.com',
    industry: 'SaaS',
    foundedDate: '2020-01-01',
    stage: 'Series A',
    location: 'San Francisco, CA',
    description: 'A test startup for API integration',
  },
  capital: {
    totalFundingRaised: '5000000',
    lastRoundAmount: '3000000',
    lastRoundDate: '2023-01-01',
    fundingRounds: '2',
    monthlyBurnRate: '100000',
    runwayMonths: '18',
    annualRevenueRunRate: '1200000',
    revenueGrowthRate: '150',
    grossMargin: '80',
    investorTypes: ['tier-1-vc'],
  },
  advantage: {
    moatStrength: 7,
    advantages: ['proprietary-data', 'network-effects', 'brand-recognition'],
    hasPatents: true,
    patentCount: 3,
    uniqueValueProp: 'Revolutionary AI-powered analytics',
  },
  market: {
    marketSize: '50000000000',
    marketGrowthRate: '25',
    competitionLevel: 3,
    targetMarket: 'b2b',
  },
  people: {
    teamSize: '25',
    foundersCount: '2',
    industryExperience: 8,
    previousStartups: true,
    previousExits: '1',
    keyHires: ['cto', 'vp-sales'],
  },
};

export async function testAPIIntegration() {
  console.log('Testing API Integration...');
  
  try {
    // Test health check
    console.log('1. Testing health check...');
    const isHealthy = await apiService.checkHealth();
    console.log('   Health check:', isHealthy ? 'PASSED' : 'FAILED');
    
    // Test validation
    console.log('2. Testing data validation...');
    const validation = await apiService.validateData(testData);
    console.log('   Validation:', validation.valid ? 'PASSED' : 'FAILED');
    if (!validation.valid) {
      console.log('   Errors:', validation.errors);
    }
    
    // Test prediction
    console.log('3. Testing prediction...');
    const prediction = await apiService.submitAssessment(testData);
    console.log('   Prediction result:', {
      successProbability: prediction.successProbability,
      confidence: prediction.confidence,
      scores: prediction.scores,
    });
    
    // Test detailed analysis
    console.log('4. Testing detailed analysis...');
    const analysis = await apiService.getDetailedAnalysis(testData);
    console.log('   Analysis includes detailed insights:', !!analysis.detailedAnalysis);
    
    console.log('\\nAll tests completed!');
  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run the test
testAPIIntegration();