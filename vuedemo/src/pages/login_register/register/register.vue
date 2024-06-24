<template>
  <div class="form-container">
    <el-form :model="form" :rules="rules" ref="formRef">
      <div class="form-items-container">

        <h3 align="center">注册</h3>
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入账号"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="email" class="form-item-inline">
          <el-input v-model="form.verificationCode" placeholder="请输入验证码">
          </el-input>
          <button :disabled="countingDown" @click="sendVerificationCode">发送验证码</button>
        </el-form-item>
        <span v-if="countingDown">{{ countdown }}秒后重新获取</span>


        <el-form-item>
          <el-button type="primary" @click="submit(form.username,form.password,)">注册</el-button>
          <el-button @click="Reset()">重置</el-button>
        </el-form-item>
        <p class="no">
          <el-link type="primary" @click="goTologin">前往登录</el-link>
        </p>
      </div>
    </el-form>
  </div>

</template>

<script setup>
import {ref} from 'vue';
import router from "@/router";
import http from "@/http";
import {ElMessage} from "element-plus";


const form = ref({
  username: '',
  password: '',
  email: '',
  verificationCode: '',
});

const rules = {
  username: [
    {required: true, message: '请输入账号', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'}
  ],
  email: [
    {required: true, message: '请输入邮箱', trigger: 'blur'}
  ]
};

const formRef = ref(null);
// 验证码
const countdown = ref(60);
const countingDown = ref(false);
const sendVerificationCode = async () => {
  // 假设这是一个发送验证码的异步函数
  await fakeSendVerificationCode();
  startCountdown();
};
// 模拟发送验证码的异步操作
const startCountdown = () => {
  countingDown.value = true;
  let interval = setInterval(() => {
    if (countdown.value) {
      countdown.value--;
    } else {
      clearInterval(interval);
      countdown.value = 60;
      countingDown.value = false;
    }
  }, 1000);
};
const fakeSendVerificationCode = () => {
  http.get('index/code/', {
    params: {
      email: form.value.email
    }
  }).then(res => {
    ElMessage.success('验证码已发送');
  }).catch(err => {
    ElMessage.error('发送失败');
  })
};
// 点击注册
const submit = (a, b,) => {
  http.post('index/register/', {
    username: a, password: b, email: form.value.email, code: form.value.verificationCode
  }).then(res => {
    if (res.data.code === 200) {
      ElMessage.success('注册成功');
    }
  }).catch(err => {
    console.log('错误为' + err);
  });
};

const Reset = () => {
  formRef.value.resetFields();
};
const goTologin = () => {
  router.push('/login');
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
  height: 100%;
}

.form-item-inline .el-form-item__content {
  display: flex;
  align-items: center;
}

.code {
  display: flex;
  position: relative;
  flex-wrap: wrap;
  justify-content: center;
}

.no {
  cursor: pointer;
  text-align: center;
  font-size: 12px;
  color: #828282;
}
</style>
