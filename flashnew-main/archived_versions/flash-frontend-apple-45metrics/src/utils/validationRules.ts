import { commonRules } from '../hooks/useFormValidation';

export const companyInfoValidation = {
  companyName: {
    required: true,
    pattern: /^.{2,100}$/,
    message: 'Company name must be 2-100 characters',
  },
  website: {
    ...commonRules.url,
    required: false,
  },
  industry: {
    required: true,
    message: 'Please select an industry',
  },
  fundingStage: {
    required: true,
    message: 'Please select a funding stage',
  },
  foundedDate: {
    required: true,
    custom: (value: Date | null) => {
      if (!value) return 'Please select a founding date';
      const year = value.getFullYear();
      const currentYear = new Date().getFullYear();
      if (year < 1900 || year > currentYear) {
        return `Year must be between 1900 and ${currentYear}`;
      }
      return null;
    },
  },
};

export const capitalValidation = {
  totalFundingRaised: {
    required: true,
    min: 0,
    max: 10000000000, // $10B max
    message: 'Please enter a valid funding amount',
  },
  monthlyBurnRate: {
    required: true,
    min: 0,
    max: 100000000, // $100M max monthly burn
    message: 'Please enter a valid monthly burn rate',
  },
  runwayMonths: {
    required: true,
    min: 0,
    max: 120, // 10 years max
    message: 'Runway must be between 0 and 120 months',
  },
  annualRevenueRunRate: {
    required: true,
    min: 0,
    max: 10000000000, // $10B max
    message: 'Please enter a valid revenue amount',
  },
  grossMargin: {
    ...commonRules.percentage,
    required: true,
  },
  ltvCacRatio: {
    required: false,
    min: 0,
    max: 100,
    message: 'LTV/CAC ratio must be between 0 and 100',
  },
};

export const advantageValidation = {
  moatStrength: {
    required: true,
    min: 1,
    max: 10,
    message: 'Moat strength must be between 1 and 10',
  },
  advantages: {
    custom: (value: string[]) => {
      if (!value || value.length === 0) {
        return 'Please select at least one competitive advantage';
      }
      return null;
    },
  },
  uniqueAdvantage: {
    required: true,
    pattern: /^.{10,500}$/,
    message: 'Please describe your unique advantage (10-500 characters)',
  },
  patentCount: {
    min: 0,
    max: 1000,
    message: 'Patent count must be between 0 and 1000',
  },
};

export const marketValidation = {
  marketSize: {
    required: true,
    min: 1000000, // $1M minimum TAM
    max: 10000000000000, // $10T max
    message: 'Market size must be at least $1M',
  },
  marketGrowthRate: {
    required: true,
    min: -50,
    max: 500,
    message: 'Growth rate must be between -50% and 500%',
  },
  competitionLevel: {
    required: true,
    min: 1,
    max: 10,
    message: 'Competition level must be between 1 and 10',
  },
  differentiationLevel: {
    required: true,
    min: 1,
    max: 10,
    message: 'Differentiation level must be between 1 and 10',
  },
  targetMarket: {
    required: true,
    message: 'Please select a target market',
  },
  goToMarketStrategy: {
    required: true,
    pattern: /^.{10,500}$/,
    message: 'Please describe your go-to-market strategy (10-500 characters)',
  },
  customerAcquisitionCost: {
    min: 0,
    max: 100000,
    message: 'CAC must be between $0 and $100,000',
  },
  marketTiming: {
    required: true,
    min: 1,
    max: 10,
    message: 'Market timing score must be between 1 and 10',
  },
};

export const peopleValidation = {
  teamSize: {
    required: true,
    min: 1,
    max: 10000,
    message: 'Team size must be between 1 and 10,000',
  },
  foundersCount: {
    required: true,
    min: 1,
    max: 10,
    message: 'Founders count must be between 1 and 10',
  },
  technicalFounders: {
    min: 0,
    max: 10,
    custom: (value: number, data: any) => {
      if (value > data.foundersCount) {
        return 'Technical founders cannot exceed total founders';
      }
      return null;
    },
  },
  industryExperience: {
    required: true,
    min: 1,
    max: 10,
    message: 'Industry experience must be between 1 and 10',
  },
  previousExits: {
    min: 0,
    max: 50,
    message: 'Previous exits must be between 0 and 50',
  },
  teamCulture: {
    required: true,
    min: 1,
    max: 10,
    message: 'Team culture score must be between 1 and 10',
  },
  keyRoles: {
    custom: (value: string[]) => {
      if (!value || value.length === 0) {
        return 'Please select at least one key role filled';
      }
      return null;
    },
  },
  advisorsCount: {
    min: 0,
    max: 100,
    message: 'Advisors count must be between 0 and 100',
  },
};