const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    //基本路径 文件打包后放的位置
// 放置生成的静态资源 (js、css、img、fonts) 的 (相对于 outputDir 的) 目录。资源放的目录
    assetsDir: "static",

    publicPath: "./", // 根域上下文目录

    transpileDependencies: true,
    lintOnSave: false
})
