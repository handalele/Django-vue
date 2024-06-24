import axios from 'axios';

const http = axios.create({
    baseURL: 'http://localhost:8000/', // 设置基础 URL
});

export default http;