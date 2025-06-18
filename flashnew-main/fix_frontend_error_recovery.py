#!/usr/bin/env python3
"""
Add comprehensive error recovery to frontend FrameworkIntelligence component
"""

import os

def add_frontend_error_recovery():
    """Add error recovery to FrameworkIntelligence.tsx"""
    
    component_file = "/Users/sf/Desktop/FLASH/flash-frontend-apple/src/components/FrameworkIntelligence.tsx"
    
    print(f"Updating {component_file} with error recovery...")
    
    # Read the current component
    with open(component_file, 'r') as f:
        content = f.read()
    
    # Add import for error recovery utilities
    import_position = content.find("import styles from './FrameworkIntelligence.module.scss';")
    if import_position > -1:
        import_end = content.find('\n', import_position)
        new_imports = '''
// Error recovery utilities
const retryWithBackoff = async (
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

// Enhanced cache management
const frameworkCache = {
  set: (key: string, data: any, ttl: number = 3600000) => {
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
'''
        content = content[:import_end] + new_imports + content[import_end:]
    
    # Update fetchRecommendations to use retry and caching
    old_fetch = '''  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/recommend`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(getContext())
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch framework recommendations');
      }

      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      console.error('Framework recommendation error:', err);
      setError('Failed to load framework recommendations');'''
    
    new_fetch = '''  const fetchRecommendations = async () => {
    setIsLoading(true);
    setError(null);
    
    // Check cache first
    const cacheKey = JSON.stringify(getContext());
    const cached = frameworkCache.get(cacheKey);
    if (cached) {
      setRecommendations(cached.recommendations);
      setIsLoading(false);
      return;
    }
    
    try {
      const fetchWithRetry = async () => {
        const response = await fetch(
          `${process.env.REACT_APP_API_URL || 'http://localhost:8001'}/api/frameworks/recommend`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(getContext())
          }
        );

        if (!response.ok) {
          throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        return response.json();
      };
      
      const data = await retryWithBackoff(fetchWithRetry);
      setRecommendations(data.recommendations);
      
      // Cache successful response
      frameworkCache.set(cacheKey, data);
      
    } catch (err: any) {
      console.error('Framework recommendation error:', err);
      
      // Try to provide more specific error messages
      if (err.message.includes('fetch')) {
        setError('Unable to connect to the framework service. Please check your connection.');
      } else if (err.message.includes('timeout')) {
        setError('Request timed out. The server might be busy.');
      } else {
        setError(`Failed to load recommendations: ${err.message}`);
      }'''
    
    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch)
        print("✅ Updated fetchRecommendations with retry and caching")
    
    # Add enhanced fallback data
    enhanced_fallback = '''
      // Enhanced fallback data based on context
      const contextualFallback = getContextualFallback();
      setRecommendations(contextualFallback);'''
    
    # Find where to insert the enhanced fallback
    fallback_pos = content.find('// Set fallback data')
    if fallback_pos > -1:
        end_pos = content.find(']);', fallback_pos) + 3
        content = content[:fallback_pos] + enhanced_fallback + content[end_pos:]
    
    # Add getContextualFallback function
    contextual_fallback_fn = '''
  const getContextualFallback = () => {
    const context = getContext();
    const fallbacks = [];
    
    // Industry-specific recommendations
    if (context.industry?.toLowerCase().includes('tech') || context.industry?.toLowerCase().includes('saas')) {
      fallbacks.push({
        framework_name: "Lean Startup",
        score: 0.95,
        category: "Innovation",
        complexity: "Intermediate",
        time_to_implement: "2-3 months",
        description: "Build-Measure-Learn feedback loop for rapid validation",
        why_recommended: "Perfect for tech companies iterating quickly",
        key_benefits: ["Rapid validation", "Reduced waste", "Customer feedback"],
        implementation_tips: ["Start with MVP", "Define metrics", "Weekly iterations"]
      });
    }
    
    // Stage-specific recommendations
    if (context.company_stage === 'seed' || context.company_stage === 'pre_seed') {
      fallbacks.push({
        framework_name: "Customer Development",
        score: 0.92,
        category: "Product",
        complexity: "Basic",
        time_to_implement: "1-2 months",
        description: "Systematic approach to understanding customer needs",
        why_recommended: "Critical for early-stage validation",
        key_benefits: ["Customer insights", "Problem validation", "Solution fit"],
        implementation_tips: ["Interview 100 customers", "Document learnings", "Pivot if needed"]
      });
    }
    
    // Challenge-specific recommendations
    if (context.primary_challenge?.includes('scaling')) {
      fallbacks.push({
        framework_name: "Scaling Up (Rockefeller Habits)",
        score: 0.90,
        category: "Strategy",
        complexity: "Advanced",
        time_to_implement: "3-6 months",
        description: "Comprehensive framework for scaling businesses",
        why_recommended: "Proven system for companies ready to scale",
        key_benefits: ["Systematic growth", "Team alignment", "Execution rhythm"],
        implementation_tips: ["Start with One-Page Plan", "Daily huddles", "Quarterly themes"]
      });
    }
    
    // Always include some general frameworks
    fallbacks.push(
      {
        framework_name: "OKR Framework",
        score: 0.88,
        category: "Strategy",
        complexity: "Intermediate",
        time_to_implement: "1-2 months",
        description: "Objectives and Key Results for goal alignment",
        why_recommended: "Universal framework for any growth stage",
        key_benefits: ["Clear goals", "Measurable results", "Team alignment"],
        implementation_tips: ["Start at company level", "Cascade to teams", "Quarterly cycles"]
      },
      {
        framework_name: "SWOT Analysis",
        score: 0.85,
        category: "Strategy",
        complexity: "Basic",
        time_to_implement: "1 week",
        description: "Strategic assessment of position and opportunities",
        why_recommended: "Quick wins for strategic clarity",
        key_benefits: ["Situational awareness", "Opportunity identification", "Risk assessment"],
        implementation_tips: ["Workshop format", "Include all stakeholders", "Update quarterly"]
      }
    );
    
    return fallbacks.slice(0, 8);
  };'''
    
    # Insert before fetchRecommendations
    fetch_pos = content.find('const fetchRecommendations = async')
    if fetch_pos > -1:
        content = content[:fetch_pos] + contextual_fallback_fn + '\n\n  ' + content[fetch_pos:]
    
    # Add error recovery UI with retry
    error_ui_update = '''          {error && (
            <div className={styles.errorContainer}>
              <div className={styles.error}>
                <Icon name="exclamationmark.triangle" size={24} />
                <p>{error}</p>
              </div>
              <div className={styles.errorActions}>
                <button 
                  onClick={() => {
                    setError(null);
                    fetchRecommendations();
                  }}
                  className={styles.retryButton}
                >
                  <Icon name="arrow.clockwise" size={16} />
                  Try Again
                </button>
                <button 
                  onClick={() => {
                    setError(null);
                    const fallback = getContextualFallback();
                    setRecommendations(fallback);
                  }}
                  className={styles.fallbackButton}
                >
                  <Icon name="doc.text" size={16} />
                  Use Offline Mode
                </button>
              </div>
            </div>
          )}'''
    
    # Replace the simple error display
    simple_error = '''          {error && (
            <div className={styles.error}>
              <Icon name="exclamationmark.triangle" size={24} />
              <p>{error}</p>
            </div>
          )}'''
    
    if simple_error in content:
        content = content.replace(simple_error, error_ui_update)
        print("✅ Added enhanced error UI with retry options")
    
    # Write updated content
    with open(component_file, 'w') as f:
        f.write(content)
    
    print("✅ Frontend error recovery implementation complete")
    
    # Create CSS for error recovery UI
    css_file = "/Users/sf/Desktop/FLASH/flash-frontend-apple/src/components/FrameworkIntelligence.module.scss"
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            css_content = f.read()
        
        if '.errorContainer' not in css_content:
            error_styles = '''
.errorContainer {
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.3);
  border-radius: 12px;
  padding: 24px;
  margin: 20px 0;
}

.errorActions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.retryButton,
.fallbackButton {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retryButton {
  background: #007aff;
  color: white;
  
  &:hover {
    background: #0051d5;
    transform: translateY(-1px);
  }
}

.fallbackButton {
  background: rgba(0, 0, 0, 0.05);
  color: #000;
  
  &:hover {
    background: rgba(0, 0, 0, 0.1);
  }
}'''
            
            css_content += error_styles
            
            with open(css_file, 'w') as f:
                f.write(css_content)
            
            print("✅ Added error recovery styles")

if __name__ == "__main__":
    add_frontend_error_recovery()
    print("\n🎉 Frontend error recovery complete!")
    print("Features added:")
    print("- Retry with exponential backoff")
    print("- Local storage caching")
    print("- Contextual fallback data")
    print("- Enhanced error UI with actions")
    print("- Offline mode support")