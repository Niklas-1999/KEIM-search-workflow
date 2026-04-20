"""
Global configuration for the research agent.
Modify these values depending on your environment.
"""

# SearXNG search engine
SEARXNG_URL = "http://localhost:8080"

# Ollama API
OLLAMA_URL = "http://localhost:11434"

# Models
EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

# Search settings
TOP_SEARCH_RESULTS = 10
TOP_CRAWL_RESULTS = 5

# Chunking settings
CHUNK_SIZE = 800


# Database connection
# TODO: change credentials for your PostgreSQL installation
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/research"