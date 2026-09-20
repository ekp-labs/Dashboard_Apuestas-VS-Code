from scrapling import StealthyFetcher
def dump_network(page):
    entries = page.evaluate("""
    () => {
        const res = performance.getEntriesByType('resource')
            .filter(e => e.name.includes('understat.com') && e.name.includes('getLeagueData') || e.name.includes('getTeamsData') || e.name.includes('getPlayersData'))
            .map(e => e.name);
        return res;
    }
    """)
    print('Network entries:', entries)

f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', page_action=dump_network)
