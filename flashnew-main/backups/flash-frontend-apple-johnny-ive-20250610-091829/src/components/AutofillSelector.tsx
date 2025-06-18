import React, { useState } from 'react';
import { sampleCompanies, SampleCompany } from '../data/sampleCompanies';
import useAssessmentStore from '../store/assessmentStore';
import styles from './AutofillSelector.module.scss';

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
    // Generate product data based on company stage and expected outcome
    const stage = company.data.companyInfo.stage;
    const outcome = company.expectedOutcome;
    
    // Generate realistic product metrics based on stage and outcome
    const productData = {
      dailyActiveUsers: outcome === 'pass' ? (stage === 'series-c' ? 50000 : stage === 'series-b' ? 20000 : stage === 'series-a' ? 5000 : 1000) : 500,
      monthlyActiveUsers: outcome === 'pass' ? (stage === 'series-c' ? 200000 : stage === 'series-b' ? 80000 : stage === 'series-a' ? 20000 : 5000) : 2000,
      retentionRate: outcome === 'pass' ? 85 : outcome === 'conditional' ? 70 : 50,
      productMarketFitScore: outcome === 'pass' ? 4 : outcome === 'conditional' ? 3 : 2,
      featureAdoptionRate: outcome === 'pass' ? 80 : outcome === 'conditional' ? 60 : 40,
      userEngagementScore: outcome === 'pass' ? 4 : outcome === 'conditional' ? 3 : 2,
      timeToValueDays: outcome === 'pass' ? 3 : outcome === 'conditional' ? 7 : 14,
      productStickiness: outcome === 'pass' ? 40 : outcome === 'conditional' ? 25 : 15,
      activationRate: outcome === 'pass' ? 70 : outcome === 'conditional' ? 50 : 30,
      customerLifetimeValue: outcome === 'pass' ? (stage === 'series-c' ? 50000 : stage === 'series-b' ? 25000 : 10000) : 5000,
      averageDealSize: outcome === 'pass' ? (stage === 'series-c' ? 20000 : stage === 'series-b' ? 10000 : 5000) : 2000,
      customerSatisfactionScore: outcome === 'pass' ? 8.5 : outcome === 'conditional' ? 7 : 5.5,
      salesCycleDays: outcome === 'pass' ? 30 : outcome === 'conditional' ? 45 : 60,
      grossMargin: outcome === 'pass' ? 75 : outcome === 'conditional' ? 60 : 40,
      revenueGrowthRate: outcome === 'pass' ? 150 : outcome === 'conditional' ? 50 : 10,
      capitalEfficiencyScore: outcome === 'pass' ? 4 : outcome === 'conditional' ? 3 : 2,
    };
    
    // Directly use the sample data without mapping since forms now match the structure
    updateData({
      companyInfo: company.data.companyInfo,
      capital: company.data.capital,
      advantage: company.data.advantage,
      market: company.data.market,
      product: productData,
      people: company.data.people
    });
    
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