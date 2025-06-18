# FLASH Codebase Mismatches Report

## Executive Summary
A comprehensive scan of the FLASH codebase revealed several critical mismatches that could cause runtime failures. The most critical issues are port configuration differences, missing API endpoints, and data type inconsistencies between frontend and backend.

## Critical Mismatches Found

### 1. 🔴 Port Configuration Mismatch
**Issue**: Frontend and backend are configured for different ports

**Details**:
- **Backend config** (`config.py`): Default port 8000
- **Frontend config** (`flash-frontend/src/config.ts`): Expects port 8001
- **API servers**: Some use 8000, others use 8001

**Impact**: Frontend cannot connect to backend without manual configuration

**Fix Required**:
```typescript
// Frontend should check both ports or use environment variable
API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8001'
```

### 2. 🔴 Missing API Endpoints
**Issue**: Frontend expects endpoints that don't exist in backend

**Missing Endpoints**:
- `/predict_simple` - Frontend expects this (config.ts line 12)
- `/predict_advanced` - Frontend expects this (config.ts line 13)
- `/investor_profiles` - Frontend expects this (config.ts line 19)

**Existing Endpoints**:
- `/predict` - Standard prediction
- `/predict_enhanced` - Enhanced with patterns
- `/analyze_pattern` - Pattern analysis

**Impact**: Frontend features will fail when calling missing endpoints

### 3. 🟡 Data Type Mismatches
**Issue**: Frontend sends booleans, backend expects 0/1 integers

**Affected Fields**:
```typescript
// Frontend (types.ts)
has_debt: boolean;
network_effects_present: boolean;
has_data_moat: boolean;
regulatory_advantage_present: boolean;
key_person_dependency: boolean;

// Backend expects
has_debt: 0 | 1;
network_effects_present: 0 | 1;
// etc.
```

**Impact**: Validation errors when submitting data

### 4. 🟡 Optional vs Required Fields
**Issue**: Frontend treats some fields as optional, backend requires all 45

**Frontend Optional Fields**:
- `runway_months?`
- `burn_multiple?`

**Backend**: Expects all 45 features to be present (validated in `feature_config.py`)

**Impact**: Missing field errors

### 5. 🟡 Extra Frontend Fields
**Issue**: Frontend has fields that backend doesn't recognize

**Extra Fields in Frontend**:
- `team_cohesion_score`
- `hiring_velocity_score`
- `diversity_score`
- `technical_expertise_score`

**Impact**: These fields are ignored by backend, potentially confusing users

### 6. 🟡 Model Path Inconsistencies
**Issue**: Multiple model directories and inconsistent references

**Found Paths**:
- `models/v2_enhanced/` (config.py)
- `models/production_v45/` (orchestrators)
- `models/dna_analyzer/` (multiple versions)
- `models/pattern_models/`
- `models/pattern_v2_simple/`

**Impact**: Confusion about which models are actually used

### 7. ⚠️ Environment Configuration
**Issue**: No clear environment setup documentation

**Missing**:
- `.env.example` file
- Clear documentation of required environment variables
- Default values for development

**Impact**: Difficult setup for new developers

## Verification Commands

```bash
# Check port references
grep -r "8000\|8001" --include="*.py" --include="*.ts" --include="*.tsx" .

# Check feature counts
grep -r "45\|46\|48\|49" --include="*.py" | grep -i feature

# Check model paths
find . -name "*.pkl" -type f | sort

# Check for boolean type usage
grep -r "boolean" flash-frontend/src/
```

## Recommended Fixes

### Immediate (High Priority)
1. **Standardize Port Configuration**
   - Update all components to use port 8001
   - Or add port detection logic

2. **Fix Missing Endpoints**
   - Either implement missing endpoints in backend
   - Or update frontend to use existing endpoints

3. **Add Type Conversion Layer**
   ```python
   # In API server
   def convert_frontend_types(data):
       # Convert booleans to 0/1
       for field in BOOLEAN_FIELDS:
           if field in data and isinstance(data[field], bool):
               data[field] = 1 if data[field] else 0
       return data
   ```

### Short Term
1. **Create Environment Template**
   ```bash
   # .env.example
   API_PORT=8001
   API_HOST=0.0.0.0
   REACT_APP_API_URL=http://localhost:8001
   ```

2. **Consolidate Model Paths**
   - Move all production models to single directory
   - Update all references

3. **Document API Contract**
   - Create OpenAPI/Swagger specification
   - Generate TypeScript types from backend

### Medium Term
1. **Add Integration Tests**
   - Test frontend-backend communication
   - Validate data formats

2. **Type Safety**
   - Use Pydantic models in backend
   - Generate TypeScript types from Pydantic

## Files Requiring Updates

1. **Frontend**:
   - `flash-frontend/src/config.ts` - Fix port and endpoints
   - `flash-frontend/src/types.ts` - Align field types
   - Components calling missing endpoints

2. **Backend**:
   - `config.py` - Standardize port
   - API servers - Add missing endpoints or type conversion
   - `feature_config.py` - Document boolean handling

3. **Documentation**:
   - Add `.env.example`
   - Update README with setup instructions
   - Document API endpoints

## Testing Checklist
- [ ] Frontend can connect to backend
- [ ] All API endpoints return expected data
- [ ] Boolean fields are handled correctly
- [ ] Optional fields have defaults
- [ ] Model loading uses correct paths
- [ ] Pattern system integration works
- [ ] No 404 errors in browser console
- [ ] No validation errors on data submission

## Conclusion
While the core functionality is solid, these mismatches could cause significant issues in production. The most critical fixes are:
1. Port standardization
2. API endpoint alignment
3. Type conversion for booleans

These issues should be addressed before deployment to ensure smooth operation.