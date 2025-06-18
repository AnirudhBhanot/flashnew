import React from 'react';
import { motion } from 'framer-motion';
import './InvestmentReadiness.css';

interface ReadinessItem {
  category: 'capital' | 'advantage' | 'market' | 'people';
  item: string;
  status: 'complete' | 'warning' | 'incomplete';
  detail?: string;
  priority?: 'high' | 'medium' | 'low';
}

interface InvestmentReadinessProps {
  pillarScores: {
    capital?: number;
    advantage?: number;
    market?: number;
    people?: number;
  };
  criticalFailures: string[];
  belowThreshold: string[];
  verdict?: string;
}

const getReadinessItems = (
  pillarScores: any,
  criticalFailures: string[],
  belowThreshold: string[],
  verdict?: string
): ReadinessItem[] => {
  const items: ReadinessItem[] = [];
  
  // Validate score helper
  const validateScore = (score: any): number => {
    if (typeof score !== 'number' || isNaN(score) || !isFinite(score)) {
      return 0.5; // Default to middle value
    }
    return Math.max(0, Math.min(1, score));
  };

  // Capital items
  if (pillarScores.capital !== undefined) {
    const capitalScore = validateScore(pillarScores.capital);
    if (capitalScore >= 0.7) {
      items.push({
        category: 'capital',
        item: 'Financial health',
        status: 'complete',
        detail: 'Strong runway and burn rate management'
      });
    } else if (capitalScore >= 0.5) {
      items.push({
        category: 'capital',
        item: 'Financial health',
        status: 'warning',
        detail: 'Adequate but needs improvement',
        priority: 'medium'
      });
    } else {
      items.push({
        category: 'capital',
        item: 'Financial health',
        status: 'incomplete',
        detail: 'Critical improvements needed',
        priority: 'high'
      });
    }
  }

  // Check for critical runway issues
  const runwayIssue = criticalFailures.find(f => f.toLowerCase().includes('runway'));
  if (runwayIssue) {
    items.push({
      category: 'capital',
      item: 'Runway',
      status: 'incomplete',
      detail: runwayIssue,
      priority: 'high'
    });
  }

  // Advantage items
  if (pillarScores.advantage !== undefined) {
    const advantageScore = validateScore(pillarScores.advantage);
    if (advantageScore >= 0.7) {
      items.push({
        category: 'advantage',
        item: 'Competitive moat',
        status: 'complete',
        detail: 'Strong differentiation and defensibility'
      });
    } else if (advantageScore >= 0.5) {
      items.push({
        category: 'advantage',
        item: 'Competitive advantage',
        status: 'warning',
        detail: 'Moderate differentiation',
        priority: 'medium'
      });
    } else {
      items.push({
        category: 'advantage',
        item: 'Competitive advantage',
        status: 'incomplete',
        detail: 'Needs stronger differentiation',
        priority: 'high'
      });
    }
  }

  // Market items
  if (pillarScores.market !== undefined) {
    const marketScore = validateScore(pillarScores.market);
    if (marketScore >= 0.7) {
      items.push({
        category: 'market',
        item: 'Market opportunity',
        status: 'complete',
        detail: 'Large TAM with strong growth'
      });
    } else if (marketScore >= 0.5) {
      items.push({
        category: 'market',
        item: 'Market opportunity',
        status: 'warning',
        detail: 'Decent market size and growth',
        priority: 'medium'
      });
    } else {
      items.push({
        category: 'market',
        item: 'Market opportunity',
        status: 'incomplete',
        detail: 'Market validation needed',
        priority: 'high'
      });
    }
  }

  // Customer concentration check
  const customerIssue = criticalFailures.find(f => f.toLowerCase().includes('customer concentration'));
  if (customerIssue) {
    items.push({
      category: 'market',
      item: 'Customer diversification',
      status: 'incomplete',
      detail: customerIssue,
      priority: 'high'
    });
  }

  // People items
  if (pillarScores.people !== undefined) {
    const peopleScore = validateScore(pillarScores.people);
    if (peopleScore >= 0.8) {
      items.push({
        category: 'people',
        item: 'Team strength',
        status: 'complete',
        detail: 'Experienced team with domain expertise'
      });
    } else if (peopleScore >= 0.6) {
      items.push({
        category: 'people',
        item: 'Team strength',
        status: 'warning',
        detail: 'Good team, room for improvement',
        priority: 'medium'
      });
    } else {
      items.push({
        category: 'people',
        item: 'Team strength',
        status: 'incomplete',
        detail: 'Team needs strengthening',
        priority: 'high'
      });
    }
  }

  // Single founder check
  const founderIssue = criticalFailures.find(f => f.toLowerCase().includes('single founder'));
  if (founderIssue) {
    items.push({
      category: 'people',
      item: 'Team composition',
      status: 'incomplete',
      detail: founderIssue,
      priority: 'high'
    });
  }

  // Add general items based on verdict
  if (verdict && verdict.includes('PASS')) {
    items.push({
      category: 'market',
      item: 'Investment thesis',
      status: 'complete',
      detail: 'Clear path to returns'
    });
  }

  return items;
};

const getCategoryIcon = (category: string): string => {
  const icons: Record<string, string> = {
    capital: '💰',
    advantage: '🚀',
    market: '📊',
    people: '👥'
  };
  return icons[category] || '📋';
};

const getStatusIcon = (status: string): string => {
  const icons: Record<string, string> = {
    complete: '✅',
    warning: '⚠️',
    incomplete: '❌'
  };
  return icons[status] || '•';
};

export const InvestmentReadiness: React.FC<InvestmentReadinessProps> = ({
  pillarScores,
  criticalFailures,
  belowThreshold,
  verdict
}) => {
  const items = getReadinessItems(pillarScores, criticalFailures, belowThreshold, verdict);
  
  // Group items by CAMP category
  const groupedItems = items.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = [];
    }
    acc[item.category].push(item);
    return acc;
  }, {} as Record<string, ReadinessItem[]>);
  
  // Sort items within each group by priority and status
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  const statusOrder = { incomplete: 0, warning: 1, complete: 2 };
  
  Object.keys(groupedItems).forEach(category => {
    groupedItems[category].sort((a, b) => {
      if (a.priority && b.priority && a.priority !== b.priority) {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      }
      return statusOrder[a.status] - statusOrder[b.status];
    });
  });

  const completeCount = items.filter(i => i.status === 'complete').length;
  const totalCount = items.length;
  const readinessPercent = totalCount > 0 ? (completeCount / totalCount) * 100 : 0;
  
  // Define CAMP category order and metadata
  const campCategories = [
    { key: 'capital', name: 'Capital', subtitle: 'Financial Health & Efficiency' },
    { key: 'advantage', name: 'Advantage', subtitle: 'Competitive Moat & Differentiation' },
    { key: 'market', name: 'Market', subtitle: 'TAM Size & Growth Dynamics' },
    { key: 'people', name: 'People', subtitle: 'Team Strength & Experience' }
  ];

  return (
    <div className="investment-readiness-container">
      <div className="readiness-header">
        <h3>Investment Readiness</h3>
        <div className="readiness-score">
          <span className="score-value">{Math.round(readinessPercent)}%</span>
          <span className="score-label">Ready</span>
        </div>
      </div>

      <div className="readiness-progress">
        <div className="progress-bar">
          <motion.div 
            className="progress-fill"
            initial={{ width: 0 }}
            animate={{ width: `${readinessPercent}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
        </div>
        <div className="progress-stats">
          <span className="complete">{completeCount} Complete</span>
          <span className="remaining">{totalCount - completeCount} Remaining</span>
        </div>
      </div>

      <div className="readiness-checklist">
        {campCategories.map((category, categoryIndex) => {
          const categoryItems = groupedItems[category.key] || [];
          if (categoryItems.length === 0) return null;
          
          return (
            <motion.div
              key={category.key}
              className="camp-category-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: categoryIndex * 0.15 }}
            >
              <div className="camp-category-header">
                <div className="camp-title-group">
                  <span className="camp-icon">{getCategoryIcon(category.key)}</span>
                  <h4 className="camp-name">{category.name}</h4>
                </div>
                <p className="camp-subtitle">{category.subtitle}</p>
              </div>
              
              <div className="category-items">
                {categoryItems.map((item, itemIndex) => (
                  <motion.div 
                    key={`${category.key}-${itemIndex}`}
                    className={`checklist-item ${item.status}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: categoryIndex * 0.15 + itemIndex * 0.05 }}
                  >
                    <div className="item-header">
                      <div className="item-left">
                        <span className="status-icon">{getStatusIcon(item.status)}</span>
                        <span className="item-title">{item.item}</span>
                      </div>
                      {item.priority && (
                        <span className={`priority-badge ${item.priority}`}>
                          {item.priority} priority
                        </span>
                      )}
                    </div>
                    {item.detail && (
                      <p className="item-detail">{item.detail}</p>
                    )}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          );
        })}
      </div>

      {items.filter((i: ReadinessItem) => i.status === 'incomplete' && i.priority === 'high').length > 0 && (
        <motion.div 
          className="action-required"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <span className="action-icon">⚡</span>
          <p>Address high-priority items before proceeding with investment</p>
        </motion.div>
      )}
    </div>
  );
};