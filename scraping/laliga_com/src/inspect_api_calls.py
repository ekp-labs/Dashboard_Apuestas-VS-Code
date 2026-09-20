from scrapling import StealthyFetcher

f = StealthyFetcher()
def action(page):
    urls = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('apim.laliga.com')).slice(0,20);
    }
    """)
    print(urls)
f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=8000, page_action=action)
