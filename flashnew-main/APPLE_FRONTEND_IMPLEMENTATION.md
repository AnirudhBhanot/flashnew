# FLASH Apple Frontend - Implementation Plan

## Project Setup

### 1. Initialize New Frontend

```bash
cd /Users/sf/Desktop/FLASH
npx create-react-app flash-frontend-apple --template typescript
cd flash-frontend-apple

# Install core dependencies
npm install framer-motion@^11.0.0
npm install @react-spring/web@^9.7.0
npm install zustand@^4.4.0
npm install react-router-dom@^6.20.0
npm install d3@^7.8.0
npm install classnames@^2.3.2
npm install react-intersection-observer@^9.5.3

# Development dependencies
npm install -D @types/d3
npm install -D sass
npm install -D prettier eslint-config-prettier
```

### 2. Project Structure

```
src/
├── design-system/
│   ├── tokens/
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   ├── animations.ts
│   │   └── index.ts
│   ├── components/
│   │   ├── Button/
│   │   ├── TextField/
│   │   ├── Select/
│   │   ├── Card/
│   │   ├── NavigationBar/
│   │   ├── Progress/
│   │   ├── Icon/
│   │   └── index.ts
│   └── layouts/
│       ├── PageLayout/
│       ├── WizardLayout/
│       └── index.ts
├── pages/
│   ├── Landing/
│   ├── Assessment/
│   │   ├── CompanyInfo/
│   │   ├── Capital/
│   │   ├── Advantage/
│   │   ├── Market/
│   │   ├── People/
│   │   └── Review/
│   ├── Analysis/
│   └── Results/
├── features/
│   ├── wizard/
│   │   ├── WizardProvider.tsx
│   │   ├── useWizard.ts
│   │   └── types.ts
│   ├── assessment/
│   │   ├── assessmentStore.ts
│   │   ├── validation.ts
│   │   └── types.ts
│   └── results/
│       ├── resultsStore.ts
│       ├── animations.ts
│       └── types.ts
├── shared/
│   ├── animations/
│   │   ├── springConfigs.ts
│   │   ├── transitions.ts
│   │   └── index.ts
│   ├── hooks/
│   │   ├── useAppleTheme.ts
│   │   ├── useHaptic.ts
│   │   ├── useKeyboardNav.ts
│   │   └── index.ts
│   └── utils/
│       ├── formatting.ts
│       ├── validation.ts
│       └── api.ts
└── App.tsx
```

## Implementation Steps

### Phase 1: Design System (Week 1)

#### 1.1 Create Token System

```typescript
// src/design-system/tokens/colors.ts
export const colors = {
  light: {
    background: {
      primary: '#FFFFFF',
      secondary: '#F2F2F7',
      tertiary: '#FFFFFF',
      elevated: '#FFFFFF',
    },
    label: {
      primary: '#000000',
      secondary: 'rgba(60, 60, 67, 0.6)',
      tertiary: 'rgba(60, 60, 67, 0.3)',
      quaternary: 'rgba(60, 60, 67, 0.18)',
    },
    system: {
      blue: '#007AFF',
      green: '#34C759',
      red: '#FF3B30',
      orange: '#FF9500',
      yellow: '#FFCC00',
      teal: '#5AC8FA',
      indigo: '#5856D6',
      purple: '#AF52DE',
      pink: '#FF2D55',
    },
    separator: 'rgba(60, 60, 67, 0.12)',
  },
  dark: {
    // Dark mode colors
  }
};

// src/design-system/tokens/typography.ts
export const typography = {
  fonts: {
    display: '-apple-system-ui-serif, ui-serif',
    text: '-apple-system, BlinkMacSystemFont, "SF Pro Text"',
    rounded: '-apple-system-ui-rounded, -apple-system',
  },
  sizes: {
    largeTitle: '34px',
    title1: '28px',
    title2: '22px',
    title3: '20px',
    headline: '17px',
    body: '17px',
    callout: '16px',
    subheadline: '15px',
    footnote: '13px',
    caption1: '12px',
    caption2: '11px',
  },
  weights: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
};
```

#### 1.2 Build Core Components

```typescript
// src/design-system/components/Button/Button.tsx
import React from 'react';
import { motion } from 'framer-motion';
import classNames from 'classnames';
import styles from './Button.module.scss';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'text';
  size?: 'small' | 'medium' | 'large';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  children,
  onClick,
  disabled,
  loading,
  icon,
  fullWidth,
}) => {
  return (
    <motion.button
      className={classNames(
        styles.button,
        styles[variant],
        styles[size],
        {
          [styles.disabled]: disabled,
          [styles.loading]: loading,
          [styles.fullWidth]: fullWidth,
        }
      )}
      onClick={onClick}
      disabled={disabled || loading}
      whileTap={{ scale: 0.97 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.1 }}
    >
      {loading && <span className={styles.spinner} />}
      {icon && <span className={styles.icon}>{icon}</span>}
      <span className={styles.label}>{children}</span>
    </motion.button>
  );
};
```

#### 1.3 Create Navigation Components

```typescript
// src/design-system/components/NavigationBar/NavigationBar.tsx
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import styles from './NavigationBar.module.scss';

interface NavigationBarProps {
  title: string;
  transparent?: boolean;
  children?: React.ReactNode;
}

export const NavigationBar: React.FC<NavigationBarProps> = ({
  title,
  transparent,
  children,
}) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      className={classNames(styles.nav, {
        [styles.transparent]: transparent && !scrolled,
        [styles.scrolled]: scrolled,
      })}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className={styles.content}>
        <h1 className={styles.title}>{title}</h1>
        <div className={styles.actions}>{children}</div>
      </div>
    </motion.nav>
  );
};
```

### Phase 2: Core Features (Week 2)

#### 2.1 Wizard System

```typescript
// src/features/wizard/WizardProvider.tsx
import React, { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface WizardContextType {
  currentStep: number;
  totalSteps: number;
  data: any;
  goToStep: (step: number) => void;
  nextStep: () => void;
  previousStep: () => void;
  updateData: (stepData: any) => void;
  canNavigateToStep: (step: number) => boolean;
}

const WizardContext = createContext<WizardContextType | null>(null);

export const WizardProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [data, setData] = useState({});
  const navigate = useNavigate();

  const steps = [
    '/assessment/company',
    '/assessment/capital',
    '/assessment/advantage',
    '/assessment/market',
    '/assessment/people',
    '/assessment/review',
  ];

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      const nextIndex = currentStep + 1;
      setCurrentStep(nextIndex);
      navigate(steps[nextIndex]);
    } else {
      navigate('/analysis');
    }
  };

  const previousStep = () => {
    if (currentStep > 0) {
      const prevIndex = currentStep - 1;
      setCurrentStep(prevIndex);
      navigate(steps[prevIndex]);
    }
  };

  const goToStep = (step: number) => {
    if (canNavigateToStep(step)) {
      setCurrentStep(step);
      navigate(steps[step]);
    }
  };

  const canNavigateToStep = (step: number) => {
    return step === 0 || completedSteps.includes(step - 1);
  };

  const updateData = (stepData: any) => {
    setData((prev) => ({ ...prev, ...stepData }));
    if (!completedSteps.includes(currentStep)) {
      setCompletedSteps((prev) => [...prev, currentStep]);
    }
  };

  return (
    <WizardContext.Provider
      value={{
        currentStep,
        totalSteps: steps.length,
        data,
        goToStep,
        nextStep,
        previousStep,
        updateData,
        canNavigateToStep,
      }}
    >
      {children}
    </WizardContext.Provider>
  );
};

export const useWizard = () => {
  const context = useContext(WizardContext);
  if (!context) {
    throw new Error('useWizard must be used within WizardProvider');
  }
  return context;
};
```

#### 2.2 Assessment Store

```typescript
// src/features/assessment/assessmentStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AssessmentState {
  companyInfo: {
    name: string;
    industry: string;
    stage: string;
    foundedDate: Date | null;
  };
  capital: {
    totalFunding: number;
    burnRate: number;
    runway: number;
    arr: number;
    grossMargin?: number;
    ltvCac?: string;
  };
  advantage: {
    moatStrength: number;
    advantages: string[];
    uniqueAdvantage: string;
    hasPatents: boolean;
    patentCount?: number;
  };
  market: {
    tam: number;
    samPercentage: number;
    marketGrowth: number;
    competition: number;
    cac: number;
    arpu: number;
  };
  people: {
    teamSize: number;
    techTeam: number;
    avgExperience: number;
    founderBackgrounds: string[];
    foundersWorkedTogether: boolean;
    cultureStrength: number;
  };
  
  updateSection: <T extends keyof AssessmentState>(
    section: T,
    data: Partial<AssessmentState[T]>
  ) => void;
  
  reset: () => void;
}

export const useAssessmentStore = create<AssessmentState>()(
  persist(
    (set) => ({
      companyInfo: {
        name: '',
        industry: '',
        stage: '',
        foundedDate: null,
      },
      capital: {
        totalFunding: 0,
        burnRate: 0,
        runway: 0,
        arr: 0,
      },
      advantage: {
        moatStrength: 5,
        advantages: [],
        uniqueAdvantage: '',
        hasPatents: false,
      },
      market: {
        tam: 0,
        samPercentage: 0,
        marketGrowth: 0,
        competition: 5,
        cac: 0,
        arpu: 0,
      },
      people: {
        teamSize: 0,
        techTeam: 0,
        avgExperience: 0,
        founderBackgrounds: [],
        foundersWorkedTogether: false,
        cultureStrength: 5,
      },
      
      updateSection: (section, data) =>
        set((state) => ({
          [section]: { ...state[section], ...data },
        })),
      
      reset: () =>
        set(() => ({
          companyInfo: {
            name: '',
            industry: '',
            stage: '',
            foundedDate: null,
          },
          capital: {
            totalFunding: 0,
            burnRate: 0,
            runway: 0,
            arr: 0,
          },
          advantage: {
            moatStrength: 5,
            advantages: [],
            uniqueAdvantage: '',
            hasPatents: false,
          },
          market: {
            tam: 0,
            samPercentage: 0,
            marketGrowth: 0,
            competition: 5,
            cac: 0,
            arpu: 0,
          },
          people: {
            teamSize: 0,
            techTeam: 0,
            avgExperience: 0,
            founderBackgrounds: [],
            foundersWorkedTogether: false,
            cultureStrength: 5,
          },
        })),
    }),
    {
      name: 'flash-assessment',
    }
  )
);
```

### Phase 3: Pages Implementation (Week 3)

#### 3.1 Landing Page

```typescript
// src/pages/Landing/Landing.tsx
import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Button } from '../../design-system/components';
import { Canvas } from '@react-three/fiber';
import { StartupNetwork } from './StartupNetwork';
import styles from './Landing.module.scss';

export const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.landing}>
      <section className={styles.hero}>
        <motion.div
          className={styles.content}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.2, 0, 0, 1] }}
        >
          <h1 className={styles.title}>
            Know Your Startup's
            <span className={styles.gradient}>True Potential</span>
          </h1>
          
          <p className={styles.subtitle}>
            Get an honest assessment powered by machine learning
            and validated by analyzing 100,000+ startups
          </p>
          
          <div className={styles.actions}>
            <Button
              variant="primary"
              size="large"
              onClick={() => navigate('/assessment/company')}
            >
              Begin Assessment
              <Icon name="arrow.right" />
            </Button>
            
            <Button variant="secondary" size="large">
              <Icon name="play.circle" />
              Watch Demo
            </Button>
          </div>
        </motion.div>
        
        <div className={styles.visual}>
          <Canvas>
            <StartupNetwork />
          </Canvas>
        </div>
      </section>
      
      {/* Additional sections... */}
    </div>
  );
};
```

#### 3.2 Assessment Pages

```typescript
// src/pages/Assessment/CompanyInfo/CompanyInfo.tsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useWizard } from '../../../features/wizard/useWizard';
import { useAssessmentStore } from '../../../features/assessment/assessmentStore';
import {
  TextField,
  Select,
  DatePicker,
  Button,
} from '../../../design-system/components';
import { WizardLayout } from '../../../design-system/layouts';
import styles from './CompanyInfo.module.scss';

export const CompanyInfo: React.FC = () => {
  const { nextStep, previousStep } = useWizard();
  const { companyInfo, updateSection } = useAssessmentStore();
  const [errors, setErrors] = useState({});

  const handleContinue = () => {
    if (validate()) {
      updateSection('companyInfo', companyInfo);
      nextStep();
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!companyInfo.name) {
      newErrors.name = 'Company name is required';
    }
    if (!companyInfo.industry) {
      newErrors.industry = 'Please select an industry';
    }
    // Additional validation...
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  return (
    <WizardLayout
      title="Tell us about your company"
      step={1}
      onBack={previousStep}
    >
      <motion.div
        className={styles.form}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
      >
        <TextField
          label="Company Name"
          placeholder="Acme Inc."
          value={companyInfo.name}
          onChange={(value) => updateSection('companyInfo', { name: value })}
          error={errors.name}
          autoFocus
        />
        
        <Select
          label="Industry"
          placeholder="Select your industry"
          value={companyInfo.industry}
          onChange={(value) => updateSection('companyInfo', { industry: value })}
          error={errors.industry}
        >
          <Option value="saas">SaaS</Option>
          <Option value="fintech">FinTech</Option>
          <Option value="healthtech">HealthTech</Option>
          <Option value="marketplace">Marketplace</Option>
          <Option value="ecommerce">E-commerce</Option>
          <Option value="deeptech">DeepTech</Option>
          <Option value="other">Other</Option>
        </Select>
        
        {/* Additional fields... */}
      </motion.div>
      
      <div className={styles.actions}>
        <Button variant="text" onClick={previousStep}>
          Back
        </Button>
        <Button variant="primary" onClick={handleContinue}>
          Continue
        </Button>
      </div>
    </WizardLayout>
  );
};
```

### Phase 4: Results & Analytics (Week 4)

#### 4.1 Analysis Page

```typescript
// src/pages/Analysis/Analysis.tsx
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { analyzeStartup } from '../../shared/api';
import { useAssessmentStore } from '../../features/assessment/assessmentStore';
import styles from './Analysis.module.scss';

export const Analysis: React.FC = () => {
  const navigate = useNavigate();
  const assessmentData = useAssessmentStore();
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Initializing analysis...');

  useEffect(() => {
    performAnalysis();
  }, []);

  const performAnalysis = async () => {
    try {
      // Simulate analysis steps
      const steps = [
        { progress: 20, status: 'Analyzing financial metrics...' },
        { progress: 40, status: 'Evaluating market position...' },
        { progress: 60, status: 'Assessing team capabilities...' },
        { progress: 80, status: 'Matching startup patterns...' },
        { progress: 100, status: 'Finalizing assessment...' },
      ];

      for (const step of steps) {
        await new Promise((resolve) => setTimeout(resolve, 800));
        setProgress(step.progress);
        setStatus(step.status);
      }

      // Make API call
      const results = await analyzeStartup(assessmentData);
      
      // Navigate to results
      navigate('/results', { state: { results } });
    } catch (error) {
      console.error('Analysis failed:', error);
      // Handle error
    }
  };

  return (
    <div className={styles.analysis}>
      <motion.div
        className={styles.content}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className={styles.indicator}>
          <motion.div
            className={styles.progress}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, ease: [0.2, 0, 0, 1] }}
          >
            <svg viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="var(--apple-separator)"
                strokeWidth="2"
              />
              <motion.circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="var(--apple-blue)"
                strokeWidth="2"
                strokeLinecap="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: progress / 100 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
              />
            </svg>
            <div className={styles.percentage}>{progress}%</div>
          </motion.div>
        </div>
        
        <motion.p
          className={styles.status}
          key={status}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {status}
        </motion.p>
      </motion.div>
    </div>
  );
};
```

#### 4.2 Results Page Components

```typescript
// src/pages/Results/components/ScoreReveal.tsx
import React from 'react';
import { motion } from 'framer-motion';
import { useSpring, animated } from '@react-spring/web';
import styles from './ScoreReveal.module.scss';

interface ScoreRevealProps {
  score: number;
  verdict: string;
}

export const ScoreReveal: React.FC<ScoreRevealProps> = ({ score, verdict }) => {
  const { number } = useSpring({
    from: { number: 0 },
    to: { number: score },
    delay: 200,
    config: { mass: 1, tension: 20, friction: 10 },
  });

  return (
    <div className={styles.scoreReveal}>
      <motion.div
        className={styles.circle}
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.8, ease: [0.2, 0, 0, 1] }}
      >
        <svg viewBox="0 0 200 200">
          <defs>
            <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#34C759" />
              <stop offset="50%" stopColor="#FFCC00" />
              <stop offset="100%" stopColor="#FF3B30" />
            </linearGradient>
          </defs>
          
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="var(--apple-separator)"
            strokeWidth="20"
          />
          
          <motion.circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="url(#scoreGradient)"
            strokeWidth="20"
            strokeLinecap="round"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: score / 100 }}
            transition={{ duration: 2, ease: "easeOut" }}
          />
        </svg>
        
        <div className={styles.scoreDisplay}>
          <animated.span className={styles.number}>
            {number.to(n => `${Math.round(n)}%`)}
          </animated.span>
          <span className={styles.label}>Success Probability</span>
        </div>
      </motion.div>
      
      <motion.div
        className={styles.verdict}
        initial={{ scale: 0.8, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        transition={{ delay: 1.5, duration: 0.5, ease: [0.2, 0, 0, 1] }}
      >
        <div className={styles[verdict.toLowerCase()]}>
          <Icon name={getVerdictIcon(verdict)} />
          <span>{verdict}</span>
        </div>
      </motion.div>
    </div>
  );
};
```

### Phase 5: Polish & Testing (Week 5)

#### 5.1 Animations & Interactions

```typescript
// src/shared/animations/index.ts
export const pageTransition = {
  initial: { opacity: 0, x: 60 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -60 },
  transition: {
    duration: 0.4,
    ease: [0.2, 0, 0, 1], // Apple's emphasized easing
  },
};

export const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5, ease: [0.2, 0, 0, 1] },
};

export const scaleIn = {
  initial: { scale: 0 },
  animate: { scale: 1 },
  transition: { duration: 0.3, ease: [0.2, 0, 0, 1] },
};
```

#### 5.2 Custom Hooks

```typescript
// src/shared/hooks/useAppleTheme.ts
import { useEffect, useState } from 'react';

export const useAppleTheme = () => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      setTheme(e.matches ? 'dark' : 'light');
    };

    // Set initial theme
    setTheme(mediaQuery.matches ? 'dark' : 'light');

    // Listen for changes
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return { theme, setTheme };
};

// src/shared/hooks/useHaptic.ts
export const useHaptic = () => {
  const light = () => {
    if ('vibrate' in navigator) {
      navigator.vibrate(10);
    }
  };

  const medium = () => {
    if ('vibrate' in navigator) {
      navigator.vibrate(20);
    }
  };

  const heavy = () => {
    if ('vibrate' in navigator) {
      navigator.vibrate(30);
    }
  };

  return { light, medium, heavy };
};
```

## Deployment

### Build Configuration

```json
// package.json additions
{
  "scripts": {
    "build": "react-scripts build",
    "build:prod": "GENERATE_SOURCEMAP=false react-scripts build",
    "analyze": "source-map-explorer 'build/static/js/*.js'",
    "test": "react-scripts test",
    "test:coverage": "npm test -- --coverage --watchAll=false",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx,scss}\""
  }
}
```

### Performance Optimizations

1. **Code Splitting**
```typescript
const Landing = lazy(() => import('./pages/Landing'));
const Assessment = lazy(() => import('./pages/Assessment'));
const Results = lazy(() => import('./pages/Results'));
```

2. **Image Optimization**
- Use WebP format with fallbacks
- Implement lazy loading
- Serve responsive images

3. **Bundle Size**
- Tree shake unused code
- Minimize CSS
- Use production builds of libraries

## Testing Strategy

### Unit Tests
- Component rendering
- Hook behavior
- Store updates
- Utility functions

### Integration Tests
- Wizard flow
- API interactions
- State persistence
- Navigation

### E2E Tests
- Complete assessment flow
- Error scenarios
- Cross-browser testing
- Mobile responsiveness

This implementation plan creates a world-class frontend that feels like a native Apple application while maintaining the sophisticated analysis capabilities of FLASH.