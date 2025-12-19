import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import Link from '@docusaurus/Link';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { signIn, user } = useAuth();
  const history = useHistory();

  // Redirect if already logged in
  React.useEffect(() => {
    if (user) {
      history.push('/dashboard');
    }
  }, [user, history]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await signIn({ email, password });
      history.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Login" description="Login to your account">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Login to Your Account</h2>
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
                      Email Address
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
                    <label htmlFor="password" className="margin-bottom--sm" style={{ display: 'block' }}>
                      Password
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
                  </div>

                  <button
                    type="submit"
                    className="button button--primary button--block"
                    disabled={loading}
                  >
                    {loading ? 'Logging in...' : 'Login'}
                  </button>
                </form>

                <div className="margin-top--md text--center">
                  <p>
                    Don't have an account?{' '}
                    <Link to="/signup">Sign up</Link>
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
