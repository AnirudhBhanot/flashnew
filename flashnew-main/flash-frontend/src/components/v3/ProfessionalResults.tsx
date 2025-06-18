import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { EnrichedAnalysisData } from '../../types/api.types';
import './ProfessionalResults.css';

interface ProfessionalResultsProps {
  data: EnrichedAnalysisData;
  onBack?: () => void;
  onExport?: () => void;
}

interface RejectionReason {
  title: string;
  description: string;
  impacts: string[];
}

interface Recommendation {
  title: string;
  description: string;
  actions: string[];
}

export const ProfessionalResults: React.FC<ProfessionalResultsProps> = ({ 
  data, 
  onBack,
  onExport 
}) => {
  const [activeSection, setActiveSection] = useState<string>('overview');
  
  // Calculate overall score (0-100)
  const overallScore = Math.round(data.success_probability * 100);
  
  // Determine readiness status
  const getReadinessStatus = (score: number): { text: string; className: string } => {
    if (score >= 80) return { text: 'Ready to raise', className: 'status-ready' };
    if (score >= 65) return { text: 'Almost ready', className: 'status-almost' };
    return { text: 'Not ready to raise', className: 'status-not-ready' };
  };
  
  const readinessStatus = getReadinessStatus(overallScore);
  
  // Get CAMP scores
  const campScores = data.camp_scores || data.pillar_scores || {
    capital: 0.5,
    advantage: 0.5,
    market: 0.5,
    people: 0.5
  };
  
  // Generate rejection reasons based on low scores
  const generateRejectionReasons = (): RejectionReason[] => {
    const reasons: RejectionReason[] = [];
    
    if (campScores.advantage < 0.6) {
      reasons.push({
        title: 'Unclear competitive advantage',
        description: 'Your pitch doesn\'t clearly articulate why customers would choose you over established players. VCs need to see a unique insight or technical advantage that others can\'t easily replicate.',
        impacts: ['Advantage Score', 'Fundability']
      });
    }
    
    if (campScores.people < 0.65) {
      reasons.push({
        title: 'Team gaps for your market',
        description: 'Your team is missing key expertise needed for your target market. VCs will worry about execution risk, especially in critical early phases.',
        impacts: ['People Score', 'Execution Risk']
      });
    }
    
    if (campScores.market < 0.6) {
      reasons.push({
        title: 'Weak go-to-market strategy',
        description: 'You haven\'t identified specific customer segments, channels, or CAC targets. VCs need to see you\'ve thought deeply about how to acquire customers profitably.',
        impacts: ['Market Score', 'Growth Potential']
      });
    }
    
    if (campScores.capital < 0.65) {
      reasons.push({
        title: 'Unclear path to profitability',
        description: 'Your financial projections don\'t show a clear path to positive unit economics. VCs need confidence that you can build a sustainable business.',
        impacts: ['Capital Score', 'Financial Health']
      });
    }
    
    return reasons.slice(0, 3); // Top 3 reasons
  };
  
  // Generate recommendations based on issues
  const generateRecommendations = (): Recommendation[] => {
    const recommendations: Recommendation[] = [];
    
    if (campScores.advantage < 0.6) {
      recommendations.push({
        title: 'Define your unique technical advantage',
        description: 'Stop positioning as "X for Y" and instead highlight your proprietary approach. This could be your unique technology, process innovation, or market insight.',
        actions: [
          'Interview 20 potential customers about their biggest pain points',
          'Document 3-5 technical innovations that competitors can\'t easily copy',
          'Create a competitive matrix showing your unique position'
        ]
      });
    }
    
    if (campScores.people < 0.65) {
      recommendations.push({
        title: 'Strengthen your team',
        description: 'Add expertise in areas where you\'re weak. This could be through co-founders, early hires, or experienced advisors.',
        actions: [
          'Identify the top 3 skill gaps in your team',
          'Reach out to 5 experts in each area',
          'Consider offering advisor equity to key experts'
        ]
      });
    }
    
    if (campScores.market < 0.6) {
      recommendations.push({
        title: 'Develop a specific GTM playbook',
        description: 'Replace generic strategies with specific tactics. Test channels with small experiments and measure results.',
        actions: [
          'Define your ICP with 10+ specific attributes',
          'Run 3 channel experiments with $1000 budgets each',
          'Calculate CAC and LTV projections based on early data'
        ]
      });
    }
    
    return recommendations.slice(0, 3);
  };
  
  const rejectionReasons = generateRejectionReasons();
  const recommendations = generateRecommendations();
  
  // Scroll reveal animation
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );
    
    document.querySelectorAll('.reveal').forEach(el => {
      observer.observe(el);
    });
    
    return () => observer.disconnect();
  }, []);
  
  return (
    <div className="professional-results">
      {/* Header */}
      <header className="results-header">
        <div className="results-container">
          <div className="header-content">
            <button className="back-button" onClick={onBack}>
              ← Back
            </button>
            <div className="header-actions">
              <button className="export-button" onClick={onExport}>
                Export PDF
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* Company Info */}
      <section className="company-section">
        <div className="results-container">
          <div className="company-info">
            <div className="company-details">
              <h1>Your Startup</h1>
              <div className="company-meta">
                <span className="meta-item">{data.industry || data.userInput?.sector || 'Technology'}</span>
                <span className="meta-separator">•</span>
                <span className="meta-item">{data.funding_stage || 'Pre-seed'}</span>
                <span className="meta-separator">•</span>
                <span className="meta-item">Analysis Date: {new Date().toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Overall Score */}
      <section className="score-section">
        <div className="results-container">
          <div className="score-container">
            <svg className="score-circle" viewBox="0 0 200 200">
              <circle 
                cx="100" cy="100" r="90" 
                fill="none" 
                stroke="#eaeaea" 
                strokeWidth="20"
              />
              <circle 
                cx="100" cy="100" r="90" 
                fill="none" 
                stroke={overallScore >= 80 ? '#34c759' : overallScore >= 65 ? '#ffcc00' : '#ff3b30'}
                strokeWidth="20"
                strokeDasharray="565.48"
                strokeDashoffset={565.48 - (565.48 * overallScore / 100)}
                transform="rotate(-90 100 100)"
                className="score-progress"
              />
            </svg>
            <div className={`score-number ${overallScore >= 80 ? 'score-high' : overallScore >= 65 ? 'score-medium' : 'score-low'}`}>
              {overallScore}
            </div>
            <div className="score-label">out of 100</div>
          </div>
          
          <div className={`score-status ${readinessStatus.className}`}>
            <span className="status-dot"></span>
            <span>{readinessStatus.text}</span>
          </div>
          
          <p className="score-message">
            {overallScore >= 80 
              ? 'Your startup is well-positioned to raise funding. Focus on the recommendations below to maximize your chances.'
              : overallScore >= 65
              ? 'Your startup shows strong potential but needs some improvements before approaching investors.'
              : 'Your startup shows promise but needs significant improvements before approaching investors. Focus on the recommendations below to increase your score by 20-30 points.'}
          </p>
        </div>
      </section>
      
      {/* CAMP Breakdown */}
      <section className="camp-section">
        <div className="results-container">
          <h2 className="section-title">CAMP Framework Breakdown</h2>
          
          <div className="camp-grid">
            <div className="camp-metric">
              <div className="camp-icon">💰</div>
              <div className="camp-name">Capital</div>
              <div className={`camp-score ${campScores.capital >= 0.7 ? 'score-high' : campScores.capital >= 0.5 ? 'score-medium' : 'score-low'}`}>
                {Math.round(campScores.capital * 100)}
              </div>
              <div className="camp-benchmark">Stage avg: 72</div>
            </div>
            
            <div className="camp-metric">
              <div className="camp-icon">⚡</div>
              <div className="camp-name">Advantage</div>
              <div className={`camp-score ${campScores.advantage >= 0.7 ? 'score-high' : campScores.advantage >= 0.5 ? 'score-medium' : 'score-low'}`}>
                {Math.round(campScores.advantage * 100)}
              </div>
              <div className="camp-benchmark">Stage avg: 65</div>
            </div>
            
            <div className="camp-metric">
              <div className="camp-icon">📈</div>
              <div className="camp-name">Market</div>
              <div className={`camp-score ${campScores.market >= 0.7 ? 'score-high' : campScores.market >= 0.5 ? 'score-medium' : 'score-low'}`}>
                {Math.round(campScores.market * 100)}
              </div>
              <div className="camp-benchmark">Stage avg: 70</div>
            </div>
            
            <div className="camp-metric">
              <div className="camp-icon">👥</div>
              <div className="camp-name">People</div>
              <div className={`camp-score ${campScores.people >= 0.7 ? 'score-high' : campScores.people >= 0.5 ? 'score-medium' : 'score-low'}`}>
                {Math.round(campScores.people * 100)}
              </div>
              <div className="camp-benchmark">Stage avg: 75</div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Top Rejection Reasons */}
      {rejectionReasons.length > 0 && (
        <section className="rejection-section">
          <div className="results-container">
            <h2 className="section-title">Top {rejectionReasons.length} Reasons VCs Will Pass</h2>
            
            <div className="rejection-list">
              {rejectionReasons.map((reason, index) => (
                <motion.div 
                  key={index} 
                  className="rejection-item reveal"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="rejection-number">{index + 1}</div>
                  <div className="rejection-content">
                    <h3 className="rejection-title">{reason.title}</h3>
                    <p className="rejection-description">{reason.description}</p>
                    <div className="rejection-impact">
                      <span className="impact-label">Impacts:</span>
                      <div className="impact-pills">
                        {reason.impacts.map((impact, i) => (
                          <span key={i} className="impact-pill">{impact}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}
      
      {/* Recommendations */}
      <section className="recommendations-section">
        <div className="results-container">
          <h2 className="section-title">How to Fix These Issues</h2>
          
          <div className="recommendation-grid">
            {recommendations.map((rec, index) => (
              <motion.div 
                key={index} 
                className="recommendation-card reveal"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <h3 className="recommendation-title">{rec.title}</h3>
                <p className="recommendation-description">{rec.description}</p>
                <div className="recommendation-actions">
                  {rec.actions.map((action, i) => (
                    <div key={i} className="action-item">{action}</div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      {/* 30-Day Action Plan */}
      <section className="action-plan-section">
        <div className="results-container">
          <h2 className="section-title">Your 30-Day Action Plan</h2>
          <p className="action-plan-description">
            Focus on these priorities to improve your fundability score the fastest.
          </p>
          
          <div className="priority-list">
            <div className="priority-item">
              <div className="priority-number">1</div>
              <div className="priority-content">
                <div className="priority-title">Customer discovery sprint</div>
                <div className="priority-time">Week 1-2</div>
              </div>
            </div>
            
            <div className="priority-item">
              <div className="priority-number">2</div>
              <div className="priority-content">
                <div className="priority-title">Address biggest team gap</div>
                <div className="priority-time">Week 2-3</div>
              </div>
            </div>
            
            <div className="priority-item">
              <div className="priority-number">3</div>
              <div className="priority-content">
                <div className="priority-title">Test GTM channels</div>
                <div className="priority-time">Week 3-4</div>
              </div>
            </div>
            
            <div className="priority-item">
              <div className="priority-number">4</div>
              <div className="priority-content">
                <div className="priority-title">Refine positioning & pitch</div>
                <div className="priority-time">Week 4</div>
              </div>
            </div>
          </div>
          
          <div className="action-plan-cta">
            <button className="reanalyze-button" onClick={onBack}>
              Re-analyze After Improvements
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};