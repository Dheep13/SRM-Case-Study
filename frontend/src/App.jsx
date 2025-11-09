import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { FiHome, FiMessageSquare, FiSearch, FiBarChart2, FiMenu, FiSettings, FiBookOpen, FiCalendar, FiUser, FiLogOut } from 'react-icons/fi';
import { IoSparklesSharp } from 'react-icons/io5';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Discover from './pages/Discover';
import Analytics from './pages/Analytics';
import Admin from './pages/Admin';
import Assignments from './pages/Assignments';
import TodaysClass from './pages/TodaysClass';
import ExpertConsultation from './pages/ExpertConsultation';
import Login from './pages/Login';
import SettingsModal from './components/SettingsModal';
import ProtectedRoute from './components/ProtectedRoute';
import { isAdmin as checkAdmin, toggleAdmin } from './utils/adminAuth';
import { isAuthenticated, getCurrentUser, verifyToken, logout as authLogout } from './utils/auth';
import './App.css';

function App() {
  // ALL HOOKS MUST BE CALLED FIRST - BEFORE ANY CONDITIONAL RETURNS
  const [authenticated, setAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);
  const [studentLevel, setStudentLevel] = useState('Junior');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isAdmin, setIsAdminState] = useState(checkAdmin());
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);
  const [health, setHealth] = useState(null);
  const [logoClickCount, setLogoClickCount] = useState(0);

  // Get API base URL from environment
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ||
                       (typeof window !== 'undefined' && window.ENV?.API_BASE_URL) ||
                       'http://localhost:8000';

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (isAuthenticated()) {
        const user = getCurrentUser();
        if (user) {
          setCurrentUser(user);
          setStudentLevel(user.student_level || 'Junior');
        }
        
        // Verify token with backend
        const valid = await verifyToken();
        setAuthenticated(valid);
        if (!valid) {
          setCurrentUser(null);
        }
      }
      setCheckingAuth(false);
    };
    
    checkAuth();
  }, []);

  // Fetch health status
  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        setHealth(data);
      } catch (error) {
        setHealth({ status: 'offline' });
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [API_BASE_URL]);

  // Update user state when authenticated changes
  useEffect(() => {
    if (authenticated) {
      const user = getCurrentUser();
      if (user) {
        setCurrentUser(user);
        setStudentLevel(user.student_level || 'Junior');
      }
    } else {
      setCurrentUser(null);
    }
  }, [authenticated]);

  // Event handlers
  const handleLogoClick = () => {
    if (logoClickCount === 0) {
      setTimeout(() => setLogoClickCount(0), 3000);
    }
    setLogoClickCount(prev => prev + 1);
    
    // Double click within 3 seconds enables admin mode
    if (logoClickCount >= 1) {
      const newState = toggleAdmin();
      setIsAdminState(newState);
      setLogoClickCount(0);
      if (newState) {
        alert('Admin mode enabled! Click logo twice again to disable.');
      }
    }
  };

  const toggleSidebar = () => {
    console.log('Toggling sidebar from', sidebarOpen, 'to', !sidebarOpen);
    setSidebarOpen(!sidebarOpen);
  };

  const handleLogout = async () => {
    await authLogout();
    setAuthenticated(false);
    setCurrentUser(null);
    window.location.href = '/login';
  };

  // Show loading while checking auth (AFTER all hooks)
  if (checkingAuth) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{ color: 'white', fontSize: '1.5rem' }}>Loading...</div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={authenticated ? <Navigate to="/" replace /> : <Login onLogin={() => setAuthenticated(true)} />} 
        />
        <Route 
          path="/*" 
          element={
            <ProtectedRoute>
              <div className="app">
        {/* Top Navigation */}
        <nav className="navbar">
          <div className="navbar-content">
            <div className="navbar-left">
              <button className="menu-btn" onClick={toggleSidebar} type="button">
                <FiMenu />
              </button>
              <div className="logo" onClick={handleLogoClick} style={{ cursor: 'pointer' }} title="Double-click for admin mode">
                <IoSparklesSharp className="logo-icon" />
                <div className="logo-text">
                  <div className="logo-main">EvolveIQ</div>
                  <div className="logo-subtitle">An AI Driven MultiAgent Framework for Real Time Educational Content Generation and Industry Trend Analysis</div>
                </div>
              </div>
            </div>
            <div className="navbar-right" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              {/* Status Indicator */}
              <div className={`status-dot-indicator ${health?.status === 'healthy' ? 'online' : 'offline'}`} 
                   title={health?.status === 'healthy' ? 'System Online' : 'Connecting...'}>
              </div>
              
              {currentUser && (
                <span style={{ color: '#6b7280', fontSize: '0.9rem', marginRight: '10px' }}>
                  {currentUser.full_name || currentUser.username}
                </span>
              )}
              
              <select 
                className="level-select"
                value={studentLevel}
                onChange={(e) => setStudentLevel(e.target.value)}
              >
                <option>Freshman</option>
                <option>Sophomore</option>
                <option>Junior</option>
                <option>Senior</option>
                <option>Graduate</option>
              </select>
              
              <button
                onClick={handleLogout}
                title="Logout"
                style={{
                  padding: '8px 16px',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <FiLogOut /> Logout
              </button>
              
              {!isAdmin && (
                <button 
                  className="admin-toggle-btn"
                  onClick={() => {
                    const newState = toggleAdmin();
                    setIsAdminState(newState);
                    alert('Admin mode ' + (newState ? 'ENABLED' : 'DISABLED') + '!');
                  }}
                  title="Enable Admin Mode"
                  style={{
                    padding: '8px 16px',
                    background: '#6366f1',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '12px',
                    marginLeft: '10px'
                  }}
                >
                  Admin
                </button>
              )}
              
              {isAdmin && (
                <>
                  <button 
                    className="settings-btn"
                    onClick={() => setSettingsModalOpen(true)}
                    title="Admin Settings"
                  >
                    <FiSettings />
                  </button>
                  <button 
                    className="admin-toggle-btn"
                    onClick={() => {
                      const newState = toggleAdmin();
                      setIsAdminState(newState);
                      alert('Admin mode DISABLED');
                    }}
                    title="Disable Admin Mode"
                    style={{
                      padding: '6px 12px',
                      background: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '11px',
                      marginLeft: '20px'
                    }}
                  >
                    Exit Admin
                  </button>
                </>
              )}
            </div>
          </div>
        </nav>

        <div className="main-container">
          {/* Sidebar */}
          <aside className={`sidebar ${!sidebarOpen ? 'closed' : ''}`} data-open={sidebarOpen}>
            <div className="sidebar-content">
              <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiHome className="nav-icon" />
                <span className="nav-text">Home</span>
              </NavLink>
              <NavLink to="/chat" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiMessageSquare className="nav-icon" />
                <span className="nav-text">Chat Assistant</span>
              </NavLink>
              <NavLink to="/discover" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiSearch className="nav-icon" />
                <span className="nav-text">Discover Resources</span>
              </NavLink>
              <NavLink to="/analytics" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiBarChart2 className="nav-icon" />
                <span className="nav-text">Analytics</span>
              </NavLink>
              
              {/* Expert Consultation */}
              <NavLink to="/expert-consultation" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiUser className="nav-icon" />
                <span className="nav-text">Expert Consultation</span>
              </NavLink>
              
              {/* Teacher/Professor Functionality */}
              <div className="nav-section-divider" style={{ margin: '1rem 0', padding: '0 1rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontWeight: '600', textTransform: 'uppercase' }}>Teaching Tools</span>
              </div>
              
              <NavLink to="/assignments" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiBookOpen className="nav-icon" />
                <span className="nav-text">Assignments</span>
              </NavLink>
              <NavLink to="/todays-class" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <FiCalendar className="nav-icon" />
                <span className="nav-text">Today's Class</span>
              </NavLink>
              
              {isAdmin && (
                <div className="nav-section-divider" style={{ margin: '1rem 0', padding: '0 1rem' }}>
                  <span style={{ fontSize: '0.75rem', color: '#9ca3af', fontWeight: '600', textTransform: 'uppercase' }}>Administration</span>
                </div>
              )}
              {isAdmin && (
                <NavLink to="/admin" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                  <FiSettings className="nav-icon" />
                  <span className="nav-text">Admin</span>
                </NavLink>
              )}
            </div>
          </aside>

          {/* Main Content */}
          <main className={`content ${!sidebarOpen ? 'full' : ''}`}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<Chat studentLevel={studentLevel} />} />
              <Route path="/discover" element={<Discover />} />
              <Route path="/analytics" element={<Analytics studentLevel={studentLevel} />} />
              <Route path="/expert-consultation" element={<ExpertConsultation />} />
              <Route path="/assignments" element={<Assignments />} />
              <Route path="/todays-class" element={<TodaysClass />} />
              {isAdmin && <Route path="/admin" element={<Admin />} />}
            </Routes>
          </main>
        </div>

        {/* Settings Modal */}
        <SettingsModal 
          isOpen={settingsModalOpen}
          onClose={() => setSettingsModalOpen(false)}
          onSave={() => {
            // Settings saved, can reload if needed
          }}
        />
      </div>
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
