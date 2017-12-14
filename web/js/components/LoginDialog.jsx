const React = require('react');
const axios = require('axios');

class LoginDialog extends React.Component {
    constructor(options) {
        super();
        this.state = {
            type: options.type || "",
            inputLabel: options.inputLabel || "",
            inputRegex: options.inputRegex || "",
            message: options.message || "",
            submitText: options.submitText || "",
            errorText: options.errorText || "",
            value: "",
            valid: true,
            action: options.action || "",
            failMessage: options.failMessage || "",
            successMessage: options.successMessage || ""
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    //method to capture user input
    handleInputChange (val) {
        this.setState({value: val});
        this.checkValidity();
    }
    
    //validate the user input
    checkValidity () {
        this.setState({valid: this.state.inputRegex.test(this.state.value)});
    }
    
    //POST to server-side validation
    validateInput () {
        this.checkValidity();
        if (this.state.valid === true) {
            return;
        }
        return;
    }
    
    //handle various responses from server-side validation
    handleResponse () {
        return;
    }
    
    render () {
        return (
            <div className='background'>
                <div className='dialog'>
                    <span className='description'>{this.state.message}</span>
                    <label className='label' htmlFor='inputBox'>{this.state.inputLabel}</label>
                    <input type={this.state.type} id='inputBox' className='userInput' onChange={function (e) {this.handleInputChange(e.target.value);}.bind(this)} />
                    <span className={'errorText ' + (this.state.valid ? '' : 'hide')}>{this.state.errorText}</span>
                    <button className='submit' value={this.state.submitText} onClick={function(e) {this.validateInput();}.bind(this)} />
                </div>
            </div>
        )
    }
}

module.exports = LoginDialog;