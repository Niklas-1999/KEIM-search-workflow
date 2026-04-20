# Local AI Research Agent

A CLI tool that automatically researches topics using web search, crawling, embeddings, and a vector database.

## Features

- query expansion via LLM
- SearXNG web search
- webpage crawling
- text chunking
- embeddings via Ollama
- vector storage via pgvector
- local-first AI pipeline

---

## Requirements

Python 3.11+

Install:

pip install -r requirements.txt

---

## Install Ollama

https://ollama.com

Install models:

ollama pull llama3
ollama pull mxbai-embed-large

---

## Run SearXNG

You can run via docker:

docker run -p 8080:8080 searxng/searxng

---

## Setup PostgreSQL + pgvector

Create database:

createdb research

Then run:

CREATE EXTENSION vector;

CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  text TEXT,
  embedding VECTOR(1024)
);

---

## Run the agent

python main.py

Enter a research topic when prompted.

Example:

Research topic:
AI regulation Europe