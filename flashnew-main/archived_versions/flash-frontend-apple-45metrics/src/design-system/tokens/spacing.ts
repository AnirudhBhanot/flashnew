export const spacing = {
  xs: '4px',
  s: '8px',
  m: '16px',
  l: '20px',
  xl: '24px',
  xxl: '32px',
  xxxl: '48px',
  
  // Component-specific spacing
  buttonPadding: {
    small: '6px 14px',
    medium: '11px 20px',
    large: '14px 24px',
  },
  
  inputPadding: {
    small: '7px 12px',
    medium: '11px 16px',
    large: '15px 20px',
  },
  
  cardPadding: {
    small: '12px',
    medium: '16px',
    large: '20px',
  },
  
  // Layout spacing
  layoutMargin: {
    mobile: '16px',
    tablet: '24px',
    desktop: '32px',
  },
  
  sectionSpacing: {
    small: '40px',
    medium: '60px',
    large: '80px',
  },
};

export const radius = {
  small: '6px',
  medium: '10px',
  large: '14px',
  xl: '20px',
  pill: '999px',
  
  // Component-specific radius
  button: {
    small: '8px',
    medium: '10px',
    large: '12px',
  },
  
  input: '10px',
  card: '14px',
  modal: '20px',
};

export const shadows = {
  small: '0 1px 3px rgba(0, 0, 0, 0.12)',
  medium: '0 4px 16px rgba(0, 0, 0, 0.08)',
  large: '0 10px 40px rgba(0, 0, 0, 0.12)',
  
  // Component-specific shadows
  button: {
    default: '0 1px 3px rgba(0, 0, 0, 0.12)',
    hover: '0 4px 16px rgba(0, 0, 0, 0.08)',
    active: '0 1px 3px rgba(0, 0, 0, 0.16)',
  },
  
  card: {
    default: '0 2px 8px rgba(0, 0, 0, 0.08)',
    hover: '0 4px 16px rgba(0, 0, 0, 0.12)',
    elevated: '0 8px 32px rgba(0, 0, 0, 0.12)',
  },
  
  modal: '0 20px 80px rgba(0, 0, 0, 0.16)',
};

export const breakpoints = {
  compact: '320px',     // iPhone SE
  regular: '390px',     // iPhone 14
  medium: '744px',      // iPad Mini
  large: '1024px',      // iPad Pro 11"
  xlarge: '1366px',     // iPad Pro 12.9"
  xxlarge: '1920px',    // Desktop
};

export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
  notification: 1080,
};