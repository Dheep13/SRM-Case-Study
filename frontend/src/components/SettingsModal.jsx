import React, { useState, useEffect } from 'react';
import { FiSettings, FiX, FiSave, FiRefreshCw, FiCheck } from 'react-icons/fi';
import api from '../utils/api';

function SettingsModal({ isOpen, onClose, onSave }) {
  const [settings, setSettings] = useState({});
  const [activeTab, setActiveTab] = useState('ai');
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    setLoading(true);
    try {
      const response = await api.admin.settings();
      const data = await response.json();
      setSettings(data);
    } catch (error) {
      console.error('Error loading settings:', error);
    }
    setLoading(false);
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const response = await api.admin.updateSettings(settings);
      
      if (response.ok) {
        setSaved(true);
        setTimeout(() => {
          setSaved(false);
          onSave && onSave(settings);
        }, 2000);
      }
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Failed to save settings');
    }
    setLoading(false);
  };

  const handleReset = async () => {
    if (confirm('Reset all settings to defaults?')) {
      try {
        await api.admin.resetSettings();
        loadSettings();
      } catch (error) {
        console.error('Error resetting settings:', error);
      }
    }
  };

  const updateSetting = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content settings-modal" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <h2>
            <FiSettings style={{ marginRight: '0.5rem' }} />
            Admin Configuration
          </h2>
          <button className="close-btn" onClick={onClose}>
            <FiX />
          </button>
        </div>

        {/* Tabs */}
        <div className="settings-tabs">
          <button 
            className={activeTab === 'ai' ? 'active' : ''}
            onClick={() => setActiveTab('ai')}
          >
            AI Models
          </button>
          <button 
            className={activeTab === 'agents' ? 'active' : ''}
            onClick={() => setActiveTab('agents')}
          >
            Agents
          </button>
          <button 
            className={activeTab === 'trending' ? 'active' : ''}
            onClick={() => setActiveTab('trending')}
          >
            Trending
          </button>
          <button 
            className={activeTab === 'api' ? 'active' : ''}
            onClick={() => setActiveTab('api')}
          >
            API
          </button>
          <button 
            className={activeTab === 'rag' ? 'active' : ''}
            onClick={() => setActiveTab('rag')}
          >
            RAG
          </button>
          <button 
            className={activeTab === 'platforms' ? 'active' : ''}
            onClick={() => setActiveTab('platforms')}
          >
            Platform Access
          </button>
        </div>

        {/* Content */}
        <div className="settings-content">
          {loading ? (
            <div className="loading-spinner" style={{ textAlign: 'center', padding: '2rem' }}>
              <div className="spinner"></div>
              <p>Loading settings...</p>
            </div>
          ) : (
            <>
              {activeTab === 'ai' && <AIModelsTab settings={settings} updateSetting={updateSetting} />}
              {activeTab === 'agents' && <AgentsTab settings={settings} updateSetting={updateSetting} />}
              {activeTab === 'trending' && <TrendingTab settings={settings} updateSetting={updateSetting} />}
              {activeTab === 'api' && <APITab settings={settings} updateSetting={updateSetting} />}
              {activeTab === 'rag' && <RAGTab settings={settings} updateSetting={updateSetting} />}
              {activeTab === 'platforms' && <PlatformAccessTab settings={settings} updateSetting={updateSetting} />}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <button className="btn-secondary" onClick={handleReset} disabled={loading}>
            <FiRefreshCw /> Reset to Defaults
          </button>
          <div className="modal-footer-right">
            <button className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button 
              className="btn-primary" 
              onClick={handleSave}
              disabled={loading}
            >
              {saved ? <FiCheck /> : <FiSave />}
              {saved ? 'Saved!' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// AI Models Tab
function AIModelsTab({ settings, updateSetting }) {
  const aiSettings = settings.ai_models || {};

  return (
    <div className="settings-tab-content">
      <h3>AI Model Configuration</h3>
      
      <div className="form-group">
        <label>LLM Model</label>
        <select 
          value={aiSettings.llm_model || 'gpt-4-turbo-preview'}
          onChange={e => updateSetting('ai_models', 'llm_model', e.target.value)}
        >
          <option value="gpt-4-turbo-preview">GPT-4 Turbo</option>
          <option value="gpt-4o">GPT-4o</option>
          <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
        </select>
      </div>

      <div className="form-group">
        <label>Temperature: {aiSettings.temperature || 0.7}</label>
        <input 
          type="range" 
          min="0" 
          max="2" 
          step="0.1"
          value={aiSettings.temperature || 0.7}
          onChange={e => updateSetting('ai_models', 'temperature', parseFloat(e.target.value))}
        />
        <span className="helper-text">Controls randomness (0=deterministic, 2=creative)</span>
      </div>

      <div className="form-group">
        <label>Max Tokens</label>
        <input 
          type="number" 
          min="100" 
          max="4000"
          value={aiSettings.max_tokens || 2000}
          onChange={e => updateSetting('ai_models', 'max_tokens', parseInt(e.target.value))}
        />
      </div>

      <div className="form-group">
        <label>Embeddings Model</label>
        <input 
          type="text"
          value={aiSettings.embeddings_model || 'text-embedding-3-small'}
          onChange={e => updateSetting('ai_models', 'embeddings_model', e.target.value)}
        />
      </div>
    </div>
  );
}

// Agents Tab
function AgentsTab({ settings, updateSetting }) {
  const agentsSettings = settings.agents || {};

  return (
    <div className="settings-tab-content">
      <h3>Agent Configuration</h3>
      
      <div className="setting-section">
        <h4>Content Scraper</h4>
        <div className="form-group">
          <label className="checkbox-label">
            <input 
              type="checkbox"
              checked={agentsSettings.content_scraper?.enabled !== false}
              onChange={e => updateSetting('agents', 'content_scraper', {
                ...agentsSettings.content_scraper,
                enabled: e.target.checked
              })}
            />
            <span>Enable Content Scraper</span>
          </label>
        </div>
        <div className="form-group">
          <label>Max Search Results</label>
          <input 
            type="number" 
            min="5" 
            max="50"
            value={agentsSettings.content_scraper?.max_search_results || 10}
            onChange={e => updateSetting('agents', 'content_scraper', {
              ...agentsSettings.content_scraper,
              max_search_results: parseInt(e.target.value)
            })}
          />
        </div>
      </div>

      <div className="setting-section">
        <h4>Trend Analyzer</h4>
        <div className="form-group">
          <label className="checkbox-label">
            <input 
              type="checkbox"
              checked={agentsSettings.trend_analyzer?.enabled !== false}
              onChange={e => updateSetting('agents', 'trend_analyzer', {
                ...agentsSettings.trend_analyzer,
                enabled: e.target.checked
              })}
            />
            <span>Enable Trend Analyzer</span>
          </label>
        </div>
        <div className="form-group">
          <label>Max Trend Items</label>
          <input 
            type="number" 
            min="5" 
            max="50"
            value={agentsSettings.trend_analyzer?.max_trend_items || 15}
            onChange={e => updateSetting('agents', 'trend_analyzer', {
              ...agentsSettings.trend_analyzer,
              max_trend_items: parseInt(e.target.value)
            })}
          />
        </div>
      </div>
    </div>
  );
}

// Trending Tab
function TrendingTab({ settings, updateSetting }) {
  const trendingSettings = settings.trending || {};

  return (
    <div className="settings-tab-content">
      <h3>Trending Skills Algorithm</h3>
      
      <div className="form-group">
        <label>Trending Threshold: {trendingSettings.trending_threshold || 70}</label>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={trendingSettings.trending_threshold || 70}
          onChange={e => updateSetting('trending', 'trending_threshold', parseInt(e.target.value))}
        />
        <span className="helper-text">Minimum score to consider a skill "trending"</span>
      </div>

      <div className="form-group">
        <label>Mention Weight: {trendingSettings.mention_weight || 0.5}</label>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          value={trendingSettings.mention_weight || 0.5}
          onChange={e => updateSetting('trending', 'mention_weight', parseFloat(e.target.value))}
        />
      </div>

      <div className="form-group">
        <label>GitHub Weight: {trendingSettings.github_weight || 0.3}</label>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          value={trendingSettings.github_weight || 0.3}
          onChange={e => updateSetting('trending', 'github_weight', parseFloat(e.target.value))}
        />
      </div>

      <div className="form-group">
        <label>LinkedIn Weight: {trendingSettings.linkedin_weight || 0.2}</label>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          value={trendingSettings.linkedin_weight || 0.2}
          onChange={e => updateSetting('trending', 'linkedin_weight', parseFloat(e.target.value))}
        />
      </div>

      <div className="form-group">
        <label>Trend Window (days)</label>
        <input 
          type="number" 
          min="7" 
          max="90"
          value={trendingSettings.trend_window_days || 30}
          onChange={e => updateSetting('trending', 'trend_window_days', parseInt(e.target.value))}
        />
      </div>
    </div>
  );
}

// API Tab
function APITab({ settings, updateSetting }) {
  const apiSettings = settings.api_endpoints || {};

  return (
    <div className="settings-tab-content">
      <h3>API Configuration</h3>
      
      <div className="form-group">
        <label>GitHub API URL</label>
        <input 
          type="text"
          value={apiSettings.github_api || 'https://api.github.com'}
          onChange={e => updateSetting('api_endpoints', 'github_api', e.target.value)}
        />
      </div>

      <div className="form-group">
        <label className="checkbox-label">
          <input 
            type="checkbox"
            checked={apiSettings.tavily_enabled !== false}
            onChange={e => updateSetting('api_endpoints', 'tavily_enabled', e.target.checked)}
          />
          <span>Enable Tavily Search</span>
        </label>
      </div>
    </div>
  );
}

// RAG Tab
function RAGTab({ settings, updateSetting }) {
  const ragSettings = settings.rag_workflow || {};

  return (
    <div className="settings-tab-content">
      <h3>RAG Workflow Configuration</h3>
      
      <div className="form-group">
        <label className="checkbox-label">
          <input 
            type="checkbox"
            checked={ragSettings.enable_reasoning !== false}
            onChange={e => updateSetting('rag_workflow', 'enable_reasoning', e.target.checked)}
          />
          <span>Enable Reasoning Step</span>
        </label>
      </div>

      <div className="form-group">
        <label className="checkbox-label">
          <input 
            type="checkbox"
            checked={ragSettings.enable_refinement !== false}
            onChange={e => updateSetting('rag_workflow', 'enable_refinement', e.target.checked)}
          />
          <span>Enable Refinement Step</span>
        </label>
      </div>

      <div className="form-group">
        <label>Confidence Threshold: {ragSettings.confidence_threshold || 0.7}</label>
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
          value={ragSettings.confidence_threshold || 0.7}
          onChange={e => updateSetting('rag_workflow', 'confidence_threshold', parseFloat(e.target.value))}
        />
      </div>
    </div>
  );
}

function PlatformAccessTab({ settings, updateSetting }) {
  const platforms = settings.platforms || {};
  
  const updatePlatformSetting = (platform, key, value) => {
    const updatedPlatforms = { ...platforms };
    if (!updatedPlatforms[platform]) {
      updatedPlatforms[platform] = {};
    }
    updatedPlatforms[platform][key] = value;
    updateSetting('platforms', platform, updatedPlatforms[platform]);
  };

  const getAccessLevelColor = (level) => {
    switch (level) {
      case 'allowed': return '#10b981';
      case 'restricted': return '#f59e0b';
      case 'blocked': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="setting-section">
      <h3>Platform Access Control</h3>
      <p className="helper-text">
        Control which external platforms agents can access. Universities can restrict access to maintain security and compliance.
      </p>
      
      <div className="platforms-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
        {Object.entries(platforms).map(([platformName, config]) => (
          <div key={platformName} className="platform-card" style={{ 
            border: '1px solid #e5e7eb', 
            borderRadius: '8px', 
            padding: '1rem',
            backgroundColor: '#f9fafb'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <h4 style={{ margin: 0, textTransform: 'capitalize' }}>{platformName}</h4>
              <span style={{ 
                padding: '0.25rem 0.5rem', 
                borderRadius: '4px', 
                fontSize: '0.75rem',
                fontWeight: 'bold',
                color: 'white',
                backgroundColor: getAccessLevelColor(config.access_level)
              }}>
                {config.access_level}
              </span>
            </div>
            
            <div style={{ marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.875rem', fontWeight: '500' }}>Access Level:</label>
              <select
                value={config.access_level || 'blocked'}
                onChange={e => updatePlatformSetting(platformName, 'access_level', e.target.value)}
                style={{ 
                  width: '100%', 
                  padding: '0.5rem', 
                  marginTop: '0.25rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '4px'
                }}
              >
                <option value="blocked">Blocked</option>
                <option value="restricted">Restricted</option>
                <option value="allowed">Allowed</option>
              </select>
            </div>

            <div style={{ marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.875rem', fontWeight: '500' }}>Rate Limit (requests/hour):</label>
              <input
                type="number"
                value={config.rate_limit || 0}
                onChange={e => updatePlatformSetting(platformName, 'rate_limit', parseInt(e.target.value))}
                style={{ 
                  width: '100%', 
                  padding: '0.5rem', 
                  marginTop: '0.25rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '4px'
                }}
              />
            </div>

            <div style={{ marginBottom: '0.5rem' }}>
              <label style={{ fontSize: '0.875rem', fontWeight: '500' }}>Blocked Keywords:</label>
              <textarea
                value={(config.blocked_keywords || []).join(', ')}
                onChange={e => updatePlatformSetting(platformName, 'blocked_keywords', e.target.value.split(',').map(s => s.trim()).filter(s => s))}
                placeholder="Enter keywords separated by commas"
                style={{ 
                  width: '100%', 
                  padding: '0.5rem', 
                  marginTop: '0.25rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '4px',
                  minHeight: '60px',
                  resize: 'vertical'
                }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.875rem', fontWeight: '500' }}>Allowed Content Types:</label>
              <textarea
                value={(config.allowed_content_types || []).join(', ')}
                onChange={e => updatePlatformSetting(platformName, 'allowed_content_types', e.target.value.split(',').map(s => s.trim()).filter(s => s))}
                placeholder="Enter content types separated by commas"
                style={{ 
                  width: '100%', 
                  padding: '0.5rem', 
                  marginTop: '0.25rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '4px',
                  minHeight: '60px',
                  resize: 'vertical'
                }}
              />
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
        <h4 style={{ margin: '0 0 0.5rem 0' }}>Quick Actions</h4>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => {
              Object.keys(platforms).forEach(platform => {
                updatePlatformSetting(platform, 'access_level', 'allowed');
              });
            }}
            style={{ padding: '0.5rem 1rem', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Allow All Platforms
          </button>
          <button
            onClick={() => {
              Object.keys(platforms).forEach(platform => {
                updatePlatformSetting(platform, 'access_level', 'blocked');
              });
            }}
            style={{ padding: '0.5rem 1rem', backgroundColor: '#ef4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Block All Platforms
          </button>
          <button
            onClick={() => {
              ['reddit', 'twitter', 'facebook'].forEach(platform => {
                if (platforms[platform]) {
                  updatePlatformSetting(platform, 'access_level', 'blocked');
                }
              });
            }}
            style={{ padding: '0.5rem 1rem', backgroundColor: '#f59e0b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Block Social Media
          </button>
        </div>
      </div>
    </div>
  );
}

export default SettingsModal;

