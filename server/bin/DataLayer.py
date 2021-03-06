'''
Module to easily support connections and basic operations in PostgreSQL
'''

#TODO: Pull unit tests out of here and into unit testing directory. Also clean up unit tests.

from Errors import Error
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
                raise DataException("Could not connect using the provided connection string!", "Connect", e)
        else:
            raise DataException("Please close the current connection before connecting to another database!", "Connect", None)
            
        return self
    
    #disconnect from a DB
    def Disconnect(self):
        try:
            if self._cursor is not None:
                self._cursor.close()
                self._cursor = None
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            return "Connection closed!"
        except Exception as e:
            raise DataException("Could not close the active connection!", "Disconnect", e)
    
    #run a basic SELECT query
    def GetData(self, table, cols, wheres):
        results = None
        if (table != ""):
            try:
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
            except Exception as e:
                raise DataException("Error generating query string!", "GetData", e)
            
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "GetData", None)
            
            try:
                self._cursor.execute(query)
                results = self._cursor.fetchall()
            except Exception as e:
                raise DataException("Error executing SELECT statement!", "GetData", e)
                
        else:
            raise DataException("A table must be provided!", "GetData", None)
            
        return results
    
    #run a basic INSERT query
    def InsertData(self, table, cols):
        if (table != ""):
            try:
                #generate the query string based on input parameters
                query = ("INSERT INTO " + table + " (")
                if len(cols) == 0:
                    raise DataException("No data to insert was provided!", "InsertData", None)
                else:
                    for col in cols:
                        query += (col[0] + ",")
                query = query[:-1]
                query += (") VALUES (")
                for col in cols:
                    query += ("'" + str(col[1]) + "',")
                query = query[:-1]
                query += ");"
            except Exception as e:
                DataException("Error generating query string!", "InsertData", e)
            
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "InsertData", None)
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise DataException("Error executing INSERT statement!", "InsertData", e)
                
        else:
            raise DataException("A table must be provided!", "InsertData", None)
            
        return self
    
    #run a basic UPDATE query
    def UpdateData(self, table, cols, wheres):
        if (table != ""):
            try:
                #generate the query string based on input parameters
                query = ("UPDATE " + table + " SET ")
                if len(cols) == 0:
                    raise DataException("No data to update was provided!", "UpdateData", None)
                else:
                    for col in cols:
                        query += (col[0] + "='" + str(col[1]) + "',")
                query = query[:-1]
                query += " WHERE "
                if len(wheres) == 0:
                    raise DataException("This method does not support unfiltered updates!", "UpdateData", None)
                else:
                    for where in wheres:
                        query += (where[0] + "='" + str(where[1]) + "' AND ")
                query = query[:-5]
                query += ";"
            except Exception as e:
                raise DataException("Error generating query string!", "UpdateData", e)
            
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "UpdateData", None)
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise DataException("Error executing UPDATE statement!", "UpdateData", e)
                
        else:
            raise DataException("A table must be provided!", "UpdateData", None)
            
        return self
    
    #run a basic DELETE query
    def DeleteData(self, table, wheres):
        if (table != ""):
            try:
                #generate the query string based on input parameters
                query = ("DELETE FROM " + table)
                if len(wheres) != 0:
                    query += " WHERE "
                    for where in wheres:
                        query += (where[0] + "='" + str(where[1]) + "' AND ")
                query = query[:-5]
                query += ";"
            except Exception as e:
                raise DataException("Error generating query string!", "DeleteData", e)
            
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "DeleteData", None)
            
            try:
                self._cursor.execute(query)
                self._connection.commit()
            except Exception as e:
                raise DataException("Error executing DELETE statement!", "DeleteData", e)
                
        else:
            raise DataException("A table must be provided!", "DeleteData", None)
            
        return self
    
    #try finding rows that match "wheres" criteria
    #if found, update them using "cols"
    #if not found, insert "cols"
    def UpsertData(self, table, cols, wheres):
        pass
    
    #execute a defined PSQL function
    def ExecuteFunction(self, func_name, arg_types, arg_vals):
        results = None
        if (func_name != "" or len(arg_types) != len(arg_vals)):
            try:
                #generate query string based on input parameters
                query = ("SELECT " + func_name + "(")
                for x in range(len(arg_types)):
                    query = query + (str(arg_vals[x]) + ",") if arg_types[x] != 'string' else query + ("'" + arg_vals[x] + "',") 
                query = query[:-1] if len(arg_types) > 0 else query
                query = query + ");"
            except Exception as e:
                raise DataException("Error generating query string!", "ExecuteFunction", e)
            
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "ExecuteFunction", None)
            
            try:
                self._cursor.execute(query)
                results = self._cursor.fetchall()
                self._connection.commit()
            except Exception as e:
                raise DataException("Error executing FUNCTION!", "ExecuteFunction", e)
        else:
            raise Exception("A function name must be provided and the argument types and values must be of the same length!", "ExecuteFunction", None)
            
        return results;
    
    #execute a custom query
    def CustomQuery(self, query, q_type):
        results = None
        if (query != ""):
            #execute the query
            if self._cursor is None:
                raise DataException("Cannot execute a query without a valid connection/cursor!", "CustomQuery", None)
            
            try:
                self._cursor.execute(query)
                if q_type == 'get':
                    results = self._cursor.fetchall()
                else:    
                    self._connection.commit()
            except Exception as e:
                raise DataException("Error executing custom query!", "CustomQuery", e)
        else:
            raise Exception("A query string must be provided!", "CustomQuery", None)
            
        return results
    
#custom Authorizer errors
class DataException (Error):
    pass
    