"""
Extract LaLiga 2023-24 player xG/xA data and save to processed JSON.
"""
import json, os
from datetime import datetime
from scrapling import StealthyFetcher

LEAGUE = "La%20liga"
SEASON = 2023
URL = f"https://understat.com/league/{LEAGUE}/{SEASON}"

def fetch_players():
    fetcher = StealthyFetcher()
    resp = fetcher.fetch(URL, network_idle=True, wait=5000, wait_selector='div.jTable', wait_selector_state='attached')
    jtables = resp.find_all('div', class_='jTable')
    if len(jtables) < 2:
        raise RuntimeError('Player table not found')
    player_table = jtables[1]
    rows = player_table.find_all('tr')
    header_cells = rows[0].find_all(['td','th'])
    headers = [c.get_all_text(strip=True) for c in header_cells]
    players = []
    for row in rows[1:]:
        cells = row.find_all(['td','th'])
        if not cells:
            continue
        values = [c.get_all_text(strip=True) for c in cells]
        if len(values) < len(headers):
            continue
        player = dict(zip(headers, values))
        # Parse xG and xA – they may contain newline with delta
        def parse_metric(v):
            if not v:
                return None, None
            parts = v.split('\n')
            return parts[0], parts[1] if len(parts)>1 else None
        xg_val, xg_delta = parse_metric(player.get('xG',''))
        xa_val, xa_delta = parse_metric(player.get('xA',''))
        player['xG_value'] = xg_val
        player['xG_delta'] = xg_delta
        player['xA_value'] = xa_val
        player['xA_delta'] = xa_delta
        players.append(player)
    return players, headers

if __name__ == '__main__':
    players, headers = fetch_players()
    print(f'Extracted {len(players)} players')
    print('Headers:', headers)
    # Print sample
    for p in players[:5]:
        print(p['Player'], p['Team'], p['xG_value'], p['xA_value'])
    # Save
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'laliga_{SEASON}_players_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'season': SEASON, 'league': LEAGUE, 'headers': headers, 'players': players}, f, ensure_ascii=False, indent=2)
    print('Saved to', out_path)
