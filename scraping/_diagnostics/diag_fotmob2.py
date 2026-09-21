import json, os
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\fotmob\data\processed\fotmob_laliga_normalized_20260918T021147Z.json'
print('exists', os.path.exists(p))
if os.path.exists(p):
    d = json.load(open(p, encoding='utf-8'))
    records = d if isinstance(d, list) else d.get('records', [])
    print('total records', len(records))
    players_set = set((r.get('player_name'), r.get('team')) for r in records)
    print('distinct players', len(players_set))
    teams = set(r.get('team') for r in records if r.get('team'))
    print('teams', len(teams))
    print(sorted(teams)[:50])
