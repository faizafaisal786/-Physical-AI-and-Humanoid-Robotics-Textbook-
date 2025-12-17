import React from 'react';
import { AuthProvider } from './lib/auth-client';

export default function Root({ children }) {
  return <AuthProvider>{children}</AuthProvider>;
}