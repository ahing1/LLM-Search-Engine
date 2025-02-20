import pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pinecone.init(api_key= os.getenv("PINECONE_API_KEY"), environment="us-east1-gcp")
pinecone.create_index("llm_search", dimension=1536, metric="cosine")
