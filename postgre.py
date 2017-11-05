# -*- coding: utf-8 -*-

import psycopg2
from pandas import DataFrame


class postgre():

    """This class it is just performed for some specific functionalities in
    PostgreSQL"""

    def __init__(self, username,password, dbname):

        """Create an instance of postgre. Four parameters are needed:
           -username
           -database password
           -database name"""

        self.username = username
        self.password = password
        self.dbname = dbname

    def execute_multiple_inserts(self, data, table, chunksize):

        """This method it perform batch inserts in postgresql.
        We need to insert three arguments:
            -The data we want to insert.
            -The database table name where we are going to store the information
            -The batch size of the insert statement."""

        # we create a connection.
        try:
            conn = psycopg2.connect(dbname=self.dbname, user=self.username,
                                    password=self.password)
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                                 .format(str(e)))

        # we create a cursor
        try:
            cur = conn.cursor()
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                                 .format(e))

            # we convert the data into a tuple of tuples.
        if type(data) is list:
            if len(data) > 0:
                if type(data[0]) is list:
                    clean_data = tuple(tuple(i) for i in data)
                elif type(data[0]) is tuple:
                    clean_data = tuple(data)
                else:
                    raise ValueError("formato de datos no adecuado.formato adecuado: "
                                     + "Lista de registros,lista de listas,lista de tupla,tupla de "
                                     + "registros,tupla de listas o tupla de tuplas.")
            # Just in case we only want to insert one register per row
            else:
                clean_data = tuple(tuple(i) for i in data)
        elif type(data) is tuple:
            if len(data) > 0:
                if type(data[0]) is list:
                    clean_data = tuple(tuple(i) for i in data)
                elif type(data[0]) is tuple:
                    clean_data = data
                else:
                    raise ValueError("formato de datos no adecuado.formato adecuado: "
                                     + "Lista de registros,Lista de listas,lista de tupla,tupla de "
                                     + "registros,tupla de listas o tupla de tuplas.")
            else:
                # Just in case we only want to insert one register per row
                clean_data = tuple(tuple(i) for i in data)
        else:
            raise ValueError("formato de datos no adecuado.formato adecuado: "
                             + "Lista de registros,lista de listas,lista de tupla,tupla de registros,"
                             + "tupla de listas o tupla de tuplas.")

        # we execute the insert statement.

        if chunksize > len(clean_data):
            number_of_records = ','.join(['%s'] * len(clean_data))
            try:
                insert_statement = "INSERT INTO " + str(table) + " VALUES {0}".format(number_of_records)
                cur.execute(insert_statement, clean_data)
            except Exception as e:
                raise Exception("error durante la inserción  {0}".format(e))
        else:
            while len(clean_data) > 0:
                # we split the tuple into smaller tuples.
                insert_data, clean_data = clean_data[:chunksize], clean_data[chunksize:]
                number_of_records = ','.join(['%s'] * len(insert_data))
                try:
                    insert_statement = "INSERT INTO " + str(table) + " VALUES {0}".format(number_of_records)
                    cur.execute(insert_statement, insert_data)
                except Exception as e:
                    raise Exception("error durante la inserción {0}".format(e))
                    break
        # we commit the insert
        conn.commit()
        # we close the cursor and connection.
        cur.close()
        conn.close()

    def postgre_to_dataframe(self, query):
        """This method it is perform to transform an sql query response from postgresql to a pandas DataFrame
            python object."""

        # we create a connection.
        try:
            conn = psycopg2.connect(dbname=self.dbname, user=self.username,
                                    password=self.password)
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                                 .format(str(e)))

        # we create a cursor
        try:
            cur = conn.cursor()
        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                                 .format(e))

        # we execute the query statement.
        try:
            cur.execute(query)
            results = cur.fetchall()
            # we get the information about the columns names.
            columns_names = [i[0] for i in cur.description]

        except psycopg2.Error as e:
            raise psycopg2.Error("Hemos registrado el siguiente error: {0}"
                                 .format(e))

        # we close the cursor and connection.
        cur.close()
        conn.close()

        # we create the data frame.
        return DataFrame.from_records(results, columns=columns_names)
