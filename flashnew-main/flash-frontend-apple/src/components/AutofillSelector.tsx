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
    return company.data.companyInfo.fundingStage === selectedCategory;
  });

  const handleSelectCompany = (company: SampleCompany) => {
    // Create a clean company info object with proper field mapping
    const mappedCompanyInfo = {
      companyName: company.data.companyInfo.companyName,
      foundingDate: company.data.companyInfo.foundedDate,
      sector: company.data.companyInfo.industry,
      stage: company.data.companyInfo.fundingStage,
      headquarters: company.data.companyInfo.location,
      website: company.data.companyInfo.website,
      description: company.data.companyInfo.description
    };
    
    // Update each section individually since we're using CAMP structure (no product)
    updateData('companyInfo', mappedCompanyInfo);
    updateData('capital', company.data.capital);
    updateData('advantage', company.data.advantage);
    updateData('market', company.data.market);
    updateData('people', company.data.people);
    
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
          title="Sample Data"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="3" y="3" width="10" height="10" rx="2"/>
            <path d="M6 8h4M8 6v4" strokeLinecap="round"/>
          </svg>
        </button>
        {isOpen && (
          <div className={styles.floatingPanel}>
            <h3>Sample Data</h3>
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
        <span>Sample Data</span>
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