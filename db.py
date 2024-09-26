import psycopg2
from flask_sqlalchemy import SQLAlchemy

def get_db_connection():
    connection = psycopg2.connect(
        dbname="wwii_missions_normal",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return connection

db = SQLAlchemy()