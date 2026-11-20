# rag/qdrant_store.py
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from qdrant_client import QdrantClient
from langchain.tools import tool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from dotenv import load_dotenv
from utils.central_logging import setup_logging,get_logger
import os


#setup_logging()
logger = get_logger("search")

_qdrant_client = None
_vector_store = None
_index = None
_query_engine = None
_path = os.path.abspath("./data")

load_dotenv('./.env',override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    logger.info("Openai api key has been set")
else:
    logger.error("No openai api key found")

model_embedding = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5",normalize=True,device="cuda",    embed_batch_size=64)
Settings.llm = OpenAI(model='gpt-3.5-turbo',max_tokens=150)
Settings.embed_model = model_embedding


def get_qdrant_index():

    global _qdrant_client, _vector_store, _index

    if _index is None:
        _qdrant_client = QdrantClient(path=_path)

        _vector_store = QdrantVectorStore(
            client=_qdrant_client,
            collection_name="personal_finance_knowledge"
        )

        _index = VectorStoreIndex.from_vector_store(
            _vector_store,
            embed_model=Settings.embed_model,
            show_progress=False
        )

    return _index


def get_query_engine():
    global _query_engine

    if _query_engine is None:
        index = get_qdrant_index()

        filters = MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="category",
                    value="personal_finance"
                )
            ]
        )

        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=5,
            filters=filters
        )

        _query_engine = RetrieverQueryEngine.from_args(
            retriever=retriever
        )

    return _query_engine

def warmup():
    get_qdrant_index()
    get_query_engine()


@tool
def rag_search_tool(query:str) ->str:
    """Search financial RAG knowledge base for budgeting, debt, and emergency fund advice."""
    query_engine = create_query_engine()
    return str(query_engine.query(query))





#query_engine = create_query_engine()
#print("Query engine created")
#print(f"_qdrant_client: {_qdrant_client}")
#result = query_engine.query("Give me advice to manage my personal finance?")
#print(result)
#if _qdrant_client is not None:
#    _qdrant_client.close()