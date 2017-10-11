import AuthJwt
import Helpers
import Errors
import Config
from flask import Flask, request, jsonify, redirect

#global variable initialization
app = Flask(__name__)
config = Config.Config()
auth = AuthJwt.Authorizer(config)

#TODO: implement 400 response checking

@app.route("/authorize/session", methods=['GET'])
def authorize_session ():
    #check for JWT cookie
    jwt = request.cookies['jwt']
    app_name = request.args.get('appName')
    redirect_url = request.args.get('redirectUrl')
    
    try:
        #if there:
        if jwt is not None:
            #check if expired
            token = auth.decrypt_token(jwt, app_name)
            check = auth.check_token_expiration(token['payload'])
            #if yes, redirect to user sign in page (passing along redirect URL)
            if check is False:
                url = config.user_signin + '?appName=' + app_name + '&redirectUrl=' + redirect_url
                return redirect(url, code=302)
            #if no, redirect directly to provided URL
            else:
                return redirect(redirect_url, code=302)
        #if not there:
        else:
            #redirect to user sign in page (passing along redirect URL)
            url = config.user_signin + '?appName=' + app_name + '&redirectUrl=' + redirect_url
            return redirect(url, code=302)
    except AuthorizerException as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&appName=' + app_name + '&redirectUrl=' + redirect_url
        return redirect(url, code=302)
    except Exception as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&appName=' + app_name + '&redirectUrl=' + redirect_url
        return redirect(url, code=302)
        

@app.route("/authorize/user", methods=['POST'])
def authorize_user ():
    content = request.get_json(force=True)
    username = content['username']
    app_name = content['app_name']
    redirect_url = request.args.get('redirectUrl')
    try:
        check = auth.authorize_username(username)
        if check is True:
            #user has been authorized, so redirect to password auth page
            url = config.password_signin + '?username=' + username + '&appName=' + app_name + '&redirectUrl=' + redirect_url
            return redirect(url, code=302)
        else:
            #user failed authorization, so redirect back to user sign in page with fail param
            url = config.user_signin + '?fail=user&appName=' + app_name + '&redirectUrl=' + redirect_url
            return redirect(url, code=302)
    except AuthorizerException as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&appName=' + app_name + '&redirectUrl=' + redirect_url
        return redirect(url, code=302)
    except Exception as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&appName=' + app_name + '&redirectUrl=' + redirect_url
        return redirect(url, code=302)


@app.route("/authorize/password", methods=['POST'])
def authorize_password ():
    content = request.get_json(force=True)
    username = content['username']
    password = content['password']
    app_name = content['app_name']
    redirect_url = request.args.get('redirectUrl')
    try:
        check = auth.authorize_username(username, password)
        if check[0] is True:
            #password is correct, so redirect to provided redirect URL and set cookie containing JWT and pass along usermetadata
            jwt = auth.provision_jwt(app_name, username)
            response.set_cookie('jwt', value=jwt)
            url = redirect_url + '&usermetadata=' + check[1]
            return redirect(url, code=302)
        else:
            #user failed authorization, so redirect back to user sign in page with fail param
            url = config.user_signin + '?fail=password&redirectUrl=' + redirect_url
            return redirect(url, code=302)
    except AuthorizerException as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&redirectUrl=' + redirect_url
        return redirect(url, code=302)
    except Exception as e:
        #redirect back to user sign in page with fail param, log error
        url = config.user_signin + '?fail=app&redirectUrl=' + redirect_url
        return redirect(url, code=302)
        

@app.route("/register/application", methods=['POST', 'DELETE'])
def set_app_registration ():
    #register application
    if request.method == 'POST':
        content = request.get_json(force=True)
        app_name = content['app_name']
        try:
            secret = auth.register_application(app_name)
            #respond with 200 and secret + app_name in response body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error
        
    #unregister application
    else:
        app_name = request.args.get('app_name')
        try:
            check = auth.unregister_application(app_name)
            #respond with 200 and no body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error
            
@app.route("/register/user", methods=['POST', 'DELETE'])    
def set_user_registration ():
    #register user
    if request.method == 'POST':
        content = request.get_json(force=True)
        username = content['username']
        password = content['password']
        usermetadata = content['usermetadata']
        try:
            check = auth.register_user(username, password, usermetadata)
            #respond with 200 and username in response body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error
        
    #unregister user
    else:
        username = request.args.get('username')
        try:
            check = auth.unregister_user(username)
            #respond with 200 and no body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error
            
            
@app.route("/user", methods=['GET', 'UPDATE'])
def update_user ():
    #retrieve username
    if request.method == 'GET':
        usermetadata = request.args.get('usermetadata')
        try:
            username = auth.retrieve_username(usermetadata)
            #respond with 200 and username in response body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error
            
    #update metadata and/or password
    else:
        content = request.get_json(force=True)
        username = content['username']
        new_password = content['password'] if 'password' in content else None
        metadata = content['usermetadata'] if 'usermetadata' in content else None
        
        try:
            if new_password is not None:
                check1 = auth.update_password(username, new_password)
            if metadata is not None:
                check2 = auth.update_metadata(username, metadata)
                
            #respond with 200 and username in response body
        except AuthorizerException as e:
            #respond with 500, log error
        except Exception as e:
            #respond with 500, log error

