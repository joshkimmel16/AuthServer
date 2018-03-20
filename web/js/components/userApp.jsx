// userApp.jsx
const React = require("react");
const Header = require("./shared/Header.jsx");
const UserLogin = require("./shared/LoginDialog.jsx");
const data = {
  header: {
      title: "User Login",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg",
      showLogin: false,
      loginText: "Log In",
      logoutText: "Log Out",
      loginState: false,
      loginRedirect: "/login/user?appId=1&redirectUrl=" + encodeURIComponent(window.location.origin + "/landing")
  },
  body: {
      type: "text",
      inputLabel: "User Name:",
      inputRegex: /^[A-Za-z0-9\.]+$/,
      message: "Please enter your user name below.",
      submitText: "Submit",
      errorText: "Invalid user name. A valid name must contain only alphanumeric characters and/or '.'.",
      action: "/authorize/user",
      failMessage: "Could not verify user name! Please ensure you have entered the correct information.",
      successMessage: "User name verified!",
      modalState: 0,
      appId: 0,
      redirectUrl: "",
      targetLocation: (window.location.origin + "/login/password")
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
      var check = null;
      var appId = 0;
      var redirectUrl = "";
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == "fail") {
            check = decodeURIComponent(pair[1]);
        }
        else if (decodeURIComponent(pair[0]) == "appId") {
            appId = parseInt(decodeURIComponent(pair[1]));
        }
        else if (decodeURIComponent(pair[0]) == "redirectUrl") {
            redirectUrl = decodeURIComponent(pair[1]);
        }
      }

      var tempState = this.state.body;
      tempState.appId = appId;
      tempState.redirectUrl = redirectUrl;
      tempState.modalState = (check !== null) ? -1 : 0;
      this.setState({body: tempState});
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
      return <UserLogin
           type={this.state.body.type}
           inputLabel={this.state.body.inputLabel}
           inputRegex={this.state.body.inputRegex}
           message={this.state.body.message}
           submitText={this.state.body.submitText}
           errorText={this.state.body.errorText}
           action={this.state.body.action}
           failMessage={this.state.body.failMessage}
           successMessage={this.state.body.successMessage}
           modalState={this.state.body.modalState}
           appId={this.state.body.appId}
           redirectUrl={this.state.body.redirectUrl}
           targetLocation={this.state.body.targetLocation}
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