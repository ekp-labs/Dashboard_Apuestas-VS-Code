import json, os
from datetime import datetime
from scrapling import StealthyFetcher

URL = "https://www.laliga.com/en-ES/advanced-stats"

def capture(page):
    return page.evaluate("""
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

f = StealthyFetcher()
data = None
def store(page):
    global data
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

f.fetch(URL, network_idle=True, wait=5000, page_action=store)

if not data:
    print('No data')
else:
    headers = data['headers']
    rows = data['rows']
    # The first cell is empty, so shift
    # headers start at index 1 for NAME
    # We'll create mapping manually
    players = []
    for cells in rows:
        if len(cells) < 2:
            continue
        # cells[0] empty, cells[1] name, cells[2] team
        player = {
            'player_name': cells[1] if len(cells)>1 else '',
            'team': cells[2] if len(cells)>2 else '',
        }
        # map remaining columns
        for i, h in enumerate(headers):
            idx = i+1  # shift for empty first cell
            if idx < len(cells):
                player[h] = cells[idx]
        players.append(player)
    print(f'Extracted {len(players)}')
    for p in players[:5]:
        print(p['player_name'], p['team'])
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'advanced_stats_players_final_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump({'source':'laliga_com','url':URL,'players':players}, f_out, ensure_ascii=False, indent=2)
    print('Saved', out_path)
