import { AnimatePresence as FramerAnimatePresence } from 'framer-motion';

// Type assertion to fix TypeScript issues with framer-motion's AnimatePresence
// The issue is that AnimatePresence can return undefined, but React components must return an element
export const AnimatePresence = FramerAnimatePresence as any;

export default AnimatePresence;