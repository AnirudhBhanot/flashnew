import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './DeepDive.module.scss';

interface Phase {
  id: string;
  title: string;
  description: string;
  route: string;
  status: 'completed' | 'in-progress' | 'locked';
}

interface PhaseStatuses {
  phase1: 'completed' | 'in-progress' | 'locked';
  phase2: 'completed' | 'in-progress' | 'locked';
  phase3: 'completed' | 'in-progress' | 'locked';
  phase4: 'completed' | 'in-progress' | 'locked';
  synthesis: 'completed' | 'in-progress' | 'locked';
}

const DeepDive: React.FC = () => {
  const navigate = useNavigate();
  const [currentPhase, setCurrentPhase] = useState<number>(0);
  const [phaseStatuses, setPhaseStatuses] = useState<PhaseStatuses>({
    phase1: 'in-progress',
    phase2: 'locked',
    phase3: 'locked',
    phase4: 'locked',
    synthesis: 'locked'
  });

  // Load phase completion status from localStorage
  useEffect(() => {
    const savedStatuses = localStorage.getItem('deepDivePhaseStatuses');
    if (savedStatuses) {
      const parsed = JSON.parse(savedStatuses) as PhaseStatuses;
      setPhaseStatuses(parsed);
      
      // Update current phase based on progress
      const phaseOrder = ['phase1', 'phase2', 'phase3', 'phase4', 'synthesis'];
      const lastInProgress = phaseOrder.findIndex(id => parsed[id as keyof PhaseStatuses] === 'in-progress');
      if (lastInProgress !== -1) {
        setCurrentPhase(lastInProgress);
      } else {
        // All phases completed
        const completedCount = phaseOrder.filter(id => parsed[id as keyof PhaseStatuses] === 'completed').length;
        setCurrentPhase(Math.max(0, completedCount - 1));
      }
    }
  }, []);

  // Listen for phase completion events
  useEffect(() => {
    const handlePhaseComplete = (event: CustomEvent) => {
      const { phaseId } = event.detail;
      updatePhaseStatus(phaseId, 'completed');
    };

    window.addEventListener('deepDivePhaseComplete' as any, handlePhaseComplete as any);
    return () => {
      window.removeEventListener('deepDivePhaseComplete' as any, handlePhaseComplete as any);
    };
  }, [phaseStatuses]);

  // Update phase statuses when a phase is completed
  const updatePhaseStatus = (phaseId: string, status: 'completed') => {
    const newStatuses = { ...phaseStatuses };
    newStatuses[phaseId as keyof PhaseStatuses] = status;
    
    // Unlock next phase
    const phaseOrder: (keyof PhaseStatuses)[] = ['phase1', 'phase2', 'phase3', 'phase4', 'synthesis'];
    const currentIndex = phaseOrder.indexOf(phaseId as keyof PhaseStatuses);
    if (currentIndex < phaseOrder.length - 1) {
      const nextPhaseId = phaseOrder[currentIndex + 1];
      if (newStatuses[nextPhaseId] === 'locked') {
        newStatuses[nextPhaseId] = 'in-progress';
      }
    }
    
    setPhaseStatuses(newStatuses);
    localStorage.setItem('deepDivePhaseStatuses', JSON.stringify(newStatuses));
  };

  const phases: Phase[] = [
    {
      id: 'phase1',
      title: 'Phase 1: Context Mapping',
      description: 'External Reality Check & Internal Audit - Understanding your current position',
      route: '/deep-dive/phase1',
      status: phaseStatuses.phase1
    },
    {
      id: 'phase2',
      title: 'Phase 2: Strategic Alignment',
      description: 'Vision-Reality Gap Analysis & Growth Strategy Matrix',
      route: '/deep-dive/phase2',
      status: phaseStatuses.phase2
    },
    {
      id: 'phase3',
      title: 'Phase 3: Organizational Readiness',
      description: '7S Framework Assessment - Evaluating implementation capabilities',
      route: '/deep-dive/phase3',
      status: phaseStatuses.phase3
    },
    {
      id: 'phase4',
      title: 'Phase 4: Risk-Weighted Pathways',
      description: 'Scenario Planning & Risk Assessment - Planning for uncertainties',
      route: '/deep-dive/phase4',
      status: phaseStatuses.phase4
    },
    {
      id: 'synthesis',
      title: 'Synthesis & Recommendations',
      description: 'Integrated insights and actionable strategic recommendations',
      route: '/deep-dive/synthesis',
      status: phaseStatuses.synthesis
    }
  ];

  const handlePhaseClick = (phase: Phase, index: number) => {
    if (phase.status !== 'locked') {
      setCurrentPhase(index);
      navigate(phase.route);
    }
  };

  const getPhaseClassName = (status: string) => {
    switch (status) {
      case 'completed':
        return styles.phaseCompleted;
      case 'in-progress':
        return styles.phaseInProgress;
      case 'locked':
        return styles.phaseLocked;
      default:
        return '';
    }
  };

  // Calculate progress percentage based on completed phases
  const completedCount = phases.filter(p => p.status === 'completed').length;
  const progressPercentage = (completedCount / phases.length) * 100;

  // Add reset button for testing
  const resetProgress = () => {
    const initialStatuses: PhaseStatuses = {
      phase1: 'in-progress',
      phase2: 'locked',
      phase3: 'locked',
      phase4: 'locked',
      synthesis: 'locked'
    };
    setPhaseStatuses(initialStatuses);
    localStorage.setItem('deepDivePhaseStatuses', JSON.stringify(initialStatuses));
    setCurrentPhase(0);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Progressive Deep Dive Analysis</h1>
        <p className={styles.subtitle}>
          A comprehensive strategic analysis framework that progressively builds insights through four interconnected phases
        </p>
      </div>

      <div className={styles.progressBar}>
        <div 
          className={styles.progressFill} 
          style={{ width: `${progressPercentage}%` }}
        />
      </div>

      <div className={styles.phasesContainer}>
        {phases.map((phase, index) => (
          <div
            key={phase.id}
            className={`${styles.phaseCard} ${getPhaseClassName(phase.status)}`}
            onClick={() => handlePhaseClick(phase, index)}
          >
            <div className={styles.phaseNumber}>
              {phase.status === 'completed' ? '✓' : phase.id === 'synthesis' ? '◆' : index + 1}
            </div>
            <div className={styles.phaseContent}>
              <h3 className={styles.phaseTitle}>{phase.title}</h3>
              <p className={styles.phaseDescription}>{phase.description}</p>
            </div>
            <div className={styles.phaseStatus}>
              {phase.status === 'completed' && <span className={styles.checkmark}>✓</span>}
              {phase.status === 'in-progress' && <span className={styles.inProgress}>→</span>}
              {phase.status === 'locked' && <span className={styles.locked}>○</span>}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.instructions}>
        <h2>How It Works</h2>
        <ol>
          <li>Complete each phase sequentially to unlock the next</li>
          <li>Each phase builds upon insights from previous phases</li>
          <li>Framework selection is AI-driven based on your specific context</li>
          <li>Final synthesis provides integrated recommendations</li>
        </ol>
        
        {/* Reset button for testing - remove in production */}
        <button 
          onClick={resetProgress} 
          style={{ 
            marginTop: '20px', 
            padding: '8px 16px', 
            fontSize: '14px',
            background: '#f5f5f7',
            border: '1px solid #d2d2d7',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          Reset Progress (Testing)
        </button>
      </div>
    </div>
  );
};

export default DeepDive;