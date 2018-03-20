const React = require('react');

class Header extends React.Component {
    constructor(options) {
        super();
        this.state = {
            title: options.title || "",
            logo: options.logo || "",
            showLogin: options.showLogin || true,
            loginText: options.loginText || "",
            logoutText: options.logoutText || "",
            loginState: options.loginState || false,
            loginRedirect: options.loginRedirect || ""
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    logOut (cookie_name) {
        document.cookie = cookie_name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    
    handleLoginClick () {
        if (this.state.showLogin === true) {
            if (this.state.loginState === true)
            {
                this.logOut("jwt");  
            }
            window.location.href = this.state.loginRedirect;
        }
    }
    
    render () {
        return (
            <div className='header'>
                <img className='logo' src={this.state.logo} />
                <span className='title'>{this.state.title}</span>
                <a className={'loginLink ' + (this.state.showLogin ? '' : 'hide') } href="javascript:void(0)" onClick={function (e) {this.handleLoginClick();}.bind(this)}>{this.state.loginState === true ? this.state.logoutText : this.state.loginText}</a>
            </div>
        )
    }
}

module.exports = Header;