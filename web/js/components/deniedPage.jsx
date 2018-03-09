// userApp.jsx
const React = require("react");
const Header = require("./shared/Header.jsx");
const data = {
  header: {
      title: "Access Denied",
      logo: "/dist/248f90e02f291ea0913c525495353369.jpg"   
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
  }
    
  renderHeader () {
        return <Header
            logo={this.state.header.logo}
            title={this.state.header.title}
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
