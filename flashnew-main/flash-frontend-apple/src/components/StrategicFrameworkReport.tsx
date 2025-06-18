import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useAssessmentStore from '../store/assessmentStore';
import styles from './StrategicFrameworkReport.module.scss';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

interface SWOTAnalysis {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

interface BCGPosition {
  quadrant: string;
  marketShare: number;
  marketGrowth: number;
  relativeShare: number;
  interpretation: string;
  timeToTransition: string;
}

interface PortersForce {
  name: string;
  level: 'Low' | 'Medium' | 'High';
  score: number;
  drivers: string[];
  implications: string;
}

interface AnsoffStrategy {
  currentPosition: string;
  recommendedMove: string;
  riskLevel: string;
  implementation: string[];
  expectedROI: string;
}

interface FrameworkAnalysis {
  framework_id: string;
  framework_name: string;
  analysis: any;
  visualData?: any;
}

export const StrategicFrameworkReport: React.FC = () => {
  const [analyses, setAnalyses] = useState<FrameworkAnalysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFramework, setSelectedFramework] = useState<string>('swot');
  
  const assessmentData = useAssessmentStore(state => state.data);
  const results = useAssessmentStore(state => state.results);

  useEffect(() => {
    if (assessmentData) {
      performDeepAnalysis();
    }
  }, [assessmentData]);

  const performDeepAnalysis = async () => {
    setIsLoading(true);
    
    // Transform data for analysis
    const companyData = {
      name: assessmentData.companyInfo?.companyName || 'Your Company',
      stage: assessmentData.capital?.fundingStage || 'seed',
      sector: assessmentData.market?.sector || 'technology',
      
      // Financial metrics
      revenue: Number(assessmentData.capital?.annualRevenue) || 0,
      burn: Number(assessmentData.capital?.monthlyBurn) || 0,
      runway: Number(assessmentData.capital?.runwayMonths) || 0,
      totalRaised: Number(assessmentData.capital?.totalRaised) || 0,
      
      // Market metrics
      tam: Number(assessmentData.market?.tam) || 0,
      sam: Number(assessmentData.market?.sam) || 0,
      som: Number(assessmentData.market?.som) || 0,
      marketGrowth: Number(assessmentData.market?.marketGrowthRate) || 15,
      competitorCount: Number(assessmentData.market?.competitorCount) || 10,
      customerConcentration: Number(assessmentData.market?.customerConcentration) || 0,
      marketShare: assessmentData.market?.som && assessmentData.market?.sam ? 
        (Number(assessmentData.market.som) / Number(assessmentData.market.sam) * 100) : 0.5,
      
      // Product metrics
      users: Number(assessmentData.advantage?.monthlyActiveUsers) || 0,
      churn: Number(assessmentData.advantage?.churnRate) || 5,
      nps: Number(assessmentData.advantage?.npsScore) || 0,
      productStage: assessmentData.advantage?.productStage || 'mvp',
      
      // Team metrics
      teamSize: Number(assessmentData.people?.fullTimeEmployees) || 1,
      foundersExperience: Number(assessmentData.people?.industryExperience) || 0,
      keyHires: assessmentData.people?.keyHires || [],
    };

    // Perform comprehensive analysis
    const swotAnalysis = generateDetailedSWOT(companyData, assessmentData);
    const bcgAnalysis = generateDetailedBCG(companyData);
    const portersAnalysis = generateDetailedPorters(companyData, assessmentData);
    const ansoffAnalysis = generateDetailedAnsoff(companyData, assessmentData);

    setAnalyses([
      { framework_id: 'swot', framework_name: 'SWOT Analysis', analysis: swotAnalysis },
      { framework_id: 'bcg', framework_name: 'BCG Matrix', analysis: bcgAnalysis },
      { framework_id: 'porters', framework_name: "Porter's Five Forces", analysis: portersAnalysis },
      { framework_id: 'ansoff', framework_name: 'Ansoff Matrix', analysis: ansoffAnalysis }
    ]);
    
    setIsLoading(false);
  };

  const generateDetailedSWOT = (company: any, rawData: any): SWOTAnalysis => {
    const swot: SWOTAnalysis = {
      strengths: [],
      weaknesses: [],
      opportunities: [],
      threats: []
    };

    // STRENGTHS - Specific to this company
    if (company.runway > 18) {
      swot.strengths.push(`Strong financial position with ${company.runway} months runway (industry avg: 12-18 months)`);
    }
    if (rawData.advantage?.proprietaryTech) {
      swot.strengths.push(`Proprietary technology creating barriers to entry (${rawData.advantage.patentsFiled || 0} patents filed)`);
    }
    if (company.nps > 50) {
      swot.strengths.push(`Exceptional customer satisfaction with NPS of ${company.nps} (world-class is >50)`);
    }
    if (company.churn < 3) {
      swot.strengths.push(`Best-in-class retention with ${company.churn}% monthly churn (SaaS benchmark: 3-5%)`);
    }
    if (company.foundersExperience > 10) {
      swot.strengths.push(`Deep domain expertise: ${company.foundersExperience} years industry experience`);
    }
    if (rawData.capital?.primaryInvestor === 'tier_1') {
      swot.strengths.push(`Tier 1 VC backing provides credibility and network access`);
    }

    // WEAKNESSES - Specific pain points
    if (company.runway < 6) {
      swot.weaknesses.push(`Critical: Only ${company.runway} months runway - immediate fundraising required`);
    }
    if (company.burn > 0 && company.revenue >= 0) {
      const monthlyRevenue = company.revenue / 12;
      if (company.burn > monthlyRevenue * 2) {
        const excessPercent = monthlyRevenue > 0 ? ((company.burn - monthlyRevenue) / company.burn * 100).toFixed(0) : 100;
        swot.weaknesses.push(`Burn rate ($${(company.burn/1000).toFixed(0)}k/mo) exceeds revenue by ${excessPercent}%`);
      }
    }
    if (company.marketShare < 1) {
      swot.weaknesses.push(`Minimal market presence at ${company.marketShare || '<1'}% share vs. ${company.competitorCount} competitors`);
    }
    if (company.teamSize < 5 && company.stage !== 'pre-seed') {
      swot.weaknesses.push(`Under-resourced with only ${company.teamSize} FTEs for ${company.stage} stage`);
    }
    if (!rawData.advantage?.networkEffects && company.sector === 'marketplace') {
      swot.weaknesses.push(`No network effects in a marketplace business - critical competitive disadvantage`);
    }

    // OPPORTUNITIES - Market-specific
    if (company.marketGrowth > 20) {
      swot.opportunities.push(`Explosive market growth at ${company.marketGrowth}% CAGR (vs. GDP growth of 2-3%)`);
    }
    if (company.tam > 10000000000) {
      swot.opportunities.push(`Massive TAM of $${(company.tam/1000000000).toFixed(1)}B allows for multiple winners`);
    }
    if (company.som > 0 && company.sam > 0 && company.som < company.sam * 0.01) {
      const multiplier = (company.sam * 0.01 / company.som).toFixed(0);
      swot.opportunities.push(`Capturing just 1% of SAM would ${multiplier}x current market share`);
    }
    if (rawData.market?.regulatoryChanges) {
      swot.opportunities.push(`Recent regulatory changes in ${company.sector} favor new entrants`);
    }

    // THREATS - Real risks
    if (company.competitorCount > 20) {
      swot.threats.push(`Highly fragmented market with ${company.competitorCount}+ competitors`);
    }
    if (company.customerConcentration > 30) {
      swot.threats.push(`Revenue concentration risk: ${company.customerConcentration}% from top customers`);
    } else if (rawData.market?.customerConcentration > 30) {
      swot.threats.push(`Customer concentration risk: ${rawData.market.customerConcentration}% revenue from key accounts`);
    }
    if (company.stage === 'seed' && company.productStage === 'concept') {
      swot.threats.push(`Product-market fit risk: Still in concept stage after seed funding`);
    }
    if (rawData.market?.substituteThreat === 'high') {
      swot.threats.push(`High substitution threat from ${rawData.market.primarySubstitute || 'alternatives'}`);
    }

    // Ensure each section has at least one item
    if (swot.strengths.length === 0) {
      swot.strengths.push(`${company.stage} stage startup with ${company.teamSize} team members`);
    }
    if (swot.weaknesses.length === 0) {
      swot.weaknesses.push(`Limited resources typical of ${company.stage} stage`);
    }
    if (swot.opportunities.length === 0) {
      swot.opportunities.push(`Operating in ${company.sector} sector with emerging opportunities`);
    }
    if (swot.threats.length === 0) {
      swot.threats.push(`Standard market risks for ${company.stage} stage companies`);
    }

    return swot;
  };

  const generateDetailedBCG = (company: any): BCGPosition => {
    const marketShare = company.som && company.sam ? (company.som / company.sam * 100) : 0.5;
    const relativeShare = marketShare / (100 / Math.max(company.competitorCount, 1));
    
    let quadrant = '';
    let interpretation = '';
    let timeToTransition = '';

    if (company.marketGrowth > 20 && relativeShare > 1) {
      quadrant = 'Star';
      interpretation = `Strong position in high-growth market. Current ${marketShare.toFixed(1)}% share with ${relativeShare.toFixed(1)}x competitor average.`;
      timeToTransition = '2-3 years to Cash Cow as market matures';
    } else if (company.marketGrowth > 20 && relativeShare <= 1) {
      quadrant = 'Question Mark';
      interpretation = `Weak position (${marketShare.toFixed(1)}% share) in attractive ${company.marketGrowth}% growth market. Critical inflection point.`;
      timeToTransition = '12-18 months to prove viability or exit';
    } else if (company.marketGrowth <= 20 && relativeShare > 1) {
      quadrant = 'Cash Cow';
      interpretation = `Dominant in mature market. Focus on profitability and cash generation.`;
      timeToTransition = 'Maintain position for 3-5 years';
    } else {
      quadrant = 'Dog';
      interpretation = `Weak position in low-growth market. Consider pivot or exit strategies.`;
      timeToTransition = '6-12 months to decide on transformation';
    }

    return {
      quadrant,
      marketShare,
      marketGrowth: company.marketGrowth,
      relativeShare,
      interpretation,
      timeToTransition
    };
  };

  const generateDetailedPorters = (company: any, rawData: any): PortersForce[] => {
    const forces: PortersForce[] = [];

    // Threat of New Entrants
    const entrantScore = calculateEntrantThreat(company, rawData);
    forces.push({
      name: 'Threat of New Entrants',
      level: entrantScore < 0.3 ? 'Low' : entrantScore < 0.6 ? 'Medium' : 'High',
      score: entrantScore,
      drivers: [
        company.totalRaised > 5000000 ? `Capital requirements high ($${(company.totalRaised/1000000).toFixed(1)}M raised)` : 'Low capital barriers',
        rawData.advantage?.proprietaryTech ? 'Proprietary technology barriers' : 'No technical moats',
        rawData.advantage?.networkEffects ? 'Network effects protection' : 'No network effects',
        rawData.advantage?.regulatoryBarriers ? 'Regulatory barriers exist' : 'Minimal regulatory barriers'
      ].filter(Boolean),
      implications: entrantScore > 0.6 ? 
        'High threat requires rapid market share capture and moat building' :
        'Protected position allows focus on execution over defense'
    });

    // Bargaining Power of Suppliers
    forces.push({
      name: 'Bargaining Power of Suppliers',
      level: 'Medium',
      score: 0.5,
      drivers: [
        'Cloud infrastructure commoditized (AWS/GCP/Azure)',
        rawData.advantage?.customHardware ? 'Custom hardware dependencies' : 'Standard components',
        'Talent market competitive for engineers'
      ],
      implications: 'Manage supplier risk through multi-vendor strategies'
    });

    // Bargaining Power of Buyers
    const buyerPower = calculateBuyerPower(company, rawData);
    forces.push({
      name: 'Bargaining Power of Buyers',
      level: buyerPower < 0.3 ? 'Low' : buyerPower < 0.6 ? 'Medium' : 'High',
      score: buyerPower,
      drivers: [
        company.customerConcentration > 20 ? `High concentration: ${company.customerConcentration}% from top clients` : 'Diversified customer base',
        rawData.market?.contractLength === 'monthly' ? 'Short contracts increase churn risk' : 'Long-term contracts',
        rawData.advantage?.switchingCosts === 'high' ? 'High switching costs lock in customers' : 'Low switching barriers'
      ],
      implications: buyerPower > 0.6 ? 
        'Reduce dependency through customer diversification and switching costs' :
        'Strong position allows premium pricing'
    });

    // Threat of Substitutes
    forces.push({
      name: 'Threat of Substitutes',
      level: rawData.market?.substituteThreat || 'Medium',
      score: rawData.market?.substituteThreat === 'high' ? 0.8 : 0.5,
      drivers: [
        'In-house development as alternative',
        'Open source solutions available',
        rawData.market?.primarySubstitute || 'Manual processes'
      ],
      implications: 'Differentiate through unique value not available in substitutes'
    });

    // Competitive Rivalry
    const rivalryScore = company.competitorCount > 20 ? 0.9 : company.competitorCount > 10 ? 0.7 : 0.4;
    forces.push({
      name: 'Competitive Rivalry',
      level: rivalryScore > 0.7 ? 'High' : rivalryScore > 0.4 ? 'Medium' : 'Low',
      score: rivalryScore,
      drivers: [
        `${company.competitorCount} direct competitors`,
        company.marketGrowth > 20 ? 'High growth reduces rivalry' : 'Slow growth intensifies competition',
        'Low differentiation increases price competition'
      ],
      implications: rivalryScore > 0.7 ? 
        'Differentiation critical in crowded market' :
        'Room for multiple winners'
    });

    return forces;
  };

  const generateDetailedAnsoff = (company: any, rawData: any): AnsoffStrategy => {
    let currentPosition = '';
    let recommendedMove = '';
    let riskLevel = '';
    let implementation: string[] = [];
    let expectedROI = '';

    // Determine current position
    if (company.marketShare < 5 && company.productStage === 'growth') {
      currentPosition = 'Market Penetration';
      recommendedMove = 'Deepen Market Penetration';
      riskLevel = 'Low';
      implementation = [
        `Increase marketing spend from ${rawData.capital?.marketingSpend || 15}% to 25% of revenue`,
        `Launch referral program targeting ${company.users} existing users`,
        `Optimize pricing to capture additional ${((company.sam - company.som) / company.sam * 10).toFixed(0)}% of SAM`,
        `Focus on reducing CAC from $${rawData.market?.customerAcquisitionCost || 500} to sub-$300`
      ];
      expectedROI = '3-5x revenue growth in 18 months';
    } else if (company.marketShare > 5 && company.stage === 'series-a') {
      currentPosition = 'Market Development';
      recommendedMove = 'Expand to Adjacent Markets';
      riskLevel = 'Medium';
      implementation = [
        `Target ${rawData.market?.secondaryMarket || 'adjacent vertical'} with $${(company.tam * 0.2 / 1000000000).toFixed(1)}B TAM`,
        `Leverage existing tech for new use cases`,
        `Pilot with 10 customers in new segment`,
        `Allocate 30% of resources to new market`
      ];
      expectedROI = '40% revenue uplift in 24 months';
    } else {
      // Default strategy for other cases
      currentPosition = 'Market Penetration';
      recommendedMove = 'Focus on Core Market';
      riskLevel = 'Low';
      implementation = [
        `Strengthen product-market fit with existing customers`,
        `Improve unit economics before expansion`,
        `Build repeatable sales process`,
        `Achieve profitability in core market`
      ];
      expectedROI = '2x revenue growth in 12 months';
    }

    return {
      currentPosition,
      recommendedMove,
      riskLevel,
      implementation,
      expectedROI
    };
  };

  const calculateEntrantThreat = (company: any, rawData: any): number => {
    let score = 0.5;
    if (company.totalRaised < 1000000) score += 0.2;
    if (!rawData.advantage?.proprietaryTech) score += 0.15;
    if (!rawData.advantage?.networkEffects) score += 0.15;
    if (company.marketGrowth > 25) score += 0.1;
    return Math.min(score, 1);
  };

  const calculateBuyerPower = (company: any, rawData: any): number => {
    let score = 0.3;
    if (company.customerConcentration > 30) score += 0.3;
    if (rawData.market?.contractLength === 'monthly') score += 0.2;
    if (rawData.advantage?.switchingCosts !== 'high') score += 0.2;
    return Math.min(score, 1);
  };

  const renderSWOT = (swot: SWOTAnalysis) => (
    <div className={styles.swotGrid}>
      <div className={styles.swotQuadrant}>
        <h4 className={styles.swotHeader}>Strengths</h4>
        <ul className={styles.swotList}>
          {swot.strengths.map((item, i) => (
            <li key={i} className={styles.swotItem}>
              <span className={styles.swotBullet}>•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
      
      <div className={styles.swotQuadrant}>
        <h4 className={styles.swotHeader}>Weaknesses</h4>
        <ul className={styles.swotList}>
          {swot.weaknesses.map((item, i) => (
            <li key={i} className={styles.swotItem}>
              <span className={styles.swotBullet}>•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
      
      <div className={styles.swotQuadrant}>
        <h4 className={styles.swotHeader}>Opportunities</h4>
        <ul className={styles.swotList}>
          {swot.opportunities.map((item, i) => (
            <li key={i} className={styles.swotItem}>
              <span className={styles.swotBullet}>•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
      
      <div className={styles.swotQuadrant}>
        <h4 className={styles.swotHeader}>Threats</h4>
        <ul className={styles.swotList}>
          {swot.threats.map((item, i) => (
            <li key={i} className={styles.swotItem}>
              <span className={styles.swotBullet}>•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );

  const renderBCG = (bcg: BCGPosition) => (
    <div className={styles.bcgAnalysis}>
      <div className={styles.bcgMatrix}>
        <div className={styles.bcgGrid}>
          <div className={`${styles.bcgQuadrant} ${bcg.quadrant === 'Star' ? styles.active : ''}`}>
            <h5>Star</h5>
            <p>High Growth, High Share</p>
          </div>
          <div className={`${styles.bcgQuadrant} ${bcg.quadrant === 'Question Mark' ? styles.active : ''}`}>
            <h5>Question Mark</h5>
            <p>High Growth, Low Share</p>
          </div>
          <div className={`${styles.bcgQuadrant} ${bcg.quadrant === 'Cash Cow' ? styles.active : ''}`}>
            <h5>Cash Cow</h5>
            <p>Low Growth, High Share</p>
          </div>
          <div className={`${styles.bcgQuadrant} ${bcg.quadrant === 'Dog' ? styles.active : ''}`}>
            <h5>Dog</h5>
            <p>Low Growth, Low Share</p>
          </div>
        </div>
      </div>
      
      <div className={styles.bcgDetails}>
        <h4>Your Position: {bcg.quadrant}</h4>
        <p className={styles.interpretation}>{bcg.interpretation}</p>
        
        <div className={styles.bcgMetrics}>
          <div className={styles.metric}>
            <label>Market Share</label>
            <span>{bcg.marketShare.toFixed(1)}%</span>
          </div>
          <div className={styles.metric}>
            <label>Market Growth</label>
            <span>{bcg.marketGrowth}% CAGR</span>
          </div>
          <div className={styles.metric}>
            <label>Relative Share</label>
            <span>{bcg.relativeShare.toFixed(1)}x</span>
          </div>
        </div>
        
        <div className={styles.timeline}>
          <span className={styles.timelineIcon}>⏱</span>
          <p>{bcg.timeToTransition}</p>
        </div>
      </div>
    </div>
  );

  const renderPorters = (forces: PortersForce[]) => (
    <div className={styles.portersAnalysis}>
      {forces.map((force, i) => (
        <div key={i} className={styles.forceCard}>
          <div className={styles.forceHeader}>
            <h4>{force.name}</h4>
            <span className={`${styles.forceLevel} ${styles[force.level.toLowerCase()]}`}>
              {force.level}
            </span>
          </div>
          
          <div className={styles.forceDrivers}>
            <h5>Key Drivers:</h5>
            <ul>
              {force.drivers.map((driver, j) => (
                <li key={j}>{driver}</li>
              ))}
            </ul>
          </div>
          
          <div className={styles.forceImplication}>
            <strong>Strategic Implication:</strong>
            <p>{force.implications}</p>
          </div>
        </div>
      ))}
      
      <div className={styles.overallAttractiveness}>
        <h4>Industry Attractiveness Score</h4>
        <div className={styles.scoreBar}>
          <div 
            className={styles.scoreProgress} 
            style={{ width: `${(1 - forces.reduce((acc, f) => acc + f.score, 0) / forces.length) * 100}%` }}
          />
        </div>
        <p>
          {forces.filter(f => f.level === 'High').length} high threats • 
          {forces.filter(f => f.level === 'Medium').length} medium threats • 
          {forces.filter(f => f.level === 'Low').length} low threats
        </p>
      </div>
    </div>
  );

  const renderAnsoff = (ansoff: AnsoffStrategy) => (
    <div className={styles.ansoffAnalysis}>
      <div className={styles.ansoffMatrix}>
        <div className={styles.ansoffGrid}>
          <div className={`${styles.ansoffQuadrant} ${ansoff.currentPosition.includes('Penetration') ? styles.active : ''}`}>
            <h5>Market Penetration</h5>
            <p>Existing Products, Existing Markets</p>
          </div>
          <div className={`${styles.ansoffQuadrant} ${ansoff.currentPosition.includes('Development') ? styles.active : ''}`}>
            <h5>Market Development</h5>
            <p>Existing Products, New Markets</p>
          </div>
          <div className={`${styles.ansoffQuadrant} ${ansoff.currentPosition.includes('Product') ? styles.active : ''}`}>
            <h5>Product Development</h5>
            <p>New Products, Existing Markets</p>
          </div>
          <div className={`${styles.ansoffQuadrant} ${ansoff.currentPosition.includes('Diversification') ? styles.active : ''}`}>
            <h5>Diversification</h5>
            <p>New Products, New Markets</p>
          </div>
        </div>
      </div>
      
      <div className={styles.ansoffStrategy}>
        <h4>Recommended Strategy: {ansoff.recommendedMove}</h4>
        <div className={styles.riskIndicator}>
          <span>Risk Level:</span>
          <span className={`${styles.risk} ${styles[ansoff.riskLevel.toLowerCase()]}`}>
            {ansoff.riskLevel}
          </span>
        </div>
        
        <div className={styles.implementation}>
          <h5>Implementation Roadmap:</h5>
          <ol>
            {ansoff.implementation.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
        
        <div className={styles.expectedROI}>
          <strong>Expected Outcome:</strong>
          <p>{ansoff.expectedROI}</p>
        </div>
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner} />
          <p>Performing strategic analysis...</p>
        </div>
      </div>
    );
  }

  const currentAnalysis = analyses.find(a => a.framework_id === selectedFramework);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Strategic Framework Analysis</h2>
        <p>Deep business intelligence tailored to {assessmentData.companyInfo?.companyName || 'your company'}</p>
      </div>

      <div className={styles.frameworkTabs}>
        {analyses.map(analysis => (
          <button
            key={analysis.framework_id}
            className={`${styles.tab} ${selectedFramework === analysis.framework_id ? styles.active : ''}`}
            onClick={() => setSelectedFramework(analysis.framework_id)}
          >
            {analysis.framework_name}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {currentAnalysis && (
          <motion.div
            key={selectedFramework}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={styles.analysisContent}
          >
            {selectedFramework === 'swot' && renderSWOT(currentAnalysis.analysis)}
            {selectedFramework === 'bcg' && renderBCG(currentAnalysis.analysis)}
            {selectedFramework === 'porters' && renderPorters(currentAnalysis.analysis)}
            {selectedFramework === 'ansoff' && renderAnsoff(currentAnalysis.analysis)}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};