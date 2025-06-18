import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styles from './CompetitorAnalysisMinimal.module.scss';

interface Competitor {
  name: string;
  stage: string;
  funding: string;
  strengths: string[];
  weaknesses: string[];
  marketShare: number;
}

const competitorData: Record<string, Competitor[]> = {
  saas: [
    {
      name: 'Salesforce',
      stage: 'Public',
      funding: '$0',
      strengths: ['Market leader', 'Enterprise relationships', 'Ecosystem'],
      weaknesses: ['Complex implementation', 'High cost', 'Legacy architecture'],
      marketShare: 23
    },
    {
      name: 'HubSpot',
      stage: 'Public',
      funding: '$0',
      strengths: ['User-friendly', 'Marketing suite', 'SMB focus'],
      weaknesses: ['Limited enterprise features', 'Price scaling', 'Customization'],
      marketShare: 8
    },
    {
      name: 'Monday.com',
      stage: 'Public',
      funding: '$0',
      strengths: ['Visual interface', 'Flexibility', 'Quick adoption'],
      weaknesses: ['Limited depth', 'Performance at scale', 'Integration gaps'],
      marketShare: 4
    }
  ],
  fintech: [
    {
      name: 'Stripe',
      stage: 'Private',
      funding: '$8.7B',
      strengths: ['Developer experience', 'Global reach', 'Innovation'],
      weaknesses: ['Enterprise sales', 'Support scaling', 'Pricing complexity'],
      marketShare: 15
    },
    {
      name: 'Square',
      stage: 'Public',
      funding: '$0',
      strengths: ['SMB ecosystem', 'Hardware integration', 'Brand recognition'],
      weaknesses: ['Enterprise limitations', 'International expansion', 'Margin pressure'],
      marketShare: 12
    },
    {
      name: 'Plaid',
      stage: 'Private',
      funding: '$425M',
      strengths: ['Bank connections', 'Developer tools', 'Market position'],
      weaknesses: ['Regulatory risk', 'Single product', 'Privacy concerns'],
      marketShare: 6
    }
  ]
};

export const CompetitorAnalysisMinimalV2: React.FC = () => {
  const [selectedIndustry, setSelectedIndustry] = useState<string>('saas');
  const [selectedView, setSelectedView] = useState<string>('overview');

  const competitors = competitorData[selectedIndustry] || competitorData.saas;
  
  const yourStartup = {
    name: 'Your Startup',
    strengths: ['Agility', 'Innovation', 'Customer focus'],
    weaknesses: ['Limited resources', 'Brand awareness', 'Scale'],
    opportunities: ['Niche markets', 'New technology', 'Partnerships'],
    threats: ['Competition', 'Market timing', 'Funding']
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Competitor Analysis</h3>
      <p className={styles.subtitle}>
        Understanding your competitive landscape
      </p>

      {/* Industry Selection */}
      <div className={styles.industryTabs}>
        {Object.keys(competitorData).map(industry => (
          <button
            key={industry}
            className={`${styles.industryTab} ${selectedIndustry === industry ? styles.active : ''}`}
            onClick={() => setSelectedIndustry(industry)}
          >
            {industry.toUpperCase()}
          </button>
        ))}
      </div>

      {/* View Toggle */}
      <div className={styles.viewToggle}>
        <button
          className={`${styles.toggle} ${selectedView === 'overview' ? styles.active : ''}`}
          onClick={() => setSelectedView('overview')}
        >
          Overview
        </button>
        <button
          className={`${styles.toggle} ${selectedView === 'swot' ? styles.active : ''}`}
          onClick={() => setSelectedView('swot')}
        >
          SWOT Analysis
        </button>
      </div>

      {selectedView === 'overview' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className={styles.overview}
        >
          {/* Market Share Visualization */}
          <div className={styles.marketShare}>
            <h4 className={styles.sectionTitle}>Market Share Distribution</h4>
            <div className={styles.shareChart}>
              {competitors.map((competitor, index) => (
                <motion.div
                  key={competitor.name}
                  initial={{ width: 0 }}
                  animate={{ width: `${competitor.marketShare}%` }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className={styles.shareBar}
                  style={{ opacity: 1 - (index * 0.2) }}
                >
                  <span className={styles.shareLabel}>
                    {competitor.name} ({competitor.marketShare}%)
                  </span>
                </motion.div>
              ))}
              <div className={styles.shareRemaining}>
                <span className={styles.shareLabel}>
                  Others ({100 - competitors.reduce((acc, c) => acc + c.marketShare, 0)}%)
                </span>
              </div>
            </div>
          </div>

          {/* Competitor Cards */}
          <div className={styles.competitors}>
            {competitors.map((competitor, index) => (
              <motion.div
                key={competitor.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={styles.competitorCard}
              >
                <div className={styles.competitorHeader}>
                  <h5 className={styles.competitorName}>{competitor.name}</h5>
                  <span className={styles.competitorStage}>{competitor.stage}</span>
                </div>
                
                {competitor.funding !== '$0' && (
                  <div className={styles.competitorFunding}>
                    Funding: {competitor.funding}
                  </div>
                )}

                <div className={styles.competitorDetails}>
                  <div className={styles.detailSection}>
                    <span className={styles.detailLabel}>Strengths</span>
                    <ul className={styles.detailList}>
                      {competitor.strengths.slice(0, 2).map((strength, i) => (
                        <li key={i}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className={styles.detailSection}>
                    <span className={styles.detailLabel}>Weaknesses</span>
                    <ul className={styles.detailList}>
                      {competitor.weaknesses.slice(0, 2).map((weakness, i) => (
                        <li key={i}>{weakness}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {selectedView === 'swot' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className={styles.swot}
        >
          <div className={styles.swotGrid}>
            <div className={styles.swotQuadrant}>
              <h4 className={styles.quadrantTitle}>Strengths</h4>
              <ul className={styles.swotList}>
                {yourStartup.strengths.map((strength, index) => (
                  <li key={index}>{strength}</li>
                ))}
              </ul>
            </div>
            
            <div className={styles.swotQuadrant}>
              <h4 className={styles.quadrantTitle}>Weaknesses</h4>
              <ul className={styles.swotList}>
                {yourStartup.weaknesses.map((weakness, index) => (
                  <li key={index}>{weakness}</li>
                ))}
              </ul>
            </div>
            
            <div className={styles.swotQuadrant}>
              <h4 className={styles.quadrantTitle}>Opportunities</h4>
              <ul className={styles.swotList}>
                {yourStartup.opportunities.map((opportunity, index) => (
                  <li key={index}>{opportunity}</li>
                ))}
              </ul>
            </div>
            
            <div className={styles.swotQuadrant}>
              <h4 className={styles.quadrantTitle}>Threats</h4>
              <ul className={styles.swotList}>
                {yourStartup.threats.map((threat, index) => (
                  <li key={index}>{threat}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className={styles.swotInsight}>
            <h4 className={styles.insightTitle}>Strategic Positioning</h4>
            <p className={styles.insightText}>
              As a new entrant, focus on leveraging your agility and innovation to target underserved niches. 
              Build strategic partnerships to overcome resource limitations and establish credibility. 
              Your customer-centric approach can be a key differentiator against larger, slower competitors.
            </p>
          </div>
        </motion.div>
      )}

      {/* Competitive Advantages */}
      <div className={styles.advantages}>
        <h4 className={styles.advantagesTitle}>Your Competitive Advantages</h4>
        <div className={styles.advantagesList}>
          <div className={styles.advantage}>
            <span className={styles.advantageIcon}>→</span>
            <span className={styles.advantageText}>
              Speed to market - Ship features 10x faster than enterprises
            </span>
          </div>
          <div className={styles.advantage}>
            <span className={styles.advantageIcon}>→</span>
            <span className={styles.advantageText}>
              Customer intimacy - Direct founder involvement in customer success
            </span>
          </div>
          <div className={styles.advantage}>
            <span className={styles.advantageIcon}>→</span>
            <span className={styles.advantageText}>
              Innovation focus - Not constrained by legacy systems or processes
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};