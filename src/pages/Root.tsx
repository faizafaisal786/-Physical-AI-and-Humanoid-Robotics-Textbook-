import React from 'react';
import { AuthProvider } from '../lib/auth-client.js';

export default function Root({ children }) {
  return <AuthProvider>{children}</AuthProvider>;
}