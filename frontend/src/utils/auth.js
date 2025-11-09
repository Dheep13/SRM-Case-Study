// Authentication utilities

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
                     (typeof window !== 'undefined' && window.ENV?.API_BASE_URL) || 
                     'http://localhost:8000';

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  const token = localStorage.getItem('auth_token');
  return !!token;
};

/**
 * Get current user from localStorage
 */
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
};

/**
 * Get auth token
 */
export const getAuthToken = () => {
  return localStorage.getItem('auth_token');
};

/**
 * Verify token with backend
 */
export const verifyToken = async () => {
  const token = getAuthToken();
  if (!token) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    });

    const data = await response.json();
    
    if (data.valid && data.user) {
      // Update user info
      localStorage.setItem('user', JSON.stringify(data.user));
      return true;
    } else {
      // Token invalid, clear storage (but don't call logout to avoid recursion)
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      return false;
    }
  } catch (error) {
    console.error('Token verification error:', error);
    // On error, don't clear storage - might be network issue
    return false;
  }
};

/**
 * Logout user
 */
export const logout = async () => {
  const token = getAuthToken();
  
  if (token) {
    try {
      await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
  
  // Always clear local storage even if API call fails
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user');
};

/**
 * Set authentication data
 */
export const setAuth = (token, user) => {
  localStorage.setItem('auth_token', token);
  localStorage.setItem('user', JSON.stringify(user));
};

