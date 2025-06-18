// DeepSeek Framework Generator - Uses AI to create detailed framework database
// Generates 500+ frameworks with full methodology and implementation details

import { Framework, FrameworkCategory, VisualizationType } from './strategicFrameworkDatabase';

// DeepSeek API configuration (using existing key)
const DEEPSEEK_API_URL = process.env.REACT_APP_DEEPSEEK_API_URL || 'https://api.deepseek.com/v1/chat/completions';
const DEEPSEEK_API_KEY = process.env.REACT_APP_DEEPSEEK_API_KEY || 'sk-f68b7148243e4663a31386a5ea6093cf';

interface DeepSeekResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

// Call DeepSeek API
async function callDeepSeek(prompt: string): Promise<string> {
  try {
    const response = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'system',
            content: 'You are a PhD-level business strategy expert with deep knowledge of all business frameworks.'
          },
          {
            role: 'user',
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      throw new Error(`DeepSeek API error: ${response.statusText}`);
    }

    const data: DeepSeekResponse = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error('DeepSeek API call failed:', error);
    // Fallback to mock data in development
    return 'Mock framework data';
  }
}

// Generate comprehensive framework list by category
export async function generateFrameworksByCategory(
  category: FrameworkCategory,
  count: number = 35
): Promise<string[]> {
  const prompt = `
    As a business strategy expert, list exactly ${count} ${category} frameworks.
    
    Requirements:
    1. Include both classic and modern frameworks
    2. Cover different industries and company stages
    3. Mix well-known and lesser-known but valuable frameworks
    4. Include frameworks from:
       - Top consulting firms (McKinsey, BCG, Bain, etc.)
       - Academic research
       - Industry practitioners
       - Startup ecosystem
    
    Format each as:
    [Framework Name] | [Origin/Author] | [Year] | [Brief Purpose]
    
    Category: ${category}
  `;

  const response = await callDeepSeek(prompt);
  
  // Parse response into framework names
  return response.split('\n')
    .filter(line => line.includes('|'))
    .map(line => {
      const parts = line.split('|');
      return parts[0].trim().replace(/^\[|\]$/g, '');
    });
}

// Generate detailed framework specification
export async function generateFrameworkDetails(
  name: string,
  category: FrameworkCategory
): Promise<Framework> {
  const prompt = `
    Create a comprehensive specification for the "${name}" framework in the ${category} category.
    
    Provide detailed information in JSON format with this exact structure:
    {
      "id": "snake_case_id",
      "name": "${name}",
      "category": "${category}",
      "subcategory": "specific subcategory",
      "description": "one paragraph description",
      "purpose": "primary purpose and value",
      
      "origin": {
        "author": "person or organization",
        "year": number,
        "source": "publication or company",
        "academicPaper": "paper title if applicable",
        "company": "company if applicable"
      },
      
      "applicability": {
        "stages": ["pre_seed", "seed", "series_a", "series_b", "growth", "mature"],
        "industries": ["saas", "marketplace", "fintech", etc or "all"],
        "companySize": { "min": number, "max": number },
        "situations": ["growth", "turnaround", "pivot", "scale", etc],
        "geographies": ["global", "us", "europe", "asia"]
      },
      
      "methodology": {
        "overview": "how the framework works",
        "requiredMetrics": [
          {
            "flashField": "exact FLASH field name",
            "alternativeFields": ["backup fields"],
            "importance": "required|recommended|optional",
            "description": "what this metric represents"
          }
        ],
        "calculationSteps": [
          {
            "id": "step_id",
            "name": "Step Name",
            "formula": "mathematical formula or logic",
            "inputs": ["input variables"],
            "output": "output variable",
            "unit": "%, $, score, etc"
          }
        ],
        "interpretationRules": [
          {
            "condition": "logical condition",
            "position": "resulting position/state",
            "description": "what this means",
            "implications": ["implication 1", "implication 2"],
            "recommendations": ["recommendation 1", "recommendation 2"]
          }
        ],
        "timeToComplete": "X minutes/hours"
      },
      
      "visualization": {
        "type": "matrix_2x2|spider|canvas|pyramid|funnel|etc",
        "axes": {
          "x": { "label": "X axis label", "min": 0, "max": 100 },
          "y": { "label": "Y axis label", "min": 0, "max": 100 }
        },
        "segments": [
          {
            "id": "segment_id",
            "label": "Segment Name",
            "description": "what this segment means",
            "color": "#HEX"
          }
        ]
      },
      
      "insights": {
        "whenMostPowerful": "ideal use case",
        "limitations": ["limitation 1", "limitation 2"],
        "commonMisuses": ["misuse 1", "misuse 2"],
        "bestPractices": ["practice 1", "practice 2"],
        "academicValidation": "research backing"
      },
      
      "implementation": {
        "prerequisites": ["prerequisite 1", "prerequisite 2"],
        "steps": ["step 1", "step 2", "step 3"],
        "deliverables": ["deliverable 1", "deliverable 2"],
        "typicalDuration": "X days/weeks",
        "requiredResources": ["resource 1", "resource 2"]
      },
      
      "relatedFrameworks": [
        {
          "id": "framework_id",
          "relationship": "complementary|alternative|prerequisite|advanced",
          "description": "how they relate"
        }
      ],
      
      "cases": [
        {
          "company": "Company Name",
          "industry": "Industry",
          "stage": "Stage",
          "situation": "challenge faced",
          "application": "how framework was used",
          "outcome": "results achieved",
          "keyLearning": "main takeaway"
        }
      ],
      
      "metadata": {
        "popularity": 1-10,
        "complexity": "basic|intermediate|advanced|expert",
        "evidenceStrength": "theoretical|empirical|proven",
        "lastUpdated": "2024-01-01",
        "tags": ["tag1", "tag2", "tag3"]
      }
    }
    
    IMPORTANT: 
    - Use only these FLASH fields: funding_stage, total_capital_raised_usd, cash_on_hand_usd, monthly_burn_usd, runway_months, annual_revenue_run_rate, revenue_growth_rate_percent, gross_margin_percent, burn_multiple, ltv_cac_ratio, investor_tier_primary, has_debt, patent_count, network_effects_present, has_data_moat, regulatory_advantage_present, tech_differentiation_score, switching_cost_score, brand_strength_score, scalability_score, product_stage, product_retention_30d, product_retention_90d, sector, tam_size_usd, sam_size_usd, som_size_usd, market_growth_rate_percent, customer_count, customer_concentration_percent, user_growth_rate_percent, net_dollar_retention_percent, competition_intensity, competitors_named_count, dau_mau_ratio, founders_count, team_size_full_time, years_experience_avg, domain_expertise_years_avg, prior_startup_experience_count, prior_successful_exits_count, board_advisor_experience_score, advisors_count, team_diversity_percent, key_person_dependency
    - Provide specific, actionable content
    - Include real formulas where applicable
    - Make it immediately usable
  `;

  const response = await callDeepSeek(prompt);
  
  try {
    // Parse JSON response
    const frameworkData = JSON.parse(response);
    
    // Ensure date is properly formatted
    frameworkData.metadata.lastUpdated = new Date(frameworkData.metadata.lastUpdated);
    
    return frameworkData as Framework;
  } catch (error) {
    console.error('Failed to parse framework JSON:', error);
    // Return a minimal framework structure as fallback
    return createFallbackFramework(name, category);
  }
}

// Create fallback framework if AI generation fails
function createFallbackFramework(name: string, category: FrameworkCategory): Framework {
  const id = name.toLowerCase().replace(/[^a-z0-9]/g, '_');
  
  return {
    id,
    name,
    category,
    description: `${name} framework for ${category.toLowerCase()} analysis`,
    purpose: `Analyze and improve ${category.toLowerCase()} performance`,
    
    origin: {
      author: 'Unknown',
      year: 2020,
      source: 'Industry Practice'
    },
    
    applicability: {
      stages: ['all'],
      industries: ['all'],
      companySize: { min: 1, max: 10000 },
      situations: ['general']
    },
    
    methodology: {
      overview: `Apply ${name} methodology to analyze current state`,
      requiredMetrics: [],
      calculationSteps: [],
      interpretationRules: [],
      timeToComplete: '30 minutes'
    },
    
    visualization: {
      type: VisualizationType.CANVAS,
      segments: []
    },
    
    insights: {
      whenMostPowerful: 'General analysis',
      limitations: ['Requires customization'],
      commonMisuses: ['Over-simplification'],
      bestPractices: ['Adapt to context']
    },
    
    implementation: {
      prerequisites: ['Data gathering'],
      steps: ['Analyze', 'Interpret', 'Act'],
      deliverables: ['Analysis report'],
      typicalDuration: '1 week',
      requiredResources: ['Analysis team']
    },
    
    relatedFrameworks: [],
    cases: [],
    
    metadata: {
      popularity: 5,
      complexity: 'intermediate',
      evidenceStrength: 'theoretical',
      lastUpdated: new Date(),
      tags: [category.toLowerCase()]
    }
  };
}

// Generate frameworks for specific situations
export async function generateSituationalFrameworks(): Promise<Framework[]> {
  const situations = [
    { situation: 'hypergrowth', description: 'Scaling from $1M to $100M ARR' },
    { situation: 'pivot', description: 'Changing business model or market' },
    { situation: 'turnaround', description: 'Fixing declining business' },
    { situation: 'market_entry', description: 'Entering new market or geography' },
    { situation: 'fundraising', description: 'Preparing for investment round' },
    { situation: 'acquisition', description: 'M&A planning and integration' },
    { situation: 'platform_transition', description: 'Moving to platform model' },
    { situation: 'crisis_management', description: 'Managing through crisis' }
  ];

  const frameworks: Framework[] = [];

  for (const { situation, description } of situations) {
    const prompt = `
      List 5 most relevant frameworks for a startup in "${situation}" situation: ${description}
      
      For each framework:
      1. Why it's critical for this situation
      2. Specific adaptation needed
      3. Expected outcome
      
      Format: [Framework Name] | [Why Critical]
    `;

    const response = await callDeepSeek(prompt);
    const frameworkNames = response.split('\n')
      .filter(line => line.includes('|'))
      .map(line => line.split('|')[0].trim().replace(/^\[|\]$/g, ''));

    for (const name of frameworkNames) {
      const framework = await generateFrameworkDetails(name, FrameworkCategory.STRATEGY);
      framework.applicability.situations.push(situation);
      frameworks.push(framework);
    }
  }

  return frameworks;
}

// Generate industry-specific frameworks
export async function generateIndustryFrameworks(): Promise<Framework[]> {
  const industries = [
    'saas', 'marketplace', 'fintech', 'healthtech', 'edtech',
    'ecommerce', 'gaming', 'social', 'deeptech', 'biotech'
  ];

  const frameworks: Framework[] = [];

  for (const industry of industries) {
    const prompt = `
      List 5 frameworks specifically designed for ${industry} companies.
      Include metrics, growth models, and operational frameworks unique to ${industry}.
      
      Format: [Framework Name] | [${industry} Focus]
    `;

    const response = await callDeepSeek(prompt);
    const frameworkNames = response.split('\n')
      .filter(line => line.includes('|'))
      .map(line => line.split('|')[0].trim().replace(/^\[|\]$/g, ''));

    for (const name of frameworkNames) {
      const framework = await generateFrameworkDetails(
        name, 
        FrameworkCategory.OPERATIONAL
      );
      framework.applicability.industries = [industry];
      frameworks.push(framework);
    }
  }

  return frameworks;
}

// Master framework generation orchestrator
export async function generateCompleteFrameworkDatabase(): Promise<Framework[]> {
  console.log('🚀 Starting AI-powered framework generation...');
  
  const allFrameworks: Framework[] = [];
  let totalGenerated = 0;

  // Phase 1: Generate by category (15 categories × 35 frameworks = 525 frameworks)
  for (const category of Object.values(FrameworkCategory)) {
    console.log(`\n📚 Generating ${category} frameworks...`);
    
    try {
      const frameworkNames = await generateFrameworksByCategory(category as FrameworkCategory, 35);
      
      for (const name of frameworkNames) {
        try {
          console.log(`  ⚙️ Generating details for: ${name}`);
          const framework = await generateFrameworkDetails(name, category as FrameworkCategory);
          allFrameworks.push(framework);
          totalGenerated++;
          
          // Rate limiting - wait 100ms between API calls
          await new Promise(resolve => setTimeout(resolve, 100));
        } catch (error) {
          console.error(`  ❌ Failed to generate ${name}:`, error);
        }
      }
    } catch (error) {
      console.error(`❌ Failed to generate ${category} frameworks:`, error);
    }
  }

  // Phase 2: Add situational frameworks
  console.log('\n🎯 Generating situational frameworks...');
  try {
    const situationalFrameworks = await generateSituationalFrameworks();
    allFrameworks.push(...situationalFrameworks);
    totalGenerated += situationalFrameworks.length;
  } catch (error) {
    console.error('❌ Failed to generate situational frameworks:', error);
  }

  // Phase 3: Add industry-specific frameworks
  console.log('\n🏭 Generating industry-specific frameworks...');
  try {
    const industryFrameworks = await generateIndustryFrameworks();
    allFrameworks.push(...industryFrameworks);
    totalGenerated += industryFrameworks.length;
  } catch (error) {
    console.error('❌ Failed to generate industry frameworks:', error);
  }

  console.log(`\n✅ Generation complete! Total frameworks: ${totalGenerated}`);
  
  // Remove duplicates based on ID
  const uniqueFrameworks = Array.from(
    new Map(allFrameworks.map(f => [f.id, f])).values()
  );

  console.log(`📊 Unique frameworks after deduplication: ${uniqueFrameworks.length}`);
  
  return uniqueFrameworks;
}

// Save frameworks to file (for backup/caching)
export async function saveFrameworksToFile(frameworks: Framework[]): Promise<void> {
  const dataStr = JSON.stringify(frameworks, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = 'strategic_frameworks_database.json';
  link.click();
  
  URL.revokeObjectURL(url);
  console.log('📁 Framework database saved to file');
}

// Load frameworks from file
export async function loadFrameworksFromFile(file: File): Promise<Framework[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const frameworks = JSON.parse(e.target?.result as string);
        // Convert date strings back to Date objects
        frameworks.forEach((f: any) => {
          f.metadata.lastUpdated = new Date(f.metadata.lastUpdated);
        });
        resolve(frameworks);
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = reject;
    reader.readAsText(file);
  });
}