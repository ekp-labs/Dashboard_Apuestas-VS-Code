from scrapling import StealthyFetcher
import json
f = StealthyFetcher()
def action(page):
    links = page.evaluate("""
    () => {
        return Array.from(document.querySelectorAll('a')).map(a=>({href:a.href, text:a.innerText.trim()})).filter(l=>l.text.includes('2023/2024') || l.href.includes('2023')).slice(0,50);
    }
    """)
    print(json.dumps(links, indent=2))
f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
