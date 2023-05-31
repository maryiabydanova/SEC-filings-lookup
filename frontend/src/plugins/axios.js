import axios from 'axios'
const apiURL = import.meta.env.VITE_BASE_URL
const instance = axios.create({
  baseURL: apiURL,
  timeout:  60000, // default timeout is 10 seconds
  headers:  { 'Content-Type': 'application/json' }, // optional headers object
});

instance.interceptors.response.use(function (response) {
  // Any status code that lie within the range of 2xx cause this function to trigger
  // Do something with response data
  return response.data; // do like this
}, function (error) {
  // Any status codes that falls outside the range of 2xx cause this function to trigger
  // Do something with response error
  return Promise.reject(error);
});

export default instance;