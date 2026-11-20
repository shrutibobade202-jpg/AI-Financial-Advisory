from utils.central_logging import setup_logging,get_logger
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
import os
from download import dowload_vectorial_db
from pathlib import Path


setup_logging()

# Create a logger instance
logger = get_logger("qdrantdb")

folder = Path("./data")

if  folder.exists() == False:
    dowload_vectorial_db()
else:
    if  folder.is_dir() == False:
        dowload_vectorial_db()

def get_financial_vector_store(client: QdrantClient, collection_name: str):

    existing_collections = [
        c.name for c in client.get_collections().collections
    ]

    if collection_name not in existing_collections:
        print(f"Collection '{collection_name}' created.")
        logger.info(f"Collection '{collection_name}' created.")

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name
    )


