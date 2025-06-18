import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Progress, Rate, Tag, Button, Space, Alert, Input, Select, Slider, Timeline, Tooltip, Modal, Form } from 'antd';
import {
  EyeOutlined,
  RocketOutlined,
  FlagOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
  ArrowRightOutlined,
  SyncOutlined,
  ThunderboltOutlined,
  AimOutlined,
  CompassOutlined,
  DashboardOutlined,
  RiseOutlined,
  FireOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  BulbOutlined,
  TeamOutlined,
  DollarOutlined,
  GlobalOutlined,
  SafetyOutlined,
  EditOutlined,
  PlusOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import styles from './VisionRealityGap.module.scss';

const { TextArea } = Input;
const { Option } = Select;

interface VisionClarity {
  visionStatement: string;
  measurability: number;
  teamAlignment: number;
  timeHorizon: string;
  strategicClarity: number;
  inspirational: number;
}

interface CurrentReality {
  marketPosition: number;
  resourceAvailability: number;
  operationalCapability: number;
  teamReadiness: number;
  technologyMaturity: number;
  customerBase: number;
  financialHealth: number;
  brandRecognition: number;
}

interface Gap {
  id: string;
  area: string;
  currentState: number;
  desiredState: number;
  gap: number;
  impact: 'critical' | 'high' | 'medium' | 'low';
  effort: 'high' | 'medium' | 'low';
  timeline: string;
  strategy: string;
  risks: string[];
}

interface BridgingStrategy {
  id: string;
  title: string;
  description: string;
  timeline: string;
  resources: string[];
  milestones: string[];
  priority: number;
}

interface VisionRealityGapProps {
  companyId: string;
  onUpdate?: (data: any) => void;
}

const VisionRealityGap: React.FC<VisionRealityGapProps> = ({ companyId, onUpdate }) => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [editingStrategy, setEditingStrategy] = useState<string | null>(null);
  const [showStrategyModal, setShowStrategyModal] = useState(false);
  
  const [visionClarity, setVisionClarity] = useState<VisionClarity>({
    visionStatement: 'To revolutionize enterprise collaboration through AI-powered insights, becoming the global leader in workplace productivity solutions by 2030',
    measurability: 75,
    teamAlignment: 68,
    timeHorizon: '5-7 years',
    strategicClarity: 72,
    inspirational: 85
  });

  const [currentReality, setCurrentReality] = useState<CurrentReality>({
    marketPosition: 35,
    resourceAvailability: 45,
    operationalCapability: 52,
    teamReadiness: 48,
    technologyMaturity: 65,
    customerBase: 28,
    financialHealth: 42,
    brandRecognition: 22
  });

  const [gaps, setGaps] = useState<Gap[]>([
    {
      id: '1',
      area: 'Market Position',
      currentState: 35,
      desiredState: 85,
      gap: 50,
      impact: 'critical',
      effort: 'high',
      timeline: '24 months',
      strategy: 'Aggressive market expansion through partnerships and targeted acquisitions',
      risks: ['Competition from established players', 'Market saturation', 'Execution challenges']
    },
    {
      id: '2',
      area: 'Team Capabilities',
      currentState: 48,
      desiredState: 90,
      gap: 42,
      impact: 'critical',
      effort: 'high',
      timeline: '18 months',
      strategy: 'Strategic hiring in key roles, comprehensive training programs, culture transformation',
      risks: ['Talent shortage', 'Cultural resistance', 'Integration challenges']
    },
    {
      id: '3',
      area: 'Technology Platform',
      currentState: 65,
      desiredState: 95,
      gap: 30,
      impact: 'high',
      effort: 'medium',
      timeline: '12 months',
      strategy: 'Accelerate R&D, form technology partnerships, adopt best-in-class tools',
      risks: ['Technical debt', 'Integration complexity', 'Scalability issues']
    },
    {
      id: '4',
      area: 'Financial Resources',
      currentState: 42,
      desiredState: 80,
      gap: 38,
      impact: 'high',
      effort: 'high',
      timeline: '12-18 months',
      strategy: 'Series B fundraising, revenue acceleration, operational efficiency',
      risks: ['Market conditions', 'Investor sentiment', 'Burn rate']
    },
    {
      id: '5',
      area: 'Brand Recognition',
      currentState: 22,
      desiredState: 75,
      gap: 53,
      impact: 'medium',
      effort: 'medium',
      timeline: '24 months',
      strategy: 'Thought leadership, strategic PR, customer success stories',
      risks: ['Message consistency', 'Market noise', 'ROI measurement']
    }
  ]);

  const [bridgingStrategies, setBridgingStrategies] = useState<BridgingStrategy[]>([
    {
      id: '1',
      title: 'Talent Acquisition Blitz',
      description: 'Rapid scaling of team with focus on senior engineering and sales leadership',
      timeline: 'Q1-Q2 2025',
      resources: ['$2M hiring budget', 'Executive search firm', 'Employee referral program'],
      milestones: ['Hire VP Engineering', 'Build sales team to 20', 'Establish EU office'],
      priority: 1
    },
    {
      id: '2',
      title: 'Product-Market Fit Acceleration',
      description: 'Intensive customer development and product iteration cycles',
      timeline: 'Q1-Q3 2025',
      resources: ['Product team expansion', 'Customer research budget', 'Beta program'],
      milestones: ['100 customer interviews', 'Launch v2.0', 'Achieve 80+ NPS'],
      priority: 2
    },
    {
      id: '3',
      title: 'Strategic Partnership Program',
      description: 'Form alliances with enterprise software vendors and system integrators',
      timeline: 'Q2-Q4 2025',
      resources: ['BD team', 'Partnership incentives', 'Integration resources'],
      milestones: ['3 strategic partnerships', 'Joint go-to-market', '1000 referred customers'],
      priority: 3
    }
  ]);

  const [overallGapScore, setOverallGapScore] = useState(0);
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    calculateOverallGap();
    loadData();
  }, [companyId]);

  const loadData = () => {
    const savedData = localStorage.getItem(`visionRealityGap_${companyId}`);
    if (savedData) {
      const parsed = JSON.parse(savedData);
      setVisionClarity(parsed.visionClarity);
      setCurrentReality(parsed.currentReality);
      setGaps(parsed.gaps);
      setBridgingStrategies(parsed.bridgingStrategies);
    }
  };

  const saveData = () => {
    const data = { visionClarity, currentReality, gaps, bridgingStrategies };
    localStorage.setItem(`visionRealityGap_${companyId}`, JSON.stringify(data));
    onUpdate?.(data);
  };

  const calculateOverallGap = () => {
    setIsCalculating(true);
    
    // Calculate vision score (0-100)
    const visionScore = (
      visionClarity.measurability * 0.3 +
      visionClarity.teamAlignment * 0.3 +
      visionClarity.strategicClarity * 0.2 +
      visionClarity.inspirational * 0.2
    );
    
    // Calculate reality score (0-100)
    const realityScore = Object.values(currentReality).reduce((sum, val) => sum + val, 0) / 
                        Object.keys(currentReality).length;
    
    // Calculate gap score (higher is worse)
    const gapScore = Math.abs(visionScore - realityScore);
    setOverallGapScore(Math.round(gapScore));
    
    setTimeout(() => setIsCalculating(false), 500);
  };

  const getGapSeverity = (gap: number) => {
    if (gap >= 40) return { color: '#f5222d', text: 'Critical' };
    if (gap >= 25) return { color: '#fa8c16', text: 'High' };
    if (gap >= 15) return { color: '#faad14', text: 'Medium' };
    return { color: '#52c41a', text: 'Low' };
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'critical': return '#f5222d';
      case 'high': return '#fa8c16';
      case 'medium': return '#faad14';
      case 'low': return '#52c41a';
      default: return '#8c8c8c';
    }
  };

  const getEffortColor = (effort: string) => {
    switch (effort) {
      case 'high': return '#f5222d';
      case 'medium': return '#faad14';
      case 'low': return '#52c41a';
      default: return '#8c8c8c';
    }
  };

  const handleAddStrategy = (values: any) => {
    const newStrategy: BridgingStrategy = {
      id: Date.now().toString(),
      ...values,
      resources: values.resources.split(',').map((r: string) => r.trim()),
      milestones: values.milestones.split(',').map((m: string) => m.trim())
    };
    
    setBridgingStrategies([...bridgingStrategies, newStrategy]);
    setShowStrategyModal(false);
    form.resetFields();
  };

  const renderVisionAssessment = () => (
    <Card 
      title={
        <Space>
          <EyeOutlined style={{ color: '#1890ff' }} />
          <span>Vision Clarity Assessment</span>
        </Space>
      }
      className={styles.visionCard}
    >
      <div className={styles.visionStatement}>
        <TextArea
          value={visionClarity.visionStatement}
          onChange={(e) => setVisionClarity({ ...visionClarity, visionStatement: e.target.value })}
          placeholder="Enter your company's vision statement..."
          rows={3}
          className={styles.visionInput}
        />
      </div>
      
      <Row gutter={[16, 16]} className={styles.visionMetrics}>
        <Col span={12}>
          <div className={styles.metric}>
            <span><AimOutlined /> Measurability</span>
            <Progress percent={visionClarity.measurability} strokeColor="#1890ff" />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metric}>
            <span><TeamOutlined /> Team Alignment</span>
            <Progress percent={visionClarity.teamAlignment} strokeColor="#52c41a" />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metric}>
            <span><CompassOutlined /> Strategic Clarity</span>
            <Progress percent={visionClarity.strategicClarity} strokeColor="#722ed1" />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metric}>
            <span><FireOutlined /> Inspirational Power</span>
            <Progress percent={visionClarity.inspirational} strokeColor="#fa541c" />
          </div>
        </Col>
      </Row>
      
      <div className={styles.timeHorizon}>
        <span>Time Horizon:</span>
        <Select 
          value={visionClarity.timeHorizon}
          onChange={(value) => setVisionClarity({ ...visionClarity, timeHorizon: value })}
          style={{ width: 150 }}
        >
          <Option value="1-2 years">1-2 years</Option>
          <Option value="3-5 years">3-5 years</Option>
          <Option value="5-7 years">5-7 years</Option>
          <Option value="7-10 years">7-10 years</Option>
        </Select>
      </div>
    </Card>
  );

  const renderCurrentReality = () => (
    <Card 
      title={
        <Space>
          <DashboardOutlined style={{ color: '#13c2c2' }} />
          <span>Current Reality Assessment</span>
        </Space>
      }
      className={styles.realityCard}
    >
      <div className={styles.realityMetrics}>
        <div className={styles.metricGroup}>
          <h4><GlobalOutlined /> Market & Customer</h4>
          <div className={styles.sliderMetric}>
            <span>Market Position</span>
            <Slider 
              value={currentReality.marketPosition}
              onChange={(value) => setCurrentReality({ ...currentReality, marketPosition: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
          <div className={styles.sliderMetric}>
            <span>Customer Base</span>
            <Slider 
              value={currentReality.customerBase}
              onChange={(value) => setCurrentReality({ ...currentReality, customerBase: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
          <div className={styles.sliderMetric}>
            <span>Brand Recognition</span>
            <Slider 
              value={currentReality.brandRecognition}
              onChange={(value) => setCurrentReality({ ...currentReality, brandRecognition: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
        </div>
        
        <div className={styles.metricGroup}>
          <h4><RocketOutlined /> Operations & Technology</h4>
          <div className={styles.sliderMetric}>
            <span>Operational Capability</span>
            <Slider 
              value={currentReality.operationalCapability}
              onChange={(value) => setCurrentReality({ ...currentReality, operationalCapability: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
          <div className={styles.sliderMetric}>
            <span>Technology Maturity</span>
            <Slider 
              value={currentReality.technologyMaturity}
              onChange={(value) => setCurrentReality({ ...currentReality, technologyMaturity: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
        </div>
        
        <div className={styles.metricGroup}>
          <h4><TeamOutlined /> Team & Resources</h4>
          <div className={styles.sliderMetric}>
            <span>Team Readiness</span>
            <Slider 
              value={currentReality.teamReadiness}
              onChange={(value) => setCurrentReality({ ...currentReality, teamReadiness: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
          <div className={styles.sliderMetric}>
            <span>Resource Availability</span>
            <Slider 
              value={currentReality.resourceAvailability}
              onChange={(value) => setCurrentReality({ ...currentReality, resourceAvailability: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
          <div className={styles.sliderMetric}>
            <span>Financial Health</span>
            <Slider 
              value={currentReality.financialHealth}
              onChange={(value) => setCurrentReality({ ...currentReality, financialHealth: value })}
              marks={{ 0: '0', 50: '50', 100: '100' }}
            />
          </div>
        </div>
      </div>
    </Card>
  );

  const renderGapAnalysis = () => (
    <Card 
      title={
        <Space>
          <ThunderboltOutlined style={{ color: '#f5222d' }} />
          <span>Gap Analysis</span>
        </Space>
      }
      extra={
        <Tag color={getGapSeverity(overallGapScore).color}>
          Overall Gap: {overallGapScore}%
        </Tag>
      }
      className={styles.gapAnalysisCard}
    >
      <div className={styles.gapVisualizer}>
        <div className={styles.gapHeader}>
          <div className={styles.currentState}>
            <h4>Current Reality</h4>
            <div className={styles.scoreCircle}>
              {Math.round(Object.values(currentReality).reduce((a, b) => a + b, 0) / Object.keys(currentReality).length)}
            </div>
          </div>
          
          <div className={styles.gapIndicator}>
            <ArrowRightOutlined style={{ fontSize: 48, color: getGapSeverity(overallGapScore).color }} />
            <div className={styles.gapDistance}>
              <span className={styles.gapValue}>{overallGapScore}%</span>
              <span className={styles.gapLabel}>Gap to Close</span>
            </div>
          </div>
          
          <div className={styles.visionState}>
            <h4>Vision Target</h4>
            <div className={styles.scoreCircle}>
              {Math.round((visionClarity.measurability + visionClarity.teamAlignment + 
                          visionClarity.strategicClarity + visionClarity.inspirational) / 4)}
            </div>
          </div>
        </div>
      </div>
      
      <div className={styles.gapsList}>
        {gaps.map((gap) => (
          <div key={gap.id} className={styles.gapItem}>
            <div className={styles.gapHeader}>
              <h4>{gap.area}</h4>
              <Space>
                <Tag color={getImpactColor(gap.impact)}>Impact: {gap.impact}</Tag>
                <Tag color={getEffortColor(gap.effort)}>Effort: {gap.effort}</Tag>
                <Tag><ClockCircleOutlined /> {gap.timeline}</Tag>
              </Space>
            </div>
            
            <div className={styles.gapProgress}>
              <div className={styles.progressBar}>
                <div className={styles.currentBar} style={{ width: `${gap.currentState}%` }}>
                  <span>{gap.currentState}%</span>
                </div>
                <div className={styles.gapBar} style={{ width: `${gap.gap}%`, left: `${gap.currentState}%` }}>
                  <span>{gap.gap}% gap</span>
                </div>
                <div className={styles.targetMarker} style={{ left: `${gap.desiredState}%` }}>
                  <span>{gap.desiredState}%</span>
                </div>
              </div>
            </div>
            
            <div className={styles.gapStrategy}>
              <p><BulbOutlined /> {gap.strategy}</p>
            </div>
            
            {gap.risks.length > 0 && (
              <div className={styles.gapRisks}>
                <span className={styles.riskLabel}><WarningOutlined /> Key Risks:</span>
                {gap.risks.map((risk, index) => (
                  <Tag key={index} color="orange">{risk}</Tag>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );

  const renderBridgingStrategies = () => (
    <Card 
      title={
        <Space>
          <FlagOutlined style={{ color: '#722ed1' }} />
          <span>Bridging Strategies</span>
        </Space>
      }
      extra={
        <Button 
          type="primary" 
          icon={<PlusOutlined />}
          onClick={() => setShowStrategyModal(true)}
        >
          Add Strategy
        </Button>
      }
      className={styles.strategiesCard}
    >
      <Timeline mode="left">
        {bridgingStrategies
          .sort((a, b) => a.priority - b.priority)
          .map((strategy) => (
            <Timeline.Item 
              key={strategy.id}
              color={strategy.priority === 1 ? 'red' : strategy.priority === 2 ? 'orange' : 'blue'}
              label={strategy.timeline}
            >
              <div className={styles.strategyItem}>
                <div className={styles.strategyHeader}>
                  <h4>{strategy.title}</h4>
                  <Tag color={strategy.priority === 1 ? 'red' : strategy.priority === 2 ? 'orange' : 'blue'}>
                    Priority {strategy.priority}
                  </Tag>
                </div>
                <p className={styles.strategyDescription}>{strategy.description}</p>
                
                <div className={styles.strategyDetails}>
                  <div className={styles.resources}>
                    <span className={styles.label}><DollarOutlined /> Resources:</span>
                    <ul>
                      {strategy.resources.map((resource, index) => (
                        <li key={index}>{resource}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className={styles.milestones}>
                    <span className={styles.label}><CheckCircleOutlined /> Milestones:</span>
                    <ul>
                      {strategy.milestones.map((milestone, index) => (
                        <li key={index}>{milestone}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </Timeline.Item>
          ))}
      </Timeline>
    </Card>
  );

  const renderRiskAssessment = () => {
    const allRisks = gaps.flatMap(gap => gap.risks);
    const uniqueRisks = [...new Set(allRisks)];
    
    return (
      <Card 
        title={
          <Space>
            <SafetyOutlined style={{ color: '#fa8c16' }} />
            <span>Vision Achievement Risk Assessment</span>
          </Space>
        }
        className={styles.riskCard}
      >
        <Alert
          message="Key Risk Factors"
          description="These risks could impact your ability to achieve the vision"
          type="warning"
          showIcon
          className={styles.riskAlert}
        />
        
        <div className={styles.riskGrid}>
          {uniqueRisks.map((risk, index) => (
            <div key={index} className={styles.riskItem}>
              <ExclamationCircleOutlined style={{ color: '#fa8c16' }} />
              <span>{risk}</span>
            </div>
          ))}
        </div>
        
        <div className={styles.riskMitigation}>
          <h4>Mitigation Strategies</h4>
          <Space direction="vertical" style={{ width: '100%' }}>
            <Alert
              message="Regular Progress Reviews"
              description="Weekly team syncs and monthly board reviews to track gap closure"
              type="info"
              showIcon
            />
            <Alert
              message="Agile Resource Allocation"
              description="Flexible budget and team allocation based on priority shifts"
              type="info"
              showIcon
            />
            <Alert
              message="Partnership Acceleration"
              description="Strategic alliances to rapidly close capability gaps"
              type="info"
              showIcon
            />
          </Space>
        </div>
      </Card>
    );
  };

  return (
    <div className={styles.visionRealityGap}>
      <div className={styles.header}>
        <h1>Vision-Reality Gap Analysis</h1>
        <p>Identify and bridge the gaps between your vision and current reality</p>
      </div>
      
      <Row gutter={[24, 24]}>
        <Col span={12}>
          {renderVisionAssessment()}
        </Col>
        <Col span={12}>
          {renderCurrentReality()}
        </Col>
      </Row>
      
      {renderGapAnalysis()}
      {renderBridgingStrategies()}
      {renderRiskAssessment()}
      
      <div className={styles.actions}>
        <Space>
          <Button 
            type="primary" 
            size="large"
            icon={<CheckCircleOutlined />}
            onClick={saveData}
            loading={isCalculating}
          >
            Save Analysis
          </Button>
          <Button 
            size="large"
            icon={<SyncOutlined />}
            onClick={calculateOverallGap}
            loading={isCalculating}
          >
            Recalculate Gaps
          </Button>
          <Button 
            type="primary"
            size="large"
            onClick={() => {
              // Check if assessment is complete
              const hasVision = visionClarity.visionStatement.length > 0;
              const hasStrategies = bridgingStrategies.length > 0;
              const hasGaps = gaps.length > 0;
              
              if (hasVision && hasStrategies && hasGaps) {
                saveData();
                // Dispatch phase completion event
                window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
                  detail: { phaseId: 'phase2' } 
                }));
                alert('Phase 2 completed! Phase 3 is now unlocked.');
                // Navigate to Phase 3
                setTimeout(() => navigate('/deep-dive/phase3'), 1000);
              } else {
                alert('Please complete vision statement, identify gaps, and define bridging strategies before marking this phase as complete.');
              }
            }}
            disabled={visionClarity.visionStatement.length === 0 || bridgingStrategies.length === 0 || gaps.length === 0}
          >
            Complete Phase 2
          </Button>
        </Space>
      </div>
      
      <Modal
        title="Add Bridging Strategy"
        visible={showStrategyModal}
        onCancel={() => setShowStrategyModal(false)}
        footer={null}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleAddStrategy}
        >
          <Form.Item
            name="title"
            label="Strategy Title"
            rules={[{ required: true, message: 'Please enter a title' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <TextArea rows={3} />
          </Form.Item>
          
          <Form.Item
            name="timeline"
            label="Timeline"
            rules={[{ required: true, message: 'Please enter a timeline' }]}
          >
            <Input placeholder="e.g., Q1-Q2 2025" />
          </Form.Item>
          
          <Form.Item
            name="resources"
            label="Resources (comma-separated)"
            rules={[{ required: true, message: 'Please enter resources' }]}
          >
            <TextArea rows={2} placeholder="e.g., $1M budget, 5 engineers, External consultants" />
          </Form.Item>
          
          <Form.Item
            name="milestones"
            label="Milestones (comma-separated)"
            rules={[{ required: true, message: 'Please enter milestones' }]}
          >
            <TextArea rows={2} placeholder="e.g., MVP launch, 100 customers, Series A closed" />
          </Form.Item>
          
          <Form.Item
            name="priority"
            label="Priority"
            rules={[{ required: true, message: 'Please select priority' }]}
          >
            <Select>
              <Option value={1}>Priority 1 (Highest)</Option>
              <Option value={2}>Priority 2</Option>
              <Option value={3}>Priority 3</Option>
              <Option value={4}>Priority 4 (Lowest)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                Add Strategy
              </Button>
              <Button onClick={() => setShowStrategyModal(false)}>
                Cancel
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default VisionRealityGap;