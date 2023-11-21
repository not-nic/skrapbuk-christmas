import { createWebHistory, createRouter} from "vue-router";
import Home from "../views/Home.vue";
import Profile from "../views/Profile.vue";
import Signup from "../views/Signup.vue";
import Questions from "../views/Questions.vue";
import PageNotFound from "../views/PageNotFound.vue";

const routes = [
    { path: "/", name: "home", component: Home },
    { path: "/profile", name: "profile", component: Profile },
    { path: "/signup", name: "signup", component: Signup },
    { path: "/questions", name: "questions", component: Questions },
    { path: "/:pathMatch(.*)*", name: 'notFound', component: PageNotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router