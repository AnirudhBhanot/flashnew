# Flash Frontend Apple - Johnny Ive Design Backup

**Backup Date**: June 10, 2025 - 09:18:29
**Backup Type**: Complete frontend with Johnny Ive-level minimalist design

## What's Included

### Minimalist Design System
- `/src/design-system/minimalist/` - Complete minimalist component library
  - FormField - Progressive disclosure wrapper
  - MinimalInput - Large typography inputs
  - MinimalSelect - Clean dropdowns
  - MinimalToggle - Elegant toggles
  - MinimalScale - Visual scale selectors
  - MinimalProgress - Subtle progress indicators

### Redesigned Pages
1. **Landing Page** (`/src/pages/Landing/`)
   - Ultra-minimal hero with 96px headline
   - Single "Begin" CTA
   - Extreme whitespace

2. **Company Info** (`/src/pages/Assessment/CompanyInfo/`)
   - Progressive field disclosure
   - Large typography inputs
   - Matches CAMP form aesthetics

3. **Capital Form** (`/src/pages/Assessment/Capital/`)
   - 72px input typography
   - One question at a time
   - Automatic calculations

4. **Advantage Form** (`/src/pages/Assessment/Advantage/`)
   - Typography-first design
   - Unique textarea overlay
   - Visual moat counter

5. **Market Form** (`/src/pages/Assessment/Market/`)
   - Progressive disclosure
   - TAM/SAM/SOM visualization
   - Clean sector selection

6. **People Form** (`/src/pages/Assessment/People/`)
   - Founder icon visualization
   - Team statistics
   - Optional engagement metrics

### Key Features
- **45 Backend Features**: All properly mapped in `/src/services/api.ts`
- **CAMP Structure**: 4 main sections (Capital, Advantage, Market, People)
- **SF Pro Typography**: Throughout the design
- **Minimal Color Palette**: 99% grayscale with subtle blue accent
- **Smooth Animations**: Framer Motion with Apple easing curves

### Design Principles
1. Ultra-minimalist aesthetic
2. Typography-first approach
3. Progressive disclosure
4. Subtle interactions
5. Color restraint

## How to Restore

```bash
# From the FLASH directory
cp -r backups/flash-frontend-apple-johnny-ive-20250610-091829/* flash-frontend-apple/
cd flash-frontend-apple
npm install
npm start
```

## Important Files
- `/src/styles/minimalist-global.scss` - Global minimalist styles
- `/src/design-system/minimalist/` - All minimalist components
- All CAMP forms have both original and minimalist versions