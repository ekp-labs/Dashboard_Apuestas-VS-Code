from scrapling import StealthyFetcher
f = StealthyFetcher()
ids=[55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70]
for i in ids:
    r=f.fetch(f'https://www.fotmob.com/leagues/{i}', network_idle=True, wait=2000)
    print(i, r.status, 'laliga' in r.html_content.lower())
