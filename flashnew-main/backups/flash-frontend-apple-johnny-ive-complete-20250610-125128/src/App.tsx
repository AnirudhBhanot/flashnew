import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AnimatePresence } from './helpers/motion';
import { useAppleTheme } from './shared/hooks/useAppleTheme';
import { LoadingScreen } from './design-system/components/LoadingScreen';
import { AutofillSelector } from './components/AutofillSelector';
import { ErrorProvider } from './contexts/ErrorContext';
import './App.css';

// Lazy load pages for better performance
const Landing = lazy(() => import('./pages/Landing'));
const Assessment = lazy(() => import('./pages/Assessment'));
const Analysis = lazy(() => import('./pages/Analysis'));
const Results = lazy(() => import('./pages/Results/ResultsV2'));

function App() {
  const { theme } = useAppleTheme();

  return (
    <ErrorProvider>
      <Router>
        <div className="app" data-theme={theme}>
          <AnimatePresence mode="wait">
            <Suspense fallback={<LoadingScreen />}>
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/assessment/*" element={<Assessment />} />
                <Route path="/analysis" element={<Analysis />} />
                <Route path="/results" element={<Results />} />
              </Routes>
            </Suspense>
          </AnimatePresence>
          
          {/* Development only: Floating autofill selector */}
          {process.env.NODE_ENV === 'development' && (
            <AutofillSelector variant="floating" />
          )}
        </div>
      </Router>
    </ErrorProvider>
  );
}

export default App;