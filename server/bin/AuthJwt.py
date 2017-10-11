import datetime
import json
from Helpers import Helpers
from DataLayer import DataLayer
from Errors import Error

#initialize globals
h = Helpers()

#class to handle the creation of JWTs
class TokenGenerator:
    
    #pass in necessary internals
    def __init__ (algorithm, payload, secret):
        self.algorithm = algorithm
        self.payload = payload
        self.secret = secret
    
    #hash the given string
    def create_hash (self, s):
        try:
            if self.algorithm is "HS256":
                return h.hash_hmac(s, self.secret)
            else if self.algorithm is "RSA":
                return h.hash_rsa(s, self.secret)
            else:
                return s
        except Exception as e:
            raise TokenGeneratorException("Error encountered while hashing the given string!", "create_hash", e)
    
    #generate a JWT
    def generate_token (self):
        try:
            header = h.base64_encode('{"type": "jwt", "alg": "' + self.algorithm + '"}')
            payload = h.base64_encode(self.payload)
            signature = h.base64_encode(self.create_hash(header + "." + payload))
            return (header + "." + payload + "." + signature)
        except Exception as e:
            raise TokenGeneratorException("Error encountered while creating the JWT!", "generate_token", e)
    

#custom TokenGenerator errors
class TokenGeneratorException (Error):
    pass


#class implementing all methods required for Auth web server
#TODO: add salt to password hashing
class Authorizer:
    
    #MEMBERS
    #data_layer => to connect to DB and execute queries
    #default_alg => default algorithm to use for secrets and encryption when none is specified
    #password_secret => private key to encrypt/decrypt user passwords
    #token_lifetime => number (in milliseconds) representing the length that a jwt should be considered valid
    
    #constructor that captures info for DB connections
    #also capture statics for JWT generation
    def __init__ (config):
        self.data_layer = DataLayer(config["server"], config["db"], config["user"], config["password"])
        self.default_alg = config["default_alg"]
        self.password_secret = config["password_secret"]
        self.token_lifetime = config["token_lifetime"]
        
    #validate that the given user has been registered
    def authorize_username (username):
        try:
            self.data_layer.Connect()
            test = self.data_layer.Select('users', ['username'], ['username'], [username])
            self.data_layer.Disconnect()
            return len(test) is 1
        except Exception as e:
            raise AuthorizerException("Error validating the provided username!", "authorize_username", e)
    
    #validate that the given user's password is correct
    def authorize_password (self, username, password):
        try:
            hashed = h.hash_hmac(password, self.password_secret)
            self.data_layer.Connect()
            test = self.data_layer.Select('users', ['user_metadata'], ['username', 'password'], [username, hashed])
            self.data_layer.Disconnect()
            return (True, test[0]) if len(test) is 1 else (False, None)
        except Exception as e:
            raise AuthorizerException("Error validating the provided password!", "authorize_password", e)
    
    #decrypt a provided jwt
    def decrypt_token (self, jwt, app_name):
        try:
            #get the secret for the given application
            self.data_layer.Connect()
            s = self.data_layer.Select('applications', ['secret', 'algorithm'], ['app_name'], [app_name])
            self.data_layer.Disconnect()
            if len(s) is 1:
                secret = s[0]['secret']
                alg = s[0]['algorithm']
                token = jwt.split('.')
                if len(token) is not 3:
                    raise ("Invalid JWT!")
                header = token[0]
                payload = token[1]
                signature = token[2]
                
                #compute the signature to ensure that it is valid
                tg = TokenGenerator(alg, h.base64_decode(payload), secret)
                sig = h.base64_encode(tg.create_hash(header + "." + payload))
                
                #if not, throw an error
                if not sig == signature:
                    raise ("The signature is not valid for the provided JWT!")
                #if so, create dictionary components
                else:
                    result = {}
                    result['header'] = h.base64_decode(header)
                    result['payload'] = h.base64_decode(payload)
                    return result
            else:
                raise ("Couldn't find the provided application's secret!")
        except Exception as e:
            raise AuthorizerException("Could not parse provided JWT!", "decrypt_token", e)
    
    #determine whether the given jwt has expired
    #returns True if the given payload has NOT expired yet
    def check_token_expiration (self, payload):
        try:
            expires = payload['exp']
            return h.compare_datetime(expires)
        except Exception as e:
            raise AuthorizerException("Error encountered while validating token expiration!", "check_token_expiration", e)
            
    
    #generate a jwt to be passed to the requester
    def provision_jwt (self, app_name, username):
        try:
            #generate payload
            #get app secret and algorithm
            
            self.data_layer.Connect()
            user_info = self.data_layer.Select('users', ['username', 'usermetadata'], ['username'], [username])
            
            app_info = self.data_layer.Select('applications', ['secret', 'algorithm'], ['app_name'], [app_name])
            self.data_layer.Disconnect()
            
            if len(user_info) is not 1 or len(app_info) is not 1:
                raise ("Missing user and/or app info!")
                
            dt = datetime.datetime.now() + datetime.timedelta(milliseconds=self.token_lifetime)
            expires = h.create_datetime_string(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            payload = json.dumps({"exp": h.get_date_string_from_milliseconds(expires), "username": user_info['username'], "usermetadata": json.loads(user_info['usermetadata'])})
        
            #use TokenGenerator for remainder of work
            tf = TokenGenerator(app_info['algorithm'], payload, app_info['secret'])
            return tf.generate_token()
        except Exception as e:
            raise AuthorizerException("Error encountered while generating the JWT for the given user!", "provision_jwt", e)
    
    #method to create an application
    #this creates a secret for the given application
    #optional parameter to explicitly determine the hashing algorithm used for jwts
    #returns secret since this must be passed back to the registered app
    def register_application (self, app_name, alg=self.default_alg):
        try:
            secret = h.generate_secret(alg)
            self.data_layer.Connect()
            self.data_layer.Insert('applications', ['app_name', 'secret', 'algorithm'], [app_name, secret, alg])
            self.data_layer.Disconnect()
            return secret
        except Exception as e:
            raise AuthorizerException("Could register the application!", "register_application", e)
    
    #method to delete an application
    def unregister_application (self, app_name):
        try:
            self.data_layer.Connect()
            self.data_layer.Delete('applications', ['app_name'], [app_name])
            self.data_layer.Disconnect()
            return app_name
        except Exception as e:
            raise AuthorizerException("Could not unregister the given application!", "unregister_application", e)
    
    #method to create a user in the system
    def register_user (self, username, password, user_metadata):
        try:
            um = json.dumps(user_metadata)
            hashed = h.hash_hmac(password, self.password_secret)
            self.data_layer.Connect()
            self.data_layer.Insert('users', ['username', 'password', 'usermetadata'], [username, hashed, um])
            self.data_layer.Disconnect()
            return username
        except Exception as e:
            raise AuthorizerException("Could not register the user!", "register_user", e)
    
    #method to retrieve the given user's username
    #THIS METHOD NEEDS TO BE REFINED
    def retrieve_username (self, metadata_keys, metadata_values):
        def transform_vals (val):
            return ("'" + str(val) + "'")
        
        def transform_keys (key):
            return ('[' + str(key) + ']')
        
        try:
            where_clause = h.list_join(h.list_merge(h.list_map(metadata_keys, transform_keys), h.list_map(metadata_values, transform_vals)), ' AND ')
            query = 'SELECT [username] FROM [users] WHERE ' + where_clause + ';'
            self.data_layer.Connect()
            result = self.data_layer.Custom(query)
            self.data_layer.Disconnect()
            if len(result) is 1:
                return result[0]['username']
            else:
                raise ("Could not find the given user using the data provided!")
        except Exception as e:
            raise AuthorizerException("Error encountered while trying to retrieve username!", "retrieve_username", e)
    
    #method to update the given user's password
    def update_password (self, username, new_password):
        try:
            hashed = h.hash_hmac(new_password, self.password_secret)
            self.data_layer.Connect()
            self.data_layer.Update('users', ['password'], [hashed], ['username'], [username])
            self.data_layer.Disconnect()
            return username
        except Exception as e:
            raise AuthorizerException("Could not update the given user's password!", "update_password", e)
    
    #method to update the given user's metadata
    def update_metadata (self, username, new_metadata):
        try:
            self.data_layer.Connect()
            self.data_layer.Update('users', ['usermetadata'], [new_metadata], ['username'], [username])
            self.data_layer.Disconnect()
            return username
        except Exception as e:
            raise AuthorizerException("Could not update the given user's metadata!", "update_metadata", e)
    
    #method to delete the given user
    def unregister_user (self, username):
        try:
            self.data_layer.Connect()
            self.data_layer.Delete('users', ['username'], [username])
            self.data_layer.Disconnect()
            return username
        except Exception as e:
            raise AuthorizerException("Could not unregister the given user!", "unregister_user", e)
    

#custom Authorizer errors
class AuthorizerException (Error):
    pass
