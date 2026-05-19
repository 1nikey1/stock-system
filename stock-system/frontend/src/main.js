import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios
 from 'axios'

//后端地址
axios.defaults.baseURL='http://127.0.0.1:5000'

//请求拦截器，自动添加token
axios.interceptors.request.use(config=>{
    //获取token
    const token=localStorage.getItem('token')
    //自动携带token
    if(token) {
        config.headers.Authorization=token}
        return config
})
axios.interceptors.response.use(

    response=>response,
    error=>{
        //token失效
        if(error.response?.status===401){
            localStorage.removeItem('token')
            router.push('/')
            alert('登录状态已过期，请重新登录')
        }
        return Promise.reject(error)
    }
)

const app = createApp(App)

app.use(router)   // 👉 必须在 mount 前
app.use(ElementPlus)   // 👉 必须在 mount 前
app.mount('#app')