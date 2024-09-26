import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        dbname="wwii_missions_normal",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return connection
