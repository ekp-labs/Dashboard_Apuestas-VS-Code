from scrapling import StealthyFetcher
def dump_page(page):
    data = page.evaluate("""
    () => {
        // Try to find any global variable containing player data
        const keys = Object.keys(window).filter(k => k.toLowerCase().includes('player') || k.toLowerCase().includes('league'));
        return {keys, hasPlayers: !!window.players, sample: Object.values(window).find(v => typeof v === 'object' && Array.isArray(v) && v.length>0 && v[0] && v[0].player)
    }
    """)
    print(data)

f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', page_action=dump_page)
