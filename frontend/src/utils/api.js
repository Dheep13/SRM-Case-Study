// API configuration
// Use environment variable if available (for Cloud Foundry), otherwise default to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
                     (typeof window !== 'undefined' && window.ENV?.API_BASE_URL) || 
                     'http://localhost:8000';

console.log('🔧 API Configuration:', {
  'import.meta.env.VITE_API_BASE_URL': import.meta.env.VITE_API_BASE_URL,
  'window.ENV': typeof window !== 'undefined' ? window.ENV : 'N/A',
  'Final API_BASE_URL': API_BASE_URL
});

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
  
  // Tech News
  techNews: (query = 'AI technology artificial intelligence', limit = 10, daysBack = 7) => 
    fetch(`${API_BASE_URL}/api/tech-news?query=${encodeURIComponent(query)}&limit=${limit}&days_back=${daysBack}`),
  
  // Skill Forecast
  skillForecast: (maxSkills = 10) => 
    fetch(`${API_BASE_URL}/api/skill-forecast?max_skills=${maxSkills}`),
  
  // Trending Skills
  trendingSkills: (maxSkills = 10, daysBack = 30) => 
    fetch(`${API_BASE_URL}/api/trending-skills?max_skills=${maxSkills}&days_back=${daysBack}`),

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
    auditLog: (limit = 20) => fetch(`${API_BASE_URL}/api/admin/audit-log?limit=${limit}`),
    
    // Agent Access Control
    agentAccess: {
      get: () => fetch(`${API_BASE_URL}/api/admin/agent-access`),
      update: (data) => fetch(`${API_BASE_URL}/api/admin/agent-access`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }),
      audit: (limit = 100) => fetch(`${API_BASE_URL}/api/admin/agent-access/audit?limit=${limit}`),
      test: (data) => fetch(`${API_BASE_URL}/api/admin/agent-access/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
    }
  }
};

export default api;
