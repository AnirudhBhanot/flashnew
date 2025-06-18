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
  sector: string;
  stage: string;
  foundingDate: Date | null;
  headquarters?: string;
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
    sector: storeData.companyInfo?.sector || '',
    stage: storeData.companyInfo?.stage || '',
    foundingDate: storeData.companyInfo?.foundingDate ? new Date(storeData.companyInfo.foundingDate) : null,
    headquarters: storeData.companyInfo?.headquarters || '',
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
        sector: stored.sector || '',
        stage: stored.stage || '',
        foundingDate: stored.foundingDate ? new Date(stored.foundingDate) : null,
        headquarters: stored.headquarters || '',
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
              foundingDate: formData.foundingDate?.toISOString() || '',
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
          headquarters: formData.headquarters || '',
          description: formData.description || '',
          foundingDate: formData.foundingDate?.toISOString() || '',
        } 
      });
      nextStep();
    });
  };

  const handleBack = () => {
    navigate('/');
  };

  const sectorOptions = [
    { value: 'ai-ml', label: 'AI/ML' },
    { value: 'saas', label: 'SaaS' },
    { value: 'fintech', label: 'FinTech' },
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'ecommerce', label: 'E-commerce' },
    { value: 'edtech', label: 'EdTech' },
    { value: 'logistics', label: 'Logistics' },
    { value: 'real-estate', label: 'Real Estate' },
    { value: 'transportation', label: 'Transportation' },
    { value: 'clean-tech', label: 'Clean Tech' },
    { value: 'deep-tech', label: 'Deep Tech' },
    { value: 'other', label: 'Other' },
  ];

  const stageOptions = [
    { value: 'pre-seed', label: 'Pre-Seed' },
    { value: 'seed', label: 'Seed' },
    { value: 'series-a', label: 'Series A' },
    { value: 'series-b', label: 'Series B' },
    { value: 'series-c', label: 'Series C' },
    { value: 'series-d+', label: 'Series D+' },
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
              label="Sector"
              placeholder="Select your sector"
              value={formData.sector}
              onChange={(value) => updateField('sector', value)}
              options={sectorOptions}
              error={touched.sector ? errors.sector : undefined}
              helper="Choose the sector that best describes your business"
              required
            />
            
            <Select
              label="Stage"
              placeholder="Select your funding stage"
              value={formData.stage}
              onChange={(value) => updateField('stage', value)}
              options={stageOptions}
              error={touched.stage ? errors.stage : undefined}
              helper="Your current funding stage"
              required
            />
            
            <DatePicker
              label="Founding Date"
              placeholder="When was your company founded?"
              value={formData.foundingDate}
              onChange={(date) => updateField('foundingDate', date)}
              error={touched.foundingDate ? errors.foundingDate : undefined}
              max={new Date()}
              helper="Month and year are sufficient"
              required
            />
            
            <TextField
              label="Headquarters"
              placeholder="San Francisco, CA"
              value={formData.headquarters || ''}
              onChange={(value) => updateField('headquarters', value)}
              error={touched.headquarters ? errors.headquarters : undefined}
              helper="City, State/Country"
            />
            
            <TextField
              label="Description"
              placeholder="Brief description of what your company does"
              value={formData.description || ''}
              onChange={(value) => updateField('description', value)}
              error={touched.description ? errors.description : undefined}
              helper="Optional - a short description of your business"
              multiline
              rows={3}
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

// Use the minimalist version by default
export { default } from './CompanyInfoMinimal';

// Export the original version as well if needed
export { default as CompanyInfoOriginal } from './CompanyInfoOriginal';