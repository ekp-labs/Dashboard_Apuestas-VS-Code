"""
Merge three sources into common season 2023-24 model where possible
"""
import json, os
from datetime import datetime

base = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas'
out_dir = os.path.join(base, 'data', 'integrated')
os.makedirs(out_dir, exist_ok=True)

# Load Understat 2023
under_path = os.path.join(base, 'scraping/understat/data/processed/laliga_2023_players_api_20260917T233430Z.json')
with open(under_path,'r',encoding='utf-8') as f:
    under_data = json.load(f)

players_by_key = {}
for p in under_data.get('players',[]):
    key = (p.get('player_name','').lower().strip(), p.get('team_title','').lower().strip())
    players_by_key[key] = {
        'player_name': p.get('player_name'),
        'team': p.get('team_title'),
        'season':'2023-24',
        'league':'LaLiga',
        'understat':{
            'games':int(p.get('games') or 0),
            'minutes':int(p.get('time') or 0),
            'goals':int(p.get('goals') or 0),
            'assists':int(p.get('assists') or 0),
            'xG':float(p.get('xG') or 0),
            'xA':float(p.get('xA') or 0),
            'shots':int(p.get('shots') or 0),
        },
        'laliga_com': None,
        'fotmob': {}
    }

# Try load LaLiga.com 2023-24
laliga_path = os.path.join(base, 'scraping/laliga_com/data/processed/advanced_stats_2023_24.json')
if os.path.exists(laliga_path):
    with open(laliga_path,'r',encoding='utf-8') as f:
        laliga_data = json.load(f)
    for p in laliga_data.get('players',[]):
        key = (p.get('player_name','').lower().strip(), p.get('team','').lower().strip())
        if key in players_by_key:
            players_by_key[key]['laliga_com'] = {
                'm': p.get('m'),
                'g': p.get('g'),
                'fgp': p.get('fgp'),
                's': p.get('s'),
                'so': p.get('so'),
                'yc': p.get('yc'),
                'rc': p.get('rc'),
                'sy': p.get('sy'),
                'pf': p.get('pf'),
                'og': p.get('og'),
                'gc': p.get('gc')
            }

# Try load FotMob 2023-24
fotmob_path = os.path.join(base, 'scraping/fotmob/data/processed/fotmob_laliga_2023_24_normalized.json')
if os.path.exists(fotmob_path):
    with open(fotmob_path,'r',encoding='utf-8') as f:
        fotmob_data = json.load(f)
    # fotmob_data is a list of metric records
    for rec in fotmob_data:
        key = (rec.get('player_name','').lower().strip(), rec.get('team','').lower().strip())
        if key in players_by_key:
            metric = rec.get('metric')
            value = rec.get('value')
            players_by_key[key]['fotmob'][metric] = value

# Create merged view
merged = list(players_by_key.values())

sources_available = ['understat']
sources_missing = []
if any(p['laliga_com'] for p in merged):
    sources_available.append('laliga_com')
else:
    sources_missing.append('laliga_com')
if any(p['fotmob'] for p in merged if p['fotmob']):
    sources_available.append('fotmob')
else:
    sources_missing.append('fotmob')

out_path = os.path.join(out_dir, f'dashboard_common_2023_24_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.json')
with open(out_path,'w',encoding='utf-8') as f:
    json.dump({
        'season':'2023-24',
        'league':'LaLiga',
        'generated_at':datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'sources_available':sources_available,
        'sources_missing':sources_missing,
        'players':merged
    }, f, ensure_ascii=False, indent=2)

print('Merged common season file:', out_path)
print('Players:', len(merged))
print('Sources available:', sources_available)
