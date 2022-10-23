import {createRouter, createWebHistory} from "vue-router";

const routes = [

];

const router = createRouter({
    history: createWebHistory(),
    routes
})

// check if logged in for private pages on each request
router.beforeEach((to, from, next) => {
    const publicPages = [''];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = true //localStorage.getItem('user'); TODO: implement this


    if (authRequired && !loggedIn) {
        next('/login');
    } else {
        next();
    }
});

export default router;