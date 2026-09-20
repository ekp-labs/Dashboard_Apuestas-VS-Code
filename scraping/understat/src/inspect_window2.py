from scrapling import StealthyFetcher
def dump_page(page):
    keys = page.evaluate("() => Object.keys(window).filter(k => k.toLowerCase().includes('player'))")
    print('player keys:', keys)

f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=8000, wait_selector='div.jTable', page_action=dump_page)
