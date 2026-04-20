"""
Vector database using PostgreSQL + pgvector.
"""

import psycopg
from config import DATABASE_URL

conn = psycopg.connect(DATABASE_URL)


def insert_document(text, embedding):

    with conn.cursor() as cur:

        cur.execute(
            """
            INSERT INTO documents (text, embedding)
            VALUES (%s, %s)
            """,
            (text, embedding)
        )

    conn.commit()


"""
IMPORTANT:

You must create the table manually.

Run this SQL in PostgreSQL:

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(1024)
);

Adjust vector size if using a different embedding model.
"""