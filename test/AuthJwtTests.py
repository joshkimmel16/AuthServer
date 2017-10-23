from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from AuthJwt import Authorizer

config = {"server": "localhost","db": "auth","user": "postgres","password": "admin","default_alg": "HS256","password_secret": b'j\x15tMk&\x1ea\xb2\x9e\x95\x97w\x0c\x19!\xa2\xa0KRd\t\xbee\x8e\x95\xdd\x03,[\xa6Xp\xd9\xa8\x04\x15\x96\xb5\x9aD\x9e+\xb8\x03\xc2m\x0b\xddy\x92\x9a\xd2\x82\x15\xa0\xb7t\x85\xe3^\xb5\xb0\x06\xbe\x88\xf8\xe2\\\x8e\x18\xe1\xba\x1b<\xe5\xfd\xe0\x08\xa2\xbd\xae\xb3\xa8%\xc27V\x1a\xd3\x0f\xc9&\x01\x89\x9auQ}C',"token_lifetime": 8640000000}

#constructor
a = Authorizer(config)

#register application
new_app = a.register_application("Test Application")

#update application
up1 = a.update_application(new_app["id"], "New Test Application", "HS256")

#register user
new_user = a.register_user("test.user", "tu", {'key': 'value'})

#retrieve user
r1 = a.retrieve_username({"key": "value"})

#update username
up2 = a.update_username(new_user["id"], "newtest.user")

#update password
up3 = a.update_password(new_user["id"], "newtu")

#update metadata
up4 = a.update_metadata(new_user["id"], {'newkey': 'newvalue'})

#authorize username
au1 = a.authorize_username('test.user') #incorrect userid
au2 = a.authorize_username('newtest.user') #good userid
if au1["valid"] == True or au2["valid"] == False:
    raise Exception("Username authorization test failed!")
    
#authorize password
ap1 = a.authorize_password(new_user["id"] + 1, 'newtu') #bad user id
ap2 = a.authorize_password(new_user["id"], 'tu') #bad password
ap3 = a.authorize_password(new_user["id"], 'newtu') #good password
if ap1["valid"] == True or ap2["valid"] == True or ap3["valid"] == False:
    raise Exception("Password authorization test failed!")
    
#generate JWT
jwt = a.provision_jwt(new_app["id"], new_user["id"])

#decrypt JWT
decrypted = a.decrypt_token(jwt, new_app["id"])

#check expiration
check = a.check_token_expiration(decrypted["payload"])
if check == False:
    raise Exception("Token expiration check failed!")
    
#unregister user
d1 = a.unregister_user(new_user["id"])

#unregister application
d2 = a.unregister_application(new_app["id"])
