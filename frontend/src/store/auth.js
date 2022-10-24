import AuthService from '../services/auth';
import jwt_decode from "jwt-decode";


const user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? {
    status: {loggedIn: true, role: user.role},
    user: user
} : {status: {loggedIn: false, role: null}, user: null};
validateInitialState();

function validateInitialState() {
    console.debug("Store Initial State: ", initialState);
    // initialState.status.role = 'superadmin';
    // initialState.user = {username: 'superadmin'};
    // todo-do
    if (initialState.user && initialState.user.accessToken) {
        // decode jwt and check if token expired
        const decoded = jwt_decode(initialState.user.accessToken);
        const currentTime = Date.now() / 1000;
        if (decoded.exp < currentTime) {
            // check for refresh token with vue-cookies
            const refreshToken = this.$cookies.get('refreshToken');
            if (refreshToken) {
                this.$store.dispatch('auth/refreshToken');
            }
        }
    }
    return user;
}


export const auth = {
    namespaced: true,
    state: initialState,
    actions: {
        login({commit}, user) {
            return AuthService.login(user).then(
                loggedInUser => {
                    commit('loginSuccess', loggedInUser);
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            );
        },
        refreshToken({commit}) {
            return AuthService.refreshToken().then(
                user => {
                    commit('loginSuccess', user);
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            );
        },
        logout({commit}) {
            console.log('store logout called');
            AuthService.logout();
            commit('logout');
            // this.$cookies.remove('refreshToken');
            //todo-do
            return Promise.resolve();
        }
    },
    mutations: {
        loginSuccess(state, user) {
            console.debug('store state loginSuccess: ', state);
            state.status.loggedIn = true;
            state.status.role = user.role;
            state.user = user;
        },
        loginFailure(state) {
            console.debug('store state loginFailure: ', state);
            state.status.loggedIn = false;
            state.status.role = null;
            state.status.role = null;
            state.user = null;
        },
        logout(state) {
            console.debug('store state logout: ', state);
            state.status.loggedIn = false;
            state.status.role = null;
            state.user = null;
        }
    },
    getters: {
        getCurrentUsername: state => {
            return state.user ? state.user.username : '';
        },
        getCurrentRole: state => {
            return state.status.role ? state.status.role : '';
        },
        hasPrivilegedAccess: state => {
            return state.status.role ?
                (state.status.role === 'admin' || state.status.role === 'superadmin') : false;
        },
        isSuperAdmin: state => {
            return state.status.role ? state.status.role === 'superadmin' : false;
        }
    }
};