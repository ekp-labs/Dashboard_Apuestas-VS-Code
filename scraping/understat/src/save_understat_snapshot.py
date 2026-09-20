"""
Save Understat LaLiga 2023-24 HTML snapshot for inspection.
"""
import os
from datetime import datetime
from scrapling import StealthyFetcher

BASE_URL = "https://understat.com/league/La%20liga/2023"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(OUTPUT_DIR, exist_ok=True)

fetcher = StealthyFetcher()
print(f"Fetching {BASE_URL}...")
resp = fetcher.fetch(BASE_URL)
print(f"Status: {resp.status}, HTML length: {len(resp.html_content)}")

timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
filename = f"laliga_2023_snapshot_{timestamp}.html"
path = os.path.join(OUTPUT_DIR, filename)

with open(path, 'w', encoding='utf-8') as f:
    f.write(resp.html_content)

print(f"Saved snapshot to {path}")

# Also save a small excerpt for quick inspection
snippet_path = os.path.join(OUTPUT_DIR, 'laliga_2023_snippet.txt')
with open(snippet_path, 'w', encoding='utf-8') as f:
    f.write(resp.html_content[:20000])

print(f"Saved snippet to {snippet_path}")
