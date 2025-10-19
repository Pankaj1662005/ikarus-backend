
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

print(">>> pinecone_client loaded successfully")

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "ikarus-products")  # Your actual index name
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")        # Ensure this matches exactly

# ✅ Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

def get_index():
    # Check if index exists
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,       # As per your index
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV
            )
        )
    return pc.Index(INDEX_NAME)

def upsert_to_pinecone(records):
    index = get_index()
    index.upsert(vectors=records)

def query_pinecone(vector, top_k=5):
    index = get_index()
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)
    return result["matches"]
