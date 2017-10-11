from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from Helpers import Helpers

h = Helpers()

#base64 encode/decode
encode_string = "This is a test encoding string!"
es = h.base64_encode(encode_string)
ds = h.base64_decode(es)
if not encode_string == ds:
    raise Exception("Test failed! Method: Base64 encode/decode")
    
#hashing and secret generation
password = "Thisisatest123!"
alg = 'HS256'
secret1 = h.generate_secret(alg)
secret2 = h.generate_secret(alg)
hashed1 = h.hash_hmac(password, secret1)
hashed2 = h.hash_hmac("blah", secret1)
hashed3 = h.hash_hmac(password, secret2)
hashed4 = h.hash_hmac(password, secret1)
if hashed1 == hashed2 or hashed1 == hashed3 or not hashed1 == hashed4:
    raise Exception("Test failed! Method: Hash and secret generation")
    
#datetime string parsing



    


