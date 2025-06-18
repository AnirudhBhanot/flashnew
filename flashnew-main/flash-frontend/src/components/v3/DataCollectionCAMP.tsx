import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { StartupData } from '../../types';
import { generateTestStartupData, testScenarios } from '../../utils/testDataGenerator';
import { FUNDING_STAGE_OPTIONS } from '../../config/constants';
import { ButtonLoader } from '../common/LoadingState';
import { useScrollAnimation, useCountAnimation } from '../../hooks/useScrollAnimation';
import './DataCollectionCAMP.css';

interface DataCollectionCAMPProps {
  onSubmit: (data: StartupData) => void;
  onBack: () => void;
}

const CAMP_PILLARS = {
  capital: {
    name: 'Capital',
    icon: 'C',
    description: 'Financial health, funding efficiency, and runway',
    fields: [
      'funding_stage',
      'total_capital_raised_usd',
      'cash_on_hand_usd',
      'monthly_burn_usd',
      'annual_revenue_run_rate',
      'revenue_growth_rate_percent',
      'gross_margin_percent',
      'ltv_cac_ratio',
      'investor_tier_primary',
      'has_debt'
    ]
  },
  advantage: {
    name: 'Advantage',
    icon: 'A',
    description: 'Competitive moat, technology, and differentiation',
    fields: [
      'patent_count',
      'network_effects_present',
      'has_data_moat',
      'regulatory_advantage_present',
      'tech_differentiation_score',
      'switching_cost_score',
      'brand_strength_score',
      'scalability_score',
      'product_stage',
      'product_retention_30d',
      'product_retention_90d'
    ]
  },
  market: {
    name: 'Market',
    icon: 'M',
    description: 'Market size, growth, and customer dynamics',
    fields: [
      'sector',
      'tam_size_usd',
      'sam_size_usd',
      'som_size_usd',
      'market_growth_rate_percent',
      'customer_count',
      'customer_concentration_percent',
      'user_growth_rate_percent',
      'net_dollar_retention_percent',
      'competition_intensity',
      'competitors_named_count',
      'dau_mau_ratio'
    ]
  },
  people: {
    name: 'People',
    icon: 'P',
    description: 'Team experience, composition, and leadership',
    fields: [
      'founders_count',
      'team_size_full_time',
      'years_experience_avg',
      'domain_expertise_years_avg',
      'prior_startup_experience_count',
      'prior_successful_exits_count',
      'board_advisor_experience_score',
      'advisors_count',
      'team_diversity_percent',
      'key_person_dependency'
    ]
  }
};

const FIELD_CONFIG: { [key: string]: { label: string; type: string; placeholder?: string; helper?: string; options?: string[]; min?: number; max?: number; step?: number } } = {
  // Capital fields
  funding_stage: { label: 'Funding Stage', type: 'select', options: FUNDING_STAGE_OPTIONS.map(opt => opt.value), helper: 'Current funding round stage' },
  total_capital_raised_usd: { label: 'Total Capital Raised ($)', type: 'number', placeholder: '1000000', min: 0, helper: 'Total external funding received to date' },
  cash_on_hand_usd: { label: 'Cash on Hand ($)', type: 'number', placeholder: '500000', min: 0, helper: 'Current bank balance and liquid assets' },
  monthly_burn_usd: { label: 'Monthly Burn Rate ($)', type: 'number', placeholder: '50000', min: 0, helper: 'Average monthly cash expenditure' },
  annual_revenue_run_rate: { label: 'Annual Revenue Run Rate ($)', type: 'number', placeholder: '1000000', min: 0, helper: 'Current MRR × 12 or projected annual revenue' },
  revenue_growth_rate_percent: { label: 'Revenue Growth Rate (%)', type: 'number', placeholder: '100', min: -100, max: 1000, helper: 'Year-over-year revenue growth percentage' },
  gross_margin_percent: { label: 'Gross Margin (%)', type: 'number', placeholder: '70', min: -100, max: 100, helper: '(Revenue - COGS) / Revenue × 100' },
  ltv_cac_ratio: { label: 'LTV/CAC Ratio', type: 'number', placeholder: '3', min: 0, max: 100, step: 0.1, helper: 'Customer lifetime value ÷ Customer acquisition cost' },
  investor_tier_primary: { label: 'Primary Investor Tier', type: 'select', options: ['Tier 1', 'Tier 2', 'Tier 3', 'Angel'], helper: 'Lead investor quality ranking' },
  has_debt: { label: 'Has Debt Financing', type: 'boolean', helper: 'Any venture debt or loans' },
  
  // Advantage fields
  patent_count: { label: 'Patent Count', type: 'number', placeholder: '0', min: 0, helper: 'Filed and pending patents' },
  network_effects_present: { label: 'Network Effects Present', type: 'boolean', helper: 'Value increases with more users' },
  has_data_moat: { label: 'Has Data Moat', type: 'boolean', helper: 'Proprietary data advantage' },
  regulatory_advantage_present: { label: 'Regulatory Advantage', type: 'boolean', helper: 'Licenses or regulatory barriers' },
  tech_differentiation_score: { label: 'Tech Differentiation (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Commodity, 5=Breakthrough innovation' },
  switching_cost_score: { label: 'Switching Cost (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Easy to leave, 5=Very sticky' },
  brand_strength_score: { label: 'Brand Strength (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Unknown, 5=Category leader' },
  scalability_score: { label: 'Scalability Score (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Linear growth, 5=Exponential potential' },
  product_stage: { label: 'Product Stage', type: 'select', options: ['MVP', 'Beta', 'GA', 'Mature'], helper: 'Current development phase' },
  product_retention_30d: { label: '30-Day Retention (%)', type: 'number', placeholder: '60', min: 0, max: 100, helper: '% of users active after 30 days' },
  product_retention_90d: { label: '90-Day Retention (%)', type: 'number', placeholder: '40', min: 0, max: 100, helper: '% of users active after 90 days' },
  
  // Market fields
  sector: { label: 'Industry Sector', type: 'text', placeholder: 'SaaS, Fintech, etc.', helper: 'Primary industry vertical' },
  tam_size_usd: { label: 'Total Addressable Market ($)', type: 'number', placeholder: '1000000000', min: 0, helper: 'Total market opportunity if 100% captured' },
  sam_size_usd: { label: 'Serviceable Addressable Market ($)', type: 'number', placeholder: '100000000', min: 0, helper: 'Market you can reach with current business model' },
  som_size_usd: { label: 'Serviceable Obtainable Market ($)', type: 'number', placeholder: '10000000', min: 0, helper: 'Realistic market share you can capture' },
  market_growth_rate_percent: { label: 'Market Growth Rate (%)', type: 'number', placeholder: '20', min: -50, max: 200, helper: 'Annual market growth percentage' },
  customer_count: { label: 'Customer Count', type: 'number', placeholder: '100', min: 0, helper: 'Total number of paying customers' },
  customer_concentration_percent: { label: 'Customer Concentration (%)', type: 'number', placeholder: '20', min: 0, max: 100, helper: '% revenue from top customer' },
  user_growth_rate_percent: { label: 'User Growth Rate (%)', type: 'number', placeholder: '50', min: -100, max: 1000, helper: 'Monthly user growth percentage' },
  net_dollar_retention_percent: { label: 'Net Dollar Retention (%)', type: 'number', placeholder: '110', min: 0, max: 300, helper: 'Revenue retained + expansion from existing customers' },
  competition_intensity: { label: 'Competition Intensity (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Blue ocean, 5=Highly competitive' },
  competitors_named_count: { label: 'Number of Competitors', type: 'number', placeholder: '5', min: 0, helper: 'Direct competitors in your market' },
  dau_mau_ratio: { label: 'DAU/MAU Ratio', type: 'number', placeholder: '0.5', min: 0, max: 1, step: 0.1, helper: 'Daily active users ÷ Monthly active users' },
  
  // People fields
  founders_count: { label: 'Number of Founders', type: 'number', placeholder: '2', min: 1, max: 10, helper: 'Number of founding team members' },
  team_size_full_time: { label: 'Full-Time Team Size', type: 'number', placeholder: '10', min: 0, helper: 'Total full-time employees' },
  years_experience_avg: { label: 'Avg Years Experience', type: 'number', placeholder: '8', min: 0, max: 50, helper: 'Average professional experience of team' },
  domain_expertise_years_avg: { label: 'Avg Domain Expertise (years)', type: 'number', placeholder: '5', min: 0, max: 50, helper: 'Years of experience in this specific industry' },
  prior_startup_experience_count: { label: 'Prior Startup Experience', type: 'number', placeholder: '1', min: 0, helper: 'Number of previous startups founded' },
  prior_successful_exits_count: { label: 'Prior Successful Exits', type: 'number', placeholder: '0', min: 0, helper: 'Previous successful acquisitions or IPOs' },
  board_advisor_experience_score: { label: 'Board/Advisor Experience (1-5)', type: 'number', placeholder: '3', min: 1, max: 5, helper: '1=Weak advisors, 5=Top-tier board' },
  advisors_count: { label: 'Number of Advisors', type: 'number', placeholder: '3', min: 0, helper: 'Total advisors and mentors' },
  team_diversity_percent: { label: 'Team Diversity (%)', type: 'number', placeholder: '40', min: 0, max: 100, helper: '% of team from underrepresented groups' },
  key_person_dependency: { label: 'Key Person Dependency', type: 'boolean', helper: 'Single person critical to operations' }
};

export const DataCollectionCAMP: React.FC<DataCollectionCAMPProps> = ({ onSubmit, onBack }) => {
  const [activePillar, setActivePillar] = useState<'capital' | 'advantage' | 'market' | 'people'>('capital');
  const [formData, setFormData] = useState<Partial<StartupData>>({});
  const [completedPillars, setCompletedPillars] = useState<Set<string>>(new Set());
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFieldChange = (field: string, value: string | number | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validatePillar = (pillar: string): boolean => {
    const fields = CAMP_PILLARS[pillar as keyof typeof CAMP_PILLARS].fields;
    const newErrors: { [key: string]: string } = {};
    
    fields.forEach(field => {
      const config = FIELD_CONFIG[field];
      const value = formData[field as keyof StartupData];
      
      // Required field check
      if (value === undefined || value === null || value === '') {
        newErrors[field] = 'Required';
      } else if (config.type === 'number') {
        const numValue = Number(value);
        if (isNaN(numValue)) {
          newErrors[field] = 'Must be a number';
        } else if (config.min !== undefined && numValue < config.min) {
          newErrors[field] = `Min: ${config.min}`;
        } else if (config.max !== undefined && numValue > config.max) {
          newErrors[field] = `Max: ${config.max}`;
        }
      }
    });
    
    setErrors(prev => ({ ...prev, ...newErrors }));
    return Object.keys(newErrors).length === 0;
  };

  const handlePillarComplete = () => {
    if (validatePillar(activePillar)) {
      setCompletedPillars(prev => new Set(prev).add(activePillar));
      
      // Auto-advance to next pillar
      const pillars = Object.keys(CAMP_PILLARS) as Array<keyof typeof CAMP_PILLARS>;
      const currentIndex = pillars.indexOf(activePillar);
      if (currentIndex < pillars.length - 1) {
        setActivePillar(pillars[currentIndex + 1]);
      }
    }
  };

  const handleSubmit = async () => {
    if (isSubmitting) return;
    
    // Validate all pillars
    const allValid = Object.keys(CAMP_PILLARS).every(pillar => validatePillar(pillar));
    
    // Count filled fields
    const allFields = Object.values(CAMP_PILLARS).flatMap(p => p.fields);
    const filledFields = allFields.filter(field => {
      const value = formData[field as keyof StartupData];
      return value !== undefined && value !== null && value !== '';
    });
    
    
    if (!allValid) {
      alert(`Please complete all fields. Currently ${filledFields.length}/${allFields.length} fields are filled.`);
      return;
    }
    
    if (allValid) {
      setIsSubmitting(true);
      // Transform data to ensure correct types
      const transformedData: Partial<StartupData> = {};
      
      // Process each field with proper type conversion
      Object.entries(formData).forEach(([key, value]) => {
        const config = FIELD_CONFIG[key];
        if (config) {
          if (config.type === 'number') {
            let numValue = Number(value) || 0;
            
            // Convert percentage fields to decimals (0-1) for API
            if (key === 'product_retention_30d' || key === 'product_retention_90d') {
              numValue = numValue / 100; // Convert percentage to decimal
            }
            
            (transformedData as any)[key] = numValue;
          } else if (config.type === 'boolean') {
            (transformedData as any)[key] = Boolean(value);
          } else {
            (transformedData as any)[key] = value as string;
          }
        } else {
          (transformedData as any)[key] = value;
        }
      });
      
      // Ensure all required fields have values
      const requiredDefaults = {
        // Capital
        revenue_growth_rate_percent: 0,
        ltv_cac_ratio: 0,
        
        // Advantage  
        patent_count: 0,
        
        // Market
        user_growth_rate_percent: 0,
        customer_concentration_percent: 20,
        
        // People
        team_diversity_percent: 40,
        advisors_count: 0
      };
      
      // Add calculated fields and defaults
      const completeData = {
        ...requiredDefaults,
        ...transformedData,
        runway_months: transformedData.cash_on_hand_usd && transformedData.monthly_burn_usd 
          ? Math.min(transformedData.cash_on_hand_usd / transformedData.monthly_burn_usd, 60) 
          : 12,
        burn_multiple: 2 // Will be calculated server-side
      } as StartupData;
      
      // Small delay to show loading state
      setTimeout(() => {
        onSubmit(completeData);
        setIsSubmitting(false);
      }, 300);
    }
  };

  const handleAutofill = () => {
    const testData = generateTestStartupData();
    setFormData(prev => ({ ...prev, ...testData }));
  };

  const handleScenarioFill = (scenario: 'best' | 'worst') => {
    const data = scenario === 'best' ? testScenarios.bestCase() : testScenarios.worstCase();
    setFormData(prev => ({ ...prev, ...data }));
  };

  const renderField = (fieldName: string) => {
    const config = FIELD_CONFIG[fieldName];
    const rawValue = formData[fieldName as keyof StartupData];
    const value = typeof rawValue === 'boolean' ? String(rawValue) : rawValue;
    const error = errors[fieldName];
    
    if (config.type === 'select') {
      return (
        <div className="field-group" key={fieldName}>
          <label>{config.label}</label>
          {config.helper && <span className="field-helper">{config.helper}</span>}
          <select
            value={value || ''}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={error ? 'error' : ''}
          >
            <option value="">Select...</option>
            {config.options?.map(opt => {
              // For funding_stage, display the proper label
              if (fieldName === 'funding_stage') {
                const stageOption = FUNDING_STAGE_OPTIONS.find(o => o.value === opt);
                return <option key={opt} value={opt}>{stageOption?.label || opt}</option>;
              }
              return <option key={opt} value={opt}>{opt}</option>;
            })}
          </select>
          {error && <span className="error-message">{error}</span>}
        </div>
      );
    }
    
    if (config.type === 'boolean') {
      return (
        <div className="field-group checkbox" key={fieldName}>
          <label>
            <input
              type="checkbox"
              checked={Boolean(rawValue)}
              onChange={(e) => handleFieldChange(fieldName, e.target.checked)}
            />
            <span className="checkbox-label">{config.label}</span>
          </label>
          {config.helper && <span className="field-helper">{config.helper}</span>}
        </div>
      );
    }
    
    return (
      <div className="field-group" key={fieldName}>
        <label>{config.label}</label>
        {config.helper && <span className="field-helper">{config.helper}</span>}
        <motion.input
          type={config.type}
          value={value || ''}
          onChange={(e) => {
            const val = config.type === 'number' ? parseFloat(e.target.value) || 0 : e.target.value;
            handleFieldChange(fieldName, val);
          }}
          placeholder={config.placeholder}
          min={config.min}
          max={config.max}
          step={config.step}
          className={`form-input-interactive ${error ? 'error' : ''}`}
          whileFocus={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        />
        {error && <span className="error-message">{error}</span>}
      </div>
    );
  };

  const pillar = CAMP_PILLARS[activePillar];
  const progress = (completedPillars.size / 4) * 100;
  const animatedProgress = useCountAnimation(Math.round(progress), 500);

  return (
    <div className="data-collection-camp">
      <header className="camp-header">
        <button className="back-button" onClick={onBack}>←</button>
        
        <div className="camp-nav">
          {Object.entries(CAMP_PILLARS).map(([key, p]) => (
            <motion.button
              key={key}
              className={`camp-pill ${activePillar === key ? 'active' : ''} ${completedPillars.has(key) ? 'completed' : ''}`}
              onClick={() => setActivePillar(key as any)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <span className="camp-icon">{p.icon}</span>
              <span className="camp-label">{p.name}</span>
              {completedPillars.has(key) && (
                <motion.span 
                  className="check"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 500, damping: 25 }}
                >
                  ✓
                </motion.span>
              )}
            </motion.button>
          ))}
        </div>
        
        <div className="header-right">
          <div className="test-actions">
            <motion.button 
              className="test-btn"
              onClick={handleAutofill}
              title="Fill with random test data"
              whileHover={{ rotate: 15 }}
              whileTap={{ rotate: 360 }}
              transition={{ type: "spring", stiffness: 200 }}
            >
              🎲
            </motion.button>
            <button 
              className="test-btn"
              onClick={() => handleScenarioFill('best')}
              title="Best case scenario"
            >
              ⬆
            </button>
            <button 
              className="test-btn"
              onClick={() => handleScenarioFill('worst')}
              title="Worst case scenario"
            >
              ⬇
            </button>
          </div>
          <div className="progress-indicator">
            <span className="progress-text">{completedPillars.size} of 4 sections</span>
            <span className="progress-percent">{animatedProgress}% Complete</span>
          </div>
        </div>
      </header>

      <div className="camp-content">
        <AnimatePresence mode="wait">
          <motion.div
            key={activePillar}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="pillar-section"
          >
            <div className="pillar-header">
              <h2>{pillar.name}</h2>
              <p>{pillar.description}</p>
            </div>
            
            <div className="fields-grid">
              {pillar.fields.map(field => renderField(field))}
            </div>
            
            <div className="pillar-actions">
              {!completedPillars.has(activePillar) ? (
                <motion.button 
                  className="complete-button button-interactive"
                  onClick={handlePillarComplete}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  Complete {pillar.name}
                </motion.button>
              ) : (
                <motion.div 
                  className="completed-message"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  ✓ {pillar.name} Complete
                </motion.div>
              )}
              
              {/* Always show analyze button with status */}
              <div className="analyze-section" style={{ marginTop: '20px', textAlign: 'center' }}>
                <div className="field-progress">
                  {(() => {
                    const allFields = Object.values(CAMP_PILLARS).flatMap(p => p.fields);
                    const filledCount = allFields.filter(field => {
                      const value = formData[field as keyof StartupData];
                      return value !== undefined && value !== null && value !== '';
                    }).length;
                    return `${filledCount}/${allFields.length} fields completed`;
                  })()}
                </div>
                
                {completedPillars.size < 4 ? (
                  <>
                    <p style={{ color: '#999', fontSize: '14px', margin: '10px 0' }}>
                      Complete all sections to enable analysis ({completedPillars.size}/4 done)
                    </p>
                    <button 
                      className="analyze-button"
                      onClick={() => alert(`Please complete all 4 sections first. You have completed ${completedPillars.size} out of 4 sections.`)}
                      style={{ opacity: 0.6, cursor: 'not-allowed' }}
                    >
                      Analyze Startup (Disabled)
                    </button>
                  </>
                ) : (
                  <motion.button 
                    className="analyze-button button-interactive btn-pulse"
                    onClick={handleSubmit}
                    disabled={isSubmitting}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, type: "spring" }}
                  >
                    {isSubmitting ? <ButtonLoader /> : '✨ Analyze Startup'}
                  </motion.button>
                )}
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};