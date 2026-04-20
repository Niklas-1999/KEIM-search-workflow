import tarfile
from pathlib import Path

p = Path('downloads/crawl4ai-0.8.6.tar.gz')
with tarfile.open(p, 'r:gz') as tf:
    print('=== __init__.py ===')
    init_member = tf.getmember('crawl4ai-0.8.6/crawl4ai/__init__.py')
    print(tf.extractfile(init_member).read().decode())
    print('\n=== README.md snippet ===')
    readme_member = tf.getmember('crawl4ai-0.8.6/README.md')
    readme = tf.extractfile(readme_member).read().decode().splitlines()
    for i, line in enumerate(readme):
        if 'async with AsyncWebCrawler' in line:
            print('\n'.join(readme[max(0, i-2):min(len(readme), i+10)]))
            break
    print('\n=== CrawlResult definition ===')
    models_member = tf.getmember('crawl4ai-0.8.6/crawl4ai/models.py')
    models = tf.extractfile(models_member).read().decode().splitlines()
    for i, line in enumerate(models):
        if 'class CrawlResult' in line:
            for j in range(i, len(models)):
                if models[j].strip() == '':
                    break
                print(models[j])
            break
    print('\n=== Markdown field search ===')
    for line in models:
        if 'markdown' in line.lower():
            print(line)
