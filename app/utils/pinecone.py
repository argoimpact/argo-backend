from pinecone import Pinecone

from app.config import app_config

api_key = app_config.pinecone_api_key

if not api_key:
    raise ValueError("API key is not set")

pinecone_client = Pinecone(api_key=api_key)
