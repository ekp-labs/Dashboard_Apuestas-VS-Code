from scrapling import StealthyFetcher
from bs4 import BeautifulSoup
f = StealthyFetcher()
url = "https://www.laliga.com/en-ES/laliga-easports"
resp = f.fetch(url, network_idle=True, wait=3000)
soup = BeautifulSoup(resp.html_content, 'html.parser')
links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'estadistica' in href.lower() or 'statistics' in href.lower() or 'clasificacion' in href.lower():
        links.append(href)
print('found', len(links))
for l in set(links):
    print(l)
