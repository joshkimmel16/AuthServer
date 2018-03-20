// userApp.jsx
const React = require("react");
const Header = require("./shared/Header.jsx");
const data = {
  header: {
      title: "Access Denied",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg",
      showLogin: true,
      loginText: "Log In",
      logoutText: "Log Out",
      loginState: false,
      loginRedirect: "/login/user?appId=1"
  },
  body: {}
};

class App extends React.Component {
  constructor() {
        super();
        this.state = {
            header: data.header,
            body: data.body
        };
      
        var check = this.checkCookie("jwt");
        if (check === true)
        {
            var h = this.state.header;
            h.loginState = true;
            this.setState({header: h});
        }
  }
    
  checkCookie (cookie_name) {
      return document.cookie.indexOf(cookie_name + '=') !== -1;
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
    
  renderBody () {
      return <div className='deniedBody'></div>
  }
    
  render () {
    return (
        <div className='main'>
            {this.renderHeader()}
            {this.renderBody()}
        </div>
    )
  }
}

module.exports = App;
