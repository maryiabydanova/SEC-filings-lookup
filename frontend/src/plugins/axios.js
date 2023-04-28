import axios from 'axios'

const axiosPlugin = {
    install: (app, options) => {
        const instance = axios.create({
          baseURL: 'http://127.0.0.1:8000/',
          timeout: options?.timeout || 10000, // default timeout is 10 seconds
          headers: options?.headers || { 'Content-Type': 'application/json' }, // optional headers object
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
        app.config.globalProperties.$axios = instance;
    },
}

export default axiosPlugin;