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
const Results = lazy(() => import('./pages/Results/ResultsV2Enhanced'));
const DeepDive = lazy(() => import('./pages/DeepDive'));
const Phase1Context = lazy(() => import('./pages/DeepDive/Phase1_Context'));
const Phase2Strategic = lazy(() => import('./pages/DeepDive/Phase2_Strategic'));
const Phase3Organizational = lazy(() => import('./pages/DeepDive/Phase3_Organizational'));
const Phase4RiskPathways = lazy(() => import('./pages/DeepDive/Phase4_RiskPathways'));
const Synthesis = lazy(() => import('./pages/DeepDive/Synthesis'));
const TestFramework = lazy(() => import('./pages/TestFramework'));
const TestResults = lazy(() => import('./pages/TestResults'));
const TestMichelin = lazy(() => import('./pages/TestMichelin'));
const TestStrategic = lazy(() => import('./pages/TestStrategic'));
const TestFrameworkIntelligence = lazy(() => import('./pages/TestFrameworkIntelligence'));
const TestDataDrivenFramework = lazy(() => import('./pages/TestDataDrivenFramework'));
const TestStrategicFramework = lazy(() => import('./pages/TestStrategicFramework'));
const TestStrategicFrameworkSimple = lazy(() => import('./pages/TestStrategicFrameworkSimple'));
const TestIntelligentFramework = lazy(() => import('./pages/TestIntelligentFramework'));

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
                <Route path="/deep-dive" element={<DeepDive />} />
                <Route path="/deep-dive/phase1" element={<Phase1Context />} />
                <Route path="/deep-dive/phase2" element={<Phase2Strategic />} />
                <Route path="/deep-dive/phase3" element={<Phase3Organizational />} />
                <Route path="/deep-dive/phase4" element={<Phase4RiskPathways />} />
                <Route path="/deep-dive/synthesis" element={<Synthesis />} />
                <Route path="/test-framework" element={<TestFramework />} />
                <Route path="/test-results" element={<TestResults />} />
                <Route path="/test-michelin" element={<TestMichelin />} />
                <Route path="/test-strategic" element={<TestStrategic />} />
                <Route path="/test-framework-intelligence" element={<TestFrameworkIntelligence />} />
                <Route path="/test-data-driven-framework" element={<TestDataDrivenFramework />} />
                <Route path="/test-strategic-framework" element={<TestStrategicFramework />} />
                <Route path="/test-strategic-simple" element={<TestStrategicFrameworkSimple />} />
                <Route path="/test-intelligent-framework" element={<TestIntelligentFramework />} />
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