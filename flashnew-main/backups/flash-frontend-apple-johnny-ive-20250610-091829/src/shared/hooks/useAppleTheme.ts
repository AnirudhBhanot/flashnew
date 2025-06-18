import { useEffect, useState } from 'react';

export type Theme = 'light' | 'dark' | 'auto';

export const useAppleTheme = () => {
  const [theme, setTheme] = useState<Theme>('light');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Get saved preference
    const savedTheme = localStorage.getItem('flash-theme') as Theme | null;
    if (savedTheme) {
      setTheme(savedTheme);
    } else {
      // If no saved preference, default to light
      setTheme('light');
      localStorage.setItem('flash-theme', 'light');
    }
  }, []);

  useEffect(() => {
    const updateResolvedTheme = () => {
      if (theme === 'auto') {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        setResolvedTheme(mediaQuery.matches ? 'dark' : 'light');
      } else {
        setResolvedTheme(theme as 'light' | 'dark');
      }
    };

    updateResolvedTheme();

    // Listen for system theme changes
    if (theme === 'auto') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = (e: MediaQueryListEvent) => {
        setResolvedTheme(e.matches ? 'dark' : 'light');
      };

      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', resolvedTheme);
    
    // Update meta theme-color
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', resolvedTheme === 'dark' ? '#000000' : '#FFFFFF');
    }
  }, [resolvedTheme]);

  const changeTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem('flash-theme', newTheme);
  };

  return {
    theme: resolvedTheme,
    setTheme: changeTheme,
    preferredTheme: theme,
  };
};