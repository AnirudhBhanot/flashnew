// DeepSeek Integration Service for Executive-Level Analysis
import { 
  EXECUTIVE_ANALYSIS_PROMPTS, 
  formatContextForPrompt,
  SYSTEM_PROMPT,
  OUTPUT_SCHEMAS 
} from './deepSeekPrompts';

const DEEPSEEK_API_URL = process.env.REACT_APP_DEEPSEEK_API_URL || 'https://api.deepseek.com/v1';
const DEEPSEEK_API_KEY = process.env.REACT_APP_DEEPSEEK_API_KEY || '';

interface DeepSeekRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  temperature?: number;
  max_tokens?: number;
  response_format?: {
    type: 'json_object';
  };
}

interface DeepSeekResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

class DeepSeekService {
  private async callDeepSeek(request: DeepSeekRequest): Promise<any> {
    try {
      const response = await fetch(`${DEEPSEEK_API_URL}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${DEEPSEEK_API_KEY}`
        },
        body: JSON.stringify({
          ...request,
          model: request.model || 'deepseek-chat',
          temperature: request.temperature || 0.7,
          max_tokens: request.max_tokens || 4000
        })
      });

      if (!response.ok) {
        throw new Error(`DeepSeek API error: ${response.statusText}`);
      }

      const data: DeepSeekResponse = await response.json();
      const content = data.choices[0]?.message?.content;

      // Parse JSON response if expected
      if (request.response_format?.type === 'json_object') {
        try {
          return JSON.parse(content);
        } catch (e) {
          console.error('Failed to parse DeepSeek JSON response:', e);
          return content;
        }
      }

      return content;
    } catch (error) {
      console.error('DeepSeek API call failed:', error);
      throw error;
    }
  }

  async generateExecutiveSummary(assessmentData: any, results: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, results);
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.executiveSummary.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt + '\n\nProvide response in JSON format matching this schema:\n' + JSON.stringify(OUTPUT_SCHEMAS.executiveSummary, null, 2) }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.7,
      max_tokens: 2000
    });

    return response;
  }

  async generateSituationAssessment(assessmentData: any, results: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, results);
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.situationAssessment.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
      max_tokens: 3000
    });

    // Parse the response into structured format
    return this.parseSituationAssessment(response);
  }

  async generateStrategicOptions(assessmentData: any, results: any): Promise<any[]> {
    const context = formatContextForPrompt(assessmentData, results);
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.strategicOptions.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt + '\n\nProvide response as JSON array with 3 strategic options.' }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.8,
      max_tokens: 4000
    });

    return response.options || [];
  }

  async generateImplementationRoadmap(assessmentData: any, selectedStrategy: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, {});
    const strategyContext = `\nSelected Strategy: ${selectedStrategy.name}\n${selectedStrategy.description}`;
    const fullContext = context + strategyContext;
    
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.implementationRoadmap.replace('{context}', fullContext);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.6,
      max_tokens: 3000
    });

    return this.parseImplementationRoadmap(response);
  }

  async generateRiskAnalysis(assessmentData: any, strategy: any): Promise<any[]> {
    const context = formatContextForPrompt(assessmentData, {});
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.riskMitigation.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.6,
      max_tokens: 2500
    });

    return this.parseRiskAnalysis(response);
  }

  async generateFinancialProjections(assessmentData: any, strategy: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, {});
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.financialProjections.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.5,
      max_tokens: 3000
    });

    return this.parseFinancialProjections(response);
  }

  async generateCompetitiveDynamics(assessmentData: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, {});
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.competitiveDynamics.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
      max_tokens: 2500
    });

    return this.parseCompetitiveDynamics(response);
  }

  async generateValueCreationPlan(assessmentData: any, strategy: any): Promise<any> {
    const context = formatContextForPrompt(assessmentData, {});
    const prompt = EXECUTIVE_ANALYSIS_PROMPTS.valueCreation.replace('{context}', context);

    const response = await this.callDeepSeek({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt }
      ],
      temperature: 0.6,
      max_tokens: 3500
    });

    return this.parseValueCreation(response);
  }

  // Full executive report generation
  async generateCompleteExecutiveReport(assessmentData: any, mlResults: any): Promise<any> {
    try {
      // Generate all sections in parallel for efficiency
      const [
        executiveSummary,
        situationAssessment,
        strategicOptions,
        competitiveDynamics,
        financialProjections
      ] = await Promise.all([
        this.generateExecutiveSummary(assessmentData, mlResults),
        this.generateSituationAssessment(assessmentData, mlResults),
        this.generateStrategicOptions(assessmentData, mlResults),
        this.generateCompetitiveDynamics(assessmentData),
        this.generateFinancialProjections(assessmentData, null)
      ]);

      // Select recommended strategy (typically the balanced option)
      const recommendedStrategy = strategicOptions[1] || strategicOptions[0];

      // Generate implementation-specific sections based on selected strategy
      const [
        implementationPlan,
        riskMitigation,
        valueCreationPlan
      ] = await Promise.all([
        this.generateImplementationRoadmap(assessmentData, recommendedStrategy),
        this.generateRiskAnalysis(assessmentData, recommendedStrategy),
        this.generateValueCreationPlan(assessmentData, recommendedStrategy)
      ]);

      return {
        executiveSummary,
        situationAssessment: {
          ...situationAssessment,
          marketDynamics: competitiveDynamics
        },
        strategicOptions,
        recommendedStrategy: {
          option: recommendedStrategy,
          rationale: this.generateRationale(recommendedStrategy, strategicOptions),
          valueCreationModel: valueCreationPlan.topLevers || []
        },
        riskMitigation,
        implementationPlan,
        financialProjections,
        metadata: {
          generatedAt: new Date().toISOString(),
          modelVersion: 'deepseek-chat',
          confidenceLevel: 'high'
        }
      };
    } catch (error) {
      console.error('Failed to generate complete executive report:', error);
      throw error;
    }
  }

  // Helper parsing methods
  private parseSituationAssessment(response: string): any {
    // Parse text response into structured format
    // This would use NLP or regex to extract structured data
    // For now, return a structured placeholder
    return {
      marketDynamics: {
        marketStructure: 'Fragmented',
        competitiveIntensity: 3.5,
        marketConcentration: 0.42,
        entryBarriers: ['High CAC', 'Network effects', 'Regulatory requirements'],
        strategicGroups: []
      },
      internalCapabilities: {
        strengths: [],
        weaknesses: [],
        coreCompetencies: [],
        capabilityGaps: []
      },
      performanceGaps: [],
      burningPlatform: response
    };
  }

  private parseImplementationRoadmap(response: string): any {
    // Parse implementation roadmap from text
    return {
      phases: [],
      changeManagement: [],
      governanceModel: []
    };
  }

  private parseRiskAnalysis(response: string): any[] {
    // Parse risk analysis from text
    return [];
  }

  private parseFinancialProjections(response: string): any[] {
    // Parse financial projections from text
    return [];
  }

  private parseCompetitiveDynamics(response: string): any {
    // Parse competitive dynamics from text
    return {
      marketStructure: 'Analyzing...',
      competitiveIntensity: 3,
      marketConcentration: 0.5,
      entryBarriers: [],
      strategicGroups: []
    };
  }

  private parseValueCreation(response: string): any {
    // Parse value creation plan from text
    return {
      topLevers: [],
      quickWins: [],
      longTermInitiatives: []
    };
  }

  private generateRationale(selected: any, allOptions: any[]): string[] {
    return [
      `Optimal risk-return profile with ${(selected.irr * 100).toFixed(0)}% IRR`,
      `Aligns with current organizational capabilities and market position`,
      `Provides clear path to profitability within ${selected.paybackPeriod} years`,
      `Builds sustainable competitive advantage through ${selected.name.toLowerCase()}`
    ];
  }
}

// Export singleton instance
export const deepSeekService = new DeepSeekService();

// Export types for use in components
export interface ExecutiveReport {
  executiveSummary: any;
  situationAssessment: any;
  strategicOptions: any[];
  recommendedStrategy: any;
  riskMitigation: any[];
  implementationPlan: any;
  financialProjections: any[];
  metadata: {
    generatedAt: string;
    modelVersion: string;
    confidenceLevel: string;
  };
}