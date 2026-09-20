import json, os
from datetime import datetime
from scrapling import StealthyFetcher

URL = "https://www.laliga.com/en-ES/advanced-stats"

def scroll_and_extract(page):
    # scroll multiple times
    page.evaluate("""
    () => {
        window.scrollTo(0, document.body.scrollHeight);
    }
    """)
    # Wait a bit
    import time; time.sleep(1)

f = StealthyFetcher()
# We'll use page_action to both scroll and extract
extracted = None
def action(page):
    global extracted
    # scroll
    for _ in range(10):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
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

if extracted:
    headers = extracted['headers']
    rows = extracted['rows']
    players = []
    for cells in rows:
        if len(cells) < 3:
            continue
        player = {
            'player_name': cells[1],
            'team': cells[2],
        }
        for i,h in enumerate(headers):
            idx = i+1
            if idx < len(cells):
                player[h] = cells[idx]
        players.append(player)
    print('Rows extracted', len(players))
    # save
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'advanced_stats_full_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f_out:
        json.dump({'source':'laliga_com','url':URL,'players':players}, f_out, ensure_ascii=False, indent=2)
    print('Saved', out_path)
