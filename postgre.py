# -*- coding: utf-8 -*-

import psycopg2
import credentials
class postgre():
    '''This class it is just performed for execute multiple row insert in 
    PostgreSQL'''
    def __init__(self,username=credentials.username,
                password=credentials.password,dbname=credentials.dbname):
        self.username=credentials.username
        self.password=credentials.password
        self.dbname=credentials.dbname
        
    def connect(self):
        try:
            conn = psycopg2.connect(dbname=self.dbname,user=self.username,
                                    password=self.password)
            return conn
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                            .format(str(e))) 
     
    def execute_multiple_inserts(self,data,table,chunksize,conn):
        #we create a cursor 
        try:
           cur = conn.cursor()
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                .format(e))   

        #we convert the data into a tuple of tuples.
        if type(data) is list:
            if len(data)>0:
                if type(data[0]) is list:
                    clean_data=tuple(tuple(i) for i in data)
                elif type(data[0]) is tuple:
                    clean_data=tuple(data)
                else:
                    raise ValueError("formato de datos no adecuado.formato adecuado: "
                        +"Lista de registros,lista de listas,lista de tupla,tupla de " 
                        +"registros,tupla de listas o tupla de tuplas.")
            #Just in case we only want to insert one register per row
            else:
                cleandata=tuple(tuple(i) for i in data)
        elif type(data) is tuple:
            if len(data)>0:
                if type(data[0]) is list:
                    clean_data=tuple(tuple(i) for i in data)
                elif type(data[0]) is tuple:
                    clean_data=data
                else:
                    raise ValueError("formato de datos no adecuado.formato adecuado: "
                        +"Lista de registros,Lista de listas,lista de tupla,tupla de " 
                        +"registros,tupla de listas o tupla de tuplas.")
            else:
                #Just in case we only want to insert one register per row                
                cleandata=tuple(tuple(i) for i in data)
        else:
            raise ValueError("formato de datos no adecuado.formato adecuado: "
               +"Lista de registros,lista de listas,lista de tupla,tupla de registros,"
               +"tupla de listas o tupla de tuplas.")
        
        #we execute the insert statement.

        if chunksize>len(clean_data):
            number_of_records = ','.join(['%s'] * len(clean_data))
            print(number_of_records)
            try:
                insert_statement="INSERT INTO "+str(table)+" VALUES {0}".format(number_of_records)
                cur.execute(insert_statement,clean_data)
            except Exception as e:
                   raise Exception("error durante la inserción  {0}".format(e))
        else:
            while len(clean_data)>0:
                #we split the tuple into smaller tuples.
                insert_data,clean_data=clean_data[:chunksize],clean_data[chunksize:] 
                number_of_records = ','.join(['%s'] * len(insert_data))
                try:
                    insert_statement="INSERT INTO "+str(table)+" VALUES {0}".format(number_of_records)
                    cur.execute(insert_statement,insert_data)
                except Exception as e:
                    raise Exception("error durante la inserción {0}".format(e))
                    break
        #we commit the insert 
        conn.commit()
        #we close the cursor and connection.
        cur.close()
        conn.close()