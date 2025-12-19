import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

// Root wrapper to provide AuthContext to entire app
export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
