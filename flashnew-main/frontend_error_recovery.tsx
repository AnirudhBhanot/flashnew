import React, { useState } from 'react';
import { Icon } from '../design-system/components';

// Enhanced error recovery component
export const FrameworkErrorRecovery: React.FC<{
  error: string;
  onRetry: () => void;
  onUseFallback: () => void;
}> = ({ error, onRetry, onUseFallback }) => {
  const [showDetails, setShowDetails] = useState(false);

  const getErrorMessage = (error: string) => {
    if (error.includes('fetch')) return 'Unable to connect to the framework service';
    if (error.includes('timeout')) return 'The request took too long to complete';
    if (error.includes('404')) return 'Framework data not found';
    if (error.includes('500')) return 'Server error occurred';
    return 'An unexpected error occurred';
  };

  const getErrorSuggestion = (error: string) => {
    if (error.includes('fetch') || error.includes('network')) 
      return 'Please check your internet connection and try again';
    if (error.includes('timeout')) 
      return 'The server might be busy. Please try again in a moment';
    return 'You can retry or use our cached recommendations';
  };

  return (
    <div className="error-recovery">
      <div className="error-icon">
        <Icon name="exclamationmark.triangle" size={48} />
      </div>
      
      <h3>{getErrorMessage(error)}</h3>
      <p>{getErrorSuggestion(error)}</p>
      
      <div className="error-actions">
        <button onClick={onRetry} className="primary-button">
          <Icon name="arrow.clockwise" size={16} />
          Try Again
        </button>
        
        <button onClick={onUseFallback} className="secondary-button">
          <Icon name="doc.text" size={16} />
          Use Cached Data
        </button>
      </div>
      
      <button 
        onClick={() => setShowDetails(!showDetails)}
        className="details-toggle"
      >
        {showDetails ? 'Hide' : 'Show'} Technical Details
      </button>
      
      {showDetails && (
        <div className="error-details">
          <code>{error}</code>
        </div>
      )}
    </div>
  );
};

// Enhanced fallback data with more comprehensive frameworks
export const getComprehensiveFallbackData = (context: any) => {
  const { industry = 'tech', stage = 'growth', challenges = [] } = context;
  
  // Industry-specific framework recommendations
  const industryFrameworks: Record<string, any[]> = {
    tech: [
      {
        framework_name: "Lean Startup",
        score: 0.95,
        category: "Innovation",
        complexity: "Intermediate",
        time_to_implement: "2-3 months",
        description: "Build-Measure-Learn feedback loop for rapid product development",
        why_recommended: "Essential for tech startups to validate ideas quickly",
        key_benefits: ["Reduce waste", "Faster learning", "Customer validation"],
        implementation_tips: ["Start with MVP", "Define key metrics", "Iterate based on feedback"]
      },
      {
        framework_name: "Agile Methodology",
        score: 0.92,
        category: "Operations",
        complexity: "Intermediate",
        time_to_implement: "1-2 months",
        description: "Iterative approach to software development and project management",
        why_recommended: "Industry standard for tech product development",
        key_benefits: ["Flexibility", "Continuous delivery", "Team collaboration"],
        implementation_tips: ["Start with Scrum", "Daily standups", "Sprint retrospectives"]
      }
    ],
    fintech: [
      {
        framework_name: "Regulatory Compliance Framework",
        score: 0.98,
        category: "Operations",
        complexity: "Advanced",
        time_to_implement: "3-6 months",
        description: "Comprehensive approach to financial regulations and compliance",
        why_recommended: "Critical for fintech regulatory requirements",
        key_benefits: ["Risk mitigation", "Legal compliance", "Trust building"],
        implementation_tips: ["Hire compliance officer", "Regular audits", "Document everything"]
      }
    ],
    ecommerce: [
      {
        framework_name: "Customer Journey Mapping",
        score: 0.94,
        category: "Marketing",
        complexity: "Basic",
        time_to_implement: "2-4 weeks",
        description: "Visual representation of customer experience across touchpoints",
        why_recommended: "Essential for optimizing e-commerce conversion",
        key_benefits: ["Better UX", "Higher conversion", "Reduced friction"],
        implementation_tips: ["Map current state", "Identify pain points", "Test improvements"]
      }
    ]
  };
  
  // Stage-specific frameworks
  const stageFrameworks: Record<string, any[]> = {
    seed: [
      {
        framework_name: "Product-Market Fit Framework",
        score: 0.96,
        category: "Product",
        complexity: "Intermediate",
        time_to_implement: "2-3 months",
        description: "Systematic approach to achieving product-market fit",
        why_recommended: "Critical milestone for seed stage startups",
        key_benefits: ["Clear validation", "Growth readiness", "Investor confidence"],
        implementation_tips: ["Survey users", "Track retention", "Measure NPS"]
      }
    ],
    growth: [
      {
        framework_name: "AARRR Metrics",
        score: 0.93,
        category: "Growth",
        complexity: "Basic",
        time_to_implement: "1 month",
        description: "Pirate metrics for tracking growth funnel",
        why_recommended: "Essential for measuring and optimizing growth",
        key_benefits: ["Clear metrics", "Identify bottlenecks", "Data-driven decisions"],
        implementation_tips: ["Set up analytics", "Define conversion events", "Weekly reviews"]
      }
    ]
  };
  
  // Challenge-specific frameworks
  const challengeFrameworks: Record<string, any[]> = {
    scaling: [
      {
        framework_name: "Scaling Up (Rockefeller Habits)",
        score: 0.91,
        category: "Strategy",
        complexity: "Advanced",
        time_to_implement: "3-6 months",
        description: "Comprehensive framework for scaling businesses",
        why_recommended: "Proven approach for companies in scaling phase",
        key_benefits: ["Systematic growth", "Team alignment", "Execution rhythm"],
        implementation_tips: ["Start with One-Page Plan", "Daily huddles", "Quarterly planning"]
      }
    ],
    fundraising: [
      {
        framework_name: "Investor Pitch Framework",
        score: 0.94,
        category: "Financial",
        complexity: "Intermediate",
        time_to_implement: "2-4 weeks",
        description: "Structured approach to creating compelling investor presentations",
        why_recommended: "Essential for successful fundraising",
        key_benefits: ["Clear story", "Investor alignment", "Higher success rate"],
        implementation_tips: ["10-slide deck", "Practice pitch", "Know your numbers"]
      }
    ]
  };
  
  // Combine recommendations based on context
  let recommendations = [
    ...(industryFrameworks[industry.toLowerCase()] || industryFrameworks.tech),
    ...(stageFrameworks[stage.toLowerCase()] || stageFrameworks.growth),
    ...(challengeFrameworks[challenges[0]?.toLowerCase()] || [])
  ];
  
  // Add general frameworks
  const generalFrameworks = [
    {
      framework_name: "OKR Framework",
      score: 0.88,
      category: "Strategy",
      complexity: "Intermediate",
      time_to_implement: "1-2 months",
      description: "Objectives and Key Results for goal setting and tracking",
      why_recommended: "Universal framework for alignment and execution",
      key_benefits: ["Clear goals", "Team alignment", "Measurable outcomes"],
      implementation_tips: ["Start with company OKRs", "Cascade to teams", "Quarterly cycles"]
    },
    {
      framework_name: "SWOT Analysis",
      score: 0.85,
      category: "Strategy",
      complexity: "Basic",
      time_to_implement: "1 week",
      description: "Analyze Strengths, Weaknesses, Opportunities, and Threats",
      why_recommended: "Quick strategic assessment tool",
      key_benefits: ["Situational awareness", "Strategic clarity", "Action planning"],
      implementation_tips: ["Be honest", "Involve team", "Update regularly"]
    }
  ];
  
  recommendations = [...recommendations, ...generalFrameworks];
  
  // Remove duplicates and sort by score
  const uniqueRecommendations = recommendations
    .filter((item, index, self) => 
      index === self.findIndex((t) => t.framework_name === item.framework_name)
    )
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
  
  return {
    recommendations: uniqueRecommendations,
    roadmap: generateFallbackRoadmap(uniqueRecommendations),
    combinations: generateFallbackCombinations(uniqueRecommendations)
  };
};

// Generate fallback roadmap
const generateFallbackRoadmap = (recommendations: any[]) => {
  const phases = [];
  
  // Phase 1: Foundation (Basic frameworks)
  const basicFrameworks = recommendations.filter(f => f.complexity === 'Basic');
  if (basicFrameworks.length > 0) {
    phases.push({
      phase: 1,
      duration: "1-2 months",
      frameworks: basicFrameworks.slice(0, 3).map(f => f.framework_name),
      objectives: ["Establish baseline", "Quick wins", "Build momentum"],
      success_metrics: ["Framework adoption", "Initial results", "Team buy-in"],
      dependencies: []
    });
  }
  
  // Phase 2: Core Implementation (Intermediate)
  const intermediateFrameworks = recommendations.filter(f => f.complexity === 'Intermediate');
  if (intermediateFrameworks.length > 0) {
    phases.push({
      phase: 2,
      duration: "3-4 months",
      frameworks: intermediateFrameworks.slice(0, 3).map(f => f.framework_name),
      objectives: ["Core capabilities", "Process optimization", "Scale preparation"],
      success_metrics: ["Process efficiency", "Quality metrics", "Growth indicators"],
      dependencies: phases.length > 0 ? [phases[0].frameworks[0]] : []
    });
  }
  
  // Phase 3: Advanced Implementation
  const advancedFrameworks = recommendations.filter(f => f.complexity === 'Advanced');
  if (advancedFrameworks.length > 0) {
    phases.push({
      phase: 3,
      duration: "4-6 months",
      frameworks: advancedFrameworks.slice(0, 2).map(f => f.framework_name),
      objectives: ["Strategic excellence", "Competitive advantage", "Market leadership"],
      success_metrics: ["Market position", "Financial performance", "Innovation metrics"],
      dependencies: phases.length > 0 ? [phases[phases.length - 1].frameworks[0]] : []
    });
  }
  
  return phases;
};

// Generate fallback combinations
const generateFallbackCombinations = (recommendations: any[]) => {
  const combinations = [];
  
  // Strategy + Execution combination
  const strategyFramework = recommendations.find(f => f.category === 'Strategy');
  const operationsFramework = recommendations.find(f => f.category === 'Operations');
  
  if (strategyFramework && operationsFramework) {
    combinations.push({
      frameworks: [strategyFramework.framework_name, operationsFramework.framework_name],
      synergy_score: 0.92,
      combined_benefit: "Strategic planning with operational excellence",
      implementation_order: [strategyFramework.framework_name, operationsFramework.framework_name],
      estimated_impact: "High"
    });
  }
  
  // Growth + Product combination
  const growthFramework = recommendations.find(f => f.category === 'Growth');
  const productFramework = recommendations.find(f => f.category === 'Product');
  
  if (growthFramework && productFramework) {
    combinations.push({
      frameworks: [productFramework.framework_name, growthFramework.framework_name],
      synergy_score: 0.89,
      combined_benefit: "Product-led growth strategy",
      implementation_order: [productFramework.framework_name, growthFramework.framework_name],
      estimated_impact: "High"
    });
  }
  
  // Innovation + Marketing combination
  const innovationFramework = recommendations.find(f => f.category === 'Innovation');
  const marketingFramework = recommendations.find(f => f.category === 'Marketing');
  
  if (innovationFramework && marketingFramework) {
    combinations.push({
      frameworks: [innovationFramework.framework_name, marketingFramework.framework_name],
      synergy_score: 0.85,
      combined_benefit: "Innovation-driven market approach",
      implementation_order: [innovationFramework.framework_name, marketingFramework.framework_name],
      estimated_impact: "Medium"
    });
  }
  
  return combinations.slice(0, 5);
};

// Retry with exponential backoff
export const retryWithBackoff = async (
  fn: () => Promise<any>,
  maxRetries: number = 3,
  initialDelay: number = 1000
) => {
  let lastError;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (i < maxRetries - 1) {
        const delay = initialDelay * Math.pow(2, i);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
};

// Local storage cache management
export const frameworkCache = {
  set: (key: string, data: any, ttl: number = 3600000) => { // 1 hour default
    const item = {
      data,
      timestamp: Date.now(),
      ttl
    };
    localStorage.setItem(`framework_cache_${key}`, JSON.stringify(item));
  },
  
  get: (key: string) => {
    const item = localStorage.getItem(`framework_cache_${key}`);
    if (!item) return null;
    
    const parsed = JSON.parse(item);
    const age = Date.now() - parsed.timestamp;
    
    if (age > parsed.ttl) {
      localStorage.removeItem(`framework_cache_${key}`);
      return null;
    }
    
    return parsed.data;
  },
  
  clear: () => {
    Object.keys(localStorage)
      .filter(key => key.startsWith('framework_cache_'))
      .forEach(key => localStorage.removeItem(key));
  }
};