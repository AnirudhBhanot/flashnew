import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  Button, 
  Icon, 
  PercentageField,
  NumberField,
  Select,
  CurrencyField
} from '../../../design-system/components';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './Product.module.scss';

interface ProductData {
  productStage: string;
  productRetention30d: number | string;
  productRetention90d: number | string;
  dauMauRatio: number | string;
  annualRevenueRunRate: number | string;
  revenueGrowthRatePercent: number | string;
  grossMarginPercent: number | string;
  ltvCacRatio: number | string;
}

const Product: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  
  const [formData, setFormData] = useState<ProductData>({
    productStage: data.product?.productStage || 'mvp',
    productRetention30d: data.product?.productRetention30d || '',
    productRetention90d: data.product?.productRetention90d || '',
    dauMauRatio: data.product?.dauMauRatio || '',
    annualRevenueRunRate: data.product?.annualRevenueRunRate || '',
    revenueGrowthRatePercent: data.product?.revenueGrowthRatePercent || '',
    grossMarginPercent: data.product?.grossMarginPercent || '',
    ltvCacRatio: data.product?.ltvCacRatio || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof ProductData, string>>>({});
  
  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ product: formData });
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof ProductData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof ProductData, string>> = {};
    
    if (!formData.productStage) {
      newErrors.productStage = 'Product stage is required';
    }
    
    if (!formData.annualRevenueRunRate && formData.annualRevenueRunRate !== 0) {
      newErrors.annualRevenueRunRate = 'ARR is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ product: formData });
      nextStep();
    }
  };

  const stageOptions = [
    { value: 'concept', label: 'Concept' },
    { value: 'prototype', label: 'Prototype' },
    { value: 'mvp', label: 'MVP' },
    { value: 'beta', label: 'Beta' },
    { value: 'launched', label: 'Launched' },
    { value: 'growth', label: 'Growth' },
    { value: 'mature', label: 'Mature' },
  ];

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
          <h1 className={styles.title}>Product & Revenue Metrics</h1>
          <p className={styles.subtitle}>Tell us about your product performance and revenue</p>
          
          <div className={styles.form}>
            <Select
              label="Product Stage"
              placeholder="Select your product stage"
              value={formData.productStage}
              onChange={(value) => updateField('productStage', value)}
              options={stageOptions}
              error={errors.productStage}
              helper="What stage is your product currently in?"
              required
            />
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Retention Metrics</h3>
              
              <PercentageField
                label="30-Day Retention"
                placeholder="70"
                value={formData.productRetention30d}
                onChange={(value) => updateField('productRetention30d', value)}
                helper="Percentage of users still active after 30 days"
              />
              
              <PercentageField
                label="90-Day Retention"
                placeholder="50"
                value={formData.productRetention90d}
                onChange={(value) => updateField('productRetention90d', value)}
                helper="Percentage of users still active after 90 days"
              />
              
              <PercentageField
                label="DAU/MAU Ratio"
                placeholder="40"
                value={formData.dauMauRatio}
                onChange={(value) => updateField('dauMauRatio', value)}
                helper="Daily Active Users ÷ Monthly Active Users"
              />
            </div>
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Revenue Metrics</h3>
              
              <CurrencyField
                label="Annual Revenue Run Rate"
                placeholder="0"
                value={formData.annualRevenueRunRate}
                onChange={(value) => updateField('annualRevenueRunRate', value)}
                error={errors.annualRevenueRunRate}
                helper="Current MRR × 12"
                required
              />
              
              <PercentageField
                label="Revenue Growth Rate"
                placeholder="100"
                value={formData.revenueGrowthRatePercent}
                onChange={(value) => updateField('revenueGrowthRatePercent', value)}
                helper="Year-over-year revenue growth percentage"
              />
              
              <PercentageField
                label="Gross Margin"
                placeholder="70"
                value={formData.grossMarginPercent}
                onChange={(value) => updateField('grossMarginPercent', value)}
                helper="(Revenue - COGS) ÷ Revenue × 100"
              />
              
              <NumberField
                label="LTV:CAC Ratio"
                placeholder="3.0"
                value={formData.ltvCacRatio}
                onChange={(value) => updateField('ltvCacRatio', value)}
                suffix=":1"
                helper="Customer Lifetime Value ÷ Customer Acquisition Cost"
                allowDecimal
                step={0.1}
              />
            </div>
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

export default Product;