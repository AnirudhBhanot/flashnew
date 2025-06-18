import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ConfigProvider } from './providers/ConfigProvider';
import { DataCollectionCAMP } from './components/v3/DataCollectionCAMP';
import { HybridAnalysisPage } from './components/v3/HybridAnalysisPage';
import { AnalysisResults } from './components/v3/AnalysisResults';
import { InvestmentMemo } from './components/v3/InvestmentMemo';
import { ConfigurationAdmin } from './components/admin';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ThemeToggle } from './components/ui/ThemeToggle';
import { StartupData } from './types';
import { EnrichedAnalysisData } from './types/api.types';
import './AppV3Dark.css';

type AppState = 'landing' | 'collection' | 'analyzing' | 'results';

export const AppV3: React.FC = () => {
  const [appState, setAppState] = useState<AppState>('landing');
  const [startupData, setStartupData] = useState<Partial<StartupData>>({});
  const [results, setResults] = useState<EnrichedAnalysisData | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);

  // Check for admin route
  useEffect(() => {
    const path = window.location.pathname;
    if (path === '/admin/config' || path === '/admin') {
      setIsAdmin(true);
    }
  }, []);

  const handleStartAnalysis = () => {
    setAppState('collection');
  };

  const handleDataSubmit = (data: StartupData) => {
    setStartupData(data);
    setAppState('analyzing');
  };

  const handleAnalysisComplete = (analysisResults: EnrichedAnalysisData) => {
    setResults(analysisResults);
    setAppState('results');
  };

  const handleBackToHome = () => {
    setAppState('landing');
    setStartupData({});
    setResults(null);
  };

  const handleExportPDF = () => {
    // TODO: Implement PDF export with InvestmentMemo component
    window.print(); // Temporary solution
  };

  // Show admin interface if on admin route
  if (isAdmin) {
    return (
      <ConfigProvider>
        <div className="app-v3">
          <ErrorBoundary>
            <ConfigurationAdmin />
          </ErrorBoundary>
        </div>
      </ConfigProvider>
    );
  }

  return (
    <ConfigProvider>
      <div className="app-v3">
      {/* Global Header */}
      <motion.header 
        className="app-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-content">
          <div className="header-logo">
            <span className="logo-text">FLASH</span>
          </div>
          <div className="header-actions">
            <ThemeToggle variant="minimal" />
          </div>
        </div>
      </motion.header>
      
      <AnimatePresence mode="wait">
        {appState === 'landing' && (
          <motion.div
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="landing-page"
          >
            <div className="landing-content">
              <motion.div
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.8 }}
              >
                <h1>FLASH</h1>
                <p className="tagline">Investment intelligence</p>
              </motion.div>

              <motion.div
                className="camp-grid"
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4, duration: 0.8 }}
              >
                <div className="camp-feature">
                  <div className="camp-icon">💰</div>
                  <h3>Capital</h3>
                  <p>Financial health analysis</p>
                </div>
                <div className="camp-feature">
                  <div className="camp-icon">⚡</div>
                  <h3>Advantage</h3>
                  <p>Competitive positioning</p>
                </div>
                <div className="camp-feature">
                  <div className="camp-icon">📈</div>
                  <h3>Market</h3>
                  <p>Market opportunity sizing</p>
                </div>
                <div className="camp-feature">
                  <div className="camp-icon">👥</div>
                  <h3>People</h3>
                  <p>Team assessment</p>
                </div>
              </motion.div>

              <motion.button
                className="start-button"
                onClick={handleStartAnalysis}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6, duration: 0.8 }}
              >
                Start Analysis
              </motion.button>
            </div>
          </motion.div>
        )}

        {appState === 'collection' && (
          <motion.div
            key="collection"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <ErrorBoundary>
              <DataCollectionCAMP 
                onSubmit={handleDataSubmit}
                onBack={handleBackToHome}
              />
            </ErrorBoundary>
          </motion.div>
        )}

        {appState === 'analyzing' && (
          <ErrorBoundary>
            <HybridAnalysisPage
              startupData={startupData}
              onComplete={handleAnalysisComplete}
              onBack={handleBackToHome}
            />
          </ErrorBoundary>
        )}

        {appState === 'results' && results && (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <ErrorBoundary>
              <AnalysisResults data={results} onExportPDF={handleExportPDF} />
            </ErrorBoundary>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header with back button for results */}
      {appState === 'results' && (
        <motion.div 
          className="results-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <button 
            className="back-button"
            onClick={handleBackToHome}
          >
            ← New Analysis
          </button>
        </motion.div>
      )}
      </div>
    </ConfigProvider>
  );
};

export default AppV3;