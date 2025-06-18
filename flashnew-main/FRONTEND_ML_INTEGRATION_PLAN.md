# Frontend ML Integration Plan
## Bridging the Gap to 100% Integration

### Current State: 70% Integrated
### Target State: 100% Integration with ML Infrastructure

---

## Priority 1: Critical Security Fix 🚨

### Implement Authentication
**Files to modify:**
- `src/utils/api.ts` - Add auth headers
- `src/config.ts` - Add auth configuration
- `src/App.tsx` - Add auth context

**Implementation:**
```typescript
// utils/api.ts
const getAuthHeaders = () => {
  const apiKey = localStorage.getItem('FLASH_API_KEY');
  const token = localStorage.getItem('FLASH_JWT_TOKEN');
  
  if (token) {
    return { 'Authorization': `Bearer ${token}` };
  } else if (apiKey) {
    return { 'X-API-Key': apiKey };
  }
  return {};
};

export const makePrediction = async (data: StartupData) => {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify(data)
  });
  
  if (response.status === 401) {
    throw new Error('Authentication required');
  }
  
  return response.json();
};
```

---

## Priority 2: Core ML Features 🎯

### 1. Model Information Display
**New Component:** `ModelInfoPanel.tsx`
```typescript
interface ModelInfo {
  orchestrator_version: string;
  total_models: number;
  model_types: string[];
  pattern_count: number;
  integrity_status: 'healthy' | 'compromised';
}

const ModelInfoPanel: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  
  useEffect(() => {
    fetch('/models/info', { headers: getAuthHeaders() })
      .then(res => res.json())
      .then(setModelInfo);
  }, []);
  
  return (
    <Card>
      <Typography variant="h6">ML System Status</Typography>
      <Chip label={`${modelInfo?.total_models} Models`} color="primary" />
      <Chip label={`${modelInfo?.pattern_count} Patterns`} color="secondary" />
      <Chip 
        label={modelInfo?.integrity_status || 'Unknown'} 
        color={modelInfo?.integrity_status === 'healthy' ? 'success' : 'error'}
      />
    </Card>
  );
};
```

### 2. Real-time Performance Monitoring
**New Component:** `ModelPerformanceMonitor.tsx`
```typescript
const ModelPerformanceMonitor: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  
  // Poll for updates every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchPerformanceMetrics();
      fetchActiveAlerts();
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        <MetricsChart data={metrics} />
      </Grid>
      <Grid item xs={12} md={6}>
        <AlertsList alerts={alerts} />
      </Grid>
    </Grid>
  );
};
```

### 3. Enhanced Error Handling
**Update:** `utils/errorHandling.ts`
```typescript
export const handleMLError = (error: any) => {
  if (error.code === 'MODEL_DRIFT_DETECTED') {
    return 'Our models are being updated for better accuracy. Please try again in a few minutes.';
  }
  
  if (error.code === 'INTEGRITY_CHECK_FAILED') {
    return 'Security verification failed. Please contact support.';
  }
  
  if (error.code === 'SERVICE_UNAVAILABLE') {
    return 'ML system is temporarily unavailable. Using cached predictions.';
  }
  
  return 'An unexpected error occurred. Please try again.';
};
```

---

## Priority 3: Advanced ML Features 🚀

### 1. Model Version Display
**Update:** `ModelContributions.tsx`
```typescript
// Add version info to existing component
interface ModelContribution {
  model: string;
  accuracy: number;
  contribution: number;
  version?: string;
  deployed_at?: string;
}

// Display version info
<Tooltip title={`Version: ${model.version} | Deployed: ${model.deployed_at}`}>
  <Typography variant="body2">{model.model}</Typography>
</Tooltip>
```

### 2. Feedback Collection
**New Component:** `PredictionFeedback.tsx`
```typescript
const PredictionFeedback: React.FC<{predictionId: string}> = ({ predictionId }) => {
  const [outcome, setOutcome] = useState<'success' | 'failure' | null>(null);
  
  const submitFeedback = async () => {
    await fetch('/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify({
        features_hash: predictionId,
        actual_outcome: outcome === 'success' ? 1.0 : 0.0
      })
    });
  };
  
  return (
    <Card>
      <Typography>Was this prediction accurate?</Typography>
      <ButtonGroup>
        <Button onClick={() => setOutcome('success')}>Yes</Button>
        <Button onClick={() => setOutcome('failure')}>No</Button>
      </ButtonGroup>
      <Button onClick={submitFeedback} disabled={!outcome}>
        Submit Feedback
      </Button>
    </Card>
  );
};
```

### 3. A/B Test Results Display
**New Component:** `ABTestDashboard.tsx`
```typescript
const ABTestDashboard: React.FC = () => {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Experiment</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Winner</TableCell>
            <TableCell>Improvement</TableCell>
            <TableCell>Confidence</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {experiments.map(exp => (
            <TableRow key={exp.name}>
              <TableCell>{exp.name}</TableCell>
              <TableCell>
                <Chip 
                  label={exp.status}
                  color={exp.status === 'completed' ? 'success' : 'warning'}
                />
              </TableCell>
              <TableCell>{exp.winner || '-'}</TableCell>
              <TableCell>
                {exp.results?.relative_improvement 
                  ? `+${(exp.results.relative_improvement * 100).toFixed(1)}%`
                  : '-'}
              </TableCell>
              <TableCell>
                {exp.results?.p_value 
                  ? `${((1 - exp.results.p_value) * 100).toFixed(1)}%`
                  : '-'}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
```

---

## Implementation Timeline

### Week 1: Security & Core Integration
- [ ] Implement authentication (JWT/API key)
- [ ] Add error handling for ML-specific errors
- [ ] Create model info display panel
- [ ] Update API calls with auth headers

### Week 2: Monitoring & Feedback
- [ ] Add performance monitoring dashboard
- [ ] Implement alert display system
- [ ] Create feedback collection UI
- [ ] Add model version information

### Week 3: Advanced Features
- [ ] Build A/B test results dashboard
- [ ] Add drift detection notifications
- [ ] Implement model comparison view
- [ ] Create ML system health dashboard

### Week 4: Polish & Testing
- [ ] Add loading states for ML operations
- [ ] Implement caching for ML metadata
- [ ] Create comprehensive error boundaries
- [ ] Add integration tests

---

## New UI Components Needed

1. **MLSystemStatus** - Overall ML health indicator
2. **ModelVersionBadge** - Show current model versions
3. **PerformanceMetrics** - Real-time performance charts
4. **AlertNotifications** - ML system alerts
5. **FeedbackWidget** - Collect prediction outcomes
6. **ABTestResults** - Experiment dashboard
7. **ModelComparison** - Compare model performances
8. **DriftIndicator** - Show when models need retraining

---

## API Integration Checklist

- [ ] `/auth/login` - User authentication
- [ ] `/models/info` - Model information
- [ ] `/models/integrity` - Integrity status
- [ ] `/models/versions` - Version history
- [ ] `/monitoring/performance` - Performance metrics
- [ ] `/monitoring/alerts` - Active alerts
- [ ] `/monitoring/report` - Full report
- [ ] `/experiments/results` - A/B test results
- [ ] `/feedback` - Submit outcomes

---

## Success Metrics

1. **Authentication Coverage**: 100% of API calls authenticated
2. **Error Handling**: Graceful degradation for all ML failures
3. **Monitoring Integration**: Real-time metrics displayed
4. **User Feedback**: >10% of predictions get feedback
5. **Performance**: <200ms additional latency from ML features

---

**Estimated Effort**: 4 weeks for full integration
**Priority**: P0 - Authentication, P1 - Core ML, P2 - Advanced Features
**Result**: 100% integrated frontend with complete ML observability