// registerApp.jsx
const React = require("react");
const Header = require("./components/Header.jsx");
const AppReg = require("./components/appRegistration.jsx");
const data = {
  header: {
      title: "Register Application",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg"   
  },
  body: {
      nameDescription: "Please enter a name for the application being registered:",
      nameLabel: "Name:",
      nameRegex: /^[A-Za-z0-9 ]+$/,
      nameErrorHelp: "Invalid application name. A valid name must contain only alphanumeric characters and/or spaces.",
      algDescription: "Please select an algorithm to be used for encryption from the list below:",
      algLabel: "Algorithm:",
      algOptions: [{value: "HS256", text: "HMAC"}, {value: "RSA", text: "RSA"}],
      algErrorHelp: "Invalid algorithm. Please select an option from the list initially provided on the page.",
      submitText: "Register",
      action: "/register/application",
      failMessage: "Registration failed!",
      successMessage: "Application registered! The secret below is unique to your application and necessary for token decryption - do not lose it! Secret: ",
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
    
  renderHeader () {
        return <Header
            logo={this.state.header.logo}
            title={this.state.header.title}
        />
  }
    
  renderDialog () {
      return <AppReg
           nameDescription={this.state.body.nameDescription}
           nameLabel={this.state.body.nameLabel}
           nameRegex={this.state.body.nameRegex}
           nameErrorHelp={this.state.body.nameErrorHelp}
           algDescription={this.state.body.algDescription}
           algLabel={this.state.body.algLabel}
           algOptions={this.state.body.algOptions}
           algErrorHelp={this.state.body.algErrorHelp}
           submitText={this.state.body.submitText}
           action={this.state.body.action}
           failMessage={this.state.body.failMessage}
           successMessage={this.state.body.successMessage}
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

