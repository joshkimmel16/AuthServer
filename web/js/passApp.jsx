// passApp.jsx
const React = require("react");
const Header = require("./components/Header.jsx");
const PassCheck = require("./components/LoginDialog.jsx");
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
      appId: 1
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
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == "fail") {
            check = decodeURIComponent(pair[1]);
        }
      }

      if (check !== null) {
          var tempState = this.state.body;
          tempState.modalState = -1;
          this.setState({body: tempState});
      }
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