import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AppV3 } from '../AppV3';
import '@testing-library/jest-dom';

// Mock child components
jest.mock('../components/v3/DataCollectionCAMP', () => ({
  DataCollectionCAMP: ({ onSubmit }: any) => (
    <div data-testid="data-collection">
      <button onClick={() => onSubmit({
        funding_stage: 'seed',
        total_capital_raised_usd: 1000000,
        sector: 'SaaS',
        team_size_full_time: 10
      })}>
        Submit Data
      </button>
    </div>
  )
}));

jest.mock('../components/v3/HybridAnalysisPage', () => ({
  HybridAnalysisPage: ({ onComplete }: any) => {
    React.useEffect(() => {
      setTimeout(() => {
        onComplete({
          success_probability: 0.75,
          verdict: 'PASS',
          pillar_scores: { capital: 0.7, advantage: 0.8, market: 0.65, people: 0.75 }
        });
      }, 100);
    }, [onComplete]);
    
    return <div data-testid="analysis-page">Analyzing...</div>;
  }
}));

jest.mock('../components/v3/AnalysisResults', () => ({
  AnalysisResults: ({ data, onBack }: any) => (
    <div data-testid="results-page">
      <div>Success Probability: {(data.success_probability * 100).toFixed(0)}%</div>
      <button onClick={onBack}>Back to Home</button>
    </div>
  )
}));

jest.mock('../components/admin', () => ({
  ConfigurationAdmin: () => <div data-testid="admin-panel">Admin Panel</div>
}));

describe('AppV3', () => {
  beforeEach(() => {
    // Reset location before each test
    delete (window as any).location;
    (window as any).location = { pathname: '/' };
  });

  it('should render landing page by default', () => {
    render(<AppV3 />);
    
    expect(screen.getByText(/AI-Powered Startup Assessment/i)).toBeInTheDocument();
    expect(screen.getByText(/Start Analysis/i)).toBeInTheDocument();
  });

  it('should navigate through the complete flow', async () => {
    render(<AppV3 />);
    
    // Start from landing page
    const startButton = screen.getByText(/Start Analysis/i);
    fireEvent.click(startButton);
    
    // Should show data collection
    expect(screen.getByTestId('data-collection')).toBeInTheDocument();
    
    // Submit data
    const submitButton = screen.getByText('Submit Data');
    fireEvent.click(submitButton);
    
    // Should show analysis page
    expect(screen.getByTestId('analysis-page')).toBeInTheDocument();
    
    // Wait for analysis to complete
    await waitFor(() => {
      expect(screen.getByTestId('results-page')).toBeInTheDocument();
    });
    
    // Check results are displayed
    expect(screen.getByText(/Success Probability: 75%/)).toBeInTheDocument();
    
    // Go back to home
    const backButton = screen.getByText('Back to Home');
    fireEvent.click(backButton);
    
    // Should be back at landing page
    expect(screen.getByText(/AI-Powered Startup Assessment/i)).toBeInTheDocument();
  });

  it('should show admin panel when on admin route', () => {
    (window as any).location = { pathname: '/admin/config' };
    
    render(<AppV3 />);
    
    expect(screen.getByTestId('admin-panel')).toBeInTheDocument();
  });

  it('should handle errors with ErrorBoundary', () => {
    // Mock console.error to avoid noise
    const originalError = console.error;
    console.error = jest.fn();
    
    // Mock a component to throw an error
    jest.mock('../components/v3/DataCollectionCAMP', () => ({
      DataCollectionCAMP: () => {
        throw new Error('Test error');
      }
    }));
    
    render(<AppV3 />);
    
    // Start analysis to trigger the error
    const startButton = screen.getByText(/Start Analysis/i);
    fireEvent.click(startButton);
    
    // Should show error UI (if ErrorBoundary is properly implemented)
    // Note: This assumes ErrorBoundary shows "Something went wrong"
    expect(screen.queryByText(/Something went wrong/i)).toBeInTheDocument();
    
    console.error = originalError;
  });

  it('should preserve state when navigating between phases', async () => {
    const { container } = render(<AppV3 />);
    
    // Start analysis
    fireEvent.click(screen.getByText(/Start Analysis/i));
    
    // Submit data
    fireEvent.click(screen.getByText('Submit Data'));
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByTestId('results-page')).toBeInTheDocument();
    });
    
    // Verify the data was preserved through the flow
    expect(screen.getByText(/Success Probability: 75%/)).toBeInTheDocument();
  });
});