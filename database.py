import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('user_name'),
        password=os.getenv('password'),
        database=os.getenv('db'))
    
    print("DB connected")
    return connection 