import json
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\understat\data\processed\laliga_2023_players_api_20260917T233430Z.json'
d = json.load(open(p, encoding='utf-8'))
players = d.get('players', [])
print(players[0])
