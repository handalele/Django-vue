<template>
  <div class="wrapper">
    <h1>发布博客</h1>
    <h3>标题</h3>
    <el-input v-model="title" placeholder="请输入标题" style="width: 340px"/>
    <h3>分类</h3>
    <el-select
        v-model="value"
        size="large"
        style="width: 340px"
    >
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
      />
    </el-select>
    <h3>内容</h3>
    <el-input v-model="content" type="textarea" :rows="30" placeholder="请输入内容"/>
    <el-button type="primary" @click="publish">发布</el-button>
  </div>


</template>

<script setup>
import http from "@/http";
import {ref} from "vue";
import {ElMessage} from "element-plus";
// 导入 useStore 函数
import {useStore} from 'vuex'

const store = useStore()
// 选择器
const title = ref('')
const value = ref('')
const content = ref('')
const options = [
  {
    value: '前端',
    label: '前端',
  },
  {
    value: '后端',
    label: '后端',
  },
  {
    value: '数据库',
    label: '数据库',
  },
  {
    value: '算法',
    label: '算法',
  },
  {
    value: '其他',
    label: '其他',
  }
]
const publish = () => {
  console.log(title.value, value.value, content.value, store.getters.getUsername)
  http.post('index/publish/', {
    title: title.value,
    content_type: value.value,
    content: content.value,
    user: store.state.username
  }).then(res => {
    if (res.data.code === 200) {
      ElMessage({
        message: '发布成功',
        type: 'success'
      })
    }
  }).catch(err => {
    ElMessage({
      message: '发布失败',
      type: 'error'
    })
  })
}
</script>

<style scoped>
.wrapper {
  width: 80%;
  height: 100%;
  background-color: white;
}

</style>
