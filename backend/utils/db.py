import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def save_article(title, url, content, source):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO articles (title, url, content, source) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, url, content, source))
    conn.commit()
    conn.close()