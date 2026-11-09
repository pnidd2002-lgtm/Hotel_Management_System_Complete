import React, { useState } from 'react';

export default function LoginModal({ show, onClose, onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Register fields
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!show) return null;

  // Login handler
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Invalid username/email or password');
      }

      onLoginSuccess(data);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Register handler
  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fullName, email, password, phone, address })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || 'Registration failed');
      }

      onLoginSuccess(data);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(11, 19, 32, 0.7)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content shadow-lg border-0" style={{ borderRadius: '24px', overflow: 'hidden' }}>
          
          {/* Header */}
          <div className="modal-header py-3 px-4 text-white" style={{ backgroundColor: '#0b1320' }}>
            <div>
              <span className="boutique-tagline d-block" style={{ fontSize: '0.65rem' }}>DUTCH POINT NEGOMBO</span>
              <h5 className="modal-title brand-serif fs-4 mb-0">
                {isRegister ? 'Guest Registration' : 'Welcome Back'}
              </h5>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>

          <div className="modal-body p-4 bg-white">
            {error && (
              <div className="alert alert-danger py-2 small mb-3">{error}</div>
            )}

            {!isRegister ? (
              /* LOGIN */
              <form onSubmit={handleLogin}>
                <div className="mb-3">
                  <label className="form-label small fw-semibold text-secondary">Username or Email</label>
                  <input 
                    type="text" 
                    className="form-control rounded-pill px-3 py-2" 
                    required 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. Pasindu or name@example.com"
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label small fw-semibold text-secondary">Password</label>
                  <input 
                    type="password" 
                    className="form-control rounded-pill px-3 py-2" 
                    required 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password"
                  />
                </div>

                <button 
                  type="submit" 
                  className="btn btn-luxury-dark w-100 py-2 mt-2" 
                  disabled={loading}
                >
                  {loading ? 'Authenticating...' : 'Sign In'}
                </button>

                <div className="text-center mt-3 small text-muted">
                  New to Dutch Point?{' '}
                  <button 
                    type="button" 
                    className="btn btn-link p-0 small text-decoration-none fw-semibold brand-gold"
                    onClick={() => { setIsRegister(true); setError(''); }}
                  >
                    Register an Account
                  </button>
                </div>
              </form>
            ) : (
              /* REGISTER */
              <form onSubmit={handleRegister}>
                <div className="mb-2">
                  <label className="form-label small fw-semibold text-secondary">Full Name</label>
                  <input 
                    type="text" 
                    className="form-control rounded-pill form-control-sm px-3" 
                    required 
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Rachel Adams"
                  />
                </div>

                <div className="row g-2 mb-2">
                  <div className="col-md-6">
                    <label className="form-label small fw-semibold text-secondary">Email Address</label>
                    <input 
                      type="email" 
                      className="form-control rounded-pill form-control-sm px-3" 
                      required 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="rachel@example.com"
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-semibold text-secondary">Phone</label>
                    <input 
                      type="text" 
                      className="form-control rounded-pill form-control-sm px-3" 
                      required 
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+94 77 123 4567"
                    />
                  </div>
                </div>

                <div className="mb-2">
                  <label className="form-label small fw-semibold text-secondary">Password</label>
                  <input 
                    type="password" 
                    className="form-control rounded-pill form-control-sm px-3" 
                    required 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Create a password"
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label small fw-semibold text-secondary">Address / City</label>
                  <input 
                    type="text" 
                    className="form-control rounded-pill form-control-sm px-3" 
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    placeholder="e.g. Negombo, Sri Lanka"
                  />
                </div>

                <button 
                  type="submit" 
                  className="btn btn-luxury-dark w-100 py-2" 
                  disabled={loading}
                >
                  {loading ? 'Creating account...' : 'Complete Registration'}
                </button>

                <div className="text-center mt-3 small text-muted">
                  Already registered?{' '}
                  <button 
                    type="button" 
                    className="btn btn-link p-0 small text-decoration-none fw-semibold brand-gold"
                    onClick={() => { setIsRegister(false); setError(''); }}
                  >
                    Back to Sign In
                  </button>
                </div>
              </form>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}
