// Test Apple UI Frontend-Backend Connectivity
const API_BASE_URL = 'http://localhost:8001';

async function testAppleUIConnectivity() {
  console.log('Testing Apple UI Frontend-Backend Connectivity...\n');
  
  // Test 1: Check if Apple UI is accessible
  try {
    const appleUIResponse = await fetch('http://localhost:3001');
    console.log('✅ Apple UI Frontend:', appleUIResponse.ok ? 'Running on port 3001' : 'Not accessible');
  } catch (error) {
    console.log('❌ Apple UI Frontend Failed:', error.message);
  }
  
  // Test 2: API Health Check from Apple UI perspective
  try {
    const healthResponse = await fetch(`${API_BASE_URL}/health`);
    const healthData = await healthResponse.json();
    console.log('✅ Backend Health Check:', healthData);
  } catch (error) {
    console.log('❌ Backend Health Check Failed:', error.message);
  }
  
  // Test 3: Test with Apple UI formatted data
  try {
    const appleUIData = {
      // Company Info
      funding_stage: "seed",
      sector: "saas",
      
      // Capital
      total_capital_raised_usd: 2000000,
      cash_on_hand_usd: 1500000,
      monthly_burn_usd: 100000,
      runway_months: 15,
      burn_multiple: 2.0,
      investor_tier_primary: "tier_2",
      has_debt: false,
      
      // Advantage
      patent_count: 2,
      network_effects_present: true,
      has_data_moat: true,
      regulatory_advantage_present: false,
      tech_differentiation_score: 4,
      switching_cost_score: 3,
      brand_strength_score: 3,
      scalability_score: 4,
      
      // Market
      tam_size_usd: 50000000000,
      sam_size_usd: 5000000000,
      som_size_usd: 500000000,
      market_growth_rate_percent: 30,
      customer_count: 100,
      customer_concentration_percent: 20,
      user_growth_rate_percent: 200,
      net_dollar_retention_percent: 120,
      competition_intensity: 3,
      competitors_named_count: 5,
      
      // People
      founders_count: 2,
      team_size_full_time: 15,
      years_experience_avg: 12,
      domain_expertise_years_avg: 8,
      prior_startup_experience_count: 2,
      prior_successful_exits_count: 1,
      board_advisor_experience_score: 4,
      advisors_count: 3,
      team_diversity_percent: 40,
      key_person_dependency: false,
      
      // Product metrics
      product_stage: "growth",
      product_retention_30d: 0.85,
      product_retention_90d: 0.75,
      dau_mau_ratio: 0.6,
      annual_revenue_run_rate: 2400000,
      revenue_growth_rate_percent: 200,
      gross_margin_percent: 85,
      ltv_cac_ratio: 3.5
    };
    
    const predictionResponse = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(appleUIData)
    });
    
    if (predictionResponse.ok) {
      const result = await predictionResponse.json();
      console.log('✅ Apple UI Data Prediction:', {
        success_probability: result.success_probability,
        risk_level: result.risk_level,
        camp_scores: result.camp_scores
      });
    } else {
      const error = await predictionResponse.json();
      console.log('❌ Prediction Failed:', error);
    }
  } catch (error) {
    console.log('❌ Apple UI Data Test Failed:', error.message);
  }
  
  console.log('\n📱 Apple UI Connectivity Test Complete!');
  console.log('\nAccess Points:');
  console.log('- Original Frontend: http://localhost:3000');
  console.log('- Apple UI Frontend: http://localhost:3001');
  console.log('- Backend API: http://localhost:8001');
}

// Run the test
testAppleUIConnectivity();