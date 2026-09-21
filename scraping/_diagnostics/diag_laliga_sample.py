import json
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\laliga_com\data\processed\advanced_stats_normalized_20260918T011945Z.json'
d = json.load(open(p, encoding='utf-8'))
players = d.get('players', [])
print(len(players))
print(players[:3])
