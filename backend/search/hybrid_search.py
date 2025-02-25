import mysql.connector
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
import time
import json


load_dotenv()

# Initialize OpenAI & Pinecone
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

# Define index name
index_name = "llm-search"

# Ensure index exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Use 1536 if working with OpenAI embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # Adjust region if needed
        )
    )

# Connect to the index
index = pc.Index(index_name)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DB", "llm_search_db")
    )

# 1️⃣ Keyword Search (BM25 in MySQL)
def keyword_search(query, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # BM25 full-text search
    sql = """
    SELECT id, title, content, MATCH(title, content) AGAINST (%s) AS score
    FROM articles
    WHERE MATCH(title, content) AGAINST (%s IN NATURAL LANGUAGE MODE)
    ORDER BY score DESC
    LIMIT %s;
    """
    cursor.execute(sql, (query, query, limit))
    results = cursor.fetchall()
    conn.close()    
    return results

def embed_text(text):
    """Generates an embedding using OpenAI's new API format"""
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding

# 2️⃣ Semantic Search (Pinecone)
def semantic_search(query, top_k=5):
    query_embedding = embed_text(query)  # Use the fixed embedding function
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [{"id": match["id"], "score": match["score"]} for match in results["matches"]]

cache = {}

# 3️⃣ Hybrid Search (Merging Both)
def hybrid_search(query, top_k=5, bm25_weight=0.7, semantic_weight=0.3):
    
    if query in cache:
        print("Cache hit!")
        return cache[query]

    start_time = time.time()
    
    keyword_results = keyword_search(query, limit=top_k)
    semantic_results = semantic_search(query, top_k=top_k)

   # Convert to dictionary for easier merging
    combined_results = {}

    for result in keyword_results:
        article_id = result["id"]
        combined_results[article_id] = {"id": article_id, "score": result["score"] * bm25_weight}

    for result in semantic_results:
        article_id = result["id"]
        if article_id in combined_results:
            combined_results[article_id]["score"] += result["score"] * semantic_weight
        else:
            combined_results[article_id] = {"id": article_id, "score": result["score"] * semantic_weight}

    # Sort results by score
    sorted_results = sorted(combined_results.values(), key=lambda x: x["score"], reverse=True)
    
    cache[query] = sorted_results[:top_k]
    print(f"⏳ Search took {round(time.time() - start_time, 2)}s")
    
    return sorted_results[:top_k]

# Example search
if __name__ == "__main__":
    query = "How is AI used in healthcare?"
    results = hybrid_search(query)
    for res in results:
        print(f"ID: {res['id']}, Score: {res['score']}")
