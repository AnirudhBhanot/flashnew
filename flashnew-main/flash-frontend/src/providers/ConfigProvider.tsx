/**
 * Configuration Provider
 * Manages configuration state and provides it to the application
 */

import React, { useState, useEffect, useCallback, useMemo, ReactNode } from 'react';
import { ConfigContext, IConfigContext } from './ConfigContext';
import { IConfiguration, IConfigChange, IContext, ConfigPath, ConfigValue } from '../config/types';
import { defaultConfiguration } from '../config/defaults';
import { ConfigurationService } from '../services/ConfigService';
import { get, set, cloneDeep } from 'lodash';

interface ConfigProviderProps {
  children: ReactNode;
  initialConfig?: Partial<IConfiguration>;
  enableRemoteConfig?: boolean;
  enableCaching?: boolean;
}

export const ConfigProvider: React.FC<ConfigProviderProps> = ({
  children,
  initialConfig,
  enableRemoteConfig = true,
  enableCaching = true,
}) => {
  const [config, setConfig] = useState<IConfiguration>(() => ({
    ...defaultConfiguration,
    ...initialConfig,
  }));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  // Configuration service instance
  const configService = useMemo(
    () => ConfigurationService.getInstance(enableCaching),
    [enableCaching]
  );

  // Initialize configuration
  useEffect(() => {
    const initializeConfig = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Initialize service
        await configService.initialize();
        
        // Get initial configuration
        const loadedConfig = await configService.getConfiguration();
        setConfig(loadedConfig);
        
        // Subscribe to configuration changes
        const unsubscribe = configService.subscribe((newConfig, changes) => {
          setConfig(newConfig);
          
          // Log changes in development
          if (process.env.NODE_ENV === 'development' && changes?.length) {
            console.log('[ConfigProvider] Configuration updated:', changes);
          }
        });
        
        // Cleanup subscription
        return () => {
          unsubscribe();
        };
      } catch (err) {
        console.error('[ConfigProvider] Failed to initialize configuration:', err);
        setError(err as Error);
        // Fall back to default configuration
        setConfig(defaultConfiguration);
      } finally {
        setLoading(false);
      }
    };
    
    initializeConfig();
  }, [configService]);

  // Get configuration value with context support
  const getValue = useCallback(<T = any>(
    path: ConfigPath,
    defaultValue?: T,
    context?: IContext
  ): T => {
    // Get base value
    let value = get(config, path, defaultValue);
    
    // Apply context-specific overrides
    if (context) {
      // Check for stage-specific override
      if (context.stage) {
        const stagePath = `${path}.byStage.${context.stage}`;
        const stageValue = get(config, stagePath);
        if (stageValue !== undefined) {
          value = typeof value === 'object' ? { ...value, ...stageValue } : stageValue;
        }
      }
      
      // Check for sector-specific override
      if (context.sector) {
        const sectorPath = `${path}.bySector.${context.sector}`;
        const sectorValue = get(config, sectorPath);
        if (sectorValue !== undefined) {
          value = typeof value === 'object' ? { ...value, ...sectorValue } : sectorValue;
        }
      }
    }
    
    return value as T;
  }, [config]);

  // Update configuration value
  const updateValue = useCallback(async (
    path: ConfigPath,
    value: ConfigValue
  ): Promise<void> => {
    try {
      const newConfig = cloneDeep(config);
      set(newConfig, path, value);
      
      // Update local state immediately
      setConfig(newConfig);
      
      // Persist to service
      await configService.updateConfiguration(path, value);
    } catch (err) {
      console.error('[ConfigProvider] Failed to update configuration:', err);
      throw err;
    }
  }, [config, configService]);

  // Bulk update configuration
  const bulkUpdate = useCallback(async (
    updates: Record<ConfigPath, ConfigValue>
  ): Promise<void> => {
    try {
      const newConfig = cloneDeep(config);
      
      Object.entries(updates).forEach(([path, value]) => {
        set(newConfig, path, value);
      });
      
      // Update local state immediately
      setConfig(newConfig);
      
      // Persist to service
      await configService.bulkUpdateConfiguration(updates);
    } catch (err) {
      console.error('[ConfigProvider] Failed to bulk update configuration:', err);
      throw err;
    }
  }, [config, configService]);

  // Reset configuration to defaults
  const reset = useCallback(async (path?: ConfigPath): Promise<void> => {
    try {
      if (path) {
        // Reset specific path
        const defaultValue = get(defaultConfiguration, path);
        await updateValue(path, defaultValue);
      } else {
        // Reset entire configuration
        setConfig(defaultConfiguration);
        await configService.resetConfiguration();
      }
    } catch (err) {
      console.error('[ConfigProvider] Failed to reset configuration:', err);
      throw err;
    }
  }, [configService, updateValue]);

  // Subscribe to configuration changes
  const subscribe = useCallback((
    callback: (config: IConfiguration, changes?: IConfigChange[]) => void
  ): (() => void) => {
    return configService.subscribe(callback);
  }, [configService]);

  // Check if feature is enabled
  const isFeatureEnabled = useCallback((feature: string): boolean => {
    return get(config.features, feature, false);
  }, [config.features]);

  // Get stage-aware threshold
  const getStageAwareThreshold = useCallback((
    basePath: string,
    stage: string,
    sector?: string
  ): any => {
    return getValue(basePath, undefined, { stage, sector });
  }, [getValue]);

  // Get sector-aware threshold
  const getSectorAwareThreshold = useCallback((
    basePath: string,
    sector: string,
    stage?: string
  ): any => {
    return getValue(basePath, undefined, { stage, sector });
  }, [getValue]);

  // Refresh configuration from remote
  const refresh = useCallback(async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      await configService.refreshConfiguration();
    } catch (err) {
      console.error('[ConfigProvider] Failed to refresh configuration:', err);
      setError(err as Error);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [configService]);

  // Context value
  const contextValue: IConfigContext = useMemo(
    () => ({
      config,
      loading,
      error,
      get: getValue,
      update: updateValue,
      bulkUpdate,
      reset,
      subscribe,
      isFeatureEnabled,
      getStageAwareThreshold,
      getSectorAwareThreshold,
      refresh,
    }),
    [
      config,
      loading,
      error,
      getValue,
      updateValue,
      bulkUpdate,
      reset,
      subscribe,
      isFeatureEnabled,
      getStageAwareThreshold,
      getSectorAwareThreshold,
      refresh,
    ]
  );

  // Show loading state
  if (loading && !initialConfig) {
    return (
      <div className="config-loading">
        Loading configuration...
      </div>
    );
  }

  // Show error state in development
  if (error && process.env.NODE_ENV === 'development') {
    return (
      <div className="config-error">
        <h3>Configuration Error</h3>
        <p>{error.message}</p>
        <button onClick={() => window.location.reload()}>Reload</button>
      </div>
    );
  }

  return (
    <ConfigContext.Provider value={contextValue}>
      {children}
    </ConfigContext.Provider>
  );
};