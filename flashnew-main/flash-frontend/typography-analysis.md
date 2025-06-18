# FLASH Frontend Typography Analysis

## Overview
After analyzing all CSS files in the flash-frontend project, I've identified significant typography inconsistencies across components. The project has a design system defined but it's not being consistently used.

## Current Typography Patterns

### 1. Font Families
```css
/* Design System (defined in design-system.css) */
--font-family-display: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-family-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-family-mono: 'SF Mono', 'IBM Plex Mono', 'Roboto Mono', monospace;

/* Other font-family declarations found */
- InvestmentMemo.css: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif
- index.css (code): 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace
```

### 2. Font Size Usage

#### Design System Variables (defined but underutilized)
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
--font-size-6xl: 3.75rem;   /* 60px */
--font-size-7xl: 4.5rem;    /* 72px */
```

#### Actual Usage (mixed units and values)
- **Pixel-based**: 11px, 12px, 13px, 14px, 15px, 16px, 18px, 20px, 22px, 24px, 28px, 32px, 36px, 44px, 48px, 56px, 64px, 72px, 96px
- **Rem-based**: 0.75rem, 0.8rem, 0.85rem, 0.875rem, 0.9rem, 0.95rem, 1rem, 1.1rem, 1.125rem, 1.2rem, 1.25rem, 1.3rem, 1.5rem, 1.75rem, 1.8rem, 2rem, 2.5rem, 3rem, 4rem

### 3. Font Weight Patterns

#### Design System Variables
```css
--font-weight-thin: 200;
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

#### Actual Usage
- Numeric values: 400, 500, 600, 700, 800
- Keywords: bold, 600 (most common), 700 (second most common)
- Note: Design system thin (200) and light (300) weights are defined but never used

### 4. Line Height Usage

#### Design System Variables
```css
--line-height-tight: 1.2;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

#### Actual Usage
- Values found: 0.85, 1, 1.2, 1.4, 1.5, 1.6, 1.75
- Most components don't explicitly set line-height
- Inconsistent usage between components

### 5. Letter Spacing

#### Design System Variables
```css
--letter-spacing-tight: -0.02em;
--letter-spacing-normal: 0;
--letter-spacing-wide: 0.02em;
```

#### Actual Usage
- Values found: -0.03em, -0.02em, -0.01em, 0.025em, 0.05em, 0.5px, 1px
- Many components use custom letter-spacing values

## Key Inconsistencies Found

### 1. Mixed Unit Usage
- Some components use pixels (px) while others use rem
- No consistent pattern for when to use which unit

### 2. Arbitrary Font Sizes
- Many components define custom font sizes instead of using design system variables
- Examples:
  - AdvancedResultsPage: font-size: 3rem, 2.5rem, 1.8rem, 1.2rem, 0.9rem
  - AnalysisOrb: font-size: 72px, 32px, 18px, 14px, 12px
  - AppV3Dark: font-size: 96px, 64px, 48px, 24px

### 3. Inconsistent Typography Hierarchy
- No clear heading hierarchy (h1-h6) defined
- Different components use different sizes for similar content

### 4. Design System Underutilization
- ScoreCard.css and ScoreBreakdown.css properly use CSS variables
- Most other components hardcode values

### 5. Font Family Inconsistencies
- InvestmentMemo.css defines its own font stack
- Most components don't explicitly set font-family (inherit from body)

## Recommendations

### 1. Standardize on Design System Variables
- Replace all hardcoded font sizes with CSS variables
- Use rem units consistently (already defined in design system)

### 2. Define Typography Components
Create standard classes for:
- Headings (h1-h6)
- Body text variations
- Caption/label text
- Display text (for large numbers/scores)

### 3. Consolidate Font Weights
- Stick to the defined weights (400, 500, 600, 700)
- Remove unused thin (200) and light (300) from design system
- Consider if 800 weight is necessary

### 4. Standardize Line Heights
- Use design system line-height variables consistently
- Define specific line-heights for headings vs body text

### 5. Fix Letter Spacing
- Convert pixel-based letter-spacing to em units
- Use design system variables where appropriate

### 6. Create Typography Documentation
Document when to use:
- Display font vs body font
- Different heading levels
- Specific font sizes for different contexts

## Files Requiring Major Updates
1. AdvancedResultsPage.css - 20+ hardcoded font sizes
2. AppV3Dark.css - Large custom font sizes (96px, 64px)
3. AnalysisOrb.css - Mixed px and custom values
4. InvestmentMemo.css - Custom font-family definition
5. Most v3 component files - Need to adopt design system variables

## Next Steps
1. Update all components to use design system variables
2. Create utility classes for common typography patterns
3. Remove redundant/custom typography definitions
4. Ensure consistent hierarchy across all components
5. Test typography at different screen sizes