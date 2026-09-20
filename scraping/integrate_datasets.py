"""
Integrate three sources into common model
"""
import json, os
from datetime import datetime

base = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas'

# Load Understat 2023
under_path = os.path.join(base, 'scraping/understat/data/processed/laliga_2023_players_api_20260917T233430Z.json')
with open(under_path,'r',encoding='utf-8') as f:
    under_data = json.load(f)

under_players = []
for p in under_data.get('players',[]):
    under_players.append({
        'source':'understat',
        'season':str(under_data.get('season')),
        'league':'La_Liga',
        'player_name':p.get('player_name'),
        'team':p.get('team_title'),
        'position':p.get('position'),
        'games':int(p.get('games') or 0),
        'minutes':int(p.get('time') or 0),
        'goals':int(p.get('goals') or 0),
        'assists':int(p.get('assists') or 0),
        'xG':float(p.get('xG') or 0),
        'xA':float(p.get('xA') or 0),
        'shots':int(p.get('shots') or 0),
        'key_passes':int(p.get('key_passes') or 0),
        'yellow_cards':int(p.get('yellow_cards') or 0),
        'red_cards':int(p.get('red_cards') or 0),
    })

# Load LaLiga.com normalized
laliga_path = os.path.join(base, 'scraping/laliga_com/data/processed/advanced_stats_normalized_20260918T011945Z.json')
with open(laliga_path,'r',encoding='utf-8') as f:
    laliga_data = json.load(f)

laliga_players = []
for p in laliga_data.get('players',[]):
    laliga_players.append({
        'source':'laliga_com',
        'season':p.get('season'),
        'league':'LaLiga',
        'player_name':p.get('player_name').title() if p.get('player_name') else None,
        'team':p.get('team').title() if p.get('team') else None,
        'apps':int(p.get('m') or 0),
        'goals':int(p.get('g') or 0),
        'shots':int(p.get('s') or 0),
        'shots_on_target':int(p.get('so') or 0),
        'yellow_cards':int(p.get('yc') or 0),
        'red_cards':int(p.get('rc') or 0),
        'fouls_committed':int(p.get('pf') or 0),
        'fouls_received':int(p.get('sy') or 0),
    })

# Load FotMob normalized
fotmob_path = os.path.join(base, 'scraping/fotmob/data/processed/fotmob_laliga_normalized_20260918T021147Z.json')
with open(fotmob_path,'r',encoding='utf-8') as f:
    fotmob_records = json.load(f)

# Aggregate FotMob per player by metric
fotmob_agg = {}
for rec in fotmob_records:
    key = (rec['player_name'].lower(), rec['team'].lower())
    if key not in fotmob_agg:
        fotmob_agg[key] = {
            'source':'fotmob',
            'season':rec['season'],
            'league':'laliga',
            'player_name':rec['player_name'],
            'team':rec['team'],
            'metrics':{}
        }
    fotmob_agg[key]['metrics'][rec['metric']] = rec['value']

fotmob_players = list(fotmob_agg.values())

# Combine
combined = {
    'generated_at': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
    'sources':['understat','laliga_com','fotmob'],
    'understat_players':under_players,
    'laliga_com_players':laliga_players,
    'fotmob_players':fotmob_players,
}

out_dir = os.path.join(base, 'data', 'integrated')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, f'dashboard_players_integrated_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.json')
with open(out_path,'w',encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print('Integrated dataset saved to', out_path)
print('Understat players:', len(under_players))
print('LaLiga.com players:', len(laliga_players))
print('FotMob players aggregated:', len(fotmob_players))
