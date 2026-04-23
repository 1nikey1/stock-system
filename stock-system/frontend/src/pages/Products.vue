<template>  
  <div class="container">
    <h2>商品列表</h2>
    <div class="search-box">
      <input v-model="keyword" placeholder="输入商品名称搜索"/>
      <button @click="fetchProducts">搜索</button>
      <button @click="logout">退出登录</button>
    </div>

    <div v-if="editing">
      <h3>编辑商品</h3>

      <p>名称：</p><input v-model="form.name" placeholder="名称"/>
      <p>库存：</p><input v-model="form.stock" placeholder="库存"/>
      <p>成本价：</p><input v-model="form.cost_price" placeholder="成本价"/>
      <p>售价：</p><input v-model="form.sell_price" placeholder="售价"/>

      <button @click="updateProduct">保存</button>
      <button @click="cancelEdit">取消</button>
      <hr>
    </div>

    <div v-if="showAdd">
      <h3>新增商品</h3>

      <p>名称：</p><input v-model="newForm.name"/>
      <p>库存：</p><input v-model="newForm.stock"/>
      <p>成本价：</p><input v-model="newForm.cost_price"/>
      <p>售价：</p><input v-model="newForm.sell_price"/>

      <button @click="addProduct">提交</button>
      <button @click="cancelAdd">取消</button>
      <hr>
    </div>
    <table border="1" width="100%">
      <thead>
        <tr>
          <th>ID</th>
          <th>名称</th>
          <th>库存</th>
          <th>成本价</th>
          <th>售价</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in goodsList" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.stock }}</td>
          <td>{{ item.cost_price }}</td>
          <td>{{ item.sell_price }}</td>
          <td>
            <button @click="editProduct(item)">编辑</button>
            <button @click="deleteProduct(item.id)">删除</button>
          </td>
        </tr>

        <tr v-if="goodsList.length===0">
          <td colspan="6">暂无数据</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      goodsList: [],
      keyword: '',

      editing: false,
      form: {
        id: null,
        name: '',
        stock: '',
        cost_price: '',
        sell_price: ''
      },

      showAdd:false,
      newForm:{
        name:'',
        stock:'',
        cost_price:'',
        sell_price:''
      }
    }
  },

  mounted() {
    this.fetchProducts()
  },

  methods: {

    // 获取商品
    fetchProducts() {
      axios.get('http://localhost:5000/api/products', {
        params: { keyword: this.keyword }
      }).then(res => {
        this.goodsList = res.data
      }).catch(err => {
        console.error('获取商品失败:', err)
        alert('获取商品失败')
      })
    },

    // 删除
    deleteProduct(id) {
      if (!confirm('确定删除吗？')) return

      axios.delete(`http://localhost:5000/api/products/${id}`)
        .then(() => {
          alert('删除成功')
          this.fetchProducts()
        })
        .catch(err => {
          console.error(err)
          alert('删除失败')
        })
    },

    // 编辑
    editProduct(item) {
      this.editing = true
      this.form = {
        id: item.id,
        name: item.name,
        stock: item.stock,
        cost_price: item.cost_price,
        sell_price: item.sell_price
      }
    },

    cancelEdit() {
      this.editing = false
    },

    // 更新
    updateProduct() {
      axios.put(`http://localhost:5000/api/products/${this.form.id}`, this.form)
        .then(() => {
          alert('修改成功')
          this.editing = false
          this.fetchProducts()
        })
        .catch(err => {
          console.error(err)
          alert('修改失败')
        })
    },

    logout() {
      localStorage.removeItem('user')
      this.$router.push('/')
    },

    addProduct(){
      if(!this.newForm.name){
        alert('请输入商品名称')
        return
      }
      axios.post('http://localhost:5000/api/products', this.newForm)
        .then(()=>{
          alert('新增成功')
          this.showAdd=false

          this.newForm={
            name:'',
            stock:'',
            cost_price:'',
            sell_price:''
          }
          this.fetchProducts()
        })
        .catch(err=>{
          console.error(err)
          alert('新增失败')
        })
    },
    cancelAdd(){
      this.showAdd=false
    }
  }
}
</script>
<style>
.container{
  width:800px;
  margin:50px auto;
}
.search-box{
  margin-bottom:20px;
}
input{
  padding:5px;
  margin-right: 10px;
}
button{
  margin-right:10px;
  padding:5px 10px;
}
</style>