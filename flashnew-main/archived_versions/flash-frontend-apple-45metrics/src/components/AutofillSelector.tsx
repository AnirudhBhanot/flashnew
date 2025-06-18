import React, { useState } from 'react';
import { sampleCompanies, SampleCompany } from '../data/sampleCompanies';
import useAssessmentStore from '../store/assessmentStore';
import styles from './AutofillSelector.module.scss';

// Helper functions to map data formats
const mapIndustry = (sector: string): string => {
  const industryMap: Record<string, string> = {
    'ai-ml': 'saas',
    'healthcare': 'healthtech',
    'saas': 'saas',
    'fintech': 'fintech',
    'ecommerce': 'ecommerce',
    'edtech': 'edtech',
    'logistics': 'enterprise',
    'real-estate': 'other',
    'transportation': 'other',
    'clean-tech': 'deeptech',
    'deep-tech': 'deeptech',
    'biotech': 'healthtech',
    'marketplace': 'marketplace',
    'consumer': 'consumer',
    'enterprise': 'enterprise'
  };
  return industryMap[sector] || 'other';
};

const mapStage = (stage: string): string => {
  // Convert hyphenated to underscore format
  return stage.replace(/-/g, '_');
};

interface AutofillSelectorProps {
  variant?: 'inline' | 'floating';
  onSelect?: () => void;
}

export const AutofillSelector: React.FC<AutofillSelectorProps> = ({ 
  variant = 'inline',
  onSelect 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const updateData = useAssessmentStore(state => state.updateData);

  const categories = [
    { value: 'all', label: 'All Companies' },
    { value: 'pass', label: 'Likely Pass' },
    { value: 'fail', label: 'Likely Fail' },
    { value: 'conditional', label: 'Conditional' },
    { value: 'pre-seed', label: 'Pre-Seed' },
    { value: 'seed', label: 'Seed' },
    { value: 'series-a', label: 'Series A' },
    { value: 'series-b', label: 'Series B' },
    { value: 'series-c', label: 'Series C+' }
  ];

  const filteredCompanies = sampleCompanies.filter(company => {
    if (selectedCategory === 'all') return true;
    if (['pass', 'fail', 'conditional'].includes(selectedCategory)) {
      return company.expectedOutcome === selectedCategory;
    }
    return company.data.companyInfo.stage === selectedCategory;
  });

  const handleSelectCompany = (company: SampleCompany) => {
    // Map the sample data to the store format with correct field mappings
    const mappedData = {
      companyInfo: {
        companyName: company.data.companyInfo.companyName,
        website: company.data.companyInfo.website,
        industry: mapIndustry(company.data.companyInfo.sector),
        foundedDate: company.data.companyInfo.foundingDate,
        stage: mapStage(company.data.companyInfo.stage),
        location: company.data.companyInfo.headquarters,
        description: company.data.companyInfo.description
      },
      capital: {
        totalFundingRaised: company.data.capital.totalRaised,
        monthlyBurnRate: company.data.capital.monthlyBurn,
        runwayMonths: Math.round(company.data.capital.cashOnHand / company.data.capital.monthlyBurn),
        annualRevenueRunRate: company.data.capital.totalRaised * 0.6, // Estimate
        grossMargin: 70, // Default
        ltvCacRatio: 3 // Default
      },
      advantage: {
        moatStrength: Math.round((company.data.advantage.techDifferentiation + company.data.advantage.switchingCosts) / 2),
        advantages: [],
        uniqueAdvantage: company.data.advantage.patentCount > 0 ? 'Patented technology' : 'Technical innovation',
        hasPatents: company.data.advantage.patentCount > 0,
        patentCount: company.data.advantage.patentCount
      },
      market: {
        marketSize: company.data.market.tam,
        marketGrowthRate: company.data.market.growthRate,
        competitionLevel: company.data.market.competitionIntensity,
        differentiationLevel: 3, // Default
        targetMarket: 'Enterprise',
        goToMarketStrategy: 'Direct sales',
        customerAcquisitionCost: 1000, // Default
        marketTiming: 3 // Default
      },
      people: {
        teamSize: company.data.people.teamSize,
        foundersCount: company.data.people.founderCount,
        technicalFounders: Math.ceil(company.data.people.founderCount / 2),
        industryExperience: company.data.people.domainExpertise,
        previousStartups: company.data.people.priorExits > 0,
        previousExits: company.data.people.priorExits,
        teamCulture: 4, // Default
        keyRoles: [],
        advisorsCount: company.data.people.advisorCount,
        teamWeaknesses: company.data.people.keyPersonRisk ? 'Key person dependency' : 'None identified'
      }
    };
    
    // Update all sections
    updateData('companyInfo', mappedData.companyInfo);
    updateData('capital', mappedData.capital);
    updateData('advantage', mappedData.advantage);
    updateData('market', mappedData.market);
    updateData('people', mappedData.people);
    
    setIsOpen(false);
    onSelect?.();
    
    // Show success message
    const message = document.createElement('div');
    message.className = styles.successMessage;
    message.textContent = `Loaded: ${company.name}`;
    document.body.appendChild(message);
    setTimeout(() => message.remove(), 3000);
  };

  if (variant === 'floating') {
    return (
      <div className={styles.floatingContainer}>
        <button
          className={styles.floatingButton}
          onClick={() => setIsOpen(!isOpen)}
          title="Load Sample Company"
        >
          <span>🧪</span>
        </button>
        {isOpen && (
          <div className={styles.floatingPanel}>
            <h3>Load Sample Company</h3>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className={styles.categorySelect}
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
            <div className={styles.companyList}>
              {filteredCompanies.map(company => (
                <button
                  key={company.id}
                  className={styles.companyItem}
                  onClick={() => handleSelectCompany(company)}
                >
                  <div className={styles.companyName}>{company.name}</div>
                  <div className={styles.companyDesc}>{company.description}</div>
                  <div className={`${styles.outcome} ${styles[company.expectedOutcome]}`}>
                    {company.expectedOutcome.toUpperCase()}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className={styles.inlineContainer}>
      <button
        className={styles.triggerButton}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span>Load Sample Company</span>
        <svg 
          className={isOpen ? styles.rotated : ''} 
          width="16" 
          height="16" 
          viewBox="0 0 16 16" 
          fill="currentColor"
        >
          <path d="M3.5 5.5L8 10L12.5 5.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
        </svg>
      </button>
      
      {isOpen && (
        <div className={styles.dropdown}>
          <div className={styles.dropdownHeader}>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className={styles.categorySelect}
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>
          <div className={styles.companyList}>
            {filteredCompanies.map(company => (
              <button
                key={company.id}
                className={styles.companyItem}
                onClick={() => handleSelectCompany(company)}
              >
                <div className={styles.companyInfo}>
                  <div className={styles.companyName}>{company.name}</div>
                  <div className={styles.companyDesc}>{company.description}</div>
                </div>
                <div className={`${styles.outcome} ${styles[company.expectedOutcome]}`}>
                  {company.expectedOutcome.toUpperCase()}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};