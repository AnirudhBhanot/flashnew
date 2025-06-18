# Testing Frontend LLM Integration

## 1. Start the Backend API Server

```bash
cd /Users/sf/Desktop/FLASH
python3 api_server_unified.py
```

Wait for: "INFO:     Application startup complete."

## 2. Start the Frontend Dev Server

In a new terminal:
```bash
cd /Users/sf/Desktop/FLASH/flash-frontend
npm start
```

## 3. Test the Integration

### Step 1: Initial Analysis
1. Open http://localhost:3000
2. Click "Start Analysis"
3. Fill in startup data:
   - Funding Stage: Series A
   - Sector: SaaS
   - Annual Revenue: 2000000
   - Growth Rate: 150%
   - Monthly Burn: 200000
   - Team Size: 25
4. Complete all CAMP sections
5. Submit the form

### Step 2: Check AI Features

#### A. Recommendations Tab
- Look for the "✨ AI-Powered Recommendations" badge
- Recommendations should be specific to your startup
- Each should have:
  - Specific action title
  - Why it matters
  - How to do it (steps)
  - Timeline
  - Expected impact

#### B. CAMP Tab - What-If Analysis
1. Expand any CAMP pillar (e.g., Capital)
2. Look for "🤖 AI-powered predictions based on real startup data"
3. Select 2-3 improvements
4. Click "Get AI Analysis"
5. You should see:
   - AI Prediction with confidence interval
   - Timeline for improvements
   - Realistic impact assessment

### Step 3: Monitor Network Tab

1. Open Browser DevTools (F12)
2. Go to Network tab
3. Filter by "api/analysis"
4. You should see:
   - `/api/analysis/status` - Checking LLM availability
   - `/api/analysis/recommendations/dynamic` - Getting AI recommendations
   - `/api/analysis/whatif/dynamic` - When clicking "Get AI Analysis"

### Step 4: Test Fallback

1. Stop the API server (Ctrl+C)
2. Refresh the page and do another analysis
3. The app should still work with static recommendations
4. No AI badges should appear

## Expected Results

### With LLM Working:
- ✨ AI badges on recommendations
- 🤖 AI indicator on What-If analysis
- Personalized, industry-specific recommendations
- Realistic predictions with confidence intervals
- ~15-20 second load time for AI features

### With LLM Unavailable:
- No AI badges
- Static recommendations based on rules
- Basic What-If calculations
- Instant results (no API calls)

## Troubleshooting

### "Failed to fetch LLM recommendations"
- Check API server is running on port 8001
- Check browser console for errors
- Verify DeepSeek API key in .env

### No AI Features Showing
- Check Network tab for API calls
- Look for `/api/analysis/status` response
- Should return `{"status": "operational"}`

### Slow Performance
- AI features take 15-20 seconds (normal)
- Check if Redis is running for caching
- Monitor API server logs

## Success Indicators

1. **Visual**: AI badges and indicators appear
2. **Content**: Recommendations are specific and contextual
3. **Behavior**: What-If shows realistic predictions
4. **Fallback**: App works without API server
5. **Performance**: Results appear within 20 seconds