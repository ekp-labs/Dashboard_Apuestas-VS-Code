import json, os, re
from scrapling import StealthyFetcher

SEASON_ID = 21053
LEAGUE_ID = 87
LEAGUE_SLUG = 'laliga'
SEASON_LABEL = '2023-24'

METRICS = [
    'expected_goals',
    'expected_assists',
    'expected_goals_per_90',
    'expected_assists_per_90',
    'goals',
    'assists'
]

METRIC_MAP = {
    'expected_goals': 'Expected goals (xG)',
    'expected_assists': 'Expected assists (xA)',
    'expected_goals_per_90': 'xG per 90',
    'expected_assists_per_90': 'xA per 90',
    'goals': 'Goals',
    'assists': 'Assists'
}

f = StealthyFetcher()

def fetch_inner_text(url):
    extracted = None
    def action(page):
        nonlocal extracted
        extracted = page.evaluate("() => document.body.innerText")
    f.fetch(url, network_idle=True, wait=10000, page_action=action)
    return extracted

records = []
all_players = set()

def parse_lines(lines):
    clean = [l.strip() for l in lines if l.strip()!='']
    i = 0
    found = []
    while i < len(clean):
        if not re.fullmatch(r'\d+', clean[i]):
            i+=1
            continue
        # rank
        i+=1
        if i>=len(clean):
            break
        player = clean[i]
        i+=1
        if i>=len(clean):
            break
        # skip metadata line
        # metadata may be 'Goals: 24' or 'Goals per 90: 1.04' etc.
        i+=1
        if i>=len(clean):
            break
        val_str = clean[i]
        try:
            val = float(val_str)
            # sanity check player name
            if len(player.split())>=2 and not player.lower().startswith('expected'):
                found.append((player, val))
        except:
            pass
        i+=1
    return found

for metric_slug in METRICS:
    metric_name = METRIC_MAP.get(metric_slug, metric_slug)
    url = f'https://www.fotmob.com/leagues/{LEAGUE_ID}/stats/season/{SEASON_ID}/players/{metric_slug}/{LEAGUE_SLUG}'
    print('Fetching', metric_slug)
    text = fetch_inner_text(url)
    if not text:
        print('  No text')
        continue
    lines = text.splitlines()
    parsed = parse_lines(lines)
    for player, val in parsed:
        ui_words = {'Expected goals','Expected assists','LaLiga','All','Striker','Winger','Attacking Midfielder','Midfielder','Fullback','Center-back','Keeper','Goals','Assists'}
        if player in ui_words or player.lower() in ['laLiga','all']:
            continue
        records.append({
            'source':'fotmob',
            'league':'laliga',
            'league_id':LEAGUE_ID,
            'season':SEASON_LABEL,
            'metric':metric_name,
            'player_name':player,
            'value':val
        })
        all_players.add(player)
    print('  Parsed', len(parsed), 'rows')

out_dir = r'f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\fotmob\data\processed'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'fotmob_laliga_2023_24_normalized.json')
with open(out_path,'w',encoding='utf-8') as out_f:
    json.dump(records, out_f, ensure_ascii=False, indent=2)

print('Saved', out_path)
print('Total records', len(records))
print('Distinct players', len(all_players))
from collections import Counter
cnt = Counter(r['metric'] for r in records)
print('Metrics extracted:', dict(cnt))
print('Sample 5:')
for r in records[:5]:
    print(r)
