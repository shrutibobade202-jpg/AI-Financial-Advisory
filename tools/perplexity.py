import requests
import os 
from dotenv import load_dotenv
from langchain.tools import tool
from utils.central_logging import setup_logging,get_logger
load_dotenv('./.env',override=True)


#setup_logging()

# Create a logger instance
logger = get_logger("perplexity")


# Get our API keys
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

#print(f"Perplexity api key: {perplexity_api_key}")

if perplexity_api_key:
    message = "Perplexity api key has been set"
    logger.info(message)
    print(message)
else:
    message = "Error no perplexity api key found"
    logger.error(message)
    print(message)

PPLX_URL = "https://api.perplexity.ai/chat/completions"
def perplexity_search(
    query: str,
    model: str = "sonar-pro",
    max_tokens: int = 500
) -> str:
    """
    Query Perplexity for live web search with citations.
    """
    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a financial news assistant. "
                    "Search the web and provide a concise summary with key facts. "
                    "Include sources or citations when available."
                )
            },
            {"role": "user", "content": query}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "top_p": 0.9
    }

    resp = requests.post(PPLX_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"]


@tool
def perplexity_live_search(query: str) -> str:
    """
    Use Perplexity for live web search and news.
    Best for:
    - rate cuts/hikes
    - market sentiment
    - current market outlook
    - macro outlook
    - recent volatility drivers
    - verifying breaking developments
    """
    return perplexity_search(query)


