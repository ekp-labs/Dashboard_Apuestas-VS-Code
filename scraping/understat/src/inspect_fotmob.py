from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://www.fotmob.com/leagues/la-liga/77"
resp = f.fetch(url, network_idle=True, wait=5000)
text = resp.html_content
print('xG' in text)
# find links
from bs4 import BeautifulSoup
soup = BeautifulSoup(text, 'html.parser')
links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'player' in href.lower() or 'stats' in href.lower():
        links.append(href)
print('links', list(set(links))[:20])
