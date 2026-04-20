import asyncio
from rich import print

from llm import generate_queries
from search import search
from crawler import crawl
from chunking import chunk_text
from embeddings import embed
from vectordb import insert_document
from json_saver import save_json


async def run():

    topic = input("\nResearch topic: ")

    print("\n[green]Generating search queries...[/green]")

    queries = generate_queries(topic)

    urls = []

    for q in queries:

        results = await search(q)

        urls += [r["url"] for r in results[:3]]

    urls = list(set(urls))[:10]

    print(f"\n[yellow]Crawling {len(urls)} pages...[/yellow]")

    for url in urls:

        try:

            text = await crawl(url)

            if not text:
                print(f"[yellow]Skipped {url} (no text extracted)[/yellow]")
                continue

            save_json(url, text, topic)

            chunks = chunk_text(text)

            for chunk in chunks:

                embedding = embed(chunk)

                insert_document(chunk, embedding)

        except Exception as e:

            print(f"[red]Failed to process {url}: {e}[/red]")

    print("\n[bold green]Research data stored successfully![/bold green]")


if __name__ == "__main__":

    asyncio.run(run())