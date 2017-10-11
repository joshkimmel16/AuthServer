from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from Errors import Error

e0 = Exception("Base")

#test 1 => no inner exception
e1 = Error("First error", "test_one", None)
print (e1.message)
print (e1.stack_trace)
print (e1.method)

print ("")

#test 2 => inner exception is not of Error class
e2 = Error("Second error", "test_two", e0)
print (e2.message)
print (e2.stack_trace)
print (e2.method)

print ("")

#test 3 => inner exception is of Error class
e3 = Error("Third error", "test_three", e2)
print (e3.message)
print (e3.stack_trace)
print (e3.method)

print ("")

#test 4 => testing recursive functions
e4 = Error("Fourth error", "test_four", e3)
print (e4.message)
print (e4.stack_trace)
print (e4.method)