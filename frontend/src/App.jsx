import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { FiHome, FiMessageSquare, FiSearch, FiBarChart2, FiMenu } from 'react-icons/fi';
import { IoSparklesSharp } from 'react-icons/io5';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Discover from './pages/Discover';
import Analytics from './pages/Analytics';
import './App.css';

function App() {
  const [studentLevel, setStudentLevel] = useState('Junior');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    console.log('Toggling sidebar from', sidebarOpen, 'to', !sidebarOpen);
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Router>
      <div className="app">
        {/* Top Navigation */}
        <nav className="navbar">
          <div className="navbar-content">
            <div className="navbar-left">
              <button className="menu-btn" onClick={toggleSidebar} type="button">
                <FiMenu />
              </button>
              <h1 className="logo">
                <IoSparklesSharp className="logo-icon" />
                GenAI Learning Assistant
              </h1>
            </div>
            <div className="navbar-right">
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
            </div>
          </aside>

          {/* Main Content */}
          <main className={`content ${!sidebarOpen ? 'full' : ''}`}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<Chat studentLevel={studentLevel} />} />
              <Route path="/discover" element={<Discover />} />
              <Route path="/analytics" element={<Analytics studentLevel={studentLevel} />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
