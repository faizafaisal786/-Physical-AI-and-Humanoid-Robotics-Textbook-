import { createAuthClient } from 'better-auth/react';

export const { useAuth, AuthProvider, signIn, signOut, signUp } = createAuthClient({
  fetchOptions: {
    baseUrl: typeof window !== 'undefined' ? '' : process.env.BASE_URL || 'http://localhost:3000',
  },
});