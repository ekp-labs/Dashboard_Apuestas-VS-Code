from scrapling import StealthyFetcher
def dump_network(page):
    entries = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource')
            .map(e => e.name)
            .filter(n => n.includes('understat.com/get'));
    }
    """)
    print('Network entries:', entries)

f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', page_action=dump_network)
