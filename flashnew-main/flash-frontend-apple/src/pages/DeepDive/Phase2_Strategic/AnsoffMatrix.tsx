import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Icon } from '../../../design-system/components';
import styles from './AnsoffMatrix.module.scss';

interface QuadrantData {
  initiatives: string[];
  resourceAllocation: number;
  riskLevel: 'Low' | 'Medium' | 'High' | 'Very High';
  successProbability: number;
  recommendations: string[];
}

interface AnsoffData {
  marketPenetration: QuadrantData;
  productDevelopment: QuadrantData;
  marketDevelopment: QuadrantData;
  diversification: QuadrantData;
  totalResourceAllocation: number;
  primaryStrategy: string;
  notes: string;
}

const AnsoffMatrix: React.FC = () => {
  const [activeQuadrant, setActiveQuadrant] = useState<string | null>(null);
  const [data, setData] = useState<AnsoffData>({
    marketPenetration: {
      initiatives: [],
      resourceAllocation: 25,
      riskLevel: 'Low',
      successProbability: 75,
      recommendations: []
    },
    productDevelopment: {
      initiatives: [],
      resourceAllocation: 25,
      riskLevel: 'Medium',
      successProbability: 60,
      recommendations: []
    },
    marketDevelopment: {
      initiatives: [],
      resourceAllocation: 25,
      riskLevel: 'Medium',
      successProbability: 55,
      recommendations: []
    },
    diversification: {
      initiatives: [],
      resourceAllocation: 25,
      riskLevel: 'Very High',
      successProbability: 35,
      recommendations: []
    },
    totalResourceAllocation: 100,
    primaryStrategy: '',
    notes: ''
  });

  useEffect(() => {
    const savedData = localStorage.getItem('ansoffMatrixData');
    if (savedData) {
      setData(JSON.parse(savedData));
    }
  }, []);

  const saveData = () => {
    localStorage.setItem('ansoffMatrixData', JSON.stringify(data));
  };

  const updateQuadrantData = (quadrant: keyof AnsoffData, field: keyof QuadrantData, value: any) => {
    if (quadrant in data && typeof data[quadrant] === 'object') {
      setData(prev => ({
        ...prev,
        [quadrant]: {
          ...prev[quadrant] as QuadrantData,
          [field]: value
        }
      }));
    }
  };

  const updateResourceAllocation = (quadrant: keyof AnsoffData, value: number) => {
    if (quadrant in data && typeof data[quadrant] === 'object') {
      const total = Object.keys(data)
        .filter(key => ['marketPenetration', 'productDevelopment', 'marketDevelopment', 'diversification'].includes(key))
        .reduce((sum, key) => {
          if (key === quadrant) return sum + value;
          return sum + (data[key as keyof AnsoffData] as QuadrantData).resourceAllocation;
        }, 0);
      
      if (total <= 100) {
        updateQuadrantData(quadrant, 'resourceAllocation', value);
        setData(prev => ({ ...prev, totalResourceAllocation: total }));
      }
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Low': return '#34c759';
      case 'Medium': return '#ff9500';
      case 'High': return '#ff3b30';
      case 'Very High': return '#af52de';
      default: return '#8e8e93';
    }
  };

  const getQuadrantIcon = (quadrant: string) => {
    switch (quadrant) {
      case 'marketPenetration': return 'arrow.up.circle';
      case 'productDevelopment': return 'lightbulb';
      case 'marketDevelopment': return 'globe';
      case 'diversification': return 'square.grid.2x2';
      default: return 'circle';
    }
  };

  const generateRecommendations = (quadrant: string) => {
    const recommendations: { [key: string]: string[] } = {
      marketPenetration: [
        'Increase sales force effectiveness',
        'Improve customer retention programs',
        'Optimize pricing strategy',
        'Enhance customer service quality',
        'Implement loyalty programs'
      ],
      productDevelopment: [
        'Conduct customer research for new features',
        'Accelerate product roadmap execution',
        'Invest in R&D capabilities',
        'Form strategic technology partnerships',
        'Beta test with key customers'
      ],
      marketDevelopment: [
        'Research new geographic markets',
        'Identify new customer segments',
        'Adapt product for new markets',
        'Build distribution partnerships',
        'Localize marketing messages'
      ],
      diversification: [
        'Conduct thorough market research',
        'Consider acquisitions or partnerships',
        'Start with pilot programs',
        'Ensure adequate resources',
        'Build new competencies gradually'
      ]
    };

    return recommendations[quadrant] || [];
  };

  const calculateStrategicFit = () => {
    const allocations = [
      data.marketPenetration.resourceAllocation,
      data.productDevelopment.resourceAllocation,
      data.marketDevelopment.resourceAllocation,
      data.diversification.resourceAllocation
    ];
    
    const maxAllocation = Math.max(...allocations);
    const strategies = ['marketPenetration', 'productDevelopment', 'marketDevelopment', 'diversification'];
    const primaryIndex = allocations.indexOf(maxAllocation);
    
    return strategies[primaryIndex];
  };

  const quadrants = [
    { key: 'marketPenetration', title: 'Market Penetration', x: 'Existing', y: 'Existing' },
    { key: 'productDevelopment', title: 'Product Development', x: 'New', y: 'Existing' },
    { key: 'marketDevelopment', title: 'Market Development', x: 'Existing', y: 'New' },
    { key: 'diversification', title: 'Diversification', x: 'New', y: 'New' }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Ansoff Matrix: Growth Strategy Analysis</h2>
        <p>Evaluate growth opportunities across products and markets</p>
      </div>

      {/* Visual Matrix */}
      <div className={styles.matrixContainer}>
        <div className={styles.matrixLabels}>
          <div className={styles.xLabel}>Products</div>
          <div className={styles.yLabel}>Markets</div>
        </div>
        
        <div className={styles.matrix}>
          <div className={styles.axisLabels}>
            <div className={styles.topLabels}>
              <span>Existing</span>
              <span>New</span>
            </div>
            <div className={styles.leftLabels}>
              <span>Existing</span>
              <span>New</span>
            </div>
          </div>
          
          <div className={styles.quadrants}>
            {quadrants.map((quadrant, index) => {
              const quadrantData = data[quadrant.key as keyof AnsoffData] as QuadrantData;
              return (
                <motion.div
                  key={quadrant.key}
                  className={`${styles.quadrant} ${activeQuadrant === quadrant.key ? styles.active : ''}`}
                  onClick={() => setActiveQuadrant(quadrant.key)}
                  whileHover={{ scale: 1.02 }}
                  style={{
                    gridColumn: index % 2 === 0 ? 1 : 2,
                    gridRow: index < 2 ? 1 : 2
                  }}
                >
                  <div className={styles.quadrantHeader}>
                    <Icon name={getQuadrantIcon(quadrant.key)} size={24} />
                    <h3>{quadrant.title}</h3>
                  </div>
                  
                  <div className={styles.quadrantStats}>
                    <div className={styles.stat}>
                      <span>Resources</span>
                      <strong>{quadrantData.resourceAllocation}%</strong>
                    </div>
                    <div className={styles.stat}>
                      <span>Risk</span>
                      <strong style={{ color: getRiskColor(quadrantData.riskLevel) }}>
                        {quadrantData.riskLevel}
                      </strong>
                    </div>
                    <div className={styles.stat}>
                      <span>Success</span>
                      <strong>{quadrantData.successProbability}%</strong>
                    </div>
                  </div>
                  
                  <div className={styles.quadrantProgress}>
                    <div 
                      className={styles.progressBar}
                      style={{ 
                        width: `${quadrantData.resourceAllocation}%`,
                        backgroundColor: getRiskColor(quadrantData.riskLevel)
                      }}
                    />
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Detailed View */}
      {activeQuadrant && (
        <motion.div 
          className={styles.detailView}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className={styles.detailHeader}>
            <h3>{quadrants.find(q => q.key === activeQuadrant)?.title}</h3>
            <button onClick={() => setActiveQuadrant(null)}>
              <Icon name="xmark" size={20} />
            </button>
          </div>

          <div className={styles.detailContent}>
            <div className={styles.detailSection}>
              <h4>Current Initiatives</h4>
              <div className={styles.initiativesList}>
                {(data[activeQuadrant as keyof AnsoffData] as QuadrantData).initiatives.map((initiative, index) => (
                  <div key={index} className={styles.initiative}>
                    <Icon name="checkmark.circle" size={16} />
                    <span>{initiative}</span>
                  </div>
                ))}
                <input
                  type="text"
                  placeholder="Add new initiative..."
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && e.currentTarget.value) {
                      const newInitiatives = [
                        ...(data[activeQuadrant as keyof AnsoffData] as QuadrantData).initiatives,
                        e.currentTarget.value
                      ];
                      updateQuadrantData(activeQuadrant as keyof AnsoffData, 'initiatives', newInitiatives);
                      e.currentTarget.value = '';
                    }
                  }}
                />
              </div>
            </div>

            <div className={styles.detailSection}>
              <h4>Resource Allocation</h4>
              <div className={styles.sliderContainer}>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={(data[activeQuadrant as keyof AnsoffData] as QuadrantData).resourceAllocation}
                  onChange={(e) => updateResourceAllocation(activeQuadrant as keyof AnsoffData, parseInt(e.target.value))}
                />
                <span>{(data[activeQuadrant as keyof AnsoffData] as QuadrantData).resourceAllocation}%</span>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h4>Risk Assessment</h4>
              <div className={styles.riskButtons}>
                {['Low', 'Medium', 'High', 'Very High'].map(risk => (
                  <button
                    key={risk}
                    className={`${styles.riskButton} ${
                      (data[activeQuadrant as keyof AnsoffData] as QuadrantData).riskLevel === risk ? styles.active : ''
                    }`}
                    onClick={() => updateQuadrantData(activeQuadrant as keyof AnsoffData, 'riskLevel', risk)}
                    style={{
                      borderColor: getRiskColor(risk),
                      backgroundColor: (data[activeQuadrant as keyof AnsoffData] as QuadrantData).riskLevel === risk 
                        ? getRiskColor(risk) 
                        : 'transparent'
                    }}
                  >
                    {risk}
                  </button>
                ))}
              </div>
            </div>

            <div className={styles.detailSection}>
              <h4>Success Probability</h4>
              <div className={styles.sliderContainer}>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={(data[activeQuadrant as keyof AnsoffData] as QuadrantData).successProbability}
                  onChange={(e) => updateQuadrantData(activeQuadrant as keyof AnsoffData, 'successProbability', parseInt(e.target.value))}
                />
                <span>{(data[activeQuadrant as keyof AnsoffData] as QuadrantData).successProbability}%</span>
              </div>
            </div>

            <div className={styles.detailSection}>
              <h4>Strategic Recommendations</h4>
              <div className={styles.recommendations}>
                {generateRecommendations(activeQuadrant).map((rec, index) => (
                  <div key={index} className={styles.recommendation}>
                    <Icon name="lightbulb" size={16} />
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Strategic Summary */}
      <div className={styles.summary}>
        <h3>Strategic Summary</h3>
        <div className={styles.summaryContent}>
          <div className={styles.summaryItem}>
            <Icon name="target" size={20} />
            <div>
              <h4>Primary Strategy</h4>
              <p>{quadrants.find(q => q.key === calculateStrategicFit())?.title || 'Balanced Approach'}</p>
            </div>
          </div>
          
          <div className={styles.summaryItem}>
            <Icon name="chart.pie" size={20} />
            <div>
              <h4>Resource Distribution</h4>
              <p>{data.totalResourceAllocation}% allocated</p>
            </div>
          </div>
          
          <div className={styles.summaryItem}>
            <Icon name="exclamationmark.triangle" size={20} />
            <div>
              <h4>Overall Risk Profile</h4>
              <p>{
                data.diversification.resourceAllocation > 40 ? 'High' :
                (data.marketDevelopment.resourceAllocation + data.productDevelopment.resourceAllocation) > 60 ? 'Medium' :
                'Low'
              }</p>
            </div>
          </div>
        </div>
        
        <div className={styles.notesSection}>
          <h4>Strategic Notes</h4>
          <textarea
            value={data.notes}
            onChange={(e) => setData(prev => ({ ...prev, notes: e.target.value }))}
            placeholder="Add strategic considerations, market insights, or implementation notes..."
            rows={4}
          />
        </div>
      </div>

      <div className={styles.actions}>
        <button onClick={saveData} className={styles.saveButton}>
          <Icon name="square.and.arrow.down" size={16} />
          Save Analysis
        </button>
      </div>
    </div>
  );
};

export default AnsoffMatrix;