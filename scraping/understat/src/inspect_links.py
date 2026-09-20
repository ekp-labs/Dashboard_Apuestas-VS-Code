from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=5000, wait_selector='div.jTable')
html = resp.html_content
import re
links = re.findall(r'href=\"([^\"]+)\"', html)
print('num links', len(links))
for l in links[:50]:
    print(l)
