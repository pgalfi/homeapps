import axios from 'axios';
import {API_BASE} from "../config";

export const api_instance = axios.create({
    baseURL: API_BASE,
    timeout: 1000,
});

export const authenticate = (username, password) => {
    return api_instance.post("/api-token-auth/", {
        username: username,
        password: password
    })
};

export const change_password = (token, old_password, new_password) => {
    return api_instance.put("/user/password/", {
        old_password: old_password,
        new_password: new_password
    }, {
        headers: {
            "Authorization": "Token " + token,
        }
    });
};