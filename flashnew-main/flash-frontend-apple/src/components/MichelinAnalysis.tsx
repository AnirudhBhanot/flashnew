import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Icon } from '../design-system/components';
import { FrameworkImplementation } from './FrameworkImplementation';
import styles from './MichelinAnalysis.module.scss';

const MICHELIN_FRAMEWORKS = [
  {
    id: 'bcg_matrix',
    name: 'BCG Growth-Share Matrix',
    description: 'Position your product portfolio based on market growth and share',
    icon: 'chart.bar.xaxis'
  },
  {
    id: 'porters_five_forces',
    name: "Porter's Five Forces",
    description: 'Analyze competitive forces shaping your industry',
    icon: 'shield.lefthalf.filled'
  },
  {
    id: 'swot_analysis',
    name: 'SWOT Analysis',
    description: 'Comprehensive view of strengths, weaknesses, opportunities, and threats',
    icon: 'square.grid.2x2'
  },
  {
    id: 'value_chain',
    name: 'Value Chain Analysis',
    description: 'Identify competitive advantages in your business activities',
    icon: 'link'
  },
  {
    id: 'business_model_canvas',
    name: 'Business Model Canvas',
    description: 'Visualize all aspects of your business model',
    icon: 'rectangle.grid.3x2'
  },
  {
    id: 'blue_ocean_strategy',
    name: 'Blue Ocean Strategy',
    description: 'Find uncontested market spaces for growth',
    icon: 'water.waves'
  }
];

export const MichelinAnalysis: React.FC = () => {
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);
  const [completedFrameworks, setCompletedFrameworks] = useState<Set<string>>(new Set());

  const handleFrameworkComplete = (frameworkId: string) => {
    setCompletedFrameworks(prev => new Set(prev).add(frameworkId));
    setSelectedFramework(null);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Michelin-Style Framework Analysis</h2>
        <p className={styles.subtitle}>
          See how your startup performs across established business frameworks with specific insights and recommendations
        </p>
        <div className={styles.progress}>
          <span>{completedFrameworks.size} of {MICHELIN_FRAMEWORKS.length} frameworks analyzed</span>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill} 
              style={{ width: `${(completedFrameworks.size / MICHELIN_FRAMEWORKS.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {!selectedFramework ? (
        <div className={styles.frameworkGrid}>
          {MICHELIN_FRAMEWORKS.map((framework, index) => (
            <motion.div
              key={framework.id}
              className={`${styles.frameworkCard} ${completedFrameworks.has(framework.id) ? styles.completed : ''}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => setSelectedFramework(framework.id)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className={styles.frameworkIcon}>
                <Icon name={framework.icon} size={32} />
              </div>
              <h3>{framework.name}</h3>
              <p>{framework.description}</p>
              {completedFrameworks.has(framework.id) && (
                <div className={styles.completedBadge}>
                  <Icon name="checkmark.circle.fill" size={20} />
                  <span>Analyzed</span>
                </div>
              )}
              <button className={styles.analyzeButton}>
                {completedFrameworks.has(framework.id) ? 'View Analysis' : 'Analyze Now'}
                <Icon name="arrow.right" size={16} />
              </button>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className={styles.analysisView}>
          <button 
            className={styles.backButton}
            onClick={() => setSelectedFramework(null)}
          >
            <Icon name="arrow.left" size={20} />
            Back to Frameworks
          </button>
          <FrameworkImplementation 
            frameworkId={selectedFramework} 
            onClose={() => handleFrameworkComplete(selectedFramework)}
          />
        </div>
      )}

      {completedFrameworks.size === MICHELIN_FRAMEWORKS.length && (
        <motion.div 
          className={styles.completionMessage}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <Icon name="star.fill" size={48} />
          <h3>Complete Framework Analysis</h3>
          <p>You've analyzed your startup across all major business frameworks!</p>
        </motion.div>
      )}
    </div>
  );
};

export default MichelinAnalysis;