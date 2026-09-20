from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    data = page.evaluate("""
    () => {
        const anchors = Array.from(document.querySelectorAll('a'));
        const seasonLinks = anchors.filter(a=>a.href.includes('/stats/season/') && a.href.includes('/laliga')).map(a=>({href:a.href, text:a.innerText.trim()}));
        return seasonLinks;
    }
    """)
    print(json.dumps(data, indent=2))

f.fetch('https://www.fotmob.com/leagues/87/stats/laliga', network_idle=True, wait=10000, page_action=action)
