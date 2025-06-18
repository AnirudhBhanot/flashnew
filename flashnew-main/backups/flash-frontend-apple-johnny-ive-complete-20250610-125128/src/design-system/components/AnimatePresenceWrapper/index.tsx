import React from 'react';
import { AnimatePresence as FramerAnimatePresence } from 'framer-motion';

interface AnimatePresenceWrapperProps {
  children: React.ReactNode;
  mode?: 'wait' | 'sync' | 'popLayout';
  initial?: boolean;
  onExitComplete?: () => void;
}

// Type assertion to fix TypeScript issues with framer-motion's AnimatePresence
const AnimatePresenceFixed = FramerAnimatePresence as any;

// Wrapper to fix TypeScript issues with framer-motion's AnimatePresence
export const AnimatePresence: React.FC<AnimatePresenceWrapperProps> = (props) => {
  return <AnimatePresenceFixed {...props} />;
};

export default AnimatePresence;