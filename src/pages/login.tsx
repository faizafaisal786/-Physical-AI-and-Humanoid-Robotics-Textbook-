import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../lib/auth-client';

function LoginPage() {
  const { signIn } = useAuth();
  
  const handleGoogleLogin = () => {
    signIn.social({
      provider: 'google',
      callbackURL: '/dashboard',
    });
  };

  const handleGithubLogin = () => {
    signIn.social({
      provider: 'github',
      callbackURL: '/dashboard',
    });
  };

  return (
    <Layout title="Login" description="Login to your account">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="card">
              <div className="card__header">
                <h2>Login to Physical AI Textbook</h2>
              </div>
              <div className="card__body">
                <div className="button-group button-group--block">
                  <button 
                    className="button button--secondary"
                    onClick={handleGoogleLogin}
                  >
                    Sign in with Google
                  </button>
                </div>
                <div className="margin-top--md button-group button-group--block">
                  <button 
                    className="button button--secondary"
                    onClick={handleGithubLogin}
                  >
                    Sign in with GitHub
                  </button>
                </div>
                
                <div className="margin-top--md">
                  <p>Or create an account:</p>
                  <a href="/register" className="button button--primary button--block">
                    Register
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default LoginPage;