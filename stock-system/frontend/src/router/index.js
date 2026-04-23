import {createRouter,createWebHistory} from 'vue-router'

import Login from '../pages/Login.vue'
import Products from '../pages/Products.vue'
const routes=[
    {
        path:'/',
        component:Login
    },
    {
        path:'/products',
        component:Products
    }
]
const router=createRouter({
    history:createWebHistory(),
    routes
})

router.beforeEach((to,from,next)=>{
    const user=localStorage.getItem('user')
    if(to.path!=='/' && !user) {
        next('/')
    } else {
        next()
    }
})
export default router  