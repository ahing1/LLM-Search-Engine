from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load environment variables
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

print(f"Connected to Pinecone index: {index_name}")
