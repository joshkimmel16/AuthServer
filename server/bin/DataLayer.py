'''
Module to easily support connections and basic operations in PostgreSQL
'''

import psycopg2

#script globals
DEBUG = False

#data layer object
class PostGres:
    
    #constructor
    def __init__(self):
        self._connection = None
        self._cursor = None
    
    #connect to a DB
    def Connect(self, host, db, user, password):
        if self._connection is None:
            try:
                self._connection = psycopg2.connect("dbname='"+db+"' user='"+user+"' host='"+host+"' password='"+password+"'")
                self._cursor = self._connection.cursor()
            except Exception as e:
                raise e
        else:
            raise Exception("Please close the current connection before connecting to another database!")
            
        return self
    
    #disconnect from a DB
    def Disconnect(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        return "Connection closed!"
    
    #run a basic SELECT query
    def GetData(self, table, cols, wheres):
        results = None
        if (table != ""):
            
            #generate the query string based on input parameters
            query = "SELECT "
            if len(cols) == 0:
                query += "*"
            else:
                for col in cols:
                    query += (col + ",")
                query = query[:-1]
            query += (" FROM " + table)
            if len(wheres) != 0:
                query += " WHERE "
                for where in wheres:
                    query += (where[0] + "='" + str(where[1]) + "' AND ")
                query = query[:-5]
            query += ";"
            
            #execute the query
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                results = self._cursor.fetchall()
            except Exception as e:
                raise e
                
        else:
            raise Exception("A table must be provided!")
            
        return results
    
    #run a basic INSERT query
    def InsertData(self, table, cols):
        if (table != ""):
            
            #generate the query string based on input parameters
            query = ("INSERT INTO " + table + " (")
            if len(cols) == 0:
                raise Exception("No data to insert was provided!")
            else:
                for col in cols:
                    query += (col[0] + ",")
            query = query[:-1]
            query += (") VALUES (")
            for col in cols:
                query += ("'" + str(col[1]) + "',")
            query = query[:-1]
            query += ");"
            
            #execute the query
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise e
                
        else:
            raise Exception("A table must be provided!")
            
        return self
    
    #run a basic UPDATE query
    def UpdateData(self, table, cols, wheres):
        if (table != ""):
            
            #generate the query string based on input parameters
            query = ("UPDATE " + table + " SET ")
            if len(cols) == 0:
                raise Exception("No data to update was provided!")
            else:
                for col in cols:
                    query += (col[0] + "='" + str(col[1]) + "',")
            query = query[:-1]
            query += " WHERE "
            if len(wheres) == 0:
                raise Exception("This method does not support unfiltered updates!")
            else:
                for where in wheres:
                    query += (where[0] + "='" + str(where[1]) + "' AND ")
            query = query[:-5]
            query += ";"
            
            #execute the query
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise e
                
        else:
            raise Exception("A table must be provided!")
            
        return self
    
    #run a basic DELETE query
    def DeleteData(self, table, wheres):
        if (table != ""):
            
            #generate the query string based on input parameters
            query = ("DELETE FROM " + table)
            if len(wheres) != 0:
                query += " WHERE "
                for where in wheres:
                    query += (where[0] + "='" + str(where[1]) + "' AND ")
            query = query[:-5]
            query += ";"
            
            #execute the query
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise e
                
        else:
            raise Exception("A table must be provided!")
            
        return self
    
    #try finding rows that match "wheres" criteria
    #if found, update them using "cols"
    #if not found, insert "cols"
    def UpsertData(self, table, cols, wheres):
        pass
    
    #execute a defined PSQL function
    def ExecuteFunction(self, func_name, arg_types, arg_vals):
        if (func_name != "" or len(arg_types) != len(arg_vals)):
            
            #generate query string based on input parameters
            results = None
            query = ("SELECT " + func_name + "(")
            for x in range(len(arg_types)):
                query = query + (arg_vals[x] + ",") if arg_types[x] != 'string' else query + ("'" + arg_vals[x] + "',") 
            query = query[:-1]
            query = query + ");"
            
            #execute the query
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                results = self._cursor.fetchall()
            except Exception as e:
                raise e
        else:
            raise Exception("A function name must be provided and the argument types and values must be of the same length!")
            
        return results;
    
    #execute a custom query
    def CustomQuery(self, query, q_type):
        if (query != ""):
            #execute the query
            results = None
            if self._cursor is None:
                raise Exception("Cannot execute a query without a valid connection/cursor!")
            
            try:
                self._cursor.execute(query)
                if q_type == 'get':
                    results = self._cursor.fetchall()
                else:    
                    self._connection.commit()
            except Exception as e:
                raise e
        else:
            raise Exception("A query string must be provided!")
            
        return results
    
    
#method to run unit tests
#PASSED INITIAL TESTING
def debug():
    global DataLayer
    DataLayer = PostGres()
    DataLayer.Connect("localhost", "Test", "postgres", "lemmick")
    DataLayer.InsertData("Testing", [("Col1", "Hello"), ("Col2", "World")])
    print (DataLayer.GetData("Testing", [], [("Col1", "Hello")]))
    DataLayer.UpdateData("Testing", [("Col1", "Goodbye")], [("Col2", "World")])
    print (DataLayer.GetData("Testing", [], [("Col2", "World")]))
    DataLayer.DeleteData("Testing", [("Col2", "World")])
    print (DataLayer.GetData("Testing", [], [("Col2", "World")]))
    
    
#method to execute when running this module directly
def main():
    global DataLayer
    DataLayer = PostGres()
    
#primary execution point for this module
if __name__ == "__main__":
    if DEBUG:
        debug()
    else:
        main()