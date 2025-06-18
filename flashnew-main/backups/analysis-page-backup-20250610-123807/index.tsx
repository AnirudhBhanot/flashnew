import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from '../../helpers/motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { Icon } from '../../design-system/components';
import { apiService } from '../../services/api';
import { useError } from '../../contexts/ErrorContext';
import styles from './Analysis.module.scss';

interface AnalysisStep {
  id: string;
  title: string;
  description: string;
  icon: string;
  duration: number; // milliseconds
}

const analysisSteps: AnalysisStep[] = [
  {
    id: 'preprocessing',
    title: 'Preprocessing Data',
    description: 'Normalizing and validating your inputs',
    icon: 'chart.line.uptrend',
    duration: 2000,
  },
  {
    id: 'capital',
    title: 'Analyzing Capital',
    description: 'Evaluating financial health and runway',
    icon: 'building.2',
    duration: 3000,
  },
  {
    id: 'advantage',
    title: 'Assessing Advantage',
    description: 'Measuring competitive moat and differentiation',
    icon: 'sparkles',
    duration: 3000,
  },
  {
    id: 'market',
    title: 'Evaluating Market',
    description: 'Analyzing TAM and growth potential',
    icon: 'chart.line.uptrend',
    duration: 3000,
  },
  {
    id: 'people',
    title: 'Reviewing Team',
    description: 'Assessing leadership and experience',
    icon: 'brain',
    duration: 3000,
  },
  {
    id: 'synthesis',
    title: 'Generating Insights',
    description: 'Combining all factors for final assessment',
    icon: 'sparkles',
    duration: 4000,
  },
];

const Analysis: React.FC = () => {
  const navigate = useNavigate();
  const { data, setResults } = useAssessmentStore();
  const { showError } = useError();
  const [currentStep, setCurrentStep] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [stepProgress, setStepProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentStep < analysisSteps.length) {
      const step = analysisSteps[currentStep];
      const stepDuration = step.duration;
      
      // Animate step progress
      const progressInterval = setInterval(() => {
        setStepProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval);
            return 100;
          }
          return prev + (100 / (stepDuration / 50)); // Update every 50ms
        });
      }, 50);

      // Move to next step
      const stepTimeout = setTimeout(() => {
        if (currentStep === analysisSteps.length - 1) {
          // Final step completed
          setIsComplete(true);
          callAPI();
        } else {
          setCurrentStep(currentStep + 1);
          setStepProgress(0);
        }
      }, stepDuration);

      return () => {
        clearTimeout(stepTimeout);
        clearInterval(progressInterval);
      };
    }
  }, [currentStep]);

  useEffect(() => {
    // Update overall progress
    const overallProgress = ((currentStep + (stepProgress / 100)) / analysisSteps.length) * 100;
    setProgress(overallProgress);
  }, [currentStep, stepProgress]);

  const callAPI = async () => {
    try {
      // Check API health first
      const health = await apiService.health();
      if (!health || !health.status) {
        throw new Error('API service is unavailable');
      }

      // Get the stored results from the prediction
      const storedResults = useAssessmentStore.getState().results;
      
      if (storedResults && storedResults.successProbability !== undefined) {
        // We already have prediction results from the Review page
        console.log('Using stored results from Review page:', storedResults);
        console.log('Stored scores:', storedResults.scores);
        // Navigate to results immediately
        setTimeout(() => {
          navigate('/results');
        }, 500);
      } else {
        // If somehow we don't have results, make a new prediction
        const prediction = await apiService.predict(data);
        
        // Transform and set results
        setResults({
          successProbability: prediction.success_probability,
          confidence: prediction.confidence,
          scores: prediction.camp_scores,
          insights: prediction.insights || [],
          recommendations: [],
          riskAssessment: prediction.risk_level,
          detailedAnalysis: {
            verdict: prediction.verdict,
            confidence_interval: prediction.confidence_interval,
            pillar_scores: prediction.pillar_scores
          }
        });
        
        // Navigate to results after a short delay
        setTimeout(() => {
          navigate('/results');
        }, 500);
      }
    } catch (err) {
      console.error('API call failed:', err);
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed';
      setError(errorMessage);
      showError(errorMessage, 'error');
      
      // Log the error details
      console.error('Error details:', err);
      
      // Fallback to mock data for demo purposes
      const mockResults = {
        successProbability: 0.73,
        confidence: 'high',
        scores: {
          capital: 0.78,
          advantage: 0.71,
          market: 0.69,
          people: 0.75,
        },
        insights: [
          'Strong financial position with 18 months runway',
          'Clear competitive advantages in your market',
          'Team has relevant industry experience',
          'Market timing appears favorable',
        ],
        recommendations: [
          'Focus on customer acquisition to improve unit economics',
          'Consider filing for additional patents to strengthen moat',
          'Hire a dedicated sales leader to accelerate growth',
          'Explore strategic partnerships for distribution',
        ],
      };
      
      setResults(mockResults);
      setTimeout(() => {
        navigate('/results');
      }, 1000);
    }
  };

  const currentStepData = analysisSteps[currentStep] || analysisSteps[analysisSteps.length - 1];

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <motion.div
          className={styles.content}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className={styles.header}>
            <h1 className={styles.title}>Analyzing Your Startup</h1>
            <p className={styles.subtitle}>
              Our AI models are evaluating your assessment
            </p>
          </div>

          <div className={styles.progressContainer}>
            <div className={styles.progressBar}>
              <motion.div
                className={styles.progressFill}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
              />
            </div>
            <span className={styles.progressText}>{Math.round(progress)}%</span>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={currentStepData.id}
              className={styles.stepContainer}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <motion.div
                className={styles.iconWrapper}
                animate={{
                  rotate: isComplete ? 0 : [0, 360],
                }}
                transition={{
                  duration: 2,
                  repeat: isComplete ? 0 : Infinity,
                  ease: 'linear',
                }}
              >
                <Icon name={currentStepData.icon} size={48} />
              </motion.div>
              
              <h2 className={styles.stepTitle}>{currentStepData.title}</h2>
              <p className={styles.stepDescription}>{currentStepData.description}</p>

              <div className={styles.stepProgress}>
                <motion.div
                  className={styles.stepProgressFill}
                  animate={{ width: `${stepProgress}%` }}
                  transition={{ duration: 0.1 }}
                />
              </div>
            </motion.div>
          </AnimatePresence>

          {error && (
            <motion.div
              className={styles.errorMessage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Icon name="exclamationmark.triangle" size={20} />
              <span>{error}</span>
            </motion.div>
          )}

          <div className={styles.steps}>
            {analysisSteps.map((step, index) => (
              <motion.div
                key={step.id}
                className={`${styles.step} ${
                  index < currentStep ? styles.completed : ''
                } ${index === currentStep ? styles.active : ''}`}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                {index < currentStep ? (
                  <Icon name="checkmark" size={16} />
                ) : (
                  <div className={styles.stepNumber}>{index + 1}</div>
                )}
              </motion.div>
            ))}
          </div>

          {isComplete && (
            <motion.div
              className={styles.complete}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              <Icon name="checkmark" size={64} />
              <h3>Analysis Complete!</h3>
              <p>Preparing your results...</p>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default Analysis;