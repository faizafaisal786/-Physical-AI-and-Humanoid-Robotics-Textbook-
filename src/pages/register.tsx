import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../lib/auth-client';

function RegisterPage() {
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await signUp.email({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        callbackURL: '/dashboard'
      });
    } catch (err) {
      setError(err.message || 'Registration failed');
    }
  };

  return (
    <Layout title="Register" description="Create a new account">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Create Account</h2>
              </div>
              <div className="card__body">
                {error && (
                  <div className="alert alert--danger">
                    {error}
                  </div>
                )}
                <form onSubmit={handleSubmit}>
                  <div className="margin-bottom--sm">
                    <label htmlFor="name">Full Name</label>
                    <input
                      type="text"
                      id="name"
                      className="form-control"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="margin-bottom--sm">
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      required
                    />
                  </div>
                  <div className="margin-bottom--sm">
                    <label htmlFor="password">Password</label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      value={formData.password}
                      onChange={(e) => setFormData({...formData, password: e.target.value})}
                      required
                      minLength={6}
                    />
                  </div>
                  <button type="submit" className="button button--primary button--block">
                    Register
                  </button>
                </form>
                
                <div className="margin-top--md">
                  <p>Already have an account? <a href="/login">Sign in</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default RegisterPage;