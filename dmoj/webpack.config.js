var BundleTracker = require('webpack-bundle-tracker');
module.exports = {
    context: __dirname,
    entry: "./static/js/src/index",//entry 文件夹的位置
    output: {
        path: './static/js/dist',
        filename: "[name].dev.js"
    },
    module: {//使用babel loader
        loaders: [
            {
                test: //.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel',
                query:
                {
                    presets: ['es2015']
                }
            }
            ]
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
// Usage在当前目录执行 webpack(全局或是项目)
// 会自动读取/static/js/src/index.js
// 生成/static/js/dist/main.dev.js