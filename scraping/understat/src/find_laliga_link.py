from scrapling import DynamicFetcher
import re

f = DynamicFetcher()
r = f.fetch('https://understat.com/league/EPL/2023')
html = r.html_content

# Buscar enlaces que contengan LaLiga
links = re.findall(r'href="([^"]+)"', html)
laliga_links = [l for l in links if 'LaLiga' in l or 'laliga' in l.lower()]
print('Enlaces encontrados:', laliga_links[:20])

# También buscar patrones /league/
league_links = [l for l in links if '/league/' in l]
print('League links:', list(set(league_links))[:20])

# Buscar texto LaLiga
if 'LaLiga' in html or 'laliga' in html.lower():
    print('Texto LaLiga presente en HTML')
else:
    print('Texto LaLiga NO presente')

# Mostrar snippet
idx = html.lower().find('laliga')
if idx != -1:
    print(html[idx-100:idx+200])
