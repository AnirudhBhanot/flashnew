import React, { useEffect } from 'react';
import { DataDrivenFrameworkAnalysis } from '../components/DataDrivenFrameworkAnalysis';
import useAssessmentStore from '../store/assessmentStore';
import styles from './TestDataDrivenFramework.module.scss';

// Sample data that demonstrates the data-driven analysis
const sampleAssessmentData = {
  companyInfo: {
    companyName: "TechStartup Inc",
    stage: "seed",
    industry: "SaaS"
  },
  capital: {
    totalRaised: 2000000,
    cashOnHand: 1500000,
    monthlyBurn: 150000,
    runwayMonths: 10,
    burnMultiple: 1.2,
    annualRevenueRunRate: 1200000,
    fundingStage: 'seed',
    primaryInvestor: 'tier_2'
  },
  advantage: {
    productStage: 'launched',
    proprietaryTech: true,
    patentCount: 3,
    networkEffects: true,
    hasDataMoat: true,
    regulatoryAdvantage: false,
    techDifferentiation: 4,
    switchingCosts: 3,
    brandStrength: 2,
    scalability: 4
  },
  market: {
    tam: 5000000000, // $5B
    sam: 500000000,  // $500M
    som: 50000000,   // $50M
    marketGrowthRate: 35, // 35% annually
    customerCount: 120,
    customerConcentration: 40, // Top 20% = 40% of revenue
    competitorCount: 15,
    userGrowthRate: 25, // 25% monthly
    netDollarRetention: 115,
    competitionIntensity: 4,
    businessModel: 'b2b',
    sector: 'saas',
    customerAcquisitionCost: 5000,
    lifetimeValue: 20000,
    ltvCacRatio: 4,
    revenueGrowthRate: 200, // 200% YoY
    grossMargin: 75,
    productRetention30d: 85,
    productRetention90d: 70,
    dauMauRatio: 60
  },
  people: {
    founderCount: 2,
    teamSize: 15,
    fullTimeEmployees: 15,
    avgExperience: 8,
    domainExpertiseYears: 12,
    industryExperience: 12,
    priorStartupCount: 2,
    priorExits: 1,
    boardAdvisorScore: 4,
    advisorCount: 5,
    teamDiversity: 40,
    keyPersonDependency: false
  }
};

const TestDataDrivenFramework: React.FC = () => {
  const setAssessmentData = useAssessmentStore(state => state.setData);

  useEffect(() => {
    // Set the sample data in the store
    setAssessmentData(sampleAssessmentData);
  }, [setAssessmentData]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Data-Driven Framework Analysis</h1>
        <p>Demonstrating quantified insights and specific recommendations based on actual startup data</p>
      </div>
      
      <div className={styles.dataOverview}>
        <h2>Test Data Overview</h2>
        <div className={styles.dataGrid}>
          <div className={styles.dataCard}>
            <h3>Financial Metrics</h3>
            <ul>
              <li>ARR: $1.2M</li>
              <li>Monthly Burn: $150K</li>
              <li>Runway: 10 months</li>
              <li>Cash: $1.5M</li>
            </ul>
          </div>
          <div className={styles.dataCard}>
            <h3>Market Position</h3>
            <ul>
              <li>TAM: $5B</li>
              <li>Market Growth: 35%</li>
              <li>Competitors: 15</li>
              <li>Customer Count: 120</li>
            </ul>
          </div>
          <div className={styles.dataCard}>
            <h3>Unit Economics</h3>
            <ul>
              <li>CAC: $5K</li>
              <li>LTV: $20K</li>
              <li>LTV/CAC: 4.0x</li>
              <li>Gross Margin: 75%</li>
            </ul>
          </div>
          <div className={styles.dataCard}>
            <h3>Growth Metrics</h3>
            <ul>
              <li>Revenue Growth: 200% YoY</li>
              <li>User Growth: 25% MoM</li>
              <li>NDR: 115%</li>
              <li>30d Retention: 85%</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className={styles.analysisSection}>
        <DataDrivenFrameworkAnalysis />
      </div>
      
      <div className={styles.comparisonNote}>
        <h3>Key Improvements in This Analysis</h3>
        <div className={styles.improvements}>
          <div className={styles.improvement}>
            <h4>❌ Generic Analysis (Old)</h4>
            <ul>
              <li>"Focus on customer acquisition"</li>
              <li>"Consider raising more funding"</li>
              <li>"Improve product-market fit"</li>
              <li>"Optimize operations"</li>
            </ul>
          </div>
          <div className={styles.improvement}>
            <h4>✅ Data-Driven Analysis (New)</h4>
            <ul>
              <li>"Increase monthly growth from 25% to 37.5% to achieve market leadership in 8 months"</li>
              <li>"Reduce CAC from $5K to $3.5K through channel optimization - save $180K annually"</li>
              <li>"Target 2.1% market share ($105M revenue) based on current trajectory"</li>
              <li>"Invest $900K over 6 months for 3.5x ROI based on current burn efficiency"</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestDataDrivenFramework;