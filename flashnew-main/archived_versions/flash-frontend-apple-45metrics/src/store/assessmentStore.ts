import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface AssessmentData {
  companyInfo?: any;
  capital?: any;
  advantage?: any;
  market?: any;
  people?: any;
  product?: any;
}

interface AssessmentStore {
  // Assessment data
  data: AssessmentData;
  
  // Assessment status
  isSubmitted: boolean;
  submittedAt: Date | null;
  
  // Results from API
  results: {
    successProbability?: number;
    confidence?: string;
    scores?: {
      capital: number;
      advantage: number;
      market: number;
      people: number;
    };
    insights?: string[];
    recommendations?: string[];
  } | null;
  
  // Actions
  updateData: (section: keyof AssessmentData, data: any) => void;
  submitAssessment: () => void;
  setResults: (results: any) => void;
  resetAssessment: () => void;
  
  // Computed
  getCompletionStatus: () => {
    totalSteps: number;
    completedSteps: number;
    percentage: number;
    isComplete: boolean;
  };
}

const useAssessmentStore = create<AssessmentStore>()(
  persist(
    (set, get) => ({
      // Initial state
      data: {},
      isSubmitted: false,
      submittedAt: null,
      results: null,
      
      // Actions
      updateData: (section, sectionData) =>
        set((state) => ({
          data: {
            ...state.data,
            [section]: sectionData,
          },
        })),
      
      submitAssessment: () =>
        set({
          isSubmitted: true,
          submittedAt: new Date(),
        }),
      
      setResults: (results) =>
        set({ results }),
      
      resetAssessment: () =>
        set({
          data: {},
          isSubmitted: false,
          submittedAt: null,
          results: null,
        }),
      
      // Computed
      getCompletionStatus: () => {
        const state = get();
        const sections = ['companyInfo', 'capital', 'advantage', 'market', 'people', 'product'];
        const completedSteps = sections.filter(
          (section) => state.data[section as keyof AssessmentData]
        ).length;
        
        return {
          totalSteps: sections.length,
          completedSteps,
          percentage: (completedSteps / sections.length) * 100,
          isComplete: completedSteps === sections.length,
        };
      },
    }),
    {
      name: 'flash-assessment-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        data: state.data,
        isSubmitted: state.isSubmitted,
        submittedAt: state.submittedAt,
        results: state.results,
      }),
    }
  )
);

export default useAssessmentStore;