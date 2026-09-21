from scrapling import StealthyFetcher
URL = "https://www.laliga.com/en-ES/advanced-stats"
f = StealthyFetcher()
def action(page):
    requests = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource').map(r => ({
            name: r.name,
            initiatorType: r.initiatorType,
            type: r.transferSize>0?'xhr':''
        }));
    }
    """)
    print('Resources:', len(requests))
    for r in requests:
        if 'api' in r['name'].lower() or 'stats' in r['name'].lower() or 'player' in r['name'].lower() or 'season' in r['name'].lower():
            print(r['name'])
# also log fetch
f.fetch(URL, network_idle=True, wait=5000, page_action=action)
