from dao import database
import pandas as pd
import psycopg2
import psycopg2.extras as psql_extras
from typing import Dict, List
import pandas as pd

def create_table_by_command(sql):
     # host, database, user, password
    conn_info = database.load_connection_info("dao/db.ini")

    # Cria a conexao
    database.create_db(conn_info)

    # Conecta no banco
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    database.create_table(sql, connection, cursor)

    connection.close()
    cursor.close()        
    
def insert_dataTable_by_comand(sql, df):
    conn_info = database.load_connection_info("dao/db.ini")
    
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    database.insert_data(sql, connection, cursor, df, 100)

    connection.close()
    cursor.close()    
    
def getData_from_database(query):
    conn_info = database.load_connection_info("dao/db.ini")

    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    col_names = database.get_column_names("pessoa", cursor)
   
    df = pd.DataFrame(columns=col_names)

    dataF = database.get_data_from_db(query, connection, cursor, df, col_names)
    print(dataF)

    connection.close()
    cursor.close()
    
    return dataF
        