from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://www.laliga.com/en-ES/advanced-stats"
resp = f.fetch(url, network_idle=True, wait=5000)
txt = resp.html_content
print('xG' in txt, 'xA' in txt)
# find columns
import re
cols = re.findall(r'<th[^>]*>(.*?)</th>', txt, re.S)
print('columns sample:', cols[:50])
