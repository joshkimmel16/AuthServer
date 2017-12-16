from sys import path
import os
import AuthConfig
path.append(os.getcwd() + "\\bin")
import AuthJwt
import Statics
import Helpers
import Errors
import Sanitizer
from flask import Flask, request, jsonify, redirect, Response, make_response, render_template
from flask_cors import CORS

#global variable initialization
app = Flask(__name__, static_folder="../web/dist", template_folder="../web")
config = AuthConfig.Config().config
cors = CORS(app, resources={r"/*": {"origins": "*"}})
auth = AuthJwt.Authorizer(config)
statics = Statics.Statics(config)
s = Sanitizer.Sanitizer()
h = Helpers.Helpers()
AuthorizerException = AuthJwt.AuthorizerException
SanitizerException = Sanitizer.SanitizerException
StaticsException = Statics.StaticsException

#TODO: 
#implement server logging
#implement application id to secret cache
    #will require some modifications in AuthJwt
#implement access rights model for users

#define error handlers
@app.errorhandler(SanitizerException)
def sanitizer_exception(err):
    resp = jsonify({"error": err.message})
    resp.status_code = 400
    return resp

@app.errorhandler(AuthorizerException)
def authorization_exception(err):
    resp = jsonify({"error": err.message})
    resp.status_code = 500
    return resp

@app.errorhandler(StaticsException)
def statics_exception(err):
    resp = jsonify({"error": err.message})
    resp.status_code = 500
    return resp

@app.errorhandler(Exception)
def generic_exception(err):
    resp = jsonify({"error": "An unexpected error occurred!"})
    resp.status_code = 500
    return resp

@app.errorhandler(404)
def route_not_found(err):
    resp = jsonify({"error": "The requested route has not been implemented!"})
    resp.status_code = 404
    return resp

@app.errorhandler(405)
def method_not_allowed(err):
    resp = jsonify({"error": "The provided method is not valid for the given route!"})
    resp.status_code = 405
    return resp 

#get static web resources
@app.route('/dist/<path:path>', methods=['GET'])
def send_resource(path):
    return path

#user login web page
@app.route("/login/user", methods=['GET'])
def index ():
    return render_template("index.html")

@app.route("/authorize/session", methods=['POST'])
def authorize_session ():
    #check for JWT cookie
    jwt = request.cookies['jwt']
    content = request.get_json(force=True)
    app_id = content['app_id']
    redirect_url = content['redirect_url']
    
    try:
        #if there:
        if jwt is not None:
            #check if signature is valid and not expired
            token = auth.decrypt_token(jwt, app_id)
            check = auth.check_token_expiration(token['payload'])
            #if yes, redirect back with fail param
            if check is False:
                url = redirect_url + '?fail=token&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=token&appId=' + str(app_id)
                return redirect(url, code=302)
            #if no, redirect directly to provided URL
            else:
                url = redirect_url
                return redirect(url, code=302)
        #if not there:
        else:
            #missing token, so redirect back with fail param
            url = redirect_url + '?fail=token&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=token&appId=' + str(app_id)
            return redirect(url, code=302)
    except AuthorizerException as e:
        #redirect back with fail param, log error
        url = redirect_url + '?fail=token&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=token&appId=' + str(app_id)
        return redirect(url, code=302)
    except Exception as e:
        #redirect back with fail param, log error
        url = redirect_url + '?fail=app&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=app&appId=' + str(app_id)
        return redirect(url, code=302)  

#validates whether a provided username is registered
#no need to check JWT
#this route always responds with a 302 to either the password validation page (if success) or back to username validation page (if failure)
@app.route("/authorize/user", methods=['POST'])
def authorize_user ():
    try:
        content = request.get_json(force=True)
        username = content['username']
        app_id = content['app_id']
        redirect_url = content['redirect_url']
        
        s.Evaluate("authorize_user", content)
        check = auth.authorize_username(username)
        if check["valid"] is True:
            #user has been authorized, so redirect to password auth page
            url = redirect_url + '?userid=' + str(check["id"]) + '&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fuserid=' + str(check["id"]) + '&appId=' + str(app_id)
            return redirect(url, code=302)
        else:
            #user failed authorization, so redirect back with fail param
            url = redirect_url + '?fail=user&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=user&appId=' + str(app_id)
            return redirect(url, code=302)
    except SanitizerException as e:
        #can't assume the redirect URL was OK so respond with 400, log error
        raise e
    except AuthorizerException as e:
        #redirect back with fail param, log error
        url = redirect_url + '?fail=app&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=app&appId=' + str(app_id)
        return redirect(url, code=302)
    except Exception as e:
        #can't assume the redirect URL was OK so respond with 500, log error
        raise e

#validates whether a provided password is correct for the provided username
#no need to check JWT
#this route always responds with a 302 to either the provided redirect URL (if success) or back to username validation page (if failure)
@app.route("/authorize/password", methods=['POST'])
def authorize_password ():
    try:
        content = request.get_json(force=True)
        s.Evaluate("authorize_password", content)

        user_id = content['user_id']
        password = content['password']
        app_id = content['app_id']
        redirect_url = content['redirect_url']
        check = auth.authorize_password(user_id, password)
        if check["valid"] is True:
            #password is correct, so redirect to provided redirect URL and set cookie containing JWT and pass along usermetadata
            jwt = auth.provision_jwt(app_id, user_id)
            response = make_response(redirect(redirect_url))
            response.set_cookie('jwt', jwt)
            return response
        else:
            #user failed authorization, so redirect back with fail param
            url = redirect_url + '?fail=password&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=password&appId=' + str(app_id)
            return redirect(url, code=302)
    except SanitizerException as e:
        #can't assume the redirect URL was OK so respond with 400, log error
        raise e
    except AuthorizerException as e:
        #redirect back with fail param, log error
        url = redirect_url + '?fail=app&appId=' + str(app_id) if h.check_url(redirect_url) is False else redirect_url + '&fail=app&appId=' + str(app_id)
        return redirect(url, code=302)
    except Exception as e:
        #can't assume the redirect URL was OK so respond with 500, log error
        raise e

#registers an application
#no need to check JWT for this route
@app.route("/register/application", methods=['POST'])
def register_application ():
    try:
        content = request.get_json(force=True)
        s.Evaluate("register_application", content)
        
        app_name = content["name"]
        app_alg = content["algorithm"] if "algorithm" in content else None
        
        output = auth.register_application(app_name, app_alg)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("register_user", content)
        
        u_name = content["name"]
        u_password = content["password"]
        u_metadata = content["metadata"] if "metadata" in content else {}
        
        output = auth.register_user(u_name, u_password, u_metadata)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("retrieve_user", content)
        
        output = auth.retrieve_username(content)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("update_application", content)
        
        app_id = content["id"]
        app_name = content["name"] if "name" in content else None
        app_alg = content["algorithm"] if "algorithm" in content else None
        
        output = auth.update_application(app_id, app_name, app_alg)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("update_username", content)
        
        u_id = content["id"]
        u_name = content["name"]
        
        output = auth.update_username(u_id, u_name)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("update_password", content)
        
        u_id = content["id"]
        u_password = content["password"]
        
        output = auth.update_password(u_id, u_password)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("update_metadata", content)
        
        u_id = content["id"]
        u_metadata = content["metadata"]
        
        output = auth.update_metadata(u_id, u_metadata)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("unregister_application", content)
        
        app_id = content["id"]
        
        output = auth.unregister_application(app_id)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
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
        s.Evaluate("unregister_user", content)
        
        u_id = content["id"]
        
        output = auth.unregister_user(u_id)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
    except AuthorizerException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#creates a static asset
@app.route("/statics/create", methods=['POST'])
def create_asset ():
    try:
        content = request.get_json(force=True)
        s.Evaluate("create_asset", content)
        
        a_page = content["page"]
        a_component = content["component"]
        a_key = content["key"]
        a_value = content["value"]
        
        output = statics.create_asset(a_page, a_component, a_key, a_value)
        
        #respond with 200 and output in body
        resp = jsonify({"message": output})
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
    except StaticsException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
        
#gets all static assets for the given page
@app.route("/statics/get", methods=['GET'])
def get_assets ():
    try:
        content = request.get_json(force=True)
        s.Evaluate("get_assets", content)
        
        a_page = content["page"]
        
        output = statics.get_assets(a_page)
        
        #respond with 200 and output in body
        resp = jsonify(output)
        resp.status_code = 200
        return resp
    except SanitizerException as e:
        #respond with 400, specific error message
        raise e
    except StaticsException as e:
        #respond with 500, specific error message
        raise e
    except Exception as e:
        #respond with 500, generic error message
        raise e
    
#main application entry point
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config["server"]["port"])
