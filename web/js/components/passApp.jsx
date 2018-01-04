// passApp.jsx
const React = require("react");
const Header = require("./shared/Header.jsx");
const PassCheck = require("./shared/LoginDialog.jsx");
const data = {
  header: {
      title: "Verify Password",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg"   
  },
  body: {
      type: "password",
      inputLabel: "Password:",
      inputRegex: /^[A-Za-z0-9!@#\$%\^\&\*\(\)]+/,
      message: "Please enter your password below.",
      submitText: "Submit",
      errorText: "Invalid password. A valid password must contain only alphanumeric characters and/or !@#$%^&*()",
      action: "/authorize/password",
      failMessage: "Could not verify password! Please ensure you have entered the correct information.",
      successMessage: "Password verified!",
      modalState: 0,
      appId: 0,
      redirectUrl: "",
      targetLocation: "",
      userId: 0
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
      var userId = 0;
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
        else if (decodeURIComponent(pair[0]) == "userId") {
            userId = parseInt(decodeURIComponent(pair[1]));
        }
      }

      var tempState = this.state.body;
      tempState.appId = appId;
      tempState.redirectUrl = redirectUrl;
      tempState.targetLocation = redirectUrl;
      tempState.userId = userId;
      tempState.modalState = (check !== null) ? -1 : 0;
      this.setState({body: tempState});
  }
    
  renderHeader () {
        return <Header
            logo={this.state.header.logo}
            title={this.state.header.title}
        />
  }
    
  renderDialog () {
      return <PassCheck
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
           userId={this.state.body.userId}
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