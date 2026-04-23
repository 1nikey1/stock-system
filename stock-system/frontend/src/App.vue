<!--<script setup>-->
<!--import HelloWorld from './components/HelloWorld.vue'-->
<!--</script>-->

<template>
  <router-view/>
</template>
  <!-- <div class="layout">
    <aside class="sidebar">
      <h2>库存系统</h2>
      <ul>
        <li @click="current='products'">商品</li>
        <li @click="current='apply'">申请</li>
        <li @click="current='admin'">审核</li>
      </ul>
    </aside>
    <main class="content">
      <Products v-if="current==='products'"/>
      <Apply v-if="current==='apply'"/>
      <Admin v-if="current==='admin'"/>
    </main>
  </div>
</template>
<script>
import Products from './pages/Products.vue'
import Apply from './pages/Apply.vue'
import Admin from './pages/Admin.vue'
export default {
  components:{Products,Apply,Admin},
  data(){
    return{
      current:'products'
    }
  }
}

</script>
<style>
.layout{
  display: flex;
  height: 100vh;
}
.sidebar{
  width: 200px;
  background: #2c3e50;
  color: white;
  padding: 20px;
}
.sidebar li{
  cursor: pointer;
  margin: 10px 0;
}
.content{
  flex: 1;
  padding: 20px;
}
</style> -->