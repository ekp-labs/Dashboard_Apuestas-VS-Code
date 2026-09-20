"""
Extract full player list with scroll automation.
"""
import json, os
from datetime import datetime
from scrapling import StealthyFetcher

LEAGUE = "La%20liga"
SEASON = 2023
URL = f"https://understat.com/league/{LEAGUE}/{SEASON}"

def scroll_action(page):
    # Scroll the second jTable container repeatedly
    # Use evaluate to scroll
    page.evaluate("""
    () => {
        const tables = Array.from(document.querySelectorAll('div.jTable'));
        if (tables.length < 2) return;
        const container = tables[1];
        // Make container scrollable
        for (let i = 0; i < 20; i++) {
            container.scrollTop = container.scrollHeight;
        }
    }
    """)

fetcher = StealthyFetcher()
resp = fetcher.fetch(URL, network_idle=True, wait=5000, wait_selector='div.jTable', wait_selector_state='attached', page_action=scroll_action)

jtables = resp.find_all('div', class_='jTable')
if len(jtables) < 2:
    raise RuntimeError('Player table not found')
player_table = jtables[1]
rows = player_table.find_all('tr')
header = [c.get_all_text(strip=True) for c in rows[0].find_all(['td','th'])]
players = []
for row in rows[1:]:
    cells = row.find_all(['td','th'])
    if not cells:
        continue
    values = [c.get_all_text(strip=True) for c in cells]
    if len(values) < len(header):
        continue
    # Skip totals row with empty player
    if not values[1]:
        continue
    players.append(dict(zip(header, values)))

print(f'Rows extracted: {len(rows)}, players: {len(players)}')
for p in players[:10]:
    print(p['Player'], p['Team'], p['xG'])

out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(out_dir, exist_ok=True)
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
out_path = os.path.join(out_dir, f'laliga_{SEASON}_players_scroll_{ts}.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'season': SEASON, 'league': LEAGUE, 'headers': header, 'players': players}, f, ensure_ascii=False, indent=2)
print('Saved', out_path, 'with', len(players), 'players')
