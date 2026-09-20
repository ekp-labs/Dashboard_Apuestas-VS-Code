from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=5000, wait_selector='div.jTable', wait_selector_state='attached')

# Find all divs with class jTable
jtables = resp.find_all('div', class_='jTable')
print('jTable divs:', len(jtables))

# Try to extract rows via selector
# Find the second jTable (players)
if len(jtables) >= 2:
    player_table = jtables[1]
    # Find rows
    rows = player_table.find_all('tr')
    print('rows in player table:', len(rows))
    # Print first few rows text
    for i, row in enumerate(rows[:10]):
        cells = row.find_all(['td','th'])
        texts = [c.get_all_text(strip=True) for c in cells]
        print(i, texts)
else:
    print('No player table found')
