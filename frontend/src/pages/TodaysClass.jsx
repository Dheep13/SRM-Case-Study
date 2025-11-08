import React, { useState } from 'react';
import { FiCalendar, FiClock, FiUsers, FiBookOpen, FiVideo, FiFileText, FiLink, FiPlus } from 'react-icons/fi';

const TodaysClass = () => {
  const [todayContent, setTodayContent] = useState([
    {
      id: 1,
      title: "Introduction to Neural Networks",
      type: "lecture",
      duration: "90 minutes",
      students: 45,
      status: "scheduled",
      materials: ["Slides", "Code Examples", "Reading Assignment"],
      description: "Covering the basics of neural networks and backpropagation"
    },
    {
      id: 2,
      title: "Hands-on Lab: TensorFlow Basics",
      type: "lab",
      duration: "120 minutes",
      students: 42,
      status: "completed",
      materials: ["Lab Instructions", "Dataset", "Solution Code"],
      description: "Practical session on building your first neural network"
    }
  ]);

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newContent, setNewContent] = useState({
    title: '',
    type: 'lecture',
    duration: '',
    description: '',
    materials: []
  });

  const handleCreateContent = () => {
    if (newContent.title && newContent.duration) {
      const content = {
        id: todayContent.length + 1,
        ...newContent,
        students: 0,
        status: 'scheduled',
        materials: newContent.materials.filter(m => m.trim() !== '')
      };
      setTodayContent([...todayContent, content]);
      setNewContent({ title: '', type: 'lecture', duration: '', description: '', materials: [] });
      setShowCreateForm(false);
    }
  };

  const addMaterial = () => {
    setNewContent({...newContent, materials: [...newContent.materials, '']});
  };

  const updateMaterial = (index, value) => {
    const updatedMaterials = [...newContent.materials];
    updatedMaterials[index] = value;
    setNewContent({...newContent, materials: updatedMaterials});
  };

  const removeMaterial = (index) => {
    const updatedMaterials = newContent.materials.filter((_, i) => i !== index);
    setNewContent({...newContent, materials: updatedMaterials});
  };

  const getTypeIcon = (type) => {
    switch(type) {
      case 'lecture': return <FiBookOpen />;
      case 'lab': return <FiVideo />;
      case 'discussion': return <FiUsers />;
      default: return <FiFileText />;
    }
  };

  const getTypeColor = (type) => {
    switch(type) {
      case 'lecture': return '#3b82f6';
      case 'lab': return '#10b981';
      case 'discussion': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title gradient-text">Today's Class Content</h1>
        <p className="page-subtitle">Plan and manage your daily class materials</p>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiCalendar style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{todayContent.length}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Sessions</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiClock style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{todayContent.reduce((sum, c) => sum + parseInt(c.duration), 0)}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Minutes</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiUsers style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{todayContent.reduce((sum, c) => sum + c.students, 0)}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Students</p>
        </div>
      </div>

      {/* Create Content Button */}
      <div style={{ marginBottom: '2rem' }}>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(true)}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <FiPlus />
          Create Class Content
        </button>
      </div>

      {/* Create Content Form */}
      {showCreateForm && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="modal" style={{ background: 'white', padding: '2rem', borderRadius: '12px', width: '90%', maxWidth: '600px', maxHeight: '80vh', overflowY: 'auto' }}>
            <h3 style={{ marginTop: 0 }}>Create Class Content</h3>
            
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Content Title</label>
              <input
                type="text"
                value={newContent.title}
                onChange={(e) => setNewContent({...newContent, title: e.target.value})}
                placeholder="e.g., Introduction to Neural Networks"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Content Type</label>
              <select
                value={newContent.type}
                onChange={(e) => setNewContent({...newContent, type: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              >
                <option value="lecture">Lecture</option>
                <option value="lab">Lab Session</option>
                <option value="discussion">Discussion</option>
                <option value="workshop">Workshop</option>
              </select>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Duration (minutes)</label>
              <input
                type="number"
                value={newContent.duration}
                onChange={(e) => setNewContent({...newContent, duration: e.target.value})}
                placeholder="90"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Description</label>
              <textarea
                value={newContent.description}
                onChange={(e) => setNewContent({...newContent, description: e.target.value})}
                placeholder="Describe what will be covered in this session..."
                rows="3"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px', resize: 'vertical' }}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Materials & Resources</label>
              {newContent.materials.map((material, index) => (
                <div key={index} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <input
                    type="text"
                    value={material}
                    onChange={(e) => updateMaterial(index, e.target.value)}
                    placeholder="e.g., Slides, Code Examples, Reading Assignment"
                    style={{ flex: 1, padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  />
                  <button
                    onClick={() => removeMaterial(index)}
                    style={{ padding: '0.75rem', background: '#ef4444', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                  >
                    ×
                  </button>
                </div>
              ))}
              <button
                onClick={addMaterial}
                style={{ padding: '0.5rem 1rem', background: '#f3f4f6', border: '1px solid #d1d5db', borderRadius: '6px', cursor: 'pointer', fontSize: '0.875rem' }}
              >
                + Add Material
              </button>
            </div>

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button 
                onClick={() => setShowCreateForm(false)}
                style={{ padding: '0.75rem 1.5rem', border: '1px solid #d1d5db', background: 'white', borderRadius: '6px', cursor: 'pointer' }}
              >
                Cancel
              </button>
              <button 
                onClick={handleCreateContent}
                className="btn-primary"
                style={{ padding: '0.75rem 1.5rem' }}
              >
                Create Content
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Content List */}
      <div className="content-grid" style={{ display: 'grid', gap: '1rem' }}>
        {todayContent.map(content => (
          <div key={content.id} className="content-card" style={{ 
            background: 'white', 
            border: '1px solid #e5e7eb', 
            borderRadius: '12px', 
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ 
                  padding: '0.5rem', 
                  borderRadius: '8px', 
                  background: `${getTypeColor(content.type)}20`,
                  color: getTypeColor(content.type)
                }}>
                  {getTypeIcon(content.type)}
                </div>
                <div>
                  <h3 style={{ margin: '0 0 0.25rem 0', color: '#1f2937' }}>{content.title}</h3>
                  <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem', textTransform: 'capitalize' }}>{content.type}</p>
                </div>
              </div>
              <span style={{ 
                padding: '0.25rem 0.75rem', 
                borderRadius: '20px', 
                fontSize: '0.75rem',
                fontWeight: '500',
                background: content.status === 'completed' ? '#dcfce7' : content.status === 'scheduled' ? '#dbeafe' : '#fef3c7',
                color: content.status === 'completed' ? '#166534' : content.status === 'scheduled' ? '#1e40af' : '#92400e'
              }}>
                {content.status}
              </span>
            </div>
            
            <p style={{ margin: '0 0 1rem 0', color: '#4b5563' }}>{content.description}</p>
            
            {content.materials.length > 0 && (
              <div style={{ marginBottom: '1rem' }}>
                <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '0.875rem', color: '#6b7280' }}>Materials:</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {content.materials.map((material, index) => (
                    <span key={index} style={{ 
                      padding: '0.25rem 0.5rem', 
                      background: '#f3f4f6', 
                      borderRadius: '4px', 
                      fontSize: '0.75rem',
                      color: '#374151'
                    }}>
                      {material}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.875rem', color: '#6b7280' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FiClock />
                {content.duration} minutes
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FiUsers />
                {content.students} students
              </div>
            </div>
          </div>
        ))}
      </div>

      {todayContent.length === 0 && (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
          <FiCalendar style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
          <h3>No class content yet</h3>
          <p>Create your first class session to get started!</p>
        </div>
      )}
    </div>
  );
};

export default TodaysClass;
