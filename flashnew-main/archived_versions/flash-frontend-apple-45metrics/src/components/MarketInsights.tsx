import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '../design-system/components';
import { Icon } from '../design-system/components';
import useAssessmentStore from '../store/assessmentStore';
import styles from './MarketInsights.module.scss';

interface MarketInsightsData {
  market_trends: string[];
  funding_climate: string;
  recent_exits: string[];
  opportunities: string[];
  competitors: string[];
  investment_thesis: string;
}

const MarketInsights: React.FC = () => {
  const { data: assessmentData } = useAssessmentStore();
  const [insights, setInsights] = useState<MarketInsightsData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const fetchInsights = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/analysis/insights/market`,
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
              tam_size_usd: assessmentData?.market?.marketSize || 0
            }
          })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch market insights');
      }

      const data = await response.json();
      setInsights(data);
      setIsExpanded(true);
    } catch (err) {
      console.error('Market insights error:', err);
      setError('Failed to generate market insights');
      // Set fallback data
      setInsights({
        market_trends: [
          'Increasing focus on AI/ML integration across industries',
          'Growing emphasis on sustainability and ESG metrics',
          'Remote-first business models becoming permanent'
        ],
        funding_climate: 'Cautious optimism with increased due diligence and focus on profitability',
        recent_exits: [
          'Similar Company A - $500M acquisition by major tech firm',
          'Competitor B - Series D at $1.2B valuation',
          'Industry peer C - IPO at $2B market cap'
        ],
        opportunities: [
          'Expansion into adjacent markets with similar customer profiles',
          'Strategic partnerships with enterprise clients',
          'International expansion in emerging markets'
        ],
        competitors: [
          'Market Leader X (strength: brand recognition)',
          'Fast-growing Startup Y (strength: innovation speed)',
          'Traditional Player Z (strength: enterprise relationships)'
        ],
        investment_thesis: 'Strong team with relevant experience, addressing a growing market need with defensible technology'
      });
      setIsExpanded(true);
    } finally {
      setIsLoading(false);
    }
  };

  const getSectorIcon = (sector: string) => {
    const iconMap: { [key: string]: string } = {
      'saas': 'cloud',
      'fintech': 'dollarsign.circle',
      'healthtech': 'heart.circle',
      'edtech': 'book.circle',
      'ecommerce': 'cart',
      'marketplace': 'bag',
      'deeptech': 'cpu',
      'consumer': 'person.2',
      'enterprise': 'building.2',
      'proptech': 'house',
      'biotech': 'leaf',
      'agtech': 'leaf.circle',
      'cleantech': 'bolt.circle',
      'cybersecurity': 'lock.shield',
      'gaming': 'gamecontroller',
      'logistics': 'shippingbox',
      'insurtech': 'shield',
      'legaltech': 'book.closed',
      'hrtech': 'person.3'
    };
    return iconMap[sector] || 'star';
  };

  const sector = assessmentData?.companyInfo?.industry || 'tech';
  const stage = assessmentData?.companyInfo?.stage || 'seed';

  return (
    <div className={styles.container}>
      <div className={styles.mainCard}>
        <div className={styles.header}>
          <div className={styles.iconWrapper}>
            <Icon name={getSectorIcon(sector)} size={32} />
          </div>
          <div className={styles.headerContent}>
            <h2 className={styles.title}>Market Intelligence</h2>
            <p className={styles.subtitle}>
              Current insights for {stage} {sector} startups
            </p>
          </div>
        </div>

        {!insights && !isLoading && (
          <motion.div 
            className={styles.prompt}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className={styles.promptText}>
              Get real-time market intelligence specific to your industry and stage
            </p>
            <Button
              variant="primary"
              size="large"
              onClick={fetchInsights}
              loading={isLoading}
              icon={<Icon name="chart.line.uptrend" />}
            >
              Analyze Market
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
            <p>Analyzing market conditions...</p>
          </motion.div>
        )}

        <AnimatePresence>
          {insights && isExpanded && (
            <motion.div 
              className={styles.content}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.5 }}
            >
              {/* Market Trends */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="chart.line.uptrend" size={20} />
                  <h3>Current Market Trends</h3>
                </div>
                <div className={styles.trendsList}>
                  {insights.market_trends.map((trend, index) => (
                    <motion.div
                      key={index}
                      className={styles.trendItem}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <span className={styles.trendNumber}>{index + 1}</span>
                      <p>{trend}</p>
                    </motion.div>
                  ))}
                </div>
              </section>

              {/* Funding Climate */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="dollarsign.circle" size={20} />
                  <h3>Funding Climate</h3>
                </div>
                <div className={styles.climateCard}>
                  <p>{insights.funding_climate}</p>
                </div>
              </section>

              {/* Recent Exits */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="arrow.up.right.circle" size={20} />
                  <h3>Recent Exits & Funding</h3>
                </div>
                <div className={styles.exitsList}>
                  {insights.recent_exits.map((exit, index) => (
                    <motion.div
                      key={index}
                      className={styles.exitItem}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Icon name="checkmark.circle.fill" size={16} />
                      <p>{exit}</p>
                    </motion.div>
                  ))}
                </div>
              </section>

              {/* Opportunities */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="lightbulb" size={20} />
                  <h3>Market Opportunities</h3>
                </div>
                <div className={styles.opportunitiesGrid}>
                  {insights.opportunities.map((opportunity, index) => (
                    <motion.div
                      key={index}
                      className={styles.opportunityCard}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 }}
                      whileHover={{ scale: 1.02 }}
                    >
                      <Icon name="arrow.up.forward" size={16} />
                      <p>{opportunity}</p>
                    </motion.div>
                  ))}
                </div>
              </section>

              {/* Competitive Landscape */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="person.2.circle" size={20} />
                  <h3>Competitive Landscape</h3>
                </div>
                <div className={styles.competitorsList}>
                  {insights.competitors.map((competitor, index) => (
                    <motion.div
                      key={index}
                      className={styles.competitorItem}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className={styles.competitorIcon}>
                        <Icon name="building.2" size={16} />
                      </div>
                      <p>{competitor}</p>
                    </motion.div>
                  ))}
                </div>
              </section>

              {/* Investment Thesis */}
              <section className={styles.section}>
                <div className={styles.sectionHeader}>
                  <Icon name="doc.text" size={20} />
                  <h3>Investment Thesis</h3>
                </div>
                <div className={styles.thesisCard}>
                  <p>{insights.investment_thesis}</p>
                </div>
              </section>
            </motion.div>
          )}
        </AnimatePresence>

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

export { MarketInsights };