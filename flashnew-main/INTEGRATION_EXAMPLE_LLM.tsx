/**
 * Example integration of LLM features into AnalysisResults component
 * This shows how to modify the existing component to use dynamic AI analysis
 */

import React, { useState, useEffect } from 'react';
import { llmService } from '../services/llmService';

// Add to your AnalysisResults component:

export const AnalysisResultsWithLLM: React.FC<AnalysisResultsProps> = ({ data }) => {
  // New state for LLM features
  const [llmRecommendations, setLlmRecommendations] = useState(null);
  const [isLoadingLLM, setIsLoadingLLM] = useState(false);
  const [llmAvailable, setLlmAvailable] = useState(false);
  const [showAIBadge, setShowAIBadge] = useState(false);

  // Check LLM availability on mount
  useEffect(() => {
    checkLLMAvailability();
  }, []);

  // Fetch LLM recommendations when data changes
  useEffect(() => {
    if (data && llmAvailable) {
      fetchLLMRecommendations();
    }
  }, [data, llmAvailable]);

  const checkLLMAvailability = async () => {
    try {
      const available = await llmService.isAvailable();
      setLlmAvailable(available);
    } catch (error) {
      console.error('Failed to check LLM availability:', error);
      setLlmAvailable(false);
    }
  };

  const fetchLLMRecommendations = async () => {
    setIsLoadingLLM(true);
    try {
      const response = await llmService.getRecommendations(
        data.userInput,
        {
          capital: data.camp_scores?.capital || data.pillar_scores?.capital || 0.5,
          advantage: data.camp_scores?.advantage || data.pillar_scores?.advantage || 0.5,
          market: data.camp_scores?.market || data.pillar_scores?.market || 0.5,
          people: data.camp_scores?.people || data.pillar_scores?.people || 0.5,
          success_probability: data.success_probability || 0.5
        },
        data.verdict
      );

      if (response.type === 'ai_generated') {
        setLlmRecommendations(response.recommendations);
        setShowAIBadge(true);
      }
    } catch (error) {
      console.error('Failed to fetch LLM recommendations:', error);
      // Fall back to existing logic
    } finally {
      setIsLoadingLLM(false);
    }
  };

  // Modified getRecommendations function
  const getRecommendations = (data: any): Array<any> => {
    // Use LLM recommendations if available
    if (llmRecommendations && llmRecommendations.length > 0) {
      return llmService.formatRecommendations(llmRecommendations);
    }

    // Otherwise use existing fallback logic
    return getStaticRecommendations(data);
  };

  // New What-If analysis with LLM
  const calculateDynamicWhatIf = async (improvements: any[]) => {
    if (!llmAvailable) {
      // Use existing static calculation
      return calculateStaticWhatIf(improvements);
    }

    try {
      const whatIfResult = await llmService.analyzeWhatIf(
        data.userInput,
        {
          capital: data.camp_scores?.capital || 0.5,
          advantage: data.camp_scores?.advantage || 0.5,
          market: data.camp_scores?.market || 0.5,
          people: data.camp_scores?.people || 0.5,
          success_probability: data.success_probability || 0.5
        },
        improvements.map(imp => ({
          id: imp.id,
          description: imp.description
        }))
      );

      return {
        newProbability: whatIfResult.new_probability.value,
        confidenceInterval: {
          lower: whatIfResult.new_probability.lower,
          upper: whatIfResult.new_probability.upper
        },
        scoreChanges: whatIfResult.score_changes,
        timeline: whatIfResult.timeline,
        risks: whatIfResult.risks
      };
    } catch (error) {
      console.error('Dynamic what-if failed:', error);
      return calculateStaticWhatIf(improvements);
    }
  };

  // In the render section, add AI indicators:
  return (
    <div className="analysis-results">
      {/* Recommendations Section */}
      <div className="recommendations-section">
        <div className="section-header">
          <h2>Recommendations</h2>
          {showAIBadge && (
            <span className="ai-badge">
              <span className="ai-icon">✨</span>
              AI-Powered
            </span>
          )}
        </div>

        {isLoadingLLM ? (
          <div className="llm-loading">
            <div className="loading-spinner" />
            <p>Generating personalized recommendations...</p>
          </div>
        ) : (
          <div className="recommendations-grid">
            {getRecommendations(data).map((rec, idx) => (
              <div key={idx} className="recommendation-card">
                {rec.ai_generated && <div className="ai-indicator" />}
                {/* Rest of recommendation card */}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* What-If Section with dynamic calculations */}
      <div className="whatif-section">
        <h2>What-If Analysis</h2>
        {llmAvailable && (
          <p className="ai-notice">
            Predictions powered by AI analysis of similar companies
          </p>
        )}
        {/* Rest of what-if UI */}
      </div>
    </div>
  );
};

// CSS additions for AI indicators
const aiStyles = `
.ai-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-left: 12px;
}

.ai-icon {
  font-size: 1.1em;
}

.ai-indicator {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
  }
}

.llm-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.ai-notice {
  font-size: 0.875rem;
  color: #667eea;
  font-style: italic;
  margin-bottom: 16px;
}
`;