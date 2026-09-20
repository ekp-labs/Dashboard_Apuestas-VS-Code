"""
Extractor piloto de estadísticas de jugadores de LaLiga.com
Fuente: https://www.laliga.com/en-ES/advanced-stats
Métricas disponibles: NAME, TEAM, M, G, %, FGP, %, S, %, SO, %, YC, RC, SY, G, PF, OG, GC
"""
import json, os
from datetime import datetime
from scrapling import StealthyFetcher
from bs4 import BeautifulSoup

URL = "https://www.laliga.com/en-ES/advanced-stats"

def fetch_players():
    fetcher = StealthyFetcher()
    resp = fetcher.fetch(URL, network_idle=True, wait=5000)
    # Save raw snapshot
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    raw_path = os.path.join(raw_dir, f'advanced_stats_{ts}.html')
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(resp.html_content)
    soup = BeautifulSoup(resp.html_content, 'html.parser')
    # The table is rendered dynamically; try to locate rows with player names
    # For pilot, extract visible text blocks
    players = []
    # Simple heuristic: find all <td> with player name pattern
    # We'll collect rows from the table body
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        headers = []
        for i,row in enumerate(rows):
            cells = [c.get_text(strip=True) for c in row.find_all(['th','td'])]
            if i==0:
                headers = cells
            else:
                if len(cells) >= 2 and cells[0] and cells[1]:
                    player = dict(zip(headers, cells))
                    players.append(player)
        if players:
            break
    return players, raw_path

if __name__ == '__main__':
    players, raw_path = fetch_players()
    print(f'Raw saved to {raw_path}')
    print(f'Players extracted: {len(players)}')
    for p in players[:10]:
        print(p)
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'players_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'source': 'laliga_com', 'url': URL, 'players': players}, f, ensure_ascii=False, indent=2)
    print('Saved', out_path)
