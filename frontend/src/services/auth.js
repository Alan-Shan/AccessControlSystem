import axios from 'axios';
import store from "@/store";

const AUTH_URL = process.env.VUE_APP_AUTH_URL

// axios instance with interceptors
const instance = axios.create({
    baseURL: AUTH_URL,
});

instance.interceptors.response.use(
    response => response,
    async error => {
        // dispatch async store action to logout
        store.dispatch('auth/logout').then(() => {
            // redirect to login page
            window.location.href = '/login';
        });
        if (error.response.status === 401) {
            // dispatch logout
            await store.dispatch('auth/logout');
        }
    }
)

class AuthService {
    login(user) {
        return instance.post('/login', {
            username: user.username,
            password: user.password
        })
            .then(response => {
                if (response.data.accessToken) {
                    localStorage.setItem('user', JSON.stringify({
                        accessToken: response.data.accessToken,
                        username: response.data.identity,
                        role: this.whoami().then(response => {
                            return response.data.role;
                        }).catch(error => {
                            console.log(error);
                            return null;
                        })
                    }));
                }

                return response.data;
            });
    }

    logout() {
        localStorage.removeItem('user');
        instance.delete('/logout').then(r => {
            console.debug(r);
        }) // TODO
    }

    refreshToken() {
        return instance.post('/refresh').then(response => {
            if (response.data.accessToken) {
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

    whoami() {
        return instance.get('/who_ami');
    }
}

export default new AuthService();