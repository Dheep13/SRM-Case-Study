import React, { useState } from 'react';
import { FiUser, FiClock, FiDollarSign, FiCalendar, FiStar, FiMail, FiBriefcase, FiMapPin, FiCheck, FiUsers, FiVideo } from 'react-icons/fi';

const ExpertConsultation = () => {
  const [selectedExpert, setSelectedExpert] = useState(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [bookingDetails, setBookingDetails] = useState({
    duration: '2-weeks',
    startDate: '',
    sessionType: 'one-on-one',
    purpose: ''
  });

  const experts = [
    {
      id: 1,
      name: "Dr. Sarah Chen",
      title: "Senior AI Researcher at Google",
      expertise: ["Machine Learning", "Deep Learning", "Neural Networks"],
      experience: "15+ years",
      rating: 4.9,
      reviews: 127,
      price: "$199/week",
      avatar: "SC",
      company: "Google",
      location: "San Francisco, CA",
      languages: ["English", "Mandarin"],
      availability: "Mon-Fri, 2pm-6pm PST",
      specialties: "ML Engineering, Research, Career Guidance"
    },
    {
      id: 2,
      name: "Michael Rodriguez",
      title: "Lead Software Architect at Amazon",
      expertise: ["Cloud Architecture", "Distributed Systems", "AWS"],
      experience: "12+ years",
      rating: 4.8,
      reviews: 89,
      price: "$179/week",
      avatar: "MR",
      company: "Amazon",
      location: "Seattle, WA",
      languages: ["English", "Spanish"],
      availability: "Mon-Thu, 9am-1pm PST",
      specialties: "System Design, Career Development, Leadership"
    },
    {
      id: 3,
      name: "Dr. Priya Patel",
      title: "Data Science Director at Microsoft",
      expertise: ["Data Science", "Python", "Big Data"],
      experience: "10+ years",
      rating: 4.9,
      reviews: 156,
      price: "$159/week",
      avatar: "PP",
      company: "Microsoft",
      location: "Redmond, WA",
      languages: ["English", "Hindi"],
      availability: "Tue-Sat, 10am-4pm PST",
      specialties: "Data Engineering, Analytics, Mentorship"
    },
    {
      id: 4,
      name: "James Thompson",
      title: "DevOps Lead at Netflix",
      expertise: ["DevOps", "Kubernetes", "CI/CD"],
      experience: "8+ years",
      rating: 4.7,
      reviews: 94,
      price: "$149/week",
      avatar: "JT",
      company: "Netflix",
      location: "Los Gatos, CA",
      languages: ["English"],
      availability: "Mon-Wed, 2pm-8pm PST",
      specialties: "Infrastructure, Automation, Career Strategy"
    },
    {
      id: 5,
      name: "Dr. Emily Watson",
      title: "Security Architect at Meta",
      expertise: ["Cybersecurity", "Ethical Hacking", "Privacy"],
      experience: "14+ years",
      rating: 4.8,
      reviews: 73,
      price: "$189/week",
      avatar: "EW",
      company: "Meta",
      location: "Menlo Park, CA",
      languages: ["English", "French"],
      availability: "Mon-Fri, 8am-2pm PST",
      specialties: "Security, Compliance, Risk Management"
    },
    {
      id: 6,
      name: "Alex Kim",
      title: "Product Manager at Apple",
      expertise: ["Product Management", "Strategy", "Leadership"],
      experience: "7+ years",
      rating: 4.6,
      reviews: 58,
      price: "$169/week",
      avatar: "AK",
      company: "Apple",
      location: "Cupertino, CA",
      languages: ["English", "Korean"],
      availability: "Wed-Sun, 11am-5pm PST",
      specialties: "Product Strategy, Career Growth, Interview Prep"
    }
  ];

  const durationOptions = [
    { value: '1-week', label: '1 Week', priceMultiplier: 1 },
    { value: '2-weeks', label: '2 Weeks', priceMultiplier: 1.8 },
    { value: '4-weeks', label: '4 Weeks', priceMultiplier: 3.2 },
    { value: 'custom', label: 'Custom Duration', priceMultiplier: 1 }
  ];

  const sessionTypes = [
    { value: 'one-on-one', label: 'One-on-One Sessions', icon: FiUser },
    { value: 'group', label: 'Group Sessions', icon: FiUsers },
    { value: 'hybrid', label: 'Hybrid (Mix of both)', icon: FiVideo }
  ];

  const handleBookConsultation = (expert) => {
    setSelectedExpert(expert);
    setShowBookingModal(true);
  };

  const calculateTotalPrice = () => {
    if (!selectedExpert) return 0;
    const basePrice = parseInt(selectedExpert.price.replace(/[^0-9]/g, ''));
    const duration = durationOptions.find(d => d.value === bookingDetails.duration);
    return basePrice * (duration?.priceMultiplier || 1);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title gradient-text">Expert Consultation</h1>
        <p className="page-subtitle">Book industry experts for personalized mentorship and guidance</p>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiUser style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>{experts.length}</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Available Experts</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiStar style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>4.8</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Average Rating</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiUsers style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>597</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Total Bookings</p>
        </div>
        <div className="stat-card" style={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px' }}>
          <FiClock style={{ fontSize: '2rem', marginBottom: '0.5rem' }} />
          <h3 style={{ margin: 0, fontSize: '2rem' }}>24/7</h3>
          <p style={{ margin: 0, opacity: 0.9 }}>Available Support</p>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="section" style={{ background: 'white', padding: '1.5rem', borderRadius: '12px', marginBottom: '2rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <h2 style={{ marginTop: 0 }}>How It Works</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
          <div style={{ textAlign: 'center', padding: '1rem' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1', marginBottom: '0.5rem' }}>1</div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem' }}>Choose Expert</h3>
            <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Browse and select an expert in your field</p>
          </div>
          <div style={{ textAlign: 'center', padding: '1rem' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1', marginBottom: '0.5rem' }}>2</div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem' }}>Select Duration</h3>
            <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Choose 1-week, 2-week, or custom duration</p>
          </div>
          <div style={{ textAlign: 'center', padding: '1rem' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1', marginBottom: '0.5rem' }}>3</div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem' }}>Book & Pay</h3>
            <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Secure your consultation slot</p>
          </div>
          <div style={{ textAlign: 'center', padding: '1rem' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: '#6366f1', marginBottom: '0.5rem' }}>4</div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem' }}>Start Learning</h3>
            <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Get personalized mentorship and guidance</p>
          </div>
        </div>
      </div>

      {/* Experts Grid */}
      <div className="section" style={{ marginBottom: '2rem' }}>
        <h2 className="section-title" style={{ marginTop: 0 }}>Available Experts</h2>
        <div className="experts-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem' }}>
          {experts.map(expert => (
            <div key={expert.id} className="expert-card" style={{ 
              background: 'white', 
              borderRadius: '12px', 
              padding: '1.5rem',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              border: '1px solid #e5e7eb',
              transition: 'transform 0.2s, box-shadow 0.2s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
            }}>
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <div style={{ 
                  width: '60px', 
                  height: '60px', 
                  borderRadius: '12px', 
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: '600',
                  fontSize: '1.25rem'
                }}>
                  {expert.avatar}
                </div>
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 0.25rem 0', fontSize: '1.125rem', color: '#1f2937' }}>{expert.name}</h3>
                  <p style={{ margin: '0 0 0.25rem 0', color: '#6b7280', fontSize: '0.875rem' }}>{expert.title}</p>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FiStar style={{ color: '#fbbf24' }} />
                    <span style={{ fontWeight: '600' }}>{expert.rating}</span>
                    <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>({expert.reviews} reviews)</span>
                  </div>
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <FiBriefcase style={{ fontSize: '0.875rem', color: '#6b7280' }} />
                  <span style={{ fontSize: '0.875rem', color: '#374151' }}><strong>Experience:</strong> {expert.experience}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <FiMapPin style={{ fontSize: '0.875rem', color: '#6b7280' }} />
                  <span style={{ fontSize: '0.875rem', color: '#374151' }}>{expert.location}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <FiClock style={{ fontSize: '0.875rem', color: '#6b7280' }} />
                  <span style={{ fontSize: '0.875rem', color: '#374151' }}>{expert.availability}</span>
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: '600', color: '#6b7280', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Expertise</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {expert.expertise.map((skill, idx) => (
                    <span key={idx} style={{ 
                      padding: '0.25rem 0.5rem', 
                      background: '#e0e7ff', 
                      color: '#4338ca', 
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: '500'
                    }}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '1rem', borderTop: '1px solid #e5e7eb' }}>
                <div>
                  <div style={{ fontSize: '1.25rem', fontWeight: '700', color: '#059669' }}>{expert.price}</div>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>per week</div>
                </div>
                <button 
                  onClick={() => handleBookConsultation(expert)}
                  className="btn-primary"
                  style={{ padding: '0.75rem 1.5rem', fontSize: '0.875rem' }}
                >
                  Book Consultation
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Booking Modal */}
      {showBookingModal && selectedExpert && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }} onClick={() => setShowBookingModal(false)}>
          <div className="modal" style={{ background: 'white', padding: '2rem', borderRadius: '12px', width: '90%', maxWidth: '600px', maxHeight: '80vh', overflowY: 'auto' }} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
              <div>
                <h3 style={{ margin: '0 0 0.5rem 0' }}>Book Consultation</h3>
                <p style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>with {selectedExpert.name}</p>
              </div>
              <button 
                onClick={() => setShowBookingModal(false)}
                style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: '#6b7280' }}
              >
                ×
              </button>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Select Duration</label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem' }}>
                {durationOptions.map(option => (
                  <button
                    key={option.value}
                    onClick={() => setBookingDetails({...bookingDetails, duration: option.value})}
                    style={{ 
                      padding: '1rem', 
                      border: bookingDetails.duration === option.value ? '2px solid #6366f1' : '1px solid #d1d5db',
                      borderRadius: '8px',
                      background: bookingDetails.duration === option.value ? '#f0f4ff' : 'white',
                      cursor: 'pointer',
                      textAlign: 'left'
                    }}
                  >
                    <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{option.label}</div>
                    {option.value !== 'custom' && (
                      <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                        ${parseInt(selectedExpert.price.replace(/[^0-9]/g, '')) * option.priceMultiplier}/week
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Session Type</label>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                {sessionTypes.map(type => (
                  <button
                    key={type.value}
                    onClick={() => setBookingDetails({...bookingDetails, sessionType: type.value})}
                    style={{ 
                      flex: 1,
                      padding: '0.75rem', 
                      border: bookingDetails.sessionType === type.value ? '2px solid #6366f1' : '1px solid #d1d5db',
                      borderRadius: '8px',
                      background: bookingDetails.sessionType === type.value ? '#f0f4ff' : 'white',
                      cursor: 'pointer',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}
                  >
                    <type.icon style={{ fontSize: '1.5rem', color: bookingDetails.sessionType === type.value ? '#6366f1' : '#6b7280' }} />
                    <span style={{ fontSize: '0.75rem', textAlign: 'center' }}>{type.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Preferred Start Date</label>
              <input
                type="date"
                value={bookingDetails.startDate}
                onChange={(e) => setBookingDetails({...bookingDetails, startDate: e.target.value})}
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '8px' }}
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>Purpose of Consultation</label>
              <textarea
                value={bookingDetails.purpose}
                onChange={(e) => setBookingDetails({...bookingDetails, purpose: e.target.value})}
                placeholder="e.g., Career guidance, project help, interview preparation..."
                rows="4"
                style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '8px', resize: 'vertical' }}
              />
            </div>

            <div style={{ background: '#f9fafb', padding: '1rem', borderRadius: '8px', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: '600' }}>Consultation Fee</span>
                <span style={{ fontWeight: '700', fontSize: '1.125rem', color: '#059669' }}>
                  ${calculateTotalPrice()}/week
                </span>
              </div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                {durationOptions.find(d => d.value === bookingDetails.duration)?.label} duration
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              <button 
                onClick={() => setShowBookingModal(false)}
                style={{ flex: 1, padding: '0.75rem', border: '1px solid #d1d5db', background: 'white', borderRadius: '8px', cursor: 'pointer', fontWeight: '500' }}
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  alert('Booking confirmed! You will receive an email confirmation shortly.');
                  setShowBookingModal(false);
                }}
                className="btn-primary"
                style={{ flex: 1, padding: '0.75rem', fontWeight: '500' }}
              >
                Confirm Booking
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExpertConsultation;
