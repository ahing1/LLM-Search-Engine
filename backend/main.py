from fastapi import FastAPI
from utils.db import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "LLM-Powered Search Engine Running"}

@app.get("/search")
def search(query: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents WHERE title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results
