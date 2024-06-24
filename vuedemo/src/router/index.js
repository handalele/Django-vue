import {createWebHashHistory} from "vue-router";
import {createRouter, createWebHistory} from "vue-router";
import {useStore} from 'vuex'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'top',
        redirect: '/login',
    },
    {
        path: '/home',
        name: 'Home',
        component: () => import('../pages/login_register/home.vue'),
        children: [
            {
                path: '/login',
                name: 'login',
                component: () => import('@/pages/login_register/login/login.vue')
            },
            {
                path: '/register',
                name: 'register',
                component: () => import('@/pages/login_register/register/register.vue')
            },
        ]
    },
    {
        path: '/index',
        name: 'index',
        component: () => import('../pages/index/vueindex.vue'),
        children: [
            {
                path: '/blog',
                name: 'blog',
                component: () => import('@/pages/index/index.vue')
            },
            {
                path: '/publish',
                name: 'publish',
                component: () => import('@/pages/index/publish.vue')
            },
            {
                path: '/detail/:id',
                name: 'detail',
                component: () => import('@/pages/detail/detail.vue')
            },
            {
                path: '/user',
                name: 'user',
                component: () => import('@/pages/index/person_blog.vue')
            },
            {
                path: '/edit',
                name: 'edit',
                component: () => import('@/pages/user/userchange.vue')
            },
        ]
    },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach((to, from, next) => {
    if (to.path === '/login' || to.path === '/register') {
        next();
    } else {
        // 对于其他页面，需要检查用户是否已经登录
        let token = sessionStorage.getItem('user-token');
        if (token === null || token === '') {
            // 如果没有令牌，重定向到登录页面
            next('/login');
        } else {
            // 如果有令牌，允许继续访问目标页面
            next();
        }
    }
})

router.afterEach(() => {
    // 跳转后的操作
})

router.beforeResolve((to, from, next) => {
    // 在导航被确认之前的操作
    next()
})
export default router