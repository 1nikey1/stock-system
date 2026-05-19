<template>
  <div class="login-page">

    <div class="login-card">

      <h1 class="title">
        别问不是好东西
      </h1>


      <el-input
        v-model="username"
        placeholder="请输入账号"
        size="large"
      />

      <el-input
        v-model="password"
        type="password"
        placeholder="请输入密码"
        size="large"
        show-password
      />

      <el-button
        type="primary"
        size="large"
        class="login-btn"
        @click="login"
      >
        登录系统
      </el-button>

    </div>

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
                    //保存token
                    localStorage.setItem(
                        'token',res.data.token
                    )
                    //保存用户名
                    localStorage.setItem(
                        'username',this.username
                    )
                    alert('登录成功')
                    //跳转到库存页面
                    this.$router.push('/products')
                } else {
                    alert('登录失败：' + res.data.message)
                }
            }).catch(err => {
                console.error('登录请求失败:', err)
                alert('登录请求失败，请稍后再试')
            })}}}
</script>

<style scoped>

.login-page{

    width:100vw;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    background:
    linear-gradient(
        135deg,
        #1677ff,
        #722ed1
    );
}

.login-card{

    width:380px;

    padding:40px;

    border-radius:20px;

    background:rgba(255,255,255,.95);

    box-shadow:
    0 10px 40px rgba(0,0,0,.2);

    display:flex;
    flex-direction:column;

    gap:20px;
}

.title{

    text-align:center;

    font-size:30px;

    font-weight:bold;

    color:#333;

    margin:0;
}

.sub-title{

    text-align:center;

    color:#888;

    margin-top:-10px;
}

.login-btn{

    width:100%;
}

</style>