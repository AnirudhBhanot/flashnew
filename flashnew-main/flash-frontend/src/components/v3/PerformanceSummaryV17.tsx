import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import './PerformanceSummaryV17.css';

interface Metric {
  label: string;
  value: string | number;
  unit?: string;
  status?: 'good' | 'warning' | 'critical';
  trend?: 'up' | 'down' | 'stable';
  description?: string;
}

interface SummaryCard {
  id: string;
  title: string;
  icon: React.ReactNode;
  metrics: Metric[];
  insight: {
    type: 'success' | 'warning' | 'info' | 'error';
    message: string;
  };
  details?: React.ReactNode;
}

interface PerformanceSummaryV17Props {
  data: any;
}

export const PerformanceSummaryV17: React.FC<PerformanceSummaryV17Props> = ({ data }) => {
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());

  const toggleExpanded = (cardId: string) => {
    setExpandedCards(prev => {
      const newSet = new Set(prev);
      if (newSet.has(cardId)) {
        newSet.delete(cardId);
      } else {
        newSet.add(cardId);
      }
      return newSet;
    });
  };

  const formatValue = (value: string | number, unit?: string): string => {
    if (unit === '%') return `${value}%`;
    if (unit === 'x') return `${value}x`;
    if (unit === '$B') return `$${value}B`;
    if (unit === 'months') return `${value} months`;
    if (unit === 'years') return `${value} years`;
    return String(value);
  };

  const getStatusColor = (status?: 'good' | 'warning' | 'critical') => {
    switch (status) {
      case 'good': return 'var(--color-success)';
      case 'warning': return 'var(--color-warning)';
      case 'critical': return 'var(--color-error)';
      default: return 'var(--color-text-secondary)';
    }
  };

  const cards: SummaryCard[] = [
    {
      id: 'capital',
      title: 'Capital',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 6v12M9 9h6M9 15h6" />
        </svg>
      ),
      metrics: [
        {
          label: 'Revenue Growth',
          value: data.revenue_growth_rate_percent || 50,
          unit: '%',
          status: data.revenue_growth_rate_percent > 100 ? 'good' : 'warning',
          trend: 'up'
        },
        {
          label: 'Burn Multiple',
          value: (data.burn_multiple || 2.0).toFixed(1),
          unit: 'x',
          status: data.burn_multiple < 2 ? 'good' : data.burn_multiple < 3 ? 'warning' : 'critical',
          description: 'Cash burned per $1 of new ARR'
        },
        {
          label: 'Runway',
          value: Math.round(data.runway_months || 9),
          unit: 'months',
          status: data.runway_months > 18 ? 'good' : data.runway_months > 12 ? 'warning' : 'critical'
        }
      ],
      insight: {
        type: data.burn_multiple < 2 ? 'success' : 'warning',
        message: data.burn_multiple < 2 ? 'Efficient capital use' : 'Watch burn rate'
      },
      details: (
        <div className="metric-details">
          <h4>Financial Calculations</h4>
          <div className="detail-item">
            <span>Monthly Burn</span>
            <span>${((data.monthly_burn_usd || 467000) / 1000).toFixed(0)}k</span>
          </div>
          <div className="detail-item">
            <span>Cash Balance</span>
            <span>${((data.total_funding_amount_usd || 2500000) / 1000000).toFixed(1)}M</span>
          </div>
          <div className="detail-item">
            <span>LTV/CAC Ratio</span>
            <span>{(data.ltv_cac_ratio || 3.0).toFixed(1)}:1</span>
          </div>
        </div>
      )
    },
    {
      id: 'advantage',
      title: 'Advantage',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
        </svg>
      ),
      metrics: [
        {
          label: 'Tech Score',
          value: `${data.technology_score || 3}/5`,
          status: data.technology_score >= 4 ? 'good' : data.technology_score >= 3 ? 'warning' : 'critical'
        },
        {
          label: 'Has Patent',
          value: data.has_patent ? 'Yes' : 'No',
          status: data.has_patent ? 'good' : 'warning'
        },
        {
          label: 'NPS Score',
          value: data.nps_score || 'N/A',
          status: data.nps_score > 50 ? 'good' : data.nps_score > 30 ? 'warning' : 'critical'
        }
      ],
      insight: {
        type: data.technology_score >= 4 ? 'success' : 'info',
        message: data.technology_score >= 4 ? 'Strong differentiation' : 'Build competitive moat'
      },
      details: (
        <div className="metric-details">
          <h4>Competitive Position</h4>
          <div className="detail-item">
            <span>Unique Features</span>
            <span>{data.unique_features || 3}</span>
          </div>
          <div className="detail-item">
            <span>IP Protection</span>
            <span>{data.has_patent ? 'Protected' : 'At Risk'}</span>
          </div>
          <div className="detail-item">
            <span>Market Position</span>
            <span>{data.scalability_score >= 4 ? 'Leader' : 'Challenger'}</span>
          </div>
        </div>
      )
    },
    {
      id: 'market',
      title: 'Market',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      ),
      metrics: [
        {
          label: 'TAM Size',
          value: Math.round((data.tam_size_usd || 2000000000) / 1000000000),
          unit: '$B',
          status: 'good'
        },
        {
          label: 'Market Growth',
          value: data.market_growth_rate || 15,
          unit: '%',
          status: data.market_growth_rate > 20 ? 'good' : 'warning',
          trend: 'stable'
        },
        {
          label: 'Competition',
          value: data.competition_intensity > 3 ? 'High' : 'Moderate',
          status: data.competition_intensity > 3 ? 'warning' : 'good'
        }
      ],
      insight: {
        type: data.tam_size_usd > 50000000000 ? 'success' : 'info',
        message: data.tam_size_usd > 50000000000 ? 'Large opportunity' : 'Niche market'
      },
      details: (
        <div className="metric-details">
          <h4>Market Analysis</h4>
          <div className="detail-item">
            <span>SAM (Serviceable)</span>
            <span>${(data.tam_size_usd * 0.15 / 1000000000).toFixed(1)}B</span>
          </div>
          <div className="detail-item">
            <span>Market Share Target</span>
            <span>0.5% in 3 years</span>
          </div>
          <div className="detail-item">
            <span>Key Competitors</span>
            <span>{data.competition_intensity > 3 ? '10+' : '5-10'}</span>
          </div>
        </div>
      )
    },
    {
      id: 'people',
      title: 'People',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
          <path d="M16 3.13a4 4 0 0 1 0 7.75" />
        </svg>
      ),
      metrics: [
        {
          label: 'Team Size',
          value: data.team_size_full_time || 3,
          status: data.team_size_full_time > 15 ? 'good' : 'warning'
        },
        {
          label: 'Avg Experience',
          value: data.years_experience_avg || 2,
          unit: 'years',
          status: data.years_experience_avg > 8 ? 'good' : 'warning'
        },
        {
          label: 'Key Hires',
          value: data.team_size_full_time > 20 ? 'Complete' : 'Needed',
          status: data.team_size_full_time > 20 ? 'good' : 'critical'
        }
      ],
      insight: {
        type: data.years_experience_avg > 10 ? 'success' : 'info',
        message: data.years_experience_avg > 10 ? 'Experienced team' : 'Growing team'
      },
      details: (
        <div className="metric-details">
          <h4>Team Breakdown</h4>
          <div className="detail-item">
            <span>Engineering</span>
            <span>{Math.round(data.team_size_full_time * 0.5)}</span>
          </div>
          <div className="detail-item">
            <span>Sales & Marketing</span>
            <span>{Math.round(data.team_size_full_time * 0.3)}</span>
          </div>
          <div className="detail-item">
            <span>Operations</span>
            <span>{Math.round(data.team_size_full_time * 0.2)}</span>
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="performance-summary-v17">
      <div className="summary-header">
        <h2>Performance Overview</h2>
        <p className="summary-subtitle">Key metrics and health indicators</p>
      </div>

      <div className="summary-grid">
        {cards.map((card, index) => (
          <motion.div
            key={card.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card variant="bordered" className="summary-card">
              <div className="card-header">
                <div className="card-icon">{card.icon}</div>
                <h3>{card.title}</h3>
              </div>

              <div className="metrics-list">
                {card.metrics.map((metric, idx) => (
                  <div key={idx} className="metric-item">
                    <div className="metric-label">
                      <span>{metric.label}</span>
                      {metric.trend && (
                        <span className={`trend-indicator trend-${metric.trend}`}>
                          {metric.trend === 'up' ? '↑' : metric.trend === 'down' ? '↓' : '→'}
                        </span>
                      )}
                    </div>
                    <div 
                      className="metric-value"
                      style={{ color: getStatusColor(metric.status) }}
                    >
                      {formatValue(metric.value, metric.unit)}
                    </div>
                  </div>
                ))}
              </div>

              <div className={`insight-badge insight-${card.insight.type}`}>
                <span className="insight-icon">
                  {card.insight.type === 'success' ? '✓' : 
                   card.insight.type === 'warning' ? '!' : 
                   card.insight.type === 'error' ? '✕' : 'i'}
                </span>
                <span>{card.insight.message}</span>
              </div>

              {card.details && (
                <>
                  <Button
                    variant="ghost"
                    size="small"
                    className="expand-button"
                    onClick={() => toggleExpanded(card.id)}
                  >
                    {expandedCards.has(card.id) ? 'Less Details' : 'More Details'}
                    <svg 
                      width="16" 
                      height="16" 
                      viewBox="0 0 16 16" 
                      className={`expand-icon ${expandedCards.has(card.id) ? 'expanded' : ''}`}
                    >
                      <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="2" fill="none" />
                    </svg>
                  </Button>

                  <AnimatePresence>
                    {expandedCards.has(card.id) && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="details-container"
                      >
                        {card.details}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </>
              )}
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};