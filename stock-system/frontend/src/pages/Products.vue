<template>  
  <div class="container">
    <h2>商品列表</h2>
    <div class="toolbar">
      <el-input
      v-model="keyword"
      placeholder="请输入关键词"
      style="width:220px"/>
      <br>
      <div class="btn-group">
      <el-button type="primary" @click="fetchProducts">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
      <el-button type="success" @click="openAddDialog">新增</el-button>
      <el-button type="warning" @click="exportCSV">导出</el-button>
      <el-button type="info" @click="$router.push('/stock-records')">库存记录</el-button>
      <el-button type="danger" @click="logout">退出登录</el-button>
    </div>
    </div>

    <el-table :data="goodsList" border style="width:100%">
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="name" label="商品名称"/>
      <el-table-column prop="图片" width="120">
        <template #default="scope">
          <el-image
            :src="scope.row.image"
            style="width:60px;height:60px;border-radius: 6px;"
            fit="cover"
            :preview-src-list="[scope.row.image]"
            preview-telepored/>
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存"/>
      <el-table-column prop="cost_price" label="成本价"/>
      <el-table-column prop="sell_price" label="售价"/>
      <el-table-column label="操作" width="260" align="center">
        <template #default="scope">
          <div class="action-buttons">
          <el-button type="primary" size="small" @click="editProduct(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="deleteProduct(scope.row.id)">删除</el-button>
          <el-button type="success" size="small" @clikc="openStockIn(scope.row)">入库</el-button>
          <el-button type="warning" size="small" @click="openStockOut(scope.row)">出库</el-button>
        </div></template>
      </el-table-column>
    </el-table>

     <el-dialog v-model="showAdd" title="新增商品" width="500px">
    <el-form label-width="80px">
    <el-form-item label="名称">
      <el-input v-model="newForm.name"/>
    </el-form-item>
    <el-form-item label="库存">
      <el-input v-model="newForm.stock"/>
    </el-form-item>
    <el-form-item label="成本价">
      <el-input v-model="newForm.cost_price"/>
    </el-form-item>
    <el-form-item label="售价">
      <el-input v-model="newForm.sell_price"/>
    </el-form-item>
    <el-form-item label="图片">
      <input type="file" @change="handleFile">
      
      <!--图片预览-->
      <div v-if="previewImage" style="margin-top:10px;">
      <img :src="previewImage" width="120" style="border-radius:8px;"/>
      </div>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showAdd=false">取 消</el-button>
    <el-button type="primary" @click="addProduct">提交</el-button>
  </template>
</el-dialog>

<el-dialog v-model="editing" title="编辑商品" width="500px">
  <el-form label-width="80px">
    <el-form-item label="名称">
      <el-input v-model="form.name"/>
    </el-form-item>
    <el-form-item label="库存">
      <el-input v-model="form.stock"/>
    </el-form-item>
    <el-form-item label="成本价">
      <el-input v-model="form.cost_price"/>
    </el-form-item>
    <el-form-item label="售价">
      <el-input v-model="form.sell_price"/>
    </el-form-item>

    <el-form-item label="图片">
      <input type="file" @change="handleEditFile">
      <div v-if="editPreviewImage" style="margin-top:10px;">
        <img :src="editPreviewImage" width="120" style="border-radius: 8px;"/>
      </div>
    </el-form-item>

  </el-form>
  <template #footer>
    <el-button @click="editing=false">取消</el-button>
    <el-button type="primary" @click="updateProduct">保存</el-button>
  </template>

</el-dialog>

<!--入库弹窗-->
<el-dialog v-model="showStockIn" title="商品入库" width="500px">
  <el-form label-width="80px">
    <el-form-item label="商品">
      <el-input v-model="stockForm.goods_name" disabled/>
    </el-form-item>
    <el-form-item label="数量">
      <el-input v-model="stockForm.quantity"/>
    </el-form-item>
    <el-form-item label="备注">
      <el-input v-model="stockForm.remark"/>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showStockIn=false">取消</el-button>
    <el-button type="primary" @click="submitStockIn">提交</el-button>
  </template>
</el-dialog>
<!--出库弹窗-->
<el-dialog v-model="showStockOut" title="商品出库" width="500px">
  <el-form label-width="80px">
    <el-form-item label="商品">
      <el-input v-model="stockForm.goods_name" disabled/>
    </el-form-item>
    <el-form-item label="数量">
      <el-input v-model="stockForm.quantity"/>
    </el-form-item>
    <el-form-item label="备注">
      <el-input v-model="stockForm.remark"/>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showStockOut=false">取消</el-button>
    <el-button type="primary" @click="submitStockOut">提交</el-button>
  </template>
</el-dialog>

  </div>

 
</template>



<script>
import axios from 'axios'

export default {
  data() {
    return {
      goodsList: [],
      keyword: '',
      file:null,
      previewImage:'',
      editFile:null,
      editPreviewImage:'',
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
      },
      showStockIn:false,
      showStockOut:false,
      stockForm:{
        goods_id:null,
        goods_name:'',
        quantity:'',
        remark:''
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
      this.editPreviewImage=item.image
      this.editFile=null
    },

    cancelEdit() {
      this.editing = false
    },

    // 更新
    updateProduct() {
      const formData=new FormData()

      formData.append('name',this.form.name)
      formData.append('stock',this.form.stock)
      formData.append('cost_price',this.form.cost_price)
      formData.append('sell_price',this.form.sell_price)

      if(this.editFile){
        formData.append('file',this.editFile)
      }
      axios.put(`http://localhost:5000/api/products/${this.form.id}`, formData)
        .then(() => {
          alert('更新成功')
          this.editing = false
          this.fetchProducts()
        })
        .catch(err => {
          console.error(err)
          alert('更新失败')
        })
    },

    logout() {
      localStorage.removeItem('user')
      this.$router.push('/')
    },

    addProduct(){
      const formData=new FormData()
      formData.append('name',this.newForm.name)
      formData.append('stock',this.newForm.stock)
      formData.append('cost_price',this.newForm.cost_price)
      formData.append('sell_price',this.newForm.sell_price)
      if(this.file){
        formData.append('file',this.file)
      }
      if(!this.newForm.name){
        alert('请输入商品名称')
        return
      }
      axios.post('http://localhost:5000/api/products', formData)
        .then(()=>{
          alert('新增成功')
          this.showAdd=false

          this.newForm={
            name:'',
            stock:'',
            cost_price:'',
            sell_price:''
          }
          this.file=null
          this.fetchProducts()
        })
        .catch(err=>{
          console.error(err)
          alert('新增失败')
        })
    },
    cancelAdd(){
      this.showAdd=false
    },
    resetSearch(){
      this.keyword=''
      this.fetchProducts()
    },
    handleFile(e){
      this.file=e.target.files[0]
    },
    openAddDialog(){
      this.showAdd=true
    },
    handleEditFile(e){
      this.editFile=e.target.files[0]
      if(this.editFile){
        this.editPreviewImage=URL.createObjectURL(this.editFile)
      }
    },
    exportCSV(){

       window.open('http://localhost:5000/api/export/products')

    },
    openStockIn(goods){
      this.stockForm={
        goods_id:goods.id,
        goods_name:goods.name,
        quantity:'',
        remark:''
      }
      this.showStockIn=true
    },
    openStockOut(goods){
      this.stockForm={
        goods_id:goods.id,
        goods_name:goods.name,
        quantity:'',
        remark:''
      }
      this.showStockOut=true
    },
    submitStockIn(){
      axios.post('http://localhost:5000/api/stock/in',
        {
          goods_id:this.stockForm.goods_id,
          quantity:this.stockForm.quantity,
          remark:this.stockForm.remark
        }
      ).then(res=>{
        alert(res.data.message)
        this.showStockIn=false
        this.fetchProducts()
      }).catch(err=>{
        console.error(err)
        alert('入库失败')
      })
    },
    submitStockOut(){
      axios.post('http://localhost:5000/api/stock/out',
        {
          goods_id:this.stockForm.goods_id,
          quantity:this.stockForm.quantity,
          remark:this.stockForm.remark
        }
      ).then(res=>{
        if(!res.data.success){
          alert(res.data.message)
          return
        }
        alert(res.data.message)
        this.showStockOut=false
        this.fetchProducts()
      }).catch(err=>{
        console.error(err)
        alert('出库失败')
      })
    }

  }
}
</script>
<style>
.container{
  width:1200px;
  margin:30px auto;
}
.search-box{
  margin-bottom:20px;
}
.toolbar{
  margin-bottom:20px;
  display:flex;
  gap:10px;
  flex-wrap:wrap;
}
.btn-group{
  margin-top:10px;
  display:flex;
  gap:10px;
}
.action-buttons{
  display:flex;
  justify-content: center;
  gap:8px;
}
.action-buttons .el-button{
  width:80px;
  margin:0;
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