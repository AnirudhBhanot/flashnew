import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowUpRight, ChevronDown, ChevronRight } from 'lucide-react';
import { EnhancedInsightsMinimalV2 } from './EnhancedInsightsMinimalV2';
import { DeepDiveAnalysisMinimalV2 } from './DeepDiveAnalysisMinimalV2';
import { LLMRecommendationsMinimalV2 } from './LLMRecommendationsMinimalV2';
import { CAMPAnalysisMinimalV2 } from './CAMPAnalysisMinimalV2';
import { SuccessScoreMinimal } from './SuccessScoreMinimal';

interface ResultsV2EnhancedProps {
  formData: any;
  results: any;
  onBack: () => void;
}

const ResultsV2Enhanced: React.FC<ResultsV2EnhancedProps> = ({ formData, results, onBack }) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['score']));
  const [activeAnalysis, setActiveAnalysis] = useState<string>('camp');

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const score = results.success_probability || 75;
  const scoreColor = score >= 70 ? 'rgb(34, 197, 94)' : score >= 40 ? 'rgb(251, 191, 36)' : 'rgb(239, 68, 68)';

  // CAMP Framework data
  const campData = {
    Capital: results.scores?.capital || 0.65,
    Advantage: results.scores?.advantage || 0.72,
    Market: results.scores?.market || 0.68,
    People: results.scores?.people || 0.75
  };

  // Prepare scores for components that need them
  const campScores = {
    capital: campData.Capital || 0,
    advantage: campData.Advantage || 0,
    market: campData.Market || 0,
    people: campData.People || 0
  };

  const analysisSections = [
    { id: 'score', title: 'Success Score', alwaysOpen: true },
    { id: 'camp', title: 'CAMP Framework Analysis' },
    { id: 'insights', title: 'Enhanced Insights' },
    { id: 'deepdive', title: 'Deep Dive Analysis' },
    { id: 'recommendations', title: 'FLASH Intelligence' },
    { id: 'actions', title: 'Recommended Actions' }
  ];

  const SectionHeader = ({ section, isExpanded, onToggle }: any) => (
    <motion.button
      onClick={() => onToggle(section.id)}
      className="w-full text-left py-6 border-b border-gray-100 flex items-center justify-between group"
      whileHover={{ x: 4 }}
      transition={{ duration: 0.2 }}
    >
      <h2 className="text-2xl font-light text-gray-900">{section.title}</h2>
      {!section.alwaysOpen && (
        <motion.div
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown className="w-5 h-5 text-gray-400 group-hover:text-gray-600" />
        </motion.div>
      )}
    </motion.button>
  );

  const ScoreDisplay = () => (
    <SuccessScoreMinimal 
      score={score / 100} 
      confidence={results.confidence}
      companyName={formData.startupName || formData.companyInfo?.companyName}
    />
  );

  const CAMPAnalysis = () => (
    <div className="py-8">
      <CAMPAnalysisMinimalV2 scores={campScores} />
    </div>
  );

  const ActionsSection = () => (
    <div className="py-8">
      <div className="flex flex-col gap-4 max-w-md mx-auto">
        {[
          { label: 'Download Report', action: 'download' },
          { label: 'Schedule Consultation', action: 'consult' },
          { label: 'Share Results', action: 'share' }
        ].map((action, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.1 }}
            className="py-4 px-6 text-center border border-gray-200 hover:border-gray-900 hover:bg-gray-900 hover:text-white transition-all duration-200"
            whileTap={{ scale: 0.98 }}
          >
            <span className="text-base font-normal">{action.label}</span>
          </motion.button>
        ))}
      </div>
    </div>
  );

  const renderSectionContent = (sectionId: string) => {
    switch (sectionId) {
      case 'score':
        return <ScoreDisplay />;
      case 'camp':
        return <CAMPAnalysis />;
      case 'insights':
        return (
          <div className="py-8">
            <EnhancedInsightsMinimalV2 
              scores={campScores}
              probability={score}
            />
          </div>
        );
      case 'deepdive':
        return (
          <div className="py-8">
            <DeepDiveAnalysisMinimalV2 
              scores={campScores}
              assessmentData={formData}
              insights={results.insights}
            />
          </div>
        );
      case 'recommendations':
        return (
          <div className="py-8">
            <LLMRecommendationsMinimalV2 
              assessmentData={formData}
              basicResults={results}
            />
          </div>
        );
      case 'actions':
        return <ActionsSection />;
      default:
        return null;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-white"
    >
      {/* Header */}
      <header className="border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <motion.button
              onClick={onBack}
              className="text-gray-400 hover:text-gray-600 transition-colors text-sm"
              whileHover={{ x: -2 }}
            >
              ← Back
            </motion.button>
            <h1 className="text-sm font-light text-gray-500">Startup Analysis Report</h1>
            <div className="w-16" /> {/* Spacer for centering */}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">

        {/* Analysis Sections */}
        <div className="space-y-0">
          {analysisSections.map((section) => (
            <div key={section.id}>
              <SectionHeader
                section={section}
                isExpanded={expandedSections.has(section.id)}
                onToggle={toggleSection}
              />
              <AnimatePresence>
                {(section.alwaysOpen || expandedSections.has(section.id)) && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    style={{ overflow: 'hidden' }}
                  >
                    {renderSectionContent(section.id)}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-100 mt-24">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <p className="text-center text-sm text-gray-400">
            Analysis generated on {new Date().toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </p>
        </div>
      </footer>
    </motion.div>
  );
};

export default ResultsV2Enhanced;