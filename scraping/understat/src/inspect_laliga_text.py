from scrapling import StealthyFetcher
f = StealthyFetcher()
url = "https://www.laliga.com/en-ES/laliga-easports"
resp = f.fetch(url, network_idle=True, wait=5000)
text = resp.html_content
# search for xG
if 'xG' in text:
    print('xG found in HTML')
else:
    print('xG not found')
# search for 'Statistics'
if 'Statistics' in text:
    print('Statistics found')
else:
    print('Statistics not found')
