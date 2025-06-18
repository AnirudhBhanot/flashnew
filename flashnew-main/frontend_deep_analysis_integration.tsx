// Frontend integration example for Deep Framework Analysis
// Add this to your React application

import React, { useState } from 'react';
import axios from 'axios';

// Types
interface DeepAnalysisRequest {
  startup_data: any; // Your startup data interface
  framework_ids: string[];
  analysis_depth: 'quick' | 'standard' | 'comprehensive';
  include_implementation_plan: boolean;
  include_metrics: boolean;
  include_benchmarks: boolean;
}

interface FrameworkDeepAnalysis {
  framework_id: string;
  framework_name: string;
  category: string;
  position: string;
  score: number;
  detailed_analysis: any;
  implementation_plan?: any;
  success_metrics?: any[];
  industry_benchmarks?: any;
  strategic_recommendations: string[];
  risk_factors: any[];
  expected_outcomes: any;
}

interface DeepAnalysisResponse {
  startup_name: string;
  analysis_date: string;
  executive_summary: string;
  framework_analyses: FrameworkDeepAnalysis[];
  integrated_insights: any;
  prioritized_actions: any[];
  implementation_roadmap: any;
  success_probability: number;
  key_risks: any[];
  monitoring_plan: any;
}

// API Service
class DeepAnalysisService {
  private baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

  async performDeepAnalysis(request: DeepAnalysisRequest): Promise<DeepAnalysisResponse> {
    const response = await axios.post(`${this.baseURL}/api/frameworks/deep-analysis`, request);
    return response.data;
  }

  async getQuickInsights(frameworkId: string, startupData: any): Promise<any> {
    const response = await axios.post(
      `${this.baseURL}/api/frameworks/quick-insights/${frameworkId}`,
      startupData
    );
    return response.data;
  }

  async getAnalysisTemplates(): Promise<any> {
    const response = await axios.get(`${this.baseURL}/api/frameworks/analysis-templates`);
    return response.data;
  }
}

// React Component
export const DeepFrameworkAnalysis: React.FC<{ startupData: any }> = ({ startupData }) => {
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<DeepAnalysisResponse | null>(null);
  const [selectedFrameworks, setSelectedFrameworks] = useState<string[]>([
    'bcg_matrix',
    'ansoff_matrix',
    'porters_five_forces'
  ]);
  const [analysisDepth, setAnalysisDepth] = useState<'quick' | 'standard' | 'comprehensive'>('comprehensive');

  const deepAnalysisService = new DeepAnalysisService();

  const performAnalysis = async () => {
    setLoading(true);
    try {
      const result = await deepAnalysisService.performDeepAnalysis({
        startup_data: startupData,
        framework_ids: selectedFrameworks,
        analysis_depth: analysisDepth,
        include_implementation_plan: true,
        include_metrics: true,
        include_benchmarks: true
      });
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis failed:', error);
      // Handle error
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3">Performing deep strategic analysis...</span>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Deep Framework Analysis</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Select Frameworks</label>
            <div className="space-y-2">
              {['bcg_matrix', 'ansoff_matrix', 'porters_five_forces', 'blue_ocean', 'vrio'].map(framework => (
                <label key={framework} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedFrameworks.includes(framework)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedFrameworks([...selectedFrameworks, framework]);
                      } else {
                        setSelectedFrameworks(selectedFrameworks.filter(f => f !== framework));
                      }
                    }}
                    className="mr-2"
                  />
                  <span className="capitalize">{framework.replace('_', ' ')}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Analysis Depth</label>
            <select
              value={analysisDepth}
              onChange={(e) => setAnalysisDepth(e.target.value as any)}
              className="w-full p-2 border rounded"
            >
              <option value="quick">Quick (5-10 minutes)</option>
              <option value="standard">Standard (10-15 minutes)</option>
              <option value="comprehensive">Comprehensive (15-20 minutes)</option>
            </select>
          </div>

          <button
            onClick={performAnalysis}
            disabled={selectedFrameworks.length === 0}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            Perform Deep Analysis
          </button>
        </div>
      </div>
    );
  }

  // Display results
  return (
    <div className="space-y-6">
      {/* Executive Summary */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Executive Summary</h2>
        <p className="text-gray-700 whitespace-pre-line">{analysis.executive_summary}</p>
        
        <div className="mt-4 flex items-center">
          <div className="text-lg font-semibold">
            Success Probability: 
            <span className={`ml-2 ${
              analysis.success_probability >= 70 ? 'text-green-600' :
              analysis.success_probability >= 50 ? 'text-yellow-600' : 'text-red-600'
            }`}>
              {analysis.success_probability}%
            </span>
          </div>
        </div>
      </div>

      {/* Framework Analyses */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {analysis.framework_analyses.map((framework) => (
          <div key={framework.framework_id} className="bg-white p-4 rounded-lg shadow">
            <h3 className="font-bold text-lg mb-2">{framework.framework_name}</h3>
            <div className="text-sm text-gray-600 mb-2">
              Position: <span className="font-semibold">{framework.position}</span>
            </div>
            <div className="text-sm text-gray-600 mb-3">
              Score: <span className="font-semibold">{(framework.score * 100).toFixed(0)}%</span>
            </div>
            
            <div className="space-y-2">
              <h4 className="font-semibold text-sm">Key Recommendations:</h4>
              <ul className="text-sm space-y-1">
                {framework.strategic_recommendations.slice(0, 3).map((rec, idx) => (
                  <li key={idx} className="text-gray-700">• {rec}</li>
                ))}
              </ul>
            </div>

            {framework.risk_factors.length > 0 && (
              <div className="mt-3 pt-3 border-t">
                <h4 className="font-semibold text-sm mb-1">Top Risk:</h4>
                <p className="text-sm text-red-600">
                  {framework.risk_factors[0].risk} ({framework.risk_factors[0].impact} impact)
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Prioritized Actions */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Priority Actions</h2>
        <div className="space-y-3">
          {analysis.prioritized_actions.slice(0, 5).map((action, idx) => (
            <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2">
              <div className="font-semibold">{idx + 1}. {action.action}</div>
              <div className="text-sm text-gray-600 mt-1">
                <span className="mr-4">Impact: {action.impact}</span>
                <span className="mr-4">Effort: {action.effort}</span>
                <span>Timeline: {action.timeline}</span>
              </div>
              {action.success_metrics && (
                <div className="text-sm text-gray-500 mt-1">
                  Metrics: {action.success_metrics.join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Implementation Roadmap */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Implementation Roadmap</h2>
        <div className="space-y-4">
          {Object.entries(analysis.implementation_roadmap).map(([phase, details]: [string, any]) => (
            <div key={phase} className="border rounded p-4">
              <h3 className="font-semibold capitalize">{phase.replace('_', ' ')}</h3>
              <p className="text-sm text-gray-600">{details.timeline}</p>
              <p className="mt-2">Focus: {details.focus}</p>
              {details.key_initiatives && (
                <ul className="mt-2 text-sm space-y-1">
                  {details.key_initiatives.map((init: string, idx: number) => (
                    <li key={idx}>• {init}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Monitoring Plan */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Monitoring Plan</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold mb-2">Weekly Metrics</h3>
            <ul className="text-sm space-y-1">
              {analysis.monitoring_plan.weekly_metrics?.map((metric: string, idx: number) => (
                <li key={idx}>• {metric}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Decision Triggers</h3>
            <div className="text-sm space-y-2">
              {analysis.monitoring_plan.decision_triggers?.map((trigger: any, idx: number) => (
                <div key={idx} className="bg-gray-50 p-2 rounded">
                  <span className="font-medium">If:</span> {trigger.condition}<br/>
                  <span className="font-medium">Then:</span> {trigger.action}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => {
            // Export full analysis
            const blob = new Blob([JSON.stringify(analysis, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `deep-analysis-${new Date().toISOString()}.json`;
            a.click();
          }}
          className="bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700"
        >
          Export Full Analysis
        </button>
        
        <button
          onClick={() => setAnalysis(null)}
          className="bg-gray-600 text-white py-2 px-4 rounded hover:bg-gray-700"
        >
          New Analysis
        </button>
      </div>
    </div>
  );
};