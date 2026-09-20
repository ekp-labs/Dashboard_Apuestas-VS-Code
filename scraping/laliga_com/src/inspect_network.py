from scrapling import StealthyFetcher
def dump(page):
    urls = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource')
            .map(e => e.name)
            .filter(n => n.includes('laliga.com') && (n.includes('api') || n.includes('stats')));
    }
    """)
    print(urls[:30])

f = StealthyFetcher()
f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=5000, page_action=dump)
