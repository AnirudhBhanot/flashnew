import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon, Button } from '../design-system/components';
import { RadarChart, ScoreBarChart } from './charts';
import styles from './DeepDiveAnalysis.module.scss';

interface DeepDiveAnalysisProps {
  scores: {
    capital: number;
    advantage: number;
    market: number;
    people: number;
  };
  assessmentData: any;
  insights?: any;
}

interface PillarBreakdown {
  score: number;
  subScores: { name: string; value: number; description: string }[];
  strengths: string[];
  weaknesses: string[];
  benchmarks: { metric: string; yourValue: any; industryAvg: any; topPerformers: any }[];
  recommendations: string[];
}

export const DeepDiveAnalysis: React.FC<DeepDiveAnalysisProps> = ({
  scores,
  assessmentData,
  insights
}) => {
  const [selectedPillar, setSelectedPillar] = useState<string | null>(null);
  const [expandedMetrics, setExpandedMetrics] = useState<string[]>([]);

  const toggleMetric = (metric: string) => {
    setExpandedMetrics(prev => 
      prev.includes(metric) 
        ? prev.filter(m => m !== metric)
        : [...prev, metric]
    );
  };

  // Generate detailed breakdowns for each pillar
  const getCapitalBreakdown = (): PillarBreakdown => {
    const data = assessmentData.capital || {};
    const fundingScore = Math.min(1, (data.totalFundingRaised || 0) / 5000000);
    const runwayScore = Math.min(1, (data.runwayMonths || 0) / 18);
    const revenueScore = Math.min(1, (data.annualRevenueRunRate || 0) / 1000000);
    const burnScore = Math.max(0, 1 - ((data.monthlyBurnRate || 100000) / 500000));
    const marginScore = (data.grossMargin || 0) / 100;

    return {
      score: scores.capital,
      subScores: [
        { name: 'Funding Health', value: fundingScore, description: 'Total capital raised vs. stage expectations' },
        { name: 'Runway Duration', value: runwayScore, description: 'Months of operation at current burn rate' },
        { name: 'Revenue Growth', value: revenueScore, description: 'Annual recurring revenue trajectory' },
        { name: 'Burn Efficiency', value: burnScore, description: 'Capital efficiency and spending discipline' },
        { name: 'Unit Economics', value: marginScore, description: 'Gross margins and profitability potential' }
      ],
      strengths: [
        runwayScore > 0.7 ? 'Strong runway provides flexibility' : null,
        revenueScore > 0.5 ? 'Solid revenue traction' : null,
        marginScore > 0.6 ? 'Healthy gross margins' : null
      ].filter(Boolean) as string[],
      weaknesses: [
        runwayScore < 0.5 ? 'Limited runway requires near-term funding' : null,
        burnScore < 0.5 ? 'High burn rate relative to progress' : null,
        marginScore < 0.4 ? 'Low margins may limit growth' : null
      ].filter(Boolean) as string[],
      benchmarks: [
        { 
          metric: 'Monthly Burn', 
          yourValue: `$${(data.monthlyBurnRate || 0).toLocaleString()}`,
          industryAvg: '$150,000',
          topPerformers: '$100,000'
        },
        {
          metric: 'Runway',
          yourValue: `${data.runwayMonths || 0} months`,
          industryAvg: '12 months',
          topPerformers: '18+ months'
        },
        {
          metric: 'ARR',
          yourValue: `$${(data.annualRevenueRunRate || 0).toLocaleString()}`,
          industryAvg: '$500,000',
          topPerformers: '$2M+'
        }
      ],
      recommendations: [
        runwayScore < 0.7 ? 'Extend runway by optimizing burn rate or raising capital' : null,
        revenueScore < 0.5 ? 'Focus on revenue growth through sales acceleration' : null,
        marginScore < 0.5 ? 'Improve unit economics before scaling' : null
      ].filter(Boolean) as string[]
    };
  };

  const getAdvantageBreakdown = (): PillarBreakdown => {
    const data = assessmentData.advantage || {};
    const moatScore = (data.moatStrength || 5) / 10;
    const patentScore = data.hasPatents ? Math.min(1, (data.patentCount || 0) / 5) : 0;
    const differentiationScore = (data.advantages?.length || 0) / 5;
    const uniquenessScore = data.uniqueAdvantage ? 0.8 : 0.2;

    return {
      score: scores.advantage,
      subScores: [
        { name: 'Competitive Moat', value: moatScore, description: 'Barriers to entry and defensibility' },
        { name: 'IP Protection', value: patentScore, description: 'Patents and intellectual property' },
        { name: 'Differentiation', value: differentiationScore, description: 'Unique value propositions' },
        { name: 'Market Position', value: uniquenessScore, description: 'Distinctive market positioning' }
      ],
      strengths: [
        moatScore > 0.7 ? 'Strong competitive barriers' : null,
        patentScore > 0.5 ? 'Protected intellectual property' : null,
        differentiationScore > 0.6 ? 'Multiple competitive advantages' : null
      ].filter(Boolean) as string[],
      weaknesses: [
        moatScore < 0.5 ? 'Weak competitive moat' : null,
        patentScore === 0 ? 'No IP protection' : null,
        differentiationScore < 0.4 ? 'Limited differentiation' : null
      ].filter(Boolean) as string[],
      benchmarks: [
        {
          metric: 'Moat Strength',
          yourValue: `${moatScore * 10}/10`,
          industryAvg: '6/10',
          topPerformers: '8+/10'
        },
        {
          metric: 'Key Advantages',
          yourValue: data.advantages?.length || 0,
          industryAvg: '3',
          topPerformers: '5+'
        }
      ],
      recommendations: [
        moatScore < 0.7 ? 'Strengthen competitive barriers through network effects or switching costs' : null,
        !data.hasPatents ? 'Consider filing patents for core innovations' : null,
        differentiationScore < 0.6 ? 'Develop additional unique value propositions' : null
      ].filter(Boolean) as string[]
    };
  };

  const getMarketBreakdown = (): PillarBreakdown => {
    const data = assessmentData.market || {};
    const tamScore = Math.min(1, (data.marketSize || 0) / 10000000000);
    const growthScore = Math.min(1, (data.marketGrowthRate || 0) / 30);
    const competitionScore = Math.max(0, 1 - ((data.competitionLevel || 5) / 10));
    const timingScore = (data.marketTiming || 5) / 10;
    const strategyScore = data.goToMarketStrategy ? 0.8 : 0.2;

    return {
      score: scores.market,
      subScores: [
        { name: 'Market Size', value: tamScore, description: 'Total addressable market potential' },
        { name: 'Growth Rate', value: growthScore, description: 'Market expansion velocity' },
        { name: 'Competition', value: competitionScore, description: 'Competitive landscape favorability' },
        { name: 'Market Timing', value: timingScore, description: 'Entry timing and market readiness' },
        { name: 'GTM Strategy', value: strategyScore, description: 'Go-to-market approach clarity' }
      ],
      strengths: [
        tamScore > 0.7 ? 'Large addressable market' : null,
        growthScore > 0.6 ? 'Fast-growing market' : null,
        timingScore > 0.7 ? 'Excellent market timing' : null
      ].filter(Boolean) as string[],
      weaknesses: [
        tamScore < 0.5 ? 'Limited market size' : null,
        competitionScore < 0.4 ? 'Highly competitive market' : null,
        strategyScore < 0.5 ? 'Unclear go-to-market strategy' : null
      ].filter(Boolean) as string[],
      benchmarks: [
        {
          metric: 'TAM',
          yourValue: `$${((data.marketSize || 0) / 1000000000).toFixed(1)}B`,
          industryAvg: '$5B',
          topPerformers: '$10B+'
        },
        {
          metric: 'Growth Rate',
          yourValue: `${data.marketGrowthRate || 0}%`,
          industryAvg: '15%',
          topPerformers: '25%+'
        },
        {
          metric: 'CAC',
          yourValue: `$${(data.customerAcquisitionCost || 0).toLocaleString()}`,
          industryAvg: '$500',
          topPerformers: '<$200'
        }
      ],
      recommendations: [
        tamScore < 0.6 ? 'Expand market definition or target adjacent segments' : null,
        competitionScore < 0.5 ? 'Develop stronger differentiation against competitors' : null,
        strategyScore < 0.7 ? 'Refine and test go-to-market strategy' : null
      ].filter(Boolean) as string[]
    };
  };

  const getPeopleBreakdown = (): PillarBreakdown => {
    const data = assessmentData.people || {};
    const teamSizeScore = Math.min(1, (data.teamSize || 0) / 20);
    const experienceScore = (data.industryExperience || 5) / 10;
    const previousSuccessScore = data.previousStartups ? 
      Math.min(1, (data.previousExits || 0) / 2) : 0.2;
    const leadershipScore = (data.keyRoles?.length || 0) / 5;
    const cultureScore = (data.teamCulture || 5) / 10;

    return {
      score: scores.people,
      subScores: [
        { name: 'Team Size', value: teamSizeScore, description: 'Team scaling and capacity' },
        { name: 'Experience', value: experienceScore, description: 'Industry and domain expertise' },
        { name: 'Track Record', value: previousSuccessScore, description: 'Previous startup success' },
        { name: 'Leadership', value: leadershipScore, description: 'Key roles and leadership coverage' },
        { name: 'Culture', value: cultureScore, description: 'Team cohesion and culture strength' }
      ],
      strengths: [
        experienceScore > 0.7 ? 'Deep industry experience' : null,
        previousSuccessScore > 0.5 ? 'Proven entrepreneurial track record' : null,
        leadershipScore > 0.6 ? 'Strong leadership team' : null
      ].filter(Boolean) as string[],
      weaknesses: [
        teamSizeScore < 0.3 ? 'Small team may limit execution' : null,
        experienceScore < 0.5 ? 'Limited industry experience' : null,
        leadershipScore < 0.4 ? 'Key leadership gaps' : null
      ].filter(Boolean) as string[],
      benchmarks: [
        {
          metric: 'Team Size',
          yourValue: data.teamSize || 0,
          industryAvg: '12',
          topPerformers: '20+'
        },
        {
          metric: 'Technical Founders',
          yourValue: data.technicalFounders || 0,
          industryAvg: '1',
          topPerformers: '2+'
        },
        {
          metric: 'Advisors',
          yourValue: data.advisorsCount || 0,
          industryAvg: '3',
          topPerformers: '5+'
        }
      ],
      recommendations: [
        teamSizeScore < 0.5 ? 'Scale team strategically in critical areas' : null,
        experienceScore < 0.6 ? 'Recruit industry veterans or advisors' : null,
        leadershipScore < 0.6 ? 'Fill key leadership positions' : null
      ].filter(Boolean) as string[]
    };
  };

  const pillarData = {
    capital: getCapitalBreakdown(),
    advantage: getAdvantageBreakdown(),
    market: getMarketBreakdown(),
    people: getPeopleBreakdown()
  };

  const pillars = [
    { id: 'capital', name: 'Capital', icon: 'building.2', color: '#007AFF' },
    { id: 'advantage', name: 'Advantage', icon: 'sparkles', color: '#FF9500' },
    { id: 'market', name: 'Market', icon: 'chart.line.uptrend', color: '#34C759' },
    { id: 'people', name: 'People', icon: 'brain', color: '#AF52DE' }
  ];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>
          <Icon name="chart.bar.xaxis" size={24} />
          Deep Dive Analysis
        </h3>
        <p className={styles.subtitle}>
          Click on any pillar below for detailed metrics and benchmarks
        </p>
      </div>

      {/* Pillar Selection */}
      <div className={styles.pillarGrid}>
        {pillars.map(pillar => (
          <motion.button
            key={pillar.id}
            className={`${styles.pillarCard} ${selectedPillar === pillar.id ? styles.selected : ''}`}
            onClick={() => setSelectedPillar(selectedPillar === pillar.id ? null : pillar.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div 
              className={styles.pillarIcon}
              style={{ backgroundColor: `${pillar.color}20`, color: pillar.color }}
            >
              <Icon name={pillar.icon} size={28} />
            </div>
            <h4 className={styles.pillarName}>{pillar.name}</h4>
            <div className={styles.pillarScore}>
              <span className={styles.scoreValue}>
                {Math.round(scores[pillar.id as keyof typeof scores] * 100)}%
              </span>
              <div className={styles.scoreBar}>
                <motion.div 
                  className={styles.scoreBarFill}
                  initial={{ width: 0 }}
                  animate={{ width: `${scores[pillar.id as keyof typeof scores] * 100}%` }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  style={{ backgroundColor: pillar.color }}
                />
              </div>
            </div>
          </motion.button>
        ))}
      </div>

      {/* Detailed Analysis */}
      <AnimatePresence>
        {selectedPillar && (
          <motion.div
            className={styles.detailSection}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className={styles.detailHeader}>
              <h3 className={styles.detailTitle}>
                {pillars.find(p => p.id === selectedPillar)?.name} Analysis
              </h3>
              <Button
                variant="text"
                size="small"
                onClick={() => setSelectedPillar(null)}
                icon={<Icon name="xmark" />}
              >
                Close
              </Button>
            </div>

            {/* Sub-scores */}
            <div className={styles.subScoresSection}>
              <h4 className={styles.sectionTitle}>Component Scores</h4>
              <div className={styles.subScores}>
                {pillarData[selectedPillar as keyof typeof pillarData].subScores.map((subScore, index) => (
                  <motion.div
                    key={subScore.name}
                    className={styles.subScore}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => toggleMetric(subScore.name)}
                  >
                    <div className={styles.subScoreHeader}>
                      <span className={styles.subScoreName}>{subScore.name}</span>
                      <span className={styles.subScoreValue}>
                        {Math.round(subScore.value * 100)}%
                      </span>
                    </div>
                    <div className={styles.subScoreBar}>
                      <motion.div
                        className={styles.subScoreBarFill}
                        initial={{ width: 0 }}
                        animate={{ width: `${subScore.value * 100}%` }}
                        transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
                      />
                    </div>
                    {expandedMetrics.includes(subScore.name) && (
                      <motion.p
                        className={styles.subScoreDescription}
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                      >
                        {subScore.description}
                      </motion.p>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Strengths & Weaknesses */}
            <div className={styles.analysisGrid}>
              {pillarData[selectedPillar as keyof typeof pillarData].strengths.length > 0 && (
                <div className={styles.analysisSection}>
                  <h4 className={styles.sectionTitle}>
                    <Icon name="checkmark.circle" size={20} />
                    Strengths
                  </h4>
                  <ul className={styles.analysisList}>
                    {pillarData[selectedPillar as keyof typeof pillarData].strengths.map((strength, index) => (
                      <motion.li
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        {strength}
                      </motion.li>
                    ))}
                  </ul>
                </div>
              )}

              {pillarData[selectedPillar as keyof typeof pillarData].weaknesses.length > 0 && (
                <div className={styles.analysisSection}>
                  <h4 className={styles.sectionTitle}>
                    <Icon name="exclamationmark.triangle" size={20} />
                    Areas for Improvement
                  </h4>
                  <ul className={styles.analysisList}>
                    {pillarData[selectedPillar as keyof typeof pillarData].weaknesses.map((weakness, index) => (
                      <motion.li
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        {weakness}
                      </motion.li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Benchmarks */}
            <div className={styles.benchmarkSection}>
              <h4 className={styles.sectionTitle}>Industry Benchmarks</h4>
              <div className={styles.benchmarkTable}>
                <div className={styles.benchmarkHeader}>
                  <span>Metric</span>
                  <span>Your Value</span>
                  <span>Industry Avg</span>
                  <span>Top 10%</span>
                </div>
                {pillarData[selectedPillar as keyof typeof pillarData].benchmarks.map((benchmark, index) => (
                  <motion.div
                    key={benchmark.metric}
                    className={styles.benchmarkRow}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <span className={styles.benchmarkMetric}>{benchmark.metric}</span>
                    <span className={styles.benchmarkValue}>{benchmark.yourValue}</span>
                    <span className={styles.benchmarkAvg}>{benchmark.industryAvg}</span>
                    <span className={styles.benchmarkTop}>{benchmark.topPerformers}</span>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            {pillarData[selectedPillar as keyof typeof pillarData].recommendations.length > 0 && (
              <div className={styles.recommendationsSection}>
                <h4 className={styles.sectionTitle}>
                  <Icon name="lightbulb" size={20} />
                  Recommendations
                </h4>
                <div className={styles.recommendationsList}>
                  {pillarData[selectedPillar as keyof typeof pillarData].recommendations.map((rec, index) => (
                    <motion.div
                      key={index}
                      className={styles.recommendationItem}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Icon name="arrow.right.circle" size={16} />
                      <span>{rec}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};