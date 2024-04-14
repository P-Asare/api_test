import mysql.connector

db_config = {
    'host': '16.171.235.91',
    'user': 'root',
    'password': '5cdswaakye',
    'database': 'scholarsphere'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)