# FLASH - Apple Design System
## A Native Apple Experience for Startup Assessment

### Design Philosophy

Following Apple's principles of clarity, deference, and depth, FLASH will embody:

1. **Clarity** - Content is paramount, with pristine typography and purposeful layouts
2. **Deference** - The interface steps back to highlight content and functionality
3. **Depth** - Realistic motion and layered interfaces provide context and hierarchy

### Core Design Principles

#### 1. Simplicity Through Sophistication
- Remove all unnecessary elements
- Every pixel has purpose
- White space is a design element
- Progressive disclosure of complexity

#### 2. Native Platform Integration
- Feels like a built-in Apple app
- Respects system preferences (appearance, accent color, accessibility)
- Uses platform conventions (gestures, navigation patterns)
- Seamless integration with Apple ecosystem

#### 3. Human-Centered Design
- Intuitive without instruction
- Forgiving of mistakes
- Delightful micro-interactions
- Accessibility as a core feature

### Visual Language

#### Color System

```css
/* Light Mode (Default) */
--apple-bg-primary: #FFFFFF;
--apple-bg-secondary: #F2F2F7; /* System Gray 6 */
--apple-bg-tertiary: #FFFFFF;
--apple-bg-elevated: #FFFFFF;

--apple-label-primary: #000000;
--apple-label-secondary: rgba(60, 60, 67, 0.6);
--apple-label-tertiary: rgba(60, 60, 67, 0.3);
--apple-label-quaternary: rgba(60, 60, 67, 0.18);

--apple-separator: rgba(60, 60, 67, 0.12);
--apple-opaque-separator: #C6C6C8;

/* System Colors */
--apple-blue: #007AFF;
--apple-green: #34C759;
--apple-indigo: #5856D6;
--apple-orange: #FF9500;
--apple-pink: #FF2D55;
--apple-purple: #AF52DE;
--apple-red: #FF3B30;
--apple-teal: #5AC8FA;
--apple-yellow: #FFCC00;

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  --apple-bg-primary: #000000;
  --apple-bg-secondary: #1C1C1E;
  --apple-bg-tertiary: #2C2C2E;
  --apple-bg-elevated: #1C1C1E;
  
  --apple-label-primary: #FFFFFF;
  --apple-label-secondary: rgba(235, 235, 245, 0.6);
  --apple-label-tertiary: rgba(235, 235, 245, 0.3);
  
  --apple-separator: rgba(84, 84, 88, 0.6);
}
```

#### Typography

```css
/* SF Pro Display for large titles */
--apple-font-largeTitle: -apple-system-ui-serif, ui-serif;
--apple-font-display: -apple-system, BlinkMacSystemFont, "SF Pro Display";
--apple-font-text: -apple-system, BlinkMacSystemFont, "SF Pro Text";
--apple-font-rounded: -apple-system-ui-rounded, -apple-system;

/* Type Scale */
--apple-text-largeTitle: 34px;    /* Large Title */
--apple-text-title1: 28px;        /* Title 1 */
--apple-text-title2: 22px;        /* Title 2 */
--apple-text-title3: 20px;        /* Title 3 */
--apple-text-headline: 17px;      /* Headline - Semibold */
--apple-text-body: 17px;          /* Body */
--apple-text-callout: 16px;       /* Callout */
--apple-text-subheadline: 15px;   /* Subheadline */
--apple-text-footnote: 13px;      /* Footnote */
--apple-text-caption1: 12px;      /* Caption 1 */
--apple-text-caption2: 11px;      /* Caption 2 */

/* Font Weights */
--apple-font-weight-regular: 400;
--apple-font-weight-medium: 500;
--apple-font-weight-semibold: 600;
--apple-font-weight-bold: 700;
```

#### Spacing & Layout

```css
/* Apple Standard Spacing */
--apple-spacing-xs: 4px;
--apple-spacing-s: 8px;
--apple-spacing-m: 16px;
--apple-spacing-l: 20px;
--apple-spacing-xl: 24px;
--apple-spacing-xxl: 32px;

/* Safe Areas */
--apple-safe-area-top: env(safe-area-inset-top);
--apple-safe-area-bottom: env(safe-area-inset-bottom);

/* Corner Radius */
--apple-radius-small: 6px;
--apple-radius-medium: 10px;
--apple-radius-large: 14px;
--apple-radius-xl: 20px;
```

### Component Library

#### 1. Navigation Bar
- Blurred background with vibrancy
- Large title that transitions to inline on scroll
- Right-aligned action buttons
- Back button with custom labeling

#### 2. Buttons

**Primary Button**
```jsx
<Button variant="primary">
  Continue
</Button>
```
- Filled with system blue
- 50px height (large), 44px (medium), 34px (small)
- Corner radius: 12px (large), 10px (medium), 8px (small)
- Subtle shadow on press

**Secondary Button**
```jsx
<Button variant="secondary">
  Learn More
</Button>
```
- System gray background
- Same sizing as primary

**Text Button**
```jsx
<Button variant="text">
  Skip
</Button>
```
- No background
- System blue text
- Subtle opacity change on press

#### 3. Input Fields

**Text Field**
```jsx
<TextField
  label="Company Name"
  placeholder="Enter your company name"
  helper="This will be used to personalize your analysis"
/>
```
- Rounded rect background (System Gray 6)
- Floating label OR inline label
- 44px minimum height
- Clear button when filled
- Subtle focus ring

#### 4. Cards

**Content Card**
```jsx
<Card elevated>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>
```
- White/elevated background
- Subtle shadow in light mode
- 14px corner radius
- Hover state with slight scale

#### 5. Lists

**Table View Style**
```jsx
<List>
  <ListItem
    leading={<Icon name="chart" />}
    title="Revenue Growth"
    subtitle="Year over year"
    trailing="150%"
    accessory="chevron"
  />
</List>
```
- Inset separators
- 44px minimum row height
- Chevron for navigation
- Swipe actions support

### Animation System

#### Core Animations

1. **Spring Animations** (Primary)
```javascript
const springConfig = {
  mass: 1,
  stiffness: 300,
  damping: 30
};
```

2. **Ease Curves**
```css
--apple-ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
--apple-ease-in-out: cubic-bezier(0.45, 0, 0.55, 1);
--apple-ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
```

3. **Duration Standards**
```css
--apple-duration-instant: 0.1s;
--apple-duration-fast: 0.2s;
--apple-duration-regular: 0.3s;
--apple-duration-slow: 0.4s;
--apple-duration-sleepy: 0.5s;
```

#### Signature Animations

1. **Rubber Band** (Scroll Boundaries)
2. **Zoom Transition** (Navigation)
3. **Slide Over** (Modals)
4. **Magic Move** (Shared Element Transitions)
5. **Ripple** (Touch Feedback)

### Page Designs

#### 1. Landing Page

**Hero Section**
- Large title: "Assess Your Startup's Potential"
- Subtitle in system gray
- Primary CTA: "Begin Assessment"
- Secondary: "See How It Works"
- Animated gradient mesh background (subtle)

**Features Grid**
- 2x2 grid of feature cards
- SF Symbols for icons
- Hover states with slight lift
- Each card has title + description

**Trust Section**
- Centered testimonials
- Company logos in grayscale
- Smooth carousel with dots indicator

#### 2. Assessment Wizard

**Progress Indicator**
- Segmented control style at top
- Animated fill as user progresses
- Labels appear on desktop, hidden on mobile

**Question Cards**
- One question per screen
- Large, readable typography
- Input appropriate to data type
- "Continue" button activates when valid

**Navigation**
- Back button always available
- Skip option for optional fields
- Keyboard navigation support
- Smooth transitions between steps

#### 3. Analysis Page

**Loading State**
- Apple-style activity indicator
- Subtle pulsing of UI elements
- Progress messages that update
- Estimated time remaining

**Visualization**
- Animated circular progress rings
- Gradient fills for scores
- Smooth number counting animations
- Interactive hover states

#### 4. Results Page

**Score Display**
- Large circular visualization
- Animated fill on load
- Score counter animation
- Color coding (green/yellow/red)

**Insights Cards**
- Vertical stack of cards
- Each with icon, title, and detail
- Expandable for more information
- Share button per insight

**Recommendations**
- Priority ordered list
- Actionable items with checkboxes
- Time estimates for each
- Export to Notes/Reminders

### Interaction Patterns

#### Gestures
- **Swipe to go back** (iOS navigation)
- **Pull to refresh** (Update analysis)
- **Long press** (Context menus)
- **Pinch to zoom** (Charts)
- **3D Touch/Haptic Touch** (Quick actions)

#### Feedback
- **Haptic feedback** on interactions
- **Sound effects** for success/error
- **Visual feedback** immediate
- **Loading states** never block UI
- **Error states** helpful and actionable

### Responsive Design

#### Breakpoints
```css
/* Apple-style breakpoints */
--apple-compact: 320px;   /* iPhone SE */
--apple-regular: 390px;   /* iPhone 14 */
--apple-medium: 744px;    /* iPad Mini */
--apple-large: 1024px;    /* iPad Pro 11" */
--apple-xlarge: 1366px;   /* iPad Pro 12.9" */
--apple-xxlarge: 1920px;  /* Desktop */
```

#### Adaptive Layouts
- **Compact**: Single column, stacked elements
- **Regular**: Optimized for one-handed use
- **Medium+**: Multi-column layouts
- **Large+**: Sidebar navigation
- **XLarge+**: Full desktop experience

### Accessibility

#### Built-in Support
- **VoiceOver** full compatibility
- **Dynamic Type** support
- **Reduce Motion** alternatives
- **High Contrast** mode
- **Keyboard Navigation** complete

#### ARIA Implementation
```jsx
<Button
  role="button"
  aria-label="Begin startup assessment"
  aria-describedby="assessment-description"
>
  Begin Assessment
</Button>
```

### Platform-Specific Features

#### iOS/iPadOS
- Widget for quick score check
- Shortcuts integration
- Share sheet integration
- iCloud sync for data
- Handoff support

#### macOS
- Menu bar integration
- Touch Bar support (older Macs)
- Keyboard shortcuts throughout
- Native window management
- Quick Look preview

### Implementation Technologies

#### Core Stack
```json
{
  "framework": "React with TypeScript",
  "styling": "CSS Modules + CSS Variables",
  "animations": "Framer Motion",
  "icons": "SF Symbols (via API)",
  "charts": "Swift Charts (via WebView) or D3",
  "state": "Zustand",
  "routing": "React Router"
}
```

#### Key Dependencies
```json
{
  "react": "^18.2.0",
  "framer-motion": "^11.0.0",
  "d3": "^7.8.0",
  "zustand": "^4.4.0",
  "react-router-dom": "^6.20.0",
  "@react-spring/web": "^9.7.0"
}
```

### File Structure
```
src/
├── design-system/
│   ├── tokens/
│   ├── components/
│   └── layouts/
├── pages/
│   ├── Landing/
│   ├── Assessment/
│   ├── Analysis/
│   └── Results/
├── features/
│   ├── wizard/
│   ├── scoring/
│   └── insights/
└── shared/
    ├── animations/
    ├── hooks/
    └── utils/
```

This design system brings FLASH to Apple's standards, creating an experience that feels native, intuitive, and delightful while maintaining the sophisticated analysis capabilities of the platform.