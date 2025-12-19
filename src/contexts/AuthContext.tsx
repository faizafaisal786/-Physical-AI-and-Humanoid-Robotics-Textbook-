import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useAuth as useBetterAuth } from 'better-auth/react';

interface AuthContextType {
  user: any;
  signIn: (provider?: string) => Promise<void>;
  signOut: () => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  isLoading: boolean;
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
  const { 
    session, 
    signIn: betterSignIn, 
    signOut: betterSignOut, 
    signUp: betterSignUp,
    isLoading 
  } = useAuthHook();

  const signIn = async (provider?: string) => {
    if (provider) {
      await betterSignIn.social({
        provider,
        callbackURL: '/',
      });
    } else {
      // For email/password sign in, you'd handle differently
      console.log("Email/password sign in not implemented in this example");
    }
  };

  const signOut = async () => {
    await betterSignOut();
  };

  const signUp = async (email: string, password: string, name: string) => {
    await betterSignUp.email({
      email,
      password,
      name,
      callbackURL: '/dashboard', // Redirect after signup
    });
  };

  const value = {
    user: session?.user,
    signIn,
    signOut,
    signUp,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to manage auth state
const useAuthHook = () => {
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check session on component mount
    const fetchSession = async () => {
      try {
        const response = await fetch('/api/auth/session');
        const data = await response.json();
        setSession(data.session || null);
      } catch (error) {
        console.error('Error fetching session:', error);
        setSession(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSession();

    // Listen for session changes
    const handleStorageChange = () => {
      fetchSession();
    };

    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const signIn = {
    social: async ({ provider, callbackURL }: { provider: string; callbackURL: string }) => {
      if (provider === 'google') {
        window.location.href = `/api/auth/social/google?callbackURL=${encodeURIComponent(callbackURL)}`;
      } else if (provider === 'github') {
        window.location.href = `/api/auth/social/github?callbackURL=${encodeURIComponent(callbackURL)}`;
      }
    },
    email: async ({ email, password, callbackURL }: { email: string; password: string; callbackURL: string }) => {
      const response = await fetch('/api/auth/sign-in/email-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, callbackURL }),
      });
      const result = await response.json();
      if (result.session) {
        setSession(result.session);
        window.location.href = callbackURL;
      }
      return result;
    }
  };

  const signUp = {
    email: async ({ email, password, name, callbackURL }: { email: string; password: string; name: string; callbackURL: string }) => {
      const response = await fetch('/api/auth/sign-up/email-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name, callbackURL }),
      });
      const result = await response.json();
      if (result.session) {
        setSession(result.session);
        window.location.href = callbackURL;
      }
      return result;
    }
  };

  const signOut = async () => {
    const response = await fetch('/api/auth/sign-out', {
      method: 'POST',
    });
    const result = await response.json();
    setSession(null);
    window.location.reload(); // Refresh the page to reflect signed-out state
    return result;
  };

  return { session, signIn, signOut, signUp, isLoading };
};