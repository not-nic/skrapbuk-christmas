import {createApp, markRaw} from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

const pinia = createPinia()

// allow vue-router to be used in pinia store.
pinia.use(({ store }) => {
    store.$router = markRaw(router)
})

createApp(App).use(router).use(pinia).mount('#app')
