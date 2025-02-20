import pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response["data"][0]["embedding"]

def store_embedding(text, doc_id):
    vector = embed_text(text)
    pinecone.upsert([(doc_id, vector)])
