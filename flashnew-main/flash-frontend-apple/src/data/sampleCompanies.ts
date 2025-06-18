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
        foundedDate: '2024-01-15',
        fundingStage: 'pre-seed',
        industry: 'ai-ml',
        location: 'Remote',
        website: 'https://chataisolutions.com',
        description: 'Building AI chatbots for customer service'
      },
      capital: {
        totalRaised: 50000,
        cashOnHand: 35000,
        monthlyBurn: 8000,
        runway: 4.375,
        burnMultiple: 8,  // High burn multiple - spending 8x revenue
        lastValuation: 500000,
        primaryInvestor: 'none',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'pre-seed',
        annualRevenueRunRate: 12000,  // $12K ARR - very early stage
        monthlyRevenue: 1000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 0,
        networkEffects: false,
        hasDataMoat: false,
        regulatoryAdvantage: false,
        techDifferentiation: 2,
        switchingCosts: 1,
        brandStrength: 1,
        scalability: 2,
        productStage: 'mvp',
        uniqueAdvantage: 'None - generic AI wrapper'
      },
      market: {
        sector: 'ai-ml',
        tam: 50000000000, // $50B AI market
        sam: 5000000000,  // $5B chatbot market
        som: 50000000,    // $50M realistic target
        marketGrowthRate: 25,
        customerCount: 0,
        customerConcentration: 0,
        userGrowthRate: 0,
        netDollarRetention: 0,
        competitionIntensity: 5,
        competitorCount: 500,
        revenueGrowthRate: 0,
        grossMargin: 70,  // Assuming 70% gross margin for AI chatbot
        ltvCacRatio: 0.5  // Poor unit economics
      },
      people: {
        founderCount: 1,
        teamSize: 1,
        avgExperience: 3,
        domainExpertiseYears: 2,
        priorStartupCount: 0,
        priorExits: 0,
        boardAdvisorScore: 0,
        advisorCount: 0,
        teamDiversity: 0,
        keyPersonDependency: true,
        productRetention30d: 0,
        productRetention90d: 0,
        dauMauRatio: 0
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
        foundedDate: '2023-09-01',
        fundingStage: 'pre-seed',
        industry: 'healthcare',
        location: 'Boston, MA',
        website: 'https://neuropharma.com',
        description: 'AI-powered drug discovery for neurodegenerative diseases'
      },
      capital: {
        totalRaised: 500000,
        cashOnHand: 450000,
        monthlyBurn: 25000,
        runway: 18,
        burnMultiple: 2.5,  // Research phase, some pilot revenue
        lastValuation: 5000000,
        primaryInvestor: 'university',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'pre-seed',
        annualRevenueRunRate: 120000,  // $120K ARR from pilot programs
        monthlyRevenue: 10000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 3,
        networkEffects: false,
        hasDataMoat: true,
        regulatoryAdvantage: true,
        techDifferentiation: 5,
        switchingCosts: 4,
        brandStrength: 2,
        scalability: 3,
        productStage: 'research',
        uniqueAdvantage: 'Patented AI drug discovery platform'
      },
      market: {
        sector: 'healthcare',
        tam: 150000000000, // $150B neurodegenerative drugs
        sam: 20000000000,  // $20B AI drug discovery
        som: 500000000,    // $500M realistic target
        marketGrowthRate: 15,
        customerCount: 0,
        customerConcentration: 0,
        userGrowthRate: 0,
        netDollarRetention: 0,
        competitionIntensity: 3,
        competitorCount: 50,
        revenueGrowthRate: 0,
        grossMargin: 0,
        ltvCacRatio: 0
      },
      people: {
        founderCount: 3,
        teamSize: 5,
        avgExperience: 15,
        domainExpertiseYears: 20,
        priorStartupCount: 3,
        priorExits: 2,
        boardAdvisorScore: 4,
        advisorCount: 4,
        teamDiversity: 40,
        keyPersonDependency: false,
        productRetention30d: 0,
        productRetention90d: 0,
        dauMauRatio: 0
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
        foundedDate: '2023-03-15',
        fundingStage: 'seed',
        industry: 'saas',
        location: 'San Francisco, CA',
        website: 'https://taskflowpro.com',
        description: 'AI-enhanced project management for remote teams'
      },
      capital: {
        totalRaised: 2000000,
        cashOnHand: 1600000,
        monthlyBurn: 120000,
        runway: 13.33,
        burnMultiple: 2.4,
        lastValuation: 10000000,
        primaryInvestor: 'tier_3',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'seed',
        annualRevenueRunRate: 600000,
        monthlyRevenue: 50000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 0,
        networkEffects: true,
        hasDataMoat: false,
        regulatoryAdvantage: false,
        techDifferentiation: 3,
        switchingCosts: 3,
        brandStrength: 2,
        scalability: 3,
        productStage: 'growth',
        uniqueAdvantage: 'AI-enhanced project insights'
      },
      market: {
        sector: 'saas',
        tam: 30000000000, // $30B project management
        sam: 5000000000,  // $5B AI-enhanced PM
        som: 100000000,   // $100M realistic target
        marketGrowthRate: 20,
        customerCount: 100,
        customerConcentration: 15,
        userGrowthRate: 15,
        netDollarRetention: 110,
        competitionIntensity: 4,
        competitorCount: 200,
        revenueGrowthRate: 20,
        grossMargin: 75,
        ltvCacRatio: 2.5
      },
      people: {
        founderCount: 2,
        teamSize: 12,
        avgExperience: 8,
        domainExpertiseYears: 6,
        priorStartupCount: 1,
        priorExits: 0,
        boardAdvisorScore: 3,
        advisorCount: 2,
        teamDiversity: 25,
        keyPersonDependency: false,
        productRetention30d: 85,
        productRetention90d: 70,
        dauMauRatio: 60
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
        foundedDate: '2023-06-01',
        fundingStage: 'seed',
        industry: 'fintech',
        location: 'Miami, FL',
        website: 'https://cryptoeasy.io',
        description: 'Simple crypto trading for beginners'
      },
      capital: {
        totalRaised: 1500000,
        cashOnHand: 800000,
        monthlyBurn: 150000,
        runway: 5.33,
        burnMultiple: 5,
        lastValuation: 8000000,
        primaryInvestor: 'angel',
        hasDebt: true,
        debtAmount: 200000,
        fundingStage: 'seed',
        annualRevenueRunRate: 360000,
        monthlyRevenue: 30000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 0,
        networkEffects: false,
        hasDataMoat: false,
        regulatoryAdvantage: false,
        techDifferentiation: 1,
        switchingCosts: 1,
        brandStrength: 1,
        scalability: 2,
        productStage: 'mvp',
        uniqueAdvantage: 'None - commodity trading platform'
      },
      market: {
        sector: 'fintech',
        tam: 100000000000, // $100B crypto trading
        sam: 10000000000,  // $10B retail crypto
        som: 10000000,     // $10M realistic target
        marketGrowthRate: -10,   // Declining market
        customerCount: 1000,
        customerConcentration: 0,
        userGrowthRate: -5,
        netDollarRetention: 80,
        competitionIntensity: 5,
        competitorCount: 1000,
        revenueGrowthRate: -10,
        grossMargin: 40,
        ltvCacRatio: 0.8
      },
      people: {
        founderCount: 2,
        teamSize: 8,
        avgExperience: 5,
        domainExpertiseYears: 2,
        priorStartupCount: 0,
        priorExits: 0,
        boardAdvisorScore: 1,
        advisorCount: 1,
        teamDiversity: 12,
        keyPersonDependency: true,
        productRetention30d: 50,
        productRetention90d: 20,
        dauMauRatio: 30
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
        foundedDate: '2021-11-01',
        fundingStage: 'series-a',
        industry: 'ecommerce',
        location: 'Los Angeles, CA',
        website: 'https://ecothread.com',
        description: 'Sustainable fashion with AI-powered personalization'
      },
      capital: {
        totalRaised: 8000000,
        cashOnHand: 5000000,
        monthlyBurn: 400000,
        runway: 12.5,
        burnMultiple: 1.33,
        lastValuation: 40000000,
        primaryInvestor: 'tier_2',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'series-a',
        annualRevenueRunRate: 3600000,
        monthlyRevenue: 300000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 2,
        networkEffects: false,
        hasDataMoat: true,
        regulatoryAdvantage: false,
        techDifferentiation: 3,
        switchingCosts: 2,
        brandStrength: 4,
        scalability: 3,
        productStage: 'scaling',
        uniqueAdvantage: 'AI personalization with sustainable materials'
      },
      market: {
        sector: 'ecommerce',
        tam: 300000000000, // $300B fashion
        sam: 50000000000,  // $50B sustainable fashion
        som: 500000000,    // $500M realistic target
        marketGrowthRate: 25,
        customerCount: 50000,
        customerConcentration: 5,
        userGrowthRate: 30,
        netDollarRetention: 120,
        competitionIntensity: 3,
        competitorCount: 100,
        revenueGrowthRate: 40,
        grossMargin: 65,
        ltvCacRatio: 3.5
      },
      people: {
        founderCount: 2,
        teamSize: 45,
        avgExperience: 12,
        domainExpertiseYears: 15,
        priorStartupCount: 2,
        priorExits: 1,
        boardAdvisorScore: 4,
        advisorCount: 5,
        teamDiversity: 45,
        keyPersonDependency: false,
        productRetention30d: 90,
        productRetention90d: 75,
        dauMauRatio: 70
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
        foundedDate: '2020-08-01',
        fundingStage: 'series-a',
        industry: 'edtech',
        location: 'Austin, TX',
        website: 'https://learnsmart.edu',
        description: 'Personalized K-12 learning with AI tutors'
      },
      capital: {
        totalRaised: 10000000,
        cashOnHand: 4000000,
        monthlyBurn: 600000,
        runway: 6.67,
        burnMultiple: 2,
        lastValuation: 50000000,
        primaryInvestor: 'tier_2',
        hasDebt: true,
        debtAmount: 1000000,
        fundingStage: 'series-a',
        annualRevenueRunRate: 3600000,
        monthlyRevenue: 300000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 1,
        networkEffects: true,
        hasDataMoat: true,
        regulatoryAdvantage: true,
        techDifferentiation: 3,
        switchingCosts: 3,
        brandStrength: 3,
        scalability: 2,
        productStage: 'growth',
        uniqueAdvantage: 'AI-powered personalized curriculum'
      },
      market: {
        sector: 'edtech',
        tam: 200000000000, // $200B education
        sam: 30000000000,  // $30B online K-12
        som: 300000000,    // $300M realistic target
        marketGrowthRate: 5,     // Post-COVID slowdown
        customerCount: 10000,
        customerConcentration: 20,
        userGrowthRate: 10,
        netDollarRetention: 95,
        competitionIntensity: 4,
        competitorCount: 150,
        revenueGrowthRate: 15,
        grossMargin: 70,
        ltvCacRatio: 2.0
      },
      people: {
        founderCount: 3,
        teamSize: 60,
        avgExperience: 10,
        domainExpertiseYears: 8,
        priorStartupCount: 1,
        priorExits: 0,
        boardAdvisorScore: 3,
        advisorCount: 3,
        teamDiversity: 35,
        keyPersonDependency: false,
        productRetention30d: 80,
        productRetention90d: 65,
        dauMauRatio: 50
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
        foundedDate: '2019-05-15',
        fundingStage: 'series-b',
        industry: 'logistics',
        location: 'Chicago, IL',
        website: 'https://logiflow.ai',
        description: 'End-to-end supply chain optimization using AI'
      },
      capital: {
        totalRaised: 35000000,
        cashOnHand: 20000000,
        monthlyBurn: 1200000,
        runway: 16.67,
        burnMultiple: 0.8,
        lastValuation: 200000000,
        primaryInvestor: 'tier_1',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'series-b',
        annualRevenueRunRate: 18000000,
        monthlyRevenue: 1500000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 5,
        networkEffects: true,
        hasDataMoat: true,
        regulatoryAdvantage: false,
        techDifferentiation: 5,
        switchingCosts: 5,
        brandStrength: 4,
        scalability: 4,
        productStage: 'mature',
        uniqueAdvantage: 'Proprietary AI models with network effects'
      },
      market: {
        sector: 'logistics',
        tam: 500000000000, // $500B logistics
        sam: 50000000000,  // $50B AI logistics
        som: 2000000000,   // $2B realistic target
        marketGrowthRate: 18,
        customerCount: 200,
        customerConcentration: 25,
        userGrowthRate: 25,
        netDollarRetention: 130,
        competitionIntensity: 3,
        competitorCount: 30,
        revenueGrowthRate: 35,
        grossMargin: 80,
        ltvCacRatio: 4.5
      },
      people: {
        founderCount: 3,
        teamSize: 150,
        avgExperience: 15,
        domainExpertiseYears: 20,
        priorStartupCount: 4,
        priorExits: 3,
        boardAdvisorScore: 5,
        advisorCount: 8,
        teamDiversity: 40,
        keyPersonDependency: false,
        productRetention30d: 95,
        productRetention90d: 90,
        dauMauRatio: 85
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
        foundedDate: '2018-09-01',
        fundingStage: 'series-b',
        industry: 'real-estate',
        location: 'New York, NY',
        website: 'https://propertyhub.com',
        description: 'All-in-one property management platform'
      },
      capital: {
        totalRaised: 40000000,
        cashOnHand: 8000000,
        monthlyBurn: 2000000,
        runway: 4,
        burnMultiple: 4,
        lastValuation: 180000000,
        primaryInvestor: 'tier_3',
        hasDebt: true,
        debtAmount: 5000000,
        fundingStage: 'series-b',
        annualRevenueRunRate: 6000000,
        monthlyRevenue: 500000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 0,
        networkEffects: false,
        hasDataMoat: false,
        regulatoryAdvantage: false,
        techDifferentiation: 2,
        switchingCosts: 2,
        brandStrength: 2,
        scalability: 2,
        productStage: 'growth',
        uniqueAdvantage: 'None - crowded market'
      },
      market: {
        sector: 'real-estate',
        tam: 100000000000, // $100B property management
        sam: 10000000000,  // $10B digital PM
        som: 100000000,    // $100M realistic target
        marketGrowthRate: 8,
        customerCount: 5000,
        customerConcentration: 10,
        userGrowthRate: 5,
        netDollarRetention: 85,
        competitionIntensity: 5,
        competitorCount: 200,
        revenueGrowthRate: 10,
        grossMargin: 60,
        ltvCacRatio: 1.5
      },
      people: {
        founderCount: 2,
        teamSize: 120,
        avgExperience: 8,
        domainExpertiseYears: 5,
        priorStartupCount: 1,
        priorExits: 0,
        boardAdvisorScore: 2,
        advisorCount: 4,
        teamDiversity: 20,
        keyPersonDependency: true,
        productRetention30d: 70,
        productRetention90d: 50,
        dauMauRatio: 40
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
        foundedDate: '2017-03-01',
        fundingStage: 'series-c',
        industry: 'transportation',
        location: 'Palo Alto, CA',
        website: 'https://robodeliver.com',
        description: 'Autonomous last-mile delivery at scale'
      },
      capital: {
        totalRaised: 150000000,
        cashOnHand: 80000000,
        monthlyBurn: 3500000,
        runway: 22.86,
        burnMultiple: 0.7,
        lastValuation: 1000000000,
        primaryInvestor: 'tier_1',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'series-c',
        annualRevenueRunRate: 60000000,
        monthlyRevenue: 5000000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 25,
        networkEffects: true,
        hasDataMoat: true,
        regulatoryAdvantage: true,
        techDifferentiation: 5,
        switchingCosts: 4,
        brandStrength: 5,
        scalability: 5,
        productStage: 'mature',
        uniqueAdvantage: 'Industry-leading autonomous delivery tech'
      },
      market: {
        sector: 'transportation',
        tam: 800000000000, // $800B delivery
        sam: 100000000000, // $100B autonomous delivery
        som: 10000000000,  // $10B realistic target
        marketGrowthRate: 35,
        customerCount: 500,
        customerConcentration: 15,
        userGrowthRate: 40,
        netDollarRetention: 140,
        competitionIntensity: 3,
        competitorCount: 20,
        revenueGrowthRate: 50,
        grossMargin: 85,
        ltvCacRatio: 5.0
      },
      people: {
        founderCount: 4,
        teamSize: 500,
        avgExperience: 18,
        domainExpertiseYears: 25,
        priorStartupCount: 6,
        priorExits: 5,
        boardAdvisorScore: 5,
        advisorCount: 12,
        teamDiversity: 35,
        keyPersonDependency: false,
        productRetention30d: 98,
        productRetention90d: 95,
        dauMauRatio: 90
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
        foundedDate: '2016-07-15',
        fundingStage: 'series-c',
        industry: 'clean-tech',
        location: 'Phoenix, AZ',
        website: 'https://sunpowerhomes.com',
        description: 'AI-optimized residential solar installations'
      },
      capital: {
        totalRaised: 120000000,
        cashOnHand: 30000000,
        monthlyBurn: 4000000,
        runway: 7.5,
        burnMultiple: 1.33,
        lastValuation: 600000000,
        primaryInvestor: 'tier_2',
        hasDebt: true,
        debtAmount: 20000000,
        fundingStage: 'series-c',
        annualRevenueRunRate: 36000000,
        monthlyRevenue: 3000000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 8,
        networkEffects: false,
        hasDataMoat: true,
        regulatoryAdvantage: true,
        techDifferentiation: 3,
        switchingCosts: 4,
        brandStrength: 3,
        scalability: 3,
        productStage: 'mature',
        uniqueAdvantage: 'AI-optimized solar panel placement'
      },
      market: {
        sector: 'clean-tech',
        tam: 200000000000, // $200B renewable energy
        sam: 50000000000,  // $50B residential solar
        som: 2000000000,   // $2B realistic target
        marketGrowthRate: 10,
        customerCount: 50000,
        customerConcentration: 5,
        userGrowthRate: 15,
        netDollarRetention: 100,
        competitionIntensity: 4,
        competitorCount: 100,
        revenueGrowthRate: 20,
        grossMargin: 45,
        ltvCacRatio: 2.5
      },
      people: {
        founderCount: 3,
        teamSize: 350,
        avgExperience: 14,
        domainExpertiseYears: 15,
        priorStartupCount: 3,
        priorExits: 2,
        boardAdvisorScore: 4,
        advisorCount: 7,
        teamDiversity: 30,
        keyPersonDependency: false,
        productRetention30d: 95,
        productRetention90d: 90,
        dauMauRatio: 75
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
        foundedDate: '2023-12-01',
        fundingStage: 'seed',
        industry: 'deep-tech',
        location: 'Houston, TX',
        website: 'https://asteroidmine.space',
        description: 'Mining rare minerals from near-Earth asteroids'
      },
      capital: {
        totalRaised: 3000000,
        cashOnHand: 2500000,
        monthlyBurn: 300000,
        runway: 8.33,
        burnMultiple: 30,  // Very high burn, minimal revenue
        lastValuation: 20000000,
        primaryInvestor: 'angel',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'seed',
        annualRevenueRunRate: 120000,  // $120K from research grants/consulting
        monthlyRevenue: 10000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 2,
        networkEffects: false,
        hasDataMoat: false,
        regulatoryAdvantage: true,
        techDifferentiation: 5,
        switchingCosts: 5,
        brandStrength: 2,
        scalability: 1,
        productStage: 'concept',
        uniqueAdvantage: 'Ambitious space mining technology'
      },
      market: {
        sector: 'deep-tech',
        tam: 1000000000000, // $1T space economy (2040)
        sam: 10000000000,   // $10B space mining (2040)
        som: 0,             // $0 current market
        marketGrowthRate: 0,
        customerCount: 0,
        customerConcentration: 0,
        userGrowthRate: 0,
        netDollarRetention: 0,
        competitionIntensity: 2,
        competitorCount: 5,
        revenueGrowthRate: 0,
        grossMargin: 0,
        ltvCacRatio: 0
      },
      people: {
        founderCount: 2,
        teamSize: 8,
        avgExperience: 20,
        domainExpertiseYears: 15,
        priorStartupCount: 2,
        priorExits: 0,
        boardAdvisorScore: 3,
        advisorCount: 3,
        teamDiversity: 25,
        keyPersonDependency: true,
        productRetention30d: 0,
        productRetention90d: 0,
        dauMauRatio: 0
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
        foundedDate: '2020-02-01',
        fundingStage: 'series-a',
        industry: 'healthcare',
        location: 'Nashville, TN',
        website: 'https://dentapractice.com',
        description: 'Practice management software for dental offices'
      },
      capital: {
        totalRaised: 5000000,
        cashOnHand: 6000000, // Profitable!
        monthlyBurn: -100000, // Net positive
        runway: 999, // Infinite - profitable
        burnMultiple: -2, // Negative burn multiple - profitable
        lastValuation: 50000000,
        primaryInvestor: 'tier_3',
        hasDebt: false,
        debtAmount: 0,
        fundingStage: 'series-a',
        annualRevenueRunRate: 6000000,
        monthlyRevenue: 500000,
        hasRevenue: true
      },
      advantage: {
        patentCount: 0,
        networkEffects: true,
        hasDataMoat: true,
        regulatoryAdvantage: true,
        techDifferentiation: 2,
        switchingCosts: 5,
        brandStrength: 3,
        scalability: 4,
        productStage: 'mature',
        uniqueAdvantage: 'Deep vertical integration and high switching costs'
      },
      market: {
        sector: 'healthcare',
        tam: 10000000000, // $10B dental software
        sam: 2000000000,  // $2B practice management
        som: 200000000,   // $200M realistic target
        marketGrowthRate: 12,
        customerCount: 2000,
        customerConcentration: 3,
        userGrowthRate: 20,
        netDollarRetention: 115,
        competitionIntensity: 2,
        competitorCount: 20,
        revenueGrowthRate: 25,
        grossMargin: 85,
        ltvCacRatio: 6.0
      },
      people: {
        founderCount: 2,
        teamSize: 35,
        avgExperience: 15,
        domainExpertiseYears: 20,
        priorStartupCount: 2,
        priorExits: 1,
        boardAdvisorScore: 4,
        advisorCount: 4,
        teamDiversity: 40,
        keyPersonDependency: false,
        productRetention30d: 95,
        productRetention90d: 92,
        dauMauRatio: 80
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
    company.data.companyInfo.fundingStage === stage
  );
};

// Helper function to get a random sample
export const getRandomSample = () => {
  const index = Math.floor(Math.random() * sampleCompanies.length);
  return sampleCompanies[index];
};