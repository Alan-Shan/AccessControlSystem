import {makeAutoObservable} from 'mobx';
import {authService} from '../services/auth';
import jwt_decode from 'jwt-decode';

class AuthStore {
    user = null;
    status = {
        loggedIn: false,
        role: null,
    };

    constructor() {
        makeAutoObservable(this);
        this.initialize();
    }

    initialize() {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user) {
            this.status.loggedIn = true;
            this.status.role = user.role;
            this.user = user;
            (async () => {
                await this.validateInitialState();
            })();
        }
    }

    async validateInitialState() {
        if (this.user && this.user.accessToken) {
            const decoded = jwt_decode(this.user.accessToken);
            const currentTime = Date.now() / 1000;
            if (decoded.exp < currentTime) {
                const refreshToken = false;
                if (refreshToken) {
                    try {
                        await this.refreshToken();
                    } catch (error) {
                        console.error('Error refreshing token:', error);
                    }
                }
            }
        }
    }

    async login(user) {
        try {
            const loggedInUser = await authService.login(user);
            this.loginSuccess(loggedInUser);
            return loggedInUser;
        } catch (error) {
            this.loginFailure();
            throw error;
        }
    }

    async refreshToken() {
        try {
            const user = await authService.refreshToken();
            this.loginSuccess(user);
            return user;
        } catch (error) {
            this.loginFailure();
            throw error;
        }
    }

    logout() {
        authService.logout();
        this.logoutSuccess();
    }

    loginSuccess(user) {
        this.status.loggedIn = true;
        this.status.role = user.role;
        this.user = user;
    }

    loginFailure() {
        this.status.loggedIn = false;
        this.status.role = null;
        this.user = null;
    }

    logoutSuccess() {
        this.status.loggedIn = false;
        this.status.role = null;
        this.user = null;
    }

    get currentUsername() {
        return this.user ? this.user.username : '';
    }

    get currentRole() {
        return this.status.role ? this.status.role : '';
    }

    get userFriendlyRoleName() {
        return this.status.role
            ? this.status.role === 'admin'
                ? 'Администратор'
                : 'Господь Бог'
            : '';
    }

    get hasPrivilegedAccess() {
        return this.status.role
            ? this.status.role === 'admin' || this.status.role === 'super_admin'
            : false;
    }

    get isSuperAdmin() {
        return this.status.role ? this.status.role === 'super_admin' : false;
    }
}

export const authStore = new AuthStore();