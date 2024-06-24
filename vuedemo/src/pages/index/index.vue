<template>
  <div style="width: 100%; height: 100%;">
    <div class="main-hover">
      <ul class="active">
        <li><a href="https://blog.csdn.net/nav/back-end">后端</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">前端</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">Python</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">人工智能</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">Java</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">后端</a></li>
        <li><a href="https://blog.csdn.net/nav/back-end">后端</a></li>
      </ul>
    </div>

    <div class="main-top">
      <el-carousel style="height: 100%; width: 50%">
        <el-carousel-item v-for="(item, index) in images_list" :key="index">
          <img :src="item" style="height: 350px; width: 100%"/>
        </el-carousel-item>
      </el-carousel>
    </div>

    <div class="main-down">

      <div class="content" v-for="item in blog" :key="item">
        <div class="content-left">
<!--          <img :src="item.img">-->
<img
          alt="avatar"
          src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
        />
        </div>
        <div class="content-right">
          <router-link :to="{ name: 'detail', params: { id: item.id } }">
            <p>{{ item.title }}</p>
            <p style="font-family: 'Microsoft Yahei',serif">{{ shortenContent(item.content) }}</p>
          </router-link>
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; justify-content: center; flex-direction: row;"  >
              <span class="action"  @click="upvoteMethod(item.id)">
          <span v-if="item.is_upvoted"><IconHeartFill :style="{ color: '#f53f3f' }"/></span>
          <span v-else><IconHeart/></span>
                 <span style="font-size: 17px;font-family: 等线,serif;margin-left: 2px;"> {{ item.up }} </span>
          </span>
<!--            <span style="font-size: 20px;font-family: 等线,serif"> {{ item.up }} </span>-->
            </div>


            <div>
              <span style="margin-left: 10px">作者:{{ item.author }}</span>
              <span style="margin-left: 10px">{{ formattedDate(item.create_time) }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>

// 轮播图
import {onMounted, ref} from "vue";
import http from "@/http";
import {ElMessage} from "element-plus";
import {useStore} from "vuex";
import {
  IconHeart,
  IconHeartFill,
} from '@arco-design/web-vue/es/icon';
// 评论
const formRef = ref(null);
// 导入 useStore 函数
const store = useStore();
let blog = ref([]);
onMounted(() => {
      submitForm()
    }
)

// 刷新博客
function submitForm() {
  http.get(`/index/blog/user?username=${store.state.username}`).then(res => {
    blog.value = res.data.data
  })
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
  return str.length > 100 ? str.substr(0, 100) + '...' : str;
}

// 轮播图
let images_list = ref([
  require('@/assets/carousel/bo1.png'),
  require('@/assets/carousel/bo2.png'),
  require('@/assets/carousel/bo3.png'),
  require('@/assets/carousel/bo4.png'),
  require('@/assets/carousel/bo5.png'),
]);

// 点赞功能实现
function upvoteMethod(id) {

  http.post('/index/upvote/', {
    content_id: id,
    user_id: store.state.username
  }).then(res => {
    const new_up = res.data.up
    if (res.data.code === 200) {
      for (let i = 0; i < blog.value.length; i++) {
        if (blog.value[i].id === id) {
          blog.value[i].up = new_up
          blog.value[i].is_upvoted = true
          ElMessage.success('点赞成功！');
          break
        }
      }
    } else if (res.data.code === 201) {
      for (let i = 0; i < blog.value.length; i++) {
        if (blog.value[i].id === id) {
          blog.value[i].up = new_up
          blog.value[i].is_upvoted = false
          ElMessage.success('取消点赞！');
          break
        }
      }
    }
  }).catch(err => {
    console.log(err)
  })
}
</script>
<style scoped>
.action {
  display: flex;
  padding: 0 4px;
  color: var(--color-text-1);
  line-height: 14px;
  background: transparent;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.1s ease;
}

.action:hover {
  background: var(--color-fill-3);
}

.content-left img {
  height: 80%;
  width: 80%;
  max-height: 120px;
  max-width: 220px;

}

.content-right {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 80%;
}

.content-right a {
  text-decoration: none;
  color: black;
  margin-left: 0;
}

.main-hover {
  height: 10%;
  width: 100%;
  background-color: white;
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  margin-bottom: 10px;
}

.main-top {
  min-height: 30vh;
  width: 100%;
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  border-radius: 10px;
  background-color: #fafafa;
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__container {
  height: 100%;
  width: 100%;
}

.main-down {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  flex-direction: column;
  width: 100%;
  border-radius: 10px;
  background-color: white;
  margin-top: 20px;
}
.content {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  width: 100%;
  margin-bottom: 10px;
  border-top: 1px solid #f0f0f2;
  border-bottom: 1px solid #f0f0f2;
}


.content-left {
  display: flex;
  align-items: center; /* 垂直居中 */
  height: 100%;
  width: 20%;
}
</style>