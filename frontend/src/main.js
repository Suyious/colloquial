import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
