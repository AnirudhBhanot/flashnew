# CAMP Naming Update Summary

## Changes Made (May 31, 2025)

### Recommendation Implemented
Based on user feedback, we've updated the UI to use CAMP framework names directly with business-friendly subtitles, rather than hiding CAMP behind generic business terms.

### Before vs After

| Before | After |
|--------|-------|
| Capital Efficiency | **Capital**<br/><small>Financial Health & Efficiency</small> |
| Competitive Advantage | **Advantage**<br/><small>Competitive Moat & Differentiation</small> |
| Market Opportunity | **Market**<br/><small>TAM Size & Growth Dynamics</small> |
| Team Quality | **People**<br/><small>Team Strength & Experience</small> |

### Benefits
1. **Brand Consistency**: CAMP framework is now visible throughout the application
2. **Educational Value**: Users learn and adopt the CAMP terminology
3. **Professional Credibility**: VCs appreciate the technical precision
4. **Clear Communication**: Business-friendly subtitles provide context without hiding the framework

### Files Updated
1. **WeightageExplanation.tsx**: 
   - Updated `getPillarDescription` to include subtitle field
   - Modified component to display CAMP names with subtitles
   
2. **WeightageExplanation.css**:
   - Added `.pillar-subtitle` styling for the business-friendly descriptions

### Visual Impact
- CAMP pillar names are displayed prominently (20px, bold)
- Subtitles appear below in smaller text (14px, gray)
- Clean hierarchy maintains readability while educating users

### Testing
All components verified to use consistent CAMP naming with no remaining business-only terms.

## Next Steps
Consider updating:
- Marketing materials to emphasize the CAMP framework
- Documentation to explain CAMP methodology  
- Onboarding to introduce users to CAMP terminology