import client from './client';

export interface UserUpdateData {
  first_name?: string;
  last_name?: string;
  phone?: string;
  country?: string;
  age?: number;
  gender?: string;
}

export const usersApi = {
  // Get current user's profile
  getCurrentUser: async () => {
    const response = await client.get('/users/me');
    return response.data;
  },

  // Update current user's profile
  updateProfile: async (data: UserUpdateData) => {
    const response = await client.patch('/users/me', data);
    return response.data;
  },

  // Get user's statistics
  getUserStats: async () => {
    const response = await client.get('/users/me/stats');
    return response.data;
  }
}; 