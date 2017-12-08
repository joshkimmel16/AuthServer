import re
from Errors import Error

#TODO:
#implement remaining sanitization methods for active routes
#push sanitization patterns/checks into config?
#implement method to validate usermetadata - use config?

class Sanitizer:
    
    #constructor
    def __init__ (self):
        self.funcs = {}
        self.funcs["authorize_user"] = self.authorize_user
        self.funcs["authorize_password"] = self.authorize_password
        self.funcs["register_application"] = self.register_application
        self.funcs["update_application"] = self.update_application
        self.funcs["unregister_application"] = self.unregister_application
        self.funcs["register_user"] = self.register_user
        self.funcs["retrieve_user"] = self.retrieve_user
        self.funcs["update_username"] = self.update_username
        self.funcs["update_password"] = self.update_password
        self.funcs["update_metadata"] = self.update_metadata
        self.funcs["unregister_user"] = self.unregister_user
        self.funcs["create_asset"] = self.create_asset
        self.funcs["get_assets"] = self.get_assets
    
    #main function to evaluate the legitimacy of inputs to a given route
    def Evaluate (self, route, body):
        if route in self.funcs:
            return self.funcs[route](body)
        else:
            raise SanitizerException("The requested route does not have an implemented validator!", "Evaluate", None)
            
    #validate inputs to /authorize/user
    def authorize_user (self, body):
        try:
            if 'username' in body:
                name_pattern = re.compile("^[A-Za-z0-9\.]+$")
                if not isinstance(body["username"], str) or name_pattern.match(body["username"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'username'!", "authorize_user", None)
            else:
                raise SanitizerException("Missing required paramater 'username'!", "authorize_user", None)
            if 'app_id' in body:
                if not isinstance(body["app_id"], int) or body["app_id"] < 1:
                    raise SanitizerException("Invalid value provided for parameter 'app_id'!", "authorize_user", None)
            else:
                raise SanitizerException("Missing required paramater 'app_id'!", "authorize_user", None)
            if 'redirect_url' in body:
                url_pattern = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)")
                if not isinstance(body["redirect_url"], str) or url_pattern.match(body["redirect_url"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'redirect_url'!", "authorize_user", None)
            else:
                raise SanitizerException("Missing required paramater 'redirect_url'!", "authorize_user", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "authorize_user", e)
            
    #validate inputs to /authorize/user
    def authorize_password (self, body):
        try:
            if 'user_id' in body:
                if not isinstance(body["user_id"], int) or body["user_id"] < 1:
                    raise SanitizerException("Invalid value provided for parameter 'user_id'!", "authorize_password", None)
            else:
                raise SanitizerException("Missing required paramater 'user_id'!", "authorize_password", None)
            if "password" in body:
                pass_pattern = re.compile("^[A-Za-z0-9!@#\$%\^\&\*\(\)]+$")
                if not isinstance(body["password"], str) or pass_pattern.match(body["password"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'password'!", "authorize_password", None)
            else:
                raise SanitizerException("Missing required paramater 'password'!", "register_user", None)
            if 'app_id' in body:
                if not isinstance(body["app_id"], int) or body["app_id"] < 1:
                    raise SanitizerException("Invalid value provided for parameter 'app_id'!", "authorize_password", None)
            else:
                raise SanitizerException("Missing required paramater 'app_id'!", "authorize_password", None)
            if 'redirect_url' in body:
                url_pattern = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)")
                if not isinstance(body["redirect_url"], str) or url_pattern.match(body["redirect_url"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'redirect_url'!", "authorize_password", None)
            else:
                raise SanitizerException("Missing required paramater 'redirect_url'!", "authorize_password", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "authorize_password", e)
    
    #validate inputs to /register/application
    def register_application (self, body):
        try:
            if "name" in body:
                name_pattern = re.compile("^[A-Za-z0-9 ]+$")
                if not isinstance(body["name"], str) or name_pattern.match(body["name"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'name'!", "register_application", None)
            else:
                raise SanitizerException("Missing required paramater 'name'!", "register_application", None)
            if "algorithm" in body:
                if not isinstance(body["algorithm"], str) or body["algorithm"] not in ["HS256", "RSA"]:
                    raise SanitizerException("Invalid value provided for parameter 'algorithm'!", "register_application", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "register_application", e)
    
    #validate inputs to /update/application
    def update_application (self, body):
        try:
            if "name" in body:
                name_pattern = re.compile("^[A-Za-z0-9 ]+$")
                if not isinstance(body["name"], str) or name_pattern.match(body["name"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'name'!", "update_application", None)
            if "algorithm" in body:
                if not isinstance(body["algorithm"], str) or body["algorithm"] not in ["HS256", "RSA"]:
                    raise SanitizerException("Invalid value provided for parameter 'algorithm'!", "update_application", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "update_application", e)
    
    #validate inputs to /unregister/application
    def unregister_application (self, body):
        try:
            if "id" in body:
                if not isinstance(body["id"], int) or body["id"] < 1:
                    raise SanitizerException("Invalid value provided for parameter 'id'!", "unregister_application", None)
            else:
                raise SanitizerException("Missing required paramater 'id'!", "unregister_application", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "unregister_application", e)

    #validate inputs to /register/user
    def register_user (self, body):
        try:
            if "name" in body:
                name_pattern = re.compile("^[A-Za-z0-9\.]+$")
                if not isinstance(body["name"], str) or name_pattern.match(body["name"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'name'!", "register_user", None)
            else:
                raise SanitizerException("Missing required paramater 'name'!", "register_user", None)
            if "password" in body:
                pass_pattern = re.compile("^[A-Za-z0-9!@#\$%\^\&\*\(\)]+$")
                if not isinstance(body["password"], str) or pass_pattern.match(body["password"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'password'!", "register_user", None)
            else:
                raise SanitizerException("Missing required paramater 'password'!", "register_user", None)
            if "metadata" in body:
                if not isinstance(body["metadata"], dict):
                    raise SanitizerException("Invalid value provided for parameter 'metadata'!", "register_user", None)
                else:
                    self.validate_user_metadata(body["metadata"])
        except Exception as e:
            raise SanitizerException("Body failed validation!", "register_user", e)
            
    #validate inputs to /retrieve/user
    def retrieve_user (self, body):
        try:
            if "metadata" in body:
                if not isinstance(body["metadata"], dict):
                    raise SanitizerException("Invalid value provided for parameter 'metadata'!", "retrieve_user", None)
                else:
                    self.validate_user_metadata(body["metadata"])
            else:
                raise SanitizerException("Missing required paramater 'metadata'!", "retrieve_user", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "retrieve_user", e)
            
    #validate inputs to /update/username
    def update_username (self, body):
        try:
            if "name" in body:
                name_pattern = re.compile("^[A-Za-z0-9\.]+$")
                if not isinstance(body["name"], str) or name_pattern.match(body["name"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'name'!", "update_username", None)
            else:
                raise SanitizerException("Missing required paramater 'name'!", "update_username", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "update_username", e)
            
    #validate inputs to /update/password
    def update_password (self, body):
        try:
            if "password" in body:
                pass_pattern = re.compile("^[A-Za-z0-9!@#\$%\^\&\*\(\)]+$")
                if not isinstance(body["password"], str) or pass_pattern.match(body["password"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'password'!", "update_password", None)
            else:
                raise SanitizerException("Missing required paramater 'password'!", "update_password", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "update_password", e)
            
    #validate inputs to /update/metadata
    def update_metadata (self, body):
        try:
            if "metadata" in body:
                if not isinstance(body["metadata"], dict):
                    raise SanitizerException("Invalid value provided for parameter 'metadata'!", "update_metadata", None)
                else:
                    self.validate_user_metadata(body["metadata"])
            else:
                raise SanitizerException("Missing required paramater 'metadata'!", "update_metadata", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "update_metadata", e)
            
    #validate inputs to /unregister/user
    def unregister_user (self, body):
        try:
            if "id" in body:
                if not isinstance(body["id"], int) or body["id"] < 1:
                    raise SanitizerException("Invalid value provided for parameter 'id'!", "unregister_user", None)
            else:
                raise SanitizerException("Missing required paramater 'id'!", "unregister_user", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "unregister_user", e)
            
    #validate inputs to /statics/create
    def create_asset (self, body):
        try:
            if "page" in body:
                pg_pattern = re.compile("^[A-Za-z]+$")
                if not isinstance(body["page"], str) or pg_pattern.match(body["page"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'page'!", "create_asset", None)
            else:
                raise SanitizerException("Missing required paramater 'page'!", "create_asset", None)
            if "component" in body:
                comp_pattern = re.compile("^[A-Za-z]+$")
                if not isinstance(body["component"], str) or comp_pattern.match(body["component"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'component'!", "create_asset", None)
            else:
                raise SanitizerException("Missing required paramater 'component'!", "create_asset", None)
            if "key" in body:
                k_pattern = re.compile("^[A-Za-z]+$")
                if not isinstance(body["key"], str) or k_pattern.match(body["key"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'key'!", "create_asset", None)
            else:
                raise SanitizerException("Missing required paramater 'key'!", "create_asset", None)
            if "value" in body:
                if not isinstance(body["value"], str):
                    raise SanitizerException("Invalid value provided for parameter 'value'!", "create_asset", None)
            else:
                raise SanitizerException("Missing required paramater 'value'!", "create_asset", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "create_asset", e)
    
    #validate inputs to /statics/get
    def get_assets (self, body):
        try:
            if "page" in body:
                pg_pattern = re.compile("^[A-Za-z]+$")
                if not isinstance(body["page"], str) or pg_pattern.match(body["page"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'page'!", "get_assets", None)
            else:
                raise SanitizerException("Missing required paramater 'page'!", "get_assets", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "get_assets", e)
    
    #helper method to ensure user metadata is well-formed
    def validate_user_metadata (self, metadata):
        pass
    
    
#custom sanitizer error class
class SanitizerException (Error):
    pass