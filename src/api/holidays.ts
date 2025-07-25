import client from './client';

export interface HolidayTrack {
  id: number;
  url: string;
  target_price: number;
  current_price: number;
  is_active: boolean;
  created_at: string;
  user_id: number;
}

export interface CreateHolidayTrack {
  url: string;
  target_price: number;
  current_price?: number;
}

export const holidayApi = {
  // Get all tracked holidays for current user
  getAllTracked: async (): Promise<HolidayTrack[]> => {
    const response = await client.get('/holidays/my-trips');
    return response.data;
  },

  // Start tracking a new holiday
  startTracking: async (data: CreateHolidayTrack): Promise<HolidayTrack> => {
    const response = await client.post('/holidays/track', data);
    return response.data;
  },

  // Stop tracking a holiday
  stopTracking: async (id: number): Promise<void> => {
    await client.delete(`/holidays/tracked/${id}`);
  },

  // Update target price for a tracked holiday
  updateTargetPrice: async (id: number, target_price: number): Promise<HolidayTrack> => {
    const response = await client.patch(`/holidays/tracked/${id}`, { target_price });
    return response.data;
  },

  // Update current price for a tracked holiday
  updateCurrentPrice: async (id: number, current_price: number): Promise<HolidayTrack> => {
    const response = await client.post(`/holidays/update-price/${id}`, { current_price });
    return response.data;
  }
}; 