from configparser import ConfigParser
import psycopg2
import psycopg2.extras as psql_extras
from typing import Dict, List
import pandas as pd

def load_connection_info(
    ini_filename: str
) -> Dict[str, str]:
    parser = ConfigParser()
    parser.read(ini_filename)
    # Create a dictionary of the variables stored under the "postgresql" section of the .ini
    conn_info = {param[0]: param[1] for param in parser.items("postgresql")}
    return conn_info


def create_db(
    conn_info: Dict[str, str],
) -> None:
    # Connecta no banco pelo arquivo db.ini
    psql_connection_string = f"user={conn_info['user']} password={conn_info['password']} port={conn_info['port']}"
    conn = psycopg2.connect(psql_connection_string)
    cur = conn.cursor()

    # "CREATE DATABASE" requires automatic commits
    conn.autocommit = True
    sql_query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        cur.close()
    else:
        # Revert autocommit settings
        conn.autocommit = False

def create_table(
    sql_query: str, 
    conn: psycopg2.extensions.connection, 
    cur: psycopg2.extensions.cursor
) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit() 
        
def insert_data(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()        

def get_column_names(
    table: str,
    cur: psycopg2.extensions.cursor
) -> List[str]:
    cursor.execute(
        f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    col_names = [result[0] for result in cursor.fetchall()]
    return col_names
    
def insert_data(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    page_size: int
) -> None:
    data_tuples = [tuple(row.to_numpy()) for index, row in df.iterrows()]

    try:
        psql_extras.execute_values(
            cur, query, data_tuples, page_size=page_size)
        print("Query:", cur.query)

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()
        cur.close()

    else:
        conn.commit()    

def get_column_names(
    table: str,
    cur: psycopg2.extensions.cursor
) -> List[str]:
    cursor.execute(
        f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';")
    col_names = [result[0] for result in cursor.fetchall()]
    return col_names


def get_data_from_db(
    query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
    df: pd.DataFrame,
    col_names: List[str]
) -> pd.DataFrame:
    try:
        cur.execute(query)
        while True:
            # Fetch the next 100 rows
            query_results = cur.fetchmany(100)
            # If an empty list is returned, then we've reached the end of the results
            if query_results == list():
                break

            # Create a list of dictionaries where each dictionary represents a single row
            results_mapped = [
                {col_names[i]: row[i] for i in range(len(col_names))}
                for row in query_results
            ]

            # Append the fetched rows to the DataFrame
            df = df.append(results_mapped, ignore_index=True)

        return df

    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        print("Query:", cur.query)
        conn.rollback()        
        
def create_table_by_command(sql):
     # host, database, user, password
    conn_info = load_connection_info("db.ini")

    # Cria a conexao
    create_db(conn_info)

    # Conecta no banco
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    create_table(sql, connection, cursor)

    connection.close()
    cursor.close()        
    
def insert_dataTable_by_comand(sql, df):
    conn_info = load_connection_info("db.ini")
    
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    insert_data(sql, connection, cursor, df, 100)

    connection.close()
    cursor.close()    
    
def getData_from_database(query):
    conn_info = load_connection_info("db.ini")

    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    col_names = get_column_names("pessoa", cursor)
   
    df = pd.DataFrame(columns=col_names)

    dataF = get_data_from_db(query, connection, cursor, df, col_names)
    print(dataF)

    connection.close()
    cursor.close()
    
    return dataF
        
    
if __name__ == "__main__":
    conn_info = load_connection_info("db.ini")

    # Cria a conexao
    create_db(conn_info)

    # Conecta no banco
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    connection.close()
    cursor.close()