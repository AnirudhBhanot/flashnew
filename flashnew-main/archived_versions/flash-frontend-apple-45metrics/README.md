# FLASH - Apple Design System Frontend

A complete reimagining of the FLASH platform following Apple's Human Interface Guidelines and design principles.

## 🎨 Design Philosophy

This implementation follows Apple's core principles:
- **Clarity** - Content is paramount with pristine typography
- **Deference** - The interface highlights content and functionality  
- **Depth** - Realistic motion and layered interfaces provide context

## 🚀 Getting Started

### Installation
```bash
cd flash-frontend-apple
npm install
```

### Development
```bash
npm start
```
The app will run on [http://localhost:3000](http://localhost:3000)

### Build
```bash
npm run build:prod
```

## 📁 Project Structure

```
src/
├── design-system/        # Apple-compliant design system
│   ├── tokens/          # Colors, typography, spacing, animations
│   ├── components/      # Reusable UI components
│   └── layouts/         # Page layouts
├── pages/               # Application pages
│   ├── Landing/         # Homepage
│   ├── Assessment/      # Multi-step wizard
│   ├── Analysis/        # Processing screen
│   └── Results/         # Results display
├── features/            # Feature-specific logic
│   ├── wizard/          # Wizard state management
│   ├── assessment/      # Assessment data store
│   └── results/         # Results processing
└── shared/              # Shared utilities
    ├── animations/      # Animation configs
    ├── hooks/           # Custom React hooks
    └── utils/           # Helper functions
```

## 🎯 Key Features

### Design System
- **Tokens**: Comprehensive design tokens for consistency
- **Components**: Button, TextField, Select, Card, NavigationBar, etc.
- **Animations**: Smooth transitions following Apple's timing curves
- **Theme Support**: Automatic light/dark mode with system preference detection

### User Experience
- **Wizard Navigation**: Gesture-based navigation with progress tracking
- **Loading States**: Beautiful loading animations
- **Error Handling**: Graceful error states
- **Accessibility**: Full keyboard navigation and screen reader support

### Performance
- **Code Splitting**: Lazy-loaded routes
- **Optimized Animations**: GPU-accelerated transforms
- **Responsive Design**: Adapts from iPhone SE to desktop
- **Progressive Enhancement**: Works without JavaScript

## 🛠️ Development

### Code Style
```bash
# Format code
npm run format

# Lint
npm run lint
```

### Testing
```bash
# Run tests
npm test

# Coverage
npm run test:coverage
```

### Type Checking
TypeScript is configured for strict type safety.

## 📱 Responsive Breakpoints

- **Compact**: 320px (iPhone SE)
- **Regular**: 390px (iPhone 14)
- **Medium**: 744px (iPad Mini)
- **Large**: 1024px (iPad Pro 11")
- **XLarge**: 1366px (iPad Pro 12.9")
- **XXLarge**: 1920px (Desktop)

## 🎨 Color System

The design system includes:
- System colors that adapt to light/dark mode
- Semantic colors for consistent meaning
- Proper contrast ratios for accessibility
- Vibrancy effects for depth

## ⚡ Animation System

Following Apple's animation principles:
- **Spring animations** for natural motion
- **Emphasized easing** for important transitions
- **Reduced motion** support for accessibility
- **60fps** performance targets

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
REACT_APP_API_URL=http://localhost:8001
REACT_APP_ENABLE_ANALYTICS=false
```

### API Integration
The frontend expects the FLASH API to be running on port 8001.

## 📚 Component Library

### Button
```tsx
<Button variant="primary" size="large" icon={<Icon name="arrow.right" />}>
  Continue
</Button>
```

### TextField
```tsx
<TextField
  label="Company Name"
  placeholder="Acme Inc."
  value={value}
  onChange={setValue}
/>
```

### NavigationBar
```tsx
<NavigationBar title="FLASH" transparent>
  <Button variant="text">Sign In</Button>
</NavigationBar>
```

## 🚀 Deployment

### Production Build
```bash
npm run build:prod
```

### Serve Static Files
```bash
npx serve -s build -l 3000
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
```

## 📄 License

This project follows Apple's design principles but is not affiliated with Apple Inc.

## 🤝 Contributing

Please ensure all contributions maintain the Apple design standards and pass all tests.

---

Built with ❤️ following Apple's Human Interface Guidelines