// Temporary fix for framer-motion TypeScript issues
import { AnimatePresence as OriginalAnimatePresence } from 'framer-motion';

// Cast to any to bypass type checking issues with framer-motion
export const AnimatePresence = OriginalAnimatePresence as any;