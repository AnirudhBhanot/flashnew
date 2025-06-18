import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '../../contexts/ThemeContext';
import './ThemeToggle.css';

interface ThemeToggleProps {
  showLabel?: boolean;
  variant?: 'default' | 'minimal' | 'expanded';
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  showLabel = false,
  variant = 'default'
}) => {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  const themes = [
    { value: 'light', label: 'Light', icon: '☀️' },
    { value: 'dark', label: 'Dark', icon: '🌙' },
    { value: 'system', label: 'System', icon: '💻' }
  ];

  const currentThemeData = themes.find(t => t.value === theme) || themes[2];

  if (variant === 'minimal') {
    return (
      <motion.button
        className="theme-toggle-minimal"
        onClick={() => {
          const newTheme = resolvedTheme === 'dark' ? 'light' : 'dark';
          setTheme(newTheme);
        }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        aria-label="Toggle theme"
      >
        <motion.div
          className="theme-toggle-icon"
          animate={{ rotate: resolvedTheme === 'dark' ? 0 : 180 }}
          transition={{ duration: 0.5, type: "spring" }}
        >
          {resolvedTheme === 'dark' ? '🌙' : '☀️'}
        </motion.div>
      </motion.button>
    );
  }

  if (variant === 'expanded') {
    return (
      <div className="theme-toggle-expanded">
        {themes.map((themeOption) => (
          <motion.button
            key={themeOption.value}
            className={`theme-option ${theme === themeOption.value ? 'active' : ''}`}
            onClick={() => setTheme(themeOption.value as any)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="theme-option-icon">{themeOption.icon}</span>
            <span className="theme-option-label">{themeOption.label}</span>
          </motion.button>
        ))}
      </div>
    );
  }

  return (
    <div className="theme-toggle-container">
      <motion.button
        className="theme-toggle"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <span className="theme-toggle-icon">{currentThemeData.icon}</span>
        {showLabel && (
          <span className="theme-toggle-label">{currentThemeData.label}</span>
        )}
        <motion.svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          className="theme-toggle-arrow"
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <path
            d="M3 5L6 8L9 5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </motion.svg>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              className="theme-dropdown-backdrop"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />
            <motion.div
              className="theme-dropdown"
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            >
              {themes.map((themeOption, index) => (
                <motion.button
                  key={themeOption.value}
                  className={`theme-dropdown-item ${theme === themeOption.value ? 'active' : ''}`}
                  onClick={() => {
                    setTheme(themeOption.value as any);
                    setIsOpen(false);
                  }}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ x: 4 }}
                >
                  <span className="theme-dropdown-icon">{themeOption.icon}</span>
                  <span className="theme-dropdown-label">{themeOption.label}</span>
                  {theme === themeOption.value && (
                    <motion.span
                      className="theme-dropdown-check"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring", stiffness: 500 }}
                    >
                      ✓
                    </motion.span>
                  )}
                </motion.button>
              ))}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

// Theme switch component with animated toggle
export const ThemeSwitch: React.FC = () => {
  const { resolvedTheme, setTheme } = useTheme();
  const isDark = resolvedTheme === 'dark';

  return (
    <motion.button
      className="theme-switch"
      onClick={() => setTheme(isDark ? 'light' : 'dark')}
      aria-label="Toggle theme"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <motion.div
        className="theme-switch-track"
        animate={{
          backgroundColor: isDark ? '#4a5568' : '#e2e8f0'
        }}
      >
        <motion.div
          className="theme-switch-thumb"
          animate={{
            x: isDark ? 28 : 0,
            backgroundColor: isDark ? '#1a202c' : '#ffffff'
          }}
          transition={{ type: "spring", stiffness: 500, damping: 30 }}
        >
          <AnimatePresence mode="wait">
            <motion.span
              key={isDark ? 'moon' : 'sun'}
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, rotate: 180 }}
              transition={{ duration: 0.2 }}
            >
              {isDark ? '🌙' : '☀️'}
            </motion.span>
          </AnimatePresence>
        </motion.div>
      </motion.div>
    </motion.button>
  );
};