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
import styles from './MarketSimple.module.scss';

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
    setFormData(prev => ({ ...prev, [field]: value }));
    setTouched(true);
  };

  // Calculate auto-populated values
  useEffect(() => {
    // Auto-calculate SAM from TAM
    const cleanedTam = String(formData.tam).replace(/[^0-9]/g, '');
    const tamValue = Number(cleanedTam) || 0;
    if (tamValue > 0) {
      const calculatedSam = Math.round(tamValue * 0.1); // 10% of TAM
      setFormData(prev => ({ ...prev, sam: calculatedSam.toString() }));
    } else {
      setFormData(prev => ({ ...prev, sam: '' }));
    }
  }, [formData.tam]);

  useEffect(() => {
    // Auto-calculate SOM from SAM
    const cleanedSam = String(formData.sam).replace(/[^0-9]/g, '');
    const samValue = Number(cleanedSam) || 0;
    if (samValue > 0) {
      const calculatedSom = Math.round(samValue * 0.01); // 1% of SAM
      setFormData(prev => ({ ...prev, som: calculatedSom.toString() }));
    } else {
      setFormData(prev => ({ ...prev, som: '' }));
    }
  }, [formData.sam]);

  const validate = (): boolean => {
    return formData.sector !== '' && 
           formData.tam !== '' && 
           formData.marketGrowthRate !== '';
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ market: formData });
      useAssessmentStore.getState().updateData('market', formData);
      nextStep();
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

  // Format market value for display
  const formatMarketValue = (value: number | string): string => {
    // Remove any non-numeric characters (like commas) before parsing
    const cleanedValue = String(value).replace(/[^0-9]/g, '');
    const num = Number(cleanedValue);
    if (isNaN(num) || num === 0) return '$0';
    
    if (num >= 1e9) {
      return `$${(num / 1e9).toFixed(1)}B`;
    } else if (num >= 1e6) {
      return `$${(num / 1e6).toFixed(1)}M`;
    } else if (num >= 1e3) {
      return `$${(num / 1e3).toFixed(0)}K`;
    }
    return `$${num.toLocaleString()}`;
  };

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
          <FormField
            question="What sector are you in?"
            helper="Your primary industry or market"
            isActive={currentField === 0}
            onActivate={() => setCurrentField(0)}
          >
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
          </FormField>
          
          <FormField
            question="How big is your total market?"
            helper="Total addressable market (TAM)"
            isActive={currentField === 1}
            onActivate={() => setCurrentField(1)}
          >
            <MinimalInput
              value={formData.tam}
              onChange={(value) => updateField('tam', value)}
              type="currency"
              placeholder="0"
              prefix="$"
            />
          </FormField>
          
          <FormField
            question="How fast is your market growing?"
            helper="Annual growth rate percentage"
            isActive={currentField === 2}
            onActivate={() => setCurrentField(2)}
          >
            <MinimalInput
              value={formData.marketGrowthRate}
              onChange={(value) => updateField('marketGrowthRate', value)}
              type="number"
              placeholder="20"
              suffix="%/year"
              align="center"
            />
          </FormField>
          
          <FormField
            question="How many customers do you have?"
            helper="Total number of active customers"
            isActive={currentField === 3}
            onActivate={() => setCurrentField(3)}
          >
            <MinimalInput
              value={formData.customerCount}
              onChange={(value) => updateField('customerCount', value)}
              type="number"
              placeholder="0"
              align="center"
            />
          </FormField>
          
          <FormField
            question="How competitive is your market?"
            helper="Rate the intensity of competition"
            isActive={currentField === 4}
            onActivate={() => setCurrentField(4)}
          >
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
          </FormField>
          
          <FormField
            question="How many direct competitors?"
            helper="Named competitors in your market"
            isActive={currentField === 5}
            onActivate={() => setCurrentField(5)}
          >
            <MinimalInput
              value={formData.competitorCount}
              onChange={(value) => updateField('competitorCount', value)}
              type="number"
              placeholder="5"
              align="center"
            />
          </FormField>
          
          <FormField
              question="What % of revenue from top customers?"
              helper="Customer concentration percentage"
              isActive={currentField === 6}
              onActivate={() => setCurrentField(6)}
            >
              <MinimalInput
                value={formData.customerConcentration}
                onChange={(value) => updateField('customerConcentration', value)}
                type="number"
                placeholder="20"
                suffix="%"
                align="center"
              />
            </FormField>
            
            <FormField
              question="Monthly user growth rate?"
              helper="Percentage growth per month"
              isActive={currentField === 7}
              onActivate={() => setCurrentField(7)}
            >
              <MinimalInput
                value={formData.userGrowthRate}
                onChange={(value) => updateField('userGrowthRate', value)}
                type="number"
                placeholder="10"
                suffix="%/month"
                align="center"
              />
            </FormField>
            
            <FormField
              question="Net dollar retention?"
              helper="Revenue retention from existing customers"
              isActive={currentField === 8}
              onActivate={() => setCurrentField(8)}
            >
              <MinimalInput
                value={formData.netDollarRetention}
                onChange={(value) => updateField('netDollarRetention', value)}
                type="number"
                placeholder="110"
                suffix="%"
                align="center"
              />
            </FormField>
            
            <FormField
              question="What's your revenue growth rate?"
              helper="Year-over-year revenue growth"
              isActive={currentField === 9}
              onActivate={() => setCurrentField(9)}
            >
              <MinimalInput
                value={formData.revenueGrowthRate}
                onChange={(value) => updateField('revenueGrowthRate', value)}
                type="number"
                placeholder="100"
                suffix="%/year"
                align="center"
              />
            </FormField>
            
            <FormField
              question="What's your gross margin?"
              helper="Revenue minus cost of goods sold"
              isActive={currentField === 10}
              onActivate={() => setCurrentField(10)}
            >
              <MinimalInput
                value={formData.grossMargin}
                onChange={(value) => updateField('grossMargin', value)}
                type="number"
                placeholder="70"
                suffix="%"
                align="center"
              />
            </FormField>
            
            <FormField
              question="What's your LTV/CAC ratio?"
              helper="Customer lifetime value vs acquisition cost"
              isActive={currentField === 11}
              onActivate={() => setCurrentField(11)}
            >
              <MinimalInput
                value={formData.ltvCacRatio}
                onChange={(value) => updateField('ltvCacRatio', value)}
                type="number"
                placeholder="3"
                suffix="x"
                align="center"
              />
            </FormField>
            
            <FormField
              question="30-day product retention?"
              helper="Users active after 30 days"
              isActive={currentField === 12}
              onActivate={() => setCurrentField(12)}
            >
              <MinimalInput
                value={formData.productRetention30d}
                onChange={(value) => updateField('productRetention30d', value)}
                type="number"
                placeholder="50"
                suffix="%"
                align="center"
              />
            </FormField>
            
            <FormField
              question="90-day product retention?"
              helper="Users active after 90 days"
              isActive={currentField === 13}
              onActivate={() => setCurrentField(13)}
            >
              <MinimalInput
                value={formData.productRetention90d}
                onChange={(value) => updateField('productRetention90d', value)}
                type="number"
                placeholder="30"
                suffix="%"
                align="center"
              />
            </FormField>
            
            <FormField
              question="DAU/MAU ratio?"
              helper="Daily active users / Monthly active users"
              isActive={currentField === 14}
              onActivate={() => setCurrentField(14)}
            >
              <MinimalInput
                value={formData.dauMauRatio}
                onChange={(value) => updateField('dauMauRatio', value)}
                type="number"
                placeholder="20"
                suffix="%"
                align="center"
              />
            </FormField>
        </div>

        <motion.div 
          className={styles.marketSummary}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <div className={styles.marketBreakdown}>
            <div className={styles.marketItem}>
              <span className={styles.marketLabel}>TAM</span>
              <span className={styles.marketValue}>
                {formatMarketValue(formData.tam || 0)}
              </span>
            </div>
            <div className={styles.marketArrow}>→</div>
            <div className={styles.marketItem}>
              <span className={styles.marketLabel}>SAM (10%)</span>
              <span className={styles.marketValue}>
                {formatMarketValue(formData.sam || 0)}
              </span>
            </div>
            <div className={styles.marketArrow}>→</div>
            <div className={styles.marketItem}>
              <span className={styles.marketLabel}>SOM (1%)</span>
              <span className={styles.marketValue}>
                {formatMarketValue(formData.som || 0)}
              </span>
            </div>
          </div>
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
            disabled={!validate()}
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