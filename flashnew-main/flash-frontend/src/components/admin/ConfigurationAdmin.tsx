import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ConfigurationAdmin.css';

interface Configuration {
  key: string;
  version: number;
  updated_at: string;
  description: string;
}

interface ConfigValue {
  value: any;
  version: number;
  description: string;
  updated_at: string;
}

interface HistoryEntry {
  changed_at: string;
  changed_by: string;
  change_reason: string;
  old_value: any;
  new_value: any;
}

interface ABTest {
  id: number;
  test_name: string;
  config_key: string;
  variants: string[];
  traffic_split: Record<string, number>;
  expires_at: string;
  is_active: boolean;
}

const API_BASE_URL = process.env.REACT_APP_CONFIG_API_URL || 'http://localhost:8001';

export const ConfigurationAdmin: React.FC = () => {
  const [configs, setConfigs] = useState<Configuration[]>([]);
  const [selectedConfig, setSelectedConfig] = useState<string | null>(null);
  const [configValue, setConfigValue] = useState<ConfigValue | null>(null);
  const [editingValue, setEditingValue] = useState<string>('');
  const [changeReason, setChangeReason] = useState<string>('');
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [abTests, setABTests] = useState<ABTest[]>([]);
  const [activeTab, setActiveTab] = useState<'configs' | 'ab-tests' | 'import-export'>('configs');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showNewABTest, setShowNewABTest] = useState(false);

  // Fetch all configurations
  const fetchConfigs = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/config`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        }
      });
      const data = await response.json();
      setConfigs(data.configs);
    } catch (err) {
      setError('Failed to fetch configurations');
    } finally {
      setLoading(false);
    }
  };

  // Fetch specific configuration value
  const fetchConfigValue = async (key: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/config/${key}`);
      const data = await response.json();
      setConfigValue({
        value: data,
        version: 1,
        description: '',
        updated_at: new Date().toISOString()
      });
      setEditingValue(JSON.stringify(data, null, 2));
    } catch (err) {
      setError('Failed to fetch configuration value');
    }
  };

  // Fetch configuration history
  const fetchHistory = async (key: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/config/${key}/history`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        }
      });
      const data = await response.json();
      setHistory(data.history);
    } catch (err) {
      setError('Failed to fetch configuration history');
    }
  };

  // Update configuration
  const updateConfig = async () => {
    if (!selectedConfig || !editingValue || !changeReason) {
      setError('Please provide a change reason');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/config/${selectedConfig}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        },
        body: JSON.stringify({
          value: JSON.parse(editingValue),
          reason: changeReason
        })
      });

      if (response.ok) {
        setSuccess('Configuration updated successfully');
        setChangeReason('');
        fetchConfigs();
        fetchConfigValue(selectedConfig);
        fetchHistory(selectedConfig);
      } else {
        throw new Error('Failed to update configuration');
      }
    } catch (err) {
      setError('Failed to update configuration. Please check JSON syntax.');
    } finally {
      setLoading(false);
    }
  };

  // Rollback configuration
  const rollbackConfig = async (version: number) => {
    if (!selectedConfig) return;

    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/config/${selectedConfig}/rollback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        },
        body: JSON.stringify({ version })
      });

      if (response.ok) {
        setSuccess('Configuration rolled back successfully');
        fetchConfigValue(selectedConfig);
        fetchHistory(selectedConfig);
      } else {
        throw new Error('Failed to rollback configuration');
      }
    } catch (err) {
      setError('Failed to rollback configuration');
    } finally {
      setLoading(false);
    }
  };

  // Fetch A/B tests
  const fetchABTests = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ab-tests`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        }
      });
      const data = await response.json();
      setABTests(data.tests);
    } catch (err) {
      setError('Failed to fetch A/B tests');
    }
  };

  // Stop A/B test
  const stopABTest = async (testId: number, winner?: string) => {
    try {
      setLoading(true);
      const url = `${API_BASE_URL}/ab-test/${testId}/stop`;
      const body = winner ? { winner } : {};
      
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        },
        body: JSON.stringify(body)
      });

      if (response.ok) {
        setSuccess('A/B test stopped successfully');
        fetchABTests();
      } else {
        throw new Error('Failed to stop A/B test');
      }
    } catch (err) {
      setError('Failed to stop A/B test');
    } finally {
      setLoading(false);
    }
  };

  // Export configurations
  const exportConfigs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/config/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        }
      });
      
      const data = await response.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `flash-config-export-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      
      setSuccess('Configurations exported successfully');
    } catch (err) {
      setError('Failed to export configurations');
    }
  };

  // Import configurations
  const importConfigs = async (file: File, overwrite: boolean) => {
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      const response = await fetch(`${API_BASE_URL}/config/import?overwrite=${overwrite}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      setSuccess(`Imported ${result.imported} configurations, skipped ${result.skipped}`);
      fetchConfigs();
    } catch (err) {
      setError('Failed to import configurations');
    }
  };

  useEffect(() => {
    fetchConfigs();
    fetchABTests();
  }, []);

  useEffect(() => {
    if (selectedConfig) {
      fetchConfigValue(selectedConfig);
      fetchHistory(selectedConfig);
    }
  }, [selectedConfig]);

  useEffect(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError(null);
        setSuccess(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, success]);

  return (
    <div className="configuration-admin">
      <div className="admin-header">
        <h1>Configuration Management</h1>
        <p>Manage dynamic configuration values for the FLASH platform</p>
      </div>

      {/* Notifications */}
      <AnimatePresence>
        {error && (
          <motion.div 
            className="notification error"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {error}
          </motion.div>
        )}
        {success && (
          <motion.div 
            className="notification success"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {success}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Tab Navigation */}
      <div className="admin-tabs">
        <button 
          className={`tab ${activeTab === 'configs' ? 'active' : ''}`}
          onClick={() => setActiveTab('configs')}
        >
          Configurations
        </button>
        <button 
          className={`tab ${activeTab === 'ab-tests' ? 'active' : ''}`}
          onClick={() => setActiveTab('ab-tests')}
        >
          A/B Tests
        </button>
        <button 
          className={`tab ${activeTab === 'import-export' ? 'active' : ''}`}
          onClick={() => setActiveTab('import-export')}
        >
          Import/Export
        </button>
      </div>

      {/* Configurations Tab */}
      {activeTab === 'configs' && (
        <div className="admin-content">
          <div className="config-layout">
            <div className="config-list">
              <h3>Configuration Keys</h3>
              {loading && <div className="loading">Loading...</div>}
              {configs.map(config => (
                <div
                  key={config.key}
                  className={`config-item ${selectedConfig === config.key ? 'selected' : ''}`}
                  onClick={() => setSelectedConfig(config.key)}
                >
                  <div className="config-key">{config.key}</div>
                  <div className="config-meta">
                    Version {config.version} • Updated {new Date(config.updated_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>

            <div className="config-editor">
              {selectedConfig ? (
                <>
                  <div className="editor-header">
                    <h3>{selectedConfig}</h3>
                    <button 
                      className="btn-secondary"
                      onClick={() => setShowHistory(!showHistory)}
                    >
                      {showHistory ? 'Hide History' : 'View History'}
                    </button>
                  </div>

                  {!showHistory ? (
                    <>
                      <div className="editor-section">
                        <label>Configuration Value (JSON)</label>
                        <textarea
                          className="json-editor"
                          value={editingValue}
                          onChange={(e) => setEditingValue(e.target.value)}
                          rows={20}
                        />
                      </div>

                      <div className="editor-section">
                        <label>Change Reason</label>
                        <input
                          type="text"
                          className="change-reason"
                          value={changeReason}
                          onChange={(e) => setChangeReason(e.target.value)}
                          placeholder="Describe why you're making this change"
                        />
                      </div>

                      <div className="editor-actions">
                        <button 
                          className="btn-primary"
                          onClick={updateConfig}
                          disabled={loading || !changeReason}
                        >
                          Update Configuration
                        </button>
                      </div>
                    </>
                  ) : (
                    <div className="history-section">
                      <h4>Change History</h4>
                      {history.map((entry, idx) => (
                        <div key={idx} className="history-entry">
                          <div className="history-header">
                            <span className="history-date">
                              {new Date(entry.changed_at).toLocaleString()}
                            </span>
                            <span className="history-user">by {entry.changed_by}</span>
                          </div>
                          <div className="history-reason">{entry.change_reason}</div>
                          <div className="history-actions">
                            <button 
                              className="btn-small"
                              onClick={() => rollbackConfig(idx)}
                            >
                              Rollback to this version
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <div className="no-selection">
                  Select a configuration to edit
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* A/B Tests Tab */}
      {activeTab === 'ab-tests' && (
        <div className="admin-content">
          <div className="ab-tests-header">
            <h3>Active A/B Tests</h3>
            <button 
              className="btn-primary"
              onClick={() => setShowNewABTest(true)}
            >
              Create New A/B Test
            </button>
          </div>

          <div className="ab-tests-list">
            {abTests.map(test => (
              <div key={test.id} className="ab-test-card">
                <div className="ab-test-header">
                  <h4>{test.test_name}</h4>
                  <span className={`status ${test.is_active ? 'active' : 'inactive'}`}>
                    {test.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="ab-test-details">
                  <div>Config Key: {test.config_key}</div>
                  <div>Variants: {test.variants.join(', ')}</div>
                  <div>Traffic Split: {Object.entries(test.traffic_split).map(([k, v]) => `${k}: ${v * 100}%`).join(', ')}</div>
                  <div>Expires: {new Date(test.expires_at).toLocaleDateString()}</div>
                </div>
                {test.is_active && (
                  <div className="ab-test-actions">
                    <button 
                      className="btn-secondary"
                      onClick={() => stopABTest(test.id)}
                    >
                      Stop Test
                    </button>
                    {test.variants.map(variant => (
                      <button 
                        key={variant}
                        className="btn-primary"
                        onClick={() => stopABTest(test.id, variant)}
                      >
                        Apply {variant} as Winner
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Import/Export Tab */}
      {activeTab === 'import-export' && (
        <div className="admin-content">
          <div className="import-export-section">
            <div className="export-section">
              <h3>Export Configurations</h3>
              <p>Download all current configurations as a JSON file</p>
              <button className="btn-primary" onClick={exportConfigs}>
                Export All Configurations
              </button>
            </div>

            <div className="import-section">
              <h3>Import Configurations</h3>
              <p>Upload a JSON file to import configurations</p>
              <input
                type="file"
                accept=".json"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    const overwrite = window.confirm('Overwrite existing configurations?');
                    importConfigs(file, overwrite);
                  }
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* New A/B Test Modal */}
      {showNewABTest && (
        <ABTestModal
          onClose={() => setShowNewABTest(false)}
          onCreated={() => {
            setShowNewABTest(false);
            fetchABTests();
            setSuccess('A/B test created successfully');
          }}
        />
      )}
    </div>
  );
};

// A/B Test Creation Modal
const ABTestModal: React.FC<{
  onClose: () => void;
  onCreated: () => void;
}> = ({ onClose, onCreated }) => {
  const [testName, setTestName] = useState('');
  const [configKey, setConfigKey] = useState('');
  const [variantA, setVariantA] = useState('');
  const [variantB, setVariantB] = useState('');
  const [splitA, setSplitA] = useState(50);
  const [duration, setDuration] = useState(30);

  const createTest = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ab-test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('adminToken') || 'demo-token'}`
        },
        body: JSON.stringify({
          test_name: testName,
          config_key: configKey,
          variants: {
            A: JSON.parse(variantA),
            B: JSON.parse(variantB)
          },
          traffic_split: {
            A: splitA / 100,
            B: (100 - splitA) / 100
          },
          duration_days: duration
        })
      });

      if (response.ok) {
        onCreated();
      }
    } catch (err) {
      alert('Failed to create A/B test. Please check JSON syntax.');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h3>Create New A/B Test</h3>
        
        <div className="form-group">
          <label>Test Name</label>
          <input
            type="text"
            value={testName}
            onChange={(e) => setTestName(e.target.value)}
            placeholder="e.g., Success Threshold Test"
          />
        </div>

        <div className="form-group">
          <label>Configuration Key</label>
          <input
            type="text"
            value={configKey}
            onChange={(e) => setConfigKey(e.target.value)}
            placeholder="e.g., success-thresholds"
          />
        </div>

        <div className="form-group">
          <label>Variant A (JSON)</label>
          <textarea
            value={variantA}
            onChange={(e) => setVariantA(e.target.value)}
            rows={5}
            placeholder='{"minProbability": 0.75, ...}'
          />
        </div>

        <div className="form-group">
          <label>Variant B (JSON)</label>
          <textarea
            value={variantB}
            onChange={(e) => setVariantB(e.target.value)}
            rows={5}
            placeholder='{"minProbability": 0.80, ...}'
          />
        </div>

        <div className="form-group">
          <label>Traffic Split (A: {splitA}%, B: {100 - splitA}%)</label>
          <input
            type="range"
            min="0"
            max="100"
            value={splitA}
            onChange={(e) => setSplitA(Number(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Duration (days)</label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
            min="1"
            max="90"
          />
        </div>

        <div className="modal-actions">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={createTest}>Create Test</button>
        </div>
      </div>
    </div>
  );
};