import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();
const API = 'http://127.0.0.1:8000/api/v1';

export function AuthProvider({ children }) {
  const [user, setUser]   = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('fs_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios.get(`${API}/auth/me`)
        .then(r => setUser(r.data))
        .catch(() => { clearAuth(); })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const clearAuth = () => {
    localStorage.removeItem('fs_token');
    delete axios.defaults.headers.common['Authorization'];
    setToken(null);
    setUser(null);
  };

  const login = async (email, password) => {
    const form = new URLSearchParams({ username: email, password });
    const { data } = await axios.post(`${API}/auth/login`, form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    localStorage.setItem('fs_token', data.access_token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`;
    setToken(data.access_token);
    const me = await axios.get(`${API}/auth/me`);
    setUser(me.data);
    return me.data;
  };

  const register = async (username, email, password) => {
    const { data } = await axios.post(`${API}/auth/register`, { username, email, password });
    return data;
  };

  const logout = () => clearAuth();

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
export const API_BASE = API;
