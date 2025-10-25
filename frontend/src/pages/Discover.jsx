import React, { useState } from 'react';
import { FiSearch, FiCheckCircle, FiTrendingUp, FiBookOpen, FiExternalLink } from 'react-icons/fi';
import { IoRocketSharp, IoSparklesSharp } from 'react-icons/io5';

function Discover() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [maxResources, setMaxResources] = useState(10);
  const [loadToDb, setLoadToDb] = useState(true);

  const discover = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/discover', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          max_resources: maxResources,
          load_to_db: loadToDb
        })
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      alert('Error: Could not connect to API');
    }
    setLoading(false);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">
          <FiSearch style={{ marginRight: '0.5rem', display: 'inline' }} />
          Discover Resources
        </h1>
        <p className="page-subtitle">AI agents will search the web for learning materials and trends</p>
      </div>

      {/* Discovery Form */}
      <div className="discovery-form">
        <div className="form-group">
          <label>What do you want to learn?</label>
          <input
            type="text"
            className="form-input"
            placeholder="e.g., GenAI and ML skills for IT students"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && discover()}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Max Resources</label>
            <input
              type="number"
              className="form-input"
              value={maxResources}
              onChange={(e) => setMaxResources(parseInt(e.target.value))}
              min="5"
              max="20"
            />
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={loadToDb}
                onChange={(e) => setLoadToDb(e.target.checked)}
              />
              <span>Load results to database</span>
            </label>
          </div>
        </div>

        <button 
          className="discover-btn"
          onClick={discover}
          disabled={loading || !query.trim()}
        >
          {loading ? (
            <>
              <FiSearch style={{ marginRight: '0.5rem' }} />
              Discovering...
            </>
          ) : (
            <>
              <IoRocketSharp style={{ marginRight: '0.5rem' }} />
              Discover Resources
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {loading && (
        <div className="loading-state">
          <div className="spinner-large"></div>
          <p>AI agents are searching the web...</p>
          <p className="loading-substep">This may take 30-60 seconds</p>
        </div>
      )}

      {results && !loading && (
        <div className="results-section">
          {/* Stats */}
          <div className="results-stats">
            <div className="stat-badge">
              <FiBookOpen style={{ marginRight: '0.5rem' }} />
              {results.resources?.length || 0} Resources Found
            </div>
            <div className="stat-badge">
              <FiTrendingUp style={{ marginRight: '0.5rem' }} />
              {results.topics?.length || 0} Trending Topics
            </div>
            {results.stats && (
              <>
                <div className="stat-badge">
                  <FiCheckCircle style={{ marginRight: '0.5rem' }} />
                  {results.stats.resources_loaded || 0} Loaded to DB
                </div>
                <div className="stat-badge">
                  <IoSparklesSharp style={{ marginRight: '0.5rem' }} />
                  {results.stats.skills_extracted || 0} Skills Extracted
                </div>
              </>
            )}
          </div>

          {/* Resources List */}
          {results.resources && results.resources.length > 0 && (
            <div className="resources-list">
              <h3 className="section-title">
                <FiBookOpen style={{ marginRight: '0.5rem', display: 'inline' }} />
                Learning Resources
              </h3>
              {results.resources.map((resource, idx) => (
                <div key={idx} className="resource-card">
                  <div className="resource-header">
                    <h4>{resource.title || 'Untitled'}</h4>
                    <span className="resource-category">{resource.category || 'N/A'}</span>
                  </div>
                  <p className="resource-description">
                    {resource.summary || resource.description || resource.content || 'No description available'}
                  </p>
                  <div className="resource-footer">
                    <span className="resource-score">
                      <IoSparklesSharp style={{ marginRight: '0.25rem' }} />
                      Relevance: {(resource.relevance_score || 0).toFixed(2)}
                    </span>
                    {resource.url && (
                      <a 
                        href={resource.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="resource-link"
                      >
                        Visit Resource <FiExternalLink style={{ marginLeft: '0.25rem' }} />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Discover;

