from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from Statics import Statics

config = {"data": {"auth": {"server": "localhost","db": "auth","user": "postgres","password": "admin"},"statics": {"server": "localhost","db": "statics","user": "postgres","password": "admin"}},"defaults": {"default_alg": "HS256","password_secret": b'j\x15tMk&\x1ea\xb2\x9e\x95\x97w\x0c\x19!\xa2\xa0KRd\t\xbee\x8e\x95\xdd\x03,[\xa6Xp\xd9\xa8\x04\x15\x96\xb5\x9aD\x9e+\xb8\x03\xc2m\x0b\xddy\x92\x9a\xd2\x82\x15\xa0\xb7t\x85\xe3^\xb5\xb0\x06\xbe\x88\xf8\xe2\\\x8e\x18\xe1\xba\x1b<\xe5\xfd\xe0\x08\xa2\xbd\xae\xb3\xa8%\xc27V\x1a\xd3\x0f\xc9&\x01\x89\x9auQ}C',"token_lifetime": 8640000000},"log": {},"server": {"port": 4000}}

#constructor
s = Statics(config)

#create asset
r1 = s.create_asset("testPage", "testComponent", "testKey", "testValue")

#get assets
r2 = s.get_assets("testPage")
print (r2)