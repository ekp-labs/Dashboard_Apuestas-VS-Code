from scrapling import StealthyFetcher
import re, json
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content

# Find script tags with JS variables
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
found = []
for s in matches:
    if 'players' in s.lower() and 'xG' in s:
        # Try to find JSON
        # Look for data:
        m = re.search(r'(\{.*?\}|\[.*?\])', s, re.S)
        if m:
            snippet = m.group(0)[:500]
            found.append(snippet)
print('Found scripts with players:', len(found))
for fnd in found[:3]:
    print(fnd[:300])
