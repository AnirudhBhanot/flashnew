import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ScenarioPlanning.module.scss';

interface ScenarioData {
  id: string;
  name: string;
  type: 'best' | 'base' | 'worst' | 'custom';
  probability: number;
  description: string;
  assumptions: string[];
  triggers: {
    positive: string[];
    negative: string[];
  };
  financials: {
    revenue: number[];
    costs: number[];
    profit: number[];
    cashFlow: number[];
    marketShare: number[];
    customerGrowth: number[];
  };
  risks: {
    id: string;
    name: string;
    impact: number;
    likelihood: number;
    mitigation: string;
  }[];
  milestones: {
    quarter: string;
    target: string;
    metric: string;
    value: number;
  }[];
  color: string;
}

interface SensitivityParameter {
  id: string;
  name: string;
  category: string;
  baseValue: number;
  currentValue: number;
  min: number;
  max: number;
  unit: string;
  impact: 'revenue' | 'cost' | 'both';
  sensitivity: number;
}

interface ContingencyPlan {
  id: string;
  trigger: string;
  condition: string;
  actions: string[];
  resources: string[];
  timeline: string;
  owner: string;
  status: 'ready' | 'partial' | 'planning';
}

interface ScenarioPlanningProps {
  onComplete: (data: any) => void;
  initialData?: any;
}

const ScenarioPlanning: React.FC<ScenarioPlanningProps> = ({ onComplete, initialData }) => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'scenarios' | 'sensitivity' | 'contingency'>('scenarios');
  const [scenarios, setScenarios] = useState<ScenarioData[]>([
    {
      id: 'best-case',
      name: 'Best Case Scenario',
      type: 'best',
      probability: 25,
      description: 'Optimal market conditions with strong product-market fit',
      assumptions: [
        'Market grows at 20% annually',
        'Achieve 15% market share by Year 2',
        'Customer acquisition cost decreases 30%',
        'High customer retention (90%+)'
      ],
      triggers: {
        positive: [
          'Key partnership secured',
          'Viral growth achieved',
          'Major competitor exits',
          'Regulatory approval fast-tracked'
        ],
        negative: []
      },
      financials: {
        revenue: [100, 300, 600, 1200, 2000],
        costs: [150, 250, 400, 600, 800],
        profit: [-50, 50, 200, 600, 1200],
        cashFlow: [-100, -50, 150, 500, 1000],
        marketShare: [2, 5, 10, 15, 20],
        customerGrowth: [100, 300, 700, 1500, 3000]
      },
      risks: [],
      milestones: [
        { quarter: 'Q1', target: 'Product Launch', metric: 'Users', value: 1000 },
        { quarter: 'Q2', target: 'Market Expansion', metric: 'Revenue', value: 100000 },
        { quarter: 'Q3', target: 'Series A', metric: 'Funding', value: 5000000 },
        { quarter: 'Q4', target: 'Profitability', metric: 'Profit Margin', value: 15 }
      ],
      color: '#4caf50'
    },
    {
      id: 'base-case',
      name: 'Base Case Scenario',
      type: 'base',
      probability: 50,
      description: 'Expected growth trajectory with normal market conditions',
      assumptions: [
        'Market grows at 10% annually',
        'Achieve 7% market share by Year 2',
        'Customer acquisition cost stable',
        'Moderate customer retention (75%)'
      ],
      triggers: {
        positive: [
          'Product launches on schedule',
          'Steady customer growth',
          'Funding secured as planned'
        ],
        negative: [
          'Minor competitive pressure',
          'Some regulatory delays'
        ]
      },
      financials: {
        revenue: [50, 150, 350, 700, 1200],
        costs: [120, 200, 350, 550, 750],
        profit: [-70, -50, 0, 150, 450],
        cashFlow: [-120, -100, -50, 100, 400],
        marketShare: [1, 3, 5, 7, 10],
        customerGrowth: [50, 150, 400, 800, 1500]
      },
      risks: [
        {
          id: 'r1',
          name: 'Market Competition',
          impact: 6,
          likelihood: 7,
          mitigation: 'Differentiation strategy'
        }
      ],
      milestones: [
        { quarter: 'Q1', target: 'MVP Launch', metric: 'Users', value: 500 },
        { quarter: 'Q2', target: 'Revenue Start', metric: 'Revenue', value: 50000 },
        { quarter: 'Q3', target: 'Seed Plus', metric: 'Funding', value: 2000000 },
        { quarter: 'Q4', target: 'Break Even', metric: 'Profit Margin', value: 0 }
      ],
      color: '#2196f3'
    },
    {
      id: 'worst-case',
      name: 'Worst Case Scenario',
      type: 'worst',
      probability: 25,
      description: 'Challenging market conditions with significant headwinds',
      assumptions: [
        'Market contracts or grows slowly',
        'Achieve only 2% market share',
        'Customer acquisition cost increases 50%',
        'Low customer retention (50%)'
      ],
      triggers: {
        positive: [],
        negative: [
          'Major competitor enters',
          'Regulatory restrictions',
          'Economic downturn',
          'Technology becomes obsolete'
        ]
      },
      financials: {
        revenue: [20, 50, 100, 200, 400],
        costs: [100, 180, 300, 450, 600],
        profit: [-80, -130, -200, -250, -200],
        cashFlow: [-150, -250, -400, -500, -450],
        marketShare: [0.5, 1, 1.5, 2, 2.5],
        customerGrowth: [20, 50, 100, 200, 350]
      },
      risks: [
        {
          id: 'r2',
          name: 'Funding Shortage',
          impact: 9,
          likelihood: 8,
          mitigation: 'Extend runway, pivot strategy'
        },
        {
          id: 'r3',
          name: 'Product-Market Fit',
          impact: 8,
          likelihood: 7,
          mitigation: 'Rapid iteration, customer feedback'
        }
      ],
      milestones: [
        { quarter: 'Q1', target: 'Pilot Launch', metric: 'Users', value: 100 },
        { quarter: 'Q2', target: 'Pivot Strategy', metric: 'Revenue', value: 10000 },
        { quarter: 'Q3', target: 'Bridge Funding', metric: 'Funding', value: 500000 },
        { quarter: 'Q4', target: 'Survival Mode', metric: 'Burn Rate', value: -50000 }
      ],
      color: '#f44336'
    }
  ]);

  const [selectedScenario, setSelectedScenario] = useState<string>('base-case');
  const [sensitivityParams, setSensitivityParams] = useState<SensitivityParameter[]>([
    {
      id: 'market-growth',
      name: 'Market Growth Rate',
      category: 'Market',
      baseValue: 10,
      currentValue: 10,
      min: -5,
      max: 30,
      unit: '%',
      impact: 'revenue',
      sensitivity: 1.5
    },
    {
      id: 'cac',
      name: 'Customer Acquisition Cost',
      category: 'Sales',
      baseValue: 100,
      currentValue: 100,
      min: 50,
      max: 200,
      unit: '$',
      impact: 'cost',
      sensitivity: -1.2
    },
    {
      id: 'churn-rate',
      name: 'Churn Rate',
      category: 'Customer',
      baseValue: 5,
      currentValue: 5,
      min: 1,
      max: 15,
      unit: '%',
      impact: 'both',
      sensitivity: -2.0
    },
    {
      id: 'pricing',
      name: 'Average Price Point',
      category: 'Product',
      baseValue: 50,
      currentValue: 50,
      min: 25,
      max: 100,
      unit: '$',
      impact: 'revenue',
      sensitivity: 1.8
    }
  ]);

  const [contingencyPlans, setContingencyPlans] = useState<ContingencyPlan[]>([
    {
      id: 'cp1',
      trigger: 'Runway < 6 months',
      condition: 'Cash balance below $500k',
      actions: [
        'Implement hiring freeze',
        'Reduce marketing spend by 50%',
        'Accelerate fundraising timeline',
        'Consider bridge financing'
      ],
      resources: ['CFO', 'CEO', 'Board approval'],
      timeline: '2 weeks',
      owner: 'CFO',
      status: 'ready'
    },
    {
      id: 'cp2',
      trigger: 'Major competitor enters',
      condition: 'Competitor with >$50M funding',
      actions: [
        'Accelerate product roadmap',
        'Increase marketing spend',
        'Focus on differentiation',
        'Consider strategic partnerships'
      ],
      resources: ['Product team', 'Marketing budget', 'BD team'],
      timeline: '1 month',
      owner: 'CPO',
      status: 'partial'
    }
  ]);

  // Load initial data
  useEffect(() => {
    if (initialData) {
      if (initialData.scenarios) setScenarios(initialData.scenarios);
      if (initialData.sensitivityParams) setSensitivityParams(initialData.sensitivityParams);
      if (initialData.contingencyPlans) setContingencyPlans(initialData.contingencyPlans);
    }
  }, [initialData]);

  // Auto-save functionality
  useEffect(() => {
    const saveTimer = setTimeout(() => {
      const data = {
        scenarios,
        sensitivityParams,
        contingencyPlans,
        timestamp: new Date().toISOString()
      };
      if (typeof onComplete === 'function') {
        onComplete(data);
      }
      // Also save to localStorage as backup
      localStorage.setItem('scenarioPlanningData', JSON.stringify(data));
    }, 1000);
    return () => clearTimeout(saveTimer);
  }, [scenarios, sensitivityParams, contingencyPlans, onComplete]);

  const updateScenarioProbability = (scenarioId: string, probability: number) => {
    setScenarios(prev => prev.map(s => 
      s.id === scenarioId ? { ...s, probability } : s
    ));
  };

  const updateSensitivityParam = (paramId: string, value: number) => {
    setSensitivityParams(prev => prev.map(p =>
      p.id === paramId ? { ...p, currentValue: value } : p
    ));
  };

  const addContingencyPlan = () => {
    const newPlan: ContingencyPlan = {
      id: `cp-${Date.now()}`,
      trigger: '',
      condition: '',
      actions: [],
      resources: [],
      timeline: '',
      owner: '',
      status: 'planning'
    };
    setContingencyPlans(prev => [...prev, newPlan]);
  };

  const updateContingencyPlan = (planId: string, updates: Partial<ContingencyPlan>) => {
    setContingencyPlans(prev => prev.map(p =>
      p.id === planId ? { ...p, ...updates } : p
    ));
  };

  const handleCompletePhase = () => {
    const hasScenarios = scenarios.length >= 3;
    const hasContingencyPlans = contingencyPlans.length > 0;
    const hasRiskProbabilities = scenarios.some(s => s.probability > 0);
    
    if (hasScenarios && hasContingencyPlans && hasRiskProbabilities) {
      const data = {
        scenarios,
        sensitivityParams,
        contingencyPlans,
        timestamp: new Date().toISOString()
      };
      
      if (typeof onComplete === 'function') {
        onComplete(data);
      }
      
      localStorage.setItem('scenarioPlanningData', JSON.stringify(data));
      
      // Dispatch phase completion event
      window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
        detail: { phaseId: 'phase4' } 
      }));
      
      alert('Phase 4 completed! Synthesis phase is now unlocked.');
      setTimeout(() => navigate('/deep-dive/synthesis'), 1000);
    } else {
      let missing = [];
      if (!hasScenarios) missing.push('at least 3 scenarios');
      if (!hasContingencyPlans) missing.push('contingency plans');
      if (!hasRiskProbabilities) missing.push('risk probabilities for scenarios');
      alert(`Please complete the following before marking this phase as complete: ${missing.join(', ')}`);
    }
  };

  const renderScenarios = () => {
    const currentScenario = scenarios.find(s => s.id === selectedScenario);
    if (!currentScenario) return null;

    return (
      <div className={styles.scenariosTab}>
        <div className={styles.scenarioSelector}>
          <label>Active Scenario:</label>
          <select 
            value={selectedScenario} 
            onChange={(e) => setSelectedScenario(e.target.value)}
            className={styles.select}
          >
            {scenarios.map(scenario => (
              <option key={scenario.id} value={scenario.id}>
                {scenario.name} ({scenario.probability}%)
              </option>
            ))}
          </select>
        </div>

        <div className={styles.scenarioDetails}>
          <h3>{currentScenario.name}</h3>
          <p className={styles.description}>{currentScenario.description}</p>
          
          <div className={styles.probabilityControl}>
            <label>Probability: {currentScenario.probability}%</label>
            <input
              type="range"
              min="0"
              max="100"
              value={currentScenario.probability}
              onChange={(e) => updateScenarioProbability(currentScenario.id, Number(e.target.value))}
              className={styles.slider}
            />
          </div>

          <div className={styles.scenarioContent}>
            <div className={styles.section}>
              <h4>Key Assumptions</h4>
              <ul>
                {currentScenario.assumptions.map((assumption, index) => (
                  <li key={index}>{assumption}</li>
                ))}
              </ul>
            </div>

            <div className={styles.section}>
              <h4>Positive Triggers</h4>
              <ul className={styles.positiveTriggers}>
                {currentScenario.triggers.positive.map((trigger, index) => (
                  <li key={index}>{trigger}</li>
                ))}
              </ul>
            </div>

            {currentScenario.triggers.negative.length > 0 && (
              <div className={styles.section}>
                <h4>Negative Triggers</h4>
                <ul className={styles.negativeTriggers}>
                  {currentScenario.triggers.negative.map((trigger, index) => (
                    <li key={index}>{trigger}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className={styles.section}>
              <h4>Financial Projections (5 Years)</h4>
              <div className={styles.financialTable}>
                <table>
                  <thead>
                    <tr>
                      <th>Metric</th>
                      <th>Year 1</th>
                      <th>Year 2</th>
                      <th>Year 3</th>
                      <th>Year 4</th>
                      <th>Year 5</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Revenue ($k)</td>
                      {currentScenario.financials.revenue.map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                    <tr>
                      <td>Costs ($k)</td>
                      {currentScenario.financials.costs.map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                    <tr>
                      <td>Profit ($k)</td>
                      {currentScenario.financials.profit.map((val, i) => (
                        <td key={i} className={val < 0 ? styles.negative : styles.positive}>
                          {val}
                        </td>
                      ))}
                    </tr>
                    <tr>
                      <td>Market Share (%)</td>
                      {currentScenario.financials.marketShare.map((val, i) => (
                        <td key={i}>{val}</td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {currentScenario.risks.length > 0 && (
              <div className={styles.section}>
                <h4>Key Risks</h4>
                <div className={styles.risks}>
                  {currentScenario.risks.map(risk => (
                    <div key={risk.id} className={styles.riskCard}>
                      <h5>{risk.name}</h5>
                      <div className={styles.riskMetrics}>
                        <span>Impact: {risk.impact}/10</span>
                        <span>Likelihood: {risk.likelihood}/10</span>
                      </div>
                      <p>Mitigation: {risk.mitigation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderSensitivity = () => {
    return (
      <div className={styles.sensitivityTab}>
        <h3>Sensitivity Analysis</h3>
        <p className={styles.description}>
          Adjust parameters to see their impact on outcomes
        </p>

        <div className={styles.parameters}>
          {sensitivityParams.map(param => (
            <div key={param.id} className={styles.parameter}>
              <div className={styles.paramHeader}>
                <h4>{param.name}</h4>
                <span className={styles.category}>{param.category}</span>
              </div>
              
              <div className={styles.paramControl}>
                <span className={styles.min}>{param.min}{param.unit}</span>
                <input
                  type="range"
                  min={param.min}
                  max={param.max}
                  value={param.currentValue}
                  onChange={(e) => updateSensitivityParam(param.id, Number(e.target.value))}
                  className={styles.slider}
                />
                <span className={styles.max}>{param.max}{param.unit}</span>
              </div>
              
              <div className={styles.paramValue}>
                Current: {param.currentValue}{param.unit}
                {param.currentValue !== param.baseValue && (
                  <span className={styles.variance}>
                    ({param.currentValue > param.baseValue ? '+' : ''}{param.currentValue - param.baseValue}{param.unit})
                  </span>
                )}
              </div>
              
              <div className={styles.paramImpact}>
                <span>Impact: {param.impact === 'revenue' ? 'Revenue' : param.impact === 'cost' ? 'Cost' : 'Both'}</span>
                <span>Sensitivity: {param.sensitivity > 0 ? '+' : ''}{(param.sensitivity * 100).toFixed(0)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderContingency = () => {
    return (
      <div className={styles.contingencyTab}>
        <div className={styles.contingencyHeader}>
          <h3>Contingency Planning</h3>
          <button onClick={addContingencyPlan} className={styles.addButton}>
            Add Plan
          </button>
        </div>

        <div className={styles.contingencyPlans}>
          {contingencyPlans.map(plan => (
            <div key={plan.id} className={styles.contingencyCard}>
              <div className={styles.planHeader}>
                <input
                  type="text"
                  value={plan.trigger}
                  onChange={(e) => updateContingencyPlan(plan.id, { trigger: e.target.value })}
                  placeholder="Trigger Event"
                  className={styles.input}
                />
                <span className={`${styles.status} ${styles[plan.status]}`}>
                  {plan.status}
                </span>
              </div>

              <input
                type="text"
                value={plan.condition}
                onChange={(e) => updateContingencyPlan(plan.id, { condition: e.target.value })}
                placeholder="Activation Condition"
                className={styles.input}
              />

              <div className={styles.planDetails}>
                <div className={styles.detailSection}>
                  <label>Actions:</label>
                  <ul>
                    {plan.actions.map((action, index) => (
                      <li key={index}>{action}</li>
                    ))}
                  </ul>
                </div>

                <div className={styles.detailRow}>
                  <input
                    type="text"
                    value={plan.timeline}
                    onChange={(e) => updateContingencyPlan(plan.id, { timeline: e.target.value })}
                    placeholder="Timeline"
                    className={styles.smallInput}
                  />
                  <input
                    type="text"
                    value={plan.owner}
                    onChange={(e) => updateContingencyPlan(plan.id, { owner: e.target.value })}
                    placeholder="Owner"
                    className={styles.smallInput}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className={styles.scenarioPlanning}>
      <div className={styles.header}>
        <h2>Scenario Planning & Risk Analysis</h2>
        <p>Plan for multiple futures and prepare contingencies</p>
      </div>

      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'scenarios' ? styles.active : ''}`}
          onClick={() => setActiveTab('scenarios')}
        >
          Scenarios
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'sensitivity' ? styles.active : ''}`}
          onClick={() => setActiveTab('sensitivity')}
        >
          Sensitivity Analysis
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'contingency' ? styles.active : ''}`}
          onClick={() => setActiveTab('contingency')}
        >
          Contingency Planning
        </button>
      </div>

      <div className={styles.content}>
        {activeTab === 'scenarios' && renderScenarios()}
        {activeTab === 'sensitivity' && renderSensitivity()}
        {activeTab === 'contingency' && renderContingency()}
      </div>

      <div className={styles.actions}>
        <button 
          onClick={() => navigate('/deep-dive/phase3')}
          className={styles.backButton}
        >
          Back to Phase 3
        </button>
        <button 
          onClick={handleCompletePhase}
          className={styles.completeButton}
        >
          Complete Phase 4
        </button>
      </div>
    </div>
  );
};

export default ScenarioPlanning;