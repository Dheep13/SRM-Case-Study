import React, { useState } from 'react';
import { FiX, FiPlus } from 'react-icons/fi';

function AddPlatformModal({ isOpen, onClose, onAdd, existingPlatforms }) {
  const [formData, setFormData] = useState({
    key: '',
    name: '',
    domain: '',
    access_level: 'restricted',
    rate_limit: 100,
    api_endpoints: [''],
    allowed_content_types: [],
    blocked_keywords: []
  });

  const [contentTypeInput, setContentTypeInput] = useState('');
  const [keywordInput, setKeywordInput] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!formData.key) {
      setError('Platform key is required');
      return;
    }

    if (existingPlatforms.includes(formData.key)) {
      setError(`Platform "${formData.key}" already exists!`);
      return;
    }

    if (!formData.name) {
      setError('Platform name is required');
      return;
    }

    if (!formData.domain) {
      setError('Domain is required');
      return;
    }

    // Filter out empty endpoints
    const cleanedEndpoints = formData.api_endpoints.filter(e => e.trim() !== '');
    
    if (cleanedEndpoints.length === 0) {
      setError('At least one API endpoint is required');
      return;
    }

    // Create platform config
    const platformConfig = {
      name: formData.name,
      domain: formData.domain,
      access_level: formData.access_level,
      api_endpoints: cleanedEndpoints,
      rate_limit: parseInt(formData.rate_limit),
      allowed_content_types: formData.allowed_content_types,
      blocked_keywords: formData.blocked_keywords
    };

    onAdd(formData.key, platformConfig);
    handleClose();
  };

  const handleClose = () => {
    setFormData({
      key: '',
      name: '',
      domain: '',
      access_level: 'restricted',
      rate_limit: 100,
      api_endpoints: [''],
      allowed_content_types: [],
      blocked_keywords: []
    });
    setContentTypeInput('');
    setKeywordInput('');
    setError('');
    onClose();
  };

  const addEndpoint = () => {
    setFormData(prev => ({
      ...prev,
      api_endpoints: [...prev.api_endpoints, '']
    }));
  };

  const updateEndpoint = (index, value) => {
    const newEndpoints = [...formData.api_endpoints];
    newEndpoints[index] = value;
    setFormData(prev => ({ ...prev, api_endpoints: newEndpoints }));
  };

  const removeEndpoint = (index) => {
    setFormData(prev => ({
      ...prev,
      api_endpoints: prev.api_endpoints.filter((_, i) => i !== index)
    }));
  };

  const addContentType = () => {
    if (contentTypeInput.trim() && !formData.allowed_content_types.includes(contentTypeInput.trim())) {
      setFormData(prev => ({
        ...prev,
        allowed_content_types: [...prev.allowed_content_types, contentTypeInput.trim()]
      }));
      setContentTypeInput('');
    }
  };

  const removeContentType = (type) => {
    setFormData(prev => ({
      ...prev,
      allowed_content_types: prev.allowed_content_types.filter(t => t !== type)
    }));
  };

  const addKeyword = () => {
    if (keywordInput.trim() && !formData.blocked_keywords.includes(keywordInput.trim())) {
      setFormData(prev => ({
        ...prev,
        blocked_keywords: [...prev.blocked_keywords, keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const removeKeyword = (keyword) => {
    setFormData(prev => ({
      ...prev,
      blocked_keywords: prev.blocked_keywords.filter(k => k !== keyword)
    }));
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'white',
        borderRadius: '16px',
        width: '90%',
        maxWidth: '700px',
        maxHeight: '90vh',
        overflow: 'hidden',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      }}>
        {/* Header */}
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid #e5e7eb',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white'
        }}>
          <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '600' }}>
            Add New Platform
          </h2>
          <button
            onClick={handleClose}
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              border: 'none',
              borderRadius: '8px',
              padding: '0.5rem',
              cursor: 'pointer',
              color: 'white',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <FiX size={24} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ padding: '1.5rem', overflowY: 'auto', maxHeight: 'calc(90vh - 140px)' }}>
          {error && (
            <div style={{
              padding: '1rem',
              background: '#fee2e2',
              color: '#991b1b',
              borderRadius: '8px',
              marginBottom: '1rem',
              fontWeight: '500'
            }}>
              {error}
            </div>
          )}

          {/* Basic Info */}
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>
              Basic Information
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                  Platform Key * <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>(lowercase, no spaces)</span>
                </label>
                <input
                  type="text"
                  value={formData.key}
                  onChange={(e) => setFormData(prev => ({ ...prev, key: e.target.value.toLowerCase().replace(/\s/g, '_') }))}
                  placeholder="e.g., github, openai"
                  required
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    fontSize: '1rem'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                  Display Name *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="e.g., GitHub, OpenAI"
                  required
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    fontSize: '1rem'
                  }}
                />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                  Domain *
                </label>
                <input
                  type="text"
                  value={formData.domain}
                  onChange={(e) => setFormData(prev => ({ ...prev, domain: e.target.value }))}
                  placeholder="e.g., api.github.com"
                  required
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    fontSize: '1rem'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                  Access Level
                </label>
                <select
                  value={formData.access_level}
                  onChange={(e) => setFormData(prev => ({ ...prev, access_level: e.target.value }))}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    fontSize: '1rem',
                    cursor: 'pointer'
                  }}
                >
                  <option value="allowed">Allowed</option>
                  <option value="restricted">Restricted</option>
                  <option value="blocked">Blocked</option>
                </select>
              </div>
            </div>
          </div>

          {/* API Endpoints */}
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937', margin: 0 }}>
                API Endpoints *
              </h3>
              <button
                type="button"
                onClick={addEndpoint}
                style={{
                  padding: '0.5rem 1rem',
                  background: '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '0.875rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.25rem'
                }}
              >
                <FiPlus /> Add Endpoint
              </button>
            </div>
            {formData.api_endpoints.map((endpoint, idx) => (
              <div key={idx} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <input
                  type="url"
                  value={endpoint}
                  onChange={(e) => updateEndpoint(idx, e.target.value)}
                  placeholder="https://api.example.com/v1/search"
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #d1d5db',
                    fontSize: '1rem'
                  }}
                />
                {formData.api_endpoints.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeEndpoint(idx)}
                    style={{
                      padding: '0.75rem',
                      background: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      cursor: 'pointer'
                    }}
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Settings */}
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937', marginBottom: '1rem' }}>
              Settings
            </h3>
            
            <div>
              <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
                Rate Limit (requests/hour)
              </label>
              <input
                type="number"
                value={formData.rate_limit}
                onChange={(e) => setFormData(prev => ({ ...prev, rate_limit: e.target.value }))}
                min="0"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #d1d5db',
                  fontSize: '1rem'
                }}
              />
            </div>
          </div>

          {/* Content Types */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
              Allowed Content Types
            </label>
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <input
                type="text"
                value={contentTypeInput}
                onChange={(e) => setContentTypeInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addContentType())}
                placeholder="e.g., web, courses, documentation"
                style={{
                  flex: 1,
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #d1d5db',
                  fontSize: '1rem'
                }}
              />
              <button
                type="button"
                onClick={addContentType}
                style={{
                  padding: '0.75rem 1rem',
                  background: '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer'
                }}
              >
                Add
              </button>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {formData.allowed_content_types.map((type, idx) => (
                <span key={idx} style={{
                  padding: '0.5rem 1rem',
                  background: '#dbeafe',
                  color: '#1e40af',
                  borderRadius: '999px',
                  fontSize: '0.875rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  {type}
                  <button
                    type="button"
                    onClick={() => removeContentType(type)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#1e40af',
                      cursor: 'pointer',
                      padding: 0,
                      fontSize: '1.25rem',
                      lineHeight: 1
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Blocked Keywords */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
              Blocked Keywords (optional)
            </label>
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <input
                type="text"
                value={keywordInput}
                onChange={(e) => setKeywordInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                placeholder="e.g., private, confidential"
                style={{
                  flex: 1,
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #d1d5db',
                  fontSize: '1rem'
                }}
              />
              <button
                type="button"
                onClick={addKeyword}
                style={{
                  padding: '0.75rem 1rem',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer'
                }}
              >
                Add
              </button>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {formData.blocked_keywords.map((keyword, idx) => (
                <span key={idx} style={{
                  padding: '0.5rem 1rem',
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
                    type="button"
                    onClick={() => removeKeyword(keyword)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#991b1b',
                      cursor: 'pointer',
                      padding: 0,
                      fontSize: '1.25rem',
                      lineHeight: 1
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', paddingTop: '1rem', borderTop: '1px solid #e5e7eb' }}>
            <button
              type="button"
              onClick={handleClose}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#f3f4f6',
                color: '#374151',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '500'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              style={{
                padding: '0.75rem 1.5rem',
                background: '#10b981',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '500'
              }}
            >
              Add Platform
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddPlatformModal;

