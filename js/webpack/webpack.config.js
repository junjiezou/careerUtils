const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');

module.exports = {
    mode: 'production',
//   entry: './src/index.js',
    entry: {
        app: './src/index.js',
        // print: './src/print.js'
    },
    devtool: 'inline-source-map',
    devServer: {
        contentBase: './dist',
        hot: true
    },
  output: {
    // filename: 'bundle.js',
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new CleanWebpackPlugin(['dist']),
    new HtmlWebpackPlugin({
       title: 'Output Management'
     }),
     new webpack.NamedModulesPlugin(),
     new webpack.HotModuleReplacementPlugin()
    ],
  module:{
      rules:[
          {
              test: /\.css$/,
              use:[
                  'style-loader',
                  'css-loader'
              ]
          },{
              test: /\.(png|svg|jpg|gif)$/,
              use:[
                  'file-loader'
              ]
          },{
              test:/\.(woff|woff2|eot|ttf|otf)$/,
              use:[
                  'file-loader'
              ]
          }
      ]
    
  }

};