from scrapling import StealthyFetcher
import json
f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/87/stats/laliga/players'
def action(page):
    data = page.evaluate("""
    () => {
        // return page text snippet
        return document.body.innerText.slice(0,1000);
    }
    """)
    print(data)
f.fetch(url, network_idle=True, wait=8000, page_action=action)
