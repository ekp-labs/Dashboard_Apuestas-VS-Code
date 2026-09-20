"""
Extractor escalado de LaLiga.com Advanced Stats
"""
import json, os
from datetime import datetime
from scrapling import StealthyFetcher

URL = "https://www.laliga.com/en-ES/advanced-stats"

def extract_table(page):
    data = page.evaluate("""
    () => {
        const table = document.querySelector('table');
        if (!table) return null;
        const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim()).filter(h => h);
        const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr => {
            const cells = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim());
            return cells;
        });
        return {headers, rows};
    }
    """)
    return data

f = StealthyFetcher()
resp = f.fetch(URL, network_idle=True, wait=5000, page_action=lambda p: None)
# Need to re-fetch with evaluation
# Use StealthyFetcher with page_action to extract
extracted = None
def capture(page):
    global extracted
    extracted = page.evaluate("""
    () => {
        const table = document.querySelector('table');
        if (!table) return null;
        const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim()).filter(h => h);
        const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr => {
            const cells = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim());
            return cells;
        });
        return {headers, rows};
    }
    """)

resp2 = f.fetch(URL, network_idle=True, wait=5000, page_action=capture)

if not extracted:
    print('No table extracted')
else:
    headers = extracted['headers']
    rows = extracted['rows']
    players = []
    for cells in rows:
        if len(cells) < len(headers):
            continue
        player = dict(zip(headers, cells))
        # Clean name
        players.append(player)
    print(f'Extracted {len(players)} players')
    print('Headers:', headers)
    for p in players[:5]:
        print(p)
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'advanced_stats_players_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump({'source': 'laliga_com', 'url': URL, 'headers': headers, 'players': players}, f_out, ensure_ascii=False, indent=2)
    print('Saved', out_path)
