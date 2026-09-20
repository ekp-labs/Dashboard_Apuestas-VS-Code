from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    # find links with 2023
    links = page.evaluate("""
    () => {
        const anchors = Array.from(document.querySelectorAll('a'));
        const matches = anchors.filter(a=>a.innerText.includes('2023')).map(a=>({href:a.href, text:a.innerText.trim()}));
        return matches.slice(0,20);
    }
    """)
    print(json.dumps(links, indent=2))
    # try click first
    if links:
        page.evaluate(f"() => {{ window.location.href = '{links[0]['href']}'; }}")
    
f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=5000, page_action=action)
