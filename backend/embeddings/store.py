import pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
from index import index
from backend.utils.db import get_db_connection

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response["data"][0]["embedding"]

def store_embedding(text, doc_id):
    vector = embed_text(text)
    pinecone.upsert([(doc_id, vector)])

def fetch_documents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, content FROM articles")
    documents = cursor.fetchall()
    conn.close()
    return documents

def process_documents():
    documents = fetch_documents()
    for doc in documents:
        combined_text = f"{doc['title']} {doc['content']}"
        store_embedding(doc["id"], combined_text)

def check_pinecone_index():
    stats = index.describe_index_stats()
    print("Pinecone Index Stats:", stats)

check_pinecone_index()
