import axios from 'axios'

const axiosPlugin = {
    install: (app, options) => {
        const instance = axios.create({
          baseURL: 'http://127.0.0.1:8000/',
          timeout: options?.timeout || 10000, // default timeout is 10 seconds
          headers: options?.headers || {}, // optional headers object
        });
    
        app.config.globalProperties.$axios = instance;
    },
}

export default axiosPlugin;