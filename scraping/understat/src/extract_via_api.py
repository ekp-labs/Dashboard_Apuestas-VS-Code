from understatapi import UnderstatClient
import json, os
from datetime import datetime

client = UnderstatClient()
league = client.league('La_Liga')
season = 2023
players = league.get_player_data(season=str(season))
print(f'Players count: {len(players)}')
for p in players[:5]:
    print(p['player_name'], p['team_title'], p.get('xG'), p.get('xA'))

out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(out_dir, exist_ok=True)
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
out_path = os.path.join(out_dir, f'laliga_{season}_players_api_{ts}.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'season': season, 'league': 'La_Liga', 'players': players}, f, ensure_ascii=False, indent=2)
print('Saved', out_path)
