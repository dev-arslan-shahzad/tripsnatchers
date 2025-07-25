import client from './client';

export interface LoginCredentials {
  username: string;  // Using username as email for FastAPI OAuth form
  password: string;
}

export interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  country: string;
  password: string;
  age?: number;
  gender?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    const response = await client.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },

  register: async (data: RegisterData) => {
    const response = await client.post('/auth/register', data);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await client.get('/users/me');
    return response.data;
  },

  verifyEmail: async (token: string) => {
    const response = await client.get(`/auth/verify-email/${token}`);
    return response.data;
  },

  resendVerification: async (email: string) => {
    const response = await client.post('/auth/resend-verification', { email });
    return response.data;
  }
}; 