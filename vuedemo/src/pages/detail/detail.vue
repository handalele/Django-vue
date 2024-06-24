<template>
  <div class="article-list">

    <div class="article-header">
      <h2 class="article-title">{{ article.title }}</h2>
      <span class="article-author">作者: {{ article.author }}</span>
    </div>

    <div class="article-content">
      <p style="white-space: pre-wrap;">{{ article.content }}</p>
    </div>
    <div class="comments">
      <div v-for="(comment, index) in comments" :key="index" class="comment">
        <h3>{{ comment.username }}</h3>
        <p>{{ comment.comment }}</p>
        <p>{{ comment.comment_time }}</p>
      </div>
    </div>

    <div class="article-footer">
      <div class="article-meta">
        <span>点赞量: {{ article.up }}</span>
        <span>收藏量: {{ article.favorite }}</span>
      </div>
      <el-button type="primary" @click="upvote(article.id)">赞</el-button>
      <el-button type="success" @click="favorite(article.id)">收藏</el-button>
      <el-button type="warning" @click="open(article.id)">评论</el-button>
    </div>
  </div>
</template>
<script setup>
import {useRoute} from 'vue-router';
import {onMounted, ref} from 'vue';
import http from "@/http";
import {ElMessage, ElMessageBox} from "element-plus";
import {useStore} from "vuex";

const store = useStore();
const route = useRoute();
let article = ref([]);
let comments = ref([]);
// 请求数据
onMounted(() => {

  // 获取博客详细数据
  http.get(`/index/detail/${route.params.id}`,)
      .then(res => {
        article.value = res.data.data;
      })
      .catch(err => {
        console.log(err);
      })

  get_comment()

})

// 获取评论数据
function get_comment() {
  http.get(`/index/comment/detail/${route.params.id}`)
      .then(res => {
        comments.value = res.data.data;
      }).catch(err => {
    console.log(err)
  })

}

// 点赞
function upvote(id) {
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

// 评论
const open = () => {
  ElMessageBox.prompt('欢迎高质量的评论,低质的评论会被折叠', '评论', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
  })
      .then(({value}) => {
        http.post('/index/comment/', {
          author: store.state.username,
          content: route.params.id,
          comment: value,
        }).then(res => {
          if (res.data.code === 200) {
            ElMessage.success('评论成功！');
            get_comment()
          } else {
            ElMessage.error('评论失败！');
          }
        }).catch(err => {
          console.log(err)
        })
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: 'Input canceled',
        })
      })
}
</script>

<style scoped>
.article-list {
  display: flex;
  width: 100%;
  flex-direction: column;
  height: 100%;
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.article-title {
  font-size: 18px;
  font-weight: bold;

}

.article-author {
  font-size: 14px;
  color: #666;
}

.article-content {
  width: 100%;
  margin: 10px 0;
  flex: 1; /* 允许内容区域根据内容增长 */
  overflow: auto; /* 如果内容超出，显示滚动条 */
  min-height: 500px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment {
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f0f0f2;
  border-radius: 10px;
  border: 1px solid #42b983;
}
.comment:hover {
  transform: scale(1.02);
}
.article-meta {
  font-size: 20px;
  color: #999;
}
</style>