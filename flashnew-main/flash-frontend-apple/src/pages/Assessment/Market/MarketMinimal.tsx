import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../../../design-system/components/AnimatePresenceWrapper';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { 
  FormField, 
  MinimalInput, 
  MinimalSelect, 
  MinimalScale,
  MinimalProgress 
} from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './MarketMinimal.module.scss';

interface MarketData {
  sector: string;
  tam: number | string;
  sam: number | string;
  som: number | string;
  marketGrowthRate: number | string;
  customerCount: number | string;
  customerConcentration: number | string;
  userGrowthRate: number | string;
  netDollarRetention: number | string;
  competitionIntensity: number;
  competitorCount: number | string;
  revenueGrowthRate: number | string;
  grossMargin: number | string;
  ltvCacRatio: number | string;
  productRetention30d: number | string;
  productRetention90d: number | string;
  dauMauRatio: number | string;
}

const Market: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const storeData = useAssessmentStore(state => state.data);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  const [currentField, setCurrentField] = useState(0);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Use store data if available, otherwise use wizard data
  const marketData = storeData.market || data.market;
  
  const [formData, setFormData] = useState<MarketData>({
    sector: marketData?.sector || '',
    tam: marketData?.tam || '',
    sam: marketData?.sam || '',
    som: marketData?.som || '',
    marketGrowthRate: marketData?.marketGrowthRate || '',
    customerCount: marketData?.customerCount || '',
    customerConcentration: marketData?.customerConcentration || '',
    userGrowthRate: marketData?.userGrowthRate || '',
    netDollarRetention: marketData?.netDollarRetention || '',
    competitionIntensity: marketData?.competitionIntensity || 3,
    competitorCount: marketData?.competitorCount || '',
    revenueGrowthRate: marketData?.revenueGrowthRate || '',
    grossMargin: marketData?.grossMargin || '',
    ltvCacRatio: marketData?.ltvCacRatio || '',
    productRetention30d: marketData?.productRetention30d || '',
    productRetention90d: marketData?.productRetention90d || '',
    dauMauRatio: marketData?.dauMauRatio || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof MarketData, string>>>({});

  // Update form when store data changes (e.g., from autofill)
  useEffect(() => {
    const marketData = storeData.market;
    if (marketData) {
      setFormData({
        sector: marketData.sector || '',
        tam: marketData.tam || '',
        sam: marketData.sam || '',
        som: marketData.som || '',
        marketGrowthRate: marketData.marketGrowthRate || '',
        customerCount: marketData.customerCount || '',
        customerConcentration: marketData.customerConcentration || '',
        userGrowthRate: marketData.userGrowthRate || '',
        netDollarRetention: marketData.netDollarRetention || '',
        competitionIntensity: marketData.competitionIntensity || 3,
        competitorCount: marketData.competitorCount || '',
        revenueGrowthRate: marketData.revenueGrowthRate || '',
        grossMargin: marketData.grossMargin || '',
        ltvCacRatio: marketData.ltvCacRatio || '',
        productRetention30d: marketData.productRetention30d || '',
        productRetention90d: marketData.productRetention90d || '',
        dauMauRatio: marketData.dauMauRatio || '',
      });
      setTouched(true);
    }
  }, [storeData.market]);

  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ market: formData });
        // Also update the store
        useAssessmentStore.getState().updateData('market', formData);
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof MarketData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof MarketData, string>> = {};
    
    if (!formData.sector) {
      newErrors.sector = 'Please select your sector';
    }
    
    if (!formData.tam || Number(formData.tam) === 0) {
      newErrors.tam = 'Total addressable market is required';
    }
    
    if (!formData.sam || Number(formData.sam) === 0) {
      newErrors.sam = 'Serviceable addressable market is required';
    }
    
    if (!formData.som || Number(formData.som) === 0) {
      newErrors.som = 'Serviceable obtainable market is required';
    }
    
    if (!formData.marketGrowthRate && formData.marketGrowthRate !== 0) {
      newErrors.marketGrowthRate = 'Market growth rate is required';
    }
    
    // Only validate customerCount if showAdvanced is true
    if (showAdvanced && (!formData.customerCount || Number(formData.customerCount) === 0)) {
      newErrors.customerCount = 'Customer count is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    console.log('Market handleContinue clicked');
    console.log('Form data:', formData);
    
    if (validate()) {
      console.log('Validation passed');
      updateData({ market: formData });
      useAssessmentStore.getState().updateData('market', formData);
      nextStep();
    } else {
      console.log('Validation failed');
      console.log('Errors:', errors);
    }
  };


  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Enter' && e.shiftKey) {
        e.preventDefault();
        handleContinue();
      }
    };
    
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [formData]);

  const coreFields = [
    {
      question: "What sector are you in?",
      helper: "Your primary industry or market",
      component: (
        <MinimalSelect
          value={formData.sector}
          onChange={(value) => updateField('sector', value)}
          placeholder="Select sector"
          options={[
            { value: 'saas', label: 'SaaS', description: 'Software as a Service' },
            { value: 'fintech', label: 'FinTech', description: 'Financial Technology' },
            { value: 'healthcare', label: 'Healthcare', description: 'Health & Medical' },
            { value: 'ecommerce', label: 'E-commerce', description: 'Online Commerce' },
            { value: 'edtech', label: 'EdTech', description: 'Education Technology' },
            { value: 'ai_ml', label: 'AI/ML', description: 'Artificial Intelligence' },
            { value: 'biotech', label: 'Biotech', description: 'Biotechnology' },
            { value: 'cleantech', label: 'CleanTech', description: 'Clean Technology' },
            { value: 'logistics', label: 'Logistics', description: 'Supply Chain & Delivery' },
            { value: 'real_estate', label: 'Real Estate', description: 'Property Tech' },
            { value: 'transportation', label: 'Transportation', description: 'Mobility Solutions' },
            { value: 'deep_tech', label: 'Deep Tech', description: 'Advanced Technology' },
            { value: 'other', label: 'Other', description: 'Not listed above' },
          ]}
        />
      ),
      error: errors.sector
    },
    {
      question: "How big is your total market?",
      helper: "Total addressable market (TAM)",
      component: (
        <MinimalInput
          value={formData.tam}
          onChange={(value) => updateField('tam', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.tam
    },
    {
      question: "What can you realistically serve?",
      helper: "Serviceable addressable market (SAM)",
      component: (
        <MinimalInput
          value={formData.sam}
          onChange={(value) => updateField('sam', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.sam
    },
    {
      question: "What can you capture?",
      helper: "Serviceable obtainable market (SOM)",
      component: (
        <MinimalInput
          value={formData.som}
          onChange={(value) => updateField('som', value)}
          type="currency"
          placeholder="0"
          prefix="$"
        />
      ),
      error: errors.som
    },
    {
      question: "How fast is your market growing?",
      helper: "Annual growth rate percentage",
      component: (
        <MinimalInput
          value={formData.marketGrowthRate}
          onChange={(value) => updateField('marketGrowthRate', value)}
          type="number"
          placeholder="20"
          suffix="%/year"
          align="center"
        />
      ),
      error: errors.marketGrowthRate
    },
    {
      question: "How many customers do you have?",
      helper: "Total number of active customers",
      component: (
        <MinimalInput
          value={formData.customerCount}
          onChange={(value) => updateField('customerCount', value)}
          type="number"
          placeholder="100"
          align="center"
        />
      ),
      error: errors.customerCount
    },
    {
      question: "How competitive is your market?",
      helper: "Rate the intensity of competition",
      component: (
        <MinimalScale
          value={formData.competitionIntensity}
          onChange={(value) => updateField('competitionIntensity', value)}
          min={1}
          max={5}
          labels={{
            1: "Blue ocean",
            3: "Competitive",
            5: "Red ocean"
          }}
        />
      )
    }
  ];

  const advancedFields = [
    {
      question: "How concentrated is your revenue?",
      helper: "Percentage of revenue from top customers",
      component: (
        <MinimalInput
          value={formData.customerConcentration}
          onChange={(value) => updateField('customerConcentration', value)}
          type="number"
          placeholder="20"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "What's your user growth rate?",
      helper: "Monthly growth percentage",
      component: (
        <MinimalInput
          value={formData.userGrowthRate}
          onChange={(value) => updateField('userGrowthRate', value)}
          type="number"
          placeholder="10"
          suffix="%/month"
          align="center"
        />
      )
    },
    {
      question: "Net dollar retention?",
      helper: "Revenue retention from existing customers",
      component: (
        <MinimalInput
          value={formData.netDollarRetention}
          onChange={(value) => updateField('netDollarRetention', value)}
          type="number"
          placeholder="110"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "How many competitors?",
      helper: "Direct competitors in your market",
      component: (
        <MinimalInput
          value={formData.competitorCount}
          onChange={(value) => updateField('competitorCount', value)}
          type="number"
          placeholder="10"
          align="center"
        />
      )
    },
    {
      question: "Revenue growth rate?",
      helper: "Annual revenue growth percentage",
      component: (
        <MinimalInput
          value={formData.revenueGrowthRate}
          onChange={(value) => updateField('revenueGrowthRate', value)}
          type="number"
          placeholder="50"
          suffix="%/year"
          align="center"
        />
      )
    },
    {
      question: "What's your gross margin?",
      helper: "Gross profit percentage",
      component: (
        <MinimalInput
          value={formData.grossMargin}
          onChange={(value) => updateField('grossMargin', value)}
          type="number"
          placeholder="75"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "LTV/CAC ratio?",
      helper: "Customer lifetime value divided by acquisition cost",
      component: (
        <MinimalInput
          value={formData.ltvCacRatio}
          onChange={(value) => updateField('ltvCacRatio', value)}
          type="number"
          placeholder="3.0"
          suffix="x"
          align="center"
        />
      )
    },
    {
      question: "30-day retention?",
      helper: "Percentage of users retained after 30 days",
      component: (
        <MinimalInput
          value={formData.productRetention30d}
          onChange={(value) => updateField('productRetention30d', value)}
          type="number"
          placeholder="40"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "90-day retention?",
      helper: "Percentage of users retained after 90 days",
      component: (
        <MinimalInput
          value={formData.productRetention90d}
          onChange={(value) => updateField('productRetention90d', value)}
          type="number"
          placeholder="25"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "DAU/MAU ratio?",
      helper: "Daily active users divided by monthly active users",
      component: (
        <MinimalInput
          value={formData.dauMauRatio}
          onChange={(value) => updateField('dauMauRatio', value)}
          type="number"
          placeholder="20"
          suffix="%"
          align="center"
        />
      )
    }
  ];

  const fields = showAdvanced ? [...coreFields, ...advancedFields] : coreFields;

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
          <MinimalProgress current={4} total={6} showSteps />
        </div>
        
        <AutoSaveIndicator 
          lastSaved={lastSaved}
          error={saveError}
        />
      </motion.nav>
      
      <div className={styles.content}>
        <motion.div
          className={styles.header}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.25, 0, 0, 1] }}
        >
          <h1 className={styles.title}>Market</h1>
          <p className={styles.subtitle}>Understanding your opportunity</p>
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

        {!showAdvanced && (
          <motion.div 
            className={styles.advancedToggle}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <button
              className={styles.advancedButton}
              onClick={() => setShowAdvanced(true)}
            >
              Add more details
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 4V16M4 10H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </motion.div>
        )}

        <AnimatePresence>
          {formData.tam && formData.sam && formData.som && (
            <motion.div 
              className={styles.marketVisual}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
            >
              <div className={styles.tamCircle}>
                <span className={styles.marketLabel}>TAM</span>
                <span className={styles.marketValue}>
                  ${Number(formData.tam).toLocaleString()}
                </span>
              </div>
              <div className={styles.samCircle}>
                <span className={styles.marketLabel}>SAM</span>
                <span className={styles.marketValue}>
                  ${Number(formData.sam).toLocaleString()}
                </span>
              </div>
              <div className={styles.somCircle}>
                <span className={styles.marketLabel}>SOM</span>
                <span className={styles.marketValue}>
                  ${Number(formData.som).toLocaleString()}
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        
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

export default Market;