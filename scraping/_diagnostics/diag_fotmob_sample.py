import json
p = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\fotmob\data\processed\fotmob_laliga_normalized_20260918T021147Z.json'
d = json.load(open(p, encoding='utf-8'))
print(d[0])
print(d[1])
print(d[2])
