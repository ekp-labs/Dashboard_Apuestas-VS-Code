import json
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\laliga_com\data\processed\players_api_laliga-easports-2023_20260918T011534Z.json'
d = json.load(open(p, encoding='utf-8'))
print(d.get('subscription'))
