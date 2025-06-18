import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  Button, 
  Icon, 
  ScaleSelector,
  CurrencyField,
  Select,
  PercentageField,
  NumberField
} from '../../../design-system/components';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './Market.module.scss';

interface MarketData {
  sector: string;
  tamSizeUsd: number | string;
  samSizeUsd: number | string;
  somSizeUsd: number | string;
  marketGrowthRatePercent: number | string;
  customerCount: number | string;
  customerConcentrationPercent: number | string;
  userGrowthRatePercent: number | string;
  netDollarRetentionPercent: number | string;
  competitionIntensity: string;
  competitorsNamedCount: number | string;
}

const Market: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  
  const [formData, setFormData] = useState<MarketData>({
    sector: data.market?.sector || 'saas',
    tamSizeUsd: data.market?.tamSizeUsd || '',
    samSizeUsd: data.market?.samSizeUsd || '',
    somSizeUsd: data.market?.somSizeUsd || '',
    marketGrowthRatePercent: data.market?.marketGrowthRatePercent || '',
    customerCount: data.market?.customerCount || '',
    customerConcentrationPercent: data.market?.customerConcentrationPercent || '',
    userGrowthRatePercent: data.market?.userGrowthRatePercent || '',
    netDollarRetentionPercent: data.market?.netDollarRetentionPercent || '',
    competitionIntensity: data.market?.competitionIntensity || 'medium',
    competitorsNamedCount: data.market?.competitorsNamedCount || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof MarketData, string>>>({});
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ market: formData });
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof MarketData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  // Auto-calculate SAM and SOM from TAM
  const calculateMarketSizes = () => {
    const tam = Number(formData.tamSizeUsd);
    if (tam > 0) {
      const sam = tam * 0.1; // 10% of TAM
      const som = tam * 0.01; // 1% of TAM
      setFormData({
        ...formData,
        samSizeUsd: Math.round(sam).toString(),
        somSizeUsd: Math.round(som).toString()
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof MarketData, string>> = {};
    
    if (!formData.tamSizeUsd || Number(formData.tamSizeUsd) === 0) {
      newErrors.tamSizeUsd = 'Total addressable market is required';
    }
    
    if (!formData.marketGrowthRatePercent) {
      newErrors.marketGrowthRatePercent = 'Market growth rate is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ market: formData });
      nextStep();
    }
  };

  const sectorOptions = [
    { value: 'saas', label: 'SaaS' },
    { value: 'fintech', label: 'FinTech' },
    { value: 'healthtech', label: 'HealthTech' },
    { value: 'edtech', label: 'EdTech' },
    { value: 'ecommerce', label: 'E-commerce' },
    { value: 'marketplace', label: 'Marketplace' },
    { value: 'deeptech', label: 'DeepTech' },
    { value: 'consumer', label: 'Consumer' },
    { value: 'enterprise', label: 'Enterprise' },
    { value: 'proptech', label: 'PropTech' },
    { value: 'biotech', label: 'BioTech' },
    { value: 'agtech', label: 'AgTech' },
    { value: 'cleantech', label: 'CleanTech' },
    { value: 'cybersecurity', label: 'Cybersecurity' },
    { value: 'gaming', label: 'Gaming' },
    { value: 'logistics', label: 'Logistics' },
    { value: 'insurtech', label: 'InsurTech' },
    { value: 'legaltech', label: 'LegalTech' },
    { value: 'hrtech', label: 'HRTech' },
    { value: 'other', label: 'Other' },
  ];

  const competitionOptions = [
    { value: 'low', label: 'Low (Few competitors)' },
    { value: 'medium', label: 'Medium (Some competition)' },
    { value: 'high', label: 'High (Many competitors)' },
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
          <h1 className={styles.title}>Market Opportunity</h1>
          <p className={styles.subtitle}>Help us understand your market size and dynamics</p>
          
          <div className={styles.form}>
            <Select
              label="Sector"
              placeholder="Select your primary sector"
              value={formData.sector}
              onChange={(value) => updateField('sector', value)}
              options={sectorOptions}
              helper="Choose the sector that best describes your business"
              required
            />
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Market Size</h3>
              
              <div className={styles.marketSizeFields}>
                <CurrencyField
                  label="Total Addressable Market (TAM)"
                  placeholder="0"
                  value={formData.tamSizeUsd}
                  onChange={(value) => updateField('tamSizeUsd', value)}
                  error={errors.tamSizeUsd}
                  helper="Total market demand for your product/service"
                  required
                />
                <Button
                  variant="text"
                  size="small"
                  onClick={calculateMarketSizes}
                  disabled={!formData.tamSizeUsd}
                >
                  Calculate SAM/SOM
                </Button>
              </div>
              
              <CurrencyField
                label="Serviceable Addressable Market (SAM)"
                placeholder="0"
                value={formData.samSizeUsd}
                onChange={(value) => updateField('samSizeUsd', value)}
                helper="The portion of TAM you can realistically serve"
              />
              
              <CurrencyField
                label="Serviceable Obtainable Market (SOM)"
                placeholder="0"
                value={formData.somSizeUsd}
                onChange={(value) => updateField('somSizeUsd', value)}
                helper="The portion of SAM you can realistically capture"
              />
            </div>
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Market Dynamics</h3>
              
              <PercentageField
                label="Market Growth Rate"
                placeholder="20"
                value={formData.marketGrowthRatePercent}
                onChange={(value) => updateField('marketGrowthRatePercent', value)}
                error={errors.marketGrowthRatePercent}
                helper="Annual growth rate of your target market"
                required
              />
              
              <Select
                label="Competition Intensity"
                placeholder="Select competition level"
                value={formData.competitionIntensity}
                onChange={(value) => updateField('competitionIntensity', value)}
                options={competitionOptions}
                helper="How competitive is your market?"
              />
              
              <NumberField
                label="Named Competitors"
                placeholder="5"
                value={formData.competitorsNamedCount}
                onChange={(value) => updateField('competitorsNamedCount', value)}
                min={0}
                helper="Number of direct competitors you can name"
              />
            </div>
            
            <motion.div
              className={styles.advancedSection}
              initial={false}
              animate={{ height: showAdvanced ? 'auto' : 0 }}
              transition={{ duration: 0.3 }}
              style={{ overflow: 'hidden' }}
            >
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Customer Metrics</h3>
                
                <NumberField
                  label="Customer Count"
                  placeholder="100"
                  value={formData.customerCount}
                  onChange={(value) => updateField('customerCount', value)}
                  min={0}
                  helper="Current number of paying customers"
                />
                
                <PercentageField
                  label="Customer Concentration"
                  placeholder="20"
                  value={formData.customerConcentrationPercent}
                  onChange={(value) => updateField('customerConcentrationPercent', value)}
                  helper="% of revenue from top 10% of customers"
                />
                
                <PercentageField
                  label="User Growth Rate"
                  placeholder="10"
                  value={formData.userGrowthRatePercent}
                  onChange={(value) => updateField('userGrowthRatePercent', value)}
                  helper="Monthly user growth percentage"
                />
                
                <PercentageField
                  label="Net Dollar Retention"
                  placeholder="110"
                  value={formData.netDollarRetentionPercent}
                  onChange={(value) => updateField('netDollarRetentionPercent', value)}
                  helper="Revenue retained + expansion from existing customers"
                />
              </div>
            </motion.div>
            
            <Button
              variant="text"
              onClick={() => setShowAdvanced(!showAdvanced)}
              icon={<Icon name={showAdvanced ? 'chevron.up' : 'chevron.down'} />}
            >
              {showAdvanced ? 'Hide' : 'Show'} customer metrics
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

export default Market;