// Type definitions for framer-motion to fix AnimatePresence errors
import { ReactElement } from 'react';

declare module 'framer-motion' {
  export interface AnimatePresenceProps {
    children?: React.ReactNode;
    mode?: 'wait' | 'sync' | 'popLayout';
    initial?: boolean;
    onExitComplete?: () => void;
  }

  export const AnimatePresence: React.FC<AnimatePresenceProps>;
}