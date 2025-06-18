import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/WizardProvider';
import { 
  Button, 
  Icon, 
  NumberField,
  PercentageField,
  ScaleSelector,
  ToggleSwitch
} from '../../../design-system/components';
import { AutoSaveIndicator } from '../../../components/AutoSaveIndicator';
import styles from './People.module.scss';

interface PeopleData {
  foundersCount: number | string;
  teamSizeFullTime: number | string;
  yearsExperienceAvg: number | string;
  domainExpertiseYearsAvg: number | string;
  priorStartupExperienceCount: number | string;
  priorSuccessfulExitsCount: number | string;
  boardAdvisorExperienceScore: number;
  advisorsCount: number | string;
  teamDiversityPercent: number | string;
  keyPersonDependency: boolean;
}

const People: React.FC = () => {
  const { nextStep, previousStep, updateData, data } = useWizard();
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveError, setSaveError] = useState(false);
  const [touched, setTouched] = useState(false);
  
  const [formData, setFormData] = useState<PeopleData>({
    foundersCount: data.people?.foundersCount || '',
    teamSizeFullTime: data.people?.teamSizeFullTime || '',
    yearsExperienceAvg: data.people?.yearsExperienceAvg || '',
    domainExpertiseYearsAvg: data.people?.domainExpertiseYearsAvg || '',
    priorStartupExperienceCount: data.people?.priorStartupExperienceCount || '0',
    priorSuccessfulExitsCount: data.people?.priorSuccessfulExitsCount || '0',
    boardAdvisorExperienceScore: data.people?.boardAdvisorExperienceScore || 3,
    advisorsCount: data.people?.advisorsCount || '0',
    teamDiversityPercent: data.people?.teamDiversityPercent || '',
    keyPersonDependency: data.people?.keyPersonDependency || false,
  });
  
  const [errors, setErrors] = useState<Partial<Record<keyof PeopleData, string>>>({});
  const [showAdvanced, setShowAdvanced] = useState(false);
  
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
    }, 1000); // Save after 1 second of inactivity

    return () => clearTimeout(timer);
  }, [formData, touched, updateData]);
  
  const updateField = (field: keyof PeopleData, value: any) => {
    setFormData({ ...formData, [field]: value });
    setTouched(true);
  };

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof PeopleData, string>> = {};
    
    if (!formData.foundersCount || Number(formData.foundersCount) === 0) {
      newErrors.foundersCount = 'Number of founders is required';
    }
    
    if (!formData.teamSizeFullTime || Number(formData.teamSizeFullTime) === 0) {
      newErrors.teamSizeFullTime = 'Team size is required';
    }
    
    if (!formData.yearsExperienceAvg) {
      newErrors.yearsExperienceAvg = 'Average experience is required';
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
          <h1 className={styles.title}>Team & Leadership</h1>
          <p className={styles.subtitle}>Tell us about your team's experience and composition</p>
          
          <div className={styles.form}>
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Team Composition</h3>
              
              <NumberField
                label="Number of Founders"
                placeholder="2"
                value={formData.foundersCount}
                onChange={(value) => updateField('foundersCount', value)}
                error={errors.foundersCount}
                min={1}
                helper="How many co-founders does your company have?"
                required
              />
              
              <NumberField
                label="Full-Time Team Size"
                placeholder="10"
                value={formData.teamSizeFullTime}
                onChange={(value) => updateField('teamSizeFullTime', value)}
                error={errors.teamSizeFullTime}
                min={1}
                helper="Total number of full-time employees"
                required
              />
              
              <NumberField
                label="Number of Advisors"
                placeholder="2"
                value={formData.advisorsCount}
                onChange={(value) => updateField('advisorsCount', value)}
                min={0}
                helper="Active advisors providing regular guidance"
              />
              
              <PercentageField
                label="Team Diversity"
                placeholder="30"
                value={formData.teamDiversityPercent}
                onChange={(value) => updateField('teamDiversityPercent', value)}
                helper="Percentage of team from underrepresented groups"
              />
            </div>
            
            <div className={styles.section}>
              <h3 className={styles.sectionTitle}>Experience & Expertise</h3>
              
              <NumberField
                label="Average Years of Experience"
                placeholder="10"
                value={formData.yearsExperienceAvg}
                onChange={(value) => updateField('yearsExperienceAvg', value)}
                error={errors.yearsExperienceAvg}
                min={0}
                helper="Average professional experience across founding team"
                required
              />
              
              <NumberField
                label="Domain Expertise (Years)"
                placeholder="8"
                value={formData.domainExpertiseYearsAvg}
                onChange={(value) => updateField('domainExpertiseYearsAvg', value)}
                min={0}
                helper="Average years in your specific industry/domain"
              />
              
              <NumberField
                label="Prior Startups Founded"
                placeholder="1"
                value={formData.priorStartupExperienceCount}
                onChange={(value) => updateField('priorStartupExperienceCount', value)}
                min={0}
                helper="Total number of startups previously founded by team"
              />
              
              <NumberField
                label="Successful Exits"
                placeholder="0"
                value={formData.priorSuccessfulExitsCount}
                onChange={(value) => updateField('priorSuccessfulExitsCount', value)}
                min={0}
                helper="Number of successful exits (acquisition/IPO)"
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
                <h3 className={styles.sectionTitle}>Leadership & Governance</h3>
                
                <ScaleSelector
                  label="Board & Advisor Quality"
                  value={formData.boardAdvisorExperienceScore}
                  onChange={(value) => updateField('boardAdvisorExperienceScore', value)}
                  min={1}
                  max={5}
                  labels={{
                    1: "Limited",
                    3: "Experienced",
                    5: "World-class"
                  }}
                  helper="Quality and relevance of board members and advisors"
                />
                
                <ToggleSwitch
                  label="Key Person Dependency?"
                  value={formData.keyPersonDependency}
                  onChange={(value) => updateField('keyPersonDependency', value)}
                />
              </div>
            </motion.div>
            
            <Button
              variant="text"
              onClick={() => setShowAdvanced(!showAdvanced)}
              icon={<Icon name={showAdvanced ? 'chevron.up' : 'chevron.down'} />}
            >
              {showAdvanced ? 'Hide' : 'Show'} leadership details
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

export default People;