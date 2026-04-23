import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)   // 👉 必须在 mount 前
app.mount('#app')