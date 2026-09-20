from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://www.fotmob.com/leagues/54', network_idle=True, wait=3000)
print(r.status)
print('laliga' in r.html_content.lower())
print(r.html_content[:500])
