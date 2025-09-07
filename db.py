# db.py (PyMySQL)
import pymysql
import os
from config import Config

def get_conn():
    try:
        db_password = os.getenv('DB_PASSWORD', 'Vinay@123')
        return pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),         # your MySQL username
            password=db_password if db_password else None,  # your MySQL password or None
            database=os.getenv('DB_NAME', 'smartcrop'),
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.OperationalError as e:
        raise Exception(f"Database connection failed: {e}. Please check your .env file for correct DB credentials.")

def close_conn(conn):
    if conn:
        conn.close()
