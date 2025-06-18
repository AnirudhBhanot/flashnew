import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { 
  Button, 
  Icon, 
  TextField, 
  Select, 
  DatePicker 
} from '../../../design-system/components';
import { AutofillSelector } from '../../../components/AutofillSelector';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import { useFormValidation } from '../../../hooks/useFormValidation';
import { companyInfoValidation } from '../../../utils/validationRules';
import styles from './CompanyInfo.module.scss';

interface CompanyData {
  companyName: string;
  website?: string;
  industry: string;
  fundingStage: string;
  foundedDate: Date | null;
  location?: string;
  description?: string;
}

const CompanyInfo: React.FC = () => {
  const navigate = useNavigate();
  const { nextStep, updateData } = useWizard();
  const storeData = useAssessmentStore(state => state.data);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  
  // Initialize form data from store if available
  const initialData: CompanyData = {
    companyName: storeData.companyInfo?.companyName || '',
    website: storeData.companyInfo?.website || '',
    industry: storeData.companyInfo?.industry || '',
    fundingStage: storeData.companyInfo?.fundingStage || '',
    foundedDate: storeData.companyInfo?.foundedDate ? new Date(storeData.companyInfo.foundedDate) : null,
    location: storeData.companyInfo?.location || '',
    description: storeData.companyInfo?.description || '',
  };
  
  const {
    data: formData,
    errors,
    touched,
    isValid,
    updateField,
    handleSubmit,
    setData
  } = useFormValidation(initialData, companyInfoValidation, true);

  // Sync form data when store data changes (from autofill)
  useEffect(() => {
    const stored = storeData.companyInfo;
    if (stored) {
      setData({
        companyName: stored.companyName || '',
        website: stored.website || '',
        industry: stored.industry || '',
        fundingStage: stored.fundingStage || '',
        foundedDate: stored.foundedDate ? new Date(stored.foundedDate) : null,
        location: stored.location || '',
        description: stored.description || '',
      });
    }
  }, [storeData.companyInfo, setData]);

  // Auto-save data after changes
  useEffect(() => {
    const timer = setTimeout(() => {
      if (Object.keys(touched).length > 0) {
        try {
          updateData({ 
            companyInfo: {
              ...formData,
              foundedDate: formData.foundedDate?.toISOString() || '',
            } 
          });
          setLastSaved(new Date());
          setSaveError(false);
        } catch (error) {
          setSaveError(true);
        }
      }
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);

  const handleContinue = () => {
    handleSubmit(() => {
      updateData({ 
        companyInfo: {
          ...formData,
          website: formData.website || '',
          fundingStage: formData.fundingStage,
          location: formData.location || '',
          description: formData.description || '',
          foundedDate: formData.foundedDate?.toISOString() || '',
        } 
      });
      nextStep();
    });
  };

  const handleBack = () => {
    navigate('/');
  };

  const industryOptions = [
    { value: 'saas', label: 'SaaS' },
    { value: 'fintech', label: 'FinTech' },
    { value: 'healthtech', label: 'HealthTech' },
    { value: 'marketplace', label: 'Marketplace' },
    { value: 'ecommerce', label: 'E-commerce' },
    { value: 'edtech', label: 'EdTech' },
    { value: 'deeptech', label: 'DeepTech' },
    { value: 'consumer', label: 'Consumer' },
    { value: 'enterprise', label: 'Enterprise' },
    { value: 'other', label: 'Other' },
  ];

  const stageOptions = [
    { value: 'pre_seed', label: 'Pre-seed' },
    { value: 'seed', label: 'Seed' },
    { value: 'series_a', label: 'Series A' },
    { value: 'series_b', label: 'Series B' },
    { value: 'series_c', label: 'Series C+' },
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
            onClick={handleBack}
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
          <h1 className={styles.title}>Tell us about your company</h1>
          <p className={styles.subtitle}>We'll use this information to provide personalized insights</p>
          
          {/* Development only: Autofill sample data */}
          {process.env.NODE_ENV === 'development' && (
            <AutofillSelector variant="inline" />
          )}
          
          <div className={styles.form}>
            <TextField
              label="Company Name"
              placeholder="Acme Inc."
              value={formData.companyName}
              onChange={(value) => updateField('companyName', value)}
              error={touched.companyName ? errors.companyName : undefined}
              required
              autoFocus
            />
            
            <TextField
              label="Website"
              placeholder="https://example.com"
              value={formData.website || ''}
              onChange={(value) => updateField('website', value)}
              error={touched.website ? errors.website : undefined}
              helper="Optional but recommended"
            />
            
            <Select
              label="Industry"
              placeholder="Select your industry"
              value={formData.industry}
              onChange={(value) => updateField('industry', value)}
              options={industryOptions}
              error={touched.industry ? errors.industry : undefined}
              helper="Choose the industry that best describes your business"
              required
            />
            
            <Select
              label="Funding Stage"
              placeholder="Current funding stage"
              value={formData.fundingStage}
              onChange={(value) => updateField('fundingStage', value)}
              options={stageOptions}
              error={touched.fundingStage ? errors.fundingStage : undefined}
              helper="This helps us provide stage-appropriate insights"
              required
            />
            
            <DatePicker
              label="Founded"
              placeholder="When was your company founded?"
              value={formData.foundedDate}
              onChange={(date) => updateField('foundedDate', date)}
              error={touched.foundedDate ? errors.foundedDate : undefined}
              max={new Date()}
              helper="Month and year are sufficient"
              required
            />
          </div>
          
          <div className={styles.actions}>
            {!isValid && touched.companyName && (
              <p className={styles.validationHint}>
                Please fill in all required fields correctly
              </p>
            )}
            <Button 
              variant="primary" 
              size="large"
              onClick={handleContinue}
              fullWidth
              disabled={!isValid && Object.keys(touched).length > 0}
            >
              Continue
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default CompanyInfo;