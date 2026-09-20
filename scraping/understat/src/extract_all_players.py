from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', wait_selector_state='attached')
jtables = resp.find_all('div', class_='jTable')
player_table = jtables[1]
rows = player_table.find_all('tr')
print('total rows', len(rows))
# Print last few
for i,row in enumerate(rows[-5:]):
    cells = row.find_all(['td','th'])
    texts = [c.get_all_text(strip=True) for c in cells]
    print(texts)
