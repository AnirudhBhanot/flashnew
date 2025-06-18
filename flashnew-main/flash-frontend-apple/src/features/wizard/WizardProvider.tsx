import React, { createContext, useContext, ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAssessmentStore, { AssessmentData } from '../../store/assessmentStore';

interface WizardContextType {
  currentStep: number;
  totalSteps: number;
  data: AssessmentData;
  goToStep: (step: number) => void;
  nextStep: () => void;
  previousStep: () => void;
  updateData: (stepData: Partial<AssessmentData>) => void;
  canNavigateToStep: (step: number) => boolean;
}

const WizardContext = createContext<WizardContextType | null>(null);

const steps = [
  '/assessment/company',
  '/assessment/capital',
  '/assessment/advantage',
  '/assessment/market',
  '/assessment/people',
  '/assessment/review',
];

export const WizardProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentStep = steps.indexOf(location.pathname);
  
  // Get data and actions from Zustand store
  const { data, updateData: updateStoreData, getCompletionStatus } = useAssessmentStore();

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      const nextIndex = currentStep + 1;
      navigate(steps[nextIndex]);
    } else {
      navigate('/analysis');
    }
  };

  const previousStep = () => {
    if (currentStep > 0) {
      const prevIndex = currentStep - 1;
      navigate(steps[prevIndex]);
    }
  };

  const goToStep = (step: number) => {
    if (canNavigateToStep(step)) {
      navigate(steps[step]);
    }
  };

  const canNavigateToStep = (step: number) => {
    // First step is always accessible
    if (step === 0) return true;
    
    // Check if previous steps have data
    const requiredSections = ['companyInfo', 'capital', 'advantage', 'market', 'people'];
    for (let i = 0; i < step && i < requiredSections.length; i++) {
      if (!data[requiredSections[i] as keyof AssessmentData]) {
        return false;
      }
    }
    return true;
  };

  const updateData = (stepData: Partial<AssessmentData>) => {
    // Update the appropriate section in the store
    const sectionKey = Object.keys(stepData)[0] as keyof AssessmentData;
    if (sectionKey) {
      updateStoreData(sectionKey, stepData[sectionKey]);
    }
  };

  return (
    <WizardContext.Provider
      value={{
        currentStep: currentStep === -1 ? 0 : currentStep,
        totalSteps: steps.length,
        data,
        goToStep,
        nextStep,
        previousStep,
        updateData,
        canNavigateToStep,
      }}
    >
      {children}
    </WizardContext.Provider>
  );
};

export const useWizard = () => {
  const context = useContext(WizardContext);
  if (!context) {
    throw new Error('useWizard must be used within WizardProvider');
  }
  return context;
};