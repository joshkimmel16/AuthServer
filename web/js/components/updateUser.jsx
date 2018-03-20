// updateUser.jsx
const axios = require('axios');
const React = require("react");
const Header = require("./shared/Header.jsx");
const UserReg = require("./specific/userUpdate.jsx");
const data = {
  header: {
      title: "Update User Information",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg",
      showLogin: true,
      loginText: "Log In",
      logoutText: "Log Out",
      loginState: true,
      loginRedirect: "/login/user?appId=1"
  },
  body: {
      userId: 0, //HOW TO GET THIS FROM THE TEMPLATE BEING RENDERED
      username: {
        description: "If you would like to change the username, please do so here:",
        label: "Username:",
        regex: /^[A-Za-z0-9\.]+$/,
        errorText: "Invalid username. A valid username must contain only alphanumeric characters and '.'.",
        value: "",
        valid: true
      },
      firstName: {
        description: "Please enter the user's first name:",
        label: "First Name:",
        regex: /^[A-Za-z\-']+$/,
        errorText: "Invalid entry. A valid entry must contain only letters, hyphens, and apostrophes.",
        value: "",
        valid: true
      },
      lastName: {
        description: "Please enter the user's last name:",
        label: "Last Name:",
        regex: /^[A-Za-z\-']+$/,
        errorText: "Invalid entry. A valid entry must contain only letters, hyphens, and apostrophes.",
        value: "",
        valid: true
      },
      email: {
        description: "Please enter the user's email address:",
        label: "Email:",
        regex: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
        errorText: "Invalid email. If you don't know what constitutes a valid email address, do some research.",
        value: "",
        valid: true
      },
      rights: {
        description: "Please select the security type for the user being registered:",
        label: "Security Type:",
        options: [{value: 0, text: "Basic User"}, {value: 1, text: "Administrator"}],
        errorText: "Invalid security type. Please select an option from the list initially provided on the page.",
        value: "",
        valid: true
      },
      loginTitle: "User Login Information",
      metaTitle: "Additional User Information",
      submitText: "Update",
      nameAction: "/update/username",
      metaAction: "/update/metadata",
      failMessage: "User update failed!",
      successMessage: "User updated!"
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
            tempState.username.value = response.data.username;
            var met = JSON.parse(response.data.metadata);
            tempState.firstName.value = met.firstName;
            tempState.lastName.value = met.lastName;
            tempState.email.value = met.email;
            tempState.rights.value = met.rights;
            
            context.setState({body: tempState});
        })
        .catch(function(error) {
            tempState.failMessage = "Could not retrieve the given user's information!";
            tempState.modalState = -1;
            tempState.mode = 1;
            context.setState({body: tempState});
        });
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
        return <UserReg
           userId={this.state.body.userId}
           username={this.state.body.username}
           firstName={this.state.body.firstName}
           lastName={this.state.body.lastName}
           email={this.state.body.email}
           rights={this.state.body.rights}
           loginTitle={this.state.body.loginTitle}
           metaTitle={this.state.body.metaTitle}
           submitText={this.state.body.submitText}
           nameAction={this.state.body.nameAction}
           metaAction={this.state.body.metaAction}
           failMessage={this.state.body.failMessage}
           successMessage={this.state.body.successMessage}
           modalState={(this.state.body.modalState != null) ? this.state.body.modalState : 0}
           mode={(this.state.body.mode != null) ? this.state.body.mode : 0}
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