import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { configService } from '../../services/LegacyConfigService';
import { STAGE_WEIGHTS, COMPANY_EXAMPLES } from '../../config/constants';
import './WeightageExplanation.css';

interface WeightageExplanationProps {
  currentStage: string;
  pillarScores: Record<string, number>;
}

export const WeightageExplanation: React.FC<WeightageExplanationProps> = ({ 
  currentStage, 
  pillarScores 
}) => {
  const [stageWeights, setStageWeights] = useState(STAGE_WEIGHTS);
  const [companyExamples, setCompanyExamples] = useState(COMPANY_EXAMPLES);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const [weights, examples] = await Promise.all([
          configService.getStageWeights(),
          configService.getCompanyExamples()
        ]);
        setStageWeights(weights);
        setCompanyExamples(examples);
      } catch (error) {
        // Falls back to constants already set as defaults
      } finally {
        setIsLoading(false);
      }
    };
    loadConfig();
  }, []);


  // Generate stage explanations dynamically based on weights
  const getStageExplanations = () => {
    const explanations: Record<string, { focus: string; rationale: string; example: string }> = {};
    
    Object.entries(stageWeights).forEach(([stage, weights]) => {
      // Find the highest weighted pillar(s)
      const sortedPillars = Object.entries(weights).sort((a, b) => b[1] - a[1]);
      const topWeight = sortedPillars[0][1];
      const topPillars = sortedPillars.filter(([_, weight]) => weight === topWeight);
      
      let focus: string;
      if (topPillars.length === 1) {
        const pillarName = topPillars[0][0].charAt(0).toUpperCase() + topPillars[0][0].slice(1);
        focus = `${pillarName} (${Math.round(topWeight * 100)}%)`;
      } else {
        const pillarNames = topPillars.map(([pillar]) => 
          pillar.charAt(0).toUpperCase() + pillar.slice(1)
        ).join(' & ');
        focus = `${pillarNames} (${Math.round(topWeight * 100)}% each)`;
      }
      
      // Get rationale based on stage
      const rationales: Record<string, string> = {
        pre_seed: "At pre-seed, execution capability is everything. A great team can pivot, adapt, and find product-market fit.",
        seed: "Balance between strong execution and unique product differentiation. Early traction validates the concept.",
        series_a: "Product-market fit must be proven. The market size and growth potential become critical for scaling.",
        series_b: "Focus shifts to capturing significant market share and proving scalable unit economics.",
        series_c: "Path to profitability becomes paramount. Investors want to see sustainable business models.",
        growth: "Must demonstrate clear path to profitability and efficient capital deployment for expansion."
      };
      
      explanations[stage] = {
        focus,
        rationale: rationales[stage] || rationales.growth,
        example: companyExamples[stage as keyof typeof companyExamples] ? 
          `Example: ${companyExamples[stage as keyof typeof companyExamples].story}` : 
          "Example: Leading companies at this stage focus on key metrics."
      };
    });
    
    return explanations;
  };
  
  const stageExplanations = getStageExplanations();

  const getPillarDescription = (pillar: string) => {
    const descriptions: Record<string, { title: string; subtitle: string; metrics: string[] }> = {
      capital: {
        title: "Capital",
        subtitle: "Financial Health & Efficiency",
        metrics: ["Burn rate vs. growth", "Runway length", "Revenue per dollar spent", "Gross margins", "LTV/CAC ratio"]
      },
      advantage: {
        title: "Advantage",
        subtitle: "Competitive Moat & Differentiation", 
        metrics: ["Patent portfolio", "Network effects", "Brand strength", "Switching costs", "Technical differentiation"]
      },
      market: {
        title: "Market",
        subtitle: "TAM Size & Growth Dynamics",
        metrics: ["TAM/SAM/SOM size", "Market growth rate", "Customer concentration", "Competitive landscape", "Market timing"]
      },
      people: {
        title: "People",
        subtitle: "Team Strength & Experience",
        metrics: ["Founder experience", "Domain expertise", "Previous exits", "Team completeness", "Advisory board"]
      }
    };
    return descriptions[pillar] || { title: pillar, subtitle: "", metrics: [] };
  };

  const currentWeights = stageWeights[currentStage as keyof typeof stageWeights] || stageWeights.seed;
  const stageInfo = stageExplanations[currentStage as keyof typeof stageExplanations] || stageExplanations.seed;

  // Calculate weighted score
  const weightedScore = Object.entries(pillarScores).reduce((sum, [pillar, score]) => {
    return sum + (score * (currentWeights[pillar as keyof typeof currentWeights] || 0));
  }, 0);

  if (isLoading) {
    return (
      <div className="weightage-explanation loading">
        <div className="loading-spinner">Loading configuration...</div>
      </div>
    );
  }

  return (
    <motion.div 
      className="weightage-explanation"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="explanation-header">
        <h2>How Your Score is Calculated</h2>
        <p className="explanation-subtitle">
          FLASH uses stage-specific weightings because different factors matter at different stages of growth
        </p>
      </div>

      {/* Current Stage Focus */}
      <div className="stage-focus-card">
        <div className="stage-badge">
          {currentStage.replace(/_/g, ' ').toUpperCase()}
        </div>
        <h3>{stageInfo.focus}</h3>
        <p className="stage-rationale">{stageInfo.rationale}</p>
        <div className="stage-example">
          <span className="example-icon">💡</span>
          <p>{stageInfo.example}</p>
        </div>
      </div>

      {/* Weightage Breakdown */}
      <div className="weightage-grid">
        {Object.entries(currentWeights)
          .sort((a, b) => (b[1] as number) - (a[1] as number))
          .map(([pillar, weight]) => {
            const score = pillarScores[pillar] || 0;
            const contribution = score * (weight as number);
            const pillarInfo = getPillarDescription(pillar);
            
            return (
              <motion.div 
                key={pillar}
                className="weightage-card"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 }}
              >
                <div className="weightage-header">
                  <h4>{pillarInfo.title}</h4>
                  {pillarInfo.subtitle && <p className="pillar-subtitle">{pillarInfo.subtitle}</p>}
                  <div className="weight-badge">{Math.round((weight as number) * 100)}% weight</div>
                </div>
                
                <div className="score-calculation">
                  <div className="score-parts">
                    <span className="part-label">Your Score</span>
                    <span className="part-value">{Math.round(score * 100)}%</span>
                  </div>
                  <span className="multiply">×</span>
                  <div className="score-parts">
                    <span className="part-label">Weight</span>
                    <span className="part-value">{Math.round((weight as number) * 100)}%</span>
                  </div>
                  <span className="equals">=</span>
                  <div className="score-parts highlighted">
                    <span className="part-label">Contribution</span>
                    <span className="part-value">{(contribution * 100).toFixed(1)}%</span>
                  </div>
                </div>

                <div className="metrics-measured">
                  <p className="metrics-title">What we measure:</p>
                  <ul>
                    {pillarInfo.metrics.map((metric, i) => (
                      <li key={i}>{metric}</li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            );
          })}
      </div>

      {/* Final Calculation */}
      <div className="final-calculation">
        <h3>Your Final Weighted Score</h3>
        <div className="calculation-display">
          <span className="final-score">{(weightedScore * 100).toFixed(1)}%</span>
          <span className="score-description">
            Combined score across all weighted pillars
          </span>
        </div>
      </div>

      {/* Stage Progression */}
      <div className="stage-progression">
        <h3>How Weightings Change by Stage</h3>
        <div className="progression-chart">
          {Object.entries(stageWeights).map(([stage, weights]) => (
            <div 
              key={stage} 
              className={`stage-column ${stage === currentStage ? 'current' : ''}`}
            >
              <h4>{stage.replace(/_/g, ' ').toUpperCase()}</h4>
              <div className="weight-bars">
                {Object.entries(weights)
                  .sort((a, b) => b[1] - a[1])
                  .map(([pillar, weight]) => (
                    <div key={pillar} className="weight-bar">
                      <span className="pillar-label">
                        {pillar.charAt(0).toUpperCase() + pillar.slice(1)}
                      </span>
                      <div className="bar-container">
                        <div 
                          className="bar-fill"
                          style={{ width: `${weight * 100}%` }}
                        />
                        <span className="weight-label">{Math.round(weight * 100)}%</span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Insights */}
      <div className="key-insights">
        <h3>Why This Matters</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <span className="insight-icon">🎯</span>
            <h4>Stage-Appropriate Focus</h4>
            <p>VCs evaluate startups differently at each stage. Our algorithm mirrors these real-world investment criteria.</p>
          </div>
          <div className="insight-card">
            <span className="insight-icon">⚖️</span>
            <h4>Balanced Assessment</h4>
            <p>No single factor determines success. The weightings ensure a holistic view appropriate to your stage.</p>
          </div>
          <div className="insight-card">
            <span className="insight-icon">📈</span>
            <h4>Growth Trajectory</h4>
            <p>Understanding how priorities shift helps you prepare for future funding rounds and scaling challenges.</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};