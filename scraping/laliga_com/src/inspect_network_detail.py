from scrapling import StealthyFetcher
def dump(page):
    urls = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource')
            .map(e => e.name)
            .filter(n => n.includes('apim.laliga.com'));
    }
    """)
    print(urls)

f = StealthyFetcher()
f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=5000, page_action=dump)
