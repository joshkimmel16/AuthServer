const webpack = require('webpack');
const config = {
    entry:  {
        userLogin: __dirname + '/js/userLogin.jsx',
        passCheck: __dirname + '/js/passCheck.jsx',
        appRegister: __dirname + '/js/appRegister.jsx',
        userRegister: __dirname + '/js/userRegister.jsx',
        accessDenied: __dirname + '/js/accessDenied.jsx',
        userUpdate: __dirname + '/js/userUpdate.jsx'
    },
    output: {
        path: __dirname + '/dist',
        filename: '[name].bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
      rules: [
        {
          test: /\.jsx?/,
          exclude: /node_modules/,
          use: 'babel-loader'
        },
        {
          test: /\.css?/,
          use: [
              { loader: "style-loader" },
              { loader: "css-loader" }
          ]
        },
        {
          test: /\.png$/,
          loader: 'url-loader?limit=100000'
        },
        {
          test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
          loader: 'url-loader?limit=10000&mimetype=application/font-woff'
        },
        {
          test: /\.(ttf|otf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?|(jpg|gif|png|ico)$/,
          loader: 'file-loader'
        }
      ]
    }
};
module.exports = config;