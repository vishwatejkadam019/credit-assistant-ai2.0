import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/auth/login', formData);
  },
  register: (name, email, password) => 
    api.post('/auth/register', { name, email, password }),
};

export const financialAPI = {
  getFinancialData: () => api.get('/financial/current'),
  saveFinancialData: (data) => api.post('/financial/', data),
  getHistory: () => api.get('/financial/history'),
  getUtilization: () => api.get('/financial/utilization'),
};

export const aiAPI = {
  getAdvice: () => api.post('/ai-advice/'),
  getLatestAdvice: () => api.get('/ai-advice/latest'),
};

export default api;