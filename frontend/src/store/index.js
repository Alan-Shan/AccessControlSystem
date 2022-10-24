import { createStore } from "vuex";
import {auth} from "@/store/auth";

// Main Vuex store for the application
const store = createStore({
    modules: {
        auth
    },
});

export default store;