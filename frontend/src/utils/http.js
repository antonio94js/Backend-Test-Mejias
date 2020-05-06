import axios from 'axios';

const baseURL = 'http://localhost:8000'

const requestInterceptor = config => {
    const token = localStorage.getItem('auth-token');
    const auth = token ? `Bearer ${token} `: false;

    if (auth) {
      config.headers['Authorization'] = auth

    }
    return config;
};

let instance = axios.create({
    baseURL,
    timeout: 60000,
});

instance.interceptors.request.use(requestInterceptor);

export const http = instance;

