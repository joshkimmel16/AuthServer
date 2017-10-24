import re
from Errors import Error

#TODO:
#implement remaining sanitization methods for active routes
#push sanitization patterns/checks into config?

class Sanitizer:
    
    #constructor
    def __init__ (self):
        self.funcs = {}
        self.funcs["register_application"] = self.register_application
        self.funcs["update_application"] = self.update_application
        self.funcs["unregister_application"] = self.unregister_application
        self.funcs["register_user"] = self.register_user
        self.funcs["retrieve_user"] = self.retrieve_user
        self.funcs["update_username"] = self.update_username
        self.funcs["update_password"] = self.update_password
        self.funcs["update_metadata"] = self.update_metadata
        self.funcs["unregister_user"] = self.unregister_user
    
    #main function to evaluate the legitimacy of inputs to a given route
    def Evaluate (self, route, body):
        if route in self.funcs:
            return self.funcs[route](body)
        else:
            raise SanitizerException("The requested route does not have an implemented validator!", "Evaluate", None)
    
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
    
    #helper method to ensure user metadata is well-formed
    def validate_user_metadata (self, metadata):
        pass
    
#custom sanitizer error class
class SanitizerException (Error):
    pass