export const animations = {
  // Easing curves
  easing: {
    easeOut: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    easeInOut: 'cubic-bezier(0.45, 0, 0.55, 1)',
    easeIn: 'cubic-bezier(0.55, 0.06, 0.68, 0.19)',
    emphasized: 'cubic-bezier(0.2, 0, 0, 1)',
    spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
  },
  
  // Durations
  duration: {
    instant: '0.1s',
    fast: '0.2s',
    regular: '0.3s',
    slow: '0.4s',
    sleepy: '0.5s',
    
    // Component-specific
    pageTransition: '0.4s',
    modalOpen: '0.3s',
    dropdownExpand: '0.25s',
    ripple: '0.6s',
  },
  
  // Spring configurations for Framer Motion
  spring: {
    default: {
      mass: 1,
      stiffness: 300,
      damping: 30,
    },
    gentle: {
      mass: 1,
      stiffness: 200,
      damping: 25,
    },
    bouncy: {
      mass: 0.8,
      stiffness: 400,
      damping: 15,
    },
    stiff: {
      mass: 1,
      stiffness: 500,
      damping: 35,
    },
  },
  
  // Common transitions
  transitions: {
    fade: {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
      exit: { opacity: 0 },
    },
    slideUp: {
      initial: { opacity: 0, y: 20 },
      animate: { opacity: 1, y: 0 },
      exit: { opacity: 0, y: -20 },
    },
    slideDown: {
      initial: { opacity: 0, y: -20 },
      animate: { opacity: 1, y: 0 },
      exit: { opacity: 0, y: 20 },
    },
    slideLeft: {
      initial: { opacity: 0, x: 20 },
      animate: { opacity: 1, x: 0 },
      exit: { opacity: 0, x: -20 },
    },
    slideRight: {
      initial: { opacity: 0, x: -20 },
      animate: { opacity: 1, x: 0 },
      exit: { opacity: 0, x: 20 },
    },
    scale: {
      initial: { opacity: 0, scale: 0.95 },
      animate: { opacity: 1, scale: 1 },
      exit: { opacity: 0, scale: 0.95 },
    },
    zoom: {
      initial: { opacity: 0, scale: 0.5 },
      animate: { opacity: 1, scale: 1 },
      exit: { opacity: 0, scale: 0.5 },
    },
  },
  
  // Keyframes
  keyframes: {
    spin: `
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    `,
    pulse: `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `,
    bounce: `
      @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
      }
    `,
    shake: `
      @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
        20%, 40%, 60%, 80% { transform: translateX(4px); }
      }
    `,
    ripple: `
      @keyframes ripple {
        from {
          transform: scale(0);
          opacity: 1;
        }
        to {
          transform: scale(4);
          opacity: 0;
        }
      }
    `,
  },
};