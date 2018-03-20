// landingPage.jsx
const axios = require('axios');
const React = require("react");
const Header = require("./shared/Header.jsx");
const Landing = require("./specific/landingPage.jsx");
const data = {
  header: {
      title: "Welcome to Auth Server",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg",
      showLogin: true,
      loginText: "Log In",
      logoutText: "Log Out",
      loginState: true,
      loginRedirect: "/login/user?appId=1&redirectUrl=%2Flanding"
  },
  body: {
      userId: 0,
      listHeading: "What Would You Like To Do?",
      listOptions: [
          {"text": "Update User Information", "target": "/up/user", "isAdmin": false},
          {"text": "Register New User", "target": "/reg/user", "isAdmin": true},
          {"text": "Register New Application", "target": "/reg/app", "isAdmin": true}
      ],
      rights: 0
  }
};

class App extends React.Component {
  constructor() {
        super();
        this.state = {
            header: data.header,
            body: data.body
        };
  }
    
  componentDidMount () {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    var uId = -1;
    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split('=');
      if (decodeURIComponent(pair[0]) == "userId") {
         uId = parseInt(decodeURIComponent(pair[1]));
      }
    }

    var tempState = this.state.body;
    tempState.userId = uId;
      
    //use userId param to make an AJAX call to the server to retrieve all existing user information
    var context = this;
    axios.get('/retrieve/user/' + uId, {headers: {"X-Requested-With": "AJAX"}})
        .then(function(response) {
            var met = JSON.parse(response.data.metadata);
            tempState.rights = met.rights;
            
            context.setState({body: tempState});
        })
        .catch(function(error) {});
  }
    
  renderHeader () {
        return <Header
            logo={this.state.header.logo}
            title={this.state.header.title}
            showLogin={this.state.header.showLogin}
            loginText={this.state.header.loginText}
            logoutText={this.state.header.logoutText}
            loginState={this.state.header.loginState}
            loginRedirect={this.state.header.loginRedirect}
        />
  }
    
  renderDialog () {
        return <Landing
           userId={this.state.body.userId}
           listHeading={this.state.body.listHeading}
           listOptions={this.state.body.listOptions}
           rights={this.state.body.rights}
        />
  }
    
  render () {
    return (
            <div className='main'>
                {this.renderHeader()}
                {this.renderDialog()}
            </div>
        )
  }
    
}

module.exports = App;