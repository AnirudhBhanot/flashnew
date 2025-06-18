import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Progress, Button, Tabs, Space, Statistic, Tag, Alert, List, Divider, message } from 'antd';
import {
  RadarChartOutlined,
  AuditOutlined,
  CheckCircleOutlined,
  WarningOutlined,
  InfoCircleOutlined,
  ArrowRightOutlined,
  GlobalOutlined,
  TeamOutlined,
  ThunderboltOutlined,
  BulbOutlined,
  RiseOutlined,
  FallOutlined,
  SafetyOutlined,
  FireOutlined,
  LoadingOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import ExternalReality from './ExternalReality';
import InternalAudit from './InternalAudit';
import styles from './index.module.scss';
import { apiService } from '../../../services/api';
import useAssessmentStore from '../../../store/assessmentStore';

interface PhaseData {
  externalReality: {
    completion: number;
    overallScore: number;
    keyInsights: string[];
  };
  internalAudit: {
    completion: number;
    overallScore: number;
    keyInsights: string[];
  };
}

const Phase1Context: React.FC = () => {
  const navigate = useNavigate();
  const assessmentData = useAssessmentStore(state => state.data);
  const [activeTab, setActiveTab] = useState('overview');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [llmInsights, setLlmInsights] = useState<any>(null);
  const [phaseData, setPhaseData] = useState<PhaseData>({
    externalReality: {
      completion: 0,
      overallScore: 0,
      keyInsights: []
    },
    internalAudit: {
      completion: 0,
      overallScore: 0,
      keyInsights: []
    }
  });

  // Calculate phase completion
  const phaseCompletion = Math.round(
    (phaseData.externalReality.completion + phaseData.internalAudit.completion) / 2
  );

  // Load and analyze data from localStorage
  useEffect(() => {
    analyzeExternalReality();
    analyzeInternalAudit();
  }, [activeTab]);

  // Pre-fill data from initial assessment
  const prefillFromAssessment = () => {
    if (!assessmentData.companyInfo?.name) {
      message.warning('Please complete the initial assessment first');
      return;
    }

    // Pre-fill internal audit SWOT from assessment data
    const internalAudit = {
      strengths: [],
      weaknesses: [],
      opportunities: [],
      threats: [],
      capital: {
        score: assessmentData.capital?.burnRate ? 7 : 5,
        runway: assessmentData.capital?.runway || 12,
        unitEconomics: assessmentData.capital?.unitEconomics || false
      },
      advantage: {
        score: assessmentData.advantage?.networkEffects ? 8 : 5
      },
      market: {
        score: 7,
        growthRate: 25
      },
      people: {
        score: assessmentData.people?.foundersExperience > 5 ? 8 : 6,
        teamCompleteness: 70
      }
    };

    // Generate SWOT based on assessment data
    if (assessmentData.capital?.runway && assessmentData.capital.runway > 18) {
      internalAudit.strengths.push('Strong financial runway');
    }
    if (assessmentData.advantage?.networkEffects) {
      internalAudit.strengths.push('Network effects present');
    }
    if (assessmentData.people?.foundersExperience > 10) {
      internalAudit.strengths.push('Experienced founding team');
    }

    if (assessmentData.capital?.burnRate > 200000) {
      internalAudit.weaknesses.push('High burn rate');
    }
    if (!assessmentData.advantage?.ipProtection) {
      internalAudit.weaknesses.push('Limited IP protection');
    }

    internalAudit.opportunities.push('Growing market demand');
    internalAudit.opportunities.push('Partnership opportunities');

    internalAudit.threats.push('Competitive market dynamics');
    internalAudit.threats.push('Regulatory changes');

    localStorage.setItem('deepDive_internalAudit', JSON.stringify(internalAudit));
    
    // Pre-fill external reality with moderate scores
    const externalReality = {
      supplierPower: { score: 5, notes: 'Moderate supplier influence' },
      customerPower: { score: 6, notes: 'Customers have alternatives' },
      industryRivalry: { score: 7, notes: 'Competitive market' },
      substituteThreat: { score: 5, notes: 'Some substitutes exist' },
      newEntrantRisk: { score: 6, notes: 'Moderate barriers to entry' }
    };
    
    localStorage.setItem('deepDive_externalReality', JSON.stringify(externalReality));
    
    message.success('Data pre-filled from initial assessment');
    
    // Re-analyze to update UI
    analyzeExternalReality();
    analyzeInternalAudit();
  };

  const analyzeExternalReality = () => {
    const savedData = localStorage.getItem('deepDive_externalReality');
    if (savedData) {
      const data = JSON.parse(savedData);
      const forces = Object.values(data) as Array<{ score: number; notes: string }>;
      const completedForces = forces.filter(force => force.score > 0);
      const completion = (completedForces.length / forces.length) * 100;
      
      // Calculate average score
      const avgScore = completedForces.length > 0
        ? completedForces.reduce((sum, force) => sum + force.score, 0) / completedForces.length
        : 0;

      // Generate insights based on scores
      const insights: string[] = [];
      if (data.industryRivalry?.score >= 7) {
        insights.push('High competitive intensity requires strong differentiation');
      }
      if (data.customerPower?.score >= 7) {
        insights.push('Strong customer bargaining power may pressure margins');
      }
      if (data.substituteThreat?.score >= 6) {
        insights.push('Significant substitute threat demands innovation focus');
      }
      if (data.newEntrantRisk?.score >= 6) {
        insights.push('Low entry barriers increase competitive risk');
      }
      if (avgScore >= 6) {
        insights.push('Overall challenging external environment detected');
      }

      setPhaseData(prev => ({
        ...prev,
        externalReality: {
          completion,
          overallScore: avgScore,
          keyInsights: insights
        }
      }));
    }
  };

  const analyzeInternalAudit = () => {
    const savedData = localStorage.getItem('deepDive_internalAudit');
    if (savedData) {
      const data = JSON.parse(savedData);
      
      // Calculate completion based on all metrics
      let totalMetrics = 0;
      let completedMetrics = 0;
      
      ['capital', 'advantage', 'market', 'people'].forEach(category => {
        if (data[category]) {
          Object.values(data[category]).forEach((value: any) => {
            if (typeof value === 'number' || typeof value === 'boolean') {
              totalMetrics++;
              if (value !== 0 && value !== false) {
                completedMetrics++;
              }
            }
          });
        }
      });

      const completion = totalMetrics > 0 ? (completedMetrics / totalMetrics) * 100 : 0;
      
      // Calculate average score
      const scores = [
        data.capital?.score || 0,
        data.advantage?.score || 0,
        data.market?.score || 0,
        data.people?.score || 0
      ].filter(s => s > 0);
      
      const avgScore = scores.length > 0
        ? scores.reduce((sum, score) => sum + score, 0) / scores.length
        : 0;

      // Generate insights
      const insights: string[] = [];
      if (data.capital?.runway && data.capital.runway < 12) {
        insights.push('Limited runway requires immediate funding focus');
      }
      if (data.capital?.unitEconomics === false) {
        insights.push('Negative unit economics need urgent attention');
      }
      if (data.advantage?.score < 5) {
        insights.push('Weak competitive moat needs strengthening');
      }
      if (data.market?.growthRate < 20) {
        insights.push('Slow market growth may limit expansion potential');
      }
      if (data.people?.teamCompleteness < 70) {
        insights.push('Key team gaps need to be filled');
      }

      setPhaseData(prev => ({
        ...prev,
        internalAudit: {
          completion,
          overallScore: avgScore,
          keyInsights: insights
        }
      }));
    }
  };

  const getCompletionStatus = (completion: number) => {
    if (completion === 100) return { color: 'success', text: 'Complete', icon: <CheckCircleOutlined /> };
    if (completion >= 75) return { color: 'processing', text: 'Almost Done', icon: <InfoCircleOutlined /> };
    if (completion >= 50) return { color: 'warning', text: 'In Progress', icon: <WarningOutlined /> };
    return { color: 'default', text: 'Not Started', icon: <InfoCircleOutlined /> };
  };

  const performLLMAnalysis = async () => {
    try {
      setIsAnalyzing(true);
      
      // Get data from localStorage
      const externalData = localStorage.getItem('deepDive_externalReality');
      const internalData = localStorage.getItem('deepDive_internalAudit');
      
      if (!externalData || !internalData) {
        message.warning('Please complete both External Reality and Internal Audit before running AI analysis');
        return;
      }

      const external = JSON.parse(externalData);
      const internal = JSON.parse(internalData);

      // Prepare request for LLM
      const request = {
        porters_five_forces: {
          supplier_power: {
            rating: external.supplierPower?.score >= 7 ? 'High' : external.supplierPower?.score >= 4 ? 'Medium' : 'Low',
            factors: external.supplierPower?.notes ? [external.supplierPower.notes] : [],
            score: external.supplierPower?.score || 0
          },
          buyer_power: {
            rating: external.customerPower?.score >= 7 ? 'High' : external.customerPower?.score >= 4 ? 'Medium' : 'Low',
            factors: external.customerPower?.notes ? [external.customerPower.notes] : [],
            score: external.customerPower?.score || 0
          },
          competitive_rivalry: {
            rating: external.industryRivalry?.score >= 7 ? 'High' : external.industryRivalry?.score >= 4 ? 'Medium' : 'Low',
            factors: external.industryRivalry?.notes ? [external.industryRivalry.notes] : [],
            score: external.industryRivalry?.score || 0
          },
          threat_of_substitution: {
            rating: external.substituteThreat?.score >= 7 ? 'High' : external.substituteThreat?.score >= 4 ? 'Medium' : 'Low',
            factors: external.substituteThreat?.notes ? [external.substituteThreat.notes] : [],
            score: external.substituteThreat?.score || 0
          },
          threat_of_new_entry: {
            rating: external.newEntrantRisk?.score >= 7 ? 'High' : external.newEntrantRisk?.score >= 4 ? 'Medium' : 'Low',
            factors: external.newEntrantRisk?.notes ? [external.newEntrantRisk.notes] : [],
            score: external.newEntrantRisk?.score || 0
          }
        },
        internal_audit: {
          strengths: internal.strengths || [],
          weaknesses: internal.weaknesses || [],
          opportunities: internal.opportunities || [],
          threats: internal.threats || []
        }
      };

      const response = await apiService.analyzePhase1DeepDive(request);
      setLlmInsights(response);
      message.success('AI analysis completed successfully!');
      
      // Update phase data with LLM insights
      if (response.competitive_position) {
        setPhaseData(prev => ({
          ...prev,
          externalReality: {
            ...prev.externalReality,
            keyInsights: [
              ...prev.externalReality.keyInsights,
              ...(response.competitive_position.key_strengths || []).slice(0, 2)
            ]
          },
          internalAudit: {
            ...prev.internalAudit,
            keyInsights: [
              ...prev.internalAudit.keyInsights,
              ...(response.recommendations || []).slice(0, 2).map((r: any) => r.action)
            ]
          }
        }));
      }
    } catch (error) {
      console.error('LLM analysis error:', error);
      message.error('Failed to perform AI analysis. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderOverview = () => (
    <div className={styles.overview}>
      <Row gutter={[24, 24]}>
        <Col span={24}>
          <Card className={styles.phaseHeader}>
            <Row align="middle" justify="space-between">
              <Col>
                <Space direction="vertical" size={0}>
                  <h1 className={styles.phaseTitle}>Phase 1: Context Analysis</h1>
                  <p className={styles.phaseDescription}>
                    Comprehensive assessment of external market forces and internal capabilities
                  </p>
                </Space>
              </Col>
              <Col>
                <Space direction="horizontal" size={16} align="center">
                  {phaseCompletion < 50 && assessmentData.companyInfo?.name && (
                    <Button 
                      type="default"
                      icon={<ThunderboltOutlined />}
                      onClick={prefillFromAssessment}
                    >
                      Pre-fill from Assessment
                    </Button>
                  )}
                  <Progress
                    type="circle"
                    percent={phaseCompletion}
                    strokeColor="#1d1d1f"
                    format={percent => `${percent}%`}
                  />
                </Space>
              </Col>
            </Row>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card 
            className={styles.componentCard}
            hoverable
            onClick={() => setActiveTab('external')}
          >
            <Row gutter={16} align="middle">
              <Col span={6}>
                <div className={styles.iconWrapper}>
                  <GlobalOutlined className={styles.componentIcon} />
                </div>
              </Col>
              <Col span={18}>
                <h3>External Reality Check</h3>
                <p>Porter's Five Forces analysis of competitive environment</p>
                <Progress 
                  percent={Math.round(phaseData.externalReality.completion)} 
                  status={getCompletionStatus(phaseData.externalReality.completion).color as any}
                />
                <Tag color={getCompletionStatus(phaseData.externalReality.completion).color}>
                  {getCompletionStatus(phaseData.externalReality.completion).text}
                </Tag>
              </Col>
            </Row>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card 
            className={styles.componentCard}
            hoverable
            onClick={() => setActiveTab('internal')}
          >
            <Row gutter={16} align="middle">
              <Col span={6}>
                <div className={styles.iconWrapper}>
                  <AuditOutlined className={styles.componentIcon} />
                </div>
              </Col>
              <Col span={18}>
                <h3>Internal Audit</h3>
                <p>CAMP framework assessment of internal capabilities</p>
                <Progress 
                  percent={Math.round(phaseData.internalAudit.completion)} 
                  status={getCompletionStatus(phaseData.internalAudit.completion).color as any}
                />
                <Tag color={getCompletionStatus(phaseData.internalAudit.completion).color}>
                  {getCompletionStatus(phaseData.internalAudit.completion).text}
                </Tag>
              </Col>
            </Row>
          </Card>
        </Col>

        {phaseCompletion > 0 && (
          <>
            <Col span={24}>
              <Divider>Key Insights & Recommendations</Divider>
            </Col>

            <Col xs={24} lg={12}>
              <Card title={
                <Space>
                  <FireOutlined />
                  External Threats
                </Space>
              } className={styles.insightCard}>
                {phaseData.externalReality.keyInsights.length > 0 ? (
                  <List
                    size="small"
                    dataSource={phaseData.externalReality.keyInsights}
                    renderItem={item => (
                      <List.Item>
                        <Space>
                          <WarningOutlined style={{ color: '#ff3b30' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                ) : (
                  <p className={styles.noData}>Complete External Reality Check to see insights</p>
                )}
              </Card>
            </Col>

            <Col xs={24} lg={12}>
              <Card title={
                <Space>
                  <BulbOutlined />
                  Internal Priorities
                </Space>
              } className={styles.insightCard}>
                {phaseData.internalAudit.keyInsights.length > 0 ? (
                  <List
                    size="small"
                    dataSource={phaseData.internalAudit.keyInsights}
                    renderItem={item => (
                      <List.Item>
                        <Space>
                          <InfoCircleOutlined style={{ color: '#1d1d1f' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                ) : (
                  <p className={styles.noData}>Complete Internal Audit to see insights</p>
                )}
              </Card>
            </Col>

            <Col span={24}>
              <Card className={styles.summaryCard}>
                <Row gutter={[24, 16]}>
                  <Col xs={24} md={8}>
                    <Statistic
                      title="External Environment Score"
                      value={phaseData.externalReality.overallScore.toFixed(1)}
                      suffix="/ 10"
                      prefix={phaseData.externalReality.overallScore >= 6 ? <FallOutlined /> : <RiseOutlined />}
                      valueStyle={{ 
                        color: phaseData.externalReality.overallScore >= 6 ? '#ff3b30' : '#34c759' 
                      }}
                    />
                    <p className={styles.scoreDescription}>
                      {phaseData.externalReality.overallScore >= 6 
                        ? 'Challenging environment' 
                        : 'Favorable conditions'}
                    </p>
                  </Col>
                  <Col xs={24} md={8}>
                    <Statistic
                      title="Internal Strength Score"
                      value={phaseData.internalAudit.overallScore.toFixed(1)}
                      suffix="/ 10"
                      prefix={phaseData.internalAudit.overallScore >= 6 ? <RiseOutlined /> : <FallOutlined />}
                      valueStyle={{ 
                        color: phaseData.internalAudit.overallScore >= 6 ? '#34c759' : '#ff3b30' 
                      }}
                    />
                    <p className={styles.scoreDescription}>
                      {phaseData.internalAudit.overallScore >= 6 
                        ? 'Strong position' 
                        : 'Needs improvement'}
                    </p>
                  </Col>
                  <Col xs={24} md={8}>
                    <div className={styles.readinessScore}>
                      <h4>Strategic Readiness</h4>
                      <Progress
                        type="dashboard"
                        percent={phaseCompletion}
                        gapDegree={30}
                        strokeColor="#1d1d1f"
                      />
                    </div>
                  </Col>
                </Row>
              </Card>
            </Col>

            {phaseCompletion === 100 && (
              <Col span={24}>
                <Alert
                  message="Phase 1 Complete!"
                  description="You've completed the Context Analysis phase. Your startup's external environment and internal capabilities have been thoroughly assessed."
                  type="success"
                  showIcon
                  action={
                    <Space>
                      <Button 
                        type="default"
                        icon={isAnalyzing ? <LoadingOutlined /> : <BulbOutlined />}
                        onClick={performLLMAnalysis}
                        loading={isAnalyzing}
                      >
                        Get AI Insights
                      </Button>
                      <Button 
                        type="primary" 
                        icon={<ArrowRightOutlined />}
                        onClick={() => navigate('/deep-dive/phase2')}
                      >
                        Proceed to Phase 2
                      </Button>
                    </Space>
                  }
                />
              </Col>
            )}

            {llmInsights && (
              <Col span={24}>
                <Card title="AI-Powered Strategic Insights" className={styles.llmInsightsCard}>
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <h4>Competitive Position Assessment</h4>
                      <Tag color={llmInsights.competitive_position?.overall_rating === 'Strong' ? 'success' : 
                                 llmInsights.competitive_position?.overall_rating === 'Moderate' ? 'warning' : 'error'}>
                        {llmInsights.competitive_position?.overall_rating || 'Unknown'}
                      </Tag>
                      <p>{llmInsights.competitive_position?.summary}</p>
                    </Col>
                    
                    {llmInsights.strategic_gaps?.length > 0 && (
                      <Col span={12}>
                        <h4>Strategic Gaps</h4>
                        <List
                          size="small"
                          dataSource={llmInsights.strategic_gaps}
                          renderItem={(gap: any) => (
                            <List.Item>
                              <Tag color={gap.urgency === 'High' ? 'red' : gap.urgency === 'Medium' ? 'orange' : 'blue'}>
                                {gap.urgency}
                              </Tag>
                              {gap.gap}
                            </List.Item>
                          )}
                        />
                      </Col>
                    )}
                    
                    {llmInsights.recommendations?.length > 0 && (
                      <Col span={12}>
                        <h4>Key Recommendations</h4>
                        <List
                          size="small"
                          dataSource={llmInsights.recommendations}
                          renderItem={(rec: any) => (
                            <List.Item>
                              <Tag color={rec.priority === 'High' ? 'red' : rec.priority === 'Medium' ? 'orange' : 'blue'}>
                                {rec.priority}
                              </Tag>
                              {rec.action}
                            </List.Item>
                          )}
                        />
                      </Col>
                    )}
                  </Row>
                </Card>
              </Col>
            )}
          </>
        )}
      </Row>
    </div>
  );

  const tabItems = [
    {
      key: 'overview',
      label: (
        <Space>
          <RadarChartOutlined />
          Overview
        </Space>
      ),
      children: renderOverview()
    },
    {
      key: 'external',
      label: (
        <Space>
          <GlobalOutlined />
          External Reality Check
        </Space>
      ),
      children: <ExternalReality />
    },
    {
      key: 'internal',
      label: (
        <Space>
          <AuditOutlined />
          Internal Audit
        </Space>
      ),
      children: <InternalAudit />
    }
  ];

  return (
    <div className={styles.phase1Container}>
      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={tabItems}
        className={styles.phaseTabs}
      />
    </div>
  );
};

export default Phase1Context;