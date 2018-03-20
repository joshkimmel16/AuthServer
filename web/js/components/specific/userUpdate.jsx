const React = require('react');
const axios = require('axios');
const Q = require('q');
const $ = require('jquery');

class UserUpdate extends React.Component {
    constructor(options) {
        super();
        this.state = {
            "userId": 0,
            "username": {
              "description": options.username.description || "",
              "label": options.username.label || "",
              "regex": options.username.regex || /^$/,
              "value": options.username.value || "",
              "valid": options.username.valid || true,
              "errorText": options.username.errorText || ""
            },
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
            },
            "loginTitle": options.loginTitle || "",
            "metaTitle": options.metaTitle || "",
            "submitText": options.submitText || "",
            "failMessage": options.failMessage || "",
            "successMessage": options.successMessage || "",
            "modalState": options.modalState || 0,
            "mode": options.mode || 0,
            "nameAction": options.nameAction || "",
            "metaAction": options.metaAction || "",
        };
    }
    
    componentWillReceiveProps(nextProps) {
        var context = this;
        return Q(context.setState(nextProps))
            .then(() => context.setFieldValues());
    }
    
    setFieldValues ()
    {
        debugger;
        
        //set username
        $(".uNameInput").val(this.state.username.value);
        
        //set firstname
        $(".fNameInput").val(this.state.firstName.value);
        
        //set lastname
        $(".lNameInput").val(this.state.lastName.value);
        
        //set email
        $(".emailInput").val(this.state.email.value);
        
        //set rights
        $(".rInput").val(this.state.rights.value);
    }
    
    //method to capture user input
    handleInputChange (type, val) {
        var context = this;
        var tempObj = {};
        if (type === "user") {
            tempObj.username = context.state.username;
            tempObj.username.value = val;
        }
        else if (type === "first") {
            tempObj.firstName = context.state.firstName;
            tempObj.firstName.value = val;
        }
        else if (type === "last") {
            tempObj.lastName = context.state.lastName;
            tempObj.lastName.value = val;
        }
        else if (type === "email") {
            tempObj.email = context.state.email;
            tempObj.email.value = val;
        }
        else {
            tempObj.rights = context.state.rights;
            tempObj.rights.value = parseInt(val);
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
        else if (type === "first") {
            return Q(context.state.firstName.regex.test(context.state.firstName.value))
                .then(function(result) {
                    tempObj.firstName = context.state.firstName;
                    tempObj.firstName.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "last") {
            return Q(context.state.lastName.regex.test(context.state.lastName.value))
                .then(function(result) {
                    tempObj.lastName = context.state.lastName;
                    tempObj.lastName.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else if (type === "email") {
            return Q(context.state.email.regex.test(context.state.email.value))
                .then(function(result) {
                    tempObj.email = context.state.email;
                    tempObj.email.valid = result;
                    return Q(context.setState(tempObj));
                });
        }
        else {
            tempObj.rights = context.state.rights;
            if (context.state.rights.value !== "") {
                return Q(context.state.rights.options.find(function (element) {
                    return element.value === context.state.rights.value;
                }))
                .then(function(result) {
                    tempObj.rights.valid = (result !== undefined);
                    return Q(context.setState(tempObj));
                });
            }
            else {
                tempObj.rights.valid = false;
                return Q(context.setState(tempObj));
            }
        }
    }
    
    //POST to server-side user registration
    updateUser () {
        var context = this;
        return context.checkValidity("user")
            .then(context.checkValidity("first"))
            .then(context.checkValidity("last"))
            .then(context.checkValidity("email"))
            .then(context.checkValidity("rights"))
            .then(function () {
                if (context.state.username.valid === true && context.state.firstName.valid === true && context.state.lastName.valid === true && context.state.email.valid === true && context.state.rights.valid === true && context.state.mode === 0) {
                    context.setState({mode: 1});
                    var namePayload = {id: context.state.userId, name: context.state.username.value};
                    var metaPayload = {id: context.state.userId, metadata: {firstName: context.state.firstName.value, lastName: context.state.lastName.value, email: context.state.email.value, rights: parseInt(context.state.rights.value)}};
                    
                    var promises = [];
                    promises.push(axios({
                        method: "UPDATE",
                        url: context.state.nameAction,
                        data: namePayload,
                        headers: {
                            "X-Requested-With": "AJAX"
                        }
                    }));
                    promises.push(axios({
                        method: "UPDATE",
                        url: context.state.metaAction,
                        data: metaPayload,
                        headers: {
                            "X-Requested-With": "AJAX"
                        }
                    }));
                    
                    //TODO: should aggregate all errors and notify user if any call succeeds
                    Q.allSettled(promises)
                        .then(pArray => {
                            var check = true;
                            pArray.forEach((p) => {
                                if (check === true && p.state != "fulfilled") {
                                   check = false;
                                   context.handleResponse(p.value);
                               }
                            });
                            if (check === true) {
                                context.handleResponse(pArray[0].value);
                            }
                        });
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
                    </div>
                    <div className='metaInfo'>
                        <h2 className='ttl metaTitle'>{this.state.metaTitle}</h2>
                        <span className='desc fNameDesc'>{this.state.firstName.description}</span>
                        <label className='fNameLabel label' htmlFor='fName'>{this.state.firstName.label}</label>
                        <input type='text' id='fName' className='fNameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("first", e.target.value);}.bind(this)} />
                        <span className={'fNameError errorText ' + (this.state.firstName.valid === true ? 'hide' : '')}>{this.state.firstName.errorText}</span>
                        <span className='desc lNameDesc'>{this.state.lastName.description}</span>
                        <label className='lNameLabel label' htmlFor='lName'>{this.state.lastName.label}</label>
                        <input type='text' id='lName' className='lNameInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("last", e.target.value);}.bind(this)} />
                        <span className={'lNameError errorText ' + (this.state.lastName.valid === true ? 'hide' : '')}>{this.state.lastName.errorText}</span>
                        <span className='desc emailDesc'>{this.state.email.description}</span>
                        <label className='emailLabel label' htmlFor='email'>{this.state.email.label}</label>
                        <input type='text' id='email' className='emailInput form-control' disabled={this.state.mode === 1} onInput={function (e) {this.handleInputChange("email", e.target.value);}.bind(this)} />
                        <span className={'emailError errorText ' + (this.state.email.valid === true ? 'hide' : '')}>{this.state.email.errorText}</span>
                        <span className='desc rDesc'>{this.state.rights.description}</span>
                        <label className='rLabel label' htmlFor='rights'>{this.state.rights.label}</label>
                        <select id='rights' className='rInput form-control' disabled={this.state.mode === 1} onChange={function (e) {this.handleInputChange("rights", e.target.value);}.bind(this)}>
                            <option value=''></option>
                            {this.state.rights.options.map(function (opt, i) {
                                    return <option key={i} value={opt.value}>{opt.text}</option>
                                }
                            )}
                        </select>
                        <span className={'rError errorText ' + (this.state.rights.valid === true ? 'hide' : '')}>{this.state.rights.errorText}</span>
                    </div>
                    <button className='submit btn btn-default' disabled={this.state.mode === 1} onClick={function(e) {this.updateUser();}.bind(this)}>{this.state.submitText}</button>
                </div>
            </div>
        )
    }
}

module.exports = UserUpdate;