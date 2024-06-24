<template>
  <div class="mon">
    <div class="top">
      <!--    左-->
      <div class="left">
        <img src="@/assets/icon.png" style="width: 100px;"/>
        <div class="center">
          <!--      菜单按钮-->
          <ul class="active">
            <li>
              <router-link to="/blog">首页</router-link>
            </li>
            <li><a href="">收藏</a></li>
            <li><a href="">点赞</a></li>
          </ul>
        </div>
      </div>

      <!--    右边-->
      <div class="right">
        <el-input
            v-model="input2"
            style="width: 500px"
            placeholder="Type something"
            autofocus:true
        />
        <el-button :icon="Search" type="success" style="border-radius: 0 16px 16px 0;margin-right: 200px ">搜索
        </el-button>

        <el-dropdown>
        <span class="el-dropdown-link" style="display: flex;align-items: center;justify-content: center">
         <el-avatar
             src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
         /><el-icon class="el-icon--right"><arrow-down/></el-icon>
        </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :icon="User">
                <router-link class="link" to="user">个人主页</router-link>
              </el-dropdown-item>
              <el-dropdown-item :icon="Edit">
                <router-link class="link" to="edit">修改资料</router-link>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button type="danger" @click="publish" round>发布</el-button>
      </div>
    </div>

    <!--  主体-->
    <div class="main">
      <router-view></router-view>
    </div>
  </div>
</template>
<script setup>
import {ArrowDown, Edit, Plus, Search, User} from '@element-plus/icons-vue';
import router from "@/router";
import {onMounted} from "vue";
// 定义聊天机器人的配置
const chatbotConfig = {
  token: '0u5BdVJI8el0gJhF',
  baseUrl: 'http://localhost'
};

// 创建并插入聊天机器人脚本
function createChatbotScript() {
  const script = document.createElement('script');
  script.src = `${chatbotConfig.baseUrl}/embed.min.js`;
  script.id = chatbotConfig.token;
  script.defer = true;
  document.head.appendChild(script);
}

// 设置聊天机器人配置
function setChatbotConfig() {
  window.difyChatbotConfig = chatbotConfig;
}

// 在组件挂载后执行
onMounted(() => {
  createChatbotScript();
  setChatbotConfig();
});

function publish() {
  router.push('/publish');
}
</script>
<style>
.mon {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #fafafa;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 10vh;
  background-color: white;

}

.link {
  color: #475669;
  text-decoration: none;
  text-align: center;
}

.left {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  height: 100%;
  background-color: white;
}

.center {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  height: 100%;
}

.right {
  display: flex;
  align-items: center; /* 垂直居中 */
  height: 100%;
  justify-content: space-between;

}

.main {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  flex-direction: column;
  min-height: 90vh;
  width: 80%;
  margin-top: 10px;
}


.active {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
}

.active li {
  margin-right: 30px;
}

.active li a {
  color: #475669;
  text-decoration: none;
  text-align: center;
}

</style>
// const csrfToken = ref(null);
// onMounted(async () => {
//   try {
//     const response = await axios.get('http://localhost:8000/index/token/');
//     csrfToken.value = response.data.csrf_token;
//     // 设置 axios 的默认请求头
//     // axios.defaults.headers.common['X-CSRFToken'] = csrfToken.value;
//
//   } catch (error) {
//     console.error('Failed to fetch CSRF token', error);
//   }
// });
//
// function post() {
//   console.log(csrfToken.value);
//   axios.post('http://localhost:8000/index/test/', {"username": 'hanle', "password": '123'}, {
//     headers: {
//       'X-CSRFToken': csrfToken.value
//     },
//     withCredentials: true // 允许跨域请求携带凭证（如 Cookie）
//   })
//       .then(response => {
//         // 请求成功，处理响应数据
//         console.log(response.data);
//       })
//       .catch(error => {
//         // 请求失败，处理错误
//         console.error(error);
//       });
// }
