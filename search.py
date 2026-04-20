"""
Handles searching via SearXNG.
"""

import httpx
from config import SEARXNG_URL


async def search(query: str):
    """
    Perform a search using SearXNG and return a list of results.
    Each result is a dict with 'title', 'url', and 'snippet'.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyWorkflow/1.0)"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{SEARXNG_URL}/search",
                params={
                    "q": query,
                    "format": "json"
                },
                headers=headers,
                timeout=10  # avoid hanging requests
            )
        except httpx.RequestError as e:
            print(f"[ERROR] Request failed: {e}")
            return []

        # Check HTTP status code
        if response.status_code != 200:
            print(f"[ERROR] Received status {response.status_code}")
            print("Response content (first 500 chars):", response.text[:500])
            return []

        # Try parsing JSON safely
        try:
            data = response.json()
        except ValueError:
            print("[ERROR] Failed to parse JSON! Response content (first 500 chars):")
            print(response.text[:500])
            return []

    # Extract results safely
    results = []
    for r in data.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "snippet": r.get("content")
        })

    return results