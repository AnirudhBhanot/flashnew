import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../../../design-system/components/AnimatePresenceWrapper';
import { useWizard } from '../../../features/wizard/WizardProvider';
import useAssessmentStore from '../../../store/assessmentStore';
import { 
  FormField, 
  MinimalInput, 
  MinimalSelect, 
  MinimalToggle,
  MinimalScale,
  MinimalProgress 
} from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './AdvantageMinimal.module.scss';

interface AdvantageData {
  patentCount: number | string;
  networkEffects: boolean;
  hasDataMoat: boolean;
  regulatoryAdvantage: boolean;
  techDifferentiation: number;
  switchingCosts: number;
  brandStrength: number;
  scalability: number;
  productStage: string;
  uniqueAdvantage: string;
}

const Advantage: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const storeData = useAssessmentStore(state => state.data);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  const [currentField, setCurrentField] = useState(0);
  const [showTextarea, setShowTextarea] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  // Use store data if available, otherwise use wizard data
  const advantageData = storeData.advantage || data.advantage;
  
  const [formData, setFormData] = useState<AdvantageData>({
    patentCount: advantageData?.patentCount || 0,
    networkEffects: advantageData?.networkEffects || false,
    hasDataMoat: advantageData?.hasDataMoat || false,
    regulatoryAdvantage: advantageData?.regulatoryAdvantage || false,
    techDifferentiation: advantageData?.techDifferentiation || 3,
    switchingCosts: advantageData?.switchingCosts || 3,
    brandStrength: advantageData?.brandStrength || 3,
    scalability: advantageData?.scalability || 3,
    productStage: advantageData?.productStage || '',
    uniqueAdvantage: advantageData?.uniqueAdvantage || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof AdvantageData, string>>>({});

  // Update form when store data changes (e.g., from autofill)
  useEffect(() => {
    const advantageData = storeData.advantage;
    if (advantageData) {
      setFormData({
        patentCount: advantageData.patentCount || 0,
        networkEffects: advantageData.networkEffects || false,
        hasDataMoat: advantageData.hasDataMoat || false,
        regulatoryAdvantage: advantageData.regulatoryAdvantage || false,
        techDifferentiation: advantageData.techDifferentiation || 3,
        switchingCosts: advantageData.switchingCosts || 3,
        brandStrength: advantageData.brandStrength || 3,
        scalability: advantageData.scalability || 3,
        productStage: advantageData.productStage || '',
        uniqueAdvantage: advantageData.uniqueAdvantage || '',
      });
      setTouched(true);
    }
  }, [storeData.advantage]);

  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ advantage: formData });
        // Also update the store
        useAssessmentStore.getState().updateData('advantage', formData);
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof AdvantageData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof AdvantageData, string>> = {};
    
    if (!formData.productStage) {
      newErrors.productStage = 'Please select your product stage';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ advantage: formData });
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
      question: "What stage is your product in?",
      helper: "This helps us understand your product maturity",
      component: (
        <MinimalSelect
          value={formData.productStage}
          onChange={(value) => updateField('productStage', value)}
          placeholder="Select stage"
          options={[
            { value: 'idea', label: 'Idea Stage', description: 'Concept and planning phase' },
            { value: 'prototype', label: 'Prototype', description: 'Working proof of concept' },
            { value: 'mvp', label: 'MVP', description: 'Minimum viable product' },
            { value: 'beta', label: 'Beta', description: 'Testing with early users' },
            { value: 'launched', label: 'Launched', description: 'Available to customers' },
            { value: 'scaling', label: 'Scaling', description: 'Growing customer base' },
          ]}
        />
      ),
      error: errors.productStage
    },
    {
      question: "What makes you different?",
      helper: "Describe your unique advantage in your own words",
      component: (
        <div className={styles.textareaWrapper}>
          <button 
            className={styles.textareaTrigger}
            onClick={() => setShowTextarea(true)}
          >
            {formData.uniqueAdvantage || 'Tell your story...'}
          </button>
          <AnimatePresence>
            {showTextarea && (
              <motion.div
                className={styles.textareaOverlay}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setShowTextarea(false)}
              >
                <motion.div
                  className={styles.textareaModal}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.9, opacity: 0 }}
                  onClick={(e) => e.stopPropagation()}
                >
                  <textarea
                    ref={textareaRef}
                    className={styles.textarea}
                    value={formData.uniqueAdvantage}
                    onChange={(e) => updateField('uniqueAdvantage', e.target.value)}
                    placeholder="What makes your solution unique? What's your secret sauce?"
                    autoFocus
                  />
                  <button 
                    className={styles.textareaDone}
                    onClick={() => setShowTextarea(false)}
                  >
                    Done
                  </button>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )
    },
    {
      question: "How many patents do you have?",
      helper: "Filed or granted patents",
      component: (
        <MinimalInput
          value={formData.patentCount}
          onChange={(value) => updateField('patentCount', value)}
          type="number"
          placeholder="0"
          align="center"
        />
      )
    },
    {
      question: "What competitive moats do you have?",
      helper: "Select all that apply to your business",
      component: (
        <div className={styles.moats}>
          <MinimalToggle
            value={formData.networkEffects}
            onChange={(value) => updateField('networkEffects', value)}
            label="Network effects"
          />
          <MinimalToggle
            value={formData.hasDataMoat}
            onChange={(value) => updateField('hasDataMoat', value)}
            label="Proprietary data"
          />
          <MinimalToggle
            value={formData.regulatoryAdvantage}
            onChange={(value) => updateField('regulatoryAdvantage', value)}
            label="Regulatory advantage"
          />
        </div>
      )
    },
    {
      question: "How strong is your brand?",
      helper: "Rate your brand recognition and reputation",
      component: (
        <MinimalScale
          value={formData.brandStrength}
          onChange={(value) => updateField('brandStrength', value)}
          min={1}
          max={5}
          labels={{
            1: "Unknown",
            3: "Recognized",
            5: "Iconic"
          }}
        />
      )
    },
    {
      question: "How scalable is your business?",
      helper: "Can you grow without proportional cost increases?",
      component: (
        <MinimalScale
          value={formData.scalability}
          onChange={(value) => updateField('scalability', value)}
          min={1}
          max={5}
          labels={{
            1: "Linear",
            3: "Moderate",
            5: "Exponential"
          }}
        />
      )
    },
    {
      question: "How hard is it for customers to switch?",
      helper: "Rate the switching costs for your customers",
      component: (
        <MinimalScale
          value={formData.switchingCosts}
          onChange={(value) => updateField('switchingCosts', value)}
          min={1}
          max={5}
          labels={{
            1: "Easy",
            3: "Moderate",
            5: "Very hard"
          }}
        />
      )
    },
    {
      question: "How differentiated is your technology?",
      helper: "Rate your technical innovation",
      component: (
        <MinimalScale
          value={formData.techDifferentiation}
          onChange={(value) => updateField('techDifferentiation', value)}
          min={1}
          max={5}
          labels={{
            1: "Common",
            3: "Unique",
            5: "Breakthrough"
          }}
        />
      )
    }
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
          <MinimalProgress current={3} total={6} showSteps />
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
          <h1 className={styles.title}>Advantage</h1>
          <p className={styles.subtitle}>What makes you special?</p>
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
          className={styles.moatSummary}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <span className={styles.moatCount}>
            {[
              formData.networkEffects,
              formData.hasDataMoat,
              formData.regulatoryAdvantage,
              Number(formData.patentCount) > 0
            ].filter(Boolean).length}
          </span>
          <span className={styles.moatLabel}>Competitive moats</span>
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

export default Advantage;