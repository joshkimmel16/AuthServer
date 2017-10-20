import datetime
import json
import base64
from Helpers import Helpers
from DataLayer import PostGres
from Errors import Error

#initialize globals
h = Helpers()

#class to handle the creation of JWTs
class TokenGenerator:
    
    #pass in necessary internals
    def __init__ (self, algorithm, payload, secret):
        self.algorithm = algorithm
        self.payload = payload
        self.secret = secret
    
    #hash the given string
    def create_hash (self, s):
        try:
            if self.algorithm is "HS256":
                return h.hash_hmac(s, self.secret)
            elif self.algorithm is "RSA":
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


#TODO:
#no restrictions on duplicate user/application names
#no protection against SQL injection for CustomQuery in DataLayer
#figure out how to deal with retrieving forgotten usernames
    #based on metadata??

#class implementing all methods required for Auth web server
class Authorizer:
    
    #MEMBERS
    #data_layer => to connect to DB and execute queries
    #default_alg => default algorithm to use for secrets and encryption when none is specified
    #password_secret => private key to encrypt/decrypt user passwords
    #token_lifetime => number (in milliseconds) representing the length that a jwt should be considered valid
    
    #constructor that captures info for DB connections
    #also capture statics for JWT generation
    def __init__ (self, config):
        self.config = config
        self.data_layer = PostGres()
        self.default_alg = config["default_alg"]
        self.password_secret = config["password_secret"]
        self.token_lifetime = config["token_lifetime"]
        
    #validate that the given user has been registered
    def authorize_username (self, username):
        try:
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            test = self.data_layer.CustomQuery("SELECT id FROM users WHERE username='" + username + "' LIMIT 1;", "get")
            self.data_layer.Disconnect()
            return {"valid": True, "id": test[0][0]} if len(test) > 0 else {"valid": False, "id": None}
        except Exception as e:
            raise AuthorizerException("Error validating the provided username!", "authorize_username", e)
    
    #validate that the given user's password is correct
    def authorize_password (self, user_id, password):
        try:
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            u = self.data_layer.CustomQuery("SELECT * FROM users WHERE id=" + str(user_id) + " LIMIT 1;", "get")
            self.data_layer.Disconnect()
            if len(u) == 0:
                return {"valid": False}
            else:
                user = u[0]
                salt = user[3]
                pwd = user[2]
                hashed = h.hash_hmac((password + salt), self.password_secret)
                return {"valid": True} if hashed == pwd else {"valid": False}
        except Exception as e:
            raise AuthorizerException("Error validating the provided password!", "authorize_password", e)
    
    #decrypt a provided jwt
    def decrypt_token (self, jwt, app_id):
        try:
            #get the secret for the given application
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            s = self.data_layer.CustomQuery('SELECT * FROM applications WHERE id=' + str(app_id) + ' LIMIT 1;', "get")
            self.data_layer.Disconnect()
            if len(s) == 1:
                secret = base64.b64decode(str.encode(s[0][2]))
                alg = s[0][3]
                token = jwt.split('.')
                if len(token) is not 3:
                    raise AuthorizerException("Invalid JWT!", "decrypt_token", None)
                header = token[0]
                payload = token[1]
                signature = token[2]
                
                #compute the signature to ensure that it is valid
                tg = TokenGenerator(alg, h.base64_decode(payload), secret)
                sig = h.base64_encode(tg.create_hash(header + "." + payload))
                
                #if not, throw an error
                if not sig == signature:
                    raise AuthorizerException("The signature is not valid for the provided JWT!", "decrypt_token", None)
                #if so, create dictionary components
                else:
                    result = {}
                    result['header'] = json.loads(h.base64_decode(header))
                    result['payload'] = json.loads(h.base64_decode(payload))
                    return result
            else:
                raise AuthorizerException("Couldn't find the provided application's secret!", "decrypt_token", None)
        except Exception as e:
            raise AuthorizerException("Error decrypting provided JWT!", "decrypt_token", e)
    
    #determine whether the given jwt has expired
    #returns True if the given payload has NOT expired yet
    def check_token_expiration (self, payload):
        try:
            expires = payload['exp']
            return h.compare_datetime_string(expires)
        except Exception as e:
            raise AuthorizerException("Error encountered while validating token expiration!", "check_token_expiration", e)
            
    
    #generate a jwt to be passed to the requester
    def provision_jwt (self, app_id, user_id):
        try:
            #generate payload
            #get app secret and algorithm
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            user = self.data_layer.CustomQuery('SELECT * FROM users WHERE id=' + str(user_id) + " LIMIT 1;", "get")
            app = self.data_layer.CustomQuery('SELECT * FROM applications WHERE id=' + str(app_id) + " LIMIT 1;", "get")
            self.data_layer.Disconnect()
            
            if len(user) == 0 or len(app) == 0:
                raise AuthorizerException("Could not retrieve the provided user and/or application!", "provision_jwt", None)
            else:
                user = user[0]
                app = app[0]
                
            dt = datetime.datetime.now() + datetime.timedelta(milliseconds=self.token_lifetime)
            expires = h.create_datetime_string(str(dt.year), str(dt.month), str(dt.day), str(dt.hour), str(dt.minute), str(dt.second))
            payload = json.dumps({"exp": expires, "userid": user[0], "username": user[1], "usermetadata": json.loads(user[4])})
        
            #use TokenGenerator for remainder of work
            secret = base64.b64decode(str.encode(app[2]))
            tf = TokenGenerator(app[3], payload, secret)
            return tf.generate_token()
        except Exception as e:
            raise AuthorizerException("Error encountered while generating the JWT for the given user!", "provision_jwt", e)
    
    #method to create an application
    #this creates a secret for the given application
    #optional parameter to explicitly determine the hashing algorithm used for jwts
    #returns secret since this must be passed back to the registered app
    def register_application (self, app_name, alg=None):
        if alg is None:
            alg = self.default_alg
        try:
            secret = base64.b64encode(h.generate_secret(alg)).decode()
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            res = self.data_layer.ExecuteFunction('create_application', ['string', 'string', 'string'], [app_name, secret, alg])
            self.data_layer.Disconnect()
            return {"secret": secret, "id": res[0][0]}
        except Exception as e:
            raise AuthorizerException("Could register the application!", "register_application", e)
    
    #method to delete an application
    def unregister_application (self, app_id):
        try:
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            self.data_layer.ExecuteFunction('delete_application', ['int'], [app_id])
            self.data_layer.Disconnect()
            return 'Application Deleted!'
        except Exception as e:
            raise AuthorizerException("Could not unregister the given application!", "unregister_application", e)
    
    #method to update an application
    def update_application (self, app_id, app_name, app_alg):
        try:
            if app_name is not None:
                self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
                self.data_layer.ExecuteFunction('update_appname', ['int', 'string'], [app_id, app_name])
                self.data_layer.Disconnect()
            if app_alg is not None:
                self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
                self.data_layer.ExecuteFunction('update_appalgorithm', ['int', 'string'], [app_id, app_alg])
                self.data_layer.Disconnect()
            return 'Application Updated!'
        except Exception as e:
            raise AuthorizerException("Could not update the given application!", "update_application", e)
    
    #method to create a user in the system
    def register_user (self, username, password, user_metadata):
        try:
            um = json.dumps(user_metadata)
            salt = h.generate_salt()
            hashed = h.hash_hmac((password + salt), self.password_secret)
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            res = self.data_layer.ExecuteFunction('create_user', ['string', 'string', 'string', 'string'], [username, hashed, salt, um])
            self.data_layer.Disconnect()
            return {"id": res[0][0]}
        except Exception as e:
            raise AuthorizerException("Could not register the user!", "register_user", e)
    
    '''
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
            self.data_layer.Connect(config["server"], config["db"], config["user"], config["password"])
            result = self.data_layer.Custom(query) #error here
            self.data_layer.Disconnect()
            if len(result) is 1:
                return result[0]['username']
            else:
                raise ("Could not find the given user using the data provided!")
        except Exception as e:
            raise AuthorizerException("Error encountered while trying to retrieve username!", "retrieve_username", e)
    '''
    
    #method to update the given user's username
    def update_username (self, user_id, new_name):
        try:
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            self.data_layer.ExecuteFunction('update_username', ['int', 'string'], [user_id, new_name])
            self.data_layer.Disconnect()
            return "Username updated!"
        except Exception as e:
            raise AuthorizerException("Could not update the given user's username!", "update_username", e)
    
    #method to update the given user's password
    def update_password (self, user_id, new_password):
        try:
            salt = h.generate_salt()
            hashed = h.hash_hmac((new_password + salt), self.password_secret)
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            self.data_layer.ExecuteFunction('update_password', ['int', 'string', 'string'], [user_id, hashed, salt])
            self.data_layer.Disconnect()
            return "Password updated!"
        except Exception as e:
            raise AuthorizerException("Could not update the given user's password!", "update_password", e)
    
    #method to update the given user's metadata
    def update_metadata (self, user_id, new_metadata):
        try:
            um = json.dumps(new_metadata)
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            self.data_layer.ExecuteFunction('update_usermetadata', ['int', 'string'], [user_id, um])
            self.data_layer.Disconnect()
            return "User metadata updated!"
        except Exception as e:
            raise AuthorizerException("Could not update the given user's metadata!", "update_metadata", e)
    
    #method to delete the given user
    def unregister_user (self, user_id):
        try:
            self.data_layer.Connect(self.config["server"], self.config["db"], self.config["user"], self.config["password"])
            self.data_layer.ExecuteFunction('delete_user', ['int'], [user_id])
            self.data_layer.Disconnect()
            return "User deleted!"
        except Exception as e:
            raise AuthorizerException("Could not unregister the given user!", "unregister_user", e)
    

#custom Authorizer errors
class AuthorizerException (Error):
    pass
