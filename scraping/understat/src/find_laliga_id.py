from scrapling import StealthyFetcher
f = StealthyFetcher()
found = None
for i in range(1,201):
    try:
        r = f.fetch(f'https://www.fotmob.com/leagues/{i}', network_idle=True, wait=2000)
        if r.status == 200 and ('laliga' in r.html_content.lower() or 'la liga' in r.html_content.lower()):
            found = i
            print('Found La Liga at', i)
            break
    except Exception as e:
        continue
if not found:
    print('Not found')
