// Re-export framer-motion components with type fixes
import { 
  motion as framemotion, 
  AnimatePresence as FramerAnimatePresence,
  AnimatePresenceProps 
} from 'framer-motion';
import { ReactElement } from 'react';

// Type-safe AnimatePresence wrapper that ensures it returns ReactElement
export const AnimatePresence = (props: AnimatePresenceProps): ReactElement => {
  return FramerAnimatePresence(props) as ReactElement;
};

// Re-export motion as-is
export const motion = framemotion;