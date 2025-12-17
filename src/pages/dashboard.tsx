import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../lib/auth-client';

function DashboardPage() {
  const { user, signOut } = useAuth();

  if (!user) {
    return (
      <Layout title="Dashboard" description="User dashboard">
        <div className="container margin-vert--lg">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <div className="card">
                <div className="card__header">
                  <h2>Please log in</h2>
                </div>
                <div className="card__body">
                  <p>You need to be logged in to access the dashboard.</p>
                  <a href="/login" className="button button--primary">
                    Log in
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard" description="Your dashboard">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className="card">
              <div className="card__header">
                <h2>Welcome, {user.name || user.email}!</h2>
              </div>
              <div className="card__body">
                <div className="margin-bottom--md">
                  <h3>Your Profile</h3>
                  <ul>
                    <li><strong>Email:</strong> {user.email}</li>
                    <li><strong>ID:</strong> {user.id}</li>
                    <li><strong>Joined:</strong> {user.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}</li>
                  </ul>
                </div>

                <div className="margin-bottom--md">
                  <h3>Features Available</h3>
                  <ul>
                    <li>Personalized learning path</li>
                    <li>Save progress and bookmarks</li>
                    <li>Access to premium content</li>
                    <li>Download course materials</li>
                  </ul>
                </div>

                <button 
                  onClick={() => signOut()}
                  className="button button--outline button--secondary"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default DashboardPage;