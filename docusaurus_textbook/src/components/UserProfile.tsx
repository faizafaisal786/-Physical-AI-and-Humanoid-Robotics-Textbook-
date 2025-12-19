import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Link from '@docusaurus/Link';

const UserProfile = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="card">
        <div className="card__body text--center">
          <div className="loading-shimmer" style={{ height: '20px', borderRadius: '4px', margin: '10px 0' }}></div>
          <div className="loading-shimmer" style={{ height: '20px', width: '80%', borderRadius: '4px', margin: '10px auto' }}></div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="card">
        <div className="card__header">
          <h3>Sign in for Personalization</h3>
        </div>
        <div className="card__body">
          <p>Log in to save your progress, bookmark content, and access personalized recommendations.</p>
          <Link to="/login" className="button button--primary button--block">
            Sign In
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card__header">
        <h3>Your Profile</h3>
      </div>
      <div className="card__body">
        <div className="avatar avatar--vertical">
          <div className="avatar__intro">
            <div className="avatar__name">{user.full_name || user.username || 'User'}</div>
            <small className="avatar__subtitle">{user.email}</small>
          </div>
        </div>
        <div className="margin-top--md">
          <Link to="/dashboard" className="button button--block button--outline button--secondary">
            View Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
