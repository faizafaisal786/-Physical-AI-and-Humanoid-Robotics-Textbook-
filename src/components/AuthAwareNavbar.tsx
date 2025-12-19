import React from 'react';
import NavbarItem from '@theme/NavbarItem';
import { useAuth } from '../lib/auth-client.js';

const AuthAwareNavbar = () => {
  const { user, signOut } = useAuth();

  return (
    <>
      {!user ? (
        <div className="navbar__item navbar__link">
          <a href="/login">Log in</a>
        </div>
      ) : (
        <div className="dropdown dropdown--right dropdown--username">
          <span className="navbar__link">
            {user.name || user.email}
          </span>
          <ul className="dropdown__menu">
            <li>
              <a href="/dashboard" className="dropdown__link">
                Dashboard
              </a>
            </li>
            <li>
              <button 
                onClick={() => signOut()} 
                className="dropdown__link"
                style={{ width: '100%', textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer' }}
              >
                Sign out
              </button>
            </li>
          </ul>
        </div>
      )}
    </>
  );
};

export default AuthAwareNavbar;