import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { 
  FormField, 
  MinimalInput, 
  MinimalSelect, 
  MinimalToggle,
  MinimalProgress 
} from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './CapitalMinimal.module.scss';

interface CapitalData {
  totalRaised: number | string;
  cashOnHand: number | string;
  monthlyBurn: number | string;
  runway: number | string;
  burnMultiple: number | string;
  primaryInvestor: string;
  hasDebt: boolean;
  debtAmount: number | string;
  fundingStage: string;
  annualRevenueRunRate: number | string;
  monthlyRevenue: number | string;
  hasRevenue: boolean;
  lastValuation: number | string;
}

const Capital: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const storeData = useAssessmentStore(state => state.data);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  const [currentField, setCurrentField] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Use store data if available, otherwise use wizard data
  const capitalData = storeData.capital || data.capital;
  
  const [formData, setFormData] = useState<CapitalData>({
    totalRaised: capitalData?.totalRaised || '',
    cashOnHand: capitalData?.cashOnHand || '',
    monthlyBurn: capitalData?.monthlyBurn || '',
    lastValuation: capitalData?.lastValuation || '',
    primaryInvestor: capitalData?.primaryInvestor || '',
    hasDebt: capitalData?.hasDebt || false,
    debtAmount: capitalData?.debtAmount || '',
    fundingStage: capitalData?.fundingStage || '',
    annualRevenueRunRate: capitalData?.annualRevenueRunRate || '',
    monthlyRevenue: capitalData?.monthlyRevenue || '',
    hasRevenue: capitalData?.hasRevenue || false,
    runway: capitalData?.runway || '',
    burnMultiple: capitalData?.burnMultiple || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof CapitalData, string>>>({});

  // Update form when store data changes (e.g., from autofill)
  useEffect(() => {
    const capitalData = storeData.capital;
    if (capitalData) {
      setFormData({
        totalRaised: capitalData.totalRaised || '',
        cashOnHand: capitalData.cashOnHand || '',
        monthlyBurn: capitalData.monthlyBurn || '',
        lastValuation: capitalData.lastValuation || '',
        primaryInvestor: capitalData.primaryInvestor || '',
        hasDebt: capitalData.hasDebt || false,
        debtAmount: capitalData.debtAmount || '',
        fundingStage: capitalData.fundingStage || '',
        annualRevenueRunRate: capitalData.annualRevenueRunRate || '',
        monthlyRevenue: capitalData.monthlyRevenue || '',
        hasRevenue: capitalData.hasRevenue || false,
        runway: capitalData.runway || '',
        burnMultiple: capitalData.burnMultiple || '',
      });
      setTouched(true);
    }
  }, [storeData.capital]);

  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ capital: formData });
        // Also update the store
        useAssessmentStore.getState().updateData('capital', formData);
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  // Calculate runway automatically
  useEffect(() => {
    const burn = Number(formData.monthlyBurn) || 0;
    const cash = Number(formData.cashOnHand) || 0;
    if (burn > 0 && cash > 0) {
      const calculatedRunway = Math.floor(cash / burn);
      setFormData(prev => ({ ...prev, runway: calculatedRunway }));
    }
  }, [formData.monthlyBurn, formData.cashOnHand]);
  
  // Calculate burn multiple automatically
  useEffect(() => {
    const revenue = Number(formData.monthlyRevenue) || 0;
    const burn = Number(formData.monthlyBurn) || 0;
    if (revenue > 0 && burn > 0) {
      const calculatedBurnMultiple = (burn / revenue).toFixed(2);
      setFormData(prev => ({ ...prev, burnMultiple: calculatedBurnMultiple }));
    }
  }, [formData.monthlyRevenue, formData.monthlyBurn]);
  
  // Calculate ARR automatically from monthly revenue
  useEffect(() => {
    const monthlyRev = Number(formData.monthlyRevenue) || 0;
    if (monthlyRev > 0) {
      const calculatedARR = monthlyRev * 12;
      setFormData(prev => ({ ...prev, annualRevenueRunRate: calculatedARR }));
    }
  }, [formData.monthlyRevenue]);
  
  const updateField = (field: keyof CapitalData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof CapitalData, string>> = {};
    
    if (!formData.fundingStage) {
      newErrors.fundingStage = 'Please select your funding stage';
    }
    
    if (!formData.totalRaised && formData.totalRaised !== 0) {
      newErrors.totalRaised = 'Total funding is required';
    }
    
    if (!formData.cashOnHand && formData.cashOnHand !== 0) {
      newErrors.cashOnHand = 'Cash on hand is required';
    }
    
    if (!formData.monthlyBurn && formData.monthlyBurn !== 0) {
      newErrors.monthlyBurn = 'Monthly burn rate is required';
    }
    
    if (!formData.lastValuation && formData.lastValuation !== 0) {
      newErrors.lastValuation = 'Last valuation is required';
    }
    
    if (!formData.primaryInvestor) {
      newErrors.primaryInvestor = 'Please select your primary investor type';
    }
    
    if (formData.hasDebt && (!formData.debtAmount || formData.debtAmount === 0)) {
      newErrors.debtAmount = 'Please specify the debt amount';
    }
    
    if (formData.hasRevenue && (!formData.monthlyRevenue || formData.monthlyRevenue === 0)) {
      newErrors.monthlyRevenue = 'Please specify your monthly revenue';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ capital: formData });
      nextStep();
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && e.shiftKey) {
      e.preventDefault();
      handleContinue();
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [formData]);

  const fields = [
    {
      question: "What's your funding stage?",
      helper: "This helps us understand your company's maturity",
      component: (
        <MinimalSelect
          value={formData.fundingStage}
          onChange={(value) => updateField('fundingStage', value)}
          placeholder="Select stage"
          options={[
            { value: 'pre_seed', label: 'Pre-Seed', description: 'Initial funding, usually from founders or angels' },
            { value: 'seed', label: 'Seed', description: 'First institutional round' },
            { value: 'series_a', label: 'Series A', description: 'Scaling product-market fit' },
            { value: 'series_b', label: 'Series B', description: 'Scaling the business' },
            { value: 'series_c', label: 'Series C+', description: 'Expansion and growth' },
          ]}
        />
      ),
      error: errors.fundingStage
    },
    {
      question: "How much have you raised?",
      helper: "Total capital raised to date",
      component: (
        <MinimalInput
          value={formData.totalRaised}
          onChange={(value) => updateField('totalRaised', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.totalRaised
    },
    {
      question: "What's your cash position?",
      helper: "Current cash on hand",
      component: (
        <MinimalInput
          value={formData.cashOnHand}
          onChange={(value) => updateField('cashOnHand', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.cashOnHand
    },
    {
      question: "Monthly burn rate?",
      helper: "How much cash you spend per month",
      component: (
        <MinimalInput
          value={formData.monthlyBurn}
          onChange={(value) => updateField('monthlyBurn', value)}
          type="currency"
          placeholder="0"
          prefix="$"
          suffix="/month"
        />
      ),
      error: errors.monthlyBurn
    },
    {
      question: "Your last valuation?",
      helper: "Post-money valuation from your last round",
      component: (
        <MinimalInput
          value={formData.lastValuation}
          onChange={(value) => updateField('lastValuation', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.lastValuation
    },
    {
      question: "Who's your lead investor?",
      helper: "Your primary or most significant investor",
      component: (
        <MinimalSelect
          value={formData.primaryInvestor}
          onChange={(value) => updateField('primaryInvestor', value)}
          placeholder="Select investor type"
          options={[
            { value: 'none', label: 'Bootstrapped', description: 'No external investors' },
            { value: 'angel', label: 'Angel Investors', description: 'Individual investors' },
            { value: 'university', label: 'University/Research', description: 'Academic institutions' },
            { value: 'tier_3', label: 'Tier 3 VC', description: 'Emerging VC funds' },
            { value: 'tier_2', label: 'Tier 2 VC', description: 'Established regional VCs' },
            { value: 'tier_1', label: 'Tier 1 VC', description: 'Top-tier venture capital' },
          ]}
        />
      ),
      error: errors.primaryInvestor
    },
    {
      question: "Are you generating revenue?",
      component: (
        <MinimalToggle
          value={formData.hasRevenue}
          onChange={(value) => updateField('hasRevenue', value)}
          label="Yes, we have revenue"
        />
      )
    },
    ...(formData.hasRevenue ? [
      {
        question: "Monthly revenue?",
        helper: "Your average monthly recurring revenue",
        component: (
          <MinimalInput
            value={formData.monthlyRevenue}
            onChange={(value) => updateField('monthlyRevenue', value)}
            type="currency"
            placeholder="0"
            prefix="$"
            suffix="/month"
          />
        ),
        error: errors.monthlyRevenue
      }
    ] : []),
    {
      question: "Do you have any debt?",
      component: (
        <MinimalToggle
          value={formData.hasDebt}
          onChange={(value) => updateField('hasDebt', value)}
          label="Yes, we have debt"
        />
      )
    },
    ...(formData.hasDebt ? [
      {
        question: "How much debt?",
        helper: "Total outstanding debt",
        component: (
          <MinimalInput
            value={formData.debtAmount}
            onChange={(value) => updateField('debtAmount', value)}
            type="currency"
            placeholder="0"
            prefix="$"
          />
        ),
        error: errors.debtAmount
      }
    ] : [])
  ];

  return (
    <div className={styles.page}>
      <motion.nav 
        className={styles.nav}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
      >
        <button 
          className={styles.backButton}
          onClick={previousStep}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M12 4L6 10L12 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        
        <div className={styles.progress}>
          <MinimalProgress current={2} total={6} showSteps />
        </div>
        
        <AutoSaveIndicator 
          lastSaved={lastSaved}
          error={saveError}
        />
      </motion.nav>
      
      <div className={styles.content} ref={containerRef}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
        >
          <h1 className={styles.title}>Capital</h1>
          <p className={styles.subtitle}>Let's understand your financial position</p>
        </motion.div>
        
        <div className={styles.fields}>
          {fields.map((field, index) => (
            <FormField
              key={index}
              question={field.question}
              helper={field.helper}
              isActive={currentField === index}
              error={field.error}
              onActivate={() => setCurrentField(index)}
            >
              {field.component}
            </FormField>
          ))}
        </div>

        <motion.div 
          className={styles.insights}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          {formData.runway && (
            <motion.div 
              className={styles.insight}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <span className={styles.insightLabel}>Runway</span>
              <span className={styles.insightValue}>{formData.runway} months</span>
            </motion.div>
          )}
          
          {formData.burnMultiple && (
            <motion.div 
              className={styles.insight}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <span className={styles.insightLabel}>Burn Multiple</span>
              <span className={styles.insightValue}>{formData.burnMultiple}x</span>
            </motion.div>
          )}
          
          {formData.annualRevenueRunRate && Number(formData.annualRevenueRunRate) > 0 && (
            <motion.div 
              className={styles.insight}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <span className={styles.insightLabel}>ARR</span>
              <span className={styles.insightValue}>
                ${Number(formData.annualRevenueRunRate).toLocaleString()}
              </span>
            </motion.div>
          )}
        </motion.div>
        
        <motion.div 
          className={styles.actions}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <button 
            className={styles.continueButton}
            onClick={handleContinue}
          >
            Continue
            <span className={styles.shortcut}>⇧ Enter</span>
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default Capital;