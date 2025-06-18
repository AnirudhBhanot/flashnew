import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  Button, 
  Icon, 
  ScaleSelector,
  NumberField,
  ToggleSwitch
} from '../../../design-system/components';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './Advantage.module.scss';

interface AdvantageData {
  patentCount: number | string;
  networkEffectsPresent: boolean;
  hasDataMoat: boolean;
  regulatoryAdvantagePresent: boolean;
  techDifferentiationScore: number;
  switchingCostScore: number;
  brandStrengthScore: number;
  scalabilityScore: number;
}

const Advantage: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  
  const [formData, setFormData] = useState<AdvantageData>({
    patentCount: data.advantage?.patentCount || '0',
    networkEffectsPresent: data.advantage?.networkEffectsPresent || false,
    hasDataMoat: data.advantage?.hasDataMoat || false,
    regulatoryAdvantagePresent: data.advantage?.regulatoryAdvantagePresent || false,
    techDifferentiationScore: data.advantage?.techDifferentiationScore || 3,
    switchingCostScore: data.advantage?.switchingCostScore || 3,
    brandStrengthScore: data.advantage?.brandStrengthScore || 3,
    scalabilityScore: data.advantage?.scalabilityScore || 3,
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof AdvantageData, string>>>({});
  
  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ advantage: formData });
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof AdvantageData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  // Helper to get label for score
  const getScoreLabel = (score: number) => {
    if (score <= 1) return 'Very Weak';
    if (score <= 2) return 'Weak';
    if (score <= 3) return 'Moderate';
    if (score <= 4) return 'Strong';
    return 'Very Strong';
  };

  const validate = (): boolean => {
    // All fields have defaults, so validation is minimal
    return true;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ advantage: formData });
      nextStep();
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
          <h1 className={styles.title}>Competitive Advantage</h1>
          <p className={styles.subtitle}>What makes your startup unique and defensible?</p>
          
          <div className={styles.form}>
            <NumberField
              label="Patent Count"
              placeholder="0"
              value={formData.patentCount}
              onChange={(value) => updateField('patentCount', value)}
              min={0}
              helper="Include both pending and granted patents"
            />
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Competitive Moats</h3>
              
              <ToggleSwitch
                label="Network Effects Present?"
                value={formData.networkEffectsPresent}
                onChange={(value) => updateField('networkEffectsPresent', value)}
              />
              
              <ToggleSwitch
                label="Data Moat?"
                value={formData.hasDataMoat}
                onChange={(value) => updateField('hasDataMoat', value)}
              />
              
              <ToggleSwitch
                label="Regulatory Advantage?"
                value={formData.regulatoryAdvantagePresent}
                onChange={(value) => updateField('regulatoryAdvantagePresent', value)}
              />
            </div>
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Competitive Scores (1-5 Scale)</h3>
              
              <ScaleSelector
                label="Technology Differentiation"
                value={formData.techDifferentiationScore}
                onChange={(value) => updateField('techDifferentiationScore', value)}
                min={1}
                max={5}
                labels={{
                  1: "None",
                  3: "Moderate",
                  5: "Revolutionary"
                }}
                helper="How unique is your technology compared to competitors?"
              />
              
              <ScaleSelector
                label="Switching Cost"
                value={formData.switchingCostScore}
                onChange={(value) => updateField('switchingCostScore', value)}
                min={1}
                max={5}
                labels={{
                  1: "None",
                  3: "Moderate",
                  5: "Very High"
                }}
                helper="How difficult is it for customers to switch to competitors?"
              />
              
              <ScaleSelector
                label="Brand Strength"
                value={formData.brandStrengthScore}
                onChange={(value) => updateField('brandStrengthScore', value)}
                min={1}
                max={5}
                labels={{
                  1: "Unknown",
                  3: "Recognized",
                  5: "Industry Leader"
                }}
                helper="How strong is your brand recognition and reputation?"
              />
              
              <ScaleSelector
                label="Scalability"
                value={formData.scalabilityScore}
                onChange={(value) => updateField('scalabilityScore', value)}
                min={1}
                max={5}
                labels={{
                  1: "Linear",
                  3: "Good",
                  5: "Exponential"
                }}
                helper="How easily can you scale without proportional cost increases?"
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

export default Advantage;