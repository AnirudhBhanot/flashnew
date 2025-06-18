import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicFrameworkReportIntelligent.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface Framework {
  framework_id: string;
  framework_name: string;
  category: string;
  relevance_score: number;
  confidence_level: number;
  success_probability: number;
  customizations: string[];
  quick_wins: string[];
  risk_factors: string[];
  analysis: any;
}

const StrategicFrameworkReportIntelligentSimple: React.FC = () => {
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState<string>('');
  const assessmentData = useAssessmentStore(state => state.data);

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/frameworks/intelligent-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assessment_data: assessmentData || {
            capital: { fundingStage: 'seed' },
            market: { sector: 'saas' },
            people: { fullTimeEmployees: 10 }
          },
          max_frameworks: 4,
          include_market_intelligence: false
        })
      });

      if (response.ok) {
        const data = await response.json();
        setFrameworks(data.frameworks || []);
        if (data.frameworks?.length > 0) {
          setSelectedFramework(data.frameworks[0].framework_id);
        }
      } else {
        // Use mock data as fallback
        setFrameworks([
          {
            framework_id: 'swot',
            framework_name: 'SWOT Analysis',
            category: 'Strategy',
            relevance_score: 0.85,
            confidence_level: 0.80,
            success_probability: 0.75,
            customizations: [
              'Focus on quantified metrics for each SWOT element',
              'Prioritize weaknesses that can become strengths'
            ],
            quick_wins: [
              'Map top 3 strengths to revenue opportunities this week',
              'Convert one weakness into action plan'
            ],
            risk_factors: ['Analysis paralysis', 'Generic insights'],
            analysis: {
              strengths: ['Strong team', 'Good runway', 'Product-market fit signals'],
              weaknesses: ['Limited resources', 'High competition'],
              opportunities: ['Growing market', 'AI transformation'],
              threats: ['Funding environment', 'New entrants']
            }
          }
        ]);
        setSelectedFramework('swot');
      }
    } catch (error) {
      console.error('Error loading analysis:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Analyzing strategic frameworks...</p>
        </div>
      </div>
    );
  }

  const selected = frameworks.find(f => f.framework_id === selectedFramework);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Intelligent Strategic Framework Analysis</h2>
        <p>AI-powered framework selection tailored to your startup</p>
      </div>

      <div className={styles.frameworkSelector}>
        {frameworks.map(framework => (
          <button
            key={framework.framework_id}
            className={`${styles.frameworkTab} ${
              selectedFramework === framework.framework_id ? styles.active : ''
            }`}
            onClick={() => setSelectedFramework(framework.framework_id)}
          >
            <div className={styles.tabHeader}>
              <span className={styles.frameworkName}>{framework.framework_name}</span>
              <span className={styles.frameworkCategory}>{framework.category}</span>
            </div>
            <div className={styles.tabScores}>
              <span className={styles.relevanceScore}>
                {(framework.relevance_score * 100).toFixed(0)}% relevant
              </span>
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div className={styles.frameworkDetail}>
          <div className={styles.intelligenceScores}>
            <div className={styles.scoreCard}>
              <label>Success Probability</label>
              <div className={styles.scoreBar}>
                <div 
                  className={styles.scoreProgress} 
                  style={{ width: `${selected.success_probability * 100}%` }}
                />
              </div>
              <span>{(selected.success_probability * 100).toFixed(0)}%</span>
            </div>
          </div>

          <div className={styles.customizations}>
            <h4>Customizations for Your Startup</h4>
            {selected.customizations.map((custom, i) => (
              <div key={i} className={styles.customizationItem}>
                <span className={styles.customNumber}>{i + 1}</span>
                <p>{custom}</p>
              </div>
            ))}
          </div>

          <div className={styles.quickWinsSection}>
            <h4>Quick Wins This Week</h4>
            <div className={styles.quickWinsGrid}>
              {selected.quick_wins.map((win, i) => (
                <div key={i} className={styles.quickWinCard}>
                  <p>{win}</p>
                </div>
              ))}
            </div>
          </div>

          {selected.analysis && (
            <div className={styles.frameworkAnalysis}>
              <h4>Analysis Details</h4>
              <pre>{JSON.stringify(selected.analysis, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default StrategicFrameworkReportIntelligentSimple;