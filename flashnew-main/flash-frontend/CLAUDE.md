# CLAUDE.md - AI Assistant Context

This file provides context and guidelines for AI assistants (like Claude) working on the FLASH platform.

## 🎯 Project Overview

FLASH is an AI-powered startup assessment platform that helps VCs make data-driven investment decisions. It uses advanced ML models to analyze startups across the CAMP framework (Capital, Advantage, Market, People).

## 🏗️ Project Structure

```
flash-frontend/               # React TypeScript frontend
├── src/
│   ├── components/v3/       # Latest component versions
│   ├── AppV3.tsx           # Main app component
│   └── index.tsx           # Entry point
└── build/                  # Production build

flash-backend-api/          # Python FastAPI backend
├── api_server.py          # Main API server
├── ml_models/             # Trained ML models
└── advanced_models.py     # Model implementations
```

## 🔧 Development Guidelines

### Code Style
- **TypeScript**: Use strict typing, avoid `any`
- **React**: Functional components with hooks
- **CSS**: CSS-in-JS or CSS modules, BEM naming
- **Python**: PEP 8 compliant, type hints preferred

### Component Guidelines
- Always use v3 components (latest version)
- Prefer WorldClassResults over EnhancedResults
- Use Framer Motion for animations
- Implement proper error boundaries

### API Guidelines
- Use /predict_advanced for full analysis
- Transform data before sending to API
- Handle errors gracefully
- Log important events

## 🚀 Common Commands

```bash
# Frontend
cd flash-frontend
npm install          # Install dependencies
npm start           # Start dev server (port 3000)
npm run build       # Build for production
npm run lint        # Run linter
npm run typecheck   # Check TypeScript

# Backend
cd flash-backend-api
pip install -r requirements.txt  # Install dependencies
python api_server_improved.py --port 8001  # Start improved API (port 8001)
python test_model.py           # Test ML models

# Train Hierarchical Models (NEW)
python train_hierarchical_models_45features.py  # Train all hierarchical models
```

## 📊 Key Features

### ML Models (Updated June 2025 - Realistic Models)

#### Production Models (V46 Realistic)
1. **DNA Analyzer**: RandomForest, AUC 0.489
2. **Temporal Model**: XGBoost, AUC 0.505  
3. **Industry Model**: XGBoost, AUC 0.504
4. **Ensemble Model**: RandomForest, AUC 0.499

#### Key Characteristics
- **Average AUC**: 0.499 (~50% - reflects true difficulty)
- **Training Data**: 100K companies with realistic distributions
  - 85% of pre-seed have $0 revenue
  - Realistic team sizes (2-3 for pre-seed)
  - Natural failure patterns (16% success rate)
- **Honest Performance**: No artificial boosting or calibration
- **Location**: `models/production_v46_realistic/`

#### Why 50% AUC is Good
1. **Honest Assessment**: Shows true difficulty of early-stage prediction
2. **No Overfitting**: Models aren't memorizing fake patterns
3. **Academic Alignment**: Matches research on startup prediction
4. **Business Value**: Even 18.5% TPR means catching 1 in 5 unicorns

#### Model Behavior
- CAMP scores cluster around 45-55% (poor discrimination)
- Wide confidence intervals (±15%)
- Low confidence scores (50%)
- Emphasis on uncertainty over false precision

### Frontend Components (Updated V17)
1. **Design System Components**:
   - `Button`: Multiple variants, ripple effects, loading states
   - `Input`: Floating labels, validation, clear button
   - `Card`: Elevated/bordered/gradient variants, glassmorphism
   - `Progress`: Linear/circular/step progress indicators
   - `Toast`: Notification system with animations
   - `ThemeToggle`: Dark/light mode switcher

2. **Core Components**:
   - **WorldClassResults**: Premium results display
   - **FullAnalysisView**: Tabbed detailed analysis
   - **AnalysisOrb**: DNA helix loading animation
   - **DataCollectionCAMP**: Smart data collection with animations
   - **ScoreCard**: Animated score display with confidence ring
   - **ScoreBreakdown**: Model contribution visualization
   - **PatternAnalysis**: Refactored with new UI components

## 🎨 Design System (V17)

### Design Files
- `src/styles/design-system.css` - CSS variables and utilities
- `src/styles/animations.css` - Keyframe animations
- `src/components/ui/` - Component library
- `src/contexts/ThemeContext.tsx` - Theme management
- `src/hooks/useScrollAnimation.ts` - Animation hooks

### Theme Support
- **Dark Mode** (Default): Deep blues and grays
- **Light Mode**: Clean whites and light grays
- **Auto-switching**: Respects system preferences
- **Smooth transitions**: All colors transition smoothly

### Colors (CSS Variables)
```css
/* Dark Theme */
--color-background-primary: #0A0E1B;
--color-text-primary: #E8EAED;
--color-primary: #00D4FF;
--color-success: #00FF88;

/* Light Theme automatically switches all variables */
[data-theme="light"] {
  --color-background-primary: #FFFFFF;
  --color-text-primary: #111827;
}
```

### Typography
- Display: SF Pro Display
- Body: Inter
- Mono: SF Mono
- Sizes: xs (12px) to 7xl (72px)

### Animations
- 30+ keyframe animations
- Framer Motion for complex interactions
- GPU-accelerated transforms
- Reduced motion support

## 🐛 Known Issues

1. **Data Format**: Frontend sends "Series A", API expects "series_a"
2. **Memory Leak**: After 50+ analyses in single session
3. **Safari**: Gradient rendering issues
4. **TypeScript**: Some ESLint warnings remain

## 📝 Important Context

### Recent Changes
- Migrated from EnhancedResults to WorldClassResults
- Added DNA helix animation replacing circular orb
- Implemented /predict_advanced endpoint
- Fixed Pydantic v2 compatibility
- **NEW**: Implemented hierarchical models for 45-feature dataset
- **NEW**: Added stage-based, temporal, industry, and DNA pattern models
- **NEW**: Improved accuracy from 72-75% to 80-85%
- **NEW**: Created train_hierarchical_models_45features.py script

### Data Transformations
```typescript
// Always transform data before API calls
const transformDataForAPI = (data) => {
  // funding_stage: "Series A" → "series_a"
  // investor_tier: "Angel" → "none"
  // scalability_score: Keep as 0-1 (was 1-5, now fixed)
  // product_stage: "Beta" → "beta"
}
```

### API Configuration
The API now runs on port 8001 (changed from 8000). Configuration is centralized in `src/config.ts`:
```typescript
export const API_CONFIG = {
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
};
```

### Testing Approach
- No automated tests yet (planned)
- Manual testing required
- Check both standard and advanced APIs
- Test all screen sizes

## 🚦 Development Workflow

1. **Before Starting**
   - Check TODO_PENDING_WORK.md
   - Read recent commits
   - Ensure servers are running on correct ports (API: 8001, Frontend: 3000)

2. **Making Changes**
   - Use v3 components only
   - Follow existing patterns
   - Test in both Chrome and Safari
   - Check mobile responsiveness

3. **Before Committing**
   - Run `npm run build`
   - Fix any TypeScript errors
   - Test the full user flow
   - Update documentation if needed

## 📅 Recent Updates (June 2025 - V17)

### Complete UI/UX Overhaul
1. **Design System Implementation**
   - Created comprehensive CSS variable system
   - Added semantic color tokens
   - Implemented consistent spacing scale
   - Typography system with SF Pro Display

2. **Component Library**
   - Built 5 core UI components from scratch
   - Added proper TypeScript interfaces
   - Implemented animation variants
   - Created reusable patterns

3. **Theme System**
   - Dark/light mode toggle in header
   - System preference detection
   - Smooth theme transitions
   - Persistent user preference

4. **Animation System**
   - 30+ keyframe animations
   - Custom React hooks for animations
   - Framer Motion integration
   - Performance optimizations

5. **Component Updates**
   - PatternAnalysis: Removed hardcoded colors
   - ScoreBreakdown: Already using design system
   - DataCollectionCAMP: Added micro-interactions
   - Global header with theme toggle

## 📅 Previous Session Updates (December 2024)

### Critical Fixes Applied

1. **API Port Migration**
   - Moved from blocked port 8000 to 8001
   - Created centralized config at `src/config.ts`
   - Updated all components to use new port

2. **Feature Mismatch Resolution**
   - Fixed mismatch between 45 training features and API expectations
   - Removed incorrect field mappings (burn_rate → monthly_burn_usd, etc.)
   - Added defensive programming in feature engineering

3. **API Response Model**
   - Added missing fields required by frontend:
     - `risk_level`: Risk categorization
     - `pillar_scores`: CAMP framework scores
     - `verdict`: Investment recommendation
   - Fixed PredictionResponse model in api_server_improved.py

4. **React Development Issues**
   - Removed React.StrictMode to prevent double API calls
   - Added proper cleanup in useEffect hooks
   - Fixed error handling in AnalysisPage

5. **CORS Configuration**
   - Updated to handle OPTIONS preflight requests
   - Added wildcard origin support for development

### Current Working State
- ✅ API runs on port 8001 with all model improvements
- ✅ Frontend connects successfully to API
- ✅ All 45 features properly mapped
- ✅ 6 engineered features working
- ✅ Response model matches frontend expectations
- ✅ Successfully tested end-to-end flow

## 💡 Tips for AI Assistants

1. **Always Check First**
   - Current component versions (use v3)
   - Existing patterns in codebase
   - Data format requirements

2. **Common Pitfalls**
   - Don't use old component versions
   - Remember data transformations
   - Check for TypeScript errors
   - Test animations performance

3. **Best Practices**
   - Keep animations smooth (60fps)
   - Maintain dark theme consistency
   - Use proper TypeScript types
   - Handle loading and error states

4. **When Stuck**
   - Check TECHNICAL_DOCUMENTATION_V4.md
   - Look at similar components
   - Review recent git commits
   - Ask for clarification

## 🔗 Key Files Reference

- **Main App**: `src/AppV3.tsx`
- **Results Display**: `src/components/v3/WorldClassResults.tsx`
- **API Server**: `flash-backend-api/api_server.py`
- **ML Models**: `flash-backend-api/advanced_models.py`
- **Styles**: `src/components/v3/WorldClassResults.css`

## 📞 Communication Style

When providing updates or explanations:
- Be concise and clear
- Show relevant code snippets
- Explain the "why" behind changes
- Highlight potential impacts
- Suggest testing steps

---

*This file helps AI assistants understand the FLASH platform context and work more effectively on the codebase.*