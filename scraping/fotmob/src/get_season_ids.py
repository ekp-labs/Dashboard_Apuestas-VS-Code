from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    data = page.evaluate("""
    () => {
        const anchors = Array.from(document.querySelectorAll('a'));
        const seasons = anchors.filter(a=>a.href.includes('/stats/season/') && a.href.includes('/laliga')).map(a=>({href:a.href, text:a.innerText.trim()}));
        return seasons;
    }
    """)
    print(json.dumps(data, indent=2))
f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
