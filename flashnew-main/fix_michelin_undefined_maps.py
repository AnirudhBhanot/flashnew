#!/usr/bin/env python3
"""
Fix the MichelinStrategicAnalysis component to handle undefined arrays properly
"""

import re

def fix_michelin_component():
    """Add null checks to all .map() calls in MichelinStrategicAnalysis component"""
    
    file_path = "/Users/sf/Desktop/FLASH/flash-frontend-apple/src/components/MichelinStrategicAnalysis.tsx"
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define replacements for specific problematic lines
    replacements = [
        # Line 407: strategic_priorities
        (
            r'{phase1\.swot_analysis\.strategic_priorities\.map\(',
            '{(phase1.swot_analysis.strategic_priorities || []).map('
        ),
        # Line 1014: key_recommendations
        (
            r'{phase3Data\.key_recommendations\.map\(',
            '{(phase3Data.key_recommendations || []).map('
        ),
        # Line 1022: critical_success_factors
        (
            r'{phase3Data\.critical_success_factors\.map\(',
            '{(phase3Data.critical_success_factors || []).map('
        ),
        # Line 1029: next_steps
        (
            r'{phase3Data\.next_steps\.map\(',
            '{(phase3Data.next_steps || []).map('
        ),
        # Line 1033: step.actions
        (
            r'{step\.actions\.map\(',
            '{(step.actions || []).map('
        ),
        # Also check for any other potential .map() calls on arrays that might be undefined
        # In the ansoff_matrix rendering
        (
            r'{phase2\.ansoff_matrix\.strategies\.map\(',
            '{(phase2.ansoff_matrix.strategies || []).map('
        ),
        # In the blue_ocean_strategy rendering
        (
            r'{Object\.entries\(phase2\.blue_ocean_strategy\)\.map\(',
            '{Object.entries(phase2.blue_ocean_strategy || {}).map('
        ),
        # In the growth_scenarios rendering
        (
            r'{phase2\.growth_scenarios\.map\(',
            '{(phase2.growth_scenarios || []).map('
        ),
        # In balanced_scorecard perspectives
        (
            r'{Object\.entries\(phase3\.balanced_scorecard\.perspectives\)\.map\(',
            '{Object.entries(phase3.balanced_scorecard.perspectives || {}).map('
        ),
        # In okr_framework quarters
        (
            r'{phase3\.okr_framework\.quarters\.map\(',
            '{(phase3.okr_framework.quarters || []).map('
        ),
        # In risk_mitigation
        (
            r'{phase3\.risk_mitigation\.map\(',
            '{(phase3.risk_mitigation || []).map('
        ),
        # In success_metrics
        (
            r'{phase3\.success_metrics\.map\(',
            '{(phase3.success_metrics || []).map('
        ),
        # Also fix objectives inside quarters
        (
            r'{quarter\.objectives\.map\(',
            '{(quarter.objectives || []).map('
        ),
        # Fix key_results inside objectives
        (
            r'{objective\.key_results\.map\(',
            '{(objective.key_results || []).map('
        ),
        # Fix mitigation_strategies in risks
        (
            r'{risk\.mitigation_strategies\.map\(',
            '{(risk.mitigation_strategies || []).map('
        ),
    ]
    
    # Apply all replacements
    original_content = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Check if any changes were made
    if content == original_content:
        print("No changes needed - looking for alternative patterns...")
        
        # Try more generic pattern matching
        # Find all .map( occurrences and add null checks where needed
        lines = content.split('\n')
        modified_lines = []
        changes_made = 0
        
        for i, line in enumerate(lines):
            # Look for patterns like variable.property.map( or variable.map(
            # but exclude cases that already have null checks
            if '.map(' in line and ' || [])' not in line and '?' not in line:
                # Extract the variable being mapped
                map_match = re.search(r'(\w+(?:\.\w+)*?)\.map\(', line)
                if map_match:
                    var_name = map_match.group(1)
                    # Skip if it's a known safe method like Object.entries or Array methods
                    if not var_name.startswith(('Object.', 'Array.', '[', '(')):
                        # Replace the .map( with null-safe version
                        new_line = line.replace(f'{var_name}.map(', f'({var_name} || []).map(')
                        if new_line != line:
                            modified_lines.append(new_line)
                            changes_made += 1
                            print(f"Line {i+1}: Fixed {var_name}.map()")
                        else:
                            modified_lines.append(line)
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
        
        if changes_made > 0:
            content = '\n'.join(modified_lines)
            print(f"\nMade {changes_made} changes to add null checks")
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Fixed MichelinStrategicAnalysis component")
    print("Added null checks to prevent 'Cannot read properties of undefined' errors")
    print("\nThe component will now handle missing data gracefully by using empty arrays as defaults")
    print("\nPlease refresh your browser to see the changes take effect")

if __name__ == "__main__":
    fix_michelin_component()