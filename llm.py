"""
Functions for interacting with Ollama LLM.
"""

import requests
from config import OLLAMA_URL, LLM_MODEL


def generate(prompt: str):

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def generate_queries(topic: str):

    prompt = f"""
Generate 5 different search engine queries for this topic.

Topic: {topic}

Return each query on a new line.
"""

    result = generate(prompt)

    queries = [q.strip("- ").strip() for q in result.split("\n") if q.strip()]

    return queries