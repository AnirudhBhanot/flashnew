import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import styles from './MichelinStrategicAnalysis.module.scss';
import { getMichelinEndpoint, featureFlags } from '../config/features';

interface MichelinAnalysisProps {
  startupData: any;
  onClose?: () => void;
}

interface PhaseStatus {
  phase1: 'pending' | 'loading' | 'completed' | 'error';
  phase2: 'locked' | 'pending' | 'loading' | 'completed' | 'error';
  phase3: 'locked' | 'pending' | 'loading' | 'completed' | 'error';
}

interface BCGMatrixData {
  position: string;
  market_growth: number;
  relative_market_share: number;
  strategic_implications: string[];
  action_items: string[];
}

interface PortersForce {
  intensity: string;
  factors: string[];
  score: number;
}

interface SWOTItem {
  item: string;
  evidence?: string;
  impact?: string;
  potential?: string;
  mitigation?: string;
}

interface Phase1Data {
  executive_summary: string;
  bcg_matrix: BCGMatrixData;
  porters_five_forces: {
    competitive_rivalry: PortersForce;
    threat_of_new_entrants: PortersForce;
    bargaining_power_of_suppliers: PortersForce;
    bargaining_power_of_buyers: PortersForce;
    threat_of_substitutes: PortersForce;
    overall_industry_attractiveness: string;
    key_strategic_imperatives: string[];
  };
  swot_analysis: {
    strengths: SWOTItem[];
    weaknesses: SWOTItem[];
    opportunities: SWOTItem[];
    threats: SWOTItem[];
    strategic_priorities: string[];
  };
  current_position_narrative: string;
}

interface AnsoffQuadrant {
  strategy: string;
  initiatives: string[];
  investment: number;
  timeline: string;
}

interface GrowthScenario {
  name: string;
  description: string;
  revenue_projection_3yr: number;
  investment_required: number;
  key_milestones: string[];
  risks: string[];
  probability_of_success: number;
}

interface Phase2Data {
  strategic_options_overview: string;
  ansoff_matrix: {
    market_penetration: AnsoffQuadrant;
    market_development: AnsoffQuadrant;
    product_development: AnsoffQuadrant;
    diversification: AnsoffQuadrant;
    recommended_strategy: string;
    implementation_priorities: string[];
  };
  blue_ocean_strategy: {
    eliminate_factors: string[];
    reduce_factors: string[];
    raise_factors: string[];
    create_factors: string[];
    value_innovation_opportunities: any[];
    new_market_spaces: string[];
  };
  growth_scenarios: GrowthScenario[];
  recommended_direction: string;
}

interface BalancedScorecardItem {
  perspective: string;
  objectives: string[];
  measures: string[];
  targets: string[];
  initiatives: string[];
}

interface Phase3Data {
  implementation_roadmap_summary: string;
  balanced_scorecard: BalancedScorecardItem[];
  okr_framework: any[];
  resource_requirements: {
    human_resources: any[];
    financial_resources: any;
    technology_resources: string[];
    partnership_resources: string[];
  };
  risk_mitigation_plan: any[];
  success_metrics: any[];
}

interface MichelinAnalysisData {
  startup_name: string;
  analysis_date: string;
  executive_briefing: string;
  phase1: Phase1Data;
  phase2: Phase2Data;
  phase3: Phase3Data;
  key_recommendations: string[];
  critical_success_factors: string[];
  next_steps: any[];
}

export const MichelinStrategicAnalysis: React.FC<MichelinAnalysisProps> = ({ startupData, onClose }) => {
  const [phase1Data, setPhase1Data] = useState<any>(null);
  const [phase2Data, setPhase2Data] = useState<any>(null);
  const [phase3Data, setPhase3Data] = useState<any>(null);
  const [phaseStatus, setPhaseStatus] = useState<PhaseStatus>({
    phase1: 'pending',
    phase2: 'locked',
    phase3: 'locked'
  });
  const [error, setError] = useState<string | null>(null);
  const [activePhase, setActivePhase] = useState<1 | 2 | 3>(1);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());

  // Auto-start Phase 1 on mount
  useEffect(() => {
    fetchPhase1();
  }, []);

  const prepareStartupData = () => ({
    startup_name: startupData.company_name || 'Your Startup',
    sector: startupData.sector || 'technology',
    funding_stage: startupData.funding_stage || 'seed',
    total_capital_raised_usd: startupData.total_capital_raised || 1000000,
    cash_on_hand_usd: startupData.cash_on_hand || startupData.runway_months * startupData.monthly_burn_usd || 500000,
    market_size_usd: startupData.tam_size_usd || 10000000000,
    market_growth_rate_annual: startupData.market_growth_rate_percent || 20,
    competitor_count: startupData.competitors_named_count || 5,
    market_share_percentage: 0.1,
    team_size_full_time: startupData.team_size_full_time || 10,
    customer_count: startupData.customer_count || 10,
    customer_acquisition_cost_usd: 1000,
    lifetime_value_usd: 10000,
    monthly_active_users: startupData.customer_count * 100 || 1000,
    proprietary_tech: startupData.patent_count > 0,
    patents_filed: startupData.patent_count || 0,
    founders_industry_experience_years: startupData.domain_expertise_years || 5,
    b2b_or_b2c: 'b2b',
    burn_rate_usd: startupData.monthly_burn_usd || 50000,
    monthly_burn_usd: startupData.monthly_burn_usd || 50000,
    runway_months: startupData.runway_months || 12,
    product_stage: startupData.product_stage || 'beta',
    investor_tier_primary: startupData.investor_tier || 'tier_2',
    revenue_growth_rate: startupData.revenue_growth_rate_percent || 0,
    gross_margin: startupData.gross_margin || 70,
    annual_revenue_usd: startupData.annual_revenue_run_rate || 0,
  });

  const fetchPhase1 = async () => {
    try {
      setPhaseStatus(prev => ({ ...prev, phase1: 'loading' }));
      setError(null);
      
      if (featureFlags.michelinAnalysisDebugMode) {
        console.log('Michelin Phase 1 - Using approach:', featureFlags.michelinAnalysisApproach);
        console.log('Endpoint:', getMichelinEndpoint(1));
      }

      const response = await fetch(getMichelinEndpoint(1), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          startup_data: prepareStartupData(),
          include_financial_projections: true,
          analysis_depth: 'comprehensive',
        }),
      });

      if (!response.ok) {
        throw new Error(`Phase 1 analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setPhase1Data(data);
      setPhaseStatus(prev => ({ ...prev, phase1: 'completed', phase2: 'pending' }));
    } catch (err) {
      console.error('Phase 1 analysis error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate Phase 1 analysis');
      setPhaseStatus(prev => ({ ...prev, phase1: 'error' }));
    }
  };

  const fetchPhase2 = async () => {
    if (!phase1Data) return;
    
    try {
      setPhaseStatus(prev => ({ ...prev, phase2: 'loading' }));
      setError(null);

      const response = await fetch(getMichelinEndpoint(2), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          startup_data: prepareStartupData(),
          phase1_results: phase1Data.phase1,
        }),
      });

      if (!response.ok) {
        throw new Error(`Phase 2 analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setPhase2Data(data);
      setPhaseStatus(prev => ({ ...prev, phase2: 'completed', phase3: 'pending' }));
    } catch (err) {
      console.error('Phase 2 analysis error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate Phase 2 analysis');
      setPhaseStatus(prev => ({ ...prev, phase2: 'error' }));
    }
  };

  const fetchPhase3 = async () => {
    if (!phase1Data || !phase2Data) return;
    
    try {
      setPhaseStatus(prev => ({ ...prev, phase3: 'loading' }));
      setError(null);

      const response = await fetch(getMichelinEndpoint(3), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          startup_data: prepareStartupData(),
          phase1_results: phase1Data.phase1,
          phase2_results: phase2Data.phase2,
        }),
      });

      if (!response.ok) {
        throw new Error(`Phase 3 analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setPhase3Data(data);
      setPhaseStatus(prev => ({ ...prev, phase3: 'completed' }));
    } catch (err) {
      console.error('Phase 3 analysis error:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate Phase 3 analysis');
      setPhaseStatus(prev => ({ ...prev, phase3: 'error' }));
    }
  };

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const renderPhase1 = () => {
    if (!phase1Data) return null;
    const { phase1 } = phase1Data;

    return (
      <div className={styles.phaseContent}>
        <div className={styles.section}>
          <h3>Executive Summary</h3>
          <p className={styles.narrative}>{phase1.executive_summary}</p>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('bcg')}>
            <h3>BCG Matrix Analysis</h3>
            <span className={styles.toggle}>{expandedSections.has('bcg') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('bcg') && phase1.bcg_matrix_analysis && (
            <div className={styles.sectionContent}>
              <div className={styles.bcgPosition}>
                <div className={styles.positionBadge} data-position={(phase1.bcg_matrix_analysis.position || 'question mark').toLowerCase()}>
                  {phase1.bcg_matrix_analysis.position || 'Question Mark'}
                </div>
                <div className={styles.metrics}>
                  <div>Market Growth: {phase1.bcg_matrix_analysis.market_growth_rate || 'High'}</div>
                  <div>Relative Market Share: {phase1.bcg_matrix_analysis.relative_market_share || 'Low'}</div>
                </div>
              </div>
              <div className={styles.implications}>
                <h4>Strategic Implications</h4>
                <p>{phase1.bcg_matrix_analysis.strategic_implications || 'Analysis in progress.'}</p>
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('porters')}>
            <h3>Porter's Five Forces</h3>
            <span className={styles.toggle}>{expandedSections.has('porters') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('porters') && phase1.porters_five_forces && (
            <div className={styles.sectionContent}>
              <div className={styles.forcesGrid}>
                {Object.entries(phase1.porters_five_forces)
                  .filter(([key]) => typeof phase1.porters_five_forces[key] === 'object' && phase1.porters_five_forces[key].level)
                  .map(([force, data]: [string, any]) => (
                    <div key={force} className={styles.forceCard}>
                      <h4>{force.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h4>
                      <div className={styles.intensity} data-level={(data.level || 'medium').toLowerCase()}>
                        {data.level || 'Medium'}
                      </div>
                      <p className={styles.analysis}>{data.analysis || 'Analysis pending.'}</p>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('swot')}>
            <h3>SWOT Analysis</h3>
            <span className={styles.toggle}>{expandedSections.has('swot') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('swot') && (
            <div className={styles.sectionContent}>
              <div className={styles.swotGrid}>
                <div className={styles.swotQuadrant} data-type="strengths">
                  <h4>Strengths</h4>
                  <ul>
                    {(phase1.swot_analysis.strengths || []).map((item, idx) => (
                      <li key={idx}>
                        <strong>{item.point || item.item || 'Strength'}</strong>
                        {item.evidence && <span> - {item.evidence}</span>}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className={styles.swotQuadrant} data-type="weaknesses">
                  <h4>Weaknesses</h4>
                  <ul>
                    {(phase1.swot_analysis.weaknesses || []).map((item, idx) => (
                      <li key={idx}>
                        <strong>{item.point || item.item || 'Weakness'}</strong>
                        {(item.evidence || item.impact) && <span> - {item.evidence || item.impact}</span>}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className={styles.swotQuadrant} data-type="opportunities">
                  <h4>Opportunities</h4>
                  <ul>
                    {(phase1.swot_analysis.opportunities || []).map((item, idx) => (
                      <li key={idx}>
                        <strong>{item.point || item.item || 'Opportunity'}</strong>
                        {(item.evidence || item.potential) && <span> - {item.evidence || item.potential}</span>}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className={styles.swotQuadrant} data-type="threats">
                  <h4>Threats</h4>
                  <ul>
                    {(phase1.swot_analysis.threats || []).map((item, idx) => (
                      <li key={idx}>
                        <strong>{item.point || item.item || 'Threat'}</strong>
                        {(item.evidence || item.mitigation) && <span> - {item.evidence || item.mitigation}</span>}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className={styles.priorities}>
                <h4>Strategic Priorities</h4>
                <ol>
                  {(phase1.swot_analysis.strategic_priorities || []).map((priority, idx) => (
                    <li key={idx}>{priority}</li>
                  ))}
                </ol>
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <h3>Current Position Narrative</h3>
          <p className={styles.narrative}>{phase1.current_position_narrative}</p>
        </div>
      </div>
    );
  };

  const renderPhase2 = () => {
    if (!phase2Data) return null;
    const { phase2 } = phase2Data;

    return (
      <div className={styles.phaseContent}>
        <div className={styles.section}>
          <h3>Strategic Options Overview</h3>
          <p className={styles.narrative}>{phase2.strategic_options_overview}</p>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('ansoff')}>
            <h3>Ansoff Matrix Analysis</h3>
            <span className={styles.toggle}>{expandedSections.has('ansoff') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('ansoff') && phase2.ansoff_matrix_analysis && (
            <div className={styles.sectionContent}>
              <div className={styles.ansoffGrid}>
                <div className={styles.ansoffQuadrant}>
                  <h4>Market Penetration</h4>
                  <p>{phase2.ansoff_matrix_analysis.market_penetration?.expected_impact || 'Expand in existing markets'}</p>
                  <div className={styles.details}>
                    <span>Feasibility: {phase2.ansoff_matrix_analysis.market_penetration?.feasibility || 'Medium'}</span>
                    <span>Timeline: {phase2.ansoff_matrix_analysis.market_penetration?.timeline || '6-12 months'}</span>
                  </div>
                  <ul>
                    {(phase2.ansoff_matrix_analysis.market_penetration?.initiatives || []).map((init, idx) => (
                      <li key={idx}>{init}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.ansoffQuadrant}>
                  <h4>Market Development</h4>
                  <p>{phase2.ansoff_matrix_analysis.market_development?.expected_impact || 'Enter new markets'}</p>
                  <div className={styles.details}>
                    <span>Feasibility: {phase2.ansoff_matrix_analysis.market_development?.feasibility || 'Medium'}</span>
                    <span>Timeline: {phase2.ansoff_matrix_analysis.market_development?.timeline || '12-24 months'}</span>
                  </div>
                  <ul>
                    {(phase2.ansoff_matrix_analysis.market_development?.initiatives || []).map((init, idx) => (
                      <li key={idx}>{init}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.ansoffQuadrant}>
                  <h4>Product Development</h4>
                  <p>{phase2.ansoff_matrix_analysis.product_development?.expected_impact || 'Create new products'}</p>
                  <div className={styles.details}>
                    <span>Feasibility: {phase2.ansoff_matrix_analysis.product_development?.feasibility || 'Medium'}</span>
                    <span>Timeline: {phase2.ansoff_matrix_analysis.product_development?.timeline || '9-18 months'}</span>
                  </div>
                  <ul>
                    {(phase2.ansoff_matrix_analysis.product_development?.initiatives || []).map((init, idx) => (
                      <li key={idx}>{init}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.ansoffQuadrant}>
                  <h4>Diversification</h4>
                  <p>{phase2.ansoff_matrix_analysis.diversification?.expected_impact || 'New markets and products'}</p>
                  <div className={styles.details}>
                    <span>Feasibility: {phase2.ansoff_matrix_analysis.diversification?.feasibility || 'Low'}</span>
                    <span>Timeline: {phase2.ansoff_matrix_analysis.diversification?.timeline || '18-36 months'}</span>
                  </div>
                  <ul>
                    {(phase2.ansoff_matrix_analysis.diversification?.initiatives || []).map((init, idx) => (
                      <li key={idx}>{init}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className={styles.recommendation}>
                <h4>Recommended Direction</h4>
                <p>{phase2.recommended_direction || 'Focus on market penetration and product development.'}</p>
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('blueocean')}>
            <h3>Blue Ocean Strategy</h3>
            <span className={styles.toggle}>{expandedSections.has('blueocean') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('blueocean') && (phase2.blue_ocean_strategy || phase2.blueOceanStrategy) && (
            <div className={styles.sectionContent}>
              <div className={styles.fourActions}>
                <div className={styles.actionBlock} data-action="eliminate">
                  <h4>Eliminate</h4>
                  <ul>
                    {((phase2.blue_ocean_strategy.four_actions?.eliminate || phase2.blue_ocean_strategy.eliminate) || []).map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.actionBlock} data-action="reduce">
                  <h4>Reduce</h4>
                  <ul>
                    {((phase2.blue_ocean_strategy.four_actions?.reduce || phase2.blue_ocean_strategy.reduce) || []).map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.actionBlock} data-action="raise">
                  <h4>Raise</h4>
                  <ul>
                    {((phase2.blue_ocean_strategy.four_actions?.raise || phase2.blue_ocean_strategy.raise) || []).map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
                <div className={styles.actionBlock} data-action="create">
                  <h4>Create</h4>
                  <ul>
                    {((phase2.blue_ocean_strategy.four_actions?.create || phase2.blue_ocean_strategy.create) || []).map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
              </div>
              {phase2.blue_ocean_strategy.value_innovation_potential && (
                <div className={styles.valueInnovation}>
                  <h4>Value Innovation Potential</h4>
                  <p>{phase2.blue_ocean_strategy.value_innovation_potential}</p>
                </div>
              )}
              {phase2.blue_ocean_strategy.blue_ocean_opportunity && (
                <div className={styles.blueOceanOpportunity}>
                  <h4>Blue Ocean Opportunity</h4>
                  {typeof phase2.blue_ocean_strategy.blue_ocean_opportunity === 'object' ? (
                    <div className={styles.opportunityGrid}>
                      <div>
                        <strong>Market Size:</strong>
                        <p>{phase2.blue_ocean_strategy.blue_ocean_opportunity.market_size || 'TBD'}</p>
                      </div>
                      <div>
                        <strong>Differentiation:</strong>
                        <p>{phase2.blue_ocean_strategy.blue_ocean_opportunity.differentiation || 'TBD'}</p>
                      </div>
                      <div>
                        <strong>Competitive Advantage:</strong>
                        <p>{phase2.blue_ocean_strategy.blue_ocean_opportunity.competitive_advantage || 'TBD'}</p>
                      </div>
                    </div>
                  ) : (
                    <p>{phase2.blue_ocean_strategy.blue_ocean_opportunity}</p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('scenarios')}>
            <h3>Growth Scenarios</h3>
            <span className={styles.toggle}>{expandedSections.has('scenarios') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('scenarios') && phase2.growth_scenarios && (
            <div className={styles.sectionContent}>
              <div className={styles.scenariosGrid}>
                {(phase2.growth_scenarios || []).map((scenario, idx) => (
                  <div key={idx} className={styles.scenarioCard} data-risk={scenario.name?.toLowerCase() || 'moderate'}>
                    <h4>{scenario.name || `Scenario ${idx + 1}`}</h4>
                    <p>{scenario.description || `${scenario.name || 'Growth'} scenario with detailed projections and strategy`}</p>
                    <div className={styles.scenarioMetrics}>
                      <div>Expected Revenue: {scenario.expected_revenue_year3 || scenario.expected_revenue || 'Calculating...'}</div>
                      <div>Investment: {scenario.investment_required || scenario.required_resources || 'Calculating...'}</div>
                      <div>Success Probability: {scenario.success_probability || `${scenario.name?.includes('Conservative') ? '85%' : scenario.name?.includes('Base') ? '70%' : '40%'}`}</div>
                    </div>
                    {scenario.strategic_moves && (
                      <>
                        <h5>Strategic Moves</h5>
                        <ul>
                          {scenario.strategic_moves.map((move, midx) => (
                            <li key={midx}>{move}</li>
                          ))}
                        </ul>
                      </>
                    )}
                    {scenario.key_risks && (
                      <>
                        <h5>Key Risks</h5>
                        <ul>
                          {scenario.key_risks.map((risk, ridx) => (
                            <li key={ridx}>{risk}</li>
                          ))}
                        </ul>
                      </>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <h3>Recommended Direction</h3>
          <div className={styles.recommendedDirection}>
            <p>{phase2.recommended_direction}</p>
          </div>
        </div>
      </div>
    );
  };

  const renderPhase3 = () => {
    if (!phase3Data) return null;
    const { phase3 } = phase3Data;

    return (
      <div className={styles.phaseContent}>
        <div className={styles.section}>
          <h3>Implementation Roadmap Summary</h3>
          <p className={styles.narrative}>{phase3.implementation_roadmap_summary}</p>
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('scorecard')}>
            <h3>Balanced Scorecard</h3>
            <span className={styles.toggle}>{expandedSections.has('scorecard') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('scorecard') && phase3.balanced_scorecard && (
            <div className={styles.sectionContent}>
              <div className={styles.scorecardGrid}>
                {Object.entries(phase3.balanced_scorecard || {}).map(([perspective, data]: [string, any], idx) => (
                  <div key={idx} className={styles.scorecardPerspective}>
                    <h4>{perspective.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h4>
                    <div className={styles.scorecardContent}>
                      {data.objectives && (
                        <div>
                          <h5>Objectives</h5>
                          <ul>
                            {(data.objectives || []).map((obj, oidx) => (
                              <li key={oidx}>{obj}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {data.measures && (
                        <div>
                          <h5>Measures</h5>
                          <ul>
                            {(data.measures || []).map((measure, midx) => (
                              <li key={midx}>{measure}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {data.targets && (
                        <div>
                          <h5>Targets</h5>
                          <ul>
                            {(data.targets || []).map((target, tidx) => (
                              <li key={tidx}>{target}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {data.initiatives && (
                        <div>
                          <h5>Initiatives</h5>
                          <ul>
                            {(data.initiatives || []).map((init, iidx) => (
                              <li key={iidx}>{init}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('okrs')}>
            <h3>OKR Framework</h3>
            <span className={styles.toggle}>{expandedSections.has('okrs') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('okrs') && phase3.okr_framework && (
            <div className={styles.sectionContent}>
              {Object.entries(phase3.okr_framework || {}).map(([quarter, data]: [string, any], idx) => (
                <div key={idx} className={styles.okrQuarter}>
                  <h4>{quarter.toUpperCase()}</h4>
                  {(data.objectives || []).map((obj: any, oidx: number) => (
                    <div key={oidx} className={styles.objective}>
                      <h5>{obj.objective || 'Objective'}</h5>
                      <div className={styles.keyResults}>
                        {Array.isArray(obj.key_results) && typeof obj.key_results[0] === 'string' ? (
                          // Handle simple string array format
                          obj.key_results.map((kr: string, kidx: number) => (
                            <div key={kidx} className={styles.keyResult}>
                              <span>{kr}</span>
                            </div>
                          ))
                        ) : (
                          // Handle object format with kr and target
                          (obj.key_results || []).map((kr: any, kidx: number) => (
                            <div key={kidx} className={styles.keyResult}>
                              <span>{kr.kr || kr}</span>
                              {kr.target && (
                                <div className={styles.progress}>
                                  <span>Target: {kr.target}</span>
                                </div>
                              )}
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('resources')}>
            <h3>Resource Requirements</h3>
            <span className={styles.toggle}>{expandedSections.has('resources') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('resources') && phase3.resource_requirements && (
            <div className={styles.sectionContent}>
              <div className={styles.resourcesGrid}>
                {phase3.resource_requirements.human_resources && (
                  <div className={styles.resourceCategory}>
                    <h4>Human Resources</h4>
                    <ul>
                      {phase3.resource_requirements.human_resources.immediate_hires && (
                        <li>Immediate hires: {phase3.resource_requirements.human_resources.immediate_hires.join(', ')}</li>
                      )}
                      {phase3.resource_requirements.human_resources.q1_hires && (
                        <li>Q1 hires: {phase3.resource_requirements.human_resources.q1_hires.join(', ')}</li>
                      )}
                      {phase3.resource_requirements.human_resources.total_headcount_eoy && (
                        <li>Year-end headcount: {phase3.resource_requirements.human_resources.total_headcount_eoy}</li>
                      )}
                      {phase3.resource_requirements.human_resources.key_skill_gaps && (
                        <li>Key skill gaps: {phase3.resource_requirements.human_resources.key_skill_gaps.join(', ')}</li>
                      )}
                    </ul>
                  </div>
                )}
                {phase3.resource_requirements.financial_resources && (
                  <div className={styles.resourceCategory}>
                    <h4>Financial Resources</h4>
                    <div className={styles.financialMetrics}>
                      {phase3.resource_requirements.financial_resources.funding_required && (
                        <div>Funding Required: {phase3.resource_requirements.financial_resources.funding_required}</div>
                      )}
                      {phase3.resource_requirements.financial_resources.runway_extension && (
                        <div>Runway Extension: {phase3.resource_requirements.financial_resources.runway_extension}</div>
                      )}
                      {phase3.resource_requirements.financial_resources.use_of_funds && (
                        <div>
                          <h5>Use of Funds:</h5>
                          <ul>
                            {Object.entries(phase3.resource_requirements.financial_resources.use_of_funds).map(([category, percentage], idx) => (
                              <li key={idx}>{category}: {percentage}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                )}
                {phase3.resource_requirements.technology_resources && (
                  <div className={styles.resourceCategory}>
                    <h4>Technology Resources</h4>
                    <ul>
                      {phase3.resource_requirements.technology_resources.infrastructure_needs && (
                        <li>Infrastructure: {phase3.resource_requirements.technology_resources.infrastructure_needs.join(', ')}</li>
                      )}
                      {phase3.resource_requirements.technology_resources.tool_requirements && (
                        <li>Tools: {phase3.resource_requirements.technology_resources.tool_requirements.join(', ')}</li>
                      )}
                      {phase3.resource_requirements.technology_resources.platform_migrations && (
                        <li>Migrations: {phase3.resource_requirements.technology_resources.platform_migrations.join(', ')}</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('risks')}>
            <h3>Risk Mitigation Plan</h3>
            <span className={styles.toggle}>{expandedSections.has('risks') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('risks') && phase3.risk_mitigation_plan && (
            <div className={styles.sectionContent}>
              <div className={styles.riskGrid}>
                {(phase3.risk_mitigation_plan.top_risks || []).map((risk, idx) => (
                  <div key={idx} className={styles.riskCard}>
                    <h4>{risk.risk || 'Risk'}</h4>
                    <div className={styles.riskMetrics}>
                      <span className={styles.impact} data-level={(risk.impact || 'medium').toLowerCase()}>Impact: {risk.impact || 'Medium'}</span>
                      <span className={styles.likelihood} data-level={(risk.probability || 'medium').toLowerCase()}>Probability: {risk.probability || 'Medium'}</span>
                    </div>
                    {risk.mitigation && (
                      <div className={styles.riskActions}>
                        <h5>Mitigation Strategy</h5>
                        <p>{risk.mitigation}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className={styles.section}>
          <div className={styles.sectionHeader} onClick={() => toggleSection('metrics')}>
            <h3>Success Metrics</h3>
            <span className={styles.toggle}>{expandedSections.has('metrics') ? '−' : '+'}</span>
          </div>
          {expandedSections.has('metrics') && phase3.success_metrics && (
            <div className={styles.sectionContent}>
              <div className={styles.metricsGrid}>
                {(phase3.success_metrics || []).map((metric, idx) => (
                  <div key={idx} className={styles.metricCard}>
                    <h4>{metric.metric || 'Metric'}</h4>
                    <div className={styles.metricDetails}>
                      <span className={styles.target}>Target: {metric.target || 'TBD'}</span>
                      <span className={styles.frequency}>Frequency: {metric.frequency || 'Monthly'}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <motion.div 
      className={styles.michelinAnalysis}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h2>Michelin Strategic Analysis</h2>
          <p className={styles.subtitle}>McKinsey-Style 3-Phase Strategic Framework</p>
          <p className={styles.company}>{startupData.company_name || 'Your Startup'}</p>
          <p className={styles.date}>{new Date().toLocaleDateString()}</p>
        </div>
        {onClose && (
          <button onClick={onClose} className={styles.closeButton}>
            ✕
          </button>
        )}
      </div>

      {phase3Data && (
        <div className={styles.executiveBriefing}>
          <h3>Executive Briefing</h3>
          <p>{phase3Data.executive_briefing}</p>
        </div>
      )}

      <div className={styles.phaseNavigation}>
        <button 
          className={`${styles.phaseTab} ${activePhase === 1 ? styles.active : ''} ${phaseStatus.phase1}`}
          onClick={() => phaseStatus.phase1 !== 'locked' && setActivePhase(1)}
          disabled={phaseStatus.phase1 === 'locked'}
        >
          <span className={styles.phaseNumber}>Phase 1</span>
          <span className={styles.phaseTitle}>Where Are We Now?</span>
          {phaseStatus.phase1 === 'loading' && <span className={styles.phaseLoader}>⏳</span>}
          {phaseStatus.phase1 === 'completed' && <span className={styles.phaseCheck}>✓</span>}
          {phaseStatus.phase1 === 'error' && <span className={styles.phaseError}>!</span>}
        </button>
        <button 
          className={`${styles.phaseTab} ${activePhase === 2 ? styles.active : ''} ${phaseStatus.phase2}`}
          onClick={() => phaseStatus.phase2 !== 'locked' && setActivePhase(2)}
          disabled={phaseStatus.phase2 === 'locked'}
        >
          <span className={styles.phaseNumber}>Phase 2</span>
          <span className={styles.phaseTitle}>Where Should We Go?</span>
          {phaseStatus.phase2 === 'loading' && <span className={styles.phaseLoader}>⏳</span>}
          {phaseStatus.phase2 === 'completed' && <span className={styles.phaseCheck}>✓</span>}
          {phaseStatus.phase2 === 'error' && <span className={styles.phaseError}>!</span>}
        </button>
        <button 
          className={`${styles.phaseTab} ${activePhase === 3 ? styles.active : ''} ${phaseStatus.phase3}`}
          onClick={() => phaseStatus.phase3 !== 'locked' && setActivePhase(3)}
          disabled={phaseStatus.phase3 === 'locked'}
        >
          <span className={styles.phaseNumber}>Phase 3</span>
          <span className={styles.phaseTitle}>How to Get There?</span>
          {phaseStatus.phase3 === 'loading' && <span className={styles.phaseLoader}>⏳</span>}
          {phaseStatus.phase3 === 'completed' && <span className={styles.phaseCheck}>✓</span>}
          {phaseStatus.phase3 === 'error' && <span className={styles.phaseError}>!</span>}
        </button>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={activePhase}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className={styles.phaseContainer}
        >
          {activePhase === 1 && (
            phaseStatus.phase1 === 'loading' ? (
              <div className={styles.phaseLoading}>
                <div className={styles.spinner}></div>
                <h3>Analyzing Current Position...</h3>
                <p>Generating BCG Matrix, Porter's Five Forces, and SWOT Analysis</p>
              </div>
            ) : phaseStatus.phase1 === 'error' ? (
              <div className={styles.phaseError}>
                <h3>Phase 1 Error</h3>
                <p>{error}</p>
                <button onClick={fetchPhase1} className={styles.retryButton}>Retry Phase 1</button>
              </div>
            ) : phaseStatus.phase1 === 'completed' ? (
              <>
                {renderPhase1()}
                {phaseStatus.phase2 === 'pending' && (
                  <div className={styles.phaseAction}>
                    <button onClick={fetchPhase2} className={styles.continueButton}>
                      Continue to Phase 2 →
                    </button>
                  </div>
                )}
              </>
            ) : null
          )}
          
          {activePhase === 2 && (
            phaseStatus.phase2 === 'locked' ? (
              <div className={styles.phaseLocked}>
                <h3>Phase 2 Locked</h3>
                <p>Complete Phase 1 to unlock strategic options analysis</p>
              </div>
            ) : phaseStatus.phase2 === 'loading' ? (
              <div className={styles.phaseLoading}>
                <div className={styles.spinner}></div>
                <h3>Generating Strategic Options...</h3>
                <p>Creating Ansoff Matrix, Blue Ocean Strategy, and Growth Scenarios</p>
              </div>
            ) : phaseStatus.phase2 === 'error' ? (
              <div className={styles.phaseError}>
                <h3>Phase 2 Error</h3>
                <p>{error}</p>
                <button onClick={fetchPhase2} className={styles.retryButton}>Retry Phase 2</button>
              </div>
            ) : phaseStatus.phase2 === 'completed' ? (
              <>
                {renderPhase2()}
                {phaseStatus.phase3 === 'pending' && (
                  <div className={styles.phaseAction}>
                    <button onClick={fetchPhase3} className={styles.continueButton}>
                      Continue to Phase 3 →
                    </button>
                  </div>
                )}
              </>
            ) : null
          )}
          
          {activePhase === 3 && (
            phaseStatus.phase3 === 'locked' ? (
              <div className={styles.phaseLocked}>
                <h3>Phase 3 Locked</h3>
                <p>Complete Phase 2 to unlock implementation planning</p>
              </div>
            ) : phaseStatus.phase3 === 'loading' ? (
              <div className={styles.phaseLoading}>
                <div className={styles.spinner}></div>
                <h3>Creating Implementation Plan...</h3>
                <p>Developing Roadmap, OKRs, and Resource Requirements</p>
              </div>
            ) : phaseStatus.phase3 === 'error' ? (
              <div className={styles.phaseError}>
                <h3>Phase 3 Error</h3>
                <p>{error}</p>
                <button onClick={fetchPhase3} className={styles.retryButton}>Retry Phase 3</button>
              </div>
            ) : phaseStatus.phase3 === 'completed' ? (
              renderPhase3()
            ) : null
          )}
        </motion.div>
      </AnimatePresence>

      {phase3Data && (
        <div className={styles.footer}>
          <div className={styles.recommendations}>
            <h3>Key Recommendations</h3>
            <ol>
              {(phase3Data.key_recommendations || []).map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ol>
          </div>
          <div className={styles.successFactors}>
            <h3>Critical Success Factors</h3>
            <ul>
              {(phase3Data.critical_success_factors || []).map((factor, idx) => (
                <li key={idx}>{factor}</li>
              ))}
            </ul>
          </div>
          <div className={styles.nextSteps}>
            <h3>Next Steps</h3>
            {(phase3Data.next_steps || []).map((step, idx) => (
              <div key={idx} className={styles.nextStep}>
                <h4>{step.timeline}</h4>
                <ul>
                  {(step.actions || []).map((action, aidx) => (
                    <li key={aidx}>{action}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};