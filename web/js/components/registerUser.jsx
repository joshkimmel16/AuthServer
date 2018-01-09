// registerUser.jsx
const React = require("react");
const Header = require("./shared/Header.jsx");
const UserReg = require("./specific/userRegistration.jsx");
const data = {
  header: {
      title: "Register User",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg"   
  },
  body: {
      username: {
        description: "Please enter a username for the user being registered:",
        label: "Username:",
        regex: /^[A-Za-z0-9\.]+$/,
        errorText: "Invalid username. A valid username must contain only alphanumeric characters and '.'."
      },
      password: {
        description: "Please enter a password for the user being registered:",
        label: "Password:",
        regex: /^[A-Za-z0-9!@#\$%\^\&\*\(\)]+$/,
        errorText: "Invalid password. A valid password must contain only alphanumeric characters and '!@#$%^&*()'. Also, you must ensure that the two passwords match."
      },
      firstName: {
        description: "Please enter the user's first name:",
        label: "First Name:",
        regex: /^[A-Za-z\-']+$/,
        errorText: "Invalid entry. A valid entry must contain only letters, hyphens, and apostrophes."
      },
      lastName: {
        description: "Please enter the user's last name:",
        label: "Last Name:",
        regex: /^[A-Za-z\-']+$/,
        errorText: "Invalid entry. A valid entry must contain only letters, hyphens, and apostrophes."
      },
      email: {
        description: "Please enter the user's email address:",
        label: "Email:",
        regex: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
        errorText: "Invalid email. If you don't know what constitutes a valid email address, do some research."
      },
      rights: {
        description: "Please select the security type for the user being registered:",
        label: "Security Type:",
        options: [{value: 0, text: "Basic User"}, {value: 1, text: "Administrator"}],
        errorText: "Invalid security type. Please select an option from the list initially provided on the page."
      },
      loginTitle: "User Login Information",
      metaTitle: "Additional User Information",
      submitText: "Register",
      action: "/register/user",
      failMessage: "Registration failed!",
      successMessage: "User registered!"
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
        return <UserReg
           username={this.state.body.username}
           password={this.state.body.password}
           firstName={this.state.body.firstName}
           lastName={this.state.body.lastName}
           email={this.state.body.email}
           rights={this.state.body.rights}
           loginTitle={this.state.body.loginTitle}
           metaTitle={this.state.body.metaTitle}
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