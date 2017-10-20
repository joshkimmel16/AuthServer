import hmac
import hashlib
import time
import datetime
import base64
import random
from os import urandom
from Errors import Error

#define a set of methods that can be used globally as needed
class Helpers:
    
    #Base64 encode the given string
    #PASSED TESTING
    def base64_encode (self, s):
        try:
            return base64.b64encode(str.encode(s)).decode()
        except Exception as e:
            raise HelperException("Error Base64 encoding the given string!", "base64_encode", e)
        
    #Base64 decode the given string
    #PASSED TESTING
    def base64_decode (self, s):
        try:
            return base64.b64decode(str.encode(s)).decode()
        except Exception as e:
            raise HelperException("Error Base64 decoding the given string!", "base64_decode", e)
    
    #encrypt the given string using the HMACSHA256 algorithm
    #PASSED TESTING
    def hash_hmac (self, s, secret):
        try:
            return hmac.new(secret, msg=str.encode(s), digestmod=hashlib.sha256).hexdigest()
        except Exception as e:
            raise HelperException("Error using HMAC to hash the given string!", "hash_hmac", e)
    
    #encrypt the given string using the RSA algorithm
    #IMPLEMENT LATER!
    def hash_rsa (self, s, secret):
        try:
            return hashlib.sha256(str.encode(s))
        except Exception as e:
            raise HelperException("Error using RSA to hash the given string!", "hash_rsa", e)
    
    #method to extract relevant info from datetime string
    #PASSED TESTING
    def parse_datetime (self, d):
        try:
            temp = d.split('/')
            if len(temp) is not 3:
                raise Exception("Invalid datetime string - Must contain two forward slashes!")
            temp1 = temp[2].split(' ')
            if len(temp1) is not 2:
                raise Exception("Invalid datetime string - Must have a space between the year and time!")
            temp2 = temp1[1].split(':')
            if len(temp2) is not 3:
                raise Exception("Invalid datetime string - Time must contain two colons!")
            
            #(year, month, day, hour, minute, second)
            return ((temp1[0], temp[0], temp[1], temp2[0], temp2[1], temp2[2]))
        except Exception as e:
            raise HelperException("Error parsing the given datetime string!", "parse_datetime", e)
    
    #method to create a properly formed datetime string
    #PASSED TESTING
    def create_datetime_string (self, year, month, day, hour, minute, second):
        try:
            return (month + '/' + day + '/' + year + ' ' + hour + ':' + minute + ':' + second)
        except Exception as e:
            raise HelperException("Error creating the datetime string!", "create_datetime_string", e)
    
    #determine whether given datetime string is after the current time or not
    #returns True if provided date is after current datetime
    #PASSED TESTING
    def compare_datetime_string (self, d):
        try:
            today = datetime.datetime.now()
            dt = self.parse_datetime(d)
            test = datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), int(dt[3]), int(dt[4]), int(dt[5]))
        
            compare = self.convert_date_to_ms(test) - self.convert_date_to_ms(today)
            return compare > 0
        except Exception as e:
            raise HelperException("Error comparing the given datetime string to the current datetime!", "compare_datetime_string", e)
    
    #convert a given datetime object to ms since epoch
    #PASSED TESTING
    def convert_date_to_ms (self, dt):
        try:
            epoch = datetime.datetime.utcfromtimestamp(0)
            return (dt - epoch).total_seconds() * 1000.0
        except Exception as e:
            raise HelperException("Error converting the given datetime to milliseconds since epoch!", "convert_date_to_ms", e)
    
    #generate a secret for the given algorithm
    #PASSED TESTING
    def generate_secret (self, algorithm):
        try:
            if algorithm is 'HS256' or algorithm is 'RSA':
                return bytearray(urandom(100))
            else:
                return bytearray(urandom(100))
        except Exception as e:
            raise HelperException("Error generating an encryption key!", "generate_secret", e)
            
    #generate a salt string for passwords
    def generate_salt (self):
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars=[]
        for i in range(16):
            chars.append(random.choice(ALPHABET))
        return "".join(chars)
    
    #perform array join on an array
    #PASSED TESTING
    def list_join (self, l, delimiter, left_pad='', right_pad=''):
        try:
            result = ''
            for x in range(len(l)):
                if x is len(l) - 1:
                    result = (result + left_pad + l[x] + right_pad)
                else:
                    result = (result + left_pad + l[x] + right_pad + delimiter)
            return result
        except Exception as e:
            raise HelperException("Error generating string from provided list!", "list_join", e)
    
    #merge 2 arrays into 1
    #PASSED TESTING
    def list_merge(self, l1, l2):
        try:
            length1 = len(l1)
            length2 = len(l2)
            max_length = len(l1) if len(l1) >= len(l2) else len(l2)
            min_length = len(l1) if max_length is len(l2) else len(l2)
        
            result = []
            for x in range(min_length):
                result.append(l1[x] + l2[x])
            
            for y in range(min_length, max_length):
                result.append(l1[y] if len(l1) > min_length else l2[y])
            
            return result
        except Exception as e:
            raise HelperException("Error merging the provided lists!", "list_merge", e)
    
    #perform array map on given list
    #PASSED TESTING
    def list_map(self, l, func):
        try:
            result = []
            for x in l:
                result.append(func(x))
            return result
        except Exception as e:
            raise HelperException("Error mapping the provided list using the provided function!", "list_map", e)
            
#custom Authorizer errors
class HelperException (Error):
    pass