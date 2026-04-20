"""
Embedding generation using Ollama.
"""

import requests
from config import OLLAMA_URL, EMBED_MODEL


def embed(text: str):

    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )

    return response.json()["embedding"]