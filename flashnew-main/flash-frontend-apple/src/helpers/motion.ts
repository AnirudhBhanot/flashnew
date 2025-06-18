// Re-export framer-motion components with type fixes
import { 
  motion as framemotion, 
  AnimatePresence as FramerAnimatePresence
} from 'framer-motion';

// Type assertion to fix TypeScript issues with framer-motion's AnimatePresence
export const AnimatePresence = FramerAnimatePresence as any;

// Re-export motion as-is
export const motion = framemotion;