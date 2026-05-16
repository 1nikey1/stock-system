import {createRouter,createWebHistory} from 'vue-router'

import Login from '../pages/Login.vue'
import Products from '../pages/Products.vue'
import StockRecords from '../pages/StockRecords.vue'
const routes=[
    {
        path:'/',
        component:Login
    },
    {
        path:'/products',
        component:Products
    },
    {
        path:'/stock-records',
        component:StockRecords
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