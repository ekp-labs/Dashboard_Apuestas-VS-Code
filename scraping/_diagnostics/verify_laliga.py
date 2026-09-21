import json, random, os
base = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas'
laliga_path = os.path.join(base, 'scraping/laliga_com/data/processed/advanced_stats_2023_24.json')
with open(laliga_path, encoding='utf-8') as f:
    laliga_data = json.load(f)
players = laliga_data['players']
print('Total players', len(players))
# random 5
sample = random.sample(players, 5)
for p in sample:
    print(json.dumps(p, ensure_ascii=False))
# specific players
targets = [
    ('Jude Bellingham', 'REAL MADRID CF'),
    ('Antoine Griezmann', 'ATLÉTICO DE MADRID'),
    ('Isco', 'REAL BETIS BALOMPIÉ')
]
for name, team in targets:
    matches = [p for p in players if p['player_name'].lower() == name.lower() and p['team'].upper() == team.upper()]
    if matches:
        print('FOUND', name, team, json.dumps(matches[0], ensure_ascii=False))
    else:
        # try partial
        matches2 = [p for p in players if name.lower() in p['player_name'].lower()]
        print('NOT FOUND exact', name, team, 'candidates', [m['player_name']+'/'+m['team'] for m in matches2[:5]])
# Any player from Cadiz
cadiz_players = [p for p in players if 'CÁDIZ' in p['team'] or 'CADIZ' in p['team']]
print('Cadiz players count', len(cadiz_players))
print('Cadiz sample', cadiz_players[:3])

# Compare format
under_path = os.path.join(base, 'scraping/understat/data/processed/laliga_2023_players_api_20260917T233430Z.json')
with open(under_path, encoding='utf-8') as f:
    under_data = json.load(f)
under_players = under_data['players']
# Find Jude Bellingham in understat
ub = [p for p in under_players if p.get('player_name','').lower() == 'jude bellingham']
if ub:
    print('Understat Jude', ub[0])
# Compare numeric fields
for p in players:
    if p['player_name'].lower() == 'jude bellingham':
        # find under
        u = next((u for u in under_players if u.get('player_name','').lower() == 'jude bellingham'), None)
        if u:
            print('Compare Jude fields')
            print('LaLiga m', p.get('m'), 'Under games', u.get('games'))
            print('LaLiga g', p.get('g'), 'Under goals', u.get('goals'))
            print('LaLiga s', p.get('s'), 'Under shots', u.get('shots'))
            print('LaLiga yc', p.get('yc'), 'Under yellow_cards', u.get('yellow_cards'))
