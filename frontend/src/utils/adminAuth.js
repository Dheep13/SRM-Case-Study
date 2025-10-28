// Simple admin authentication utility
// For production, this should be replaced with proper authentication

const ADMIN_PASSWORD = 'admin123'; // In production, use environment variable

export const isAdmin = () => {
  return localStorage.getItem('isAdmin') === 'true';
};

export const loginAsAdmin = (password) => {
  if (password === ADMIN_PASSWORD) {
    localStorage.setItem('isAdmin', 'true');
    return true;
  }
  return false;
};

export const logoutAdmin = () => {
  localStorage.removeItem('isAdmin');
};

export const toggleAdmin = () => {
  // For development: quick toggle (should prompt for password in production)
  const currentState = isAdmin();
  localStorage.setItem('isAdmin', !currentState);
  return !currentState;
};

// Prompt for admin password
export const promptAdminLogin = () => {
  const password = prompt('Enter admin password:');
  if (password) {
    return loginAsAdmin(password);
  }
  return false;
};

