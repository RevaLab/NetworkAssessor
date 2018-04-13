var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './static/js/index',
    output: {
        path: path.resolve('./static/bundles/'),
        filename: 'app.js'
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ]
            }
        ],
    },
    resolve: {
        alias: {vue: 'vue/dist/vue.js'}
    },
    plugins: [
      new BundleTracker({filename: './webpack-stats.json'}),
    ],
};