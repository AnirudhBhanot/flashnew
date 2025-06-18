import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicFrameworkAssessment.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Framework-specific interfaces
interface SWOTData {
  strengths: { item: string; impact: 'high' | 'medium' | 'low'; evidence: string; }[];
  weaknesses: { item: string; severity: 'critical' | 'high' | 'medium'; action: string; }[];
  opportunities: { item: string; value: string; timeframe: string; }[];
  threats: { item: string; likelihood: 'high' | 'medium' | 'low'; mitigation: string; }[];
  strategic_implications: string[];
}

interface BCGData {
  position: 'Star' | 'Question Mark' | 'Cash Cow' | 'Dog';
  market_share: number;
  market_growth: number;
  relative_share: number;
  strategic_direction: string;
  investment_priority: 'high' | 'medium' | 'low' | 'divest';
  key_actions: string[];
}

interface PortersForce {
  force: string;
  strength: 'Very Low' | 'Low' | 'Medium' | 'High' | 'Very High';
  score: number;
  key_factors: string[];
  strategic_response: string;
}

interface PortersData {
  forces: PortersForce[];
  overall_attractiveness: number;
  competitive_strategy: string;
  key_success_factors: string[];
}

interface AnsoffData {
  current_strategy: 'Market Penetration' | 'Market Development' | 'Product Development' | 'Diversification';
  recommended_strategy: string;
  risk_level: 'low' | 'medium' | 'high' | 'very high';
  implementation_steps: { step: string; timeline: string; investment: string; }[];
  expected_outcomes: string[];
}

interface ValueChainData {
  primary_activities: { activity: string; strength: number; improvement_potential: string; }[];
  support_activities: { activity: string; strength: number; improvement_potential: string; }[];
  competitive_advantages: string[];
  value_creation_opportunities: string[];
}

interface FrameworkAssessment {
  framework_id: string;
  framework_name: string;
  assessment_data: SWOTData | BCGData | PortersData | AnsoffData | ValueChainData | any;
  key_insights: string[];
  recommendations: { action: string; priority: 'immediate' | 'short-term' | 'medium-term'; impact: 'high' | 'medium' | 'low'; }[];
}

const StrategicFrameworkAssessment: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [assessments, setAssessments] = useState<FrameworkAssessment[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string>('');
  const [viewMode, setViewMode] = useState<'individual' | 'integrated'>('individual');
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    console.log('StrategicFrameworkAssessment - assessmentData:', assessmentData);
    console.log('StrategicFrameworkAssessment - results:', results);
    if (assessmentData || results) {
      loadFrameworkAssessments();
    }
  }, [assessmentData, results]);

  const loadFrameworkAssessments = async () => {
    setIsLoading(true);
    console.log('loadFrameworkAssessments called');
    
    try {
      // Try API first
      const response = await fetch(`${API_URL}/api/frameworks/intelligent-analysis`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assessment_data: assessmentData,
          max_frameworks: 5,
          include_detailed_analysis: true
        })
      });

      console.log('API response status:', response.status);
      if (response.ok) {
        const data = await response.json();
        console.log('API response data:', data);
        // Transform API response to our format
        const frameworkAssessments = transformApiResponse(data);
        setAssessments(frameworkAssessments);
      } else {
        console.log('API failed, generating local assessments');
        // Generate assessments locally
        generateLocalAssessments();
      }
    } catch (error) {
      console.error('Error loading assessments:', error);
      generateLocalAssessments();
    } finally {
      setIsLoading(false);
    }
  };

  const transformApiResponse = (apiData: any): FrameworkAssessment[] => {
    // Transform API response to match our interface
    return apiData.frameworks.map((fw: any) => ({
      framework_id: fw.framework_id,
      framework_name: fw.framework_name,
      assessment_data: fw.analysis || {},
      key_insights: fw.customizations || [],
      recommendations: fw.quick_wins?.map((win: string) => ({
        action: win,
        priority: 'immediate',
        impact: 'high'
      })) || []
    }));
  };

  const generateLocalAssessments = () => {
    console.log('generateLocalAssessments called');
    const company = {
      name: assessmentData?.companyInfo?.companyName || 'Company',
      stage: assessmentData?.capital?.fundingStage || 'seed',
      revenue: assessmentData?.capital?.annualRevenue || 0,
      burn: assessmentData?.capital?.monthlyBurn || 50000,
      runway: assessmentData?.capital?.runwayMonths || 12,
      cash: assessmentData?.capital?.cashOnHand || 600000,
      marketGrowth: assessmentData?.market?.marketGrowthRate || 20,
      marketShare: assessmentData?.market?.som && assessmentData?.market?.sam 
        ? (assessmentData.market.som / assessmentData.market.sam * 100) : 0.5,
      competitors: assessmentData?.market?.competitorCount || 10,
      teamSize: assessmentData?.people?.fullTimeEmployees || 10,
      churn: assessmentData?.advantage?.churnRate || 5,
      nps: assessmentData?.advantage?.npsScore || 30,
      productStage: assessmentData?.advantage?.productStage || 'mvp'
    };
    console.log('Company data:', company);

    const assessments: FrameworkAssessment[] = [];

    // 1. SWOT Analysis
    const swotData: SWOTData = {
      strengths: [
        {
          item: company.runway > 12 ? 'Strong financial position' : 'Lean operations',
          impact: company.runway > 18 ? 'high' : 'medium',
          evidence: `${company.runway} months runway, $${(company.cash/1000).toFixed(0)}k cash`
        },
        {
          item: 'Agile team structure',
          impact: company.teamSize < 20 ? 'high' : 'medium',
          evidence: `${company.teamSize} person team enables rapid iteration`
        },
        {
          item: company.nps > 50 ? 'Strong customer satisfaction' : 'Growing customer base',
          impact: company.nps > 50 ? 'high' : 'medium',
          evidence: `NPS: ${company.nps}, Churn: ${company.churn}%`
        }
      ],
      weaknesses: [
        {
          item: company.burn > company.revenue/12 ? 'High burn rate' : 'Limited resources',
          severity: company.runway < 6 ? 'critical' : company.runway < 12 ? 'high' : 'medium',
          action: 'Implement cost optimization program'
        },
        {
          item: 'Limited market presence',
          severity: company.marketShare < 1 ? 'high' : 'medium',
          action: 'Launch aggressive customer acquisition campaign'
        }
      ],
      opportunities: [
        {
          item: `${company.marketGrowth}% market growth rate`,
          value: '$1B+ TAM opportunity',
          timeframe: '2-3 years'
        },
        {
          item: 'AI/automation adoption',
          value: '40% cost reduction potential',
          timeframe: '6-12 months'
        }
      ],
      threats: [
        {
          item: `${company.competitors}+ competitors in market`,
          likelihood: company.competitors > 20 ? 'high' : 'medium',
          mitigation: 'Build defensible moats through network effects'
        },
        {
          item: 'Funding environment uncertainty',
          likelihood: 'medium',
          mitigation: 'Extend runway to 24+ months'
        }
      ],
      strategic_implications: [
        'Focus on strengths to capture market opportunity',
        'Address burn rate before next funding round',
        'Build competitive moats while market is fragmented'
      ]
    };

    assessments.push({
      framework_id: 'swot',
      framework_name: 'SWOT Analysis',
      assessment_data: swotData,
      key_insights: [
        `Key strength: ${swotData.strengths[0].item} provides competitive advantage`,
        `Critical weakness: ${swotData.weaknesses[0].item} threatens sustainability`,
        `Major opportunity: Market growing at ${company.marketGrowth}% annually`
      ],
      recommendations: [
        {
          action: swotData.weaknesses[0].action,
          priority: 'immediate',
          impact: 'high'
        },
        {
          action: 'Double down on product differentiation',
          priority: 'short-term',
          impact: 'high'
        }
      ]
    });

    // 2. BCG Matrix
    const bcgData: BCGData = {
      position: company.marketGrowth > 20 && company.marketShare > 10 ? 'Star' :
                company.marketGrowth > 20 && company.marketShare <= 10 ? 'Question Mark' :
                company.marketGrowth <= 20 && company.marketShare > 10 ? 'Cash Cow' : 'Dog',
      market_share: company.marketShare,
      market_growth: company.marketGrowth,
      relative_share: company.marketShare / (100 / company.competitors),
      strategic_direction: company.marketGrowth > 20 ? 'Invest for growth' : 'Optimize for profitability',
      investment_priority: company.marketGrowth > 20 && company.marketShare < 10 ? 'high' : 'medium',
      key_actions: [
        'Increase marketing spend to capture market share',
        'Focus on customer retention to improve unit economics',
        'Build scalable infrastructure for growth'
      ]
    };

    assessments.push({
      framework_id: 'bcg_matrix',
      framework_name: 'BCG Growth-Share Matrix',
      assessment_data: bcgData,
      key_insights: [
        `Positioned as ${bcgData.position} - ${bcgData.strategic_direction}`,
        `Market share of ${bcgData.market_share.toFixed(1)}% in ${bcgData.market_growth}% growth market`,
        `Investment priority: ${bcgData.investment_priority}`
      ],
      recommendations: bcgData.key_actions.map((action, i) => ({
        action,
        priority: i === 0 ? 'immediate' : 'short-term',
        impact: 'high'
      }))
    });

    // 3. Porter's Five Forces
    const portersData: PortersData = {
      forces: [
        {
          force: 'Threat of New Entrants',
          strength: company.marketGrowth > 25 ? 'High' : 'Medium',
          score: company.marketGrowth > 25 ? 4 : 3,
          key_factors: [
            'Low barriers to entry',
            'Attractive market growth',
            'Limited regulatory barriers'
          ],
          strategic_response: 'Build switching costs and network effects'
        },
        {
          force: 'Bargaining Power of Buyers',
          strength: company.churn > 5 ? 'High' : 'Medium',
          score: company.churn > 5 ? 4 : 3,
          key_factors: [
            'Multiple alternatives available',
            'Low switching costs',
            'Price sensitivity'
          ],
          strategic_response: 'Increase product stickiness through integrations'
        },
        {
          force: 'Bargaining Power of Suppliers',
          strength: 'Low',
          score: 2,
          key_factors: [
            'Commoditized cloud infrastructure',
            'Multiple vendor options',
            'Standard components'
          ],
          strategic_response: 'Maintain multi-vendor strategy'
        },
        {
          force: 'Threat of Substitutes',
          strength: 'Medium',
          score: 3,
          key_factors: [
            'In-house development',
            'Open source alternatives',
            'Manual processes'
          ],
          strategic_response: 'Focus on unique value proposition'
        },
        {
          force: 'Competitive Rivalry',
          strength: company.competitors > 20 ? 'Very High' : 'High',
          score: company.competitors > 20 ? 5 : 4,
          key_factors: [
            `${company.competitors} direct competitors`,
            'Feature parity common',
            'Price competition'
          ],
          strategic_response: 'Differentiate through superior execution'
        }
      ],
      overall_attractiveness: 3.2,
      competitive_strategy: 'Differentiation Focus',
      key_success_factors: [
        'Speed of innovation',
        'Customer success',
        'Product-market fit',
        'Operational efficiency'
      ]
    };

    assessments.push({
      framework_id: 'porters_five_forces',
      framework_name: "Porter's Five Forces",
      assessment_data: portersData,
      key_insights: [
        `Industry attractiveness: ${portersData.overall_attractiveness}/5`,
        `Highest threat: ${portersData.forces.find(f => f.score === Math.max(...portersData.forces.map(f => f.score)))?.force}`,
        `Recommended strategy: ${portersData.competitive_strategy}`
      ],
      recommendations: [
        {
          action: 'Build competitive moats through network effects',
          priority: 'immediate',
          impact: 'high'
        },
        {
          action: 'Increase switching costs through deep integrations',
          priority: 'short-term',
          impact: 'high'
        }
      ]
    });

    // 4. Ansoff Matrix
    const ansoffData: AnsoffData = {
      current_strategy: company.productStage === 'mvp' ? 'Market Penetration' : 'Product Development',
      recommended_strategy: company.marketShare < 5 ? 'Market Penetration' : 'Market Development',
      risk_level: 'medium',
      implementation_steps: [
        {
          step: 'Maximize current market opportunity',
          timeline: '0-6 months',
          investment: '$500k-1M'
        },
        {
          step: 'Expand to adjacent customer segments',
          timeline: '6-12 months',
          investment: '$1-2M'
        },
        {
          step: 'Launch complementary products',
          timeline: '12-18 months',
          investment: '$2-5M'
        }
      ],
      expected_outcomes: [
        '10x revenue growth in 18 months',
        'Market leadership in core segment',
        '3 new revenue streams'
      ]
    };

    assessments.push({
      framework_id: 'ansoff_matrix',
      framework_name: 'Ansoff Growth Matrix',
      assessment_data: ansoffData,
      key_insights: [
        `Current strategy: ${ansoffData.current_strategy}`,
        `Recommended pivot to: ${ansoffData.recommended_strategy}`,
        `Risk level: ${ansoffData.risk_level}`
      ],
      recommendations: ansoffData.implementation_steps.map(step => ({
        action: step.step,
        priority: 'short-term' as const,
        impact: 'high' as const
      }))
    });

    // 5. Value Chain Analysis
    const valueChainData: ValueChainData = {
      primary_activities: [
        { activity: 'Product Development', strength: 8, improvement_potential: 'Implement agile/DevOps' },
        { activity: 'Marketing & Sales', strength: 5, improvement_potential: 'Build growth engine' },
        { activity: 'Customer Success', strength: 7, improvement_potential: 'Automate onboarding' },
        { activity: 'Operations', strength: 6, improvement_potential: 'Scale infrastructure' }
      ],
      support_activities: [
        { activity: 'Technology/R&D', strength: 8, improvement_potential: 'AI integration' },
        { activity: 'Human Resources', strength: 6, improvement_potential: 'Talent pipeline' },
        { activity: 'Finance', strength: 7, improvement_potential: 'Unit economics optimization' }
      ],
      competitive_advantages: [
        'Superior product velocity',
        'Customer-centric culture',
        'Lean operations'
      ],
      value_creation_opportunities: [
        'Automate manual processes',
        'Build platform ecosystem',
        'Develop premium tier'
      ]
    };

    assessments.push({
      framework_id: 'value_chain',
      framework_name: 'Value Chain Analysis',
      assessment_data: valueChainData,
      key_insights: [
        `Strongest link: ${valueChainData.primary_activities.reduce((a, b) => a.strength > b.strength ? a : b).activity}`,
        `Weakest link: ${valueChainData.primary_activities.reduce((a, b) => a.strength < b.strength ? a : b).activity}`,
        'Multiple value creation opportunities identified'
      ],
      recommendations: valueChainData.value_creation_opportunities.map(opp => ({
        action: opp,
        priority: 'medium-term' as const,
        impact: 'medium' as const
      }))
    });

    console.log('Generated assessments:', assessments);
    setAssessments(assessments);
    if (assessments.length > 0) {
      setSelectedFramework(assessments[0].framework_id);
    }
    console.log('Selected framework:', assessments[0]?.framework_id);
  };

  const renderSWOTAnalysis = (data: SWOTData) => (
    <div className={styles.swotAnalysis}>
      <div className={styles.swotGrid}>
        <div className={`${styles.swotQuadrant} ${styles.strengths}`}>
          <h4>Strengths</h4>
          <div className={styles.swotItems}>
            {data.strengths.map((s, i) => (
              <div key={i} className={styles.swotItem}>
                <div className={styles.itemText}>{s.item}</div>
                <div className={styles.itemDetail}>
                  <span className={`${styles.badge} ${styles[s.impact]}`}>{s.impact} impact</span>
                  • {s.evidence}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className={`${styles.swotQuadrant} ${styles.weaknesses}`}>
          <h4>Weaknesses</h4>
          <div className={styles.swotItems}>
            {data.weaknesses.map((w, i) => (
              <div key={i} className={styles.swotItem}>
                <div className={styles.itemText}>{w.item}</div>
                <div className={styles.itemDetail}>
                  <span className={`${styles.badge} ${styles[w.severity]}`}>{w.severity}</span>
                  • Action: {w.action}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className={`${styles.swotQuadrant} ${styles.opportunities}`}>
          <h4>Opportunities</h4>
          <div className={styles.swotItems}>
            {data.opportunities.map((o, i) => (
              <div key={i} className={styles.swotItem}>
                <div className={styles.itemText}>{o.item}</div>
                <div className={styles.itemDetail}>
                  {o.value} • {o.timeframe}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className={`${styles.swotQuadrant} ${styles.threats}`}>
          <h4>Threats</h4>
          <div className={styles.swotItems}>
            {data.threats.map((t, i) => (
              <div key={i} className={styles.swotItem}>
                <div className={styles.itemText}>{t.item}</div>
                <div className={styles.itemDetail}>
                  <span className={`${styles.badge} ${styles[t.likelihood]}`}>{t.likelihood} risk</span>
                  • Mitigation: {t.mitigation}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className={styles.implications}>
        <h4>Strategic Implications</h4>
        <ul>
          {data.strategic_implications.map((imp, i) => (
            <li key={i}>{imp}</li>
          ))}
        </ul>
      </div>
    </div>
  );

  const renderBCGMatrix = (data: BCGData) => (
    <div className={styles.bcgMatrix}>
      <h3>BCG Growth-Share Matrix</h3>
      <div className={styles.matrixVisual}>
        <div className={`${styles.quadrant} ${data.position === 'Star' ? styles.current : ''}`}>
          <div className={styles.quadrantLabel}>Star</div>
          <div className={styles.quadrantDesc}>High Growth, High Share</div>
          {data.position === 'Star' && <div className={styles.currentIndicator}>Current</div>}
        </div>
        <div className={`${styles.quadrant} ${data.position === 'Question Mark' ? styles.current : ''}`}>
          <div className={styles.quadrantLabel}>Question Mark</div>
          <div className={styles.quadrantDesc}>High Growth, Low Share</div>
          {data.position === 'Question Mark' && <div className={styles.currentIndicator}>Current</div>}
        </div>
        <div className={`${styles.quadrant} ${data.position === 'Cash Cow' ? styles.current : ''}`}>
          <div className={styles.quadrantLabel}>Cash Cow</div>
          <div className={styles.quadrantDesc}>Low Growth, High Share</div>
          {data.position === 'Cash Cow' && <div className={styles.currentIndicator}>Current</div>}
        </div>
        <div className={`${styles.quadrant} ${data.position === 'Dog' ? styles.current : ''}`}>
          <div className={styles.quadrantLabel}>Dog</div>
          <div className={styles.quadrantDesc}>Low Growth, Low Share</div>
          {data.position === 'Dog' && <div className={styles.currentIndicator}>Current</div>}
        </div>
      </div>
        
      
      <div className={styles.matrixMetrics}>
        <div className={styles.metric}>
          <label>Market Share</label>
          <div className={styles.value}>{data.market_share.toFixed(1)}%</div>
        </div>
        <div className={styles.metric}>
          <label>Market Growth</label>
          <div className={styles.value}>{data.market_growth}% CAGR</div>
        </div>
        <div className={styles.metric}>
          <label>Relative Share</label>
          <div className={styles.value}>{data.relative_share.toFixed(2)}x</div>
        </div>
      </div>
      
      <div className={styles.strategyBox}>
        <h4>Strategic Direction</h4>
        <div className={styles.direction}>{data.strategic_direction}</div>
        <div className={styles.actions}>
          {data.key_actions.map((action, i) => (
            <div key={i} className={styles.action}>
              <div className={styles.actionNumber}>{i + 1}</div>
              <div className={styles.actionText}>{action}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderPortersForces = (data: PortersData) => (
    <div className={styles.portersForces}>
      <h3>Porter's Five Forces Analysis</h3>
      <div className={styles.forcesGrid}>
        {data.forces.map((force, i) => (
          <div key={i} className={styles.forceCard}>
            <div className={styles.forceHeader}>
              <h4>{force.force}</h4>
              <div className={styles.forceStrength}>
                <span className={styles.strengthBadge} data-strength={force.strength}>
                  {force.strength}
                </span>
                <span className={styles.scoreValue}>({force.score}/5)</span>
              </div>
            </div>
            <div className={styles.keyFactors}>
              <h5>Key Factors</h5>
              <ul>
                {force.key_factors.map((factor, j) => (
                  <li key={j}>{factor}</li>
                ))}
              </ul>
            </div>
            <div className={styles.strategicResponse}>
              {force.strategic_response}
            </div>
          </div>
        ))}
      </div>
      <div className={styles.overallAssessment}>
        <div className={styles.assessmentHeader}>
          <h4>Industry Attractiveness</h4>
          <div className={styles.attractivenessScore}>
            <span>Overall Score:</span>
            <div className={styles.score}>{data.overall_attractiveness}/5</div>
          </div>
        </div>
        <div className={styles.competitiveStrategy}>
          <h5>Recommended Strategy</h5>
          <p>{data.competitive_strategy}</p>
        </div>
        <div className={styles.successFactors}>
          <h5>Key Success Factors</h5>
          <div className={styles.factorsList}>
            {data.key_success_factors.map((factor, i) => (
              <div key={i} className={styles.factor}>
                <div className={styles.checkmark}>✓</div>
                <span>{factor}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderAnsoffMatrix = (data: AnsoffData) => (
    <div className={styles.ansoffMatrix}>
      <h3>Ansoff Growth Matrix</h3>
      <div className={styles.matrixGrid}>
        <div className={`${styles.strategyCard} ${data.current_strategy === 'Market Penetration' ? styles.current : ''} ${data.recommended_strategy === 'Market Penetration' ? styles.recommended : ''}`}>
          <h4>Market Penetration</h4>
          <div className={styles.strategyDesc}>Existing Products → Existing Markets</div>
          <div className={styles.badges}>
            {data.current_strategy === 'Market Penetration' && <span className={`${styles.badge} ${styles.current}`}>Current</span>}
            {data.recommended_strategy === 'Market Penetration' && <span className={`${styles.badge} ${styles.recommended}`}>Recommended</span>}
            <span className={`${styles.badge} ${styles.risk}`} data-risk="low">Low Risk</span>
          </div>
        </div>
        <div className={`${styles.strategyCard} ${data.current_strategy === 'Product Development' ? styles.current : ''} ${data.recommended_strategy === 'Product Development' ? styles.recommended : ''}`}>
          <h4>Product Development</h4>
          <div className={styles.strategyDesc}>New Products → Existing Markets</div>
          <div className={styles.badges}>
            {data.current_strategy === 'Product Development' && <span className={`${styles.badge} ${styles.current}`}>Current</span>}
            {data.recommended_strategy === 'Product Development' && <span className={`${styles.badge} ${styles.recommended}`}>Recommended</span>}
            <span className={`${styles.badge} ${styles.risk}`} data-risk="medium">Medium Risk</span>
          </div>
        </div>
        <div className={`${styles.strategyCard} ${data.current_strategy === 'Market Development' ? styles.current : ''} ${data.recommended_strategy === 'Market Development' ? styles.recommended : ''}`}>
          <h4>Market Development</h4>
          <div className={styles.strategyDesc}>Existing Products → New Markets</div>
          <div className={styles.badges}>
            {data.current_strategy === 'Market Development' && <span className={`${styles.badge} ${styles.current}`}>Current</span>}
            {data.recommended_strategy === 'Market Development' && <span className={`${styles.badge} ${styles.recommended}`}>Recommended</span>}
            <span className={`${styles.badge} ${styles.risk}`} data-risk="medium">Medium Risk</span>
          </div>
        </div>
        <div className={`${styles.strategyCard} ${data.current_strategy === 'Diversification' ? styles.current : ''} ${data.recommended_strategy === 'Diversification' ? styles.recommended : ''}`}>
          <h4>Diversification</h4>
          <div className={styles.strategyDesc}>New Products → New Markets</div>
          <div className={styles.badges}>
            {data.current_strategy === 'Diversification' && <span className={`${styles.badge} ${styles.current}`}>Current</span>}
            {data.recommended_strategy === 'Diversification' && <span className={`${styles.badge} ${styles.recommended}`}>Recommended</span>}
            <span className={`${styles.badge} ${styles.risk}`} data-risk={data.risk_level}>High Risk</span>
          </div>
        </div>
      </div>
      
      <div className={styles.implementationPlan}>
        <h4>Implementation Plan</h4>
        <div className={styles.steps}>
          {data.implementation_steps.map((step, i) => (
            <div key={i} className={styles.step}>
              <div className={styles.stepNumber}>{i + 1}</div>
              <div className={styles.stepContent}>
                <div className={styles.stepTitle}>{step.step}</div>
              </div>
              <div className={styles.timeline}>{step.timeline}</div>
              <div className={styles.investment}>{step.investment}</div>
            </div>
          ))}
        </div>
        
        <div className={styles.expectedOutcomes}>
          <h5>Expected Outcomes</h5>
          <ul>
            {data.expected_outcomes.map((outcome, i) => (
              <li key={i}>{outcome}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );

  const renderValueChain = (data: ValueChainData) => (
    <div className={styles.valueChain}>
      <h3>Value Chain Analysis</h3>
      <div className={styles.chainSection}>
        <h4>Support Activities</h4>
        <div className={styles.activitiesGrid}>
          {data.support_activities.map((activity, i) => (
            <div key={i} className={styles.activity}>
              <div className={styles.activityInfo}>
                <div className={styles.activityName}>{activity.activity}</div>
                <div className={styles.improvement}>{activity.improvement_potential}</div>
              </div>
              <div className={styles.strengthIndicator}>
                <div className={styles.strengthBar}>
                  <div className={styles.strengthFill} style={{ width: `${activity.strength * 10}%` }} />
                </div>
                <div className={styles.strengthValue}>{activity.strength}/10</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className={styles.chainSection}>
        <h4>Primary Activities</h4>
        <div className={styles.activitiesGrid}>
          {data.primary_activities.map((activity, i) => (
            <div key={i} className={styles.activity}>
              <div className={styles.activityInfo}>
                <div className={styles.activityName}>{activity.activity}</div>
                <div className={styles.improvement}>{activity.improvement_potential}</div>
              </div>
              <div className={styles.strengthIndicator}>
                <div className={styles.strengthBar}>
                  <div className={styles.strengthFill} style={{ width: `${activity.strength * 10}%` }} />
                </div>
                <div className={styles.strengthValue}>{activity.strength}/10</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className={styles.competitiveAdvantages}>
        <h4>Competitive Advantages</h4>
        <div className={styles.advantagesList}>
          {data.competitive_advantages.map((adv, i) => (
            <div key={i} className={styles.advantage}>
              <div className={styles.icon}>✓</div>
              <span>{adv}</span>
            </div>
          ))}
        </div>
      </div>
      
      <div className={styles.valueOpportunities}>
        <h4>Value Creation Opportunities</h4>
        <div className={styles.opportunitiesList}>
          {data.value_creation_opportunities.map((opp, i) => (
            <div key={i} className={styles.opportunity}>
              <div className={styles.opportunityNumber}>{i + 1}</div>
              <div className={styles.opportunityText}>{opp}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderFrameworkContent = (assessment: FrameworkAssessment) => {
    console.log('renderFrameworkContent - framework_id:', assessment.framework_id);
    switch (assessment.framework_id) {
      case 'swot':
      case 'swot_analysis':
        return renderSWOTAnalysis(assessment.assessment_data as SWOTData);
      case 'bcg_matrix':
      case 'bcg_growth_share_matrix':
        return renderBCGMatrix(assessment.assessment_data as BCGData);
      case 'porters_five_forces':
      case 'porter_five_forces':
        return renderPortersForces(assessment.assessment_data as PortersData);
      case 'ansoff_matrix':
      case 'ansoff_growth_matrix':
        return renderAnsoffMatrix(assessment.assessment_data as AnsoffData);
      case 'value_chain':
      case 'value_chain_analysis':
        return renderValueChain(assessment.assessment_data as ValueChainData);
      default:
        console.log('Unknown framework:', assessment.framework_id);
        return <div>Framework visualization not available for: {assessment.framework_id}</div>;
    }
  };

  const renderIntegratedView = () => {
    const criticalInsights = assessments.flatMap(a => a.key_insights).slice(0, 5);
    const topRecommendations = assessments
      .flatMap(a => a.recommendations)
      .filter(r => r.priority === 'immediate' && r.impact === 'high')
      .slice(0, 5);

    return (
      <div className={styles.integratedView}>
        <div className={styles.executiveSummary}>
          <h3>Integrated Strategic Assessment</h3>
          <p className={styles.summaryText}>
            Based on {assessments.length} framework analyses, your startup shows {
              assessments.filter(a => 
                a.framework_id === 'bcg_matrix' && 
                (a.assessment_data as BCGData).position === 'Question Mark'
              ).length > 0 ? 'high growth potential with execution risks' : 'steady growth trajectory'
            }.
          </p>
        </div>

        <div className={styles.criticalInsights}>
          <h4>Key Strategic Insights</h4>
          <div className={styles.insightsList}>
            {criticalInsights.map((insight, i) => (
              <motion.div 
                key={i} 
                className={styles.insightItem}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <span className={styles.insightNumber}>{i + 1}</span>
                <p>{insight}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className={styles.priorityActions}>
          <h4>Priority Actions</h4>
          <div className={styles.actionGrid}>
            {topRecommendations.map((rec, i) => (
              <motion.div 
                key={i} 
                className={styles.actionCard}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <div className={styles.actionHeader}>
                  <span className={styles.priority}>{rec.priority}</span>
                  <span className={styles.impact}>{rec.impact} impact</span>
                </div>
                <p>{rec.action}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className={styles.frameworkAlignment}>
          <h4>Framework Consensus</h4>
          <div className={styles.consensusGrid}>
            <div className={styles.consensusItem}>
              <h5>Growth Strategy</h5>
              <p>All frameworks indicate focus on market penetration before expansion</p>
            </div>
            <div className={styles.consensusItem}>
              <h5>Competitive Position</h5>
              <p>Weak current position but strong potential in growing market</p>
            </div>
            <div className={styles.consensusItem}>
              <h5>Resource Allocation</h5>
              <p>Prioritize customer acquisition and product differentiation</p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Conducting framework assessments...</p>
        </div>
      </div>
    );
  }

  const selectedAssessment = assessments.find(a => a.framework_id === selectedFramework);
  console.log('Render - assessments:', assessments);
  console.log('Render - selectedFramework:', selectedFramework);
  console.log('Render - selectedAssessment:', selectedAssessment);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Strategic Framework Assessment</h2>
        <p>Professional framework analysis using proven methodologies</p>
      </div>

      <div className={styles.viewToggle}>
        <button
          className={viewMode === 'individual' ? styles.active : ''}
          onClick={() => setViewMode('individual')}
        >
          Individual Frameworks
        </button>
        <button
          className={viewMode === 'integrated' ? styles.active : ''}
          onClick={() => setViewMode('integrated')}
        >
          Integrated Analysis
        </button>
      </div>

      {viewMode === 'individual' ? (
        <>
          <div className={styles.frameworkTabs}>
            {assessments.map(assessment => (
              <button
                key={assessment.framework_id}
                className={`${styles.tab} ${selectedFramework === assessment.framework_id ? styles.active : ''}`}
                onClick={() => setSelectedFramework(assessment.framework_id)}
              >
                {assessment.framework_name}
              </button>
            ))}
          </div>

          {selectedAssessment && (
            <AnimatePresence mode="wait">
              <motion.div
                key={selectedFramework}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={styles.frameworkContent}
              >
                {renderFrameworkContent(selectedAssessment)}

                <div className={styles.insights}>
                  <h4>Key Insights</h4>
                  <ul>
                    {selectedAssessment.key_insights.map((insight, i) => (
                      <li key={i}>{insight}</li>
                    ))}
                  </ul>
                </div>

                <div className={styles.recommendations}>
                  <h4>Recommendations</h4>
                  <div className={styles.recommendationsList}>
                    {selectedAssessment.recommendations.map((rec, i) => (
                      <div key={i} className={styles.recommendation}>
                        <div className={styles.recHeader}>
                          <span className={styles.recNumber}>{i + 1}</span>
                          <span className={`${styles.priority} ${styles[rec.priority.replace('-', '')]}`}>
                            {rec.priority.replace('-', ' ')}
                          </span>
                          <span className={`${styles.impact} ${styles[rec.impact]}`}>
                            {rec.impact} impact
                          </span>
                        </div>
                        <p>{rec.action}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          )}
        </>
      ) : (
        renderIntegratedView()
      )}
    </div>
  );
};

export default StrategicFrameworkAssessment;