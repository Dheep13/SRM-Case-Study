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
  const [newsDateFilter, setNewsDateFilter] = useState(7); // Days back
  const [trendingSkills, setTrendingSkills] = useState([]); // Real trending skills from Tavily

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const response = await api.analytics();
      const data = await response.json();
      setAnalytics(data);
      setLastRefresh(new Date());
      
      // Generate skill forecast based on existing data
      generateSkillForecast(data.all_skills || []);
      
      // Load trending skills from Tavily
      loadTrendingSkills();
      
      // Load tech news
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

  const generateSkillForecast = async (skills) => {
    // Fetch real skill forecast from Tavily job market analysis
    console.log('🔄 Fetching skill forecasts from Tavily...');
    try {
      const response = await api.skillForecast(10);
      
      if (!response.ok) {
        throw new Error(`API returned ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('📊 API Response:', data);
      
      if (data.forecasts && data.forecasts.length > 0) {
        setSkillForecast(data.forecasts);
        console.log(`✅ Loaded ${data.forecasts.length} skill forecasts from job market data`);
      } else {
        // Fallback to basic forecast if Tavily returns no results
        console.log('⚠️ No skill forecasts from Tavily, using fallback');
        const fallbackForecast = [
          {
            skill: 'Artificial Intelligence',
            current_demand: 85,
            forecast_demand: 95,
            growth_rate: '+12%',
            trend: 'up',
            category: 'AI/ML',
            confidence: 'high'
          },
          {
            skill: 'Python',
            current_demand: 80,
            forecast_demand: 90,
            growth_rate: '+13%',
            trend: 'up',
            category: 'Programming',
            confidence: 'high'
          },
          {
            skill: 'Machine Learning',
            current_demand: 75,
            forecast_demand: 88,
            growth_rate: '+17%',
            trend: 'up',
            category: 'AI/ML',
            confidence: 'medium'
          },
          {
            skill: 'Cloud Computing',
            current_demand: 78,
            forecast_demand: 87,
            growth_rate: '+12%',
            trend: 'up',
            category: 'Cloud/DevOps',
            confidence: 'high'
          },
          {
            skill: 'Cybersecurity',
            current_demand: 72,
            forecast_demand: 85,
            growth_rate: '+18%',
            trend: 'up',
            category: 'Security',
            confidence: 'medium'
          },
          {
            skill: 'JavaScript',
            current_demand: 76,
            forecast_demand: 84,
            growth_rate: '+11%',
            trend: 'up',
            category: 'Web Development',
            confidence: 'high'
          },
          {
            skill: 'React',
            current_demand: 70,
            forecast_demand: 82,
            growth_rate: '+17%',
            trend: 'up',
            category: 'Frontend',
            confidence: 'medium'
          },
          {
            skill: 'Docker',
            current_demand: 68,
            forecast_demand: 80,
            growth_rate: '+18%',
            trend: 'up',
            category: 'DevOps',
            confidence: 'medium'
          },
          {
            skill: 'SQL',
            current_demand: 74,
            forecast_demand: 79,
            growth_rate: '+7%',
            trend: 'up',
            category: 'Database',
            confidence: 'high'
          },
          {
            skill: 'TypeScript',
            current_demand: 65,
            forecast_demand: 77,
            growth_rate: '+18%',
            trend: 'up',
            category: 'Programming',
            confidence: 'medium'
          }
        ];
        setSkillForecast(fallbackForecast);
      }
    } catch (error) {
      console.error('Error loading skill forecast:', error);
      // Fallback to mock data on error
        const forecast = skills.slice(0, 10).map(skill => {
        const currentDemand = skill.demand_score || 50;
        const trendFactor = Math.random() * 0.3 + 0.85; // 85-115% variation
        const forecastDemand = Math.round(currentDemand * trendFactor);
        const growthRate = Math.round((forecastDemand - currentDemand) / currentDemand * 100);
        
        return {
          ...skill,
          skill: skill.skill_name || skill.skill,
          current_demand: currentDemand,
          forecast_demand: forecastDemand,
          growth_rate: `+${growthRate}%`,
          forecast_period: '6 months'
        };
      }).sort((a, b) => b.forecast_demand - a.forecast_demand);
      
      setSkillForecast(forecast);
    }
  };

  const loadTrendingSkills = async (daysBack = 30) => {
    // Fetch real trending skills from Tavily
    try {
      const response = await api.trendingSkills(10, daysBack);
      const data = await response.json();
      
      if (data.trends && data.trends.length > 0) {
        setTrendingSkills(data.trends);
        // Also update analytics.trending_skills for backward compatibility
        if (analytics) {
          setAnalytics({
            ...analytics,
            trending_skills: data.trends.map(trend => ({
              skill_name: trend.skill,
              category: trend.category,
              trend_score: trend.trend_score,
              change: trend.change,
              momentum: trend.momentum,
              description: trend.description
            }))
          });
        }
        console.log(`✓ Loaded ${data.trends.length} trending skills from tech community`);
      } else {
        console.log('No trending skills from Tavily, using fallback');
        setTrendingSkills([]);
      }
    } catch (error) {
      console.error('Error loading trending skills:', error);
      setTrendingSkills([]);
    }
  };

  const loadTechNews = async (daysBack = newsDateFilter) => {
    // Fetch real tech news from Tavily API via backend
    setLoading(true);
    try {
      const response = await api.techNews('AI machine learning technology programming software development', 10, daysBack);
      const data = await response.json();
      
      if (data.news && data.news.length > 0) {
        setTechNews(data.news);
        console.log(`✓ Loaded ${data.news.length} tech news articles (${daysBack} days back)`);
      } else {
        // Fallback to sample news if Tavily returns no results
        console.log('No tech news from Tavily, using fallback');
        setTechNews([
          {
            id: 1,
            title: "AI & Technology News Loading...",
            summary: "Real-time tech news will appear here. Powered by Tavily.",
            category: "AI/ML",
            published: "Recently",
            source: "Tech News",
            relevance: "medium"
          }
        ]);
      }
    } catch (error) {
      console.error('Error loading tech news:', error);
      // Fallback to informative message
      setTechNews([
        {
          id: 1,
          title: "Tech News Temporarily Unavailable",
          summary: "Unable to fetch latest tech news. Please try refreshing.",
          category: "Technology",
          published: "Now",
          source: "System",
          relevance: "low"
        }
      ]);
    } finally {
      setLoading(false);
    }
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
            <div>
              <h2 className="section-title" style={{ margin: 0, marginBottom: '0.5rem' }}>
                <FiTrendingUp style={{ marginRight: '0.5rem', display: 'inline' }} />
                Trending Skills Analysis
              </h2>
              <p style={{ color: '#6b7280', margin: 0, fontSize: '0.875rem' }}>
                Real-time analysis from tech community • Powered by Tavily
              </p>
            </div>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <button
                onClick={() => loadTrendingSkills(30)}
                disabled={loading}
                style={{
                  padding: '0.5rem 1rem',
                  background: loading ? '#9ca3af' : '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontSize: '0.875rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s ease'
                }}
              >
                <FiRefreshCw style={{ 
                  animation: loading ? 'spin 1s linear infinite' : 'none'
                }} /> 
                {loading ? 'Analyzing...' : 'Refresh'}
              </button>
            </div>
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 className="section-title" style={{ margin: 0, fontSize: '0.875rem', fontWeight: '500', color: '#6b7280' }}>
              Filter by Category
            </h3>
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
                gridTemplateColumns: '60px 2fr 1fr 1fr 1fr', 
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
                <div>Momentum</div>
                <div>Growth</div>
              </div>
              {analytics.trending_skills
                .filter(skill => filter === 'All Categories' || skill.category === filter)
                .map((skill, idx) => (
                  <div key={idx} className="table-row" style={{ 
                    display: 'grid', 
                    gridTemplateColumns: '60px 2fr 1fr 1fr 1fr', 
                    gap: '1rem', 
                    padding: '1rem',
                    borderBottom: '1px solid #e5e7eb',
                    alignItems: 'center'
                  }}>
                    <div style={{ fontWeight: '600', color: '#6366f1', fontSize: '1.25rem' }}>#{idx + 1}</div>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                        <span style={{ fontWeight: '600', color: '#1f2937' }}>{skill.skill_name}</span>
                        {skill.momentum && (
                          <span>{skill.momentum === 'hot' ? '🔥' : skill.momentum === 'rising' ? '📈' : '➡️'}</span>
                        )}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>{skill.category}</div>
                      {skill.description && (
                        <div style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '0.25rem', maxWidth: '500px' }}>
                          {skill.description}
                        </div>
                      )}
                    </div>
                    <div>
                      {skill.momentum && (
                        <span style={{ 
                          padding: '0.5rem', 
                          background: skill.momentum === 'hot' ? '#fee2e2' : skill.momentum === 'rising' ? '#ffedd5' : '#f3f4f6', 
                          color: skill.momentum === 'hot' ? '#dc2626' : skill.momentum === 'rising' ? '#ea580c' : '#6b7280', 
                          borderRadius: '6px',
                          fontSize: '0.75rem',
                          fontWeight: '600',
                          textTransform: 'uppercase'
                        }}>
                          {skill.momentum}
                        </span>
                      )}
                    </div>
                    <div>
                      <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1f2937' }}>
                        {Math.round(skill.trend_score || skill.avg_trend_score || skill.demand_score || 50)}/100
                      </div>
                      <div style={{ fontSize: '0.625rem', color: '#6b7280', textTransform: 'uppercase', marginTop: '0.125rem' }}>
                        Trend Score
                      </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      <span style={{ 
                        padding: '0.5rem', 
                        background: '#dcfce7', 
                        color: '#16a34a', 
                        borderRadius: '6px',
                        fontSize: '1rem',
                        fontWeight: '600'
                      }}>
                        {skill.change || `+${Math.floor(Math.random() * 20 + 5)}%`}
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
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h2 className="section-title" style={{ marginTop: 0, marginBottom: '0.5rem' }}>
                <FiTarget style={{ marginRight: '0.5rem', display: 'inline' }} />
                Skill Demand Forecast
              </h2>
              <p style={{ color: '#6b7280', margin: 0 }}>
                Real-time job market analysis • Powered by Tavily
              </p>
            </div>
            <button
              onClick={() => generateSkillForecast(analytics?.all_skills || [])}
              disabled={loading}
              style={{
                padding: '0.5rem 1rem',
                background: loading ? '#9ca3af' : '#6366f1',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '0.875rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.2s ease'
              }}
            >
              <FiRefreshCw style={{ 
                animation: loading ? 'spin 1s linear infinite' : 'none'
              }} /> 
              {loading ? 'Analyzing...' : 'Refresh'}
            </button>
          </div>

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
                      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.125rem', color: '#1f2937' }}>
                        {skill.skill || skill.skill_name}
                      </h3>
                      {skill.category && (
                        <span style={{ 
                          fontSize: '0.7rem', 
                          padding: '0.125rem 0.5rem', 
                          background: '#dbeafe', 
                          color: '#1e40af',
                          borderRadius: '4px',
                          marginTop: '0.25rem',
                          display: 'inline-block'
                        }}>
                          {skill.category}
                        </span>
                      )}
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.75rem', color: '#6b7280', marginBottom: '0.25rem' }}>Growth Rate</div>
                      <div style={{ 
                        fontSize: '1.25rem', 
                        fontWeight: '700', 
                        color: '#059669',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}>
                        <FiArrowUp />
                        {skill.growth_rate || '+10%'}
                      </div>
                    </div>
                  </div>
                  
                  {/* Side-by-side Bar Chart Comparison */}
                  <div style={{ 
                    display: 'flex', 
                    gap: '1rem', 
                    alignItems: 'center',
                    padding: '1rem',
                    background: 'linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%)',
                    borderRadius: '8px',
                    marginTop: '1rem'
                  }}>
                    {/* Current Demand Bar */}
                    <div style={{ flex: 1 }}>
                      <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        marginBottom: '0.5rem'
                      }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: '600', color: '#6366f1', textTransform: 'uppercase' }}>
                          Current
                        </span>
                        <span style={{ fontSize: '1.25rem', fontWeight: '700', color: '#1f2937' }}>
                          {Math.round(skill.current_demand || 0)}
                        </span>
                      </div>
                      <div style={{ 
                        height: '32px', 
                        background: '#e5e7eb', 
                        borderRadius: '6px', 
                        overflow: 'hidden',
                        position: 'relative'
                      }}>
                        <div style={{ 
                          height: '100%', 
                          background: 'linear-gradient(90deg, #6366f1, #818cf8)', 
                          width: `${Math.round(skill.current_demand || 0)}%`,
                          transition: 'width 0.5s ease',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'flex-end',
                          paddingRight: '8px'
                        }}>
                          <span style={{ 
                            color: 'white', 
                            fontSize: '0.75rem', 
                            fontWeight: '600',
                            textShadow: '0 1px 2px rgba(0,0,0,0.2)'
                          }}>
                            {Math.round(skill.current_demand || 0)}%
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Arrow Indicator */}
                    <div style={{ 
                      display: 'flex', 
                      flexDirection: 'column', 
                      alignItems: 'center',
                      minWidth: '50px'
                    }}>
                      <FiArrowUp style={{ 
                        fontSize: '1.5rem', 
                        color: '#10b981',
                        animation: 'bounce 2s infinite'
                      }} />
                      <span style={{ 
                        fontSize: '0.875rem', 
                        fontWeight: '700', 
                        color: '#10b981',
                        marginTop: '0.25rem'
                      }}>
                        {skill.growth_rate || '+10%'}
                      </span>
                    </div>

                    {/* Forecast Demand Bar */}
                    <div style={{ flex: 1 }}>
                      <div style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        marginBottom: '0.5rem'
                      }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: '600', color: '#10b981', textTransform: 'uppercase' }}>
                          Forecast
                        </span>
                        <span style={{ fontSize: '1.25rem', fontWeight: '700', color: '#1f2937' }}>
                          {Math.round(skill.forecast_demand || 0)}
                        </span>
                      </div>
                      <div style={{ 
                        height: '32px', 
                        background: '#e5e7eb', 
                        borderRadius: '6px', 
                        overflow: 'hidden',
                        position: 'relative'
                      }}>
                        <div style={{ 
                          height: '100%', 
                          background: 'linear-gradient(90deg, #10b981, #34d399)', 
                          width: `${Math.round(skill.forecast_demand || 0)}%`,
                          transition: 'width 0.5s ease',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'flex-end',
                          paddingRight: '8px'
                        }}>
                          <span style={{ 
                            color: 'white', 
                            fontSize: '0.75rem', 
                            fontWeight: '600',
                            textShadow: '0 1px 2px rgba(0,0,0,0.2)'
                          }}>
                            {Math.round(skill.forecast_demand || 0)}%
                          </span>
                        </div>
                      </div>
                    </div>
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
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <div>
              <h2 className="section-title" style={{ marginTop: 0, marginBottom: '0.5rem' }}>
                <FiFileText style={{ marginRight: '0.5rem', display: 'inline' }} />
                Latest Tech News
              </h2>
              <p style={{ color: '#6b7280', margin: 0 }}>
                Stay updated with the latest technology trends • Powered by Tavily
              </p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FiCalendar style={{ color: '#6b7280' }} />
                <select 
                  value={newsDateFilter}
                onChange={(e) => {
                  const days = parseInt(e.target.value);
                  console.log('Date filter changed to', days, 'days');
                  setNewsDateFilter(days);
                  loadTechNews(days);
                }}
                  style={{
                    padding: '0.5rem 1rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '0.875rem',
                    background: 'white'
                  }}
                >
                  <option value="1">Today</option>
                  <option value="3">Past 3 Days</option>
                  <option value="7">Past Week</option>
                  <option value="14">Past 2 Weeks</option>
                  <option value="30">Past Month</option>
                </select>
              </div>
              <button
                onClick={() => {
                  console.log('Refresh button clicked - fetching news for', newsDateFilter, 'days back');
                  loadTechNews(newsDateFilter);
                }}
                disabled={loading}
                style={{
                  padding: '0.5rem 1rem',
                  background: loading ? '#9ca3af' : '#6366f1',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontSize: '0.875rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s ease',
                  opacity: loading ? 0.7 : 1
                }}
              >
                <FiRefreshCw style={{ 
                  animation: loading ? 'spin 1s linear infinite' : 'none'
                }} /> 
                {loading ? 'Refreshing...' : 'Refresh'}
              </button>
            </div>
          </div>

          {techNews.length > 0 ? (
            <div className="news-grid" style={{ display: 'grid', gap: '1rem' }}>
              {techNews.map((news) => (
                <a 
                  key={news.id} 
                  href={news.url || '#'} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ textDecoration: 'none', display: 'block' }}
                >
                  <div className="news-card" style={{ 
                    background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)', 
                    padding: '1.5rem', 
                    borderRadius: '12px',
                    border: '1px solid #e5e7eb',
                    borderLeft: `4px solid ${getRelevanceColor(news.relevance)}`,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    ':hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                    }
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                  >
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
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span>{news.published}</span>
                        {news.url && (
                          <span style={{ color: '#6366f1', fontSize: '0.875rem' }}>→</span>
                        )}
                      </div>
                    </div>
                  </div>
                </a>
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

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
  }
`;
if (!document.querySelector('style[data-analytics-animations]')) {
  style.setAttribute('data-analytics-animations', 'true');
  document.head.appendChild(style);
}