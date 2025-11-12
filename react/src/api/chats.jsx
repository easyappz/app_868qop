import instance from './axios';

export const apiStartChat = async (payload) => {
  const { data } = await instance.post('/api/chats/start/', payload);
  return data;
};

export const apiListChats = async () => {
  const { data } = await instance.get('/api/chats/');
  return data;
};

export const apiListMessages = async (threadId) => {
  const { data } = await instance.get(`/api/chats/${threadId}/messages/`);
  return data;
};

export const apiSendMessage = async (threadId, content) => {
  const { data } = await instance.post(`/api/chats/${threadId}/messages/`, { content });
  return data;
};
