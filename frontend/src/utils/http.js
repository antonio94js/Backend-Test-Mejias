import axios from 'axios';

const createAxiosInstance = (baseURL = 'http://localhost:8000') => {
  let instance = axios.create({
    baseURL,
    timeout: 60000,
  });

  return instance;
};

export const http = createAxiosInstance();

