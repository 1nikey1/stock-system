<script>
export default {
  data(){
    return{
      name:'',
      amount:0
    }
  },
  methods:{
    submit(){
      alert('提交成功（后面接后端）')
    }
  }
}
</script>
<template>
  <div>
    <h2>提交申请</h2>
    <input v-model="name" placeholder="商品名称"/>
    <input v-model="amount" placeholder="数量"/>
    <button @click="submit">提交</button>
  </div>
</template>