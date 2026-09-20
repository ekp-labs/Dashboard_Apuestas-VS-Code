from scrapling import StealthyFetcher
import json
f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/87/overview/laliga'
def action(page):
    info = page.evaluate("""
    () => {
        const title = document.title;
        const h1 = document.querySelector('h1')?.innerText || '';
        // try find player stats table
        const links = Array.from(document.querySelectorAll('a')).map(a=>a.href).filter(h=>h.includes('/players')||h.includes('stats')).slice(0,20);
        return {title, h1, links};
    }
    """)
    print(json.dumps(info, indent=2))
f.fetch(url, network_idle=True, wait=5000, page_action=action)
