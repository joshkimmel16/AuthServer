const React = require('react');
const axios = require('axios');
const Q = require('q');

class AppRegistration extends React.Component {
    constructor(options) {
        super();
        this.state = {
            "nameDescription": options.nameDescription || "",
            "nameLabel": options.nameLabel || "",
            "nameRegex": options.nameRegex || /^$/,
            "nameValue": options.nameValue || "",
            "nameValid": options.nameValid || true,
            "nameErrorHelp": options.nameErrorHelp || "",
            "algDescription": options.algDescription || "",
            "algLabel": options.algLabel || "",
            "algOptions": options.algOptions || [],
            "algValue": options.algValue || "",
            "algValid": options.algValid || true,
            "algErrorHelp": options.algErrorHelp || "",
            "submitText": options.submitText || "",
            "failMessage": options.failMessage || "",
            "successMessage": options.successMessage || "",
            "modalState": options.modalState || 0,
            "secret": options.secret || "",
            "mode": options.mode || 0,
            "action": options.action || ""
        };
    }
    
    componentWillReceiveProps(nextProps) {
        this.setState(nextProps);
    }
    
    //method to capture user input
    handleInputChange (type, val) {
        var context = this;
        var tempObj = (type === "name") ? {nameValue: val} : {algValue: val};
        return Q(context.setState(tempObj))
            .then(function () {
                return context.checkValidity(type);
            });
    }
    
    //validate the user input
    checkValidity (type) {
        var context = this;
        if (type === "name") {
            return Q(context.state.nameRegex.test(context.state.nameValue))
                .then(function(result) {
                    return Q(context.setState({nameValid: result}));
                });
        }
        else {
            if (context.state.algValue !== "") {
                return Q(context.state.algOptions.find(function (element) {
                    return element.value === context.state.algValue;
                }))
                .then(function(result) {
                   return Q(context.setState({algValid: (result !== undefined)}));
                });
            }
            else {
                return Q(context.setState({algValid: false}));
            }
        }
    }
    
    //POST to server-side app registration
    registerApp () {
        var context = this;
        return context.checkValidity("name")
            .then(context.checkValidity("alg"))
            .then(function () {
                if (context.state.nameValid === true && context.state.algValid === true && context.state.mode === 0) {
                    context.setState({mode: 1});
                    var payload = {name: context.state.nameValue, algorithm: context.state.algValue};
                    axios.post(context.state.action, payload, {headers: {"X-Requested-With": "AJAX"}})
                        .then(function(response) { context.handleResponse(response); })
                        .catch(function(error) { context.handleResponse(error.response); });
                }
            });
    }
    
    //handle various responses from server-side registration
    handleResponse (response) {
        var context = this;
        if (response.status === 200) {
            var secret = response.data.secret;
            var msg = context.state.successMessage + secret;
            context.setState({modalState: 1, successMessage: msg, secret: secret});
        }
        else if (response.status >= 400) {
            context.setState({failMessage: context.state.failMessage + ' Error: ' + response.data.error, modalState: -1, mode: 0});
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
                    <span className='desc nameDesc'>{this.state.nameDescription}</span>
                    <label className='nameLabel label' htmlFor='name'>{this.state.nameLabel}</label>
                    <input type='text' id='name' className='nameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("name", e.target.value);}.bind(this)} />
                    <span className={'nameError errorText ' + (this.state.nameValid === true ? 'hide' : '')}>{this.state.nameErrorHelp}</span>
                    <span className='desc algDesc'>{this.state.algDescription}</span>
                    <label className='algLabel label' htmlFor='alg'>{this.state.algLabel}</label>
                    <select id='alg' className='algInput form-control' disabled={this.state.mode === 1} onChange={function (e) {this.handleInputChange("alg", e.target.value);}.bind(this)}>
                        <option value=''></option>
                        {this.state.algOptions.map(function (opt, i) {
                                return <option key={i} value={opt.value}>{opt.text}</option>
                            }
                        )}
                    </select>
                    <span className={'algError errorText ' + (this.state.algValid === true ? 'hide' : '')}>{this.state.algErrorHelp}</span>
                    <button className='submit btn btn-default' disabled={this.state.nameValid === false || this.state.algValid === false || this.state.mode === 1} onClick={function(e) {this.registerApp();}.bind(this)}>{this.state.submitText}</button>
                </div>
            </div>
        )
    }
}

module.exports = AppRegistration;