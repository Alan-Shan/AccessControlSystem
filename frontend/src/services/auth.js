import axios from 'axios';
import store from "@/store";
import jwt_decode from "jwt-decode";
import api from "@/services/api";

const AUTH_URL = process.env.VUE_APP_AUTH_URL

// axios instance with interceptors
const instance = axios.create({
    baseURL: AUTH_URL,
});

instance.interceptors.response.use(
    response => response,
    async error => {
        if (error.response && error.response.status === 401) {
            // dispatch logout
            console.debug('401 error on auth interceptor');
            // await store.dispatch('auth/logout');
        }
    }
)

class AuthService {
    login(user) {
        return axios.post(instance.getUri() + '/login', {
            username: user.username,
            password: user.password
        }).then(async response => {
            console.debug(response);
            if (response && response.data.access_token) {
                const newUser = {
                    accessToken: response.data.access_token,
                    username: jwt_decode(response.data.access_token).sub,
                    role: (await api.whoAmI(response.data.access_token)).data.role
                };
                localStorage.setItem('user', JSON.stringify(newUser));
                // this.$cookies.set('refreshToken', response.data.refreshToken); todo
                return Promise.resolve(newUser);
            }
            return Promise.reject(response)
        }).catch(async error => {
            return Promise.reject(error.response);
            }
        );
    }

    logout() {
        console.debug('invalidating token');
        if (store.state.auth.user) {
            const accessToken = store.state.auth.user.accessToken;
            if (accessToken) {
                instance.delete('/logout', {
                    headers: {
                        Authorization: 'Bearer ' + accessToken
                    }
                }).then(r => {
                    console.debug(r);
                }) // TODO
            }
        }
        localStorage.removeItem('user');
    }

    refreshToken() {
        return instance.post('/refresh').then(response => {
            if (response.status === 200 && response.data.accessToken) {
                localStorage.setItem('user', JSON.stringify({
                    accessToken: response.data.accessToken,
                    username: response.data.identity,
                    role: store.state.auth.status.role
                }));
                this.$cookies.set('refreshToken', response.data.refreshToken);
            }
            return response.data;
        });
    }
}

export default new AuthService();