import { createWebHistory, createRouter} from "vue-router";
import Home from "../views/Home.vue";
import Profile from "../views/Profile.vue";
import Signup from "../views/Signup.vue";
import Questions from "../views/Questions.vue";
import PageNotFound from "../views/PageNotFound.vue";
import Join from "../views/Join.vue";
import Ban from "../views/Ban.vue";

const routes = [
    { path: "/", name: "home", component: Home },
    { path: "/profile", name: "profile", component: Profile },
    { path: "/signup", name: "signup", component: Signup },
    { path: "/questions", name: "questions", component: Questions },
    { path: "/join", name: "join", component: Join },
    { path: "/banned", name: "banned", component: Ban },
    { path: "/:pathMatch(.*)*", name: 'notFound', component: PageNotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router