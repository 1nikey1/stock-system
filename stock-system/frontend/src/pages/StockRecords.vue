<template>
    <div class="container">
        <h2>库存记录</h2>
        <!--搜索-->
        <div class="toolbar">
            <el-input
                v-model="keyword"
                placeholder="请输入商品名称"
                style="width:220px"/>
            <el-button type="primary" @click="fetchRecords">
                搜索
            </el-button>
        </div>

        <!--商品卡片-->
        <el-row :gutter="20">
            <el-col
                :span="12"
                v-for="item in recordsList"
                :key="item.goods.id">
            <el-card class="goods-card">
                <!--商品信息-->
                <div class="goods-header">
                    <el-image
                        :src="item.goods.image"
                        style="width:80px;height: 80px;border-radius:8px;"
                        fit="cover"
                        :preview-src-list="[item.goods.image]"/>
                    <div class="goods-info">
                        <h3>{{ item.goods.name }}</h3>
                        <p>当前库存：{{ item.goods.stock }}</p>
                        <p>成本价：￥{{ item.goods.cost_price }}</p>
                        <p>售价：￥{{ item.goods.sale_price }}</p>
                    </div>
                </div>
                <!--流水表格-->
                <el-table
                    :data="item.records"
                    border
                    style="margin-top:20px;">
                <el-table-column
                    prop="create_time"
                    label="时间"
                    width="180"/>
                <el-table-column
              label="类型"
              width="100"
            >

              <template #default="scope">

                <el-tag
                  :type="scope.row.type === 'in' ? 'success' : 'danger'"
                >
                  {{ scope.row.type === 'in' ? '入库' : '出库' }}
                </el-tag>

              </template>

            </el-table-column>

            <el-table-column
              prop="quantity"
              label="数量"
              width="100"
            />
                <el-table-column
                    prop="before_stock"
                    label="操作前"
                    width="100"/>
                <el-table-column
                    prop="after_stock"
                    label="操作后"
                    width="100"/>
                <el-table-column
                    prop="remark"
                    label="备注"/>
                </el-table>
            </el-card>
            </el-col>
            </el-row>
    </div>
</template>
<script>
import axios from "axios"

export default{
    data(){
        return {
            keyword:'',
            recordsList:[]
        }
    },
    mounted(){
        this.fetchRecords()
    },
    methods:{
        fetchRecords(){
            axios.get(
                'http://localhost:5000/api/stock/records',
                {
                    params:{
                        keyword:this.keyword
                    }
                }
            ).then(res=>{
                this.recordsList=res.data
            }).catch(err=>{
                console.error(err)
                alert('获取库存记录失败')
            })
        }
    }
}
</script>
<style scoped>

.container{

  width:1200px;

  margin:30px auto;

}

.toolbar{

  margin-bottom:20px;

  display:flex;

  gap:10px;

}

.goods-card{

  margin-bottom:20px;

}

.goods-header{

  display:flex;

  gap:20px;

  align-items:center;

}

.goods-info p{

  margin:5px 0;

}

</style>