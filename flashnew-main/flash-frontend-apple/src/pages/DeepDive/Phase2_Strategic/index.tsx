import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import VisionRealityGap from './VisionRealityGap';
import AnsoffMatrix from './AnsoffMatrix';
import styles from './index.module.scss';

interface Tab {
  id: string;
  label: string;
  component: React.ReactNode;
}

const Phase2Strategic: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('vision-reality');
  
  const tabs: Tab[] = [
    {
      id: 'vision-reality',
      label: 'Vision-Reality Gap',
      component: <VisionRealityGap companyId="default" />
    },
    {
      id: 'ansoff-matrix',
      label: 'Ansoff Matrix',
      component: <AnsoffMatrix />
    }
  ];

  const activeTabContent = tabs.find(tab => tab.id === activeTab)?.component;

  return (
    <div className={styles.phase2Container}>
      <div className={styles.header}>
        <h1>Phase 2: Strategic Alignment</h1>
        <p>
          Analyze the gap between your vision and current reality, then develop strategies to bridge that gap
        </p>
      </div>

      <div className={styles.navigation}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`${styles.navButton} ${activeTab === tab.id ? styles.active : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className={styles.content}>
        {activeTabContent}
      </div>
    </div>
  );
};

export default Phase2Strategic;

export { default as VisionRealityGap } from './VisionRealityGap';
export { default as AnsoffMatrix } from './AnsoffMatrix';