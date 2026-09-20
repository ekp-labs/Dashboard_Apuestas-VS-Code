from scrapling import StealthyFetcher
import json
f = StealthyFetcher()
def action(page):
    data = page.evaluate("""
    () => {
        const texts = Array.from(document.querySelectorAll('*')).filter(el=>el.innerText.includes('2023/2024')).map(el=>({tag:el.tagName, text:el.innerText.slice(0,100), href:el.closest('a')?.href}));
        return texts.slice(0,20);
    }
    """)
    print(json.dumps(data, indent=2))
f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
