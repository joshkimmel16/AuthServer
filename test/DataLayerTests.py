from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from DataLayer import PostGres

#constructor
p = PostGres()

#connect
p.Connect("localhost", "unittests", "postgres", "admin")

#InsertData and GetData
p.InsertData("testing", [("col1", "Hello"), ("col2", "World")])
print (p.GetData("testing", [], [("col1", "Hello")]))

#UpdateData and GetData
p.UpdateData("testing", [("col1", "Goodbye")], [("col2", "World")])
print (p.GetData("testing", [], [("col2", "World")]))

#DeleteData and GetData
p.DeleteData("testing", [("col2", "World")])
print (p.GetData("testing", [], [("col2", "World")]))

#ExecuteFunction
out1 = p.ExecuteFunction("test_function", ["string", "string"], ["Rage", "Boom"])
print (out1)

#CustomQuery - GET
out2 = p.CustomQuery("SELECT * FROM testing;", "get")
print (out2)

#CustomQuery - NON-GET
p.CustomQuery("DELETE FROM testing;", "delete")

#Disconnect
p.Disconnect()