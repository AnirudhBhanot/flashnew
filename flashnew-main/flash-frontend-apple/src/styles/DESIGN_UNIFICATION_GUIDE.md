# Design Unification Guide - Johnny Ive Aesthetic

## Overview
This guide ensures all FLASH components follow the minimalist Johnny Ive-inspired design system.

## Quick Start
1. Import the unified design system in all SCSS files:
   ```scss
   @import '../../styles/unified-design-system.scss';
   ```

2. Replace all hardcoded values with CSS variables
3. Use mixins for consistent component styles
4. Remove all shadows and gradients

## Key Principles

### 1. **Minimalism First**
- Pure white backgrounds (#ffffff)
- Subtle borders instead of shadows
- No gradients or heavy effects
- Clean, spacious layouts

### 2. **Typography Hierarchy**
```scss
// Use these mixins instead of hardcoded values:
@include text-hero;      // 72px headlines
@include text-title;     // 32px section titles  
@include text-subtitle;  // 28px subtitles
@include text-body;      // 20px body text
```

### 3. **Color Restraint**
- Primary text: #1d1d1f
- Secondary text: #86868b
- Borders: rgba(0, 0, 0, 0.08)
- Accents used sparingly: #007aff (blue), #34c759 (green)

### 4. **Component Patterns**

#### Cards
```scss
.card {
  @include card-minimal;
  // No additional shadows or effects needed
}
```

#### Buttons
```scss
.button {
  @include button-minimal;    // Default style
  @include button-primary;    // Primary actions
}
```

#### Progress Bars
```scss
.progress {
  @include progress-bar;
  // Thin 4px bars, no gradients
}
```

### 5. **Spacing Rhythm**
Use consistent spacing variables:
- `var(--space-xxs)`: 8px
- `var(--space-xs)`: 12px
- `var(--space-sm)`: 16px
- `var(--space-md)`: 24px
- `var(--space-lg)`: 32px
- `var(--space-xl)`: 48px
- `var(--space-xxl)`: 80px

### 6. **Animation & Interaction**
- Use `var(--easing-default)`: cubic-bezier(0.25, 0, 0, 1)
- Keep durations subtle: 200-300ms
- Hover effects: slight transforms, no color changes
- Focus states: blue border, no shadows

## Migration Checklist

### For Deep Dive Components:
- [ ] Replace `#f8f9fa` backgrounds with `var(--color-background)`
- [ ] Replace custom grays with design system colors
- [ ] Remove all `box-shadow` properties
- [ ] Remove all gradient backgrounds
- [ ] Update font sizes to use mixins
- [ ] Replace rem units with pixel-based variables
- [ ] Update border radius to use variables
- [ ] Fix button styles to use mixins

### For Framework Intelligence:
- [ ] Remove gradient backgrounds from cards
- [ ] Update shadow styles to use borders
- [ ] Replace custom colors with system colors
- [ ] Update typography to use mixins
- [ ] Fix spacing to use variables
- [ ] Remove heavy hover effects

## Common Anti-Patterns to Avoid

### ❌ Don't Do This:
```scss
// Heavy shadows
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

// Gradient backgrounds
background: linear-gradient(90deg, #4CAF50 0%, #2196F3 100%);

// Hardcoded colors
color: #666;
background: #f8f9fa;

// Inconsistent spacing
padding: 2rem;
margin-bottom: 3rem;

// Custom font sizes
font-size: 2.5rem;
font-weight: 700;
```

### ✅ Do This Instead:
```scss
// Subtle borders
border: 1px solid var(--color-border);

// Solid colors
background: var(--color-surface);

// System colors
color: var(--color-text-secondary);
background: var(--color-background);

// Consistent spacing
padding: var(--space-lg);
margin-bottom: var(--space-xl);

// Typography mixins
@include text-title;
```

## Glass Morphism Effect
For elevated surfaces, use the glass morphism mixin:
```scss
.elevatedCard {
  @include glass-morphism;
  // Creates subtle blur effect with light borders
}
```

## Testing Your Implementation

1. **Visual Consistency Check**:
   - All text should use system fonts
   - Colors should match the minimal palette
   - No heavy shadows or gradients visible
   - Consistent spacing throughout

2. **Interaction Check**:
   - Hover states are subtle (transform/opacity)
   - Animations use consistent easing
   - Focus states use blue borders

3. **Responsiveness Check**:
   - Components scale gracefully
   - Typography remains readable
   - Spacing adjusts proportionally

## Component-Specific Notes

### Deep Dive Phases
- Use minimal cards with subtle borders
- Progress indicators should be thin (4px)
- Phase numbers in circles with surface background
- No colored backgrounds for phase states

### Framework Intelligence
- Tab navigation with surface background
- Cards with minimal borders, no shadows
- Scores displayed with light font weight
- Tags and pills with full border radius

### Results Page
- Already follows the design system
- Reference for other components
- Uses proper glass morphism effects
- Minimal color usage

## Resources
- Main design system: `/styles/unified-design-system.scss`
- Results page reference: `/pages/Results/ResultsV2Enhanced.module.scss`
- Icon library: Custom SVG components in `/design-system/icons/`

Remember: When in doubt, choose the simpler option. Less is more.