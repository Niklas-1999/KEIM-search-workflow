"""
Webpage crawler.

Uses crawl4ai when installed for higher-quality extraction and JavaScript-aware
rendering. Falls back to a simple BeautifulSoup HTML extractor when crawl4ai is
not available.
"""

import httpx
from bs4 import BeautifulSoup
import io
import re

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False

try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    stop_words = {
        "news", "blog", "events", "companies", "research", "hubs", "about",
        "newsletter", "reset", "search", "open menu", "legal", "privacy policy",
        "subscribe to our newsletter", "subscribe", "de"
    }

    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        line = re.sub(r'\s+', ' ', line)
        low = line.lower()

        if low in stop_words:
            continue
        if len(line) < 4:
            continue
        if re.fullmatch(r'[\d\.\-#@\|]+', line):
            continue
        if re.fullmatch(r'[^\w]+', line):
            continue
        if line == lines[-1] if lines else False:
            continue

        lines.append(line)

    paragraphs = []
    paragraph_lines = []
    for line in lines:
        if not line:
            if paragraph_lines:
                paragraphs.append(' '.join(paragraph_lines))
                paragraph_lines = []
            continue

        paragraph_lines.append(line)

    if paragraph_lines:
        paragraphs.append(' '.join(paragraph_lines))

    cleaned = '\n\n'.join(paragraphs)
    cleaned = re.sub(r' {2,}', ' ', cleaned)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()


async def crawl(url: str):
    if CRAWL4AI_AVAILABLE:
        try:
            return await crawl_with_crawl4ai(url)
        except Exception:
            return await crawl_simple(url)
    return await crawl_simple(url)


async def crawl_simple(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyWorkflow/1.0)"
    }
    async with httpx.AsyncClient(timeout=20, headers=headers, verify=False) as client:
        response = await client.get(url)

    content_type = response.headers.get('content-type', '').lower()
    if 'application/pdf' in content_type:
        if PDF_AVAILABLE:
            try:
                pdf_file = io.BytesIO(response.content)
                pdf_reader = PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return clean_text(text)
            except Exception:
                return ""  # Failed to extract PDF text
        else:
            return ""  # PDF library not available

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "button", "input", "svg", "noscript", "iframe", "meta", "link"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return clean_text(text)


async def crawl_with_crawl4ai(url: str):
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
    )
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        flatten_shadow_dom=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)

    text = getattr(result, "markdown", None) or getattr(result, "html", None) or ""
    return clean_text(text)
