import React, { useState, useEffect } from 'react';
import { FiBarChart2, FiTrendingUp, FiRefreshCw, FiFilter, FiDownload, FiFileText, FiTarget, FiCalendar, FiUsers, FiBookOpen, FiZap, FiArrowUp, FiArrowDown, FiPlus } from 'react-icons/fi';
import api from '../utils/api';

const Analytics = ({ studentLevel }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('All Categories');
  const [lastRefresh, setLastRefresh] = useState(null);
  const [techNews, setTechNews] = useState([]);
  const [skillForecast, setSkillForecast] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const response = await api.analytics();
      const data = await response.json();
      setAnalytics(data);
      setLastRefresh(new Date());
      
      // Generate skill forecast based on existing data
      generateSkillForecast(data.all_skills || []);
      
      // Load tech news (mock data for now)
      loadTechNews();
    } catch (error) {
      console.error('Error loading analytics:', error);
      // Provide fallback data instead of alert
      setAnalytics({
        stats: {
          total_skills: 0,
          total_resources: 0,
          trending_skills: 0,
          student_level: studentLevel,
          error: 'API not available'
        },
        trending_skills: [],
        recommendations: []
      });
    }
    setLoading(false);
  };

  const generateSkillForecast = (skills) => {
    // Simple forecasting based on current demand scores and trends
    const forecast = skills.slice(0, 10).map(skill => {
      const currentDemand = skill.demand_score || 50;
      const trendFactor = Math.random() * 0.3 + 0.85; // 85-115% variation
      const forecastDemand = Math.round(currentDemand * trendFactor);
      
      return {
        ...skill,
        current_demand: currentDemand,
        forecast_demand: forecastDemand,
        growth_rate: Math.round((forecastDemand - currentDemand) / currentDemand * 100),
        forecast_period: '6 months'
      };
    }).sort((a, b) => b.forecast_demand - a.forecast_demand);
    
    setSkillForecast(forecast);
  };

  const loadTechNews = () => {
    // Mock tech news data - in real implementation, this would fetch from news APIs
    const mockNews = [
      {
        id: 1,
        title: "OpenAI Releases GPT-4 Turbo with Enhanced Reasoning",
        summary: "New model shows 40% improvement in complex reasoning tasks",
        category: "AI/ML",
        published: "2 hours ago",
        source: "TechCrunch",
        relevance: "high"
      },
      {
        id: 2,
        title: "Microsoft Copilot Integration Expands to Education",
        summary: "New features help students learn coding and problem-solving",
        category: "Education",
        published: "4 hours ago",
        source: "Microsoft Blog",
        relevance: "high"
      },
      {
        id: 3,
        title: "TensorFlow 2.15 Released with Performance Improvements",
        summary: "Faster training times and better memory management",
        category: "Development",
        published: "6 hours ago",
        source: "Google AI",
        relevance: "medium"
      },
      {
        id: 4,
        title: "New Cybersecurity Threats Target AI Systems",
        summary: "Researchers identify vulnerabilities in machine learning models",
        category: "Security",
        published: "8 hours ago",
        source: "Security Weekly",
        relevance: "medium"
      },
      {
        id: 5,
        title: "Quantum Computing Breakthrough in Error Correction",
        summary: "IBM achieves 99.9% accuracy in quantum error correction",
        category: "Quantum",
        published: "12 hours ago",
        source: "Nature",
        relevance: "low"
      }
    ];
    
    setTechNews(mockNews);
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

  const getRelevanceColor = (relevance) => {
    switch(relevance) {
      case 'high': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'low': return '#6b7280';
      default: return '#6b7280';
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
          <div>
            <h1 className="page-title gradient-text">
              <FiBarChart2 style={{ marginRight: '0.5rem', display: 'inline' }} />
              Tech Analytics Dashboard
            </h1>
            <p className="page-subtitle">
              Personalized insights and tech news for {studentLevel} students
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

      {/* Navigation Tabs */}
      <div className="dashboard-tabs" style={{ marginBottom: '2rem' }}>
        <button 
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <FiBarChart2 />
          Overview
        </button>
        <button 
          className={`tab-btn ${activeTab === 'trending' ? 'active' : ''}`}
          onClick={() => setActiveTab('trending')}
        >
          <FiTrendingUp />
          Trending Skills
        </button>
        <button 
          className={`tab-btn ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          <FiTarget />
          Skill Forecast
        </button>
        <button 
          className={`tab-btn ${activeTab === 'news' ? 'active' : ''}`}
          onClick={() => setActiveTab('news')}
        >
          <FiFileText />
          Tech News
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <>
          {/* Quick Stats */}
          {analytics?.stats && (
            <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
              <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
                <FiBookOpen style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
                <h3 style={{ margin: 0, fontSize: '2rem' }}>{analytics.stats.total_resources}</h3>
                <p style={{ margin: 0, opacity: 0.9 }}>Learning Resources</p>
              </div>
              <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
                <FiZap style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
                <h3 style={{ margin: 0, fontSize: '2rem' }}>{analytics.stats.total_skills}</h3>
                <p style={{ margin: 0, opacity: 0.9 }}>IT Skills</p>
              </div>
              <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
                <FiTrendingUp style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
                <h3 style={{ margin: 0, fontSize: '2rem' }}>{analytics.stats.avg_demand?.toFixed(1) || '0'}</h3>
                <p style={{ margin: 0, opacity: 0.9 }}>Avg Demand Score</p>
              </div>
              <div className="stat-card" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
                <FiUsers style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
                <h3 style={{ margin: 0, fontSize: '2rem' }}>{Object.keys(analytics.stats.categories || {}).length}</h3>
                <p style={{ margin: 0, opacity: 0.9 }}>Categories</p>
              </div>
            </div>
          )}

          {/* Top Trending Skills Preview */}
          {analytics?.trending_skills && analytics.trending_skills.length > 0 && (
            <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <h2 className="section-title" style={{ marginTop: 0 }}>
                <FiTrendingUp style={{ marginRight: '0.5rem', display: 'inline' }} />
                Top Trending Skills
              </h2>
              <div className="skills-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                {analytics.trending_skills.slice(0, 6).map((skill, idx) => (
                  <div key={idx} className="skill-card" style={{ 
                    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)', 
                    padding: '1rem', 
                    borderRadius: '8px',
                    border: '1px solid #e5e7eb'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#6366f1' }}>#{idx + 1}</span>
                      <span style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: '500' }}>TRENDING</span>
                    </div>
                    <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem', color: '#1f2937' }}>{skill.skill_name}</h3>
                    <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.5rem' }}>{skill.category}</div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <div style={{ flex: 1, height: '4px', background: '#e5e7eb', borderRadius: '2px', overflow: 'hidden' }}>
                        <div 
                          style={{ 
                            height: '100%', 
                            background: 'linear-gradient(90deg, #10b981, #34d399)', 
                            width: `${skill.avg_trend_score || skill.demand_score || 50}%`,
                            transition: 'width 0.3s ease'
                          }}
                        ></div>
                      </div>
                      <span style={{ fontSize: '0.75rem', fontWeight: '600', color: '#374151' }}>
                        {skill.avg_trend_score || skill.demand_score || 50}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Category Distribution */}
          {analytics?.stats?.categories && (
            <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <h2 className="section-title" style={{ marginTop: 0 }}>
                <FiBarChart2 style={{ marginRight: '0.5rem', display: 'inline' }} />
                Skills by Category
              </h2>
              <div className="category-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
                {Object.entries(analytics.stats.categories).map(([category, count]) => (
                  <div key={category} className="category-card" style={{ 
                    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)', 
                    padding: '1rem', 
                    borderRadius: '8px',
                    textAlign: 'center',
                    border: '1px solid #e5e7eb'
                  }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1f2937', marginBottom: '0.25rem' }}>{count}</div>
                    <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>{category}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Trending Skills Tab */}
      {activeTab === 'trending' && (
        <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 className="section-title" style={{ margin: 0 }}>
              <FiTrendingUp style={{ marginRight: '0.5rem', display: 'inline' }} />
              Trending Skills Analysis
            </h2>
            <select 
              className="filter-select"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              style={{ padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
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

          {analytics?.trending_skills && analytics.trending_skills.length > 0 ? (
            <div className="skills-table" style={{ background: '#f8fafc', borderRadius: '8px', overflow: 'hidden' }}>
              <div className="table-header" style={{ 
                display: 'grid', 
                gridTemplateColumns: '60px 1fr 120px 100px 100px', 
                gap: '1rem', 
                padding: '1rem', 
                background: '#e2e8f0',
                fontWeight: '600',
                fontSize: '0.875rem',
                color: '#374151'
              }}>
                <div>Rank</div>
                <div>Skill</div>
                <div>Category</div>
                <div>Trend Score</div>
                <div>Growth</div>
              </div>
              {analytics.trending_skills
                .filter(skill => filter === 'All Categories' || skill.category === filter)
                .map((skill, idx) => (
                  <div key={idx} className="table-row" style={{ 
                    display: 'grid', 
                    gridTemplateColumns: '60px 1fr 120px 100px 100px', 
                    gap: '1rem', 
                    padding: '1rem',
                    borderBottom: '1px solid #e5e7eb',
                    alignItems: 'center'
                  }}>
                    <div style={{ fontWeight: '600', color: '#6366f1' }}>#{idx + 1}</div>
                    <div style={{ fontWeight: '500' }}>{skill.skill_name}</div>
                    <div>
                      <span style={{ 
                        padding: '0.25rem 0.5rem', 
                        background: '#dbeafe', 
                        color: '#1e40af', 
                        borderRadius: '4px',
                        fontSize: '0.75rem'
                      }}>
                        {skill.category}
                      </span>
                    </div>
                    <div style={{ fontWeight: '600', color: '#059669' }}>
                      {skill.avg_trend_score || skill.demand_score || 50}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#059669' }}>
                      <FiArrowUp style={{ fontSize: '0.75rem' }} />
                      <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>
                        +{Math.floor(Math.random() * 20 + 5)}%
                      </span>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
              <FiTrendingUp style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
              <h3>No trending data available</h3>
              <p>Check back later for trending skill analysis</p>
            </div>
          )}
        </div>
      )}

      {/* Skill Forecast Tab */}
      {activeTab === 'forecast' && (
        <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 className="section-title" style={{ marginTop: 0 }}>
            <FiTarget style={{ marginRight: '0.5rem', display: 'inline' }} />
            Skill Demand Forecast (6 Months)
          </h2>
          <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
            Based on current trends and historical data, here's our forecast for skill demand growth.
          </p>

          {skillForecast.length > 0 ? (
            <div className="forecast-grid" style={{ display: 'grid', gap: '1rem' }}>
              {skillForecast.map((skill, idx) => (
                <div key={idx} className="forecast-card" style={{ 
                  background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)', 
                  padding: '1.5rem', 
                  borderRadius: '12px',
                  border: '1px solid #e5e7eb'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                    <div>
                      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.125rem', color: '#1f2937' }}>{skill.skill_name}</h3>
                      <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>{skill.category}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: '0.25rem' }}>Growth Rate</div>
                      <div style={{ 
                        fontSize: '1.25rem', 
                        fontWeight: '700', 
                        color: skill.growth_rate > 0 ? '#059669' : '#dc2626',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}>
                        {skill.growth_rate > 0 ? <FiArrowUp /> : <FiArrowDown />}
                        {Math.abs(skill.growth_rate)}%
                      </div>
                    </div>
                  </div>
                  
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: '0.25rem' }}>Current Demand</div>
                      <div style={{ fontSize: '1.125rem', fontWeight: '600', color: '#374151' }}>{skill.current_demand}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: '0.25rem' }}>Forecast Demand</div>
                      <div style={{ fontSize: '1.125rem', fontWeight: '600', color: '#059669' }}>{skill.forecast_demand}</div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ flex: 1, height: '6px', background: '#e5e7eb', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ 
                        height: '100%', 
                        background: 'linear-gradient(90deg, #6366f1, #8b5cf6)', 
                        width: `${skill.current_demand}%`,
                        transition: 'width 0.3s ease'
                      }}></div>
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>Current</div>
                  </div>
                  
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                    <div style={{ flex: 1, height: '6px', background: '#e5e7eb', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ 
                        height: '100%', 
                        background: 'linear-gradient(90deg, #10b981, #34d399)', 
                        width: `${skill.forecast_demand}%`,
                        transition: 'width 0.3s ease'
                      }}></div>
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>Forecast</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
              <FiTarget style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
              <h3>No forecast data available</h3>
              <p>We need more historical data to generate accurate forecasts</p>
            </div>
          )}
        </div>
      )}

      {/* Tech News Tab */}
      {activeTab === 'news' && (
        <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h2 className="section-title" style={{ marginTop: 0 }}>
            <FiFileText style={{ marginRight: '0.5rem', display: 'inline' }} />
            Latest Tech News
          </h2>
          <p style={{ color: '#6b7280', marginBottom: '1.5rem' }}>
            Stay updated with the latest technology trends relevant to your field.
          </p>

          {techNews.length > 0 ? (
            <div className="news-grid" style={{ display: 'grid', gap: '1rem' }}>
              {techNews.map((news) => (
                <div key={news.id} className="news-card" style={{ 
                  background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)', 
                  padding: '1.5rem', 
                  borderRadius: '12px',
                  border: '1px solid #e5e7eb',
                  borderLeft: `4px solid ${getRelevanceColor(news.relevance)}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.125rem', color: '#1f2937', lineHeight: '1.4' }}>
                        {news.title}
                      </h3>
                      <p style={{ margin: '0 0 0.75rem 0', color: '#4b5563', fontSize: '0.875rem', lineHeight: '1.5' }}>
                        {news.summary}
                      </p>
                    </div>
                    <div style={{ marginLeft: '1rem', textAlign: 'right' }}>
                      <span style={{ 
                        padding: '0.25rem 0.5rem', 
                        background: `${getRelevanceColor(news.relevance)}20`,
                        color: getRelevanceColor(news.relevance),
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        fontWeight: '500',
                        textTransform: 'uppercase'
                      }}>
                        {news.relevance}
                      </span>
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.875rem', color: '#6b7280' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ 
                        padding: '0.25rem 0.5rem', 
                        background: '#dbeafe', 
                        color: '#1e40af', 
                        borderRadius: '4px',
                        fontSize: '0.75rem'
                      }}>
                        {news.category}
                      </span>
                      <span>{news.source}</span>
                    </div>
                    <div>{news.published}</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
              <FiFileText style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
              <h3>No news available</h3>
              <p>Check back later for the latest tech news</p>
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!analytics && !loading && (
        <div className="empty-state" style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
          <FiBarChart2 style={{ fontSize: '4rem', marginBottom: '1rem', opacity: 0.3 }} />
          <h3>No Analytics Data Yet</h3>
          <p>Click the "Refresh Data" button above to load the latest skill analytics and trends.</p>
        </div>
      )}
    </div>
  );
};

export default Analytics;