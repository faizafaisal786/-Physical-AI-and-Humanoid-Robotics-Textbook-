import React from 'react';
import { useAuth } from '../lib/auth-client';

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
          <a href="/login" className="button button--primary button--block">
            Sign In
          </a>
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
            <div className="avatar__name">{user.name || 'User'}</div>
            <small className="avatar__subtitle">{user.email}</small>
          </div>
        </div>
        <div className="margin-top--md">
          <a href="/dashboard" className="button button--block button--outline button--secondary">
            View Dashboard
          </a>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;