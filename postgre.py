# -*- coding: utf-8 -*-

import psycopg2

class postgre():
    '''This class it is just performed for execute multiple row insert in 
    PostgreSQL'''
    def __init__(self,user,password,host,dbname):
        self.user=user
        self.password=password
        self.host=host
        self.dbname=dbname
        
    def connect(self):
        try:
            conn = psycopg2.connect(dbname=self.dbname,user=self.user,
                                    password=self.password)
            return conn
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error {0}"
                            .format(str(e))) 
     
    def execute_multiple_inserts(data,table,chunksize,conn):
        #we create a cursor 
        try:
           cur = conn.cursor()
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error {0}"
            .format(e))    
        #we convert the data into a tuple of tuples.
        if type(data) is list:
            if type(data[0]) is list:
                clean_data=tuple(tuple(i) for i in data)
            elif type(data[0]) is tuple:
                clean_data=tuple(data)
            else:
                raise ValueError("formato de datos no adecuado.formato adecudo:"
                    +"Lista de listas,lista de tupla,tupla de listas o tupla"+ 
                    +"tuplas")
        elif type(data) is tuple:
            if type(data[0]) is list:
                clean_data=[tuple(i) for i in data]
            elif type(data[0]) is tuple:
                clean_data=data
            else:
                raise ValueError("formato de datos no adecuado.formato adecudo:"
                    +"Lista de listas,lista de tupla,tupla de listas o tupla"+
                   +"de tuplas")
        else:
            raise ValueError("formato de datos no adecuado.formato adecudo:"
               +"Lista de listas,lista de tupla,tupla de listas o tupla de"+
               +"tuplas")
        #we split the tuple into smaller tuples.
        insert_data,clean_data=clean_data[:chunksize],clean_data[chunksize:] 
        #we execute the insert statement.
        while len(clean_data)>0:
            str_insert=str(insert_data)[1:-1]
            try:
                cur.execute("INSERT INTO "+str(table)+
                            " VALUES "+str(str_insert)+";" )
            except Exception as e:
                print("error durante la inserció0".format(e))
        #we commit the insert 
        conn.commit()
        #we close the cursor and connection.
        cur.close()
        conn.close()
a=postgre('pablo','es','muy','tonto')
a.connect()
