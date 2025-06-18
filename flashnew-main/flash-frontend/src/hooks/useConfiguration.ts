/**
 * Configuration Hooks
 * Custom hooks for accessing configuration throughout the application
 */

import { useContext, useMemo, useCallback, useEffect, useState } from 'react';
import { ConfigContext } from '../providers/ConfigContext';
import { IContext, ConfigPath } from '../config/types';

/**
 * Main configuration hook
 * Provides access to the configuration context
 */
export const useConfiguration = () => {
  const context = useContext(ConfigContext);
  
  if (!context) {
    throw new Error('useConfiguration must be used within ConfigProvider');
  }
  
  return context;
};

/**
 * Get a specific configuration value
 * @param path - Dot notation path to the configuration value
 * @param defaultValue - Default value if path doesn't exist
 * @param context - Optional context for stage/sector specific values
 */
export const useConfigValue = <T = any>(
  path: ConfigPath,
  defaultValue?: T,
  context?: IContext
): T => {
  const { config, get } = useConfiguration();
  
  return useMemo(
    () => get<T>(path, defaultValue, context),
    [get, path, defaultValue, context, config] // Include config to trigger updates
  );
};

/**
 * Get stage-aware threshold values
 * @param basePath - Base path to the threshold
 * @param stage - Current stage
 * @param sector - Optional sector
 */
export const useStageAwareThreshold = (
  basePath: string,
  stage?: string,
  sector?: string
) => {
  const { getStageAwareThreshold } = useConfiguration();
  
  return useMemo(
    () => getStageAwareThreshold(basePath, stage || 'seed', sector),
    [getStageAwareThreshold, basePath, stage, sector]
  );
};

/**
 * Get sector-aware threshold values
 * @param basePath - Base path to the threshold
 * @param sector - Current sector
 * @param stage - Optional stage
 */
export const useSectorAwareThreshold = (
  basePath: string,
  sector?: string,
  stage?: string
) => {
  const { getSectorAwareThreshold } = useConfiguration();
  
  return useMemo(
    () => getSectorAwareThreshold(basePath, sector || 'default', stage),
    [getSectorAwareThreshold, basePath, sector, stage]
  );
};

/**
 * Check if a feature is enabled
 * @param feature - Feature name
 */
export const useFeatureFlag = (feature: string): boolean => {
  const { isFeatureEnabled } = useConfiguration();
  
  return useMemo(
    () => isFeatureEnabled(feature),
    [isFeatureEnabled, feature]
  );
};

/**
 * Get success probability thresholds with context
 * @param stage - Current stage
 * @param sector - Current sector
 */
export const useSuccessThresholds = (stage?: string, sector?: string) => {
  const thresholds = useStageAwareThreshold('thresholds.success.probability', stage, sector) || {};
  const { config, loading } = useConfiguration();
  
  return useMemo(() => {
    // Return default values if still loading
    if (loading || !config) {
      return {
        excellent: 0.75,
        good: 0.65,
        fair: 0.55,
        poor: 0.45,
        getLevel: () => 'good',
        getColor: () => '#FFFFFF',
        getMessage: () => 'Loading...',
        getEmoji: () => '⏳',
        getClassName: () => 'verdict-good',
        getRanges: (): any[] => [],
        getDetailedMessage: () => 'Loading configuration...'
      };
    }
    
    return {
      excellent: thresholds.excellent || 0.75,
      good: thresholds.good || 0.65,
      fair: thresholds.fair || 0.55,
      poor: thresholds.poor || 0.45,
      
      // Helper functions
      getLevel: (probability: number) => {
        if (probability >= (thresholds.excellent || 0.75)) return 'excellent';
        if (probability >= (thresholds.good || 0.65)) return 'good';
        if (probability >= (thresholds.fair || 0.55)) return 'fair';
        return 'poor';
      },
      
      getColor: (probability: number) => {
        if (probability >= (thresholds.excellent || 0.75)) return '#FFFFFF';
        if (probability >= (thresholds.good || 0.65)) return '#E8EAED';
        if (probability >= (thresholds.fair || 0.55)) return '#9CA3AF';
        return '#6B7280';
      },
      
      getMessage: (probability: number) => {
        const level = 
          probability >= (thresholds.excellent || 0.75) ? 'excellent' :
          probability >= (thresholds.good || 0.65) ? 'good' :
          probability >= (thresholds.fair || 0.55) ? 'fair' : 'poor';
        return config.messages.success[level];
      },
      
      getEmoji: (probability: number) => {
        const level = 
          probability >= (thresholds.excellent || 0.75) ? 'excellent' :
          probability >= (thresholds.good || 0.65) ? 'good' :
          probability >= (thresholds.fair || 0.55) ? 'fair' : 'poor';
        return config.ui.display.emojis[level];
      },
      
      getClassName: (probability: number) => {
        const level = 
          probability >= (thresholds.excellent || 0.75) ? 'excellent' :
          probability >= (thresholds.good || 0.65) ? 'good' :
          probability >= (thresholds.fair || 0.55) ? 'fair' : 'poor';
        return `verdict-${level}`;
      },
      
      getRanges: (): any[] => {
        const poor = thresholds.poor || 0.45;
        const fair = thresholds.fair || 0.55;
        const good = thresholds.good || 0.65;
        const excellent = thresholds.excellent || 0.75;
        
        return [
          { min: 0, max: poor * 100, label: `0-${poor * 100}%`, className: 'poor', description: config.messages.success.poor },
          { min: poor * 100, max: fair * 100, label: `${poor * 100}-${fair * 100}%`, className: 'fair', description: config.messages.success.fair },
          { min: fair * 100, max: good * 100, label: `${fair * 100}-${good * 100}%`, className: 'good', description: config.messages.success.good },
          { min: good * 100, max: excellent * 100, label: `${good * 100}-${excellent * 100}%`, className: 'excellent', description: config.messages.success.excellent },
          { min: excellent * 100, max: 100, label: `${excellent * 100}-100%`, className: 'exceptional', description: 'Top tier potential' }
        ];
      },
      
      getDetailedMessage: (probability: number) => {
        if (probability >= (thresholds.excellent || 0.75)) {
          return "Your startup demonstrates strong fundamentals across multiple dimensions. The AI models show high confidence in your potential for success.";
        } else if (probability >= (thresholds.good || 0.65)) {
          return "Your startup shows promise but has areas that need attention. Focus on the recommendations below to improve your success probability.";
        } else {
          return "Your startup needs significant improvements in key areas. Use this analysis to identify and address critical gaps.";
        }
      }
    };
  }, [thresholds, config, loading]);
};

/**
 * Get improvement calculation function
 * @param currentScore - Current success score
 */
export const useImprovementCalculator = (currentScore: number) => {
  const config = useConfigValue('thresholds.success.improvements');
  
  const calculate = useCallback((actions: number) => {
    const calculator = config.calculateImprovement || 
      ((current: number, acts: number) => 
        Math.min(current + acts * config.perActionImprovement, current + config.maxImprovement)
      );
    
    return calculator(currentScore, actions);
  }, [config, currentScore]);
  
  return {
    // Main calculation function
    calculate,
    
    // Shorthand for calling with actions
    calculateFromActions: (actions: number) => calculate(actions),
    
    // Get max potential improvement
    calculateMaxPotential: () => Math.min(currentScore + config.maxImprovement, 0.85),
    
    // Get max improvement amount
    getMaxImprovement: () => config.maxImprovement,
    
    // Get milestone actions (first milestone)
    getMilestoneActions: () => Array.isArray(config.milestoneActions) ? config.milestoneActions[0] : 3
  };
};

/**
 * Get UI animation configuration
 */
export const useAnimationConfig = () => {
  const animationConfig = useConfigValue('ui.animation');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  return useMemo(() => ({
    enabled: animationConfig.enabled && !prefersReducedMotion,
    duration: animationConfig.duration,
    delay: animationConfig.delay,
    easing: animationConfig.easing,
    springConfig: animationConfig.springConfig,
    
    // Helper functions
    getDuration: (speed: 'fast' | 'normal' | 'slow' = 'normal') => 
      animationConfig.enabled && !prefersReducedMotion ? animationConfig.duration[speed] : 0,
    
    getDelay: (length: 'short' | 'medium' | 'long' | number = 'short') => {
      if (typeof length === 'number') {
        return animationConfig.enabled && !prefersReducedMotion ? length * 1000 : 0;
      }
      return animationConfig.enabled && !prefersReducedMotion ? animationConfig.delay[length] : 0;
    },
    
    getType: () => animationConfig.type,
    
    getSpring: () => animationConfig.springConfig,
  }), [animationConfig, prefersReducedMotion]);
};

/**
 * Get chart configuration
 */
export const useChartConfig = () => {
  const chartConfig = useConfigValue('ui.charts');
  const [screenSize, setScreenSize] = useState({ width: window.innerWidth, height: window.innerHeight });
  
  useEffect(() => {
    const handleResize = () => {
      setScreenSize({ width: window.innerWidth, height: window.innerHeight });
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return useMemo(() => {
    const isMobile = screenSize.width < 768;
    const scale = isMobile ? 0.8 : 1;
    
    return {
      ...chartConfig,
      radar: {
        ...chartConfig.radar,
        radius: chartConfig.radar.radius * scale,
        pointRadius: chartConfig.radar.pointRadius * scale,
      },
      
      // Helper functions
      getResponsiveRadius: () => chartConfig.radar.radius * scale,
      getResponsivePointRadius: () => chartConfig.radar.pointRadius * scale,
    };
  }, [chartConfig, screenSize]);
};

/**
 * Get default values for missing data
 */
export const useDefaults = () => {
  return useConfigValue('defaults');
};

/**
 * Get business metric thresholds with context
 * @param metric - Metric name (e.g., 'burnMultiple', 'teamSize')
 * @param stage - Current stage
 * @param sector - Current sector
 */
export const useMetricThreshold = (
  metric: string,
  stage?: string,
  sector?: string
) => {
  const path = `thresholds.metrics.${metric}`;
  return useStageAwareThreshold(path, stage, sector);
};

/**
 * Subscribe to configuration changes
 * @param callback - Callback function when configuration changes
 */
export const useConfigSubscription = (
  callback: (config: any, changes?: any[]) => void
) => {
  const { subscribe } = useConfiguration();
  
  useEffect(() => {
    const unsubscribe = subscribe(callback);
    return unsubscribe;
  }, [subscribe, callback]);
};

/**
 * Get formatted number based on configuration
 * @param value - Number to format
 * @param type - Type of number (percentage, currency, score)
 */
export const useNumberFormatter = () => {
  const numberConfig = useConfigValue('ui.numbers');
  
  return useMemo(() => ({
    formatPercentage: (value: number, decimals?: number) => {
      const percentage = value * 100;
      return `${percentage.toFixed(decimals ?? numberConfig.percentageDecimals)}%`;
    },
    
    formatCurrency: (value: number) => {
      return new Intl.NumberFormat(numberConfig.locale, {
        style: 'currency',
        currency: numberConfig.currency,
        minimumFractionDigits: numberConfig.currencyDecimals,
        maximumFractionDigits: numberConfig.currencyDecimals,
      }).format(value);
    },
    
    formatScore: (value: number) => {
      return value.toFixed(numberConfig.scoreDecimals);
    },
    
    formatNumber: (value: number, decimals?: number) => {
      return new Intl.NumberFormat(numberConfig.locale, {
        minimumFractionDigits: decimals ?? 0,
        maximumFractionDigits: decimals ?? 0,
      }).format(value);
    },
  }), [numberConfig]);
};