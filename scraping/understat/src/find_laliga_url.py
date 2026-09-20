from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://www.fotmob.com/leagues', network_idle=True, wait=5000)
html = r.html_content
# Simple search for la liga
import re
matches = re.findall(r'href="([^"]+)"', html)
laliga_links = [m for m in matches if 'liga' in m.lower() and 'la' in m.lower()]
print(laliga_links[:20])
