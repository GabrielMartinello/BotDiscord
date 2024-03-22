from configparser import ConfigParser
import psycopg2
import psycopg2.extras as psql_extras
from typing import Dict, List
import pandas as pd
from dotenv import load_dotenv

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


if __name__ == "__main__":
    # host, database, user, password
    conn_info = load_connection_info("db.ini")

    # Cria a conexao
    create_db(conn_info)

    # Conecta no banco
    connection = psycopg2.connect(**conn_info)
    cursor = connection.cursor()

    # Cria a tabela de pessoas
    pessoa_sql = """
        CREATE TABLE pessoa (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(60) NOT NULL
        )
    """
    create_table(pessoa_sql, connection, cursor)


    # Cria a tabela de presencas
    presenca_sql = """
        CREATE TABLE presenca (
            id SERIAL PRIMARY KEY,
            dataPresenca DATE NOT NULL,
            pessoa_id SERIAL REFERENCES pessoa(id)
        )
    """
    create_table(presenca_sql, connection, cursor)

    # Close all connections to the database
    connection.close()
    cursor.close()