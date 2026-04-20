"""
Text chunking utilities.

Large documents must be split into smaller pieces before embedding.
LLM embedding models have token limits.
"""


def chunk_text(text: str, size: int = 800):

    chunks = []

    for i in range(0, len(text), size):

        chunk = text[i:i + size]

        if chunk.strip():

            chunks.append(chunk)

    return chunks