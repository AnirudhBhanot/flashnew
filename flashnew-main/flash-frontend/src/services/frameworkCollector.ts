// Framework Collection System - Automated gathering of 500+ frameworks
// Uses DeepSeek and web scraping to build comprehensive database

import { Framework, FrameworkCategory, VisualizationType, FrameworkOrigin } from './strategicFrameworkDatabase';

// Framework sources to mine
const FRAMEWORK_SOURCES = {
  consultingFirms: [
    { name: 'McKinsey', frameworks: ['7S', 'Three Horizons', 'GE Matrix'] },
    { name: 'BCG', frameworks: ['Growth-Share Matrix', 'Experience Curve', 'Time-Based Competition'] },
    { name: 'Bain', frameworks: ['Net Promoter Score', 'Customer Loyalty', 'RAPID'] },
    { name: 'Porter', frameworks: ['Five Forces', 'Value Chain', 'Generic Strategies'] }
  ],
  
  academicFrameworks: [
    { category: 'Innovation', count: 50 },
    { category: 'Strategy', count: 75 },
    { category: 'Operations', count: 40 },
    { category: 'Marketing', count: 60 },
    { category: 'Finance', count: 45 }
  ],
  
  startupFrameworks: [
    { source: 'Lean Startup', frameworks: ['Build-Measure-Learn', 'MVP', 'Pivot'] },
    { source: 'Y Combinator', frameworks: ['Product-Market Fit', 'Do Things That Don\'t Scale'] },
    { source: 'Blitzscaling', frameworks: ['Lightning', 'Thunder', 'Blitzscaling Framework'] }
  ],
  
  digitalFrameworks: [
    { category: 'Platform', frameworks: ['Network Effects', 'Chicken-Egg', 'Platform Stack'] },
    { category: 'SaaS', frameworks: ['Rule of 40', 'Magic Number', 'Quick Ratio'] },
    { category: 'Marketplace', frameworks: ['Liquidity', 'Take Rate', 'GMV Analysis'] }
  ]
};

// Framework template generator using DeepSeek
export async function generateFrameworkDetails(
  name: string, 
  category: string,
  context: string = ''
): Promise<Partial<Framework>> {
  const prompt = `
    Generate a comprehensive business framework analysis for: ${name}
    Category: ${category}
    ${context ? `Context: ${context}` : ''}
    
    Provide in the following structure:
    1. Origin (author, year, source)
    2. Purpose and description
    3. When to use (stages, industries, situations)
    4. Methodology (steps, calculations, metrics needed)
    5. Interpretation rules
    6. Visualization type
    7. Real-world case examples
    8. Limitations and best practices
    9. Related frameworks
    
    Be specific and practical. Include formulas where applicable.
  `;
  
  // This would call DeepSeek API
  // For now, returning mock structure
  return {
    name,
    category: FrameworkCategory.STRATEGY,
    description: `${name} framework for strategic analysis`,
    purpose: `Analyze and improve ${category.toLowerCase()} performance`
  };
}

// Batch framework generator
export async function generateFrameworkBatch(
  category: FrameworkCategory,
  count: number = 10
): Promise<Partial<Framework>[]> {
  const categoryPrompts: Record<FrameworkCategory, string> = {
    [FrameworkCategory.STRATEGY]: `
      List ${count} strategic planning frameworks used by consultants and businesses.
      Include both classic (Porter, BCG) and modern (Blue Ocean, Platform) frameworks.
      Focus on frameworks that help with competitive positioning and strategic choices.
    `,
    [FrameworkCategory.INNOVATION]: `
      List ${count} innovation frameworks used by startups and R&D departments.
      Include frameworks for ideation, validation, and commercialization.
      Cover both incremental and disruptive innovation approaches.
    `,
    [FrameworkCategory.GROWTH]: `
      List ${count} growth frameworks used by high-growth companies.
      Include viral growth, paid acquisition, retention, and expansion frameworks.
      Cover B2B and B2C growth strategies.
    `,
    [FrameworkCategory.FINANCIAL]: `
      List ${count} financial analysis frameworks for startups and enterprises.
      Include valuation, unit economics, and financial planning frameworks.
      Cover both early-stage metrics and mature company analysis.
    `,
    [FrameworkCategory.OPERATIONAL]: `
      List ${count} operational excellence frameworks.
      Include lean, agile, six sigma, and modern DevOps frameworks.
      Cover both manufacturing and digital operations.
    `,
    [FrameworkCategory.MARKETING]: `
      List ${count} marketing strategy frameworks.
      Include positioning, branding, digital marketing, and growth hacking.
      Cover both traditional and modern digital approaches.
    `,
    [FrameworkCategory.PRODUCT]: `
      List ${count} product management frameworks.
      Include discovery, prioritization, roadmapping, and launch frameworks.
      Cover both B2B and B2C product strategies.
    `,
    [FrameworkCategory.LEADERSHIP]: `
      List ${count} leadership and management frameworks.
      Include team building, culture, performance management, and change.
      Cover both startup and enterprise contexts.
    `,
    [FrameworkCategory.ORGANIZATIONAL]: `
      List ${count} organizational design frameworks.
      Include structure, culture, transformation, and scaling frameworks.
      Cover both traditional hierarchies and modern flat organizations.
    `,
    [FrameworkCategory.TRANSFORMATION]: `
      List ${count} business transformation frameworks.
      Include digital transformation, turnaround, and change management.
      Cover both crisis and growth-driven transformations.
    `,
    [FrameworkCategory.COMPETITIVE]: `
      List ${count} competitive analysis frameworks.
      Include market analysis, competitor tracking, and positioning.
      Cover both direct competition and ecosystem analysis.
    `,
    [FrameworkCategory.CUSTOMER]: `
      List ${count} customer analysis frameworks.
      Include segmentation, journey mapping, and experience design.
      Cover both acquisition and retention strategies.
    `,
    [FrameworkCategory.RISK]: `
      List ${count} risk management frameworks.
      Include financial, operational, strategic, and cyber risk.
      Cover both prevention and mitigation strategies.
    `,
    [FrameworkCategory.TECHNOLOGY]: `
      List ${count} technology strategy frameworks.
      Include architecture, adoption, and digital strategy frameworks.
      Cover both IT management and product technology.
    `,
    [FrameworkCategory.SUSTAINABILITY]: `
      List ${count} sustainability and ESG frameworks.
      Include environmental, social, and governance frameworks.
      Cover both reporting and strategic integration.
    `
  };
  
  const prompt = categoryPrompts[category] + `
    
    For each framework provide:
    - Name
    - Brief description
    - Origin (author/company)
    - Key use case
    - Why it's powerful
  `;
  
  // This would call DeepSeek to generate framework list
  // Then for each framework, call generateFrameworkDetails
  
  const frameworks: Partial<Framework>[] = [];
  // Batch processing logic here
  
  return frameworks;
}

// Mining existing framework collections
export async function mineFrameworksFromSource(source: string): Promise<Partial<Framework>[]> {
  const miningPrompts: Record<string, string> = {
    'consulting': `
      Extract all strategic frameworks used by top consulting firms.
      Include McKinsey, BCG, Bain, Deloitte, Accenture, etc.
      Focus on their proprietary and commonly used frameworks.
    `,
    'academic': `
      Extract business frameworks from academic literature.
      Include Harvard Business Review, MIT Sloan, Wharton, INSEAD.
      Focus on empirically validated frameworks.
    `,
    'startup': `
      Extract frameworks used in the startup ecosystem.
      Include YC, Techstars, 500 Startups, First Round Capital.
      Focus on practical, implementation-oriented frameworks.
    `,
    'industry': `
      Extract industry-specific frameworks.
      Include SaaS, marketplace, fintech, healthcare, retail frameworks.
      Focus on metrics and operational frameworks.
    `
  };
  
  // Implementation would scrape or use DeepSeek to extract
  return [];
}

// Framework validator
export function validateFramework(framework: Partial<Framework>): string[] {
  const errors: string[] = [];
  
  if (!framework.name) errors.push('Framework name is required');
  if (!framework.category) errors.push('Framework category is required');
  if (!framework.description) errors.push('Framework description is required');
  if (!framework.methodology?.requiredMetrics) errors.push('Required metrics must be specified');
  if (!framework.visualization?.type) errors.push('Visualization type must be specified');
  
  // Check if metrics map to FLASH fields
  framework.methodology?.requiredMetrics?.forEach(metric => {
    if (!isValidFlashField(metric.flashField)) {
      errors.push(`Invalid FLASH field: ${metric.flashField}`);
    }
  });
  
  return errors;
}

function isValidFlashField(field: string): boolean {
  const validFields = [
    'funding_stage', 'total_capital_raised_usd', 'cash_on_hand_usd',
    'monthly_burn_usd', 'runway_months', 'annual_revenue_run_rate',
    'revenue_growth_rate_percent', 'gross_margin_percent', 'burn_multiple',
    'ltv_cac_ratio', 'investor_tier_primary', 'has_debt', 'patent_count',
    'network_effects_present', 'has_data_moat', 'regulatory_advantage_present',
    'tech_differentiation_score', 'switching_cost_score', 'brand_strength_score',
    'scalability_score', 'product_stage', 'product_retention_30d',
    'product_retention_90d', 'sector', 'tam_size_usd', 'sam_size_usd',
    'som_size_usd', 'market_growth_rate_percent', 'customer_count',
    'customer_concentration_percent', 'user_growth_rate_percent',
    'net_dollar_retention_percent', 'competition_intensity',
    'competitors_named_count', 'dau_mau_ratio', 'founders_count',
    'team_size_full_time', 'years_experience_avg', 'domain_expertise_years_avg',
    'prior_startup_experience_count', 'prior_successful_exits_count',
    'board_advisor_experience_score', 'advisors_count', 'team_diversity_percent',
    'key_person_dependency'
  ];
  
  return validFields.includes(field);
}

// Framework enrichment with examples
export async function enrichFrameworkWithExamples(
  framework: Partial<Framework>
): Promise<Partial<Framework>> {
  const prompt = `
    Provide 3 real-world case examples for the ${framework.name} framework:
    
    For each case include:
    - Company name and industry
    - Stage when framework was applied
    - Specific situation/challenge
    - How the framework was applied
    - Outcome achieved
    - Key learning
    
    Focus on well-known companies and documented cases.
  `;
  
  // Call DeepSeek to generate examples
  // Add to framework.cases
  
  return framework;
}

// Cross-reference framework relationships
export async function identifyFrameworkRelationships(
  framework: Framework,
  allFrameworks: Framework[]
): Promise<Framework> {
  const relatedFrameworks = allFrameworks
    .filter(f => f.id !== framework.id)
    .map(f => ({
      framework: f,
      similarity: calculateFrameworkSimilarity(framework, f)
    }))
    .filter(r => r.similarity > 0.3)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, 5)
    .map(r => ({
      id: r.framework.id,
      relationship: determineRelationship(framework, r.framework) as any,
      description: generateRelationshipDescription(framework, r.framework)
    }));
  
  return {
    ...framework,
    relatedFrameworks
  };
}

function calculateFrameworkSimilarity(f1: Framework, f2: Framework): number {
  let similarity = 0;
  
  // Same category
  if (f1.category === f2.category) similarity += 0.3;
  
  // Overlapping applicable stages
  const stageOverlap = f1.applicability.stages.filter(s => 
    f2.applicability.stages.includes(s)
  ).length / f1.applicability.stages.length;
  similarity += stageOverlap * 0.2;
  
  // Similar situations
  const situationOverlap = f1.applicability.situations.filter(s => 
    f2.applicability.situations.includes(s)
  ).length / f1.applicability.situations.length;
  similarity += situationOverlap * 0.3;
  
  // Similar complexity
  if (f1.metadata.complexity === f2.metadata.complexity) similarity += 0.2;
  
  return similarity;
}

function determineRelationship(f1: Framework, f2: Framework): string {
  // Logic to determine if complementary, alternative, prerequisite, or advanced
  if (f1.metadata.complexity === 'basic' && f2.metadata.complexity === 'advanced') {
    return 'advanced';
  }
  if (f1.category === f2.category) {
    return 'alternative';
  }
  return 'complementary';
}

function generateRelationshipDescription(f1: Framework, f2: Framework): string {
  return `${f2.name} can be used alongside ${f1.name} for comprehensive analysis`;
}

// Master collection orchestrator
export async function buildFrameworkDatabase(): Promise<Framework[]> {
  console.log('Starting framework collection...');
  
  const frameworks: Framework[] = [];
  
  // Phase 1: Generate by category
  for (const category of Object.values(FrameworkCategory)) {
    console.log(`Generating ${category} frameworks...`);
    const categoryFrameworks = await generateFrameworkBatch(category as FrameworkCategory, 35);
    
    // Validate and enrich each framework
    for (const framework of categoryFrameworks) {
      const errors = validateFramework(framework);
      if (errors.length === 0) {
        const enriched = await enrichFrameworkWithExamples(framework);
        frameworks.push(enriched as Framework);
      }
    }
  }
  
  // Phase 2: Mine from sources
  const sources = ['consulting', 'academic', 'startup', 'industry'];
  for (const source of sources) {
    console.log(`Mining frameworks from ${source}...`);
    const minedFrameworks = await mineFrameworksFromSource(source);
    frameworks.push(...minedFrameworks as Framework[]);
  }
  
  // Phase 3: Cross-reference relationships
  console.log('Identifying framework relationships...');
  const enrichedFrameworks = await Promise.all(
    frameworks.map(f => identifyFrameworkRelationships(f, frameworks))
  );
  
  console.log(`Total frameworks collected: ${enrichedFrameworks.length}`);
  return enrichedFrameworks;
}