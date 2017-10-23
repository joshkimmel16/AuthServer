from sys import path
import os
import AuthConfig
path.append(os.getcwd() + "\\bin")
import AuthJwt
import Helpers
import Errors
from flask import Flask, request, jsonify, redirect, Response
from flask_cors import CORS

#global variable initialization
app = Flask(__name__)
config = AuthConfig.Config().config
cors = CORS(app, resources={r"/*": {"origins": "*"}})
auth = AuthJwt.Authorizer(config)
AuthorizerException = AuthJwt.AuthorizerException

#TODO: 
#implement input sanitizer => 400 response
#implement server logging
#implement application id to secret cache
    #will require some modifications in AuthJwt
#implement access rights model for users

#define error handlers
#NOT WORKING??
@app.errorhandler(AuthorizerException)
def authorization_exception(err):
    resp = jsonify({"error": err.message})
    resp.status = 500
    return resp

#NOT WORKING??
@app.errorhandler(Exception)
def generic_exception(err):
    resp = jsonify({"error": "An unexpected error occurred!"})
    resp.status = 500
    return resp

#NOT WORKING
@app.errorhandler(404)
def route_not_found(err):
    resp = jsonify({"error": "The requested route has not been implemented!"})
    resp.status = 404
    return resp

#NOT WORKING
@app.errorhandler(405)
def method_not_allowed(err):
    resp = jsonify({"error": "The provided method is not valid for the given route!"})
    resp.status = 405
    return resp

'''
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
'''        

#registers an application
#no need to check JWT for this route
@app.route("/register/application", methods=['POST'])
def register_application ():
    try:
        content = request.get_json(force=True)
        app_name = content["name"]
        app_alg = content["algorithm"] if "algorithm" in content else None
        
        output = auth.register_application(app_name, app_alg)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#registers an application
#no need to check JWT for this route
@app.route("/register/user", methods=['POST'])
def register_user ():
    try:
        content = request.get_json(force=True)
        u_name = content["name"]
        u_password = content["password"]
        u_metadata = content["metadata"] if "metadata" in content else {}
        
        output = auth.register_user(u_name, u_password, u_metadata)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
@app.route("/retrieve/user", methods=['GET'])
def retrieve_user ():
    try:
        content = request.get_json(force=True)
        
        output = auth.retrieve_username(content)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#updates an application
#no need to check JWT for this route
@app.route("/update/application", methods=['UPDATE'])
def update_application ():
    try:
        content = request.get_json(force=True)
        app_id = content["id"]
        app_name = content["name"] if "name" in content else None
        app_alg = content["algorithm"] if "algorithm" in content else None
        
        output = auth.update_application(app_id, app_name, app_alg)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#updates a user's username
#no need to check JWT for this route
@app.route("/update/username", methods=['UPDATE'])
def update_username ():
    try:
        content = request.get_json(force=True)
        u_id = content["id"]
        u_name = content["name"]
        
        output = auth.update_username(u_id, u_name)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#updates a user's password
#no need to check JWT for this route
@app.route("/update/password", methods=['UPDATE'])
def update_password ():
    try:
        content = request.get_json(force=True)
        u_id = content["id"]
        u_password = content["password"]
        
        output = auth.update_password(u_id, u_password)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#updates a user's metadata
#no need to check JWT for this route
@app.route("/update/metadata", methods=['UPDATE'])
def update_metadata ():
    try:
        content = request.get_json(force=True)
        u_id = content["id"]
        u_metadata = content["metadata"]
        
        output = auth.update_metadata(u_id, u_metadata)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#unregisters an application
#no need to check JWT for this route
@app.route("/unregister/application", methods=['DELETE'])
def unregister_application ():
    try:
        content = request.get_json(force=True)
        app_id = content["id"]
        
        output = auth.unregister_application(app_id)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#unregisters a user
#no need to check JWT for this route
@app.route("/unregister/user", methods=['DELETE'])
def unregister_user ():
    try:
        content = request.get_json(force=True)
        u_id = content["id"]
        
        output = auth.unregister_user(u_id)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
    
#main application entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config["port"])
