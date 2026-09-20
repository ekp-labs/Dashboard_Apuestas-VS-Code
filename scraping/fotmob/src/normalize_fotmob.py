import json, os, re
from datetime import datetime

raw_path = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\fotmob\data\processed\fotmob_laliga_players_raw_20260918T020238Z.txt'
with open(raw_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = [l.strip() for l in text.splitlines() if l.strip()]
# Parse sections by headings
sections = {}
current = None
i = 0
while i < len(lines):
    line = lines[i]
    # detect headings
    if line in ['Top scorer','Assists','Goals + Assists','FotMob rating','Expected goals (xG)','Expected assists (xA)','xG per 90','xA per 90']:
        current = line
        sections[current] = []
        i+=1
        continue
    if current:
        # expect player, team, value pattern
        # accumulate triples
        # simple heuristic: next three lines = player, team, value
        if i+2 < len(lines):
            player = line
            team = lines[i+1]
            value = lines[i+2]
            # try parse value as float/int
            try:
                num = float(value)
            except:
                num = value
            sections[current].append({'player_name':player,'team':team,'value':num})
            i+=3
            continue
    i+=1

# Normalize
normalized = []
for sec, items in sections.items():
    for it in items:
        normalized.append({
            'source':'fotmob',
            'league':'laliga',
            'league_id':87,
            'season':'2026/2027',
            'metric':sec,
            'player_name':it['player_name'],
            'team':it['team'],
            'value':it['value']
        })

out_dir = os.path.dirname(raw_path)
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
out_path = os.path.join(out_dir, f'fotmob_laliga_normalized_{ts}.json')
with open(out_path,'w',encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False, indent=2)
print('Normalized', len(normalized), 'records ->', out_path)
print(normalized[:10])
