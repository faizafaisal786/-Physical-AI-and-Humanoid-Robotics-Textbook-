import { createAuthClient } from 'better-auth/react';

const authClient = createAuthClient({
  fetchOptions: {
    baseUrl: typeof window !== 'undefined' ? '' : process.env.BASE_URL || 'http://localhost:3000',
  },
});

export const { useAuth, AuthProvider, signIn, signOut, signUp } = authClient;

// Also export the individual functions to prevent tree-shaking issues
export { authClient };