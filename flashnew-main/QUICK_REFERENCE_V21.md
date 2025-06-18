# FLASH V21 Quick Reference Guide

## New Features Overview

### 1. Progressive Deep Dive (`/deep-dive`)
Strategic analysis system with 4 phases + synthesis

### 2. Framework Intelligence Engine
AI-powered recommendations from 500+ business frameworks

## Progressive Deep Dive Routes

```
/deep-dive                    # Main navigation
/deep-dive/phase1            # Context Mapping
/deep-dive/phase2            # Strategic Alignment  
/deep-dive/phase3            # Organizational Readiness
/deep-dive/phase4            # Risk-Weighted Pathways
/deep-dive/synthesis         # Executive Summary
```

## Framework Intelligence API

### Get Recommendations
```bash
curl -X POST http://localhost:8001/api/frameworks/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "company_stage": "seed",
    "industry": "fintech",
    "primary_challenge": "finding_product_market_fit",
    "team_size": 10,
    "resources": "limited",
    "timeline": "3-6 months",
    "goals": ["achieve_product_market_fit"],
    "current_frameworks": []
  }'
```

### Generate Roadmap
```bash
curl -X POST http://localhost:8001/api/frameworks/roadmap \
  -H "Content-Type: application/json" \
  -d '{
    "company_stage": "growth",
    "industry": "saas",
    "primary_challenge": "scaling_operations",
    "team_size": 50,
    "resources": "moderate",
    "timeline": "6-12 months",
    "goals": ["scale_revenue", "improve_efficiency"]
  }'
```

### Search Frameworks
```bash
curl "http://localhost:8001/api/frameworks/search?query=lean&category=Innovation"
```

## localStorage Keys

### Progressive Deep Dive Data
- `externalRealityData` - Porter's Five Forces scores
- `internalAuditData` - CAMP deep dive assessment
- `visionRealityGapData` - Vision and reality scores
- `ansoffMatrixData` - Growth strategy allocations
- `sevenSFrameworkData` - 7S assessment data
- `scenarioPlanningData` - Scenario definitions

### Clear Deep Dive Data
```javascript
// In browser console
localStorage.removeItem('externalRealityData');
localStorage.removeItem('internalAuditData');
localStorage.removeItem('visionRealityGapData');
localStorage.removeItem('ansoffMatrixData');
localStorage.removeItem('sevenSFrameworkData');
localStorage.removeItem('scenarioPlanningData');
```

## Component Locations

### Progressive Deep Dive Components
```
src/pages/DeepDive/
├── index.tsx                          # Main navigation
├── Phase1_Context/
│   ├── ExternalReality.tsx           # Porter's Five Forces
│   └── InternalAudit.tsx             # CAMP deep dive
├── Phase2_Strategic/
│   ├── VisionRealityGap.tsx          # Gap analysis
│   └── AnsoffMatrix.tsx              # Growth strategies
├── Phase3_Organizational/
│   └── SevenSFramework.tsx           # 7S assessment
├── Phase4_RiskPathways/
│   └── ScenarioPlanning.tsx          # Monte Carlo
└── Synthesis/
    └── index.tsx                      # Executive summary
```

### Framework Intelligence
```
src/components/
└── FrameworkIntelligence.tsx         # Main component

backend/
├── framework_intelligence/            # Engine module
└── api_framework_endpoints.py        # API endpoints
```

## Quick Start

### 1. Start Backend
```bash
cd /Users/sf/Desktop/FLASH
python api_server_unified.py
```

### 2. Start Frontend
```bash
cd /Users/sf/Desktop/FLASH/flash-frontend-apple
npm start
```

### 3. Access Features
- Main app: http://localhost:3000
- Deep Dive: http://localhost:3000/deep-dive
- API docs: http://localhost:8001/docs

## Testing New Features

### Test Progressive Deep Dive
1. Complete initial assessment
2. Go to results page
3. Click "Deep Dive Analysis" button
4. Complete phases 1-4 sequentially
5. Review synthesis

### Test Framework Intelligence
1. Go to results page
2. Expand "Framework Intelligence" section
3. View recommendations based on your context
4. Switch between tabs:
   - Recommendations
   - Implementation Roadmap
   - Framework Combinations

## Common Commands

### Run Framework Tests
```bash
cd framework_intelligence
python test_framework_engine.py
```

### Expand Framework Database
```bash
python expand_frameworks.py
```

### Check API Health
```bash
curl http://localhost:8001/health
```

## Troubleshooting

### Issue: Deep Dive phases locked
**Solution**: Complete previous phases first (sequential unlocking)

### Issue: No framework recommendations
**Solution**: Check API server is running and DeepSeek API key is set

### Issue: Data not persisting
**Solution**: Check localStorage is enabled in browser

### Issue: CORS errors
**Solution**: Ensure frontend URL is in CORS origins in api_server_unified.py

## Key Files Modified in V21

### Frontend
- `src/App.tsx` - Added Deep Dive routes
- `src/pages/Results/ResultsV2Enhanced.tsx` - Added Framework Intelligence
- `src/components/index.ts` - Exported new components

### Backend
- `api_server_unified.py` - Added framework router
- `api_framework_endpoints.py` - New framework endpoints
- `framework_intelligence/*` - New module

## Framework Categories

1. **Strategy** - SWOT, Porter's, Blue Ocean, BCG Matrix
2. **Innovation** - Design Thinking, Lean Startup, Jobs to be Done
3. **Growth** - AARRR, Growth Loops, PLG, T2D3
4. **Financial** - Unit Economics, LTV/CAC, Burn Rate
5. **Operations** - Lean, Six Sigma, Agile, DevOps
6. **Marketing** - 4Ps, STP, Customer Journey, Content
7. **Product** - Kano Model, RICE, MVP, Product Lifecycle
8. **Leadership** - Situational, Transformational, EQ
9. **Organizational** - 7S, Culture, OKRs, Balanced Scorecard

---

**Version**: V21 (December 2024)
**New Components**: 20+
**New Frameworks**: 500+
**New API Endpoints**: 7