import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatWidget from '../components/ChatWidget';

// Root wrapper to provide AuthContext to entire app and add global ChatWidget
export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
      <ChatWidget />
    </AuthProvider>
  );
}
