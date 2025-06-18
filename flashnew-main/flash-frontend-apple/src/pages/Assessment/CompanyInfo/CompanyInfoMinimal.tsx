import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { 
  FormField, 
  MinimalInput, 
  MinimalSelect,
  MinimalProgress,
  MinimalDateSelect,
  MinimalLocationSelect
} from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import { AutofillSelector } from '../../../components/AutofillSelector';
import styles from './CompanyInfoMinimal.module.scss';

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
  const [touched, setTouched] = useState(false);
  const [currentField, setCurrentField] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Initialize form data from store if available
  const [formData, setFormData] = useState<CompanyData>({
    companyName: storeData.companyInfo?.companyName || '',
    website: storeData.companyInfo?.website || '',
    sector: storeData.companyInfo?.sector || '',
    stage: storeData.companyInfo?.stage || '',
    foundingDate: storeData.companyInfo?.foundingDate ? new Date(storeData.companyInfo.foundingDate) : null,
    headquarters: storeData.companyInfo?.headquarters || '',
    description: storeData.companyInfo?.description || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof CompanyData, string>>>({});

  // Sync with store data when it changes (e.g., from autofill)
  useEffect(() => {
    if (storeData.companyInfo) {
      setFormData({
        companyName: storeData.companyInfo.companyName || '',
        website: storeData.companyInfo.website || '',
        sector: storeData.companyInfo.sector || '',
        stage: storeData.companyInfo.stage || '',
        foundingDate: storeData.companyInfo.foundingDate ? new Date(storeData.companyInfo.foundingDate) : null,
        headquarters: storeData.companyInfo.headquarters || '',
        description: storeData.companyInfo.description || '',
      });
      setTouched(true);
    }
  }, [storeData.companyInfo]);

  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
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
    }, 1000);

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);

  const updateField = (field: keyof CompanyData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof CompanyData, string>> = {};
    
    if (!formData.companyName) {
      newErrors.companyName = 'Company name is required';
    }
    
    if (!formData.sector) {
      newErrors.sector = 'Please select your sector';
    }
    
    if (!formData.stage) {
      newErrors.stage = 'Please select your funding stage';
    }
    
    if (!formData.foundingDate) {
      newErrors.foundingDate = 'Founding date is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
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
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' && e.shiftKey) {
      e.preventDefault();
      handleContinue();
    }
  };

  const sectorOptions = [
    { value: 'ai-ml', label: 'AI/ML', description: 'Artificial Intelligence & Machine Learning' },
    { value: 'saas', label: 'SaaS', description: 'Software as a Service' },
    { value: 'fintech', label: 'FinTech', description: 'Financial Technology' },
    { value: 'healthcare', label: 'Healthcare', description: 'Health & Medical Technology' },
    { value: 'ecommerce', label: 'E-commerce', description: 'Online Commerce & Marketplaces' },
    { value: 'edtech', label: 'EdTech', description: 'Education Technology' },
    { value: 'logistics', label: 'Logistics', description: 'Supply Chain & Transportation' },
    { value: 'real-estate', label: 'Real Estate', description: 'PropTech & Real Estate' },
    { value: 'clean-tech', label: 'Clean Tech', description: 'Sustainability & Environment' },
    { value: 'deep-tech', label: 'Deep Tech', description: 'Advanced Technology Research' },
    { value: 'other', label: 'Other', description: 'Other Industries' },
  ];

  const stageOptions = [
    { value: 'pre-seed', label: 'Pre-Seed', description: 'Initial founding stage' },
    { value: 'seed', label: 'Seed', description: 'Early funding round' },
    { value: 'series-a', label: 'Series A', description: 'First significant round' },
    { value: 'series-b', label: 'Series B', description: 'Growth stage funding' },
    { value: 'series-c', label: 'Series C', description: 'Expansion funding' },
    { value: 'series-d+', label: 'Series D+', description: 'Late stage funding' },
  ];

  const fields = [
    {
      question: "What's your company name?",
      component: (
        <MinimalInput
          value={formData.companyName}
          onChange={(value) => updateField('companyName', value)}
          placeholder="Acme Inc."
          autoFocus
        />
      ),
      error: errors.companyName
    },
    {
      question: "Your website?",
      helper: "Optional but helps us understand your business",
      component: (
        <MinimalInput
          value={formData.website || ''}
          onChange={(value) => updateField('website', value)}
          placeholder="https://example.com"
          type="url"
        />
      ),
      error: errors.website
    },
    {
      question: "Which sector are you in?",
      component: (
        <MinimalSelect
          value={formData.sector}
          onChange={(value) => updateField('sector', value)}
          placeholder="Select sector"
          options={sectorOptions}
        />
      ),
      error: errors.sector
    },
    {
      question: "What's your funding stage?",
      component: (
        <MinimalSelect
          value={formData.stage}
          onChange={(value) => updateField('stage', value)}
          placeholder="Select stage"
          options={stageOptions}
        />
      ),
      error: errors.stage
    },
    {
      question: "When were you founded?",
      helper: "Month and year",
      component: (
        <MinimalDateSelect
          value={formData.foundingDate}
          onChange={(date) => updateField('foundingDate', date)}
          placeholder="Select month and year"
        />
      ),
      error: errors.foundingDate
    },
    {
      question: "Where are you headquartered?",
      helper: "Optional",
      component: (
        <MinimalLocationSelect
          value={formData.headquarters || ''}
          onChange={(value) => updateField('headquarters', value)}
          placeholder="Select location"
        />
      ),
      error: errors.headquarters
    }
  ];

  return (
    <div className={styles.page} onKeyDown={handleKeyDown}>
      <motion.nav 
        className={styles.nav}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
      >
        <button 
          className={styles.backButton}
          onClick={handleBack}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M12 4L6 10L12 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        
        <div className={styles.progress}>
          <MinimalProgress current={1} total={6} showSteps />
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
          <h1 className={styles.title}>Company</h1>
          <p className={styles.subtitle}>Let's start with the basics</p>
        </motion.div>
        
        {/* Development mode: Show autofill selector */}
        {process.env.NODE_ENV === 'development' && (
          <div style={{ marginBottom: '2rem' }}>
            <AutofillSelector 
              variant="inline"
              onSelect={() => {
                // Refresh form data after autofill
                const storeData = useAssessmentStore.getState().data;
                if (storeData.companyInfo) {
                  setFormData({
                    companyName: storeData.companyInfo.companyName || '',
                    website: storeData.companyInfo.website || '',
                    sector: storeData.companyInfo.sector || '',
                    stage: storeData.companyInfo.stage || '',
                    foundingDate: storeData.companyInfo.foundingDate ? new Date(storeData.companyInfo.foundingDate) : null,
                    headquarters: storeData.companyInfo.headquarters || '',
                    description: storeData.companyInfo.description || '',
                  });
                  setTouched(true);
                }
              }}
            />
          </div>
        )}
        
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

export default CompanyInfo;