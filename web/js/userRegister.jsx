// userRegister.jsx

//JS dependencies
global.jQuery = require('jquery/dist/jquery.min.js');
const bootstrap = require('bootstrap/dist/js/bootstrap.min.js');
const React = require("react");
const ReactDOM = require("react-dom");
const App = require("./components/registerUser.jsx");

//styling and resource dependencies
require('bootstrap/dist/css/bootstrap.min.css');
require('../styles/userRegister.css');
require('../styles/img/favicon.ico');
require('../styles/img/knight.jpg');
require('../styles/img/steel_background.jpg');

ReactDOM.render(<App />, document.getElementById("content"));