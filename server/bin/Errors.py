#base class for all errors pertaining to the given application
class Error(Exception):
    def __init__ (self, message, method, inner):
        super(Error, self).__init__(message)
        self.message = self.create_message_recursive(message, inner)
        self.inner = inner
        self.method = method
        self.stack_trace = self.create_stacktrace(method, inner)
        
    def create_stacktrace (self, method, inner):
        result = "at " + method 
        kick = inner
        while (isinstance(kick, Error)):
            result = result + "\nat " + kick.method
            kick = kick.inner
        return result
    
    def create_message_recursive (self, message, inner):
        if inner is not None:
            return message + "\n" + (inner.message if hasattr(inner, 'message') else str(inner))
        else:
            return message

        