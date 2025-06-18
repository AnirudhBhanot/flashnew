import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Progress, Rate, Tag, Button, Tooltip, Space, Statistic, Alert } from 'antd';
import {
  DollarOutlined,
  RocketOutlined,
  TeamOutlined,
  TrophyOutlined,
  RadarChartOutlined,
  WarningOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  FireOutlined,
  ClockCircleOutlined,
  SafetyOutlined,
  BulbOutlined,
  GlobalOutlined,
  UserOutlined,
  SolutionOutlined,
  FundOutlined,
  ThunderboltOutlined,
  CrownOutlined,
  ExperimentOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import styles from './InternalAudit.module.scss';

interface CAMPMetrics {
  capital: {
    burnRate: number;
    runway: number;
    revenue: number;
    revenueGrowth: number;
    grossMargin: number;
    cashPosition: number;
    unitEconomics: boolean;
    score: number;
  };
  advantage: {
    ipStrength: number;
    technicalMoat: number;
    networkEffects: number;
    brandStrength: number;
    dataAdvantage: number;
    regulatoryBarriers: number;
    score: number;
  };
  market: {
    tamCapture: number;
    growthRate: number;
    marketShare: number;
    productMarketFit: number;
    customerRetention: number;
    nps: number;
    score: number;
  };
  people: {
    teamCompleteness: number;
    leadershipExperience: number;
    technicalExpertise: number;
    cultureFit: number;
    recruitingAbility: number;
    advisorNetwork: number;
    score: number;
  };
}

interface CapabilityGap {
  area: string;
  current: number;
  target: number;
  priority: 'critical' | 'high' | 'medium' | 'low';
  action: string;
}

interface InternalAuditProps {
  companyId: string;
  onUpdate?: (data: any) => void;
}

const InternalAudit: React.FC<InternalAuditProps> = ({ companyId, onUpdate }) => {
  const navigate = useNavigate();
  const [campMetrics, setCampMetrics] = useState<CAMPMetrics>({
    capital: {
      burnRate: 250000,
      runway: 18,
      revenue: 150000,
      revenueGrowth: 25,
      grossMargin: 65,
      cashPosition: 4500000,
      unitEconomics: true,
      score: 0
    },
    advantage: {
      ipStrength: 3.5,
      technicalMoat: 4,
      networkEffects: 2.5,
      brandStrength: 3,
      dataAdvantage: 3.5,
      regulatoryBarriers: 2,
      score: 0
    },
    market: {
      tamCapture: 0.15,
      growthRate: 45,
      marketShare: 2.5,
      productMarketFit: 4,
      customerRetention: 85,
      nps: 45,
      score: 0
    },
    people: {
      teamCompleteness: 75,
      leadershipExperience: 4,
      technicalExpertise: 4.5,
      cultureFit: 4,
      recruitingAbility: 3.5,
      advisorNetwork: 3,
      score: 0
    }
  });

  const [capabilityGaps, setCapabilityGaps] = useState<CapabilityGap[]>([
    {
      area: 'Sales Leadership',
      current: 2,
      target: 5,
      priority: 'critical',
      action: 'Hire VP of Sales with SaaS experience'
    },
    {
      area: 'Data Science',
      current: 3,
      target: 5,
      priority: 'high',
      action: 'Build ML team for product enhancement'
    },
    {
      area: 'Customer Success',
      current: 3.5,
      target: 5,
      priority: 'high',
      action: 'Scale CS team for enterprise clients'
    },
    {
      area: 'Marketing',
      current: 2.5,
      target: 4,
      priority: 'medium',
      action: 'Strengthen demand generation capabilities'
    }
  ]);

  const [overallScore, setOverallScore] = useState(0);
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    calculateScores();
    loadData();
  }, [companyId]);

  const loadData = () => {
    const savedData = localStorage.getItem(`internalAudit_${companyId}`);
    if (savedData) {
      const parsed = JSON.parse(savedData);
      setCampMetrics(parsed.campMetrics);
      setCapabilityGaps(parsed.capabilityGaps);
    }
  };

  const saveData = () => {
    const data = { campMetrics, capabilityGaps };
    localStorage.setItem(`internalAudit_${companyId}`, JSON.stringify(data));
    onUpdate?.(data);
  };

  const calculateScores = () => {
    setIsCalculating(true);
    
    // Calculate Capital Score (0-100)
    const capitalScore = calculateCapitalScore();
    
    // Calculate Advantage Score (0-100)
    const advantageScore = calculateAdvantageScore();
    
    // Calculate Market Score (0-100)
    const marketScore = calculateMarketScore();
    
    // Calculate People Score (0-100)
    const peopleScore = calculatePeopleScore();
    
    setCampMetrics(prev => ({
      ...prev,
      capital: { ...prev.capital, score: capitalScore },
      advantage: { ...prev.advantage, score: advantageScore },
      market: { ...prev.market, score: marketScore },
      people: { ...prev.people, score: peopleScore }
    }));
    
    // Calculate overall score with weighted average
    const overall = (capitalScore * 0.25 + advantageScore * 0.25 + 
                    marketScore * 0.3 + peopleScore * 0.2);
    setOverallScore(Math.round(overall));
    
    setTimeout(() => setIsCalculating(false), 500);
  };

  const calculateCapitalScore = () => {
    const { burnRate, runway, revenueGrowth, grossMargin, unitEconomics } = campMetrics.capital;
    
    let score = 0;
    
    // Runway score (0-25)
    if (runway >= 24) score += 25;
    else if (runway >= 18) score += 20;
    else if (runway >= 12) score += 15;
    else if (runway >= 6) score += 10;
    else score += 5;
    
    // Revenue growth score (0-25)
    if (revenueGrowth >= 100) score += 25;
    else if (revenueGrowth >= 50) score += 20;
    else if (revenueGrowth >= 25) score += 15;
    else if (revenueGrowth >= 10) score += 10;
    else score += 5;
    
    // Gross margin score (0-25)
    if (grossMargin >= 80) score += 25;
    else if (grossMargin >= 70) score += 20;
    else if (grossMargin >= 60) score += 15;
    else if (grossMargin >= 50) score += 10;
    else score += 5;
    
    // Unit economics score (0-25)
    score += unitEconomics ? 25 : 10;
    
    return Math.round(score);
  };

  const calculateAdvantageScore = () => {
    const { ipStrength, technicalMoat, networkEffects, brandStrength, dataAdvantage, regulatoryBarriers } = campMetrics.advantage;
    
    const avgScore = (ipStrength + technicalMoat + networkEffects + 
                     brandStrength + dataAdvantage + regulatoryBarriers) / 6;
    
    return Math.round(avgScore * 20);
  };

  const calculateMarketScore = () => {
    const { growthRate, productMarketFit, customerRetention, nps } = campMetrics.market;
    
    let score = 0;
    
    // Growth rate score (0-25)
    if (growthRate >= 100) score += 25;
    else if (growthRate >= 50) score += 20;
    else if (growthRate >= 30) score += 15;
    else if (growthRate >= 15) score += 10;
    else score += 5;
    
    // PMF score (0-25)
    score += productMarketFit * 5;
    
    // Retention score (0-25)
    if (customerRetention >= 90) score += 25;
    else if (customerRetention >= 80) score += 20;
    else if (customerRetention >= 70) score += 15;
    else if (customerRetention >= 60) score += 10;
    else score += 5;
    
    // NPS score (0-25)
    if (nps >= 70) score += 25;
    else if (nps >= 50) score += 20;
    else if (nps >= 30) score += 15;
    else if (nps >= 10) score += 10;
    else score += 5;
    
    return Math.round(score);
  };

  const calculatePeopleScore = () => {
    const { teamCompleteness, leadershipExperience, technicalExpertise, cultureFit, recruitingAbility, advisorNetwork } = campMetrics.people;
    
    let score = 0;
    
    // Team completeness (0-30)
    score += (teamCompleteness / 100) * 30;
    
    // Average of other metrics (0-70)
    const avgMetrics = (leadershipExperience + technicalExpertise + cultureFit + 
                       recruitingAbility + advisorNetwork) / 5;
    score += avgMetrics * 14;
    
    return Math.round(score);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#52c41a';
    if (score >= 60) return '#faad14';
    if (score >= 40) return '#fa8c16';
    return '#f5222d';
  };

  const getScoreStatus = (score: number) => {
    if (score >= 80) return { text: 'Excellent', icon: <CheckCircleOutlined /> };
    if (score >= 60) return { text: 'Good', icon: <InfoCircleOutlined /> };
    if (score >= 40) return { text: 'Fair', icon: <WarningOutlined /> };
    return { text: 'Needs Improvement', icon: <WarningOutlined /> };
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return '#f5222d';
      case 'high': return '#fa8c16';
      case 'medium': return '#faad14';
      case 'low': return '#52c41a';
      default: return '#8c8c8c';
    }
  };

  const renderCapitalMetrics = () => (
    <Card 
      title={
        <Space>
          <DollarOutlined style={{ color: '#1890ff' }} />
          <span>Capital Efficiency</span>
          <Tag color={getScoreColor(campMetrics.capital.score)}>
            Score: {campMetrics.capital.score}
          </Tag>
        </Space>
      }
      className={styles.metricsCard}
    >
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Statistic
            title="Monthly Burn Rate"
            value={campMetrics.capital.burnRate}
            prefix="$"
            suffix={
              <Tooltip title="Average monthly cash burn">
                <InfoCircleOutlined />
              </Tooltip>
            }
          />
        </Col>
        <Col span={12}>
          <Statistic
            title="Runway"
            value={campMetrics.capital.runway}
            suffix="months"
            valueStyle={{ color: campMetrics.capital.runway >= 18 ? '#52c41a' : '#f5222d' }}
          />
        </Col>
        <Col span={12}>
          <Statistic
            title="Monthly Revenue"
            value={campMetrics.capital.revenue}
            prefix="$"
          />
        </Col>
        <Col span={12}>
          <Statistic
            title="Revenue Growth"
            value={campMetrics.capital.revenueGrowth}
            prefix={campMetrics.capital.revenueGrowth > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            suffix="%"
            valueStyle={{ color: campMetrics.capital.revenueGrowth > 0 ? '#52c41a' : '#f5222d' }}
          />
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>Gross Margin</span>
            <Progress 
              percent={campMetrics.capital.grossMargin} 
              strokeColor={getScoreColor(campMetrics.capital.grossMargin)}
              format={percent => `${percent}%`}
            />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>Unit Economics</span>
            <Tag color={campMetrics.capital.unitEconomics ? 'success' : 'error'}>
              {campMetrics.capital.unitEconomics ? 'Positive' : 'Negative'}
            </Tag>
          </div>
        </Col>
      </Row>
    </Card>
  );

  const renderAdvantageMetrics = () => (
    <Card 
      title={
        <Space>
          <TrophyOutlined style={{ color: '#722ed1' }} />
          <span>Competitive Advantage</span>
          <Tag color={getScoreColor(campMetrics.advantage.score)}>
            Score: {campMetrics.advantage.score}
          </Tag>
        </Space>
      }
      className={styles.metricsCard}
    >
      <div className={styles.advantageMetrics}>
        <div className={styles.metricRow}>
          <span><SafetyOutlined /> IP Strength</span>
          <Rate value={campMetrics.advantage.ipStrength} disabled allowHalf />
        </div>
        <div className={styles.metricRow}>
          <span><ThunderboltOutlined /> Technical Moat</span>
          <Rate value={campMetrics.advantage.technicalMoat} disabled allowHalf />
        </div>
        <div className={styles.metricRow}>
          <span><GlobalOutlined /> Network Effects</span>
          <Rate value={campMetrics.advantage.networkEffects} disabled allowHalf />
        </div>
        <div className={styles.metricRow}>
          <span><CrownOutlined /> Brand Strength</span>
          <Rate value={campMetrics.advantage.brandStrength} disabled allowHalf />
        </div>
        <div className={styles.metricRow}>
          <span><FundOutlined /> Data Advantage</span>
          <Rate value={campMetrics.advantage.dataAdvantage} disabled allowHalf />
        </div>
        <div className={styles.metricRow}>
          <span><ExperimentOutlined /> Regulatory Barriers</span>
          <Rate value={campMetrics.advantage.regulatoryBarriers} disabled allowHalf />
        </div>
      </div>
    </Card>
  );

  const renderMarketMetrics = () => (
    <Card 
      title={
        <Space>
          <RocketOutlined style={{ color: '#13c2c2' }} />
          <span>Market Position</span>
          <Tag color={getScoreColor(campMetrics.market.score)}>
            Score: {campMetrics.market.score}
          </Tag>
        </Space>
      }
      className={styles.metricsCard}
    >
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Statistic
            title="TAM Capture"
            value={campMetrics.market.tamCapture}
            suffix="%"
            precision={2}
          />
        </Col>
        <Col span={12}>
          <Statistic
            title="Growth Rate"
            value={campMetrics.market.growthRate}
            prefix={<RiseOutlined />}
            suffix="% YoY"
            valueStyle={{ color: '#52c41a' }}
          />
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>Product-Market Fit</span>
            <Rate value={campMetrics.market.productMarketFit} disabled />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>Market Share</span>
            <Progress 
              percent={campMetrics.market.marketShare} 
              strokeColor="#1890ff"
              format={percent => `${percent}%`}
            />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>Customer Retention</span>
            <Progress 
              percent={campMetrics.market.customerRetention} 
              strokeColor={getScoreColor(campMetrics.market.customerRetention)}
            />
          </div>
        </Col>
        <Col span={12}>
          <div className={styles.metricItem}>
            <span>NPS Score</span>
            <Progress 
              percent={campMetrics.market.nps} 
              strokeColor={getScoreColor(campMetrics.market.nps)}
              format={percent => percent}
            />
          </div>
        </Col>
      </Row>
    </Card>
  );

  const renderPeopleMetrics = () => (
    <Card 
      title={
        <Space>
          <TeamOutlined style={{ color: '#fa541c' }} />
          <span>People & Team</span>
          <Tag color={getScoreColor(campMetrics.people.score)}>
            Score: {campMetrics.people.score}
          </Tag>
        </Space>
      }
      className={styles.metricsCard}
    >
      <div className={styles.peopleMetrics}>
        <div className={styles.metricItem}>
          <span>Team Completeness</span>
          <Progress 
            percent={campMetrics.people.teamCompleteness} 
            strokeColor={getScoreColor(campMetrics.people.teamCompleteness)}
          />
        </div>
        <div className={styles.metricRow}>
          <span><UserOutlined /> Leadership Experience</span>
          <Rate value={campMetrics.people.leadershipExperience} disabled />
        </div>
        <div className={styles.metricRow}>
          <span><BulbOutlined /> Technical Expertise</span>
          <Rate value={campMetrics.people.technicalExpertise} disabled />
        </div>
        <div className={styles.metricRow}>
          <span><FireOutlined /> Culture Fit</span>
          <Rate value={campMetrics.people.cultureFit} disabled />
        </div>
        <div className={styles.metricRow}>
          <span><SolutionOutlined /> Recruiting Ability</span>
          <Rate value={campMetrics.people.recruitingAbility} disabled />
        </div>
        <div className={styles.metricRow}>
          <span><TeamOutlined /> Advisor Network</span>
          <Rate value={campMetrics.people.advisorNetwork} disabled />
        </div>
      </div>
    </Card>
  );

  const renderCapabilityGaps = () => (
    <Card 
      title={
        <Space>
          <RadarChartOutlined style={{ color: '#f5222d' }} />
          <span>Capability Gap Analysis</span>
        </Space>
      }
      className={styles.gapAnalysisCard}
    >
      <div className={styles.gapsList}>
        {capabilityGaps.map((gap, index) => (
          <div key={index} className={styles.gapItem}>
            <div className={styles.gapHeader}>
              <span className={styles.gapArea}>{gap.area}</span>
              <Tag color={getPriorityColor(gap.priority)}>
                {gap.priority.toUpperCase()}
              </Tag>
            </div>
            <div className={styles.gapProgress}>
              <span className={styles.gapLabel}>Current vs Target</span>
              <Progress
                percent={(gap.current / gap.target) * 100}
                strokeColor={getPriorityColor(gap.priority)}
                format={() => `${gap.current}/${gap.target}`}
              />
            </div>
            <div className={styles.gapAction}>
              <InfoCircleOutlined /> {gap.action}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );

  const renderOverallAssessment = () => {
    const status = getScoreStatus(overallScore);
    
    return (
      <Card className={styles.overallCard}>
        <div className={styles.overallHeader}>
          <h2>Overall CAMP Assessment</h2>
          <div className={styles.overallScore}>
            <Progress
              type="circle"
              percent={overallScore}
              strokeColor={getScoreColor(overallScore)}
              width={120}
            />
            <div className={styles.scoreStatus}>
              {status.icon}
              <span>{status.text}</span>
            </div>
          </div>
        </div>
        
        <Row gutter={[16, 16]} className={styles.summaryScores}>
          <Col span={6}>
            <div className={styles.summaryItem}>
              <DollarOutlined />
              <span>Capital</span>
              <Progress 
                percent={campMetrics.capital.score} 
                strokeColor={getScoreColor(campMetrics.capital.score)}
                size="small"
              />
            </div>
          </Col>
          <Col span={6}>
            <div className={styles.summaryItem}>
              <TrophyOutlined />
              <span>Advantage</span>
              <Progress 
                percent={campMetrics.advantage.score} 
                strokeColor={getScoreColor(campMetrics.advantage.score)}
                size="small"
              />
            </div>
          </Col>
          <Col span={6}>
            <div className={styles.summaryItem}>
              <RocketOutlined />
              <span>Market</span>
              <Progress 
                percent={campMetrics.market.score} 
                strokeColor={getScoreColor(campMetrics.market.score)}
                size="small"
              />
            </div>
          </Col>
          <Col span={6}>
            <div className={styles.summaryItem}>
              <TeamOutlined />
              <span>People</span>
              <Progress 
                percent={campMetrics.people.score} 
                strokeColor={getScoreColor(campMetrics.people.score)}
                size="small"
              />
            </div>
          </Col>
        </Row>

        {overallScore < 60 && (
          <Alert
            message="Action Required"
            description="Your overall CAMP score indicates significant areas for improvement. Focus on the capability gaps identified below."
            type="warning"
            showIcon
            className={styles.alert}
          />
        )}
      </Card>
    );
  };

  return (
    <div className={styles.internalAudit}>
      {renderOverallAssessment()}
      
      <Row gutter={[24, 24]}>
        <Col span={12}>
          {renderCapitalMetrics()}
        </Col>
        <Col span={12}>
          {renderAdvantageMetrics()}
        </Col>
        <Col span={12}>
          {renderMarketMetrics()}
        </Col>
        <Col span={12}>
          {renderPeopleMetrics()}
        </Col>
      </Row>

      {renderCapabilityGaps()}

      <div className={styles.actions}>
        <Space>
          <Button 
            type="primary" 
            icon={<CheckCircleOutlined />}
            onClick={saveData}
            loading={isCalculating}
          >
            Save Assessment
          </Button>
          <Button 
            icon={<RadarChartOutlined />}
            onClick={calculateScores}
            loading={isCalculating}
          >
            Recalculate Scores
          </Button>
          <Button 
            type="primary"
            onClick={() => {
              // Check if assessment is complete
              const hasScores = campMetrics.capital.score > 0 && campMetrics.advantage.score > 0 && campMetrics.market.score > 0 && campMetrics.people.score > 0;
              if (hasScores && capabilityGaps.length > 0) {
                saveData();
                // Dispatch phase completion event
                window.dispatchEvent(new CustomEvent('deepDivePhaseComplete', { 
                  detail: { phaseId: 'phase1' } 
                }));
                alert('Phase 1 completed! Phase 2 is now unlocked.');
                // Navigate to Phase 2
                setTimeout(() => navigate('/deep-dive/phase2'), 1000);
              } else {
                alert('Please complete all assessments and identify capability gaps before marking this phase as complete.');
              }
            }}
            disabled={campMetrics.capital.score === 0 || campMetrics.advantage.score === 0 || campMetrics.market.score === 0 || campMetrics.people.score === 0 || capabilityGaps.length === 0}
          >
            Complete Phase 1
          </Button>
        </Space>
      </div>
    </div>
  );
};

export default InternalAudit;