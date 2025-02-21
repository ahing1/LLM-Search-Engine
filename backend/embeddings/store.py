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

def fetch_articles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, content FROM articles")
    documents = cursor.fetchall()
    conn.close()
    return documents

def store_embedding():
    articles  = fetch_articles()
    for article in articles:
        combined_text = f"{article['title']} {article['content']}"
        embedding = embed_text(combined_text)
        index.upsert([(str(article["id"]), embedding)])
        print(f"✅ Stored embedding for article ID: {article['id']}")

def check_pinecone_index():
    stats = index.describe_index_stats()
    print("Pinecone Index Stats:", stats)

check_pinecone_index()
