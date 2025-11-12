import instance from './axios';

export const apiGetMe = async () => {
  const { data } = await instance.get('/api/me/');
  return data;
};

export const apiUpdateMe = async (payload) => {
  const { data } = await instance.patch('/api/me/', payload);
  return data;
};
