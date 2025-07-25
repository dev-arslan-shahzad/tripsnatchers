import client from './client';

export interface SnatchedDeal {
  id: number;
  user_id: number;
  holiday_url: string;
  initial_price: number;
  target_price: number;
  snatched_price: number;
  date_tracked: string;
  date_snatched: string;
}

export const snatchedApi = {
  // Get all snatched deals for current user
  getAllSnatched: async (): Promise<SnatchedDeal[]> => {
    const response = await client.get('/snatched/deals');
    return response.data;
  },

  // Get details of a specific snatched deal
  getSnatchedDeal: async (id: number): Promise<SnatchedDeal> => {
    const response = await client.get(`/snatched/deals/${id}`);
    return response.data;
  }
}; 