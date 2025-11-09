import React, { useState, useEffect } from 'react';
import { FiSettings, FiServer, FiDatabase, FiActivity, FiList, FiCheckCircle, FiXCircle, FiShield } from 'react-icons/fi';
import api from '../utils/api';
import AgentAccessControl from '../components/AgentAccessControl';

function Admin() {
  const [health, setHealth] = useState(null);
  const [auditLog, setAuditLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState(null);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      // Load health status
      const healthRes = await api.admin.health();
      const healthData = await healthRes.json();
      setHealth(healthData);

      // Load audit log
      const auditRes = await api.admin.auditLog(20);
      const auditData = await auditRes.json();
      setAuditLog(auditData.entries || []);

      // Load current config
      const configRes = await api.admin.settings();
      const configData = await configRes.json();
      setConfig(configData);
    } catch (error) {
      console.error('Error loading admin data:', error);
    }
    setLoading(false);
  };

  const getStatusColor = (status) => {
    return status === 'healthy' || status === 'connected' ? '#10b981' : '#ef4444';
  };

  const getStatusIcon = (status) => {
    return status === 'healthy' || status === 'connected' ? <FiCheckCircle /> : <FiXCircle />;
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">
          <FiSettings style={{ marginRight: '0.5rem', display: 'inline' }} />
          Admin Dashboard
        </h1>
        <p className="page-subtitle">System configuration and monitoring</p>
      </div>

      {/* System Health Cards */}
      {health && (
        <div className="stats-grid">
          <div className="stat-card" style={{ borderLeft: `4px solid ${getStatusColor(health.status)}` }}>
            <div className="stat-header">
              {getStatusIcon(health.status)}
              <h3>System Status</h3>
            </div>
            <div className="stat-value" style={{ color: getStatusColor(health.status) }}>
              {health.status?.toUpperCase() || 'UNKNOWN'}
            </div>
          </div>

          <div className="stat-card" style={{ borderLeft: `4px solid ${getStatusColor(health.database)}` }}>
            <div className="stat-header">
              <FiDatabase />
              <h3>Database</h3>
            </div>
            <div className="stat-value" style={{ color: getStatusColor(health.database) }}>
              {health.database?.toUpperCase() || 'UNKNOWN'}
            </div>
          </div>

          <div className="stat-card" style={{ borderLeft: `4px solid ${health.config_loaded ? '#10b981' : '#ef4444'}` }}>
            <div className="stat-header">
              <FiSettings />
              <h3>Configuration</h3>
            </div>
            <div className="stat-value" style={{ color: health.config_loaded ? '#10b981' : '#ef4444' }}>
              {health.config_loaded ? 'LOADED' : 'NOT LOADED'}
            </div>
          </div>
        </div>
      )}

      {/* Current Configuration Overview */}
      {config && (
        <div className="section">
          <h2 className="section-title">
            <FiList style={{ marginRight: '0.5rem', display: 'inline' }} />
            Current Configuration
          </h2>

          <div className="config-cards-grid">
            <div className="config-card">
              <h4>AI Models</h4>
              <ul className="config-list">
                <li><strong>LLM:</strong> {config.ai_models?.llm_model || 'gpt-4-turbo-preview'}</li>
                <li><strong>Temperature:</strong> {config.ai_models?.temperature || 0.7}</li>
                <li><strong>Max Tokens:</strong> {config.ai_models?.max_tokens || 2000}</li>
              </ul>
            </div>

            <div className="config-card">
              <h4>Trending Algorithm</h4>
              <ul className="config-list">
                <li><strong>Threshold:</strong> {config.trending?.trending_threshold || 70}</li>
                <li><strong>Mention Weight:</strong> {config.trending?.mention_weight || 0.5}</li>
                <li><strong>GitHub Weight:</strong> {config.trending?.github_weight || 0.3}</li>
                <li><strong>Window:</strong> {config.trending?.trend_window_days || 30} days</li>
              </ul>
            </div>

            <div className="config-card">
              <h4>Agents</h4>
              <ul className="config-list">
                <li><strong>Content Scraper:</strong> {config.agents?.content_scraper?.enabled !== false ? '✅' : '❌'}</li>
                <li><strong>Trend Analyzer:</strong> {config.agents?.trend_analyzer?.enabled !== false ? '✅' : '❌'}</li>
                <li><strong>Max Results:</strong> {config.agents?.content_scraper?.max_search_results || 10}</li>
              </ul>
            </div>

            <div className="config-card">
              <h4>RAG Workflow</h4>
              <ul className="config-list">
                <li><strong>Reasoning:</strong> {config.rag_workflow?.enable_reasoning !== false ? '✅' : '❌'}</li>
                <li><strong>Refinement:</strong> {config.rag_workflow?.enable_refinement !== false ? '✅' : '❌'}</li>
                <li><strong>Confidence:</strong> {config.rag_workflow?.confidence_threshold || 0.7}</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Audit Log */}
      <div className="section">
        <h2 className="section-title">
          <FiActivity style={{ marginRight: '0.5rem', display: 'inline' }} />
          Recent Configuration Changes
        </h2>

        {auditLog.length > 0 ? (
          <div className="table-container">
            <table className="audit-log-table">
              <thead>
                <tr>
                  <th>Setting</th>
                  <th>Category</th>
                  <th>Old Value</th>
                  <th>New Value</th>
                  <th>Changed By</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {auditLog.map((entry, idx) => (
                  <tr key={idx}>
                    <td>{entry.setting_key}</td>
                    <td>{entry.category}</td>
                    <td>{JSON.stringify(entry.old_value || {}).slice(0, 30)}...</td>
                    <td>{JSON.stringify(entry.new_value || {}).slice(0, 30)}...</td>
                    <td>{entry.changed_by || 'System'}</td>
                    <td>{new Date(entry.changed_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
            No configuration changes logged yet
          </p>
        )}
      </div>

      {/* Agent Access Control */}
      <div className="section" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '2rem', borderRadius: '12px', marginBottom: '2rem' }}>
        <h2 className="section-title" style={{ color: 'white', marginBottom: '1rem' }}>
          <FiShield style={{ marginRight: '0.5rem', display: 'inline' }} />
          Agent Access Control System
        </h2>
        <p style={{ color: 'rgba(255,255,255,0.9)', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
          Manage agent permissions, platform access, rate limits, and security policies. Control which agents can access which platforms and under what conditions.
        </p>
        <div style={{ background: 'white', borderRadius: '12px', padding: '1.5rem' }}>
          <AgentAccessControl />
        </div>
      </div>

      {/* System Information */}
      <div className="section">
        <h2 className="section-title">
          <FiServer style={{ marginRight: '0.5rem', display: 'inline' }} />
          System Information
        </h2>

        <div className="info-grid">
          <div className="info-item">
            <strong>Backend API:</strong>
            <span>{window.location.origin}/api</span>
          </div>
          <div className="info-item">
            <strong>Health Endpoint:</strong>
            <span>{window.location.origin}/api/admin/health</span>
          </div>
          <div className="info-item">
            <strong>Settings Endpoint:</strong>
            <span>{window.location.origin}/api/admin/settings</span>
          </div>
          <div className="info-item">
            <strong>Access Control Endpoint:</strong>
            <span>{window.location.origin}/api/admin/agent-access</span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Loading admin data...</p>
        </div>
      )}
    </div>
  );
}

export default Admin;

