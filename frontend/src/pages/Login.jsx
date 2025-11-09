import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoSparklesSharp } from 'react-icons/io5';
import { FiLock, FiUser } from 'react-icons/fi';
import api from '../utils/api';
import { setAuth } from '../utils/auth';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [studentLevel, setStudentLevel] = useState('Junior');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.auth.login({ username, password });
      const data = await response.json();

      if (data.success) {
        // Store token and user info using utility
        setAuth(data.token, data.user);
        
        // Notify parent component
        if (onLogin) onLogin();
        
        // Navigate to home
        navigate('/', { replace: true });
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.auth.register({
        username,
        password,
        email: email || undefined,
        full_name: fullName || undefined,
        student_level: studentLevel
      });

      const data = await response.json();

      if (data.success) {
        // Store token and user info using utility
        setAuth(data.token, data.user);
        
        // Notify parent component
        if (onLogin) onLogin();
        
        // Navigate to home
        navigate('/', { replace: true });
      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <IoSparklesSharp className="login-logo" />
          <h1>EvolveIQ</h1>
          <p>AI-Driven Learning Assistant</p>
        </div>

        {error && (
          <div className="login-error">
            {error}
          </div>
        )}

        {isRegister ? (
          <form onSubmit={handleRegister} className="login-form">
            <div className="form-group">
              <FiUser className="form-icon" />
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <FiLock className="form-icon" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
              />
            </div>

            <div className="form-group">
              <input
                type="email"
                placeholder="Email (optional)"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="form-group">
              <input
                type="text"
                placeholder="Full Name (optional)"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <select
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

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Creating Account...' : 'Register'}
            </button>

            <p className="login-switch">
              Already have an account?{' '}
              <button type="button" onClick={() => setIsRegister(false)} className="link-btn">
                Login
              </button>
            </p>
          </form>
        ) : (
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <FiUser className="form-icon" />
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <FiLock className="form-icon" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>

            <p className="login-switch">
              Don't have an account?{' '}
              <button type="button" onClick={() => setIsRegister(true)} className="link-btn">
                Register
              </button>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}

export default Login;

