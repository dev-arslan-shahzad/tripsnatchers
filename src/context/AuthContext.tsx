import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authApi, type RegisterData } from '../api/auth';
import { toast } from '@/hooks/use-toast';

interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  country: string;
  age?: number;
  gender?: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Export the hook as a named constant for Fast Refresh compatibility
const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchCurrentUser = async () => {
    try {
      const userData = await authApi.getCurrentUser();
      console.log('Current user data:', userData);
      setUser(userData);
    } catch (error) {
      console.error('Error fetching current user:', error);
      localStorage.removeItem('token');
      setUser(null);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log('Initial auth check - token exists:', !!token);
    
    if (token) {
      fetchCurrentUser().finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      console.log('Attempting login for:', email);
      const response = await authApi.login({ username: email, password });
      console.log('Login response:', response);
      
      localStorage.setItem('token', response.access_token);
      await fetchCurrentUser();
    } catch (error: any) {
      console.error('Login error:', error);
      if (error.response?.status === 403 && error.response?.data?.detail?.message === "Email not verified") {
        throw new Error("Please verify your email before logging in.");
      }
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      console.log('Attempting registration for:', userData.email);
      await authApi.register(userData);
      console.log('Registration successful');
      return;
    } catch (error: any) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    console.log('Logging out...');
    localStorage.removeItem('token');
    setUser(null);
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    });
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {loading ? (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : (
        children
      )}
    </AuthContext.Provider>
  );
};

// Export both the hook and provider as named exports
export { useAuth, AuthProvider };