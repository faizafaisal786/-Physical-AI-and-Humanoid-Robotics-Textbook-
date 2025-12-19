import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Link from '@docusaurus/Link';

const AuthAwareNavbar = () => {
  const { user, signOut, isLoading } = useAuth();

  if (isLoading) {
    return null;
  }

  if (!user) {
    return (
      <div className="navbar__item">
        <Link to="/login" className="navbar__link">
          Log in
        </Link>
      </div>
    );
  }

  return (
    <div className="navbar__item dropdown dropdown--hoverable dropdown--right">
      <a className="navbar__link" href="#">
        {user.full_name || user.username || user.email}
      </a>
      <ul className="dropdown__menu">
        <li>
          <Link to="/dashboard" className="dropdown__link">
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/tasks" className="dropdown__link">
            My Tasks
          </Link>
        </li>
        <li>
          <button
            onClick={() => signOut()}
            className="dropdown__link"
            style={{
              width: '100%',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.25rem 0.5rem'
            }}
          >
            Sign out
          </button>
        </li>
      </ul>
    </div>
  );
};

export default AuthAwareNavbar;
