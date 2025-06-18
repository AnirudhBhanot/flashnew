// Test Frontend-Backend Connectivity
const API_BASE_URL = 'http://localhost:8001';

async function testConnectivity() {
  console.log('Testing FLASH Frontend-Backend Connectivity...\n');
  
  // Test 1: Health Check
  try {
    const healthResponse = await fetch(`${API_BASE_URL}/health`);
    const healthData = await healthResponse.json();
    console.log('✅ Health Check:', healthData);
  } catch (error) {
    console.log('❌ Health Check Failed:', error.message);
  }
  
  // Test 2: Config Endpoint (with API key)
  try {
    const configResponse = await fetch(`${API_BASE_URL}/config/stage-weights`, {
      headers: {
        'X-API-Key': 'test-api-key-123'
      }
    });
    const configData = await configResponse.json();
    console.log('✅ Config Endpoint:', Object.keys(configData).join(', '));
  } catch (error) {
    console.log('❌ Config Endpoint Failed:', error.message);
  }
  
  // Test 3: LLM Status
  try {
    const llmResponse = await fetch(`${API_BASE_URL}/api/analysis/status`);
    const llmData = await llmResponse.json();
    console.log('✅ LLM Status:', llmData);
  } catch (error) {
    console.log('❌ LLM Status Failed:', error.message);
  }
  
  // Test 4: Simple Prediction
  try {
    const predictionData = {
      funding_stage: "seed",
      sector: "saas",
      total_capital_raised_usd: 1000000,
      cash_on_hand_usd: 800000,
      monthly_burn_usd: 50000,
      runway_months: 16,
      burn_multiple: 2.0,
      investor_tier_primary: "tier_2",
      has_debt: false,
      patent_count: 0,
      network_effects_present: true,
      has_data_moat: false,
      regulatory_advantage_present: false,
      tech_differentiation_score: 3,
      switching_cost_score: 2,
      brand_strength_score: 2,
      scalability_score: 4,
      tam_size_usd: 10000000000,
      sam_size_usd: 1000000000,
      som_size_usd: 100000000,
      market_growth_rate_percent: 20,
      customer_count: 50,
      customer_concentration_percent: 30,
      user_growth_rate_percent: 100,
      net_dollar_retention_percent: 105,
      competition_intensity: 3,
      competitors_named_count: 5,
      founders_count: 2,
      team_size_full_time: 10,
      years_experience_avg: 8,
      domain_expertise_years_avg: 5,
      prior_startup_experience_count: 1,
      prior_successful_exits_count: 0,
      board_advisor_experience_score: 3,
      advisors_count: 2,
      team_diversity_percent: 30,
      key_person_dependency: false,
      product_stage: "beta",
      product_retention_30d: 0.75,
      product_retention_90d: 0.60,
      dau_mau_ratio: 0.5,
      annual_revenue_run_rate: 600000,
      revenue_growth_rate_percent: 100,
      gross_margin_percent: 75,
      ltv_cac_ratio: 2.5
    };
    
    const predictionResponse = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(predictionData)
    });
    
    if (predictionResponse.ok) {
      const result = await predictionResponse.json();
      console.log('✅ Prediction Test:', {
        success_probability: result.success_probability,
        confidence: result.confidence,
        risk_level: result.risk_level
      });
    } else {
      const error = await predictionResponse.json();
      console.log('❌ Prediction Failed:', error);
    }
  } catch (error) {
    console.log('❌ Prediction Test Failed:', error.message);
  }
  
  console.log('\n🏁 Connectivity Test Complete!');
}

// Run the test
testConnectivity();