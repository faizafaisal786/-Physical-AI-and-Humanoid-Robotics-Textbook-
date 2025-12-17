import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import { useAuth } from '../lib/auth-client';

const Navbar = (props) => {
  const { user, signOut } = useAuth();

  return (
    <>
      <OriginalNavbar {...props} />
      {/* Add a custom top bar for auth controls */}
      {user && (
        <div className="custom-auth-bar">
          <div className="container">
            <div style={{float: 'right', padding: '8px 0'}}>
              Welcome, {user.name || user.email}! 
              {' '}
              <a href="/dashboard">Dashboard</a>
              {' | '}
              <button 
                onClick={() => signOut()} 
                style={{background: 'none', border: 'none', color: 'inherit', cursor: 'pointer'}}
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;