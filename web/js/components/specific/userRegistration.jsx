const React = require('react');
const axios = require('axios');
const Q = require('q');

class UserRegistration extends React.Component {
    constructor(options) {
        super();
        this.state = {
            "username": {
              "description": options.username.description || "",
              "label": options.username.label || "",
              "regex": options.username.regex || /^$/,
              "value": options.username.value || "",
              "valid": options.username.valid || true,
              "errorText": options.username.errorText || ""
            },
            "password": {
              "description1": options.password.description1 || "",
              "description2": options.password.description2 || "",
              "label1": options.password.label1 || "",
              "label2": options.password.label2 || "",
              "regex": options.password.regex || /^$/,
              "value1": options.password.value1 || "",
              "value2": options.password.value2 || "",
              "valid1": options.password.valid1 || true,
              "valid2": options.password.valid2 || true,
              "errorText1": options.password.errorText1 || "",
              "errorText2": options.password.errorText2 || ""
            },
            "metadata": {
                "firstName": {
                  "description": options.firstName.description || "",
                  "label": options.firstName.label || "",
                  "regex": options.firstName.regex || /^$/,
                  "value": options.firstName.value || "",
                  "valid": options.firstName.valid || true,
                  "errorText": options.firstName.errorText || ""
                },
                "lastName": {
                  "description": options.lastName.description || "",
                  "label": options.lastName.label || "",
                  "regex": options.lastName.regex || /^$/,
                  "value": options.lastName.value || "",
                  "valid": options.lastName.valid || true,
                  "errorText": options.lastName.errorText || ""
                },
                "email": {
                  "description": options.email.description || "",
                  "label": options.email.label || "",
                  "regex": options.email.regex || /^$/,
                  "value": options.email.value || "",
                  "valid": options.email.valid || true,
                  "errorText": options.email.errorText || ""
                },
                "rights": {
                  "description": options.rights.description || "",
                  "label": options.rights.label || "",
                  "options": options.rights.options || [],
                  "value": options.rights.value || "",
                  "valid": options.rights.valid || true,
                  "errorText": options.rights.errorText || ""
                }
            },
            "loginTitle": options.loginTitle || "",
            "metaTitle": options.metaTitle || "",
            "submitText": options.submitText || "",
            "failMessage": options.failMessage || "",
            "successMessage": options.successMessage || "",
            "modalState": options.modalState || 0,
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
        var tempObj = {};
        if (type === "user") {
            tempObj.username = context.state.username;
            tempObj.username.value = val;
        }
        else if (type === "pass1") {
            tempObj.password = context.state.password;
            tempObj.password.value1 = val;
        }
        else if (type === "pass2") {
            tempObj.password = context.state.password;
            tempObj.password.value2 = val;
        }
        else if (type === "first") {
            tempObj.metadata = context.state.metadata;
            tempObj.metadata.firstName.value = val;
        }
        else if (type === "last") {
            tempObj.metadata = context.state.metadata;
            tempObj.metadata.lastName.value = val;
        }
        else if (type === "email") {
            tempObj.metadata = context.state.metadata;
            tempObj.metadata.email.value = val;
        }
        else {
            tempObj.metadata = context.state.metadata;
            tempObj.metadata.rights.value = parseInt(val);
        }
        return Q(context.setState(tempObj))
            .then(function () {
                return context.checkValidity(type);
            });
    }
    
    //validate the user input
    checkValidity (type) {
        var context = this;
        var tempObj = {};
        if (type === "user") {
            return Q(context.state.username.regex.test(context.state.username.value))
                .then(function(result) {
                    tempObj.username = context.state.username;
                    tempObj.username.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "pass1") {
            return Q(context.state.password.regex.test(context.state.password.value1))
                .then(function(result) {
                    tempObj.password = context.state.password;
                    tempObj.password.valid1 = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "pass2") {
            return Q(function () {return context.state.password.value1 === context.state.password.value2;}())
                .then(function(result) {
                    tempObj.password = context.state.password;
                    tempObj.password.valid2 = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "first") {
            return Q(context.state.metadata.firstName.regex.test(context.state.metadata.firstName.value))
                .then(function(result) {
                    tempObj.metadata = context.state.metadata;
                    tempObj.metadata.firstName.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "last") {
            return Q(context.state.metadata.lastName.regex.test(context.state.metadata.lastName.value))
                .then(function(result) {
                    tempObj.metadata = context.state.metadata;
                    tempObj.metadata.lastName.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "email") {
            return Q(context.state.metadata.email.regex.test(context.state.metadata.email.value))
                .then(function(result) {
                    tempObj.metadata = context.state.metadata;
                    tempObj.metadata.email.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else {
            tempObj.metadata = context.state.metadata;
            if (context.state.metadata.rights.value !== "") {
                return Q(context.state.metadata.rights.options.find(function (element) {
                    return element.value === context.state.metadata.rights.value;
                }))
                .then(function(result) {
                    debugger;
                    tempObj.metadata.rights.valid = (result !== undefined);
                    return Q(context.setState(tempObj));
                });
            }
            else {
                tempObj.metadata.rights.valid = false;
                return Q(context.setState(tempObj));
            }
        }
    }
    
    //POST to server-side user registration
    registerUser () {
        var context = this;
        return context.checkValidity("user")
            .then(context.checkValidity("pass1"))
            .then(context.checkValidity("pass2"))
            .then(context.checkValidity("first"))
            .then(context.checkValidity("last"))
            .then(context.checkValidity("email"))
            .then(context.checkValidity("rights"))
            .then(function () {
                if (context.state.username.valid === true && context.state.password.valid1 === true && context.state.password.valid2 === true && context.state.metadata.firstName.valid === true && context.state.metadata.lastName.valid === true && context.state.metadata.email.valid === true && context.state.metadata.rights.valid === true && context.state.mode === 0) {
                    context.setState({mode: 1});
                    var payload = {name: context.state.username.value, password: context.state.password.value1, metadata: {firstName: context.state.metadata.firstName.value, lastName: context.state.metadata.lastName.value, email: context.state.metadata.email.value, rights: parseInt(context.state.metadata.rights.value)}};
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
            context.setState({modalState: 1});
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
                    <div className='loginInfo'>
                        <h2 className='ttl loginTitle'>{this.state.loginTitle}</h2>
                        <span className='desc uNameDesc'>{this.state.username.description}</span>
                        <label className='uNameLabel label' htmlFor='uName'>{this.state.username.label}</label>
                        <input type='text' id='uName' className='uNameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("user", e.target.value);}.bind(this)} />
                        <span className={'uNameError errorText ' + (this.state.username.valid === true ? 'hide' : '')}>{this.state.username.errorText}</span>
                        <span className='desc p1Desc'>{this.state.password.description1}</span>
                        <label className='p1Label label' htmlFor='p1'>{this.state.password.label1}</label>
                        <input type='password' id='p1' className='p1Input form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("pass1", e.target.value);}.bind(this)} />
                        <span className={'p1Error errorText ' + (this.state.password.valid1 === true ? 'hide' : '')}>{this.state.password.errorText1}</span>
                        <span className='desc p2Desc'>{this.state.password.description2}</span>
                        <label className='p2Label label' htmlFor='p2'>{this.state.password.label2}</label>
                        <input type='password' id='p2' className='p2Input form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("pass2", e.target.value);}.bind(this)} />
                        <span className={'p2Error errorText ' + (this.state.password.valid2 === true ? 'hide' : '')}>{this.state.password.errorText2}</span>
                    </div>
                    <div className='metaInfo'>
                        <h2 className='ttl metaTitle'>{this.state.metaTitle}</h2>
                        <span className='desc fNameDesc'>{this.state.metadata.firstName.description}</span>
                        <label className='fNameLabel label' htmlFor='fName'>{this.state.metadata.firstName.label}</label>
                        <input type='text' id='fName' className='fNameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("first", e.target.value);}.bind(this)} />
                        <span className={'fNameError errorText ' + (this.state.metadata.firstName.valid === true ? 'hide' : '')}>{this.state.metadata.firstName.errorText}</span>
                        <span className='desc lNameDesc'>{this.state.metadata.lastName.description}</span>
                        <label className='lNameLabel label' htmlFor='lName'>{this.state.metadata.lastName.label}</label>
                        <input type='text' id='lName' className='lNameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("last", e.target.value);}.bind(this)} />
                        <span className={'lNameError errorText ' + (this.state.metadata.lastName.valid === true ? 'hide' : '')}>{this.state.metadata.lastName.errorText}</span>
                        <span className='desc emailDesc'>{this.state.metadata.email.description}</span>
                        <label className='emailLabel label' htmlFor='email'>{this.state.metadata.email.label}</label>
                        <input type='text' id='email' className='emailInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("email", e.target.value);}.bind(this)} />
                        <span className={'emailError errorText ' + (this.state.metadata.email.valid === true ? 'hide' : '')}>{this.state.metadata.email.errorText}</span>
                        <span className='desc rDesc'>{this.state.metadata.rights.description}</span>
                        <label className='rLabel label' htmlFor='rights'>{this.state.metadata.rights.label}</label>
                        <select id='rights' className='rInput form-control' disabled={this.state.mode === 1} onChange={function (e) {this.handleInputChange("rights", e.target.value);}.bind(this)}>
                            <option value=''></option>
                            {this.state.metadata.rights.options.map(function (opt, i) {
                                    return <option key={i} value={opt.value}>{opt.text}</option>
                                }
                            )}
                        </select>
                        <span className={'rError errorText ' + (this.state.metadata.rights.valid === true ? 'hide' : '')}>{this.state.metadata.rights.errorText}</span>
                    </div>
                    <button className='submit btn btn-default' disabled={this.state.nameValid === false || this.state.algValid === false || this.state.mode === 1} onClick={function(e) {this.registerUser();}.bind(this)}>{this.state.submitText}</button>
                </div>
            </div>
        )
    }
}

module.exports = UserRegistration;