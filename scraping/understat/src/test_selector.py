from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
# Find all tables
tables = r.find_all('table')
print('tables found:', len(tables))
for i, t in enumerate(tables[:5]):
    print('--- table', i, '---')
    # Print first rows
    rows = t.find_all('tr')
    print('rows:', len(rows))
    for row in rows[:3]:
        cells = row.find_all(['th','td'])
        texts = [c.text.strip() for c in cells]
        print(texts)
    break
