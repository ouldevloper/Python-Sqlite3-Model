# @Author: Abdellah Oulahyane
# @Date:   2021-03-04 04:42:25
# @Last Modified by:   Abdellah Oulahyane
# @Last Modified time: 2021-03-28 03:31:53
#================================================================================#
#                                                                                #
#      Author : Abdellah Oulahyane                                               #  
#      Licensed under the MIT License, Version                                   #
#      this is free software you can redistribute it and/or modify               #
#      Contact   : fb.com/maruki00 | vk.com/maruki00 | github.com/ouldevloper    #
#                                                                                #
#================================================================================#

import sqlite3
import os.path
import inspect
import os
from Model.sys.config import Config
from Model.sys.config import ConfigException
from Model.sys.ModelException import ModelException

class Model(object):
    config__ = Config("ressources","config")
    DBNAME__ = config__["DBNAME"]
    cnx__ = sqlite3.connect(f"{DBNAME__}")
    #print(f"./../{DBNAME__}") if os.path.isfile(f"{DBNAME__}") else print("dir not found")
    cur__ = cnx__.cursor()

    def __init__(self):
        pass
        #Configuration 
        #config__ = Config("ressources","config")
        #DBNAME__ = config__["DBNAME"]
        #self.__DBUSER = self.__config["DBUSER"]
        #self.__DBPASS = self.__config["PASS"]
        #About Connections
        #cnx__   = None
        #cur__   = None


    def __del__(self):
        self.distroy()

    def con(self):
        cnx__ = sqlite3.connect(Model.DBNAME__)

    def cls(self): 
        cnx__.close()

    def distroy(self):
        cnx__=None
        cur__=None

    #Get Database Columns from table Attributes
    def get_attrs(self,obj):
        attributes = inspect.getmembers(obj, lambda a:not(inspect.isroutine(a)))
        keys       = [a for a in attributes if not(a[0].startswith('_')  or a[0].endswith('_'))]
        return dict(keys)
    
    """
        # UPDATE FUNCTION
        #   ---> UPDATE FUNCTION TAKE 3 PARAMETTERS 
        #  1) GET SUBCLASS ATTRIBUTES AS TABLE COLUMNS
        #  2) GENERATE SQL QUERY FOR UPDATE OPERATION
        #  3) EXECUTE SQL COMMAND
        #  4) CHECK FOR ERRORS IF NOT EXISTS COMMIT CHANGES OTHER WISE ROOLBACL
        #  5) RETURN TRUE IF EVERYTHING ARE OK
        # END UPDATE FUNCTION
    """
    def add(self,obj):
        print("DB Name : ",Model.DBNAME__)
        cols = self.get_attrs(obj)
        sql = "INSERT INTO %s ( "%obj.__class__.__name__.lower()  
        sql = sql+",".join(list(cols.keys()))
        sql = sql.strip(',')+" ) VALUES ("
        sql = sql + "?,"*len(list(cols.values()))
        sql = sql.strip(',')+" )"
        try:
            cnx__ = sqlite3.connect(Model.DBNAME__)
            cur__ = cnx__.cursor()
            cur__.execute(sql,tuple(cols.values()))
           
        except sqlite3.Error as err:
            cnx__.rollback()
            raise ModelException(err)
        else:
            cnx__.commit()
        finally:
            cur__.close()
            cnx__.close()
        return True
        
    """
        # UPDATE FUNCTION
        #   ---> UPDATE FUNCTION TAKE 3 PARAMETTERS 
        #  1) GET SUBCLASS ATTRIBUTES AS TABLE COLUMNS
        #  2) GENERATE SQL QUERY FOR UPDATE OPERATION
        #  3) EXECUTE SQL COMMAND
        #  4) CHECK FOR ERRORS IF NOT EXISTS COMMIT CHANGES OTHER WISE ROOLBACL
        #  5) RETURN TRUE IF EVERYTHING ARE OK
        # END UPDATE FUNCTION
    """
    def update(self,obj,data={},ops=[]):
        #this for generate sql
        cols = self.get_attrs(obj)
        #this for passing where close values
        cols2 =  self.get_attrs(obj)
        #remove primary key from columns to generate sql
        #primary = cols.pop(primary)
        sql = "UPDATE %s SET  "%obj.__class__.__name__
        for col in list(cols.keys()):
            sql += " %s=? ,"%str(col) 
        sql = sql.strip(',')
        if len(data)>0:
            fields = list(data.keys())
            sql += " WHERE %s %s ? "%(fields[0],(data[fields[0]] if data[fields[0]]!="" else "="))      
            if len(ops)+1==len(fields):
                for index,op in enumerate(ops):
                    sql += " %s %s %s ? "%(str(op),str(fields[index+1]),(data[fields[index+1]] 
                                                    if data[fields[index+1]]!="" 
                                                    else "="))
            else:
                sql+=" and "
                for field in fields[1:]:
                    sql += "%s=? and "%str(field)
                sql=sql.strip('and ')

        try:
            cnx__ = sqlite3.connect(Model.DBNAME__)
            cur__ = cnx__.cursor()
            cur__.execute(sql, tuple(list(cols.values())+[cols2[key] for key in data if key in data]))
        except sqlite3.Error as err:
            cnx__.rollback()
            raise ModelException(err)
        else:
            cnx__.commit()
        finally:
            cur__.close()
            cnx__.close()
        return True
    
    """
        # UPDATE FUNCTION
        #   ---> UPDATE FUNCTION TAKE 3 PARAMETTERS 
        #  1) GET SUBCLASS ATTRIBUTES AS TABLE COLUMNS
        #  2) GENERATE SQL QUERY FOR UPDATE OPERATION
        #  3) EXECUTE SQL COMMAND
        #  4) CHECK FOR ERRORS IF NOT EXISTS COMMIT CHANGES OTHER WISE ROOLBACL
        #  5) RETURN TRUE IF EVERYTHING ARE OK
        # END UPDATE FUNCTION
    """
    def delete(self,obj,data={},ops=[]):
        #this for generate sql
        cols = self.get_attrs(obj)

        sql = "DELETE FROM %s "%obj.__class__.__name__
        if len(data)>0:
            fields = list(data.keys())
            sql += " WHERE %s %s ? "%(fields[0],(data[fields[0]] if data[fields[0]]!="" else "="))      
            if len(ops)+1==len(fields):
                for index,op in enumerate(ops):
                    sql += " %s %s %s ? "%(str(op),str(fields[index+1]),(data[fields[index+1]] 
                                                    if data[fields[index+1]]!="" 
                                                    else "="))
            else:
                sql+=" and "
                for field in fields[1:]:
                    sql += "%s=? and "%str(field)
                sql=sql.strip('and ')
        
        #print(sql)
        #print(tuple([cols[key] for key in data if key in data]))
        #return
        try:
            cnx__ = sqlite3.connect(Model.DBNAME__)
            cur__ = cnx__.cursor()
            cur__.execute(sql,tuple([cols[key] for key in data if key in data]))
            
            
        except sqlite3.Error as err:
            cnx__.rollback()
            raise ModelException(err)
        else:
            cnx__.commit()
            ret = True
        finally:
            cur__.close()
            cnx__.close()
        return ret
        
    """
        # UPDATE FUNCTION
        #   ---> UPDATE FUNCTION TAKE 3 PARAMETTERS 
        #  1) GET SUBCLASS ATTRIBUTES AS TABLE COLUMNS
        #  2) GENERATE SQL QUERY FOR UPDATE OPERATION
        #  3) EXECUTE SQL COMMAND
        #  4) CHECK FOR ERRORS IF NOT EXISTS COMMIT CHANGES OTHER WISE ROOLBACL
        #  5) RETURN TRUE IF EVERYTHING ARE OK
        # END UPDATE FUNCTION
    """
    def where(self,obj,data={},ops=[]):
        cols = self.get_attrs(obj)
        sql = "SELECT * FROM %s "%obj.__class__.__name__
        if len(data)>0:
            fields = list(data.keys())
            sql += " WHERE %s %s ? "%(fields[0],(data[fields[0]] if data[fields[0]]!="" else "="))      
            if len(ops)+1==len(fields):
                for index,op in enumerate(ops):
                    sql += " %s %s %s ? "%(str(op),str(fields[index+1]),(data[fields[index+1]] 
                                                    if data[fields[index+1]]!="" 
                                                    else "="))
            else:
                sql+=" and "
                for field in fields[1:]:
                    sql += "%s=? and "%str(field)
                sql=sql.strip('and ')
        try:
            cnx__ = sqlite3.connect(Model.DBNAME__)
            cur__ = cnx__.cursor()
            cur__.execute(sql,tuple([cols[key] for key in data if key in data]))
        
        except sqlite3.Error as err:
            cnx__.rollback()
            raise ModelException(err)
        else:
            for row in cur__.fetchall():
                yield obj.__class__(*row)
        finally:
            cur__.close()
            cnx__.close()

        

    """
        # UPDATE FUNCTION
        #   ---> UPDATE FUNCTION TAKE 3 PARAMETTERS 
        #  1) GET SUBCLASS ATTRIBUTES AS TABLE COLUMNS
        #  2) GENERATE SQL QUERY FOR UPDATE OPERATION
        #  3) EXECUTE SQL COMMAND
        #  4) CHECK FOR ERRORS IF NOT EXISTS COMMIT CHANGES OTHER WISE ROOLBACL
        #  5) RETURN TRUE IF EVERYTHING ARE OK
        # END UPDATE FUNCTION
    """
    def like(self,obj,value=""):
        cols = self.get_attrs(obj)
        value = value.replace("'","")
        sql = f"SELECT * FROM {obj.__class__.__name__} where ( %s ) "%(f" like '%{value}%' or ".join(cols)+f" like '%{value}%' " )

        try:
            cnx__ = sqlite3.connect(Model.DBNAME__)
            cur__ = cnx__.cursor()
            cur__.execute(sql)
        except sqlite3.Error as err:
            cnx__.rollback()
            raise ModelException(err)

        else:
            for row in cur__.fetchall():
                yield obj.__class__(*row)
        finally:
            cur__.close()
            cnx__.close()