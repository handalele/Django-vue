import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store'
import ArcoVue from '@arco-design/web-vue';
import '@arco-design/web-vue/dist/arco.css';

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(ArcoVue);
app.use(store) //注册vuex
app.mount('#app')
