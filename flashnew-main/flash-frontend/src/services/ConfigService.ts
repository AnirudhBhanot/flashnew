/**
 * Configuration Service
 * Manages configuration loading, caching, and persistence
 */

import { IConfiguration, IConfigChange, ConfigPath, ConfigValue, DeepPartial } from '../config/types';
import { defaultConfiguration } from '../config/defaults';
import { get, set, merge, cloneDeep } from 'lodash';

interface IConfigCache {
  config: IConfiguration;
  timestamp: number;
  version: string;
}

export class ConfigurationService {
  private static instance: ConfigurationService;
  private config: IConfiguration = defaultConfiguration;
  private subscribers: Set<(config: IConfiguration, changes?: IConfigChange[]) => void> = new Set();
  private cache: Map<string, any> = new Map();
  private localStorageKey = 'flash_config_cache';
  private cacheTTL = 5 * 60 * 1000; // 5 minutes
  private enableCaching: boolean;
  private pendingChanges: IConfigChange[] = [];
  
  private constructor(enableCaching: boolean = true) {
    this.enableCaching = enableCaching;
  }
  
  static getInstance(enableCaching: boolean = true): ConfigurationService {
    if (!ConfigurationService.instance) {
      ConfigurationService.instance = new ConfigurationService(enableCaching);
    }
    return ConfigurationService.instance;
  }
  
  /**
   * Initialize configuration service
   */
  async initialize(): Promise<void> {
    try {
      // Load configuration in priority order
      this.config = await this.loadConfiguration();
      
      // Start watching for changes
      this.watchConfigurationChanges();
      
      // Validate configuration
      await this.validateConfiguration();
      
      console.log('[ConfigService] Initialized with configuration version:', this.config.version);
    } catch (error) {
      console.error('[ConfigService] Initialization failed:', error);
      throw error;
    }
  }
  
  /**
   * Load configuration from multiple sources
   */
  private async loadConfiguration(): Promise<IConfiguration> {
    // 1. Start with defaults
    let config = cloneDeep(defaultConfiguration);
    
    // 2. Override with environment variables
    config = this.mergeEnvironmentVariables(config);
    
    // 3. Override with cached configuration
    if (this.enableCaching) {
      const cached = this.loadCachedConfiguration();
      if (cached && this.isCacheValid(cached)) {
        config = merge(config, cached.config);
      }
    }
    
    // 4. Override with remote configuration (if available)
    try {
      const remote = await this.loadRemoteConfiguration();
      if (remote) {
        config = merge(config, remote);
        // Cache the remote configuration
        if (this.enableCaching) {
          this.cacheConfiguration(config);
        }
      }
    } catch (error) {
      console.warn('[ConfigService] Failed to load remote configuration:', error);
    }
    
    return config;
  }
  
  /**
   * Merge environment variables into configuration
   */
  private mergeEnvironmentVariables(config: IConfiguration): IConfiguration {
    const env = process.env;
    
    // Map environment variables to configuration paths
    const envMappings: Record<string, ConfigPath> = {
      'REACT_APP_MAX_IMPROVEMENT': 'thresholds.success.improvements.maxImprovement',
      'REACT_APP_PER_ACTION_IMPROVEMENT': 'thresholds.success.improvements.perActionImprovement',
      'REACT_APP_MILESTONE_ACTIONS': 'thresholds.success.improvements.milestoneActions',
      'REACT_APP_DEFAULT_CONFIDENCE': 'defaults.confidence',
      'REACT_APP_DEFAULT_PROBABILITY': 'defaults.probability',
      'REACT_APP_SUCCESS_EXCELLENT': 'thresholds.success.probability.excellent',
      'REACT_APP_SUCCESS_GOOD': 'thresholds.success.probability.good',
      'REACT_APP_SUCCESS_FAIR': 'thresholds.success.probability.fair',
      'REACT_APP_SUCCESS_POOR': 'thresholds.success.probability.poor',
      'REACT_APP_BURN_EXCELLENT': 'thresholds.risk.burnMultiple.excellent',
      'REACT_APP_BURN_GOOD': 'thresholds.risk.burnMultiple.good',
      'REACT_APP_BURN_WARNING': 'thresholds.risk.burnMultiple.warning',
      'REACT_APP_BURN_CRITICAL': 'thresholds.risk.burnMultiple.critical',
      'REACT_APP_ANIMATION_ENABLED': 'ui.animation.enabled',
      'REACT_APP_ANIMATION_DURATION': 'ui.animation.duration.normal',
      'REACT_APP_CHART_RADIUS': 'ui.charts.radar.radius',
      'REACT_APP_CHART_LEVELS': 'ui.charts.radar.levels',
    };
    
    Object.entries(envMappings).forEach(([envKey, configPath]) => {
      if (env[envKey] !== undefined) {
        const value = this.parseEnvValue(env[envKey]!);
        set(config, configPath, value);
      }
    });
    
    return config;
  }
  
  /**
   * Parse environment variable value
   */
  private parseEnvValue(value: string): any {
    // Try to parse as JSON first
    try {
      return JSON.parse(value);
    } catch {
      // Not JSON, try other formats
    }
    
    // Boolean
    if (value === 'true') return true;
    if (value === 'false') return false;
    
    // Number
    const num = Number(value);
    if (!isNaN(num)) return num;
    
    // Array (comma-separated)
    if (value.includes(',')) {
      return value.split(',').map(v => this.parseEnvValue(v.trim()));
    }
    
    // String
    return value;
  }
  
  /**
   * Load cached configuration from localStorage
   */
  private loadCachedConfiguration(): IConfigCache | null {
    if (!this.enableCaching) return null;
    
    try {
      const cached = localStorage.getItem(this.localStorageKey);
      if (cached) {
        return JSON.parse(cached);
      }
    } catch (error) {
      console.warn('[ConfigService] Failed to load cached configuration:', error);
    }
    
    return null;
  }
  
  /**
   * Check if cache is valid
   */
  private isCacheValid(cache: IConfigCache): boolean {
    const now = Date.now();
    const age = now - cache.timestamp;
    
    // Check age
    if (age > this.cacheTTL) {
      return false;
    }
    
    // Check version
    if (cache.version !== defaultConfiguration.version) {
      return false;
    }
    
    return true;
  }
  
  /**
   * Cache configuration to localStorage
   */
  private cacheConfiguration(config: IConfiguration): void {
    if (!this.enableCaching) return;
    
    try {
      const cache: IConfigCache = {
        config,
        timestamp: Date.now(),
        version: config.version,
      };
      
      localStorage.setItem(this.localStorageKey, JSON.stringify(cache));
    } catch (error) {
      console.warn('[ConfigService] Failed to cache configuration:', error);
    }
  }
  
  /**
   * Load remote configuration from API
   */
  private async loadRemoteConfiguration(): Promise<DeepPartial<IConfiguration> | null> {
    // Skip remote loading in development by default
    if (process.env.NODE_ENV === 'development' && !process.env.REACT_APP_USE_REMOTE_CONFIG) {
      return null;
    }
    
    try {
      const response = await fetch('/api/config', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const remoteConfig = await response.json();
      return remoteConfig;
    } catch (error) {
      console.error('[ConfigService] Failed to load remote configuration:', error);
      return null;
    }
  }
  
  /**
   * Watch for configuration changes
   */
  private watchConfigurationChanges(): void {
    // In production, poll for remote changes
    if (process.env.NODE_ENV === 'production') {
      setInterval(() => {
        this.checkForRemoteChanges();
      }, 60 * 1000); // Check every minute
    }
    
    // Listen for storage events (cross-tab synchronization)
    window.addEventListener('storage', (event) => {
      if (event.key === this.localStorageKey && event.newValue) {
        try {
          const cache: IConfigCache = JSON.parse(event.newValue);
          if (this.isCacheValid(cache)) {
            this.config = cache.config;
            this.notifySubscribers([]);
          }
        } catch (error) {
          console.error('[ConfigService] Failed to sync configuration:', error);
        }
      }
    });
  }
  
  /**
   * Check for remote configuration changes
   */
  private async checkForRemoteChanges(): Promise<void> {
    try {
      const remote = await this.loadRemoteConfiguration();
      if (remote && remote.version !== this.config.version) {
        const newConfig = merge(cloneDeep(this.config), remote);
        const changes = this.detectChanges(this.config, newConfig);
        
        this.config = newConfig;
        this.cacheConfiguration(newConfig);
        this.notifySubscribers(changes);
      }
    } catch (error) {
      console.error('[ConfigService] Failed to check for remote changes:', error);
    }
  }
  
  /**
   * Validate configuration
   */
  private async validateConfiguration(): Promise<void> {
    // Basic validation
    if (!this.config.version) {
      throw new Error('Configuration missing version');
    }
    
    if (!this.config.environment) {
      throw new Error('Configuration missing environment');
    }
    
    // Validate thresholds
    const validateThreshold = (value: any, name: string) => {
      if (typeof value !== 'number' || value < 0 || value > 1) {
        throw new Error(`Invalid threshold value for ${name}: ${value}`);
      }
    };
    
    // Validate probability thresholds
    const probThresholds = this.config.thresholds.success.probability;
    validateThreshold(probThresholds.excellent, 'success.probability.excellent');
    validateThreshold(probThresholds.good, 'success.probability.good');
    validateThreshold(probThresholds.fair, 'success.probability.fair');
    validateThreshold(probThresholds.poor, 'success.probability.poor');
    
    // Ensure thresholds are in correct order
    if (probThresholds.excellent <= probThresholds.good ||
        probThresholds.good <= probThresholds.fair ||
        probThresholds.fair <= probThresholds.poor) {
      throw new Error('Success probability thresholds must be in descending order');
    }
  }
  
  /**
   * Get current configuration
   */
  getConfiguration(): IConfiguration {
    return this.config;
  }
  
  /**
   * Get configuration value
   */
  getValue<T = any>(path: ConfigPath, defaultValue?: T): T {
    return get(this.config, path, defaultValue) as T;
  }
  
  /**
   * Update configuration value
   */
  async updateConfiguration(path: ConfigPath, value: ConfigValue): Promise<void> {
    const oldValue = get(this.config, path);
    
    // Create change record
    const change: IConfigChange = {
      path,
      oldValue,
      newValue: value,
      timestamp: Date.now(),
    };
    
    // Update configuration
    const newConfig = cloneDeep(this.config);
    set(newConfig, path, value);
    
    // Validate new configuration
    this.config = newConfig;
    await this.validateConfiguration();
    
    // Cache and notify
    this.cacheConfiguration(newConfig);
    this.notifySubscribers([change]);
  }
  
  /**
   * Bulk update configuration
   */
  async bulkUpdateConfiguration(updates: Record<ConfigPath, ConfigValue>): Promise<void> {
    const changes: IConfigChange[] = [];
    const newConfig = cloneDeep(this.config);
    
    // Apply all updates
    Object.entries(updates).forEach(([path, value]) => {
      const oldValue = get(newConfig, path);
      set(newConfig, path, value);
      
      changes.push({
        path,
        oldValue,
        newValue: value,
        timestamp: Date.now(),
      });
    });
    
    // Validate new configuration
    this.config = newConfig;
    await this.validateConfiguration();
    
    // Cache and notify
    this.cacheConfiguration(newConfig);
    this.notifySubscribers(changes);
  }
  
  /**
   * Reset configuration to defaults
   */
  async resetConfiguration(path?: ConfigPath): Promise<void> {
    if (path) {
      const defaultValue = get(defaultConfiguration, path);
      await this.updateConfiguration(path, defaultValue);
    } else {
      const changes = this.detectChanges(this.config, defaultConfiguration);
      this.config = cloneDeep(defaultConfiguration);
      
      // Clear cache
      if (this.enableCaching) {
        localStorage.removeItem(this.localStorageKey);
      }
      
      this.notifySubscribers(changes);
    }
  }
  
  /**
   * Refresh configuration from remote
   */
  async refreshConfiguration(): Promise<void> {
    this.config = await this.loadConfiguration();
    this.notifySubscribers([]);
  }
  
  /**
   * Subscribe to configuration changes
   */
  subscribe(callback: (config: IConfiguration, changes?: IConfigChange[]) => void): () => void {
    this.subscribers.add(callback);
    
    // Return unsubscribe function
    return () => {
      this.subscribers.delete(callback);
    };
  }
  
  /**
   * Notify subscribers of changes
   */
  private notifySubscribers(changes: IConfigChange[]): void {
    this.subscribers.forEach(callback => {
      try {
        callback(this.config, changes);
      } catch (error) {
        console.error('[ConfigService] Subscriber error:', error);
      }
    });
  }
  
  /**
   * Detect changes between configurations
   */
  private detectChanges(oldConfig: any, newConfig: any, path: string = ''): IConfigChange[] {
    const changes: IConfigChange[] = [];
    
    // Compare objects recursively
    const keys = new Set([...Object.keys(oldConfig), ...Object.keys(newConfig)]);
    
    keys.forEach(key => {
      const currentPath = path ? `${path}.${key}` : key;
      const oldValue = oldConfig[key];
      const newValue = newConfig[key];
      
      if (oldValue !== newValue) {
        if (typeof oldValue === 'object' && typeof newValue === 'object' && 
            oldValue !== null && newValue !== null) {
          // Recurse into objects
          changes.push(...this.detectChanges(oldValue, newValue, currentPath));
        } else {
          // Value changed
          changes.push({
            path: currentPath,
            oldValue,
            newValue,
            timestamp: Date.now(),
          });
        }
      }
    });
    
    return changes;
  }
  
  /**
   * Clear cache
   */
  clearCache(): void {
    this.cache.clear();
    if (this.enableCaching) {
      localStorage.removeItem(this.localStorageKey);
    }
  }
}