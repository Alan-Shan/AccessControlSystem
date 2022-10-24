import axios from 'axios';
import store from "@/store";

const API_URL = process.env.VUE_APP_API_URL

// axios instance with interceptors
const instance = axios.create({
    baseURL: API_URL
});

instance.interceptors.request.use(function (config) {
    console.log('locale')
    // add token to request header
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.accessToken) {
        config.headers.Authorization = 'Bearer ' + user.accessToken;
    }
    return config;
});

instance.interceptors.response.use(
    response => response,
    async error => {
        if (error.response.status === 401) {
            store.dispatch('auth/refreshToken').then(() => {
                // retry request
                return instance.request(error.config);
            }).catch(() => {
                // dispatch logout
                store.dispatch('auth/logout').then(() => {
                    // redirect to login page
                    window.location.href = '/login';
                });
            });
        }
    });

class ApiService {
    postApplication(application) {
        return instance.post('/add_request', application);
    }
    getRequests() {
        return instance.get('/get_visit_requests');
    }
    getApprovedRequests() {
        return instance.get( '/get_approved_requests');
    }
    getDeniedRequests() {
        return instance.get( '/get_not_approved_requests');
    }
    getRequest(id) {
        return instance.get('/get_request/' + id);
    }
    approveRequest(id) {
        return instance.post('/approve_request/' + id);
    }
    rejectRequest(id) {
        return instance.post('/reject_request/' + id);
    }
}

export default new ApiService();