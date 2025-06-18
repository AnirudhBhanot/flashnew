# Framework System Migration Plan

## Phase 1: Backend Migration (Priority: HIGH)

### 1.1 Update api_michelin_enhanced.py
- [ ] Replace IntelligentFrameworkSelector with EnhancedFrameworkSelector
- [ ] Update framework selection calls to use new API
- [ ] Test with FLASH data

### 1.2 Update Prompt Engineering
- [ ] Modify DeepSeek prompts to leverage new framework metadata
- [ ] Include industry-specific metrics in prompts
- [ ] Add anti-pattern warnings in analysis

### 1.3 Update Other Endpoints
- [ ] api_framework_analysis_endpoints.py
- [ ] api_framework_intelligent.py
- [ ] Any other framework-using endpoints

## Phase 2: Frontend Integration (Priority: MEDIUM)

### 2.1 Update API Calls
- [ ] Switch from /api/frameworks/recommend to /api/frameworks/enhanced/select
- [ ] Handle new response format with journey data
- [ ] Display confidence scores and rationale

### 2.2 UI Enhancements
- [ ] Show framework fit scores
- [ ] Display journey timeline
- [ ] Add industry variant indicators

## Phase 3: Testing & Validation (Priority: HIGH)

### 3.1 End-to-End Testing
- [ ] Test with pre-seed SaaS (should get JTBD, not BCG)
- [ ] Test with Series B marketplace (should get BCG with GMV/Take Rate)
- [ ] Test crisis mode (3 month runway)
- [ ] Test different industries

### 3.2 Prompt Engineering Validation
- [ ] Ensure DeepSeek uses correct metrics
- [ ] Validate industry-specific insights
- [ ] Check anti-pattern handling

## Phase 4: Documentation (Priority: LOW)

### 4.1 API Documentation
- [ ] Document new endpoints
- [ ] Provide migration guide
- [ ] Update examples

### 4.2 User Documentation
- [ ] Explain framework selection logic
- [ ] Document industry variants
- [ ] Add troubleshooting guide

## Technical Debt to Address

1. **Circular Dependencies**: intelligent_framework_selector imports from integrated_framework_selector
2. **Duplicate Code**: Framework selection logic exists in multiple places
3. **Inconsistent Naming**: "Intelligent" vs "Enhanced" vs "Advanced"
4. **Missing Tests**: Need comprehensive test suite for new system

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing integrations | HIGH | Maintain backwards compatibility |
| Performance degradation | MEDIUM | Add caching layer |
| Incorrect framework selection | HIGH | Extensive testing |
| DeepSeek prompt failures | MEDIUM | Fallback mechanisms |

## Success Metrics

- [ ] 90%+ of framework selections are contextually appropriate
- [ ] No BCG Matrix for <20 person teams
- [ ] Industry variants used 100% of time when applicable
- [ ] Frontend displays journey planning
- [ ] DeepSeek generates industry-specific insights