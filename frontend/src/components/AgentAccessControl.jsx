import React, { useState, useEffect } from 'react';
import { FiShield, FiGlobe, FiCpu, FiLock, FiUnlock, FiAlertTriangle, FiCheckCircle, FiXCircle, FiRefreshCw, FiSave } from 'react-icons/fi';
import api from '../utils/api';
import AddPlatformModal from './AddPlatformModal';

function AgentAccessControl() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [auditLog, setAuditLog] = useState([]);
  const [testResult, setTestResult] = useState(null);
  const [activeTab, setActiveTab] = useState('platforms');
  const [message, setMessage] = useState(null);
  const [showAddPlatformModal, setShowAddPlatformModal] = useState(false);

  useEffect(() => {
    loadConfig();
    loadAuditLog();
  }, []);

  const loadConfig = async () => {
    setLoading(true);
    try {
      const res = await api.admin.agentAccess.get();
      const data = await res.json();
      setConfig(data);
    } catch (error) {
      console.error('Error loading config:', error);
      showMessage('Failed to load configuration', 'error');
    }
    setLoading(false);
  };

  const loadAuditLog = async () => {
    try {
      const res = await api.admin.agentAccess.audit(50);
      const data = await res.json();
      setAuditLog(data.entries || []);
    } catch (error) {
      console.error('Error loading audit log:', error);
    }
  };

  const saveConfig = async () => {
    setSaving(true);
    try {
      const res = await api.admin.agentAccess.update(config);
      const data = await res.json();
      showMessage(data.message || 'Configuration saved successfully', 'success');
      await loadAuditLog(); // Refresh audit log
    } catch (error) {
      console.error('Error saving config:', error);
      showMessage('Failed to save configuration', 'error');
    }
    setSaving(false);
  };

  const testAccess = async (agentName, platform) => {
    if (!config.platforms[platform]) return;
    
    const testData = {
      agent_name: agentName,
      platform: platform,
      endpoint: config.platforms[platform].api_endpoints[0] || '',
      content_type: config.platforms[platform].allowed_content_types?.[0] || null
    };

    try {
      const res = await api.admin.agentAccess.test(testData);
      const data = await res.json();
      setTestResult(data);
      showMessage(`Access ${data.allowed ? 'ALLOWED' : 'DENIED'} for ${agentName} to ${platform}`, data.allowed ? 'success' : 'error');
    } catch (error) {
      console.error('Error testing access:', error);
      showMessage('Test failed', 'error');
    }
  };

  const updatePlatformAccess = (platformName, field, value) => {
    setConfig(prev => ({
      ...prev,
      platforms: {
        ...prev.platforms,
        [platformName]: {
          ...prev.platforms[platformName],
          [field]: value
        }
      }
    }));
  };

  const updateAgentConfig = (agentName, field, value) => {
    setConfig(prev => ({
      ...prev,
      agents: {
        ...prev.agents,
        [agentName]: {
          ...prev.agents[agentName],
          [field]: value
        }
      }
    }));
  };

  const addEndpoint = (platformName) => {
    const newEndpoint = prompt('Enter new API endpoint URL:');
    if (newEndpoint) {
      const currentEndpoints = config.platforms[platformName].api_endpoints || [];
      updatePlatformAccess(platformName, 'api_endpoints', [...currentEndpoints, newEndpoint]);
    }
  };

  const removeEndpoint = (platformName, index) => {
    const currentEndpoints = config.platforms[platformName].api_endpoints || [];
    updatePlatformAccess(platformName, 'api_endpoints', currentEndpoints.filter((_, i) => i !== index));
  };

  const addKeyword = (platformName) => {
    const newKeyword = prompt('Enter blocked keyword:');
    if (newKeyword) {
      const currentKeywords = config.platforms[platformName].blocked_keywords || [];
      updatePlatformAccess(platformName, 'blocked_keywords', [...currentKeywords, newKeyword]);
    }
  };

  const removeKeyword = (platformName, index) => {
    const currentKeywords = config.platforms[platformName].blocked_keywords || [];
    updatePlatformAccess(platformName, 'blocked_keywords', currentKeywords.filter((_, i) => i !== index));
  };

  const addNewPlatform = (platformKey, platformConfig) => {
    // Add new platform to config
    setConfig(prev => ({
      ...prev,
      platforms: {
        ...prev.platforms,
        [platformKey]: platformConfig
      }
    }));
    
    showMessage(`Platform "${platformConfig.name}" added successfully!`, 'success');
  };

  const removePlatform = (platformKey) => {
    if (!confirm(`Are you sure you want to remove platform "${config.platforms[platformKey].name}"?`)) {
      return;
    }
    
    // Remove platform from config
    const newPlatforms = { ...config.platforms };
    delete newPlatforms[platformKey];
    
    // Remove platform from all agents' allowed lists
    const newAgents = { ...config.agents };
    Object.keys(newAgents).forEach(agentKey => {
      newAgents[agentKey].allowed_platforms = newAgents[agentKey].allowed_platforms.filter(
        p => p !== platformKey
      );
    });
    
    setConfig(prev => ({
      ...prev,
      platforms: newPlatforms,
      agents: newAgents
    }));
    
    showMessage(`Platform removed successfully`, 'success');
  };

  const showMessage = (text, type = 'info') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 5000);
  };

  const getAccessLevelColor = (level) => {
    switch(level) {
      case 'allowed': return '#10b981';
      case 'restricted': return '#f59e0b';
      case 'blocked': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getAccessLevelIcon = (level) => {
    switch(level) {
      case 'allowed': return <FiUnlock />;
      case 'restricted': return <FiAlertTriangle />;
      case 'blocked': return <FiLock />;
      default: return <FiShield />;
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <FiRefreshCw className="spin" style={{ fontSize: '2rem', color: '#6366f1' }} />
        <p style={{ marginTop: '1rem', color: '#6b7280' }}>Loading access control configuration...</p>
      </div>
    );
  }

  if (!config) return null;

  return (
    <div className="agent-access-control">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#1f2937', margin: 0 }}>
            <FiShield style={{ marginRight: '0.5rem', display: 'inline' }} />
            Agent Access Control
          </h2>
          <p style={{ color: '#6b7280', marginTop: '0.25rem', fontSize: '0.875rem' }}>
            Manage agent permissions, platforms, and security policies
          </p>
        </div>
        <button
          onClick={saveConfig}
          disabled={saving}
          style={{
            padding: '0.75rem 1.5rem',
            background: saving ? '#9ca3af' : '#6366f1',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: saving ? 'not-allowed' : 'pointer',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          {saving ? <FiRefreshCw className="spin" /> : <FiSave />}
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Message Banner */}
      {message && (
        <div style={{
          padding: '1rem',
          marginBottom: '1rem',
          borderRadius: '8px',
          background: message.type === 'success' ? '#d1fae5' : message.type === 'error' ? '#fee2e2' : '#dbeafe',
          color: message.type === 'success' ? '#065f46' : message.type === 'error' ? '#991b1b' : '#1e40af',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          {message.type === 'success' ? <FiCheckCircle /> : message.type === 'error' ? <FiXCircle /> : <FiAlertTriangle />}
          {message.text}
        </div>
      )}

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '0.5rem',
        borderBottom: '2px solid #e5e7eb',
        marginBottom: '1.5rem'
      }}>
        <button
          onClick={() => setActiveTab('platforms')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'platforms' ? '#6366f1' : 'transparent',
            color: activeTab === 'platforms' ? 'white' : '#6b7280',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            cursor: 'pointer',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <FiGlobe /> Platforms
        </button>
        <button
          onClick={() => setActiveTab('agents')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'agents' ? '#6366f1' : 'transparent',
            color: activeTab === 'agents' ? 'white' : '#6b7280',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            cursor: 'pointer',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <FiCpu /> Agents
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'audit' ? '#6366f1' : 'transparent',
            color: activeTab === 'audit' ? 'white' : '#6b7280',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            cursor: 'pointer',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <FiShield /> Audit Log
        </button>
      </div>

      {/* Platforms Tab */}
      {activeTab === 'platforms' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <p style={{ color: '#6b7280', margin: 0 }}>
              Configure platform access levels, rate limits, and security policies
            </p>
            <button
              onClick={() => setShowAddPlatformModal(true)}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#10b981',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '500',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}
            >
              + Add New Platform
            </button>
          </div>
          {Object.entries(config.platforms).map(([platformName, platform]) => (
            <div key={platformName} style={{
              background: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '12px',
              padding: '1.5rem',
              marginBottom: '1rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <h3 style={{
                    fontSize: '1.25rem',
                    fontWeight: '600',
                    color: '#1f2937',
                    margin: 0,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    {getAccessLevelIcon(platform.access_level)}
                    {platform.name}
                  </h3>
                  <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.25rem' }}>
                    {platform.domain}
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'start' }}>
                  <select
                    value={platform.access_level}
                    onChange={(e) => updatePlatformAccess(platformName, 'access_level', e.target.value)}
                    style={{
                      padding: '0.5rem 1rem',
                      borderRadius: '8px',
                      border: `2px solid ${getAccessLevelColor(platform.access_level)}`,
                      color: getAccessLevelColor(platform.access_level),
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    <option value="allowed">Allowed</option>
                    <option value="restricted">Restricted</option>
                    <option value="blocked">Blocked</option>
                  </select>
                  <button
                    onClick={() => removePlatform(platformName)}
                    title="Remove platform"
                    style={{
                      padding: '0.5rem 1rem',
                      background: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontWeight: '500'
                    }}
                  >
                    Remove
                  </button>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                    Rate Limit (requests/hour)
                  </label>
                  <input
                    type="number"
                    value={platform.rate_limit || 0}
                    onChange={(e) => updatePlatformAccess(platformName, 'rate_limit', parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      borderRadius: '6px',
                      border: '1px solid #d1d5db'
                    }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                    Allowed Content Types
                  </label>
                  <input
                    type="text"
                    value={(platform.allowed_content_types || []).join(', ')}
                    onChange={(e) => updatePlatformAccess(platformName, 'allowed_content_types', e.target.value.split(',').map(s => s.trim()))}
                    placeholder="web, courses, documentation"
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      borderRadius: '6px',
                      border: '1px solid #d1d5db'
                    }}
                  />
                </div>
              </div>

              {/* API Endpoints */}
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label style={{ fontWeight: '500', color: '#374151' }}>
                    API Endpoints
                  </label>
                  <button
                    onClick={() => addEndpoint(platformName)}
                    style={{
                      padding: '0.25rem 0.75rem',
                      background: '#6366f1',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '0.875rem'
                    }}
                  >
                    + Add
                  </button>
                </div>
                <div style={{ maxHeight: '150px', overflowY: 'auto', background: '#f9fafb', borderRadius: '6px', padding: '0.5rem' }}>
                  {(platform.api_endpoints || []).map((endpoint, idx) => (
                    <div key={idx} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '0.5rem',
                      marginBottom: '0.25rem',
                      background: 'white',
                      borderRadius: '4px'
                    }}>
                      <code style={{ fontSize: '0.875rem', color: '#6366f1' }}>{endpoint}</code>
                      <button
                        onClick={() => removeEndpoint(platformName, idx)}
                        style={{
                          padding: '0.25rem 0.5rem',
                          background: '#ef4444',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.75rem'
                        }}
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Blocked Keywords */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label style={{ fontWeight: '500', color: '#374151' }}>
                    Blocked Keywords
                  </label>
                  <button
                    onClick={() => addKeyword(platformName)}
                    style={{
                      padding: '0.25rem 0.75rem',
                      background: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '0.875rem'
                    }}
                  >
                    + Add
                  </button>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {(platform.blocked_keywords || []).map((keyword, idx) => (
                    <span key={idx} style={{
                      padding: '0.25rem 0.75rem',
                      background: '#fee2e2',
                      color: '#991b1b',
                      borderRadius: '999px',
                      fontSize: '0.875rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}>
                      {keyword}
                      <button
                        onClick={() => removeKeyword(platformName, idx)}
                        style={{
                          background: 'none',
                          border: 'none',
                          color: '#991b1b',
                          cursor: 'pointer',
                          padding: 0,
                          display: 'flex',
                          alignItems: 'center'
                        }}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Agents Tab */}
      {activeTab === 'agents' && (
        <div>
          <p style={{ color: '#6b7280', marginBottom: '1rem' }}>
            Configure agent behavior, permissions, and resource limits
          </p>
          {Object.entries(config.agents).map(([agentName, agent]) => (
            <div key={agentName} style={{
              background: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '12px',
              padding: '1.5rem',
              marginBottom: '1rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{
                    fontSize: '1.25rem',
                    fontWeight: '600',
                    color: '#1f2937',
                    margin: 0
                  }}>
                    {agent.agent_name}
                  </h3>
                  <p style={{ color: '#6b7280', fontSize: '0.875rem', marginTop: '0.25rem' }}>
                    Agent Key: <code style={{ background: '#f3f4f6', padding: '0.125rem 0.5rem', borderRadius: '4px' }}>{agentName}</code>
                  </p>
                </div>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={agent.enabled}
                    onChange={(e) => updateAgentConfig(agentName, 'enabled', e.target.checked)}
                    style={{ width: '20px', height: '20px', cursor: 'pointer' }}
                  />
                  <span style={{ fontWeight: '500', color: agent.enabled ? '#10b981' : '#ef4444' }}>
                    {agent.enabled ? 'Enabled' : 'Disabled'}
                  </span>
                </label>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                    Max Search Results
                  </label>
                  <input
                    type="number"
                    value={agent.max_search_results}
                    onChange={(e) => updateAgentConfig(agentName, 'max_search_results', parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      borderRadius: '6px',
                      border: '1px solid #d1d5db'
                    }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                    Timeout (seconds)
                  </label>
                  <input
                    type="number"
                    value={agent.timeout_seconds}
                    onChange={(e) => updateAgentConfig(agentName, 'timeout_seconds', parseInt(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      borderRadius: '6px',
                      border: '1px solid #d1d5db'
                    }}
                  />
                </div>
              </div>

              {/* Allowed Platforms */}
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                  Allowed Platforms
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '0.5rem' }}>
                  {Object.keys(config.platforms).map(platformName => (
                    <label key={platformName} style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '0.5rem',
                      background: agent.allowed_platforms.includes(platformName) ? '#dbeafe' : '#f9fafb',
                      borderRadius: '6px',
                      cursor: 'pointer'
                    }}>
                      <input
                        type="checkbox"
                        checked={agent.allowed_platforms.includes(platformName)}
                        onChange={(e) => {
                          const newPlatforms = e.target.checked
                            ? [...agent.allowed_platforms, platformName]
                            : agent.allowed_platforms.filter(p => p !== platformName);
                          updateAgentConfig(agentName, 'allowed_platforms', newPlatforms);
                        }}
                        style={{ width: '16px', height: '16px', cursor: 'pointer' }}
                      />
                      <span style={{ fontSize: '0.875rem' }}>{platformName}</span>
                      <button
                        onClick={() => testAccess(agentName, platformName)}
                        style={{
                          marginLeft: 'auto',
                          padding: '0.125rem 0.375rem',
                          background: '#6366f1',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '0.75rem'
                        }}
                      >
                        Test
                      </button>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Audit Log Tab */}
      {activeTab === 'audit' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <p style={{ color: '#6b7280', margin: 0 }}>
              Recent agent access attempts and configuration changes
            </p>
            <button
              onClick={loadAuditLog}
              style={{
                padding: '0.5rem 1rem',
                background: '#6366f1',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}
            >
              <FiRefreshCw /> Refresh
            </button>
          </div>
          <div style={{
            background: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '12px',
            overflow: 'hidden'
          }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ background: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                <tr>
                  <th style={{ padding: '1rem', textAlign: 'left', fontWeight: '600', color: '#374151' }}>Timestamp</th>
                  <th style={{ padding: '1rem', textAlign: 'left', fontWeight: '600', color: '#374151' }}>Type</th>
                  <th style={{ padding: '1rem', textAlign: 'left', fontWeight: '600', color: '#374151' }}>Agent</th>
                  <th style={{ padding: '1rem', textAlign: 'left', fontWeight: '600', color: '#374151' }}>Platform</th>
                  <th style={{ padding: '1rem', textAlign: 'left', fontWeight: '600', color: '#374151' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {auditLog.map((entry, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb' }}>
                    <td style={{ padding: '1rem', fontSize: '0.875rem', color: '#6b7280' }}>
                      {new Date(entry.timestamp).toLocaleString()}
                    </td>
                    <td style={{ padding: '1rem', fontSize: '0.875rem' }}>
                      <span style={{
                        padding: '0.25rem 0.75rem',
                        background: entry.type === 'config_change' ? '#dbeafe' : '#fef3c7',
                        color: entry.type === 'config_change' ? '#1e40af' : '#92400e',
                        borderRadius: '999px',
                        fontSize: '0.75rem',
                        fontWeight: '500'
                      }}>
                        {entry.type}
                      </span>
                    </td>
                    <td style={{ padding: '1rem', fontSize: '0.875rem', color: '#374151' }}>
                      {entry.agent || '—'}
                    </td>
                    <td style={{ padding: '1rem', fontSize: '0.875rem', color: '#374151' }}>
                      {entry.platform || entry.description || '—'}
                    </td>
                    <td style={{ padding: '1rem' }}>
                      {entry.type === 'access_attempt' && (
                        <span style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                          color: entry.allowed ? '#10b981' : '#ef4444',
                          fontWeight: '500',
                          fontSize: '0.875rem'
                        }}>
                          {entry.allowed ? <FiCheckCircle /> : <FiXCircle />}
                          {entry.allowed ? 'Allowed' : 'Denied'}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Add Platform Modal */}
      <AddPlatformModal
        isOpen={showAddPlatformModal}
        onClose={() => setShowAddPlatformModal(false)}
        onAdd={addNewPlatform}
        existingPlatforms={config ? Object.keys(config.platforms) : []}
      />
    </div>
  );
}

export default AgentAccessControl;

