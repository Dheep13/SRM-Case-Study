import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiMessageSquare, FiSearch, FiBarChart2, FiCheckCircle, FiAlertCircle, FiArrowRight, FiBook, FiZap } from 'react-icons/fi';
import { IoSparklesSharp } from 'react-icons/io5';

function Home() {
  const [health, setHealth] = useState(null);
  const [stats, setStats] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check API health
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(() => setHealth({ status: 'offline' }));

    // Get analytics stats
    fetch('/api/analytics')
      .then(res => res.json())
      .then(data => setStats(data.stats))
      .catch(err => console.log('Stats not available'));
  }, []);

  return (
    <div className="page">
      {/* Status Indicator - Top Right */}
      <div className={`status-dot-indicator ${health?.status === 'healthy' ? 'online' : 'offline'}`} 
           title={health?.status === 'healthy' ? 'System Online' : 'Connecting...'}>
      </div>

      <div className="page-header">
        <h1 className="page-title gradient-text">Welcome to Your AI Learning Assistant</h1>
        <p className="page-subtitle">Powered by Agentic RAG, AI Agents, and Real-Time Data</p>
      </div>

      {/* Feature Cards */}
      <div className="feature-grid">
        <div className="feature-card gradient-purple" onClick={() => navigate('/chat')}>
          <FiMessageSquare className="feature-icon" />
          <h3>Chat Assistant</h3>
          <p>Get personalized advice from our Agentic RAG chatbot with multi-step reasoning</p>
          <button className="feature-btn">
            Start Chatting <FiArrowRight style={{ marginLeft: '0.5rem' }} />
          </button>
        </div>

        <div className="feature-card gradient-pink" onClick={() => navigate('/discover')}>
          <FiSearch className="feature-icon" />
          <h3>Discover Resources</h3>
          <p>AI agents search the web for the latest learning materials and trends</p>
          <button className="feature-btn">
            Discover Now <FiArrowRight style={{ marginLeft: '0.5rem' }} />
          </button>
        </div>

        <div className="feature-card gradient-blue" onClick={() => navigate('/analytics')}>
          <FiBarChart2 className="feature-icon" />
          <h3>Skill Analytics</h3>
          <p>Explore trending skills, demand scores, and personalized roadmaps</p>
          <button className="feature-btn">
            View Analytics <FiArrowRight style={{ marginLeft: '0.5rem' }} />
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      {stats && (
        <div className="stats-section">
          <h2 className="section-title">
            <FiBarChart2 style={{ marginRight: '0.5rem', display: 'inline' }} />
            Quick Statistics
          </h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{stats.total_resources || 0}</div>
              <div className="stat-label">Learning Resources</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.total_skills || 0}</div>
              <div className="stat-label">IT Skills Tracked</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.avg_demand?.toFixed(1) || 0}</div>
              <div className="stat-label">Avg Demand Score</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{Object.keys(stats.categories || {}).length}</div>
              <div className="stat-label">Categories</div>
            </div>
          </div>
        </div>
      )}

      {/* What Makes This Special */}
      <div className="info-section">
        <h2 className="section-title">
          <IoSparklesSharp style={{ marginRight: '0.5rem', display: 'inline' }} />
          What Makes This Agentic?
        </h2>
        <div className="process-flow">
          <div className="process-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h4>Analyze Intent</h4>
              <p>LLM understands what you're asking</p>
            </div>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h4>Plan Search</h4>
              <p>Decides what to search for</p>
            </div>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h4>Retrieve Data</h4>
              <p>Semantic search with embeddings</p>
            </div>
          </div>
          <div className="process-arrow">→</div>
          <div className="process-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h4>Reason & Refine</h4>
              <p>Multi-step reasoning and quality check</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <a href="/docs" target="_blank" rel="noopener noreferrer" className="action-btn">
          <FiBook style={{ marginRight: '0.5rem' }} />
          API Documentation
        </a>
        <button className="action-btn" onClick={() => navigate('/chat')}>
          <FiZap style={{ marginRight: '0.5rem' }} />
          Try Sample Query
        </button>
      </div>
    </div>
  );
}

export default Home;

