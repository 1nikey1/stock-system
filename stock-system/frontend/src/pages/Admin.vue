<script>
export default {
  data(){
    return{
      list:[]
    }
  }
}
</script>

<template>
  <div>
    <h2>审核列表</h2>
    <div v-for="item in list" :key="item.id">
      <p>{{item.name}}</p>
      <button>通过</button>
      <button>驳回</button>
    </div>
  </div>
</template>

<style scoped>

</style>