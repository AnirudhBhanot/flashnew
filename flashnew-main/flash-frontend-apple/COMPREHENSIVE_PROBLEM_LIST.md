# Comprehensive Frontend-Backend Feature Problem List

## Overview
Analysis of the 45 backend features and their implementation in the frontend forms reveals multiple categories of problems. Each problem is categorized and detailed below with the specific action needed.

## Problem Categories

### 1. Fields Collected Correctly but Wrong Location (Need to Move)

#### Product Features Currently in People Form:
- **productRetention30d** → Maps to `product_retention_30d`
  - Current: People form (line 55-56, 327-336)
  - Problem: Product metric in People form
  - Action: Move to a Product form or Market form's product metrics section
  
- **productRetention90d** → Maps to `product_retention_90d`
  - Current: People form (line 56-57, 339-351)
  - Problem: Product metric in People form
  - Action: Move to a Product form or Market form's product metrics section
  
- **dauMauRatio** → Maps to `dau_mau_ratio`
  - Current: People form (line 57, 353-366)
  - Problem: Product metric in People form
  - Action: Move to a Product form or Market form's product metrics section

#### Product Features Currently in Capital Form:
- **annualRevenueRunRate** → Maps to `annual_revenue_run_rate`
  - Current: Capital form (line 52, calculated from monthlyRevenue)
  - Problem: Product metric in Capital form
  - Action: Keep calculation but ensure it's mapped correctly as a product feature

#### Product Features Currently in Market Form:
- **revenueGrowthRate** → Maps to `revenue_growth_rate_percent`
  - Current: Market form (line 57, 346-358)
  - Problem: Already in correct conceptual location
  - Action: None needed, just ensure mapping
  
- **grossMargin** → Maps to `gross_margin_percent`
  - Current: Market form (line 58, 360-372)
  - Problem: Already in correct conceptual location
  - Action: None needed, just ensure mapping
  
- **ltvCacRatio** → Maps to `ltv_cac_ratio`
  - Current: Market form (line 59, 374-387)
  - Problem: Already in correct conceptual location
  - Action: None needed, just ensure mapping

### 2. Fields Collected but Not Sent (Already in Forms)

All these fields are collected in forms but the API transformation is correctly mapping them now:

#### Capital Form Fields (Correctly Mapped):
- ✅ totalRaised → `total_capital_raised_usd`
- ✅ cashOnHand → `cash_on_hand_usd`
- ✅ monthlyBurn → `monthly_burn_usd`
- ✅ runway → `runway_months`
- ✅ burnMultiple → `burn_multiple`
- ✅ primaryInvestor → `investor_tier_primary` (with mapping)
- ✅ hasDebt → `has_debt`
- ✅ fundingStage → `funding_stage`

#### Advantage Form Fields (Correctly Mapped):
- ✅ productStage → `product_stage` (with mapping)
- ✅ patentCount → `patent_count`
- ✅ networkEffects → `network_effects_present`
- ✅ hasDataMoat → `has_data_moat`
- ✅ regulatoryAdvantage → `regulatory_advantage_present`
- ✅ techDifferentiation → `tech_differentiation_score`
- ✅ switchingCosts → `switching_cost_score`
- ✅ brandStrength → `brand_strength_score`
- ✅ scalability → `scalability_score`

#### Market Form Fields (Correctly Mapped):
- ✅ sector → `sector` (with mapping)
- ✅ tam → `tam_size_usd`
- ✅ sam → `sam_size_usd`
- ✅ som → `som_size_usd`
- ✅ marketGrowthRate → `market_growth_rate_percent`
- ✅ customerCount → `customer_count`
- ✅ customerConcentration → `customer_concentration_percent`
- ✅ userGrowthRate → `user_growth_rate_percent`
- ✅ netDollarRetention → `net_dollar_retention_percent`
- ✅ competitionIntensity → `competition_intensity`
- ✅ competitorCount → `competitors_named_count`

#### People Form Fields (Correctly Mapped):
- ✅ founderCount → `founders_count`
- ✅ teamSize → `team_size_full_time`
- ✅ avgExperience → `years_experience_avg`
- ✅ domainExpertiseYears → `domain_expertise_years_avg`
- ✅ priorStartupCount → `prior_startup_experience_count`
- ✅ priorExits → `prior_successful_exits_count`
- ✅ boardAdvisorScore → `board_advisor_experience_score`
- ✅ advisorCount → `advisors_count`
- ✅ teamDiversity → `team_diversity_percent`
- ✅ keyPersonDependency → `key_person_dependency`

### 3. Data Format Issues (Need Conversion)

#### Percentage to Decimal Conversions:
- **product_retention_30d**: Currently sent as percent, needs division by 100
  - Line 163: `Number(people.productRetention30d) / 100 || 0.5`
  - Status: ✅ Already fixed
  
- **product_retention_90d**: Currently sent as percent, needs division by 100
  - Line 164: `Number(people.productRetention90d) / 100 || 0.3`
  - Status: ✅ Already fixed
  
- **dau_mau_ratio**: Currently sent as percent, needs division by 100
  - Line 165: `Number(people.dauMauRatio) / 100 || 0.2`
  - Status: ✅ Already fixed

#### Boolean to Integer Conversions:
- **has_debt**: true/false → 1/0
  - Line 124: `capital.hasDebt ? 1 : 0`
  - Status: ✅ Already fixed
  
- **network_effects_present**: true/false → 1/0
  - Line 128: `advantage.networkEffects ? 1 : 0`
  - Status: ✅ Already fixed
  
- **has_data_moat**: true/false → 1/0
  - Line 129: `advantage.hasDataMoat ? 1 : 0`
  - Status: ✅ Already fixed
  
- **regulatory_advantage_present**: true/false → 1/0
  - Line 130: `advantage.regulatoryAdvantage ? 1 : 0`
  - Status: ✅ Already fixed
  
- **key_person_dependency**: true/false → 1/0
  - Line 159: `people.keyPersonDependency ? 1 : 0`
  - Status: ✅ Already fixed

### 4. Mapping Functions Issues

#### Investor Tier Mapping (Lines 57-66):
Current mappings:
- 'university' → 'angel' ❓ (May need review)
- 'corporate' → 'tier_3' ✅
- 'government' → 'angel' ❓ (May need review)

Missing mappings for form options:
- 'none' → ? (for bootstrapped)
- 'tier_1' → 'tier_1' (probably pass through)
- 'tier_2' → 'tier_2' (probably pass through)

#### Sector Mapping (Lines 68-84):
Current mappings look reasonable but may need expansion based on form options:
- 'ai_ml' → 'deeptech' ✅
- 'real_estate' → 'proptech' ❓ (backend might expect 'proptech' not in mapping)

Form has these options not in mapping:
- 'saas' → ?
- 'ecommerce' → ?
- 'edtech' → ?
- 'biotech' → ?
- 'logistics' → ? (already mapped from 'transportation')

#### Product Stage Mapping (Lines 86-98):
- 'idea' → 'concept' ✅
- 'scaling' → 'growth' ✅

Missing mapping:
- 'launched' → ? (currently mapped to 'launched' but backend might expect different)

### 5. Fields Collected but Not Used

These fields are collected in forms but not part of the 45 backend features:
- **uniqueAdvantage** (Advantage form) - Text field for story
- **debtAmount** (Capital form) - Amount of debt
- **lastValuation** (Capital form) - Not in backend features
- **monthlyRevenue** (Capital form) - Used to calculate ARR but not sent directly
- **hasRevenue** (Capital form) - Toggle, not sent to backend

### 6. Default Value Issues

Several fields have default values when missing:
- Most numeric fields default to 0 (appropriate)
- Scale fields default to 3 (middle value - appropriate)
- Retention fields have fallback defaults:
  - product_retention_30d: 0.5 (50%)
  - product_retention_90d: 0.3 (30%)
  - dau_mau_ratio: 0.2 (20%)

### 7. Validation Issues

The API validation function (lines 343-388) only validates a subset of required fields:
- Missing validation for many ADVANTAGE_FEATURES
- Missing validation for PRODUCT_FEATURES
- Missing validation for some PEOPLE_FEATURES

## Summary of Actions Needed

1. **UI Changes**:
   - Create a dedicated Product section or move product metrics to appropriate forms
   - Move product_retention_30d, product_retention_90d, and dau_mau_ratio out of People form

2. **Mapping Updates**:
   - Complete the investor tier mapping function
   - Complete the sector mapping function
   - Review product stage mapping

3. **Validation Updates**:
   - Add validation for all 45 required fields in validateData function

4. **Data Flow**:
   - All fields appear to be correctly collected and transformed now
   - Main issue is organization (product metrics in wrong forms)

## Current Status
✅ All 45 backend features are being collected
✅ All 45 backend features are being correctly transformed and sent
✅ Data format conversions are implemented correctly
❓ Some mapping functions may need completion
❌ Product metrics are in the wrong form (People instead of Product/Market)
❌ Validation is incomplete