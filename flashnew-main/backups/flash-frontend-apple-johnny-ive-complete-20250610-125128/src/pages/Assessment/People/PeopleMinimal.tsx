import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  FormField, 
  MinimalInput, 
  MinimalToggle,
  MinimalScale,
  MinimalProgress 
} from '../../../design-system/minimalist';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './PeopleMinimal.module.scss';

interface PeopleData {
  founderCount: number | string;
  teamSize: number | string;
  avgExperience: number | string;
  domainExpertiseYears: number | string;
  priorStartupCount: number | string;
  priorExits: number | string;
  boardAdvisorScore: number;
  advisorCount: number | string;
  teamDiversity: number | string;
  keyPersonDependency: boolean;
  productRetention30d: number | string;
  productRetention90d: number | string;
  dauMauRatio: number | string;
}

const People: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  const [currentField, setCurrentField] = useState(0);
  const [showMetrics, setShowMetrics] = useState(false);
  
  const [formData, setFormData] = useState<PeopleData>({
    founderCount: data.people?.founderCount || '',
    teamSize: data.people?.teamSize || '',
    avgExperience: data.people?.avgExperience || '',
    domainExpertiseYears: data.people?.domainExpertiseYears || '',
    priorStartupCount: data.people?.priorStartupCount || '',
    priorExits: data.people?.priorExits || '',
    boardAdvisorScore: data.people?.boardAdvisorScore || 3,
    advisorCount: data.people?.advisorCount || '',
    teamDiversity: data.people?.teamDiversity || '',
    keyPersonDependency: data.people?.keyPersonDependency || false,
    productRetention30d: data.people?.productRetention30d || '',
    productRetention90d: data.people?.productRetention90d || '',
    dauMauRatio: data.people?.dauMauRatio || '',
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof PeopleData, string>>>({});

  // Auto-save data after changes
  useEffect(() => {
    if (!touched) return;
    
    const timer = setTimeout(() => {
      try {
        updateData({ people: formData });
        setLastSaved(new Date());
        setSaveError(false);
      } catch (error) {
        setSaveError(true);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof PeopleData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof PeopleData, string>> = {};
    
    if (!formData.founderCount || Number(formData.founderCount) === 0) {
      newErrors.founderCount = 'Founder count is required';
    }
    
    if (!formData.teamSize || Number(formData.teamSize) === 0) {
      newErrors.teamSize = 'Team size is required';
    }
    
    if (!formData.avgExperience || Number(formData.avgExperience) === 0) {
      newErrors.avgExperience = 'Average experience is required';
    }
    
    if (!formData.domainExpertiseYears || Number(formData.domainExpertiseYears) === 0) {
      newErrors.domainExpertiseYears = 'Domain expertise is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinue = () => {
    if (validate()) {
      updateData({ people: formData });
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

  const coreFields = [
    {
      question: "How many founders?",
      helper: "Number of co-founders",
      component: (
        <div className={styles.founderInput}>
          <MinimalInput
            value={formData.founderCount}
            onChange={(value) => updateField('founderCount', value)}
            type="number"
            placeholder="2"
            align="center"
          />
          <AnimatePresence>
            {formData.founderCount && Number(formData.founderCount) > 0 && (
              <motion.div 
                className={styles.founderIcons}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
              >
                {Array.from({ length: Math.min(Number(formData.founderCount), 5) }).map((_, i) => (
                  <motion.div
                    key={i}
                    className={styles.founderIcon}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: i * 0.1 }}
                  />
                ))}
                {Number(formData.founderCount) > 5 && (
                  <motion.span
                    className={styles.founderMore}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    +{Number(formData.founderCount) - 5}
                  </motion.span>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ),
      error: errors.founderCount
    },
    {
      question: "How big is your team?",
      helper: "Full-time employees",
      component: (
        <MinimalInput
          value={formData.teamSize}
          onChange={(value) => updateField('teamSize', value)}
          type="number"
          placeholder="10"
          align="center"
        />
      ),
      error: errors.teamSize
    },
    {
      question: "Average years of experience?",
      helper: "Professional experience across the team",
      component: (
        <MinimalInput
          value={formData.avgExperience}
          onChange={(value) => updateField('avgExperience', value)}
          type="number"
          placeholder="10"
          suffix="years"
          align="center"
        />
      ),
      error: errors.avgExperience
    },
    {
      question: "Domain expertise?",
      helper: "Years in this specific industry",
      component: (
        <MinimalInput
          value={formData.domainExpertiseYears}
          onChange={(value) => updateField('domainExpertiseYears', value)}
          type="number"
          placeholder="5"
          suffix="years"
          align="center"
        />
      ),
      error: errors.domainExpertiseYears
    },
    {
      question: "Prior startup experience?",
      helper: "Number of startups worked at before",
      component: (
        <MinimalInput
          value={formData.priorStartupCount}
          onChange={(value) => updateField('priorStartupCount', value)}
          type="number"
          placeholder="2"
          align="center"
        />
      )
    },
    {
      question: "Any successful exits?",
      helper: "Previous successful outcomes",
      component: (
        <MinimalInput
          value={formData.priorExits}
          onChange={(value) => updateField('priorExits', value)}
          type="number"
          placeholder="0"
          align="center"
        />
      )
    },
    {
      question: "How many advisors?",
      helper: "Active advisors helping your company",
      component: (
        <MinimalInput
          value={formData.advisorCount}
          onChange={(value) => updateField('advisorCount', value)}
          type="number"
          placeholder="3"
          align="center"
        />
      )
    },
    {
      question: "Quality of board & advisors?",
      helper: "Experience and influence of your advisors",
      component: (
        <MinimalScale
          value={formData.boardAdvisorScore}
          onChange={(value) => updateField('boardAdvisorScore', value)}
          min={1}
          max={5}
          labels={{
            1: "Minimal",
            3: "Solid",
            5: "World-class"
          }}
        />
      )
    },
    {
      question: "Team diversity percentage?",
      helper: "Underrepresented groups in your team",
      component: (
        <MinimalInput
          value={formData.teamDiversity}
          onChange={(value) => updateField('teamDiversity', value)}
          type="number"
          placeholder="30"
          suffix="%"
          align="center"
        />
      )
    },
    {
      question: "Is there key person risk?",
      helper: "Does the company depend heavily on one person?",
      component: (
        <MinimalToggle
          value={formData.keyPersonDependency}
          onChange={(value) => updateField('keyPersonDependency', value)}
          label="Yes, there's dependency"
        />
      )
    }
  ];

  const metricFields = [
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

  const fields = showMetrics ? [...coreFields, ...metricFields] : coreFields;

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
          <MinimalProgress current={5} total={6} showSteps />
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
          <h1 className={styles.title}>People</h1>
          <p className={styles.subtitle}>Your most important asset</p>
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

        {!showMetrics && (
          <motion.div 
            className={styles.metricsToggle}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <button
              className={styles.metricsButton}
              onClick={() => setShowMetrics(true)}
            >
              Add engagement metrics
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 4V16M4 10H16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </motion.div>
        )}

        <AnimatePresence>
          {(formData.teamSize || formData.founderCount) && (
            <motion.div 
              className={styles.teamVisual}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.6, ease: [0.25, 0, 0, 1] }}
            >
              <motion.div 
                className={styles.teamStat}
                whileHover={{ scale: 1.05 }}
              >
                <span className={styles.statNumber}>
                  {Number(formData.teamSize || 0) + Number(formData.founderCount || 0)}
                </span>
                <span className={styles.statLabel}>Total team</span>
              </motion.div>
              
              {formData.avgExperience && (
                <motion.div 
                  className={styles.teamStat}
                  whileHover={{ scale: 1.05 }}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <span className={styles.statNumber}>
                    {Number(formData.avgExperience) * (Number(formData.teamSize || 0) + Number(formData.founderCount || 0))}
                  </span>
                  <span className={styles.statLabel}>Combined years</span>
                </motion.div>
              )}
              
              {formData.priorExits && Number(formData.priorExits) > 0 && (
                <motion.div 
                  className={styles.teamStat}
                  whileHover={{ scale: 1.05 }}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <span className={styles.statNumber}>
                    {formData.priorExits}
                  </span>
                  <span className={styles.statLabel}>Exits</span>
                </motion.div>
              )}
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

export default People;