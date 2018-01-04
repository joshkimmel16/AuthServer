const React = require('react');

class Header extends React.Component {
    constructor(options) {
        super();
        this.state = {
            title: options.title || "",
            logo: options.logo || ""
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    render () {
        return (
            <div className='header'>
                <img className='logo' src={this.state.logo} />
                <span className='title'>{this.state.title}</span>
            </div>
        )
    }
}

module.exports = Header;