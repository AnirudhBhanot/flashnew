import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './FrameworkImplementation.module.scss';
import { Icon } from '../design-system/components';
import { apiRequest } from '../services/api';
import useAssessmentStore from '../store/assessmentStore';

interface FrameworkPosition {
  position: string;
  coordinates?: { x: number; y: number };
  score?: number;
  quadrant?: string;
  stage?: string;
}

interface FrameworkInsight {
  title: string;
  description: string;
  severity: 'critical' | 'important' | 'informational';
  data_points: string[];
}

interface FrameworkAction {
  action: string;
  priority: 'immediate' | 'short-term' | 'long-term';
  impact: 'high' | 'medium' | 'low';
  effort: 'high' | 'medium' | 'low';
  specific_steps: string[];
  constraints_considered: string[];
}

interface FrameworkAnalysis {
  framework_name: string;
  position: FrameworkPosition;
  insights: FrameworkInsight[];
  actions: FrameworkAction[];
  visualization: any;
  raw_metrics?: any;
}

interface Props {
  frameworkId: string;
  onClose?: () => void;
}

export const FrameworkImplementation: React.FC<Props> = ({ frameworkId, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<FrameworkAnalysis | null>(null);
  const [activeTab, setActiveTab] = useState<'position' | 'insights' | 'actions'>('position');
  
  const assessmentData = useAssessmentStore(state => state.data);

  useEffect(() => {
    loadFrameworkAnalysis();
  }, [frameworkId]);

  const loadFrameworkAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simulate API call with mock data
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Generate mock analysis based on framework type
      const mockAnalysis = generateMockAnalysis(frameworkId);
      setAnalysis(mockAnalysis);
      
    } catch (err) {
      console.error('Error loading framework analysis:', err);
      setError('Unable to generate framework analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateMockAnalysis = (framework: string): FrameworkAnalysis => {
    const mockData: Record<string, FrameworkAnalysis> = {
      bcg_matrix: {
        framework_name: 'BCG Growth-Share Matrix',
        position: {
          position: 'Question Mark',
          score: 2.8,
          quadrant: 'High Growth, Low Share'
        },
        insights: [
          {
            title: 'High Growth Market Position',
            description: 'Your startup operates in a rapidly growing market (15%+ annual growth), but currently holds a low market share (<5%).',
            severity: 'important',
            data_points: ['Market growing at 18% YoY', 'Current market share: 3.2%', 'Competitor average: 8.5%']
          },
          {
            title: 'Investment Requirements',
            description: 'Question Marks require significant investment to gain market share and potentially become Stars.',
            severity: 'critical',
            data_points: ['Burn rate: $150k/month', 'CAC: $85', 'Runway: 12 months']
          },
          {
            title: 'Strategic Decision Point',
            description: 'You must decide whether to invest heavily to capture market share or divest and focus resources elsewhere.',
            severity: 'important',
            data_points: ['Break-even requires 15% market share', 'Investment needed: $2-3M', 'Time to profitability: 18-24 months']
          }
        ],
        actions: [
          {
            action: 'Accelerate customer acquisition',
            priority: 'immediate',
            impact: 'high',
            effort: 'high',
            specific_steps: [
              'Double marketing budget for next 6 months',
              'Implement referral program with 20% incentive',
              'Launch targeted campaigns in top 3 segments'
            ],
            constraints_considered: ['Limited runway', 'Current burn rate', 'Team capacity']
          },
          {
            action: 'Improve product differentiation',
            priority: 'short-term',
            impact: 'high',
            effort: 'medium',
            specific_steps: [
              'Conduct competitor feature analysis',
              'Identify 3 unique value propositions',
              'Build distinctive features within 90 days'
            ],
            constraints_considered: ['Development resources', 'Technical debt']
          }
        ],
        visualization: {
          type: 'matrix_2x2',
          axes: {
            x: { label: 'Relative Market Share', range: [0.1, 10] },
            y: { label: 'Market Growth Rate', range: [0, 25] }
          },
          data_point: {
            x: 0.4,
            y: 18,
            size: 30,
            label: 'Your Position'
          }
        },
        raw_metrics: {
          market_growth_rate: 18,
          relative_market_share: 0.4,
          revenue_growth: 120,
          profitability: -45
        }
      },
      porters_five_forces: {
        framework_name: "Porter's Five Forces",
        position: {
          position: 'Moderately Attractive Industry',
          score: 3.2
        },
        insights: [
          {
            title: 'High Competitive Rivalry',
            description: 'The industry shows intense competition with multiple well-funded players fighting for market share.',
            severity: 'critical',
            data_points: ['15+ direct competitors', '3 unicorns in space', 'Price competition increasing']
          },
          {
            title: 'Low Barriers to Entry',
            description: 'New entrants can easily enter the market with minimal capital requirements and technical barriers.',
            severity: 'important',
            data_points: ['$500k minimum to start', 'No regulatory barriers', 'Open source alternatives available']
          },
          {
            title: 'Moderate Buyer Power',
            description: 'Customers have growing negotiation power due to multiple alternatives and low switching costs.',
            severity: 'important',
            data_points: ['Switching cost: <$1000', 'Contract length: 12 months avg', 'Churn rate: 5% monthly']
          }
        ],
        actions: [
          {
            action: 'Build switching costs',
            priority: 'immediate',
            impact: 'high',
            effort: 'medium',
            specific_steps: [
              'Implement data lock-in features',
              'Create proprietary integrations',
              'Develop customer success program'
            ],
            constraints_considered: ['User experience', 'Regulatory compliance']
          }
        ],
        visualization: {
          type: 'force_analysis',
          forces: [
            { name: 'Competitive Rivalry', strength: 4.2, max: 5 },
            { name: 'Threat of New Entry', strength: 3.8, max: 5 },
            { name: 'Buyer Power', strength: 3.5, max: 5 },
            { name: 'Supplier Power', strength: 2.1, max: 5 },
            { name: 'Threat of Substitutes', strength: 3.2, max: 5 }
          ],
          overall_attractiveness: 'Moderate'
        },
        raw_metrics: {}
      },
      swot_analysis: {
        framework_name: 'SWOT Analysis',
        position: {
          position: 'Growth Stage with Clear Opportunities'
        },
        insights: [
          {
            title: 'Key Strengths to Leverage',
            description: 'Strong technical team and innovative product features provide competitive advantages.',
            severity: 'informational',
            data_points: ['85% engineering team', 'Patent pending on core tech', 'NPS score: 72']
          },
          {
            title: 'Critical Weaknesses to Address',
            description: 'Limited market presence and brand recognition are hindering growth.',
            severity: 'important',
            data_points: ['Brand awareness: 12%', 'Marketing spend: 8% of revenue', 'Sales team: 2 people']
          }
        ],
        actions: [
          {
            action: 'Capitalize on technical strengths',
            priority: 'immediate',
            impact: 'high',
            effort: 'low',
            specific_steps: [
              'Launch developer API program',
              'Create technical content marketing',
              'Host webinars showcasing innovation'
            ],
            constraints_considered: []
          }
        ],
        visualization: {
          type: 'canvas',
          blocks: {
            strengths: {
              score: 4.2,
              content: ['Strong technical team', 'Innovative product', 'Good unit economics']
            },
            weaknesses: {
              score: 2.8,
              content: ['Limited brand awareness', 'Small sales team', 'Geographic concentration']
            },
            opportunities: {
              score: 4.5,
              content: ['Growing market', 'Partnership opportunities', 'International expansion']
            },
            threats: {
              score: 3.2,
              content: ['Well-funded competitors', 'Economic uncertainty', 'Regulatory changes']
            }
          },
          completion_score: 85,
          strength_score: 3.7
        },
        raw_metrics: {}
      },
      value_chain: {
        framework_name: 'Value Chain Analysis',
        position: {
          position: 'Strong in Core Activities, Weak in Support'
        },
        insights: [
          {
            title: 'Technology Development Excellence',
            description: 'Your R&D and product development processes are highly efficient and innovative.',
            severity: 'informational',
            data_points: ['Dev velocity: 95th percentile', 'Time to feature: 2 weeks', 'Bug rate: 0.3%']
          },
          {
            title: 'Marketing & Sales Gaps',
            description: 'Outbound activities are underdeveloped, limiting market reach and customer acquisition.',
            severity: 'critical',
            data_points: ['Lead gen cost: $200', 'Conversion rate: 2%', 'Sales cycle: 45 days']
          }
        ],
        actions: [
          {
            action: 'Strengthen go-to-market capabilities',
            priority: 'immediate',
            impact: 'high',
            effort: 'high',
            specific_steps: [
              'Hire VP of Sales within 30 days',
              'Implement CRM and sales process',
              'Create sales enablement materials'
            ],
            constraints_considered: ['Budget constraints', 'Hiring market conditions']
          }
        ],
        visualization: {
          type: 'canvas',
          blocks: {
            inbound_logistics: { score: 3.5 },
            operations: { score: 4.5 },
            outbound_logistics: { score: 2.8 },
            marketing_sales: { score: 2.2 },
            service: { score: 3.8 },
            technology: { score: 4.8 },
            hr_management: { score: 3.2 },
            infrastructure: { score: 3.5 }
          },
          completion_score: 78,
          strength_score: 3.5
        },
        raw_metrics: {}
      },
      business_model_canvas: {
        framework_name: 'Business Model Canvas',
        position: {
          position: 'B2B SaaS Model with Subscription Revenue'
        },
        insights: [
          {
            title: 'Revenue Model Validation',
            description: 'Subscription model showing strong unit economics with improving retention.',
            severity: 'informational',
            data_points: ['MRR: $125k', 'ARPU: $250', 'LTV:CAC ratio: 3.2']
          },
          {
            title: 'Customer Segment Focus Needed',
            description: 'Serving too many segments dilutes value proposition and increases complexity.',
            severity: 'important',
            data_points: ['5 target segments', 'Segment performance varies 300%', 'Support costs increasing']
          }
        ],
        actions: [
          {
            action: 'Focus on top 2 customer segments',
            priority: 'short-term',
            impact: 'high',
            effort: 'medium',
            specific_steps: [
              'Analyze segment profitability',
              'Identify highest LTV segments',
              'Reallocate resources to focus segments'
            ],
            constraints_considered: ['Existing customer commitments']
          }
        ],
        visualization: {
          type: 'canvas',
          blocks: {
            key_partners: { score: 3.5, content: ['Technology providers', 'Channel partners', 'Integration partners'] },
            key_activities: { score: 4.2, content: ['Product development', 'Customer success', 'Sales'] },
            value_propositions: { score: 3.8, content: ['Time savings', 'Cost reduction', 'Better insights'] },
            customer_relationships: { score: 3.2, content: ['Self-service', 'Dedicated support', 'Community'] },
            customer_segments: { score: 2.8, content: ['SMBs', 'Mid-market', 'Enterprise', 'Startups', 'Agencies'] },
            channels: { score: 2.5, content: ['Direct sales', 'Website', 'Partners'] },
            cost_structure: { score: 3.5, content: ['Engineering: 45%', 'Sales: 25%', 'Marketing: 15%', 'Other: 15%'] },
            revenue_streams: { score: 4.0, content: ['Subscriptions: 85%', 'Services: 10%', 'One-time: 5%'] }
          },
          completion_score: 82,
          strength_score: 3.5
        },
        raw_metrics: {}
      },
      blue_ocean_strategy: {
        framework_name: 'Blue Ocean Strategy',
        position: {
          position: 'Red Ocean - Competing in Existing Market'
        },
        insights: [
          {
            title: 'High Competition in Current Market',
            description: 'Operating in a crowded market with established competitors and commoditizing features.',
            severity: 'critical',
            data_points: ['Feature parity: 85%', 'Price competition increasing', 'Differentiation score: 2.5/5']
          },
          {
            title: 'Blue Ocean Opportunities Identified',
            description: 'Adjacent markets show unmet needs that align with your capabilities.',
            severity: 'informational',
            data_points: ['3 underserved segments found', 'TAM expansion: $500M', 'No direct competition']
          }
        ],
        actions: [
          {
            action: 'Pivot to blue ocean opportunity',
            priority: 'short-term',
            impact: 'high',
            effort: 'high',
            specific_steps: [
              'Validate unmet needs with 50 customers',
              'Develop MVP for new segment',
              'Test pricing 2x current levels'
            ],
            constraints_considered: ['Existing product roadmap', 'Current customer needs']
          }
        ],
        visualization: {
          type: 'canvas',
          blocks: {
            eliminate: { score: 3.0, content: ['Complex features', 'Long implementation', 'Customization options'] },
            reduce: { score: 3.5, content: ['Price point', 'Feature set', 'Support requirements'] },
            raise: { score: 4.0, content: ['Ease of use', 'Time to value', 'Mobile experience'] },
            create: { score: 4.5, content: ['AI automation', 'Predictive insights', 'Industry templates'] }
          },
          completion_score: 75,
          strength_score: 3.8
        },
        raw_metrics: {}
      }
    };

    return mockData[framework] || mockData.bcg_matrix;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return styles.critical;
      case 'important': return styles.important;
      case 'informational': return styles.informational;
      default: return '';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'immediate': return styles.immediate;
      case 'short-term': return styles.shortTerm;
      case 'long-term': return styles.longTerm;
      default: return '';
    }
  };

  const renderVisualization = () => {
    if (!analysis?.visualization) return null;

    const { type, ...vizData } = analysis.visualization;

    switch (type) {
      case 'matrix_2x2':
        return <BCGMatrixVisualization data={vizData} position={analysis.position} />;
      case 'force_analysis':
        return <FiveForcesDiagram data={vizData} />;
      case 'canvas':
        return <CanvasVisualization data={vizData} />;
      default:
        return <div className={styles.pendingVisualization}>Visualization coming soon</div>;
    }
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <Icon name="arrow.clockwise" size={32} className={styles.spinner} />
        <p>Analyzing your data with {frameworkId.replace(/_/g, ' ')}...</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className={styles.error}>
        <Icon name="exclamationmark.triangle" size={32} />
        <p>{error || 'Unable to load analysis'}</p>
        <button onClick={loadFrameworkAnalysis}>Try Again</button>
      </div>
    );
  }

  return (
    <motion.div 
      className={styles.container}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h2>{analysis.framework_name}</h2>
          <p className={styles.position}>
            Your Position: <strong>{analysis.position.position}</strong>
            {analysis.position.score && (
              <span className={styles.score}> (Score: {analysis.position.score.toFixed(1)})</span>
            )}
          </p>
        </div>
        {onClose && (
          <button className={styles.closeButton} onClick={onClose}>
            <Icon name="xmark" size={20} />
          </button>
        )}
      </div>

      <div className={styles.tabs}>
        <button 
          className={`${styles.tab} ${activeTab === 'position' ? styles.active : ''}`}
          onClick={() => setActiveTab('position')}
        >
          <Icon name="chart.pie" size={16} />
          Position Analysis
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'insights' ? styles.active : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          <Icon name="lightbulb" size={16} />
          Key Insights ({analysis.insights.length})
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'actions' ? styles.active : ''}`}
          onClick={() => setActiveTab('actions')}
        >
          <Icon name="checklist" size={16} />
          Action Items ({analysis.actions.length})
        </button>
      </div>

      <div className={styles.content}>
        <AnimatePresence mode="wait">
          {activeTab === 'position' && (
            <motion.div
              key="position"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className={styles.positionTab}
            >
              <div className={styles.visualization}>
                {renderVisualization()}
              </div>
              {analysis.raw_metrics && (
                <div className={styles.metrics}>
                  <h3>Key Metrics</h3>
                  <div className={styles.metricsGrid}>
                    {Object.entries(analysis.raw_metrics).map(([key, value]) => (
                      <div key={key} className={styles.metric}>
                        <span className={styles.metricLabel}>
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                        <span className={styles.metricValue}>
                          {typeof value === 'number' ? 
                            value % 1 === 0 ? value.toLocaleString() : value.toFixed(2)
                            : value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'insights' && (
            <motion.div
              key="insights"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className={styles.insightsTab}
            >
              {analysis.insights.map((insight, index) => (
                <div 
                  key={index} 
                  className={`${styles.insightCard} ${getSeverityColor(insight.severity)}`}
                >
                  <div className={styles.insightHeader}>
                    <Icon 
                      name={insight.severity === 'critical' ? 'exclamationmark.circle.fill' : 
                            insight.severity === 'important' ? 'info.circle.fill' : 
                            'lightbulb.fill'} 
                      size={20} 
                    />
                    <h4>{insight.title}</h4>
                  </div>
                  <p className={styles.insightDescription}>{insight.description}</p>
                  {insight.data_points.length > 0 && (
                    <div className={styles.dataPoints}>
                      {insight.data_points.map((point, idx) => (
                        <span key={idx} className={styles.dataPoint}>{point}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </motion.div>
          )}

          {activeTab === 'actions' && (
            <motion.div
              key="actions"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className={styles.actionsTab}
            >
              {analysis.actions.map((action, index) => (
                <div key={index} className={styles.actionCard}>
                  <div className={styles.actionHeader}>
                    <h4>{action.action}</h4>
                    <div className={styles.actionTags}>
                      <span className={`${styles.tag} ${getPriorityColor(action.priority)}`}>
                        {action.priority}
                      </span>
                      <span className={`${styles.tag} ${styles.impact} ${styles[action.impact]}`}>
                        {action.impact} impact
                      </span>
                      <span className={`${styles.tag} ${styles.effort} ${styles[action.effort]}`}>
                        {action.effort} effort
                      </span>
                    </div>
                  </div>
                  
                  <div className={styles.actionContent}>
                    <div className={styles.steps}>
                      <h5>Specific Steps:</h5>
                      <ol>
                        {action.specific_steps.map((step, idx) => (
                          <li key={idx}>{step}</li>
                        ))}
                      </ol>
                    </div>
                    
                    {action.constraints_considered.length > 0 && (
                      <div className={styles.constraints}>
                        <h5>Constraints Considered:</h5>
                        <ul>
                          {action.constraints_considered.map((constraint, idx) => (
                            <li key={idx}>{constraint}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

// BCG Matrix Visualization Component
const BCGMatrixVisualization: React.FC<{ data: any; position: FrameworkPosition }> = ({ data, position }) => {
  const { axes, data_point, quadrants } = data;
  
  // Calculate position on canvas (0-100 scale)
  const xPos = Math.log10(data_point.x + 0.1) / Math.log10(axes.x.range[1]) * 100;
  const yPos = data_point.y / axes.y.range[1] * 100;
  
  return (
    <div className={styles.bcgMatrix}>
      <div className={styles.matrixContainer}>
        <div className={styles.yAxis}>
          <span className={styles.axisLabel}>{axes.y.label}</span>
          <span className={styles.axisHigh}>High</span>
          <span className={styles.axisLow}>Low</span>
        </div>
        
        <div className={styles.matrixGrid}>
          <div className={styles.quadrant} data-quadrant="star">
            <span className={styles.quadrantLabel}>Stars</span>
          </div>
          <div className={styles.quadrant} data-quadrant="question">
            <span className={styles.quadrantLabel}>Question Marks</span>
          </div>
          <div className={styles.quadrant} data-quadrant="cash-cow">
            <span className={styles.quadrantLabel}>Cash Cows</span>
          </div>
          <div className={styles.quadrant} data-quadrant="dog">
            <span className={styles.quadrantLabel}>Dogs</span>
          </div>
          
          <div 
            className={styles.dataPoint}
            style={{
              left: `${xPos}%`,
              bottom: `${yPos}%`,
              width: `${data_point.size}px`,
              height: `${data_point.size}px`
            }}
          >
            <span className={styles.pointLabel}>{data_point.label}</span>
          </div>
        </div>
        
        <div className={styles.xAxis}>
          <span className={styles.axisLow}>Low</span>
          <span className={styles.axisLabel}>{axes.x.label}</span>
          <span className={styles.axisHigh}>High</span>
        </div>
      </div>
    </div>
  );
};

// Five Forces Diagram Component
const FiveForcesDiagram: React.FC<{ data: any }> = ({ data }) => {
  const { forces, overall_attractiveness } = data;
  
  return (
    <div className={styles.fiveForces}>
      <div className={styles.forcesContainer}>
        <div className={styles.centralElement}>
          <h4>Industry Competition</h4>
          <p className={styles.attractiveness}>
            Attractiveness: <strong>{overall_attractiveness}</strong>
          </p>
        </div>
        
        {forces.map((force: any, index: number) => {
          const angle = (index * 72 - 90) * (Math.PI / 180);
          const radius = 150;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;
          
          return (
            <div
              key={force.name}
              className={styles.force}
              style={{
                transform: `translate(${x}px, ${y}px)`
              }}
            >
              <div className={styles.forceName}>{force.name}</div>
              <div className={styles.forceStrength}>
                <div 
                  className={styles.strengthBar}
                  style={{ 
                    width: `${(force.strength / force.max) * 100}%`,
                    backgroundColor: force.strength > 3 ? '#ef4444' : 
                                   force.strength > 2 ? '#f59e0b' : '#10b981'
                  }}
                />
              </div>
              <span className={styles.strengthValue}>{force.strength.toFixed(1)}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Canvas Visualization Component
const CanvasVisualization: React.FC<{ data: any }> = ({ data }) => {
  const { blocks, completion_score, strength_score } = data;
  
  return (
    <div className={styles.canvas}>
      <div className={styles.canvasHeader}>
        <div className={styles.canvasScore}>
          <span>Completion: {completion_score.toFixed(0)}%</span>
          <span>Strength: {strength_score.toFixed(1)}/5</span>
        </div>
      </div>
      
      <div className={styles.canvasGrid}>
        {Object.entries(blocks).map(([key, block]: [string, any]) => (
          <div key={key} className={styles.canvasBlock} data-block={key}>
            <h5>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h5>
            <div className={styles.blockScore}>
              <div 
                className={styles.scoreBar}
                style={{ 
                  width: `${(block.score / 5) * 100}%`,
                  backgroundColor: block.score > 3 ? '#10b981' : 
                                 block.score > 2 ? '#f59e0b' : '#ef4444'
                }}
              />
            </div>
            {block.content && (
              <div className={styles.blockContent}>
                {Array.isArray(block.content) ? (
                  <ul>
                    {block.content.map((item: string, idx: number) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p>{block.content}</p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FrameworkImplementation;