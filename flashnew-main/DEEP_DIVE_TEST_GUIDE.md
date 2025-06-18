# Deep Dive Testing Guide

## Services Running
✅ **API Server**: http://localhost:8001 (with JSON parsing fixes)
✅ **Frontend**: http://localhost:3000

## Testing Steps

### 1. Access the Application
Open your browser and go to: **http://localhost:3000**

### 2. Complete Assessment First (Required)
The Deep Dive system requires assessment data. You can:
- **Option A**: Use the Autofill feature (click "Autofill with Sample Data")
- **Option B**: Fill out the assessment manually

Complete all assessment pages:
1. Company Info
2. Capital
3. Advantage
4. Market
5. People
6. Review & Submit

### 3. Navigate to Results
After submitting the assessment, you'll be taken to the Results page.

### 4. Access Deep Dive
On the Results page, look for the **"Start Progressive Deep Dive →"** button and click it.

### 5. Test Each Phase

#### Phase 1: Context Mapping
- **External Reality Check**: Porter's Five Forces analysis
- **Internal Audit**: CAMP framework deep dive
- Click "Get AI Insights" to test LLM integration
- Complete both assessments and proceed

#### Phase 2: Strategic Alignment
- **Vision-Reality Gap**: Define vision and assess current reality
- **Ansoff Matrix**: Choose growth strategy
- Test the AI analysis features

#### Phase 3: Organizational Readiness
- **7S Framework**: Assess all seven elements
- Check if AI recommendations appear

#### Phase 4: Risk-Weighted Pathways
- **Scenario Planning**: Create and evaluate scenarios
- Test Monte Carlo simulations
- Build decision tree

#### Phase 5: Synthesis
- Review the executive summary
- Check if all previous phase data is integrated

## What to Look For

### ✅ Success Indicators
- Data persists between pages (stored in localStorage)
- AI insights load without errors
- All phases are unlocked and accessible
- Forms save data automatically
- Navigation between phases works smoothly

### ⚠️ Potential Issues
- If AI insights fail, the system should use fallback data
- Check browser console for any errors
- Verify data is being saved (check localStorage in DevTools)

## API Endpoints Being Tested

1. **Phase 1**: POST `/api/analysis/deepdive/phase1/analysis`
2. **Phase 2**: POST `/api/analysis/deepdive/phase2/analysis`
3. **Phase 3**: POST `/api/analysis/deepdive/phase3/analysis`
4. **Phase 4**: POST `/api/analysis/deepdive/phase4/analysis`
5. **Synthesis**: POST `/api/analysis/deepdive/synthesis`

## Browser DevTools Commands

To check stored data:
```javascript
// View all Deep Dive data
Object.keys(localStorage).filter(k => k.includes('deepDive')).forEach(k => {
  console.log(k, JSON.parse(localStorage.getItem(k)));
});
```

To clear Deep Dive data (if needed):
```javascript
// Clear all Deep Dive data
Object.keys(localStorage).filter(k => k.includes('deepDive')).forEach(k => {
  localStorage.removeItem(k);
});
```

## Quick Test Checklist

- [ ] Can access Deep Dive from Results page
- [ ] Phase 1: External Reality saves data
- [ ] Phase 1: Internal Audit saves data
- [ ] Phase 1: AI Insights button works
- [ ] Phase 2: Vision-Reality Gap works
- [ ] Phase 2: Ansoff Matrix selection works
- [ ] Phase 3: 7S Framework assessment works
- [ ] Phase 4: Scenario planning works
- [ ] Phase 5: Synthesis shows summary
- [ ] Data persists when navigating between phases
- [ ] No console errors in browser DevTools

## Troubleshooting

1. **"onComplete is not a function" error**: Fixed in the code, should not appear
2. **JSON parsing errors**: Fixed with enhanced parsing, API now handles malformed JSON
3. **Phases locked**: All phases are now unlocked by default
4. **No AI insights**: Check if DeepSeek API is responding (fallback will be used)

## API Testing Commands

Test individual endpoints:
```bash
# Test Phase 1 endpoint
curl -X POST http://localhost:8001/api/analysis/deepdive/phase1/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "porters_five_forces": {
      "supplier_power": {"rating": "Medium", "factors": ["Limited suppliers"], "score": 6.5},
      "buyer_power": {"rating": "High", "factors": ["Many alternatives"], "score": 7.8},
      "competitive_rivalry": {"rating": "High", "factors": ["Many competitors"], "score": 8.2},
      "threat_of_substitution": {"rating": "Medium", "factors": ["Some alternatives"], "score": 5.5},
      "threat_of_new_entry": {"rating": "Low", "factors": ["High barriers"], "score": 3.2}
    },
    "internal_audit": {
      "strengths": ["Strong team"],
      "weaknesses": ["Limited marketing"],
      "opportunities": ["Growing market"],
      "threats": ["Economic uncertainty"]
    }
  }'
```

---
**Ready to test!** Open http://localhost:3000 and follow the steps above.