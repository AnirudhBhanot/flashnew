import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ExternalReality.module.scss';

interface ForceAssessment {
  score: number;
  notes: string;
  factors: string[];
}

interface ExternalRealityData {
  industryRivalry: ForceAssessment;
  customerPower: ForceAssessment;
  supplierPower: ForceAssessment;
  substituteThreat: ForceAssessment;
  newEntrantRisk: ForceAssessment;
}

const ExternalReality: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<ExternalRealityData>({
    industryRivalry: { score: 0, notes: '', factors: [] },
    customerPower: { score: 0, notes: '', factors: [] },
    supplierPower: { score: 0, notes: '', factors: [] },
    substituteThreat: { score: 0, notes: '', factors: [] },
    newEntrantRisk: { score: 0, notes: '', factors: [] },
  });

  const [completionPercentage, setCompletionPercentage] = useState(0);

  // Load saved data on mount
  useEffect(() => {
    const savedData = localStorage.getItem('deepDive_externalReality');
    if (savedData) {
      setData(JSON.parse(savedData));
    }
  }, []);

  // Calculate completion percentage
  useEffect(() => {
    const forces = Object.values(data);
    const completedForces = forces.filter(force => force.score > 0).length;
    setCompletionPercentage((completedForces / forces.length) * 100);
  }, [data]);

  // Save data to localStorage
  const saveData = () => {
    localStorage.setItem('deepDive_externalReality', JSON.stringify(data));
  };

  const updateForce = (
    forceName: keyof ExternalRealityData,
    field: keyof ForceAssessment,
    value: any
  ) => {
    setData(prev => ({
      ...prev,
      [forceName]: {
        ...prev[forceName],
        [field]: value,
      },
    }));
  };

  const toggleFactor = (forceName: keyof ExternalRealityData, factor: string) => {
    const currentFactors = data[forceName].factors;
    const newFactors = currentFactors.includes(factor)
      ? currentFactors.filter(f => f !== factor)
      : [...currentFactors, factor];
    
    updateForce(forceName, 'factors', newFactors);
  };

  const getScoreColor = (score: number): string => {
    if (score === 0) return '#e2e8f0';
    if (score <= 2) return '#10b981'; // Low threat - Green
    if (score <= 3) return '#f59e0b'; // Medium threat - Yellow
    return '#ef4444'; // High threat - Red
  };

  const getScoreLabel = (score: number): string => {
    const labels = ['Not Assessed', 'Very Low', 'Low', 'Medium', 'High', 'Very High'];
    return labels[score];
  };

  const forces = [
    {
      key: 'industryRivalry' as keyof ExternalRealityData,
      title: 'Industry Rivalry',
      description: 'Competition intensity among existing players',
      icon: '⚔️',
      questions: [
        'How many direct competitors exist?',
        'How aggressive is price competition?',
        'How fast is the market growing?',
      ],
      factors: [
        'High number of competitors',
        'Low market growth',
        'High fixed costs',
        'Low switching costs',
        'High exit barriers',
        'Commodity products'
      ]
    },
    {
      key: 'customerPower' as keyof ExternalRealityData,
      title: 'Customer Power',
      description: 'Bargaining power of customers',
      icon: '👥',
      questions: [
        'How easy is it for customers to switch?',
        'How price sensitive are customers?',
        'How concentrated is the customer base?',
      ],
      factors: [
        'Few large customers',
        'Low switching costs',
        'Price sensitive buyers',
        'Backward integration threat',
        'Standard products',
        'Full information availability'
      ]
    },
    {
      key: 'supplierPower' as keyof ExternalRealityData,
      title: 'Supplier Power',
      description: 'Bargaining power of suppliers',
      icon: '🏭',
      questions: [
        'How many alternative suppliers exist?',
        'How critical are supplier inputs?',
        'How easy is it to switch suppliers?',
      ],
      factors: [
        'Few suppliers',
        'Unique products',
        'High switching costs',
        'Forward integration threat',
        'Critical inputs',
        'No substitutes'
      ]
    },
    {
      key: 'substituteThreat' as keyof ExternalRealityData,
      title: 'Substitute Threats',
      description: 'Risk from alternative solutions',
      icon: '🔄',
      questions: [
        'How many substitute products exist?',
        'How attractive are substitutes?',
        'How easy is substitution?',
      ],
      factors: [
        'Lower priced alternatives',
        'Better quality substitutes',
        'Low switching costs',
        'High buyer propensity',
        'Technology disruption',
        'Changing customer needs'
      ]
    },
    {
      key: 'newEntrantRisk' as keyof ExternalRealityData,
      title: 'New Entrants Risk',
      description: 'Threat from new market entrants',
      icon: '🚪',
      questions: [
        'How high are barriers to entry?',
        'How strong is brand loyalty?',
        'How much capital is required?',
      ],
      factors: [
        'Low capital requirements',
        'Easy market access',
        'No proprietary technology',
        'Weak brand loyalty',
        'Low regulatory barriers',
        'No network effects'
      ]
    }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>External Reality Check</h1>
        <p className={styles.subtitle}>
          Assess the competitive forces shaping your market environment
        </p>
      </div>

      <div className={styles.progressSection}>
        <div className={styles.progressHeader}>
          <span>Overall Assessment Progress</span>
          <span className={styles.percentage}>{Math.round(completionPercentage)}%</span>
        </div>
        <div className={styles.progressBar}>
          <div 
            className={styles.progressFill} 
            style={{ width: `${completionPercentage}%` }}
          />
        </div>
      </div>

      <div className={styles.forcesGrid}>
        {forces.map(force => {
          const forceData = data[force.key];
          return (
            <div key={force.key} className={styles.forceCard}>
              <div className={styles.forceHeader}>
                <div className={styles.forceIcon}>{force.icon}</div>
                <div className={styles.forceInfo}>
                  <h3 className={styles.forceName}>{force.title}</h3>
                  <p className={styles.forceDescription}>{force.description}</p>
                </div>
              </div>
              
              <div className={styles.ratingSection}>
                <div className={styles.ratingLabel}>
                  <span>Threat Level</span>
                  <span className={styles.currentScore} style={{ color: getScoreColor(forceData.score) }}>
                    {getScoreLabel(forceData.score)}
                  </span>
                </div>
                <div className={styles.ratingScale}>
                  {[1, 2, 3, 4, 5].map(score => (
                    <button
                      key={score}
                      className={`${styles.scaleOption} ${
                        forceData.score === score ? styles.selected : ''
                      }`}
                      onClick={() => updateForce(force.key, 'score', score)}
                      style={{
                        backgroundColor: forceData.score === score 
                          ? getScoreColor(score) 
                          : undefined,
                        borderColor: forceData.score === score 
                          ? getScoreColor(score) 
                          : undefined,
                        color: forceData.score === score ? 'white' : undefined
                      }}
                    >
                      {score}
                    </button>
                  ))}
                </div>
              </div>

              <div className={styles.questionsSection}>
                <h4>Consider:</h4>
                <ul className={styles.questionsList}>
                  {force.questions.map((question, index) => (
                    <li key={index}>{question}</li>
                  ))}
                </ul>
              </div>

              <div className={styles.factorsSection}>
                <h4>Key Factors:</h4>
                <div className={styles.factorsList}>
                  {force.factors.map((factor, index) => (
                    <button
                      key={index}
                      className={`${styles.factorTag} ${
                        forceData.factors.includes(factor) ? styles.selected : ''
                      }`}
                      onClick={() => toggleFactor(force.key, factor)}
                    >
                      {factor}
                    </button>
                  ))}
                </div>
              </div>

              <div className={styles.notesSection}>
                <label htmlFor={`notes-${force.key}`}>Notes & Insights:</label>
                <textarea
                  id={`notes-${force.key}`}
                  className={styles.notesInput}
                  value={forceData.notes}
                  onChange={(e) => updateForce(force.key, 'notes', e.target.value)}
                  placeholder="Add your observations and strategic insights..."
                  rows={3}
                />
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.summarySection}>
        <h3>Market Forces Summary</h3>
        <div className={styles.summaryGrid}>
          {forces.map(force => {
            const forceData = data[force.key];
            return (
              <div key={force.key} className={styles.summaryItem}>
                <span className={styles.forceLabel}>{force.title}:</span>
                <div className={styles.summaryScore}>
                  <div className={styles.scoreBarContainer}>
                    <div 
                      className={styles.scoreBar}
                      style={{ 
                        width: `${(forceData.score / 5) * 100}%`,
                        backgroundColor: getScoreColor(forceData.score)
                      }}
                    />
                  </div>
                  <span className={styles.scoreText}>
                    {getScoreLabel(forceData.score)}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
        
        <div className={styles.overallThreat}>
          <h4>Overall Market Threat Level:</h4>
          <div className={styles.threatMeter}>
            {(() => {
              const avgScore = Object.values(data).reduce(
                (sum, force) => sum + force.score, 0
              ) / Object.values(data).length;
              const threatLevel = avgScore === 0 ? 'Not Assessed' :
                avgScore <= 2 ? 'Low' :
                avgScore <= 3 ? 'Medium' : 'High';
              const color = avgScore === 0 ? '#e2e8f0' :
                avgScore <= 2 ? '#10b981' :
                avgScore <= 3 ? '#f59e0b' : '#ef4444';
              
              return (
                <>
                  <div 
                    className={styles.threatLevel}
                    style={{ backgroundColor: color }}
                  >
                    {threatLevel}
                  </div>
                  <span className={styles.threatScore}>
                    Average Score: {avgScore.toFixed(1)}
                  </span>
                </>
              );
            })()}
          </div>
        </div>
      </div>

      <div className={styles.actions}>
        <button 
          className={styles.saveButton}
          onClick={saveData}
        >
          Save Assessment
        </button>
        <button 
          className={styles.completeButton}
          onClick={() => {
            if (completionPercentage === 100) {
              saveData();
              // Dispatch phase completion event
              window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
                detail: { phaseId: 'phase1' } 
              }));
              alert('Phase 1 completed! Phase 2 is now unlocked.');
              // Navigate to Phase 2
              setTimeout(() => navigate('/deep-dive/phase2'), 1000);
            } else {
              alert('Please complete all assessments before marking this phase as complete.');
            }
          }}
          disabled={completionPercentage < 100}
        >
          Complete Phase 1
        </button>
        <button 
          className={styles.resetButton}
          onClick={() => {
            if (window.confirm('Are you sure you want to reset all assessments?')) {
              setData({
                industryRivalry: { score: 0, notes: '', factors: [] },
                customerPower: { score: 0, notes: '', factors: [] },
                supplierPower: { score: 0, notes: '', factors: [] },
                substituteThreat: { score: 0, notes: '', factors: [] },
                newEntrantRisk: { score: 0, notes: '', factors: [] },
              });
            }
          }}
        >
          Reset All
        </button>
      </div>
    </div>
  );
};

export default ExternalReality;