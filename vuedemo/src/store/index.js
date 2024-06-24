import {createStore} from 'vuex'

const store = createStore({
    state: {
        //定义数据源
        username: '',
        token: '',
        //状态管理器中定义的数据源
    },
    // 获取数据源
    getters: {
        //获取数据源
        getUsername(state) {
            return state.username
        },
        getToken(state) {
            console.log('Mutating username to:', state.token);
            return state.token
        }
    },
    mutations: {
        //修改数据源
        setUsername(state, username) {
             console.log('Mutating username to:', username);
            state.username = username
        },
        setToken(state, token) {
             console.log('Mutating username to:', token);
            state.token = token
        }
    },
    actions: {
        //异步操作
    },
})
export default store