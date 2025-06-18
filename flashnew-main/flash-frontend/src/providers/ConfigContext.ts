/**
 * Configuration Context
 * Provides configuration access throughout the application
 */

import { createContext } from 'react';
import { IConfiguration, IConfigChange, IContext, ConfigPath, ConfigValue } from '../config/types';

export interface IConfigContext {
  // Current configuration
  config: IConfiguration;
  
  // Loading state
  loading: boolean;
  
  // Error state
  error: Error | null;
  
  // Get configuration value with optional context
  get: <T = any>(path: ConfigPath, defaultValue?: T, context?: IContext) => T;
  
  // Update configuration (admin only)
  update: (path: ConfigPath, value: ConfigValue) => Promise<void>;
  
  // Bulk update configuration
  bulkUpdate: (updates: Record<ConfigPath, ConfigValue>) => Promise<void>;
  
  // Reset to defaults
  reset: (path?: ConfigPath) => Promise<void>;
  
  // Subscribe to configuration changes
  subscribe: (callback: (config: IConfiguration, changes?: IConfigChange[]) => void) => () => void;
  
  // Check if a feature is enabled
  isFeatureEnabled: (feature: string) => boolean;
  
  // Get stage-aware threshold
  getStageAwareThreshold: (basePath: string, stage: string, sector?: string) => any;
  
  // Get sector-aware threshold
  getSectorAwareThreshold: (basePath: string, sector: string, stage?: string) => any;
  
  // Refresh configuration from remote
  refresh: () => Promise<void>;
}

// Create context with default values
export const ConfigContext = createContext<IConfigContext | null>(null);

// Context display name for debugging
ConfigContext.displayName = 'ConfigContext';