# import mysql.connector

# db_config = {
#     'host': '16.171.235.91',
#     'user': 'root',
#     'password': '5cdswaakye',
#     'database': 'scholarsphere'
# }

# def get_db_connection():
#     return mysql.connector.connect(**db_config)

import pyodbc

# Azure SQL database connection configuration
server = 'final-valid.database.windows.net'
database = 'scholarsphere'
username = 'rootpalal'
password = '5cdsW@@kye'
driver = '{ODBC Driver 17 for SQL Server}'  # Make sure to install this driver

def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        print("Connection established successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None
