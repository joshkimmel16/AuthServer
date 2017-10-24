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
                name_pattern = re.compile("^[A-Za-z0-9\.]+$")
                if name_pattern.match(body["name"]) is None:
                    raise SanitizerException("Invalid value provided for parameter 'name'!", "register_application", None)
            else:
                raise SanitizerException("Missing required paramater 'name'!", "register_application", None)
            if "algorithm" in body:
                if body["algorithm"] not in ["HS256", "RSA"]:
                    raise SanitizerException("Invalid value provided for parameter 'algorithm'!", "register_application", None)
        except Exception as e:
            raise SanitizerException("Body failed validation!", "register_application", e)
    
    #validate inputs to /update/application
    def update_application (self, body):
        pass
    
    #validate inputs to /unregister/application
    def unregister_application (self, body):
        pass 
    
#custom sanitizer error class
class SanitizerException (Error):
    pass