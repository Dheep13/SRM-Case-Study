// API configuration
const API_BASE_URL = 'http://localhost:8000';

export const api = {
  // Discovery
  discover: (data) => fetch(`${API_BASE_URL}/api/discover`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }),

  // Chat
  chat: (data) => fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }),

  // Health
  health: () => fetch(`${API_BASE_URL}/api/health`),

  // Analytics
  analytics: () => fetch(`${API_BASE_URL}/api/analytics`),

  // Admin endpoints
  admin: {
    health: () => fetch(`${API_BASE_URL}/api/admin/health`),
    settings: () => fetch(`${API_BASE_URL}/api/admin/settings`),
    updateSettings: (data) => fetch(`${API_BASE_URL}/api/admin/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
    resetSettings: () => fetch(`${API_BASE_URL}/api/admin/settings/reset`, {
      method: 'POST'
    }),
    auditLog: (limit = 20) => fetch(`${API_BASE_URL}/api/admin/audit-log?limit=${limit}`)
  }
};

export default api;
