"""
Merge three sources into common season 2023-24 model where possible
"""
import json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entity_resolution import match_player

base = r'f:\- APP DEV -\\2. VS Code\\Dashboard Apuestas\\DashboardApuestas'
out_dir = os.path.join(base, 'data', 'integrated')
os.makedirs(out_dir, exist_ok=True)

# Load Understat 2023
under_path = os.path.join(base, 'scraping/understat/data/processed/laliga_2023_players_api_20260917T233430Z.json')
with open(under_path,'r',encoding='utf-8') as f:
    under_data = json.load(f)

under_players = []
for p in under_data.get('players',[]):
    under_players.append({
        'player_name': p.get('player_name'),
        'team_title': p.get('team_title'),
        'games': int(p.get('games') or 0),
        'time': int(p.get('time') or 0),
        'goals': int(p.get('goals') or 0),
        'assists': int(p.get('assists') or 0),
        'xG': float(p.get('xG') or 0),
        'xA': float(p.get('xA') or 0),
        'shots': int(p.get('shots') or 0),
    })

merged_players = []
laliga_matched = 0
fotmob_matched = 0
unmatched = []

# Load LaLiga.com 2023-24
laliga_path = os.path.join(base, 'scraping/laliga_com/data/processed/advanced_stats_2023_24.json')
laliga_players = []
if os.path.exists(laliga_path):
    with open(laliga_path,'r',encoding='utf-8') as f:
        laliga_data = json.load(f)
    for p in laliga_data.get('players',[]):
        laliga_players.append({
            'player_name': p.get('player_name'),
            'team': p.get('team'),
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
        })

# Load FotMob 2023-24 and aggregate per player
fotmob_path = os.path.join(base, 'scraping/fotmob/data/processed/fotmob_laliga_2023_24_normalized.json')
fotmob_players_agg = []
if os.path.exists(fotmob_path):
    with open(fotmob_path,'r',encoding='utf-8') as f:
        fotmob_data = json.load(f)
    agg = {}
    for rec in fotmob_data:
        key = (rec.get('player_name',''), rec.get('team',''))
        if key not in agg:
            agg[key] = {'player_name': rec.get('player_name'), 'team': rec.get('team'), 'metrics': {}}
        agg[key]['metrics'][rec.get('metric')] = rec.get('value')
    fotmob_players_agg = list(agg.values())

for up in under_players:
    player_entry = {
        'player_name': up.get('player_name'),
        'team': up.get('team_title'),
        'season':'2023-24',
        'league':'LaLiga',
        'understat':{
            'games': up.get('games',0),
            'minutes': up.get('time',0),
            'goals': up.get('goals',0),
            'assists': up.get('assists',0),
            'xG': up.get('xG',0.0),
            'xA': up.get('xA',0.0),
            'shots': up.get('shots',0),
        },
        'laliga_com': None,
        'fotmob': {}
    }

    laliga_match, score = match_player(up, laliga_players, team_a_field='team_title', team_b_field='team', threshold=0.85)
    if laliga_match:
        laliga_matched += 1
        player_entry['laliga_com'] = {
            'm': laliga_match.get('m'),
            'g': laliga_match.get('g'),
            'fgp': laliga_match.get('fgp'),
            's': laliga_match.get('s'),
            'so': laliga_match.get('so'),
            'yc': laliga_match.get('yc'),
            'rc': laliga_match.get('rc'),
            'sy': laliga_match.get('sy'),
            'pf': laliga_match.get('pf'),
            'og': laliga_match.get('og'),
            'gc': laliga_match.get('gc')
        }

    fotmob_match, fscore = match_player(up, fotmob_players_agg, team_a_field='team_title', team_b_field='team', threshold=0.85)
    if fotmob_match:
        fotmob_matched += 1
        player_entry['fotmob'] = fotmob_match.get('metrics', {})

    if not player_entry['laliga_com'] and not player_entry['fotmob']:
        unmatched.append({
            'player_name': up.get('player_name'),
            'team': up.get('team_title'),
            'understat': player_entry['understat']
        })

    merged_players.append(player_entry)

sources_available = ['understat']
sources_missing = []
if laliga_matched > 0:
    sources_available.append('laliga_com')
else:
    sources_missing.append('laliga_com')
if fotmob_matched > 0:
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
        'players':merged_players
    }, f, ensure_ascii=False, indent=2)

unmatched_path = os.path.join(out_dir, f'unmatched_players_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.json')
with open(unmatched_path,'w',encoding='utf-8') as f:
    json.dump({
        'generated_at': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        'total_understat_players': len(under_players),
        'laliga_matches': laliga_matched,
        'fotmob_matches': fotmob_matched,
        'unmatched_players': unmatched
    }, f, ensure_ascii=False, indent=2)

print('Merged common season file:', out_path)
print('Players:', len(merged_players))
print('Understat total:', len(under_players))
print('LaLiga matches:', laliga_matched)
print('FotMob matches:', fotmob_matched)
print('Unmatched players:', len(unmatched))
print('Unmatched file:', unmatched_path)
print('Sources available:', sources_available)
