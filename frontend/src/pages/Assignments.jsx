import React, { useState } from 'react';
import { FiPlus, FiBookOpen, FiUsers, FiCalendar, FiTarget } from 'react-icons/fi';

const Assignments = () => {
  const [assignments, setAssignments] = useState([
    {
      id: 1,
      title: "Machine Learning Fundamentals",
      topic: "Supervised Learning",
      dueDate: "2024-01-15",
      students: 45,
      status: "active",
      description: "Complete hands-on exercises with scikit-learn"
    },
    {
      id: 2,
      title: "Neural Networks Lab",
      topic: "Deep Learning",
      dueDate: "2024-01-20",
      students: 42,
      status: "draft",
      description: "Build a CNN for image classification"
    }
  ]);

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAssignment, setNewAssignment] = useState({
    title: '',
    topic: '',
    dueDate: '',
    description: '',
    difficulty: 'intermediate'
  });

  const handleCreateAssignment = () => {
    if (newAssignment.title && newAssignment.topic) {
      const assignment = {
        id: assignments.length + 1,
        ...newAssignment,
        students: 0,
        status: 'draft'
      };
      setAssignments([...assignments, assignment]);
      setNewAssignment({ title: '', topic: '', dueDate: '', description: '', difficulty: 'intermediate' });
      setShowCreateForm(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title gradient-text">Assignment Management</h1>
        <p className="page-subtitle">Create and manage assignments for your students</p>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiBookOpen style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{assignments.length}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Assignments</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiUsers style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{assignments.reduce((sum, a) => sum + a.students, 0)}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Students</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiTarget style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{assignments.filter(a => a.status === 'active').length}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Active Assignments</p>
        </div>
      </div>

      {/* Create Assignment Button */}
      <div style={{ marginBottom: '2rem' }}>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(true)}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <FiPlus />
          Create New Assignment
        </button>
      </div>

      {/* Create Assignment Form */}
      {showCreateForm && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="modal" style={{ background: 'white', padding: '2rem', borderRadius: '12px', width: '90%', maxWidth: '500px' }}>
            <h3 style={{ marginTop: 0 }}>Create New Assignment</h3>
            
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Assignment Title</label>
              <input
                type="text"
                value={newAssignment.title}
                onChange={(e) => setNewAssignment({...newAssignment, title: e.target.value})}
                placeholder="e.g., Machine Learning Fundamentals"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Topic</label>
              <select
                value={newAssignment.topic}
                onChange={(e) => setNewAssignment({...newAssignment, topic: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              >
                <option value="">Select a topic</option>
                <option value="Machine Learning">Machine Learning</option>
                <option value="Deep Learning">Deep Learning</option>
                <option value="Natural Language Processing">Natural Language Processing</option>
                <option value="Computer Vision">Computer Vision</option>
                <option value="Data Science">Data Science</option>
                <option value="AI Ethics">AI Ethics</option>
              </select>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Due Date</label>
              <input
                type="date"
                value={newAssignment.dueDate}
                onChange={(e) => setNewAssignment({...newAssignment, dueDate: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Difficulty Level</label>
              <select
                value={newAssignment.difficulty}
                onChange={(e) => setNewAssignment({...newAssignment, difficulty: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Description</label>
              <textarea
                value={newAssignment.description}
                onChange={(e) => setNewAssignment({...newAssignment, description: e.target.value})}
                placeholder="Describe the assignment requirements..."
                rows="4"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px', resize: 'vertical' }}
              />
            </div>

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button 
                onClick={() => setShowCreateForm(false)}
                style={{ padding: '0.75rem 1.5rem', border: '1px solid #d1d5db', background: 'white', borderRadius: '6px', cursor: 'pointer' }}
              >
                Cancel
              </button>
              <button 
                onClick={handleCreateAssignment}
                className="btn-primary"
                style={{ padding: '0.75rem 1.5rem' }}
              >
                Create Assignment
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Assignments List */}
      <div className="assignments-grid" style={{ display: 'grid', gap: '1rem' }}>
        {assignments.map(assignment => (
          <div key={assignment.id} className="assignment-card" style={{ 
            background: 'white', 
            border: '1px solid #e5e7eb', 
            borderRadius: '12px', 
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <div>
                <h3 style={{ margin: '0 0 0.5rem 0', color: '#1f2937' }}>{assignment.title}</h3>
                <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Topic: {assignment.topic}</p>
              </div>
              <span style={{ 
                padding: '0.25rem 0.75rem', 
                borderRadius: '20px', 
                fontSize: '0.75rem',
                fontWeight: '500',
                background: assignment.status === 'active' ? '#dcfce7' : '#fef3c7',
                color: assignment.status === 'active' ? '#166534' : '#92400e'
              }}>
                {assignment.status}
              </span>
            </div>
            
            <p style={{ margin: '0 0 1rem 0', color: '#4b5563' }}>{assignment.description}</p>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.875rem', color: '#6b7280' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FiCalendar />
                Due: {assignment.dueDate}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FiUsers />
                {assignment.students} students
              </div>
            </div>
          </div>
        ))}
      </div>

      {assignments.length === 0 && (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#6b7280' }}>
          <FiBookOpen style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }} />
          <h3>No assignments yet</h3>
          <p>Create your first assignment to get started!</p>
        </div>
      )}
    </div>
  );
};

export default Assignments;
