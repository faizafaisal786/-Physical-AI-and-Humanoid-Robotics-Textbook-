import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import Link from '@docusaurus/Link';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signUp, user } = useAuth();
  const history = useHistory();

  // Redirect if already logged in
  React.useEffect(() => {
    if (user) {
      history.push('/dashboard');
    }
  }, [user, history]);

  const validateForm = (): boolean => {
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }

    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
      setError('Password must contain at least one uppercase letter, one lowercase letter, and one number');
      return false;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await signUp({
        email,
        password,
        full_name: fullName || undefined,
        username: username || undefined,
      });
      history.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create a new account">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Create Your Account</h2>
              </div>
              <div className="card__body">
                {error && (
                  <div className="alert alert--danger" role="alert">
                    {error}
                  </div>
                )}

                <form onSubmit={handleSubmit}>
                  <div className="margin-bottom--md">
                    <label htmlFor="email" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="input"
                      placeholder="your@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      disabled={loading}
                      style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--ifm-color-emphasis-300)' }}
                    />
                  </div>

                  <div className="margin-bottom--md">
                    <label htmlFor="fullName" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Full Name
                    </label>
                    <input
                      type="text"
                      id="fullName"
                      className="input"
                      placeholder="John Doe"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      disabled={loading}
                      style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--ifm-color-emphasis-300)' }}
                    />
                  </div>

                  <div className="margin-bottom--md">
                    <label htmlFor="username" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Username
                    </label>
                    <input
                      type="text"
                      id="username"
                      className="input"
                      placeholder="johndoe"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      disabled={loading}
                      style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--ifm-color-emphasis-300)' }}
                    />
                  </div>

                  <div className="margin-bottom--md">
                    <label htmlFor="password" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Password *
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="input"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      disabled={loading}
                      style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--ifm-color-emphasis-300)' }}
                    />
                    <small className="text--secondary">
                      Min 8 characters, 1 uppercase, 1 lowercase, 1 number
                    </small>
                  </div>

                  <div className="margin-bottom--md">
                    <label htmlFor="confirmPassword" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Confirm Password *
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      className="input"
                      placeholder="••••••••"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      disabled={loading}
                      style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--ifm-color-emphasis-300)' }}
                    />
                  </div>

                  <button
                    type="submit"
                    className="button button--primary button--block"
                    disabled={loading}
                  >
                    {loading ? 'Creating Account...' : 'Sign Up'}
                  </button>
                </form>

                <div className="margin-top--md text--center">
                  <p>
                    Already have an account?{' '}
                    <Link to="/login">Login</Link>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
