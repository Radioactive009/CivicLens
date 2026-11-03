import { create } from 'zustand';
import api from '../services/api';

export const useAuthStore = create((set, get) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  token: localStorage.getItem('access_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,

  login: async (username, password) => {
    set({ loading: true, error: null });
    try {
      const res = await api.post('/auth/login/', { username, password });
      const { access, refresh } = res.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      // Fetch user profile
      const profileRes = await api.get('/auth/profile/');
      const user = profileRes.data;
      localStorage.setItem('user', JSON.stringify(user));

      set({ token: access, user, isAuthenticated: true, loading: false });
      return { success: true };
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Invalid username or password';
      set({ error: errorMsg, loading: false });
      return { success: false, error: errorMsg };
    }
  },

  register: async (formData) => {
    set({ loading: true, error: null });
    try {
      const res = await api.post('/auth/register/', formData);
      const { user, tokens } = res.data;
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      localStorage.setItem('user', JSON.stringify(user));

      set({ token: tokens.access, user, isAuthenticated: true, loading: false });
      return { success: true };
    } catch (err) {
      const errorMsg = err.response?.data ? Object.values(err.response.data).flat().join(' ') : 'Registration failed';
      set({ error: errorMsg, loading: false });
      return { success: false, error: errorMsg };
    }
  },

  logout: () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      api.post('/auth/logout/', { refresh: refreshToken }).catch(() => {});
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    set({ token: null, user: null, isAuthenticated: false });
  },

  updateProfile: async (data) => {
    try {
      const res = await api.patch('/auth/profile/', data);
      localStorage.setItem('user', JSON.stringify(res.data));
      set({ user: res.data });
      return { success: true };
    } catch (err) {
      return { success: false, error: err.response?.data };
    }
  }
}));

