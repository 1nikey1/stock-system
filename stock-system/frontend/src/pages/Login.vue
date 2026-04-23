<template>
    <div class="login-container">
        <h2>库存系统登录</h2>
        <input v-model="username" placeholder="请输入账号">
        <input v-model="password" type="password" placeholder="请输入密码">
        <button @click="login">登录</button>

    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            if(!this.username || !this.password) {
                alert('请输入账号和密码')
                return
            }
            axios.post('http://localhost:5000/api/login', {
                username: this.username,
                password: this.password
            }).then(res=>{
                if(res.data.success) {
                    alert('登录成功')
                    // 可以在这里进行页面跳转或者保存登录状态
                    localStorage.setItem('user',this.username)
                    this.$router.push('/products')
                } else {
                    alert('登录失败：' + res.data.message)
                }
            }).catch(err => {
                console.error('登录请求失败:', err)
                alert('登录请求失败，请稍后再试')
            })}}}
</script>

<style>
.login-container{
    width:300px;
    margin:150px,auto;
    text-align: center;
}
input{
    display: block;
    width:100%;
    margin:10px 0;
    padding:8px;
}
button{
    width:100%;
    padding:10px;
}
</style>