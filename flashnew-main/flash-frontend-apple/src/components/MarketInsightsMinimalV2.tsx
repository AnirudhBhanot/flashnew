import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styles from './MarketInsightsMinimal.module.scss';

interface MarketData {
  tam: string;
  growth: string;
  competition: string;
  trends: string[];
  opportunities: string[];
  risks: string[];
}

const marketDataByIndustry: Record<string, MarketData> = {
  saas: {
    tam: '$195B',
    growth: '18.7%',
    competition: 'High',
    trends: [
      'AI/ML integration becoming table stakes',
      'Vertical SaaS gaining momentum',
      'PLG motion dominating go-to-market'
    ],
    opportunities: [
      'Industry-specific solutions',
      'AI-powered automation',
      'Enterprise consolidation plays'
    ],
    risks: [
      'Market saturation in horizontal tools',
      'Increasing CAC across channels',
      'Shorter vendor evaluation cycles'
    ]
  },
  fintech: {
    tam: '$310B',
    growth: '23.8%',
    competition: 'Very High',
    trends: [
      'Embedded finance expanding rapidly',
      'Regulatory compliance as competitive advantage',
      'B2B payments modernization'
    ],
    opportunities: [
      'Cross-border payment solutions',
      'SMB financial automation',
      'Crypto/DeFi infrastructure'
    ],
    risks: [
      'Regulatory uncertainty',
      'Incumbent bank partnerships',
      'Cybersecurity requirements'
    ]
  },
  healthtech: {
    tam: '$280B',
    growth: '15.2%',
    competition: 'Medium',
    trends: [
      'Telemedicine normalization post-COVID',
      'AI diagnostics gaining FDA approvals',
      'Value-based care adoption'
    ],
    opportunities: [
      'Mental health platforms',
      'Senior care technology',
      'Clinical trial optimization'
    ],
    risks: [
      'Long sales cycles',
      'HIPAA compliance complexity',
      'Reimbursement challenges'
    ]
  },
  marketplace: {
    tam: '$120B',
    growth: '12.5%',
    competition: 'High',
    trends: [
      'B2B marketplaces growing faster than B2C',
      'Managed marketplaces commanding premium',
      'Supply chain transparency demands'
    ],
    opportunities: [
      'Niche B2B verticals',
      'Service marketplaces',
      'Sustainability-focused platforms'
    ],
    risks: [
      'Chicken-and-egg problem',
      'Disintermediation risk',
      'Unit economics challenges'
    ]
  }
};

export const MarketInsightsMinimalV2: React.FC = () => {
  const [selectedIndustry, setSelectedIndustry] = useState<string>('saas');
  const [selectedTab, setSelectedTab] = useState<string>('overview');

  const currentMarket = marketDataByIndustry[selectedIndustry];

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Market Insights</h3>
      <p className={styles.subtitle}>
        Industry trends and market dynamics
      </p>

      {/* Industry Selection */}
      <div className={styles.industryTabs}>
        {Object.keys(marketDataByIndustry).map(industry => (
          <button
            key={industry}
            className={`${styles.industryTab} ${selectedIndustry === industry ? styles.active : ''}`}
            onClick={() => setSelectedIndustry(industry)}
          >
            {industry.toUpperCase()}
          </button>
        ))}
      </div>

      {/* Content Tabs */}
      <div className={styles.contentTabs}>
        {['overview', 'trends', 'opportunities', 'risks'].map(tab => (
          <button
            key={tab}
            className={`${styles.contentTab} ${selectedTab === tab ? styles.active : ''}`}
            onClick={() => setSelectedTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <motion.div
        key={selectedTab + selectedIndustry}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={styles.content}
      >
        {selectedTab === 'overview' && (
          <div className={styles.overview}>
            <div className={styles.metricGrid}>
              <div className={styles.metricCard}>
                <span className={styles.metricLabel}>Total Addressable Market</span>
                <span className={styles.metricValue}>{currentMarket.tam}</span>
              </div>
              <div className={styles.metricCard}>
                <span className={styles.metricLabel}>Annual Growth Rate</span>
                <span className={styles.metricValue}>{currentMarket.growth}</span>
              </div>
              <div className={styles.metricCard}>
                <span className={styles.metricLabel}>Competition Level</span>
                <span className={styles.metricValue}>{currentMarket.competition}</span>
              </div>
            </div>

            <div className={styles.insight}>
              <p>
                The {selectedIndustry.toUpperCase()} market shows {
                  parseFloat(currentMarket.growth) > 20 ? 'exceptional' :
                  parseFloat(currentMarket.growth) > 15 ? 'strong' :
                  'moderate'
                } growth potential with a {currentMarket.tam} TAM.
              </p>
            </div>
          </div>
        )}

        {selectedTab === 'trends' && (
          <div className={styles.list}>
            {currentMarket.trends.map((trend, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={styles.listItem}
              >
                <span className={styles.listNumber}>{index + 1}</span>
                <span className={styles.listText}>{trend}</span>
              </motion.div>
            ))}
          </div>
        )}

        {selectedTab === 'opportunities' && (
          <div className={styles.list}>
            {currentMarket.opportunities.map((opportunity, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={styles.listItem}
              >
                <span className={styles.listBullet}>→</span>
                <span className={styles.listText}>{opportunity}</span>
              </motion.div>
            ))}
          </div>
        )}

        {selectedTab === 'risks' && (
          <div className={styles.list}>
            {currentMarket.risks.map((risk, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={styles.listItem}
              >
                <span className={styles.listBullet}>!</span>
                <span className={styles.listText}>{risk}</span>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>

      {/* Market Position */}
      <div className={styles.position}>
        <h4 className={styles.positionTitle}>Your Market Position</h4>
        <p className={styles.positionText}>
          Based on your assessment, you're positioned in a {currentMarket.competition.toLowerCase()} competition market 
          with {currentMarket.growth} annual growth. Focus on differentiation through unique value propositions 
          and consider the market trends when planning your go-to-market strategy.
        </p>
      </div>
    </div>
  );
};