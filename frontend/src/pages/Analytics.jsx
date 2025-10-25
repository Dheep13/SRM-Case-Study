import React, { useState } from 'react';
import { FiTarget, FiTrendingUp, FiAward, FiPackage, FiRefreshCw } from 'react-icons/fi';

function Analytics({ studentLevel }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('All Categories');
  const [lastRefresh, setLastRefresh] = useState(null);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/analytics?student_level=${studentLevel}`);
      const data = await response.json();
      setAnalytics(data);
      setLastRefresh(new Date());
    } catch (error) {
      console.error('Error loading analytics:', error);
      alert('Failed to load analytics. Please try again.');
    }
    setLoading(false);
  };

  const formatLastRefresh = () => {
    if (!lastRefresh) return null;
    const now = new Date();
    const diff = Math.floor((now - lastRefresh) / 1000); // seconds
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
    return lastRefresh.toLocaleString();
  };

  return (
    <div className="page">
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
          <div>
            <h1 className="page-title">
              <FiAward style={{ marginRight: '0.5rem', display: 'inline' }} />
              Skill Analytics
            </h1>
            <p className="page-subtitle">
              Personalized insights for {studentLevel} students
              {lastRefresh && (
                <span style={{ marginLeft: '1rem', fontSize: '0.9rem', color: '#64748b' }}>
                  • Last updated: {formatLastRefresh()}
                </span>
              )}
            </p>
          </div>
          <button 
            className="refresh-btn"
            onClick={loadAnalytics}
            disabled={loading}
            title="Refresh analytics data"
          >
            <FiRefreshCw className={loading ? 'spinning' : ''} />
            {loading ? 'Refreshing...' : 'Refresh Data'}
          </button>
        </div>
      </div>

      {/* Empty State */}
      {!analytics && !loading && (
        <div className="empty-state">
          <FiAward className="empty-icon" style={{ fontSize: '4rem', opacity: 0.3 }} />
          <h3>No Analytics Data Yet</h3>
          <p>Click the "Refresh Data" button above to load the latest skill analytics and trends.</p>
        </div>
      )}

      {/* Quick Stats */}
      {analytics?.stats && (
        <div className="stats-grid">
          <div className="stat-card gradient-purple">
            <div className="stat-value">{analytics.stats.total_resources}</div>
            <div className="stat-label">Learning Resources</div>
          </div>
          <div className="stat-card gradient-pink">
            <div className="stat-value">{analytics.stats.total_skills}</div>
            <div className="stat-label">IT Skills</div>
          </div>
          <div className="stat-card gradient-blue">
            <div className="stat-value">{analytics.stats.avg_demand.toFixed(1)}</div>
            <div className="stat-label">Avg Demand Score</div>
          </div>
          <div className="stat-card gradient-green">
            <div className="stat-value">{Object.keys(analytics.stats.categories).length}</div>
            <div className="stat-label">Categories</div>
          </div>
        </div>
      )}

      {/* Recommended Skills */}
      {analytics?.recommendations && analytics.recommendations.length > 0 && (
        <div className="section">
          <h2 className="section-title">
            <FiTarget style={{ marginRight: '0.5rem', display: 'inline' }} />
            Recommended for You
          </h2>
          <div className="skills-grid">
            {analytics.recommendations.map((skill, idx) => (
              <div key={idx} className="skill-card recommended">
                <div className="skill-rank">#{idx + 1}</div>
                <h3 className="skill-name">{skill.skill_name}</h3>
                <div className="skill-category">{skill.category}</div>
                <div className="skill-demand">
                  <div className="demand-bar">
                    <div 
                      className="demand-fill"
                      style={{ width: `${skill.demand_score}%` }}
                    ></div>
                  </div>
                  <span className="demand-score">{skill.demand_score}/100</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* All Skills */}
      {analytics?.all_skills && (
        <div className="section">
          <div className="section-header">
            <h2 className="section-title">
              <FiTrendingUp style={{ marginRight: '0.5rem', display: 'inline' }} />
              All Skills
            </h2>
            <select 
              className="filter-select"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option>All Categories</option>
              <option>AI/ML</option>
              <option>Programming</option>
              <option>DevOps</option>
              <option>Database</option>
              <option>Cloud</option>
              <option>Web Development</option>
            </select>
          </div>

          <div className="skills-table">
            <div className="table-header">
              <div>Rank</div>
              <div>Skill</div>
              <div>Category</div>
              <div>Demand</div>
            </div>
            {analytics.all_skills
              .filter(skill => filter === 'All Categories' || skill.category === filter)
              .map((skill, idx) => (
                <div key={idx} className="table-row">
                  <div className="table-cell">#{idx + 1}</div>
                  <div className="table-cell skill-cell">
                    <strong>{skill.skill_name}</strong>
                  </div>
                  <div className="table-cell">
                    <span className="category-badge">{skill.category}</span>
                  </div>
                  <div className="table-cell">
                    <div className="mini-demand-bar">
                      <div 
                        className="mini-demand-fill"
                        style={{ width: `${skill.demand_score}%` }}
                      ></div>
                    </div>
                    <span>{skill.demand_score}</span>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Category Distribution */}
      {analytics?.stats?.categories && (
        <div className="section">
          <h2 className="section-title">
            <FiPackage style={{ marginRight: '0.5rem', display: 'inline' }} />
            Category Distribution
          </h2>
          <div className="category-grid">
            {Object.entries(analytics.stats.categories).map(([category, count]) => (
              <div key={category} className="category-card">
                <div className="category-count">{count}</div>
                <div className="category-name">{category}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Analytics;

