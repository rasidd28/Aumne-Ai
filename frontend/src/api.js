import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      'An unexpected network error occurred.';
    return Promise.reject(new Error(message));
  }
);

export async function createPost(title, content) {
  const response = await client.post('/posts/', { title, content });
  return response.data;
}

export async function submitPost(postId) {
  const response = await client.post(`/posts/${postId}/submit/`);
  return response.data;
}

export async function fetchPosts(status = null) {
  const params = status ? { status } : {};
  const response = await client.get('/posts/', { params });
  return response.data;
}

export async function publishPost(postId) {
  const response = await client.patch(`/posts/${postId}/publish/`);
  return response.data;
}

export async function fetchPost(postId) {
  const response = await client.get(`/posts/${postId}`);
  return response.data;
}

export default client;
