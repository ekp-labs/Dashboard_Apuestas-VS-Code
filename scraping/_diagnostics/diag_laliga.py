import json, os
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\laliga_com\data\processed\advanced_stats_2023_24.json'
print('exists', os.path.exists(p))
if os.path.exists(p):
    d = json.load(open(p, encoding='utf-8'))
    players = d.get('players', [])
    print('total', len(players))
    teams = set(p2.get('team') for p2 in players if p2.get('team'))
    print('teams', len(teams))
    print(sorted(teams))
