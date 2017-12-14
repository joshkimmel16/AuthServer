// index.jsx

//JS dependencies
global.jQuery = require('jquery/dist/jquery.min.js');
const bootstrap = require('bootstrap/dist/js/bootstrap.min.js');
const React = require("react");
const ReactDOM = require("react-dom");
const App = require("./App");

//styling and resource dependencies
require('bootstrap/dist/css/bootstrap.min.css');
require('../styles/img/favicon.ico');

ReactDOM.render(<App />, document.getElementById("content"));