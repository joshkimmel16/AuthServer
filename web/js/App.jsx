// App.jsx
const React = require("react");
const Header = require("./components/Header.jsx");
const data = {
  title: "User Login",
  logo: "/styles/img/logo.png"
};

class App extends React.Component {
  constructor() {
        super();
        this.state = {
            header: data
        };
  }
    
  renderHeader () {
        return <Header
            logo={this.state.header.logo}
            title={this.state.header.title}
        />
  }
    
  render () {
    return (
            <div className='main'>
                {this.renderHeader()}
            </div>
        )
  }
}

module.exports = App;