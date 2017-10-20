from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from DataLayer import PostGres

#constructor
p = PostGres()

#connect
p.Connect("localhost", "auth", "postgres", "admin")

#InsertData and GetData
DataLayer.InsertData("Testing", [("Col1", "Hello"), ("Col2", "World")])
print (DataLayer.GetData("Testing", [], [("Col1", "Hello")]))

#UpdateData and GetData
DataLayer.UpdateData("Testing", [("Col1", "Goodbye")], [("Col2", "World")])
print (DataLayer.GetData("Testing", [], [("Col2", "World")]))

#DeleteData and GetData
DataLayer.DeleteData("Testing", [("Col2", "World")])
print (DataLayer.GetData("Testing", [], [("Col2", "World")]))

#ExecuteFunction
out1 = DataLayer.ExecuteFunction("test_function", ["string", "string"], ["Rage", "Boom"])
print (out1)

#CustomQuery - GET
out2 = DataLayer.CustomQuery("SELECT * FROM Testing;", "get")
print (out2)

#CustomQuery - NON-GET
DataLayer.CustomQuery("DELETE FROM Testing;", "delete")

#Disconnect
DataLayer.Disconnect()