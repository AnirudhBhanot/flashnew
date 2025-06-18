#!/usr/bin/env python3
"""
Test that different funding stages produce different stage weights in the frontend
"""

print("""
TESTING INSTRUCTIONS:

1. Open the frontend at http://localhost:3000
2. Start filling the form and test each funding stage:

TEST CASES:
-----------

Test 1: Pre-seed
- Select "Pre-seed" as funding stage
- Complete the form
- Check "What Matters Most" section
- Should show: People (40%) > Advantage (30%) > Market (20%) > Capital (10%)

Test 2: Seed  
- Select "Seed" as funding stage
- Complete the form
- Check "What Matters Most" section
- Should show: People (30%) = Advantage (30%) > Market (25%) > Capital (15%)

Test 3: Series A
- Select "Series A" as funding stage
- Complete the form
- Check "What Matters Most" section
- Should show: Market (30%) > People (25%) = Advantage (25%) > Capital (20%)

Test 4: Series B
- Select "Series B" as funding stage
- Complete the form
- Check "What Matters Most" section
- Should show: Market (35%) > Capital (25%) > Advantage (20%) = People (20%)

Test 5: Series C
- Select "Series C" as funding stage
- Complete the form
- Check "What Matters Most" section
- Should show: Capital (35%) > Market (30%) > People (20%) > Advantage (15%)

WHAT TO LOOK FOR:
-----------------
1. The "What Matters Most at [Stage] Stage" title should match your selection
2. The order and percentages should change based on the stage
3. The colored bars should reflect the percentages
4. The descriptions should match the priorities

If all stages show "Series A" or the same weights, the fix didn't work.
""")