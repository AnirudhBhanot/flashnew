import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AnimatePresence } from '../design-system/components/AnimatePresenceWrapper';
import { Button } from '../design-system/components';
import { Icon } from '../design-system/components';
import useAssessmentStore from '../store/assessmentStore';
import { MultiSeriesRadarChart } from './charts';
import styles from './CompetitorAnalysis.module.scss';

interface Competitor {
  name: string;
  stage: string;
  strengths: string[];
  weaknesses: string[];
  positioning: string;
  funding: string;
  scores?: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
}

interface CompetitorAnalysisData {
  competitors: Competitor[];
  market_positioning: string;
  competitive_advantages: string[];
  threats: string[];
  differentiation_opportunities: string[];
}

const CompetitorAnalysis: React.FC = () => {
  const { data: assessmentData, results } = useAssessmentStore();
  const [analysisData, setAnalysisData] = useState<CompetitorAnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCompetitor, setSelectedCompetitor] = useState<number | null>(null);

  const fetchAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/analysis/competitors/analyze`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(process.env.REACT_APP_API_KEY ? { 'X-API-Key': process.env.REACT_APP_API_KEY } : {})
          },
          body: JSON.stringify({
            startup_data: {
              sector: assessmentData?.companyInfo?.industry || 'tech',
              funding_stage: assessmentData?.companyInfo?.stage || 'seed',
              annual_revenue_run_rate: assessmentData?.capital?.annualRevenueRunRate || 0,
              tam_size_usd: assessmentData?.market?.marketSize || 0,
              unique_advantages: assessmentData?.advantage?.advantages || []
            },
            top_n: 5
          })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to analyze competitors');
      }

      const data = await response.json();
      
      // Generate mock scores for competitors if not provided
      const competitors = data.competitors || [];
      const enhancedCompetitors = competitors.map((comp: Competitor) => ({
        ...comp,
        scores: comp.scores || {
          capital: 0.5 + (Math.random() * 0.4),
          advantage: 0.5 + (Math.random() * 0.4),
          market: 0.5 + (Math.random() * 0.4),
          people: 0.5 + (Math.random() * 0.4)
        }
      }));

      setAnalysisData({
        ...data,
        competitors: enhancedCompetitors
      });
    } catch (err) {
      console.error('Competitor analysis error:', err);
      setError('Failed to analyze competitors');
      
      // Set fallback data
      setAnalysisData({
        competitors: [
          {
            name: "TechCorp Solutions",
            stage: "Series B",
            strengths: ["Market leader position", "Strong engineering team", "Enterprise relationships"],
            weaknesses: ["High burn rate", "Complex product", "Slow innovation"],
            positioning: "Enterprise-focused premium solution",
            funding: "$45M raised",
            scores: { capital: 0.75, advantage: 0.85, market: 0.9, people: 0.8 }
          },
          {
            name: "FastStart AI",
            stage: "Series A",
            strengths: ["Rapid growth", "AI-first approach", "Strong marketing"],
            weaknesses: ["Limited runway", "Small team", "Narrow focus"],
            positioning: "AI-powered automation for SMBs",
            funding: "$12M raised",
            scores: { capital: 0.6, advantage: 0.7, market: 0.75, people: 0.65 }
          },
          {
            name: "SimpleTech",
            stage: "Seed",
            strengths: ["Low cost structure", "Easy to use", "Good customer support"],
            weaknesses: ["Limited features", "No moat", "Small market share"],
            positioning: "Budget-friendly solution for startups",
            funding: "$2M raised",
            scores: { capital: 0.5, advantage: 0.45, market: 0.55, people: 0.5 }
          }
        ],
        market_positioning: "Mid-market challenger with strong technical differentiation",
        competitive_advantages: [
          "Superior technology architecture",
          "Better user experience",
          "More flexible pricing model",
          "Faster implementation time"
        ],
        threats: [
          "Established competitors with deeper pockets",
          "Potential new entrants with VC backing",
          "Platform consolidation by major players"
        ],
        differentiation_opportunities: [
          "Focus on underserved vertical markets",
          "Build strategic partnerships",
          "Develop unique IP and patents",
          "Create network effects through marketplace"
        ]
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getComparisonData = () => {
    if (!analysisData || !results?.scores) return null;
    
    const data = [
      {
        name: 'Your Startup',
        values: {
          Capital: results.scores.capital || 0,
          Advantage: results.scores.advantage || 0,
          Market: results.scores.market || 0,
          People: results.scores.people || 0
        }
      }
    ];

    analysisData.competitors.forEach(comp => {
      if (comp.scores) {
        data.push({
          name: comp.name,
          values: {
            Capital: comp.scores.capital,
            Advantage: comp.scores.advantage,
            Market: comp.scores.market,
            People: comp.scores.people
          }
        });
      }
    });

    return data;
  };

  return (
    <div className={styles.container}>
      <div className={styles.mainCard}>
        <div className={styles.header}>
          <h2 className={styles.title}>Competitive Landscape Analysis</h2>
          <p className={styles.subtitle}>
            Understand your position relative to key competitors
          </p>
        </div>

        {!analysisData && !isLoading && (
          <motion.div 
            className={styles.prompt}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className={styles.promptIcon}>
              <Icon name="person.2.circle" size={48} />
            </div>
            <p className={styles.promptText}>
              Identify and analyze similar companies in your space
            </p>
            <Button
              variant="primary"
              size="large"
              onClick={fetchAnalysis}
              loading={isLoading}
              icon={<Icon name="magnifyingglass" />}
            >
              Analyze Competitors
            </Button>
          </motion.div>
        )}

        {isLoading && (
          <motion.div 
            className={styles.loading}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
            <p>Analyzing competitive landscape...</p>
          </motion.div>
        )}

        {analysisData && (
          <motion.div 
            className={styles.content}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {/* Radar Chart Comparison */}
            {getComparisonData() && (
              <section className={styles.chartSection}>
                <h3>CAMP Score Comparison</h3>
                <MultiSeriesRadarChart
                  data={getComparisonData()!}
                  size={400}
                />
              </section>
            )}

            {/* Competitors List */}
            <section className={styles.competitorsSection}>
              <h3>Key Competitors</h3>
              <div className={styles.competitorsList}>
                {analysisData.competitors && analysisData.competitors.map((competitor, index) => (
                  <motion.div
                    key={index}
                    className={`${styles.competitorCard} ${selectedCompetitor === index ? styles.selected : ''}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => setSelectedCompetitor(selectedCompetitor === index ? null : index)}
                    whileHover={{ scale: 1.02 }}
                  >
                    <div className={styles.competitorHeader}>
                      <div className={styles.competitorInfo}>
                        <h4>{competitor.name}</h4>
                        <div className={styles.competitorMeta}>
                          <span className={styles.stage}>{competitor.stage}</span>
                          <span className={styles.funding}>{competitor.funding}</span>
                        </div>
                      </div>
                      <Icon 
                        name={selectedCompetitor === index ? "chevron.up" : "chevron.down"} 
                        size={20} 
                      />
                    </div>
                    
                    <AnimatePresence>
                      {selectedCompetitor === index && (
                        <motion.div
                          className={styles.competitorDetails}
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3 }}
                        >
                          <div className={styles.positioning}>
                            <Icon name="target" size={16} />
                            <p>{competitor.positioning}</p>
                          </div>
                          
                          <div className={styles.strengthsWeaknesses}>
                            <div className={styles.strengths}>
                              <h5>Strengths</h5>
                              <ul>
                                {competitor.strengths.map((strength, idx) => (
                                  <li key={idx}>
                                    <Icon name="checkmark.circle.fill" size={14} />
                                    {strength}
                                  </li>
                                ))}
                              </ul>
                            </div>
                            
                            <div className={styles.weaknesses}>
                              <h5>Weaknesses</h5>
                              <ul>
                                {competitor.weaknesses.map((weakness, idx) => (
                                  <li key={idx}>
                                    <Icon name="xmark.circle" size={14} />
                                    {weakness}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                ))}
              </div>
            </section>

            {/* Market Positioning */}
            <section className={styles.positioningSection}>
              <h3>Your Market Position</h3>
              <div className={styles.positioningCard}>
                <Icon name="location.circle" size={24} />
                <p>{analysisData.market_positioning}</p>
              </div>
            </section>

            {/* Competitive Advantages */}
            <section className={styles.advantagesSection}>
              <h3>Your Competitive Advantages</h3>
              <div className={styles.advantagesGrid}>
                {analysisData.competitive_advantages && analysisData.competitive_advantages.map((advantage, index) => (
                  <motion.div
                    key={index}
                    className={styles.advantageCard}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                  >
                    <Icon name="star.fill" size={20} />
                    <p>{advantage}</p>
                  </motion.div>
                ))}
              </div>
            </section>

            {/* Threats & Opportunities */}
            <section className={styles.threatsOpportunitiesSection}>
              <div className={styles.threats}>
                <h3>
                  <Icon name="exclamationmark.triangle" size={20} />
                  Competitive Threats
                </h3>
                <ul>
                  {analysisData.threats && analysisData.threats.map((threat, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      {threat}
                    </motion.li>
                  ))}
                </ul>
              </div>
              
              <div className={styles.opportunities}>
                <h3>
                  <Icon name="lightbulb" size={20} />
                  Differentiation Opportunities
                </h3>
                <ul>
                  {analysisData.differentiation_opportunities && analysisData.differentiation_opportunities.map((opportunity, index) => (
                    <motion.li
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      {opportunity}
                    </motion.li>
                  ))}
                </ul>
              </div>
            </section>
          </motion.div>
        )}

        {error && (
          <motion.div 
            className={styles.error}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Icon name="exclamationmark.triangle" size={24} />
            <p>{error}</p>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export { CompetitorAnalysis };