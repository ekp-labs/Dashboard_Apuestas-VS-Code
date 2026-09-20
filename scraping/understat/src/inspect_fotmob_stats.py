from scrapling import StealthyFetcher
f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/La-Liga/77'
def action(page):
    html = page.content()
    print('xG' in html)
    # list links
    links = page.evaluate("""
    () => {
        return Array.from(document.querySelectorAll('a')).map(a=>a.href).filter(h=>h.includes('player')||h.includes('stats')).slice(0,20);
    }
    """)
    print(links)
f.fetch(url, network_idle=True, wait=5000, page_action=action)
