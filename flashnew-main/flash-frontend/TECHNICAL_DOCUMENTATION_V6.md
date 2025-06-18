# FLASH Platform - Technical Documentation V6

## Recent Updates (January 8, 2025)

### Professional UI Transformation
- **Emoji Removal**: Replaced all emojis with professional SVG icons throughout the platform
- **Color Scheme Update**: Changed from blue accent (#00d4ff) to white/grayscale palette
- **ScoreCard Redesign**: Complete overhaul with modern glassmorphism design
- **Page-wide Animations**: Added animated background effects across entire application
- **Component Consistency**: Ensured uniform design language across all components

### Key Changes
- **Icons**: 30+ custom SVG icons replacing emoji characters
- **Primary Accent**: #00d4ff → #FFFFFF (white)
- **Secondary Colors**: Blue variants → Grayscale palette
- **Visual Effects**: Blue glows → White glows and shadows

See `DESIGN_TRANSFORMATION_V6.md` for detailed documentation.

## System Architecture

### Frontend (React TypeScript)
```
flash-frontend/
├── src/
│   ├── styles/
│   │   ├── design-system.css      # Design tokens (updated to white/gray)
│   │   └── animations.css         # Animation library
│   ├── components/
│   │   ├── ui/                    # V17 Component library
│   │   │   ├── Button.tsx         # Ripple effects, variants
│   │   │   ├── Input.tsx          # Floating labels
│   │   │   ├── Card.tsx           # Glassmorphism
│   │   │   ├── Progress.tsx       # Linear/circular/steps
│   │   │   └── Toast.tsx          # Notifications
│   │   └── v3/                    # Core components
│   │       ├── ScoreCard.tsx      # NEW: Modern redesign
│   │       ├── AnalysisResults.tsx # Updated: Professional icons
│   │       ├── DataCollectionCAMP.tsx
│   │       ├── AnalysisPage.tsx
│   │       └── WorldClassResults.tsx
│   ├── contexts/
│   │   └── ThemeContext.tsx       # Theme management
│   ├── AppV3.tsx                  # Main app
│   └── index.tsx                  # Entry point
├── public/
└── package.json
```

### Backend (Python FastAPI)
```
flash-backend-api/
├── api_server_unified.py          # Unified API server (port 8001)
├── models/
│   └── production_v46_realistic/  # Current production models
│       ├── dna_analyzer.pkl       # DNA pattern analyzer
│       ├── temporal_model.pkl     # Time-based predictions
│       ├── industry_model.pkl     # Industry-specific model
│       └── ensemble_model.pkl     # Combined predictions
├── utils/
│   ├── data_validation.py         # Input validation
│   └── feature_engineering.py     # Feature processing
└── requirements.txt
```

## Design System Updates (V6)

### Color Palette Changes
```css
/* Previous (Blue Accent) → Current (White/Gray) */
--color-primary: #00D4FF → #FFFFFF
--color-primary-dark: #0099CC → #E8EAED
--color-primary-light: #66E5FF → #FFFFFF
--color-border-interactive: rgba(0, 212, 255, 0.3) → rgba(255, 255, 255, 0.3)
--shadow-glow: 0 0 20px rgba(0, 212, 255, 0.4) → 0 0 20px rgba(255, 255, 255, 0.2)
```

### Score Color Mapping
```typescript
// ScoreCard and visualizations now use:
Excellent (75%+): #FFFFFF (white)
Good (50-75%): #E8EAED (light gray)
Fair (25-50%): #9CA3AF (medium gray)
Poor (0-25%): #6B7280 (dark gray)
```

### Icon System
All emojis replaced with custom SVG icons:
- 📊 → Bar chart icon
- 🎯 → Target/crosshair icon
- 💡 → Lightbulb icon
- 🚀 → Rocket/growth icon
- 💰 → Currency/dollar icon
- ⚡ → Lightning bolt icon
- 📈 → Growth chart icon
- 👥 → People/team icon
- ✓ → Checkmark in circle
- ⚠️ → Warning triangle
- And 20+ more custom icons

## API Endpoints

### Base URL
```
http://localhost:8001
```

### Core Endpoints

#### 1. Prediction Endpoint
```http
POST /predict
Content-Type: application/json

{
  "company_name": "string",
  "funding_stage": "pre_seed|seed|series_a|series_b|series_c_plus",
  "sector": "saas|fintech|healthtech|...",
  "monthly_revenue": number,
  "team_size": number,
  // ... 45 total features
}

Response:
{
  "success_probability": 0.0-1.0,
  "confidence": "low|moderate|high",
  "verdict": "PASS|FAIL",
  "risk_level": "low|medium|high",
  "pillar_scores": {
    "capital": 0.0-1.0,
    "advantage": 0.0-1.0,
    "market": 0.0-1.0,
    "people": 0.0-1.0
  }
}
```

#### 2. Configuration Endpoint
```http
GET /config/all

Response:
{
  "field_options": {
    "funding_stage": ["pre_seed", "seed", ...],
    "sector": ["saas", "fintech", ...],
    // ... all dropdown options
  }
}
```

#### 3. Analysis Status (LLM)
```http
GET /api/analysis/status

Response:
{
  "status": "ready|processing|error",
  "cached_results": number,
  "last_update": "timestamp"
}
```

#### 4. Dynamic Recommendations (LLM)
```http
POST /api/analysis/recommendations/dynamic
Content-Type: application/json

{
  "stage": "seed",
  "industry": "fintech",
  "camp_scores": {...},
  "context": {...}
}

Response:
{
  "recommendations": [...],
  "generated_at": "timestamp"
}
```

## Model Architecture

### Current Models (V46 Realistic)
- **Average AUC**: 49.9% (realistic difficulty)
- **Training Data**: 100K companies with natural patterns
- **Success Rate**: 16% (matches real-world data)

### Model Types
1. **DNA Analyzer**: RandomForest identifying startup patterns
2. **Temporal Model**: XGBoost for time-based predictions
3. **Industry Model**: XGBoost for sector-specific insights
4. **Ensemble Model**: RandomForest combining all signals

### Feature Engineering
- 45 canonical features
- 6 engineered features (ratios, growth rates)
- Handles up to 40% missing data
- Outlier robust (5% black swan events)

## Frontend Components

### Component Library (V17)
All new UI components with consistent design:

#### Button Component
- Multiple variants: primary, secondary, ghost, danger
- Ripple effects on click
- Loading states with spinner
- Icon support (left/right)
- Size variants: sm, md, lg

#### Input Component
- Floating labels
- Validation states
- Clear button
- Icon support
- Error messages

#### Card Component
- Elevated, bordered, gradient variants
- Glassmorphism effects
- Hover animations
- Click interactions

#### Progress Component
- Linear progress bars
- Circular progress rings
- Step indicators
- Animated transitions

#### Toast Component
- Success, error, warning, info variants
- Auto-dismiss
- Action buttons
- Stacking support

### Core Components

#### ScoreCard (V2 - Complete Redesign)
- Modern glassmorphism design
- Animated gradient orbs
- SVG-based score display
- Professional metric cards
- White accent colors
- Responsive layout

#### AnalysisResults (Updated)
- All emojis replaced with SVG icons
- Page-wide background animations
- Professional navigation tabs
- ScoreCard-inspired section designs
- Consistent white/gray color scheme

#### DataCollectionCAMP
- Smart form with validation
- Real-time field updates
- Progress indicator
- Micro-interactions
- Professional styling

#### WorldClassResults
- Premium results display
- Tabbed interface
- Investment memo generation
- Export functionality
- Professional icons

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- npm or yarn

### Frontend Setup
```bash
cd flash-frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Backend Setup
```bash
cd flash-backend-api
pip install -r requirements.txt
python api_server_unified.py  # Runs on http://localhost:8001
```

### Environment Variables
Create `.env` in frontend:
```
REACT_APP_API_URL=http://localhost:8001
```

## Theme System

### Theme Support
- Dark mode (default)
- Light mode
- System preference detection
- Smooth transitions
- Persistent user preference

### Theme Switching
```typescript
// ThemeContext provides:
const { theme, toggleTheme } = useTheme();
// theme: 'light' | 'dark'
// toggleTheme: () => void
```

### CSS Variables
All colors automatically switch based on theme:
```css
/* Dark theme (default) */
[data-theme="dark"] {
  --color-background-primary: #0A0E1B;
  --color-text-primary: #E8EAED;
}

/* Light theme */
[data-theme="light"] {
  --color-background-primary: #FFFFFF;
  --color-text-primary: #111827;
}
```

## Animation System

### Keyframe Animations (30+)
- fadeIn, fadeOut
- slideIn (all directions)
- scaleIn, scaleOut
- rotate, spin
- pulse, bounce
- shimmer, glow
- float animations
- And more...

### Framer Motion Integration
- Page transitions
- Component animations
- Gesture animations
- Scroll animations
- Stagger effects

### Performance Optimizations
- GPU-accelerated transforms
- will-change hints
- Reduced motion support
- Animation throttling

## Testing

### Manual Testing Checklist
- [ ] Form submission with all fields
- [ ] Form submission with minimal fields
- [ ] API error handling
- [ ] Loading states
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] Theme switching
- [ ] Icon rendering (no emoji fallbacks)
- [ ] Animation performance
- [ ] Cross-browser compatibility
- [ ] White accent visibility/contrast

### Test Data
```json
{
  "company_name": "Test Startup",
  "funding_stage": "seed",
  "sector": "fintech",
  "monthly_revenue": 50000,
  "team_size": 15,
  "burn_rate": 100000,
  "months_of_runway": 12
}
```

## Performance Optimizations

### Frontend
- CSS transforms for GPU acceleration
- Will-change for smooth animations
- Code splitting by route
- Lazy loading heavy components
- Optimized SVG rendering
- Memoized color calculations

### Backend
- Model caching in memory
- Request validation shortcuts
- Efficient feature engineering
- LLM response caching

## Deployment

### Frontend Build
```bash
npm run build
# Output in build/ directory
```

### Backend Deployment
```bash
# Using gunicorn
gunicorn api_server_unified:app -w 4 -k uvicorn.workers.UvicornWorker

# Or uvicorn directly
uvicorn api_server_unified:app --host 0.0.0.0 --port 8001
```

### Production Considerations
- Enable CORS for production domain
- Set up proper logging
- Configure rate limiting
- Implement authentication
- Set up monitoring
- Optimize asset delivery

## Troubleshooting

### Common Issues

#### Icons Not Rendering
- Check SVG syntax
- Verify viewBox attributes
- Check fill/stroke colors use currentColor

#### White Accent Too Bright
- Adjust opacity values
- Use off-white (#F9FAFB) if needed
- Check contrast ratios

#### API Connection Failed
- Check backend is running on port 8001
- Verify CORS settings
- Check network tab for errors

#### Predictions Always Low
- This is by design (realistic models)
- Average success rate is 16%
- Most predictions will be 20-60%

#### Style Issues
- Clear browser cache
- Check design-system.css is imported
- Verify CSS variable names
- Check theme context

#### Performance Issues
- Check for animation loops
- Profile React re-renders
- Monitor API response times
- Reduce animation complexity

## Future Roadmap

### Immediate
- [x] Remove all emojis
- [x] Update to white accent colors
- [x] Redesign ScoreCard
- [x] Add page-wide animations
- [ ] Complete component library
- [ ] Add more micro-interactions

### Near Term
- [ ] Automated testing framework
- [ ] Performance monitoring
- [ ] A/B testing infrastructure
- [ ] Advanced analytics
- [ ] Accessibility audit

### Long Term
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Real-time collaboration
- [ ] AI-powered insights
- [ ] White-label options

## Contributing

### Code Style
- TypeScript with strict mode
- ESLint configuration
- Prettier formatting
- Conventional commits
- No emojis in production code
- Use SVG icons exclusively

### Icon Guidelines
- Always use currentColor for fills/strokes
- Include proper viewBox
- Keep icons simple and recognizable
- Test in both themes
- Maintain consistent stroke widths

### Pull Request Process
1. Create feature branch
2. Update documentation
3. Test all changes
4. Verify no emojis remain
5. Submit PR with description
6. Address review feedback

## Version History

- **V6** (January 2025): Professional UI transformation
- **V5** (June 2025): Major UI/UX overhaul
- **V4** (May 2025): Realistic model implementation
- **V3** (April 2025): LLM integration
- **V2** (March 2025): CAMP framework
- **V1** (February 2025): Initial release

---
**Last Updated**: January 8, 2025
**Current Version**: 6.0
**Status**: Production Ready with Professional UI