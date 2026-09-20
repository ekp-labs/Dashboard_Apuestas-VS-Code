import json, os
from datetime import datetime
from scrapling import StealthyFetcher

URL = "https://www.laliga.com/en-ES/advanced-stats"

f = StealthyFetcher()
extracted = None
def action(page):
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

f.fetch(URL, network_idle=True, wait=5000, page_action=action)

if not extracted:
    print('No table')
else:
    headers = extracted['headers']
    rows = extracted['rows']
    players = []
    for cells in rows:
        if len(cells) < 3:
            continue
        player = {
            'source': 'laliga_com',
            'season': '2026-2027',
            'player_name': cells[1],
            'team': cells[2],
        }
        # map remaining metrics
        for i,h in enumerate(headers):
            idx = i+1
            if idx < len(cells):
                # normalize keys
                key = h.lower().replace(' ','_')
                player[key] = cells[idx]
        players.append(player)
    print(f'Extracted {len(players)} players')
    for p in players[:5]:
        print(p['player_name'], p['team'])
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'advanced_stats_normalized_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump({'url':URL,'players':players}, f_out, ensure_ascii=False, indent=2)
    print('Saved', out_path)
