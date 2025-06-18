import React, { useEffect } from 'react';
import { motion } from '../../helpers/motion';
import { useNavigate } from 'react-router-dom';
import useAssessmentStore from '../../store/assessmentStore';
import { apiService } from '../../services/api';
import { useError } from '../../contexts/ErrorContext';
import styles from './AnalysisProgressBar.module.scss';

const AnalysisProgressBar: React.FC = () => {
  const navigate = useNavigate();
  const { data, setResults } = useAssessmentStore();
  const { showError } = useError();

  useEffect(() => {
    // Start analysis after the progress animation
    const analysisTimeout = setTimeout(() => {
      callAPI();
    }, 2500); // 2.5 seconds for the progress animation

    return () => {
      clearTimeout(analysisTimeout);
    };
  }, []);

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
        // Navigate to results with minimal delay
        navigate('/results');
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
        
        // Navigate to results immediately
        navigate('/results');
      }
    } catch (err) {
      console.error('API call failed:', err);
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed';
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
      }, 500);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.progressContainer}>
        <motion.div
          className={styles.progressBar}
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ 
            duration: 2.5, 
            ease: [0.25, 0.1, 0.25, 1] // Custom cubic-bezier for Apple-like easing
          }}
          style={{ originX: 0 }}
        />
      </div>
    </div>
  );
};

export default AnalysisProgressBar;