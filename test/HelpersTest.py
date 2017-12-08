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
    
#salt generation test
salt = h.generate_salt()
print (salt)
    
#datetime string parsing/creation
year = "2017"
month = "10"
day = "11"
hour = "04"
minute = "32"
second = "23"
date_string = h.create_datetime_string(year, month, day, hour, minute, second)
parsed_date = h.parse_datetime(date_string)
if not (parsed_date[0] == year and parsed_date[1] == month and parsed_date[2] == day and parsed_date[3] == hour and parsed_date[4] == minute and parsed_date[5] == second):
    raise Exception("Test failed! Method: datetime parse/create")
    
#datetime comparison (also implicitly convert to ms)
d1 = h.create_datetime_string("2017", "10", "11", "04", "32", "23")
d2 = h.create_datetime_string("2222", "01", "03", "23", "11", "59")
comp1 = h.compare_datetime_string(d1)
comp2 = h.compare_datetime_string(d2)
if comp1 is True or comp2 is False:
    raise Exception("Test failed! Method: datetime compare")

#list join
l1 = ["a", "b", "c", "d"]
print (h.list_join(l1, ","))
print (h.list_join(l1, ",", "["))
print (h.list_join(l1, ",", "[", "]"))

#list merge
l2 = ["a", "b"]
l3 = ["c", "d", "e"]
l4 = []
print (h.list_merge(l2, l3))
print (h.list_merge(l3, l2))
print (h.list_merge(l3, l4))

#list map
def caps (s):
    return s.upper()
l5 = ["snap", "crackle", "pop"]
print (h.list_map(l5, caps))

#check_url
url1 = "http://test.laserfiche.com?rage=true&boom=false"
url2 = "http://test.laserfiche.com"
if h.check_url(url1) is False or h.check_url(url2) is True:
    raise Exception("Test failed! Method: check_url")
