import instance from './axios';

export const apiListListings = async (params = {}) => {
  const { data } = await instance.get('/api/listings/', { params });
  return data;
};

export const apiCreateListing = async (payload) => {
  const { data } = await instance.post('/api/listings/', payload);
  return data;
};

export const apiGetListing = async (id) => {
  const { data } = await instance.get(`/api/listings/${id}/`);
  return data;
};

export const apiUpdateListing = async (id, payload) => {
  const { data } = await instance.patch(`/api/listings/${id}/`, payload);
  return data;
};

export const apiDeleteListing = async (id) => {
  const { data } = await instance.delete(`/api/listings/${id}/`);
  return data;
};
