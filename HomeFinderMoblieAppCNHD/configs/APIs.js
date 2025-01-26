import axios from "axios";

const BASE_URL = 'https://hatien.pythonanywhere.com/';

export const endpoints = {
    
}

export const authApis = (token) => {
    return axios.create({
        baseURL: BASE_URL,
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
}

export default axios.create({
    baseURL: BASE_URL
});