import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button, TextField, Select } from '../design-system/components';
import { Icon } from '../design-system/components';
import { apiService } from '../services/api';
import useAssessmentStore from '../store/assessmentStore';
import { RadarChart } from './charts';
import styles from './WhatIfAnalysis.module.scss';

interface Improvement {
  id: string;
  description: string;
  camp_area: 'capital' | 'advantage' | 'market' | 'people';
}

interface WhatIfResult {
  new_probability: {
    value: number;
    lower: number;
    upper: number;
  };
  new_scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  score_changes: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  timeline: string;
  risks: string[];
  priority: string;
  reasoning: string;
}

const predefinedImprovements = {
  capital: [
    { id: 'reduce_burn', description: 'Reduce burn rate by 30%' },
    { id: 'raise_funding', description: 'Raise Series A funding ($5M)' },
    { id: 'increase_revenue', description: 'Double revenue in 6 months' },
    { id: 'improve_margin', description: 'Improve gross margin to 80%' }
  ],
  advantage: [
    { id: 'file_patents', description: 'File 3 key patents' },
    { id: 'build_network', description: 'Implement network effects' },
    { id: 'tech_upgrade', description: 'Major technology platform upgrade' },
    { id: 'exclusive_partnership', description: 'Secure exclusive partnership' }
  ],
  market: [
    { id: 'expand_tam', description: 'Expand to adjacent market' },
    { id: 'increase_growth', description: 'Achieve 20% MoM growth' },
    { id: 'reduce_competition', description: 'Differentiate from competitors' },
    { id: 'improve_retention', description: 'Increase retention to 95%' }
  ],
  people: [
    { id: 'hire_vp_sales', description: 'Hire VP of Sales' },
    { id: 'hire_cto', description: 'Hire experienced CTO' },
    { id: 'add_advisors', description: 'Add 3 industry advisors' },
    { id: 'expand_team', description: 'Double engineering team' }
  ]
};

const WhatIfAnalysis: React.FC = () => {
  const { data: assessmentData, results } = useAssessmentStore();
  const [selectedImprovements, setSelectedImprovements] = useState<Improvement[]>([]);
  const [customImprovement, setCustomImprovement] = useState('');
  const [selectedArea, setSelectedArea] = useState<string>('capital');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<WhatIfResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAddImprovement = (improvement: Omit<Improvement, 'id'> & { id?: string }) => {
    const newImprovement: Improvement = {
      id: improvement.id || `custom_${Date.now()}`,
      description: improvement.description,
      camp_area: improvement.camp_area
    };
    
    if (selectedImprovements.length < 5) {
      setSelectedImprovements([...selectedImprovements, newImprovement]);
    }
  };

  const handleRemoveImprovement = (id: string) => {
    setSelectedImprovements(selectedImprovements.filter(imp => imp.id !== id));
  };

  const handleAddCustom = () => {
    if (customImprovement.trim()) {
      handleAddImprovement({
        description: customImprovement,
        camp_area: selectedArea as any
      });
      setCustomImprovement('');
    }
  };

  const analyzeScenario = async () => {
    if (selectedImprovements.length === 0) return;

    setIsAnalyzing(true);
    setError(null);

    try {
      // Call the what-if API endpoint
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/analysis/whatif/dynamic`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(process.env.REACT_APP_API_KEY ? { 'X-API-Key': process.env.REACT_APP_API_KEY } : {})
        },
        body: JSON.stringify({
          startup_data: apiService.transformAssessmentToAPI(assessmentData),
          current_scores: {
            capital: results?.scores?.capital || 0.5,
            advantage: results?.scores?.advantage || 0.5,
            market: results?.scores?.market || 0.5,
            people: results?.scores?.people || 0.5,
            success_probability: results?.successProbability || 0.5
          },
          improvements: selectedImprovements
        })
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const result = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError('Failed to analyze scenario. Please try again.');
      console.error('What-if analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const currentScores = results?.scores || { capital: 0.5, advantage: 0.5, market: 0.5, people: 0.5 };
  const comparisonData = analysisResult ? [
    { name: 'Current', values: currentScores },
    { name: 'Projected', values: analysisResult.new_scores }
  ] : null;

  return (
    <div className={styles.container}>
      <div className={styles.mainCard}>
        <div className={styles.header}>
          <h2 className={styles.title}>What-If Scenario Analysis</h2>
          <p className={styles.subtitle}>
            Test how specific improvements could impact your startup's success
          </p>
        </div>

        <div className={styles.improvementSection}>
          <h3 className={styles.sectionTitle}>Select Improvements to Test</h3>
          
          {/* Selected Improvements */}
          <AnimatePresence>
            {selectedImprovements.length > 0 && (
              <motion.div 
                className={styles.selectedList}
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                {selectedImprovements.map((improvement, index) => (
                  <motion.div
                    key={improvement.id}
                    className={styles.selectedItem}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <span className={styles.improvementNumber}>{index + 1}</span>
                    <div className={styles.improvementContent}>
                      <p className={styles.improvementText}>{improvement.description}</p>
                      <span className={styles.improvementArea}>{improvement.camp_area}</span>
                    </div>
                    <Button
                      variant="secondary"
                      size="small"
                      onClick={() => handleRemoveImprovement(improvement.id)}
                      icon={<Icon name="xmark" />}
                    />
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Add Improvements */}
          <div className={styles.addSection}>
            <div className={styles.tabs}>
              {Object.keys(predefinedImprovements).map(area => (
                <button
                  key={area}
                  className={`${styles.tab} ${selectedArea === area ? styles.active : ''}`}
                  onClick={() => setSelectedArea(area)}
                >
                  {area.charAt(0).toUpperCase() + area.slice(1)}
                </button>
              ))}
            </div>

            <div className={styles.improvementOptions}>
              {predefinedImprovements[selectedArea as keyof typeof predefinedImprovements].map(improvement => (
                <motion.button
                  key={improvement.id}
                  className={styles.improvementOption}
                  onClick={() => handleAddImprovement({ ...improvement, camp_area: selectedArea as any })}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  disabled={selectedImprovements.some(imp => imp.id === improvement.id)}
                >
                  <Icon name="plus.circle" size={20} />
                  <span>{improvement.description}</span>
                </motion.button>
              ))}
            </div>

            {/* Custom Improvement */}
            <div className={styles.customSection}>
              <TextField
                label="Custom Improvement"
                value={customImprovement}
                onChange={(value) => setCustomImprovement(value)}
                placeholder="Add custom improvement..."
              />
              <Button
                variant="secondary"
                onClick={handleAddCustom}
                disabled={!customImprovement.trim()}
              >
                Add Custom
              </Button>
            </div>
          </div>

          {/* Analyze Button */}
          {selectedImprovements.length > 0 && (
            <motion.div 
              className={styles.analyzeSection}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <Button
                variant="primary"
                size="large"
                onClick={analyzeScenario}
                loading={isAnalyzing}
                disabled={selectedImprovements.length === 0}
                icon={<Icon name="chart.line.uptrend" />}
              >
                Analyze Scenario ({selectedImprovements.length} improvements)
              </Button>
            </motion.div>
          )}
        </div>

        {/* Results */}
        {analysisResult && (
          <motion.div 
            className={styles.results}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h3 className={styles.resultsTitle}>Projected Impact</h3>

            {/* Success Probability Change */}
            <div className={styles.probabilityChange}>
              <div className={styles.metric}>
                <span className={styles.label}>Current Success Probability</span>
                <span className={styles.value}>{(results?.successProbability || 0.5) * 100}%</span>
              </div>
              <Icon name="arrow.right" size={24} className={styles.arrow} />
              <div className={styles.metric}>
                <span className={styles.label}>Projected Success Probability</span>
                <span className={styles.value}>{(analysisResult.new_probability.value * 100).toFixed(0)}%</span>
                <span className={styles.range}>
                  ({(analysisResult.new_probability.lower * 100).toFixed(0)}% - 
                  {(analysisResult.new_probability.upper * 100).toFixed(0)}%)
                </span>
              </div>
            </div>

            {/* Score Comparison */}
            {comparisonData && (
              <div className={styles.chartSection}>
                <h4>CAMP Score Comparison</h4>
                <RadarChart
                  data={comparisonData}
                  height={300}
                  showLegend={true}
                />
              </div>
            )}

            {/* Timeline & Risks */}
            <div className={styles.insights}>
              <div className={styles.insightCard}>
                <Icon name="clock" size={20} />
                <div>
                  <h5>Implementation Timeline</h5>
                  <p>{analysisResult.timeline}</p>
                </div>
              </div>

              <div className={styles.insightCard}>
                <Icon name="exclamationmark.triangle" size={20} />
                <div>
                  <h5>Key Risks</h5>
                  <ul>
                    {analysisResult.risks.map((risk, index) => (
                      <li key={index}>{risk}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Reasoning */}
            {analysisResult.reasoning && (
              <div className={styles.reasoning}>
                <h5>Analysis Reasoning</h5>
                <p>{analysisResult.reasoning}</p>
              </div>
            )}
          </motion.div>
        )}

        {error && (
          <motion.div 
            className={styles.error}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <Icon name="exclamationmark.circle" size={20} />
            <p>{error}</p>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export { WhatIfAnalysis };