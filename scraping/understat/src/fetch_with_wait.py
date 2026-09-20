from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=5000, wait_selector='div.jTable', wait_selector_state='attached')
print('status', resp.status)
print('html length', len(resp.html_content))
# Check if player names appear
text = resp.get_all_text()
print('text length', len(text))
# Search for known player
sample_players = ['Bellingham', 'Joselu', 'Benzema', 'Rodri']
found = {p: p in text for p in sample_players}
print('sample players found:', found)
# Save snapshot
import os
from datetime import datetime
os.makedirs('data/raw', exist_ok=True)
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
path = f'data/raw/laliga_2023_waited_{ts}.html'
with open(path, 'w', encoding='utf-8') as out:
    out.write(resp.html_content)
print('saved', path)
