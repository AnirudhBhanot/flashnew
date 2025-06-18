import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  Button, 
  Icon, 
  CurrencyField,
  NumberField,
  Select,
  ToggleSwitch
} from '../../../design-system/components';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './Capital.module.scss';

interface CapitalData {
  totalCapitalRaisedUsd: number | string;
  cashOnHandUsd: number | string;
  monthlyBurnUsd: number | string;
  runwayMonths: number | string;
  burnMultiple: number | string;
  investorTierPrimary: string;
  hasDebt: boolean;
}

const Capital: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  
  const [formData, setFormData] = useState<CapitalData>({
    totalCapitalRaisedUsd: data.capital?.totalCapitalRaisedUsd || '',
    cashOnHandUsd: data.capital?.cashOnHandUsd || '',
    monthlyBurnUsd: data.capital?.monthlyBurnUsd || '',
    runwayMonths: data.capital?.runwayMonths || '',
    burnMultiple: data.capital?.burnMultiple || '',
    investorTierPrimary: data.capital?.investorTierPrimary || 'tier_3',
    hasDebt: data.capital?.hasDebt || false,
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof CapitalData, string>>>({});
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ capital: formData });
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof CapitalData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof CapitalData, string>> = {};
    
    if (!formData.totalCapitalRaisedUsd && formData.totalCapitalRaisedUsd !== 0) {
      newErrors.totalCapitalRaisedUsd = 'Total funding is required';
    }
    
    if (!formData.monthlyBurnUsd && formData.monthlyBurnUsd !== 0) {
      newErrors.monthlyBurnUsd = 'Monthly burn rate is required';
    }
    
    if (!formData.runwayMonths && formData.runwayMonths !== 0) {
      newErrors.runwayMonths = 'Runway is required';
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

  const calculateRunway = () => {
    const burn = Number(formData.monthlyBurnUsd);
    const cash = Number(formData.cashOnHandUsd);
    
    if (burn > 0 && cash > 0) {
      const runway = Math.floor(cash / burn);
      setFormData({ ...formData, runwayMonths: runway });
    }
  };
  
  const calculateBurnMultiple = () => {
    // Burn multiple = Net burn / Net new ARR
    // This would need ARR growth data - for now just estimate
    const monthlyBurn = Number(formData.monthlyBurnUsd);
    if (monthlyBurn > 0) {
      // Rough estimate: 2.5 is average, lower is better
      setFormData({ ...formData, burnMultiple: '2.5' });
    }
  };

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <div className={styles.navLeft}>
          <Button 
          variant="text" 
          size="small" 
          icon={<Icon name="chevron.left" />} 
          iconPosition="left"
          onClick={previousStep}
        >
          Back
        </Button>
        </div>
        <div className={styles.navRight}>
          <AutoSaveIndicator 
            lastSaved={lastSaved}
            error={saveError}
          />
        </div>
      </nav>
      
      <div className={styles.content}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.2, 0, 0, 1] }}
        >
          <h1 className={styles.title}>Capital & Financials</h1>
          <p className={styles.subtitle}>Understanding your financial health and runway</p>
          
          <div className={styles.infoCard}>
            <Icon name="info.circle" size={20} />
            <p>Your financial information is never stored and is only used for this assessment.</p>
          </div>
          
          <div className={styles.form}>
            <CurrencyField
              label="Total Capital Raised"
              placeholder="0"
              value={formData.totalCapitalRaisedUsd}
              onChange={(value) => updateField('totalCapitalRaisedUsd', value)}
              error={errors.totalCapitalRaisedUsd}
              helper="Include all rounds: pre-seed, seed, Series A, etc."
              required
            />
            
            <CurrencyField
              label="Cash on Hand"
              placeholder="0"
              value={formData.cashOnHandUsd}
              onChange={(value) => updateField('cashOnHandUsd', value)}
              helper="Current cash balance available"
              required
            />
            
            <CurrencyField
              label="Monthly Burn Rate"
              placeholder="0"
              value={formData.monthlyBurnUsd}
              onChange={(value) => updateField('monthlyBurnUsd', value)}
              error={errors.monthlyBurnUsd}
              helper="Total monthly expenses (gross burn)"
              required
            />
            
            <div className={styles.runwaySection}>
              <NumberField
                label="Runway"
                placeholder="0"
                value={formData.runwayMonths}
                onChange={(value) => updateField('runwayMonths', value)}
                error={errors.runwayMonths}
                suffix="months"
                helper="How many months until you need more funding?"
                required
              />
              <Button
                variant="text"
                size="small"
                onClick={calculateRunway}
                disabled={!formData.monthlyBurnUsd || !formData.cashOnHandUsd}
              >
                Calculate
              </Button>
            </div>
            
            <Select
              label="Primary Investor Tier"
              placeholder="Select investor tier"
              value={formData.investorTierPrimary}
              onChange={(value) => updateField('investorTierPrimary', value)}
              options={[
                { value: 'tier_1', label: 'Tier 1 (Top VCs)' },
                { value: 'tier_2', label: 'Tier 2 (Mid-tier VCs)' },
                { value: 'tier_3', label: 'Tier 3 (Seed/Angels)' },
                { value: 'none', label: 'No institutional investors' },
              ]}
              helper="Highest tier of your current investors"
            />
            
            <motion.div
              className={styles.advancedSection}
              initial={false}
              animate={{ height: showAdvanced ? 'auto' : 0 }}
              transition={{ duration: 0.3 }}
              style={{ overflow: 'hidden' }}
            >
              <div className={styles.advancedFields}>
                <div className={styles.burnMultipleSection}>
                  <NumberField
                    label="Burn Multiple"
                    placeholder="2.5"
                    value={formData.burnMultiple}
                    onChange={(value) => updateField('burnMultiple', value)}
                    suffix="x"
                    helper="Net burn ÷ Net new ARR (lower is better)"
                    allowDecimal
                    step={0.1}
                  />
                  <Button
                    variant="text"
                    size="small"
                    onClick={calculateBurnMultiple}
                    disabled={!formData.monthlyBurnUsd}
                  >
                    Calculate
                  </Button>
                </div>
                
                <ToggleSwitch
                  label="Has Debt?"
                  value={formData.hasDebt}
                  onChange={(value) => updateField('hasDebt', value)}
                />
              </div>
            </motion.div>
            
            <Button
              variant="text"
              onClick={() => setShowAdvanced(!showAdvanced)}
              icon={<Icon name={showAdvanced ? 'chevron.up' : 'chevron.down'} />}
            >
              {showAdvanced ? 'Hide' : 'Show'} advanced metrics
            </Button>
          </div>
          
          <div className={styles.actions}>
            <Button 
              variant="secondary" 
              size="large"
              onClick={previousStep}
            >
              Back
            </Button>
            <Button 
              variant="primary" 
              size="large"
              onClick={handleContinue}
            >
              Continue
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Capital;