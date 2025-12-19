import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authClient, User, LoginCredentials, SignupData, AuthResponse } from '../lib/auth-client';

interface AuthContextType {
  user: User | null;
  signIn: (credentials: LoginCredentials) => Promise<AuthResponse>;
  signOut: () => Promise<void>;
  signUp: (data: SignupData) => Promise<AuthResponse>;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(authClient.getUser());
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize user from stored session
    const currentUser = authClient.getUser();
    if (currentUser) {
      setUser(currentUser);
    }

    // Try to refresh token on mount if we have a refresh token
    const initAuth = async () => {
      if (authClient.getAccessToken()) {
        // Token exists, user should be set
        return;
      }

      // Try to refresh if we don't have access token but might have refresh token
      const newToken = await authClient.refreshAccessToken();
      if (newToken) {
        setUser(authClient.getUser());
      }
    };

    initAuth();
  }, []);

  const signIn = async (credentials: LoginCredentials): Promise<AuthResponse> => {
    setIsLoading(true);
    try {
      const result = await authClient.login(credentials);
      setUser(result.user);
      return result;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signUp = async (data: SignupData): Promise<AuthResponse> => {
    setIsLoading(true);
    try {
      const result = await authClient.signup(data);
      setUser(result.user);
      return result;
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signOut = async (): Promise<void> => {
    setIsLoading(true);
    try {
      await authClient.logout();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    signIn,
    signOut,
    signUp,
    isLoading,
    isAuthenticated: authClient.isAuthenticated(),
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
