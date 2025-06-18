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
  sector: {
    required: true,
    message: 'Please select a sector',
  },
  stage: {
    required: true,
    message: 'Please select a funding stage',
  },
  foundingDate: {
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
  headquarters: {
    required: false,
    pattern: /^.{2,100}$/,
    message: 'Headquarters must be 2-100 characters',
  },
  description: {
    required: false,
    pattern: /^.{0,500}$/,
    message: 'Description must be under 500 characters',
  },
};

export const capitalValidation = {
  totalRaised: {
    required: true,
    min: 0,
    max: 10000000000, // $10B max
    message: 'Please enter a valid funding amount',
  },
  cashOnHand: {
    required: true,
    min: -100000000, // Allow negative for companies in debt
    max: 10000000000, // $10B max
    message: 'Please enter a valid cash amount',
  },
  monthlyBurn: {
    required: true,
    min: -10000000, // Allow negative for profitable companies
    max: 100000000, // $100M max monthly burn
    message: 'Please enter a valid monthly burn rate',
  },
  lastValuation: {
    required: true,
    min: 0,
    max: 100000000000, // $100B max
    message: 'Please enter a valid valuation',
  },
  primaryInvestor: {
    required: true,
    message: 'Please select primary investor type',
  },
  debtAmount: {
    required: false,
    min: 0,
    max: 1000000000, // $1B max debt
    message: 'Please enter a valid debt amount',
  },
};

export const advantageValidation = {
  patentCount: {
    min: 0,
    max: 1000,
    message: 'Patent count must be between 0 and 1000',
  },
  brandRecognition: {
    required: true,
    min: 1,
    max: 5,
    message: 'Brand recognition must be between 1 and 5',
  },
  customerLoyalty: {
    required: true,
    min: 1,
    max: 5,
    message: 'Customer loyalty must be between 1 and 5',
  },
  switchingCosts: {
    required: true,
    min: 1,
    max: 5,
    message: 'Switching costs must be between 1 and 5',
  },
  techDifferentiation: {
    required: true,
    min: 1,
    max: 5,
    message: 'Tech differentiation must be between 1 and 5',
  },
  costAdvantage: {
    required: true,
    min: 1,
    max: 5,
    message: 'Cost advantage must be between 1 and 5',
  },
};

export const marketValidation = {
  tam: {
    required: true,
    min: 1000000, // $1M minimum TAM
    max: 10000000000000, // $10T max
    message: 'TAM must be at least $1M',
  },
  sam: {
    required: true,
    min: 100000, // $100K minimum SAM
    max: 10000000000000, // $10T max
    message: 'SAM must be at least $100K',
  },
  som: {
    required: true,
    min: 0,
    max: 10000000000000, // $10T max
    message: 'SOM must be a valid amount',
  },
  growthRate: {
    required: true,
    min: -50,
    max: 500,
    message: 'Growth rate must be between -50% and 500%',
  },
  marketShare: {
    required: false,
    min: 0,
    max: 100,
    message: 'Market share must be between 0% and 100%',
  },
  competitorCount: {
    required: false,
    min: 0,
    max: 10000,
    message: 'Competitor count must be between 0 and 10,000',
  },
  competitionIntensity: {
    required: true,
    min: 1,
    max: 5,
    message: 'Competition intensity must be between 1 and 5',
  },
  customerConcentration: {
    required: false,
    min: 0,
    max: 100,
    message: 'Customer concentration must be between 0% and 100%',
  },
  regulatoryRisk: {
    required: true,
    min: 1,
    max: 5,
    message: 'Regulatory risk must be between 1 and 5',
  },
};

export const peopleValidation = {
  founderCount: {
    required: true,
    min: 1,
    max: 10,
    message: 'Founder count must be between 1 and 10',
  },
  teamSize: {
    required: true,
    min: 1,
    max: 10000,
    message: 'Team size must be between 1 and 10,000',
  },
  techTeamSize: {
    required: true,
    min: 0,
    max: 10000,
    custom: (value: number, data: any) => {
      if (value > data.teamSize) {
        return 'Tech team size cannot exceed total team size';
      }
      return null;
    },
  },
  advisorCount: {
    min: 0,
    max: 100,
    message: 'Advisor count must be between 0 and 100',
  },
  boardSize: {
    min: 0,
    max: 50,
    message: 'Board size must be between 0 and 50',
  },
  avgExperience: {
    required: true,
    min: 0,
    max: 50,
    message: 'Average experience must be between 0 and 50 years',
  },
  priorExits: {
    min: 0,
    max: 50,
    message: 'Prior exits must be between 0 and 50',
  },
  domainExpertise: {
    required: true,
    min: 1,
    max: 5,
    message: 'Domain expertise must be between 1 and 5',
  },
  teamDiversity: {
    min: 0,
    max: 100,
    message: 'Team diversity must be between 0% and 100%',
  },
};