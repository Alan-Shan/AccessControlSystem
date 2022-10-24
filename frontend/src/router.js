import {createRouter, createWebHistory} from "vue-router";
import store from "@/store";

const routes = [
    // public home page
    {
        path: "/",
        name: "Main",
        component: () => import("./components/HelloWorld.vue"),
    },
    // admin dashboard
    {
        path: "/home",
        name: "Home",
        component: () => import("./components/AdminHome.vue"),

    },
    // public application form
    {
        path: "/applyForVisit",
        name: "ApplyForVisit",
        component: () => import("./components/ApplyForVisit.vue")
    },
    // public login page
    {
        path: "/login",
        name: "Login",
        component: () => import("./components/LoginForm.vue")
    },
    // admin dashboard requests list page
    {
        path: "/requestsList",
        name: "RequestsList",
        component: () => import("./components/RequestsList.vue")
    },
    {
        path: "/singleRequest/:id",
        name: "SingleRequest",
        component: () => import("./components/SingleRequest.vue")
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

// check if logged in for private pages on each request
router.beforeEach((to, from, next) => {
    const publicPages = ['Main', 'ApplyForVisit', 'Login'];
    const authRequired = !publicPages.includes(to.name);
    const loggedIn = store.getters['auth/hasPrivilegedAccess'] //localStorage.getItem('user'); TODO: implement this

    if (authRequired && !loggedIn) {
        next('/login');
    } else {
        if (to.name === 'Login' && loggedIn) {
            next('/home');
        }
        next();
    }
});

export default router;