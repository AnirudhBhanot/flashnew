// Realistic sample companies for testing different scenarios
// Based on real-world data patterns from actual startups

export interface SampleCompany {
  id: string;
  name: string;
  description: string;
  expectedOutcome: 'pass' | 'fail' | 'conditional';
  data: any;
}

export const sampleCompanies: SampleCompany[] = [
  // Pre-Seed Stage Companies
  {
    id: 'preseed-ai-fail',
    name: 'AI Chatbot Startup (Pre-seed) - Likely Fail',
    description: 'Generic AI wrapper with no differentiation, solo founder, no revenue',
    expectedOutcome: 'fail',
    data: {
      companyInfo: {
        companyName: 'ChatAI Solutions',
        foundingDate: '2024-01-15',
        stage: 'pre-seed',
        sector: 'ai-ml',
        headquarters: 'Remote',
        website: 'https://chataisolutions.com',
        description: 'Building AI chatbots for customer service'
      },
      capital: {
        totalRaised: 50000,
        cashOnHand: 35000,
        monthlyBurn: 8000,
        lastValuation: 500000,
        primaryInvestor: 'none',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 0,
        tradeSecrets: false,
        networkEffects: false,
        dataMode: false,
        regulatoryBarriers: false,
        brandRecognition: 1,
        customerLoyalty: 1,
        switchingCosts: 1,
        techDifferentiation: 2,
        costAdvantage: 2
      },
      market: {
        tam: 50000000000, // $50B AI market
        sam: 5000000000,  // $5B chatbot market
        som: 50000000,    // $50M realistic target
        growthRate: 25,
        marketShare: 0,
        competitorCount: 500,
        competitionIntensity: 5,
        customerConcentration: 0,
        regulatoryRisk: 2
      },
      people: {
        founderCount: 1,
        teamSize: 1,
        techTeamSize: 1,
        advisorCount: 0,
        boardSize: 0,
        avgExperience: 3,
        priorExits: 0,
        domainExpertise: 2,
        teamDiversity: 0,
        keyPersonRisk: true
      }
    }
  },
  {
    id: 'preseed-biotech-pass',
    name: 'BioTech Spin-off (Pre-seed) - Likely Pass',
    description: 'University spin-off with patented drug discovery platform, experienced team',
    expectedOutcome: 'pass',
    data: {
      companyInfo: {
        companyName: 'NeuroPharma Innovations',
        foundingDate: '2023-09-01',
        stage: 'pre-seed',
        sector: 'healthcare',
        headquarters: 'Boston, MA',
        website: 'https://neuropharma.com',
        description: 'AI-powered drug discovery for neurodegenerative diseases'
      },
      capital: {
        totalRaised: 500000,
        cashOnHand: 450000,
        monthlyBurn: 25000,
        lastValuation: 5000000,
        primaryInvestor: 'university',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 3,
        tradeSecrets: true,
        networkEffects: false,
        dataMode: true,
        regulatoryBarriers: true,
        brandRecognition: 2,
        customerLoyalty: 1,
        switchingCosts: 4,
        techDifferentiation: 5,
        costAdvantage: 3
      },
      market: {
        tam: 150000000000, // $150B neurodegenerative drugs
        sam: 20000000000,  // $20B AI drug discovery
        som: 500000000,    // $500M realistic target
        growthRate: 15,
        marketShare: 0,
        competitorCount: 50,
        competitionIntensity: 3,
        customerConcentration: 0,
        regulatoryRisk: 4
      },
      people: {
        founderCount: 3,
        teamSize: 5,
        techTeamSize: 4,
        advisorCount: 4,
        boardSize: 3,
        avgExperience: 15,
        priorExits: 2,
        domainExpertise: 5,
        teamDiversity: 40,
        keyPersonRisk: false
      }
    }
  },

  // Seed Stage Companies
  {
    id: 'seed-saas-conditional',
    name: 'B2B SaaS (Seed) - Conditional Pass',
    description: 'Project management tool with early traction but high competition',
    expectedOutcome: 'conditional',
    data: {
      companyInfo: {
        companyName: 'TaskFlow Pro',
        foundingDate: '2023-03-15',
        stage: 'seed',
        sector: 'saas',
        headquarters: 'San Francisco, CA',
        website: 'https://taskflowpro.com',
        description: 'AI-enhanced project management for remote teams'
      },
      capital: {
        totalRaised: 2000000,
        cashOnHand: 1600000,
        monthlyBurn: 120000,
        lastValuation: 10000000,
        primaryInvestor: 'tier_3',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 0,
        tradeSecrets: false,
        networkEffects: true,
        dataMode: false,
        regulatoryBarriers: false,
        brandRecognition: 2,
        customerLoyalty: 3,
        switchingCosts: 3,
        techDifferentiation: 3,
        costAdvantage: 3
      },
      market: {
        tam: 30000000000, // $30B project management
        sam: 5000000000,  // $5B AI-enhanced PM
        som: 100000000,   // $100M realistic target
        growthRate: 20,
        marketShare: 0.01,
        competitorCount: 200,
        competitionIntensity: 4,
        customerConcentration: 15,
        regulatoryRisk: 1
      },
      people: {
        founderCount: 2,
        teamSize: 12,
        techTeamSize: 7,
        advisorCount: 2,
        boardSize: 3,
        avgExperience: 8,
        priorExits: 0,
        domainExpertise: 3,
        teamDiversity: 25,
        keyPersonRisk: false
      }
    }
  },
  {
    id: 'seed-fintech-fail',
    name: 'Crypto Trading App (Seed) - Likely Fail',
    description: 'Another crypto trading platform with no clear differentiation',
    expectedOutcome: 'fail',
    data: {
      companyInfo: {
        companyName: 'CryptoEasy Trading',
        foundingDate: '2023-06-01',
        stage: 'seed',
        sector: 'fintech',
        headquarters: 'Miami, FL',
        website: 'https://cryptoeasy.io',
        description: 'Simple crypto trading for beginners'
      },
      capital: {
        totalRaised: 1500000,
        cashOnHand: 800000,
        monthlyBurn: 150000,
        lastValuation: 8000000,
        primaryInvestor: 'angel',
        hasDebt: true,
        debtAmount: 200000
      },
      advantage: {
        patentCount: 0,
        tradeSecrets: false,
        networkEffects: false,
        dataMode: false,
        regulatoryBarriers: false,
        brandRecognition: 1,
        customerLoyalty: 1,
        switchingCosts: 1,
        techDifferentiation: 1,
        costAdvantage: 2
      },
      market: {
        tam: 100000000000, // $100B crypto trading
        sam: 10000000000,  // $10B retail crypto
        som: 10000000,     // $10M realistic target
        growthRate: -10,   // Declining market
        marketShare: 0,
        competitorCount: 1000,
        competitionIntensity: 5,
        customerConcentration: 0,
        regulatoryRisk: 5
      },
      people: {
        founderCount: 2,
        teamSize: 8,
        techTeamSize: 4,
        advisorCount: 1,
        boardSize: 0,
        avgExperience: 5,
        priorExits: 0,
        domainExpertise: 2,
        teamDiversity: 12,
        keyPersonRisk: true
      }
    }
  },

  // Series A Companies
  {
    id: 'seriesa-ecommerce-pass',
    name: 'D2C Fashion Brand (Series A) - Likely Pass',
    description: 'Sustainable fashion brand with strong unit economics and brand loyalty',
    expectedOutcome: 'pass',
    data: {
      companyInfo: {
        companyName: 'EcoThread Fashion',
        foundingDate: '2021-11-01',
        stage: 'series-a',
        sector: 'ecommerce',
        headquarters: 'Los Angeles, CA',
        website: 'https://ecothread.com',
        description: 'Sustainable fashion with AI-powered personalization'
      },
      capital: {
        totalRaised: 8000000,
        cashOnHand: 5000000,
        monthlyBurn: 400000,
        lastValuation: 40000000,
        primaryInvestor: 'tier_2',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 2,
        tradeSecrets: true,
        networkEffects: false,
        dataMode: true,
        regulatoryBarriers: false,
        brandRecognition: 4,
        customerLoyalty: 4,
        switchingCosts: 2,
        techDifferentiation: 3,
        costAdvantage: 3
      },
      market: {
        tam: 300000000000, // $300B fashion
        sam: 50000000000,  // $50B sustainable fashion
        som: 500000000,    // $500M realistic target
        growthRate: 25,
        marketShare: 0.1,
        competitorCount: 100,
        competitionIntensity: 3,
        customerConcentration: 5,
        regulatoryRisk: 2
      },
      people: {
        founderCount: 2,
        teamSize: 45,
        techTeamSize: 12,
        advisorCount: 5,
        boardSize: 5,
        avgExperience: 12,
        priorExits: 1,
        domainExpertise: 4,
        teamDiversity: 45,
        keyPersonRisk: false
      }
    }
  },
  {
    id: 'seriesa-edtech-conditional',
    name: 'Online Learning Platform (Series A) - Conditional',
    description: 'K-12 education platform with mixed metrics post-COVID boom',
    expectedOutcome: 'conditional',
    data: {
      companyInfo: {
        companyName: 'LearnSmart Academy',
        foundingDate: '2020-08-01',
        stage: 'series-a',
        sector: 'edtech',
        headquarters: 'Austin, TX',
        website: 'https://learnsmart.edu',
        description: 'Personalized K-12 learning with AI tutors'
      },
      capital: {
        totalRaised: 10000000,
        cashOnHand: 4000000,
        monthlyBurn: 600000,
        lastValuation: 50000000,
        primaryInvestor: 'tier_2',
        hasDebt: true,
        debtAmount: 1000000
      },
      advantage: {
        patentCount: 1,
        tradeSecrets: false,
        networkEffects: true,
        dataMode: true,
        regulatoryBarriers: true,
        brandRecognition: 3,
        customerLoyalty: 3,
        switchingCosts: 3,
        techDifferentiation: 3,
        costAdvantage: 2
      },
      market: {
        tam: 200000000000, // $200B education
        sam: 30000000000,  // $30B online K-12
        som: 300000000,    // $300M realistic target
        growthRate: 5,     // Post-COVID slowdown
        marketShare: 0.05,
        competitorCount: 150,
        competitionIntensity: 4,
        customerConcentration: 20,
        regulatoryRisk: 3
      },
      people: {
        founderCount: 3,
        teamSize: 60,
        techTeamSize: 20,
        advisorCount: 3,
        boardSize: 5,
        avgExperience: 10,
        priorExits: 0,
        domainExpertise: 3,
        teamDiversity: 35,
        keyPersonRisk: false
      }
    }
  },

  // Series B Companies
  {
    id: 'seriesb-logistics-pass',
    name: 'Supply Chain AI (Series B) - Strong Pass',
    description: 'AI-powered logistics optimization with Fortune 500 clients',
    expectedOutcome: 'pass',
    data: {
      companyInfo: {
        companyName: 'LogiFlow AI',
        foundingDate: '2019-05-15',
        stage: 'series-b',
        sector: 'logistics',
        headquarters: 'Chicago, IL',
        website: 'https://logiflow.ai',
        description: 'End-to-end supply chain optimization using AI'
      },
      capital: {
        totalRaised: 35000000,
        cashOnHand: 20000000,
        monthlyBurn: 1200000,
        lastValuation: 200000000,
        primaryInvestor: 'tier_1',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 5,
        tradeSecrets: true,
        networkEffects: true,
        dataMode: true,
        regulatoryBarriers: false,
        brandRecognition: 4,
        customerLoyalty: 5,
        switchingCosts: 5,
        techDifferentiation: 5,
        costAdvantage: 4
      },
      market: {
        tam: 500000000000, // $500B logistics
        sam: 50000000000,  // $50B AI logistics
        som: 2000000000,   // $2B realistic target
        growthRate: 18,
        marketShare: 0.5,
        competitorCount: 30,
        competitionIntensity: 3,
        customerConcentration: 25,
        regulatoryRisk: 2
      },
      people: {
        founderCount: 3,
        teamSize: 150,
        techTeamSize: 80,
        advisorCount: 8,
        boardSize: 7,
        avgExperience: 15,
        priorExits: 3,
        domainExpertise: 5,
        teamDiversity: 40,
        keyPersonRisk: false
      }
    }
  },
  {
    id: 'seriesb-proptech-fail',
    name: 'Real Estate Platform (Series B) - Likely Fail',
    description: 'Property management platform struggling with high CAC and churn',
    expectedOutcome: 'fail',
    data: {
      companyInfo: {
        companyName: 'PropertyHub Pro',
        foundingDate: '2018-09-01',
        stage: 'series-b',
        sector: 'real-estate',
        headquarters: 'New York, NY',
        website: 'https://propertyhub.com',
        description: 'All-in-one property management platform'
      },
      capital: {
        totalRaised: 40000000,
        cashOnHand: 8000000,
        monthlyBurn: 2000000,
        lastValuation: 180000000,
        primaryInvestor: 'tier_3',
        hasDebt: true,
        debtAmount: 5000000
      },
      advantage: {
        patentCount: 0,
        tradeSecrets: false,
        networkEffects: false,
        dataMode: false,
        regulatoryBarriers: false,
        brandRecognition: 2,
        customerLoyalty: 2,
        switchingCosts: 2,
        techDifferentiation: 2,
        costAdvantage: 2
      },
      market: {
        tam: 100000000000, // $100B property management
        sam: 10000000000,  // $10B digital PM
        som: 100000000,    // $100M realistic target
        growthRate: 8,
        marketShare: 0.1,
        competitorCount: 200,
        competitionIntensity: 5,
        customerConcentration: 10,
        regulatoryRisk: 3
      },
      people: {
        founderCount: 2,
        teamSize: 120,
        techTeamSize: 40,
        advisorCount: 4,
        boardSize: 6,
        avgExperience: 8,
        priorExits: 0,
        domainExpertise: 3,
        teamDiversity: 20,
        keyPersonRisk: true
      }
    }
  },

  // Series C+ Companies
  {
    id: 'seriesc-mobility-pass',
    name: 'Autonomous Delivery (Series C) - Strong Pass',
    description: 'Last-mile delivery robots with proven unit economics',
    expectedOutcome: 'pass',
    data: {
      companyInfo: {
        companyName: 'RoboDeliver Inc',
        foundingDate: '2017-03-01',
        stage: 'series-c',
        sector: 'transportation',
        headquarters: 'Palo Alto, CA',
        website: 'https://robodeliver.com',
        description: 'Autonomous last-mile delivery at scale'
      },
      capital: {
        totalRaised: 150000000,
        cashOnHand: 80000000,
        monthlyBurn: 3500000,
        lastValuation: 1000000000,
        primaryInvestor: 'tier_1',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 25,
        tradeSecrets: true,
        networkEffects: true,
        dataMode: true,
        regulatoryBarriers: true,
        brandRecognition: 5,
        customerLoyalty: 4,
        switchingCosts: 4,
        techDifferentiation: 5,
        costAdvantage: 5
      },
      market: {
        tam: 800000000000, // $800B delivery
        sam: 100000000000, // $100B autonomous delivery
        som: 10000000000,  // $10B realistic target
        growthRate: 35,
        marketShare: 2,
        competitorCount: 20,
        competitionIntensity: 3,
        customerConcentration: 15,
        regulatoryRisk: 4
      },
      people: {
        founderCount: 4,
        teamSize: 500,
        techTeamSize: 300,
        advisorCount: 12,
        boardSize: 9,
        avgExperience: 18,
        priorExits: 5,
        domainExpertise: 5,
        teamDiversity: 35,
        keyPersonRisk: false
      }
    }
  },
  {
    id: 'seriesc-cleantech-conditional',
    name: 'Solar Tech Company (Series C) - Conditional',
    description: 'Residential solar with regulatory headwinds and market saturation',
    expectedOutcome: 'conditional',
    data: {
      companyInfo: {
        companyName: 'SunPower Homes',
        foundingDate: '2016-07-15',
        stage: 'series-c',
        sector: 'clean-tech',
        headquarters: 'Phoenix, AZ',
        website: 'https://sunpowerhomes.com',
        description: 'AI-optimized residential solar installations'
      },
      capital: {
        totalRaised: 120000000,
        cashOnHand: 30000000,
        monthlyBurn: 4000000,
        lastValuation: 600000000,
        primaryInvestor: 'tier_2',
        hasDebt: true,
        debtAmount: 20000000
      },
      advantage: {
        patentCount: 8,
        tradeSecrets: true,
        networkEffects: false,
        dataMode: true,
        regulatoryBarriers: true,
        brandRecognition: 3,
        customerLoyalty: 3,
        switchingCosts: 4,
        techDifferentiation: 3,
        costAdvantage: 3
      },
      market: {
        tam: 200000000000, // $200B renewable energy
        sam: 50000000000,  // $50B residential solar
        som: 2000000000,   // $2B realistic target
        growthRate: 10,
        marketShare: 1,
        competitorCount: 100,
        competitionIntensity: 4,
        customerConcentration: 5,
        regulatoryRisk: 5
      },
      people: {
        founderCount: 3,
        teamSize: 350,
        techTeamSize: 80,
        advisorCount: 7,
        boardSize: 8,
        avgExperience: 14,
        priorExits: 2,
        domainExpertise: 4,
        teamDiversity: 30,
        keyPersonRisk: false
      }
    }
  },

  // Edge Cases
  {
    id: 'edge-moonshot-fail',
    name: 'Space Mining Startup (Seed) - Moonshot Fail',
    description: 'Ambitious space tech with no near-term revenue path',
    expectedOutcome: 'fail',
    data: {
      companyInfo: {
        companyName: 'AsteroidMine Corp',
        foundingDate: '2023-12-01',
        stage: 'seed',
        sector: 'deep-tech',
        headquarters: 'Houston, TX',
        website: 'https://asteroidmine.space',
        description: 'Mining rare minerals from near-Earth asteroids'
      },
      capital: {
        totalRaised: 3000000,
        cashOnHand: 2500000,
        monthlyBurn: 300000,
        lastValuation: 20000000,
        primaryInvestor: 'angel',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 2,
        tradeSecrets: true,
        networkEffects: false,
        dataMode: false,
        regulatoryBarriers: true,
        brandRecognition: 2,
        customerLoyalty: 1,
        switchingCosts: 5,
        techDifferentiation: 5,
        costAdvantage: 1
      },
      market: {
        tam: 1000000000000, // $1T space economy (2040)
        sam: 10000000000,   // $10B space mining (2040)
        som: 0,             // $0 current market
        growthRate: 0,
        marketShare: 0,
        competitorCount: 5,
        competitionIntensity: 2,
        customerConcentration: 0,
        regulatoryRisk: 5
      },
      people: {
        founderCount: 2,
        teamSize: 8,
        techTeamSize: 6,
        advisorCount: 3,
        boardSize: 3,
        avgExperience: 20,
        priorExits: 0,
        domainExpertise: 4,
        teamDiversity: 25,
        keyPersonRisk: true
      }
    }
  },
  {
    id: 'edge-profitable-pass',
    name: 'Profitable B2B SaaS (Series A) - Hidden Gem',
    description: 'Boring but profitable vertical SaaS for dentists',
    expectedOutcome: 'pass',
    data: {
      companyInfo: {
        companyName: 'DentaPractice Pro',
        foundingDate: '2020-02-01',
        stage: 'series-a',
        sector: 'healthcare',
        headquarters: 'Nashville, TN',
        website: 'https://dentapractice.com',
        description: 'Practice management software for dental offices'
      },
      capital: {
        totalRaised: 5000000,
        cashOnHand: 6000000, // Profitable!
        monthlyBurn: -100000, // Net positive
        lastValuation: 50000000,
        primaryInvestor: 'tier_3',
        hasDebt: false,
        debtAmount: 0
      },
      advantage: {
        patentCount: 0,
        tradeSecrets: false,
        networkEffects: true,
        dataMode: true,
        regulatoryBarriers: true,
        brandRecognition: 3,
        customerLoyalty: 5,
        switchingCosts: 5,
        techDifferentiation: 2,
        costAdvantage: 4
      },
      market: {
        tam: 10000000000, // $10B dental software
        sam: 2000000000,  // $2B practice management
        som: 200000000,   // $200M realistic target
        growthRate: 12,
        marketShare: 2,
        competitorCount: 20,
        competitionIntensity: 2,
        customerConcentration: 3,
        regulatoryRisk: 2
      },
      people: {
        founderCount: 2,
        teamSize: 35,
        techTeamSize: 15,
        advisorCount: 4,
        boardSize: 5,
        avgExperience: 15,
        priorExits: 1,
        domainExpertise: 5,
        teamDiversity: 40,
        keyPersonRisk: false
      }
    }
  }
];

// Helper function to get samples by expected outcome
export const getSamplesByOutcome = (outcome: 'pass' | 'fail' | 'conditional') => {
  return sampleCompanies.filter(company => company.expectedOutcome === outcome);
};

// Helper function to get samples by stage
export const getSamplesByStage = (stage: string) => {
  return sampleCompanies.filter(company => 
    company.data.companyInfo.stage === stage
  );
};

// Helper function to get a random sample
export const getRandomSample = () => {
  const index = Math.floor(Math.random() * sampleCompanies.length);
  return sampleCompanies[index];
};