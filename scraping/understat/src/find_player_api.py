from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', wait_selector_state='attached')
html = resp.html_content
# Look for JSON data in script tags
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
found = False
for i,s in enumerate(scripts):
    if 'players' in s.lower() and ('xG' in s or 'xA' in s):
        print('Script', i, 'contains players')
        print(s[:1000])
        found = True
        break
if not found:
    print('No script with players found')
