import React from 'react';
import { motion } from 'framer-motion';
import { RISK_THRESHOLDS, RISK_INDICATOR_POSITIONS } from '../../../config/constants';
import './RiskAssessment.css';

interface RiskAssessmentProps {
  riskLevel: string;
  criticalFailures: string[];
  riskFactors?: string[];
}

const getRiskLevelDetails = (riskLevel: string) => {
  const level = riskLevel.toLowerCase();
  
  if (level.includes('very high')) {
    return {
      severity: 'critical',
      color: '#FF4444',
      icon: '🚨',
      message: 'Critical risks require immediate attention'
    };
  } else if (level.includes('high')) {
    return {
      severity: 'high',
      color: '#FF8800',
      icon: '⚠️',
      message: 'Significant risks need addressing'
    };
  } else if (level.includes('medium')) {
    return {
      severity: 'medium',
      color: '#FFD93D',
      icon: '⚡',
      message: 'Moderate risks to monitor'
    };
  } else {
    return {
      severity: 'low',
      color: '#00C851',
      icon: '✓',
      message: 'Risks are well managed'
    };
  }
};

const getMitigationStrategy = (failure: string): string => {
  const failureLower = failure.toLowerCase();
  
  if (failureLower.includes('runway') || failureLower.includes(`${RISK_THRESHOLDS.runway_months_critical} months`)) {
    return 'Immediate fundraising required. Consider bridge funding or revenue acceleration.';
  } else if (failureLower.includes('burn') && failureLower.includes(`${RISK_THRESHOLDS.burn_multiple_high}x`)) {
    return 'Reduce burn rate urgently. Focus on path to profitability or secure funding.';
  } else if (failureLower.includes('customer concentration')) {
    return `Diversify customer base. No single customer should exceed ${RISK_THRESHOLDS.revenue_concentration_high * 100}% of revenue.`;
  } else if (failureLower.includes('churn') && failureLower.includes(`${RISK_THRESHOLDS.churn_rate_high * 100}%`)) {
    return 'Investigate churn causes immediately. Implement customer success program.';
  } else if (failureLower.includes('single founder')) {
    return 'Build co-founder or strong executive team. Document key processes.';
  } else {
    return 'Address this risk through strategic planning and execution.';
  }
};

const getFailureIcon = (failure: string): string => {
  const failureLower = failure.toLowerCase();
  
  if (failureLower.includes('runway') || failureLower.includes('burn')) {
    return '💰';
  } else if (failureLower.includes('customer') || failureLower.includes('churn')) {
    return '👥';
  } else if (failureLower.includes('founder') || failureLower.includes('team')) {
    return '🧑‍💼';
  } else if (failureLower.includes('market')) {
    return '📊';
  } else {
    return '⚠️';
  }
};

export const RiskAssessment: React.FC<RiskAssessmentProps> = ({
  riskLevel,
  criticalFailures,
  riskFactors = []
}) => {
  const riskDetails = getRiskLevelDetails(riskLevel);
  // Remove duplicates by converting to Set and back to array
  const uniqueRisks = Array.from(new Set([...criticalFailures, ...riskFactors]));
  const allRisks = uniqueRisks.slice(0, 5); // Top 5 risks

  return (
    <div className="risk-assessment-container">
      <div className="risk-header">
        <h3>Risk Assessment</h3>
        <motion.div 
          className={`risk-badge ${riskDetails.severity}`}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 200 }}
        >
          <span className="risk-icon">{riskDetails.icon}</span>
          <span className="risk-level">{riskLevel}</span>
        </motion.div>
      </div>

      <div className="risk-meter-container">
        <div className="risk-meter">
          <div className="risk-segments">
            <div className="segment low"></div>
            <div className="segment medium"></div>
            <div className="segment high"></div>
            <div className="segment critical"></div>
          </div>
          <motion.div 
            className="risk-indicator"
            initial={{ left: '0%' }}
            animate={{ 
              left: riskDetails.severity === 'critical' ? `${RISK_INDICATOR_POSITIONS.critical}%` : 
                    riskDetails.severity === 'high' ? `${RISK_INDICATOR_POSITIONS.high}%` :
                    riskDetails.severity === 'medium' ? `${RISK_INDICATOR_POSITIONS.medium}%` : `${RISK_INDICATOR_POSITIONS.low}%`
            }}
            transition={{ duration: 1, ease: "easeInOut" }}
            style={{ backgroundColor: riskDetails.color }}
          />
        </div>
        <p className="risk-message">{riskDetails.message}</p>
      </div>

      {allRisks.length > 0 && (
        <div className="risk-factors">
          <h4>Key Risk Factors</h4>
          <div className="risk-list">
            {allRisks.map((risk, index) => (
              <motion.div 
                key={index}
                className="risk-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="risk-item-header">
                  <span className="risk-item-icon">{getFailureIcon(risk)}</span>
                  <span className="risk-item-title">{risk}</span>
                </div>
                <div className="mitigation-strategy">
                  <span className="mitigation-label">Mitigation:</span>
                  <span className="mitigation-text">{getMitigationStrategy(risk)}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {criticalFailures.length === 0 && riskDetails.severity === 'low' && (
        <motion.div 
          className="no-critical-risks"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <span className="success-icon">🎉</span>
          <p>No critical risks identified. The startup shows good fundamentals.</p>
        </motion.div>
      )}
    </div>
  );
};