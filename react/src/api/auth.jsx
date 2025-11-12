import instance from './axios';

export const apiRegister = async (payload) => {
  const { data } = await instance.post('/api/auth/register/', payload);
  return data;
};

export const apiLogin = async (payload) => {
  const { data } = await instance.post('/api/auth/login/', payload);
  return data; // { token, member }
};
