<template>
  <div class="big">
    <div v-for="item in blog" :key="item.id" class="small">

      <div class="left1">

        <router-link :to="{ name: 'detail', params: { id: item.id } }" class="title-link">
          <p class="title">{{ item.title }}</p>
          <p class="content">{{ shortenContent(item.content) }}</p>
        </router-link>

        <div class="info">
          <div class="likes">
            赞:<span>{{ item.up }}</span>
          </div>
          <div class="date">
            <span>{{ formattedDate(item.create_time) }}</span>
          </div>
        </div>

      </div>

      <div class="right">
        <a-button class="btn" type="primary" status="warning" @click="handleClick">修改</a-button>
        <a-button class="btn" type="primary" status="danger" @click="delClick(item.id)">删除</a-button>

        <el-drawer
            v-model="visible"
            title="修改博客"
            direction="rtl"
            size="50%"
        >
          <div>{{item.content}}</div>
        </el-drawer>
      </div>
    </div>
  </div>
</template>
<script setup>
import {useStore} from "vuex";
import {onMounted, ref} from "vue";
import http from "@/http";
import {ElMessage} from "element-plus";

const visible = ref(false);

const handleClick = () => {
  visible.value = true;
};
const handleOk = () => {
  visible.value = false;
};
const handleCancel = () => {
  visible.value = false;
}
// 删除博客
const delClick = (id) => {
  http.delete(`index/delete/${id}`).then(res => {
    getBlog();
    ElMessage.success('删除成功');
  }).catch(err => {
    console.log(err);
  });
}

const blog = ref([]);
const store = useStore();
onMounted(() => {
  getBlog()
});
// 获取当前用户博客
const getBlog = () => {
  http.get(`index/user/home/${store.state.username}`).then(res => {
    console.log(res.data.data);
    blog.value = res.data.data;
  }).catch(err => {
    console.log(err);
  });
}

// 时间格式
function formattedDate(create_time) {
  const date = new Date(create_time);
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0'); // 月份从0开始，所以需要+1
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 省略字符串
function shortenContent(str) {
  return str.length > 200 ? str.substr(0, 200) + '...' : str;
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.big {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  background-color: #f5f5f5;
}

.small {
  border-radius: 10px;
  background-color: #fff;
  border: 1px solid #42b983;
  margin-bottom: 20px;
  display: flex;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s;
}

.small:hover {
  transform: scale(1.02);
}

.left1 {
  width: 80%;
  display: flex;
  flex-direction: column;
}

.title-link {
  text-decoration: none;
  color: black;
}

.title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: #333;
}

.content {
  font-size: 14px;
  color: #666;
  margin: 10px 0;
}

.info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.likes, .date {
  font-size: 14px;
  color: #999;
}

.right {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 20%;
}

.btn {
  margin-bottom: 10px;
  width: 100px;
}
</style>
