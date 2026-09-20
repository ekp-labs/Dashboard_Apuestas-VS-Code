from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
# Try find text containing known player name? Let's search for 'xG'
texts = r.get_all_text()
if 'xG' in texts:
    print('xG found in text')
# Print first 500 chars of text
print(texts[:500])
print('total text length', len(texts))
