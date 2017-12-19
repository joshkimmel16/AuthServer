const React = require('react');
const axios = require('axios');
const Q = require('q');

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
            successMessage: options.successMessage || "",
            modalState: options.modalState || 0,
            appId: options.appId || 0
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    //method to capture user input
    handleInputChange (val) {
        var context = this;
        return Q(context.setState({value: val}))
            .then(function () {
                return context.checkValidity();
            });
    }
    
    //validate the user input
    checkValidity () {
        var context = this;
        return Q(context.state.inputRegex.test(context.state.value))
            .then(function(result) {
                return Q(context.setState({valid: result}));
            });
    }
    
    //POST to server-side validation
    validateInput () {
        var context = this;
        return context.checkValidity()
            .then(function () {
                if (context.state.valid === true) {
                    var payload = {username: context.state.value, app_id: context.state.appId, redirect_url: window.location.href.split(/[?#]/)[0]};
                    axios.post(context.state.action, payload, {headers: {"X-Requested-With": "AJAX"}})
                        .then(function(response) { context.handleResponse(response); })
                        .catch(function(error) { context.handleResponse(error.response); });
                }
            });
    }
    
    //handle various responses from server-side validation
    handleResponse (response) {
        var context = this;
        if (response.status === 200) {
            var target = response.data.url;
            window.location.href = target;
        }
        else if (response.status >= 400) {
            context.setState({failMessage: context.state.failMessage + ' Error: ' + response.data.error, modalState: -1});
        }
    }
    
    render () {
        return (
            <div className='background'>
                <div className={'success alert alert-success ' + (this.state.modalState === 1 ? '' : 'hide')}>
                    <strong>Success! </strong>{this.state.successMessage}
                </div>
                <div className={'fail alert alert-danger ' + (this.state.modalState === -1 ? '' : 'hide')}>
                    <strong>Oops! </strong>{this.state.failMessage}
                </div>
                <div className='dialog'>
                    <span className='description'>{this.state.message}</span>
                    <label className='label' htmlFor='inputBox'>{this.state.inputLabel}</label>
                    <input type={this.state.type} id='inputBox' className='userInput form-control' onInput={function (e) {this.handleInputChange(e.target.value);}.bind(this)} />
                    <span className={'errorText ' + (this.state.valid === true ? 'hide' : '')}>{this.state.errorText}</span>
                    <button className='submit btn btn-default' disabled={this.state.valid === false} onClick={function(e) {this.validateInput();}.bind(this)}>{this.state.submitText}</button>
                </div>
            </div>
        )
    }
}

module.exports = LoginDialog;