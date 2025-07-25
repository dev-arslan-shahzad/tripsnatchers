import axios from "axios";

// In development, use the proxy path
const isDev = import.meta.env.DEV;
const API_URL = isDev ? '/api' : import.meta.env.VITE_API_URL || "http://localhost:8000";

console.log('API URL:', API_URL);

const client = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  withCredentials: true, // Required for cookies/session
});

// Request interceptor to add auth token
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Don't modify content-type if it's FormData
  if (!(config.data instanceof FormData)) {
    config.headers['Content-Type'] = 'application/json';
  }
  
  // Log request details
  console.log('Request:', {
    url: config.url,
    method: config.method,
    headers: config.headers,
    data: config.data
  });
  return config;
}, (error) => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

// Response interceptor for error handling
client.interceptors.response.use(
  (response) => {
    console.log('Response:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    });
    return response;
  },
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      stack: error.stack
    });
    
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      // Only redirect if we're not already on the login page
      if (!window.location.pathname.includes('/login')) {
        window.location.href = "/login";
      }
    }
    
    // Enhance error object with response data
    if (error.response?.data) {
      error.message = error.response.data.detail || error.message;
    }
    
    return Promise.reject(error);
  }
);

export default client;