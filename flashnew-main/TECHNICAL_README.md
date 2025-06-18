# FLASH Platform Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Frontend Documentation](#frontend-documentation)
3. [Backend Documentation](#backend-documentation)
4. [Progressive Deep Dive System](#progressive-deep-dive-system)
5. [Framework Intelligence Engine](#framework-intelligence-engine)
6. [API Reference](#api-reference)
7. [Development Guide](#development-guide)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## System Architecture

### Overview
FLASH is a full-stack AI platform for startup assessment and strategic guidance.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Assessment  │  │   Results    │  │ Progressive      │   │
│  │   Wizard    │  │  Dashboard   │  │ Deep Dive        │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │                                    │
│                    Zustand Store                              │
└─────────────────────────┬────────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────┴────────────────────────────────────┐
│                     Backend (FastAPI)                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ ML Models   │  │ LLM Engine   │  │ Framework        │   │
│  │ (XGBoost)   │  │ (DeepSeek)   │  │ Intelligence     │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │                                    │
│                    Redis Cache                                │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack
- **Frontend**: React 18, TypeScript, SCSS Modules, Framer Motion
- **Backend**: Python 3.8+, FastAPI, scikit-learn, XGBoost
- **Database**: Redis (caching), localStorage (client persistence)
- **AI/ML**: Custom ensemble models, DeepSeek LLM integration
- **Infrastructure**: Docker-ready, CORS-enabled

## Frontend Documentation

### Project Structure
```
flash-frontend-apple/
├── public/
│   └── index.html
├── src/
│   ├── components/         # Reusable UI components
│   ├── pages/             # Route-based pages
│   │   ├── Assessment/    # Multi-step wizard
│   │   ├── Results/       # Analysis results
│   │   └── DeepDive/      # Strategic analysis
│   ├── services/          # API integration
│   ├── store/             # Zustand state management
│   ├── styles/            # Global styles
│   └── types/             # TypeScript definitions
└── package.json
```

### Key Components

#### Assessment Wizard
Multi-step form collecting 45 data points:
```typescript
// src/pages/Assessment/index.tsx
const steps = [
  'company-info',
  'capital',
  'advantage', 
  'market',
  'people'
];
```

#### Results Dashboard
Displays ML predictions and analysis:
```typescript
// src/pages/Results/ResultsV2Enhanced.tsx
- Success probability gauge
- CAMP framework scores
- Enhanced insights
- LLM recommendations
- Competitor analysis
- Framework Intelligence
```

#### Progressive Deep Dive
4-phase strategic analysis:
```typescript
// src/pages/DeepDive/
Phase1_Context/     // External + Internal analysis
Phase2_Strategic/   // Vision + Growth strategy
Phase3_Organizational/  // 7S Framework
Phase4_RiskPathways/    // Scenario planning
Synthesis/          // Executive summary
```

### State Management
Using Zustand for global state:
```typescript
// src/store/assessmentStore.ts
interface AssessmentState {
  data: AssessmentData;
  results: Results | null;
  setData: (data: Partial<AssessmentData>) => void;
  setResults: (results: Results) => void;
  reset: () => void;
}
```

### Styling System
SCSS modules with design tokens:
```scss
// src/styles/_variables.scss
:root {
  --accent-primary: #007aff;
  --background-primary: #ffffff;
  --text-primary: #1d1d1f;
  // ... more tokens
}
```

## Backend Documentation

### API Server
```python
# api_server_unified.py
app = FastAPI(
    title="FLASH API",
    version="2.0",
    description="Startup assessment and analysis platform"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### ML Models
Production v45 ensemble:
```python
# models/unified_orchestrator_v3_integrated.py
models = {
    'dna_analyzer': DNAAnalyzer,
    'temporal_model': TemporalDynamicsModel,
    'industry_model': IndustryBenchmarkModel,
    'ensemble_model': StartupSuccessEnsemble
}
```

### Framework Intelligence
```python
# framework_intelligence/framework_selector.py
class FrameworkSelector:
    def recommend_frameworks(self, context, top_n=10):
        # Multi-factor scoring algorithm
        scores = self._calculate_scores(context)
        return sorted(scores, key=lambda x: x['score'], reverse=True)[:top_n]
```

## Progressive Deep Dive System

### Phase 1: Context Mapping
- **External Reality Check**: Porter's Five Forces analysis
- **Internal Audit**: Deep CAMP framework assessment

### Phase 2: Strategic Alignment  
- **Vision-Reality Gap**: Assess alignment between vision and capabilities
- **Ansoff Matrix**: Growth strategy planning

### Phase 3: Organizational Readiness
- **7S Framework**: Evaluate organizational alignment

### Phase 4: Risk-Weighted Pathways
- **Scenario Planning**: Monte Carlo simulations for multiple futures

### Data Flow
```
User Input → localStorage → Analysis → Recommendations → Synthesis
```

## Framework Intelligence Engine

### Architecture
```
framework_intelligence/
├── framework_database.py   # 500+ framework definitions
├── framework_selector.py   # AI selection logic
└── api_framework_endpoints.py  # REST endpoints
```

### Scoring Algorithm
```python
weights = {
    'business_stage_alignment': 0.25,
    'challenge_relevance': 0.30,
    'industry_fit': 0.15,
    'complexity_match': 0.10,
    'goal_alignment': 0.10,
    'time_constraints': 0.05,
    'complementary_frameworks': 0.05
}
```

### Framework Categories
1. Strategy (50+ frameworks)
2. Innovation (50+ frameworks)
3. Growth (50+ frameworks)
4. Financial (50+ frameworks)
5. Operations (50+ frameworks)
6. Marketing (50+ frameworks)
7. Product (50+ frameworks)
8. Leadership (50+ frameworks)
9. Organizational (50+ frameworks)

## API Reference

### Core Endpoints

#### Health Check
```http
GET /health
```

#### Main Prediction
```http
POST /predict
Content-Type: application/json

{
  "founder_experience": 10,
  "total_funding": 1000000,
  "revenue_growth_rate": 150,
  // ... 42 more fields
}
```

#### Enhanced Analysis
```http
POST /analyze
Content-Type: application/json

{
  "features": { /* 45 features */ },
  "include_recommendations": true
}
```

### LLM Endpoints

#### Dynamic Recommendations
```http
POST /api/analysis/recommendations/dynamic
Content-Type: application/json

{
  "startup_data": { /* company context */ },
  "scores": { /* CAMP scores */ }
}
```

### Framework Intelligence Endpoints

#### Get Recommendations
```http
POST /api/frameworks/recommend
Content-Type: application/json

{
  "company_stage": "seed",
  "industry": "fintech",
  "primary_challenge": "finding_product_market_fit",
  "team_size": 10,
  "resources": "limited",
  "timeline": "3-6 months",
  "goals": ["achieve_pmf"],
  "current_frameworks": []
}
```

#### Generate Roadmap
```http
POST /api/frameworks/roadmap
Content-Type: application/json

{
  "company_stage": "growth",
  "industry": "saas",
  // ... context
}
```

## Development Guide

### Prerequisites
- Node.js 16+
- Python 3.8+
- Redis (optional)

### Frontend Setup
```bash
cd flash-frontend-apple
npm install
npm start  # Runs on http://localhost:3000
```

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start API server
python api_server_unified.py  # Runs on http://localhost:8001
```

### Environment Variables
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:8001
REACT_APP_API_KEY=your-api-key

# Backend (.env)
DEEPSEEK_API_KEY=your-deepseek-key
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
```

### Running Tests
```bash
# Frontend
npm test

# Backend
python -m pytest tests/

# Framework Intelligence
python framework_intelligence/test_framework_engine.py
```

## Deployment

### Docker Deployment
```dockerfile
# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]

# Backend Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api_server_unified:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Production Considerations
1. Enable HTTPS with SSL certificates
2. Set up proper CORS origins
3. Use production database (PostgreSQL/MongoDB)
4. Implement rate limiting
5. Set up monitoring (Prometheus/Grafana)
6. Configure auto-scaling
7. Implement proper logging

## Troubleshooting

### Common Issues

#### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

#### Backend Import Errors
```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

#### CORS Issues
```python
# In api_server_unified.py, ensure:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Redis Connection
```python
# In llm_analysis.py, Redis is optional:
try:
    client = redis.from_url(REDIS_URL)
    client.ping()
except:
    logger.warning("Redis not available, using in-memory cache")
```

### Performance Optimization

#### Frontend
- Enable React.lazy() for code splitting
- Use React.memo() for expensive components
- Implement virtual scrolling for long lists
- Optimize bundle size with tree shaking

#### Backend
- Use Redis caching for expensive operations
- Implement request batching
- Use async/await for I/O operations
- Enable gzip compression

### Monitoring
- Frontend: React DevTools, Performance tab
- Backend: FastAPI built-in /docs endpoint
- Logging: Structured logging with correlation IDs
- Metrics: Response times, error rates, cache hit rates

---

For additional support:
- GitHub Issues: [FLASH Repository](https://github.com/flash/platform)
- Documentation: [docs.flash.ai](https://docs.flash.ai)
- Email: support@flash.ai