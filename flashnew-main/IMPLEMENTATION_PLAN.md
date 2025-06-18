# Detailed Implementation Plan for FLASH Integration

## Overview
This plan details the exact steps to integrate all fixes and ensure seamless frontend-backend communication.

## Phase 1: Prepare Working API Server
1. **Backup current working server**
   - Copy api_server_working.py to api_server_working_backup.py
   
2. **Verify server can start**
   - Check dependencies
   - Ensure models load correctly

## Phase 2: Integrate Type Converter
1. **Import type converter module**
   - Add import statement at top of api_server_working.py
   
2. **Update predict endpoint**
   - Wrap incoming data with convert_frontend_data()
   - Test with sample data

3. **Update all POST endpoints**
   - Apply same conversion to predict_enhanced
   - Apply to analyze_pattern

## Phase 3: Add Missing Endpoints
1. **Add endpoint aliases**
   - /predict_simple → /predict
   - /predict_advanced → /predict_enhanced
   - /investor_profiles (new implementation)

2. **Test each endpoint**
   - Verify routing works
   - Check response format

## Phase 4: Create Response Transformer
1. **Map backend fields to frontend expectations**
   - confidence_score → confidence_interval
   - prediction_components → pillar_scores
   - Add missing fields with defaults

2. **Ensure all required fields present**
   - verdict (PASS/FAIL/CONDITIONAL PASS)
   - strength (STRONG/MODERATE/WEAK/CRITICAL)
   - critical_failures array
   - below_threshold array

## Phase 5: Integration Testing
1. **Start updated server**
   - Check logs for errors
   - Verify all models load

2. **Run integration tests**
   - Test type conversions
   - Test all endpoints
   - Verify response formats

3. **Frontend testing**
   - Test with actual frontend
   - Check browser console for errors
   - Verify data flow

## Phase 6: Documentation Update
1. **Update API documentation**
   - Document all endpoints
   - Show example requests/responses

2. **Update README**
   - New setup instructions
   - Environment variables

## Success Criteria
- [ ] All endpoints return 200/201
- [ ] No type conversion errors
- [ ] Frontend receives expected format
- [ ] No console errors
- [ ] All tests pass

## Rollback Plan
If issues occur:
1. Restore api_server_working_backup.py
2. Document specific error
3. Fix and retry