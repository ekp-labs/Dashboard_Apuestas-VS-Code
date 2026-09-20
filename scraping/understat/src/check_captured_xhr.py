from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
print('captured_xhr:', r.captured_xhr)
if r.captured_xhr:
    for xhr in r.captured_xhr:
        print(xhr.url, xhr.status)
