from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://www.laliga.com/en-ES/laliga-easports"
resp = f.fetch(url, network_idle=True, wait=5000)
# Try to find links containing 'player'
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.html_content, 'html.parser')
links = []
for a in soup.find_all('a'):
    href = a.get('href','')
    txt = a.get_text(strip=True)
    if 'player' in href.lower() or 'jugador' in href.lower() or 'stat' in href.lower():
        links.append((txt, href))
print('links found:', len(links))
for txt, href in links[:30]:
    print(txt, href)
