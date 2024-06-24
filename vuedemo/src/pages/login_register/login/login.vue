<template>
  <div class="form-container">
    <el-form :model="form" :rules="rules" ref="formRef">
      <div class="form-items-container">

        <h3 align="center">欢迎登录</h3>
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入账号"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit(form.username,form.password)">登录</el-button>
          <el-button @click="Reset('form')">重置</el-button>
        </el-form-item>
        <p class="no">没有账号？
          <el-link type="primary" @click="goToRegister">立即注册</el-link>
        </p>
      </div>
    </el-form>
  </div>

</template>

<script setup>
import {computed, ref} from 'vue';
import router from "@/router";
import http from "@/http";
import {ElMessage} from "element-plus";
import { useStore } from 'vuex';



const form = ref({
  username: '',
  password: ''
});

const rules = {
  username: [
    {required: true, message: '请输入账号', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'}
  ]
};

const formRef = ref(null);
// 导入 useStore 函数
const store = useStore();
// 点击登录
const handleSubmit = (a, b) => {
  http.post('index/login/', {
    username: a,
    password: b
  }).then(res => {
    if (res.data.code === 200) {
      ElMessage.success('登录成功');
      sessionStorage.setItem('user-token', res.data.token);
      store.commit('setUsername', res.data.username);
      console.log(store.state.username);
      store.commit('setToken', res.data.token);
      router.push('/blog');
    }
    else if (res.data.code === 400) {
      ElMessage.error('账号或密码错误');
    }
    else if (res.data.code === 401) {
      ElMessage.error('用户名或密码不能为空');
    }
  }).catch(err => {
    console.log(err);

  });
};

const Reset = () => {
  formRef.value.resetFields();
};
const goToRegister = () => {
  router.push('/register');
};
</script>


<style scoped>
.form-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-items-container {
  display: flex;
  flex-direction: column; /* 垂直排列表单项 */
  align-items: center; /* 垂直居中 */
  /* 如果你想要水平居中（比如对于单行表单），你可以设置 justify-content: center; */
}

h3 {
  margin-bottom: 20px;
}

.no {
  cursor: pointer;
  margin-top: 30px;
  text-align: center;
  font-size: 12px;
  color: #828282;
}
</style>