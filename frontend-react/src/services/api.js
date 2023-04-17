import axios from 'axios';
import {authStore} from "../store/auth";

const API_URL = process.env.REACT_APP_API_URL

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
            authStore.refreshToken().then(() => {
                // retry request
                return instance.request(error.config);
            }).catch(() => {
                // dispatch logout
                authStore.logout()
                window.location.href = '/login';
            });
        }
        return Promise.reject(error);
    });

class ApiService {
    postApplication(application) {
        return instance.post('/add_request', application);
    }

    getRequests() {
        return instance.get('/get_requests');
    }

    getApprovedRequests() {
        return instance.get('/get_approved_requests');
    }

    getDeniedRequests() {
        return instance.get('/get_not_approved_requests');
    }

    getRequest(id) {
        return instance.get('/get_request/' + id);
    }

    approveRequest(id) {
        return instance.post(`/approve_request/${id}`, {
        });
    }

    rejectRequest(id) {
        return instance.post('/reject_request/' + id,
            {
            });
    }

    modifyRequest(application) {
        return instance.post('/modify_request', application);
    }

    deleteRequest(id) {
        return instance.delete('/delete_request/' + id);
    }

    addAdmin(admin) {
        return instance.post('/add_admin', admin);
    }

    getAdmins() {
        return instance.get('/get_admins');
    }

    getAdmin(id) {
        return instance.get('/get_admin/' + id);
    }

    modifyAdmin(admin) {
        return instance.post('/modify_admin/', admin);
    }

    deleteAdmin(id) {
        return instance.delete('/delete_admin/' + id);
    }


    async whoAmI(access_token) {
        return await instance.get('/who_am_i', {
            headers: {
                Authorization: 'Bearer ' + access_token
            }
        });
    }
}

export const apiService = new ApiService();