from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    # Try to find element containing 2023/2024
    found = page.evaluate("""
    () => {
        const els = Array.from(document.querySelectorAll('a,button,div,span'));
        const el = els.find(e=>e.innerText.includes('2023/2024'));
        if(!el) return {error:'not found'};
        // click
        el.click();
        return {clicked:true, text:el.innerText.trim(), href:el.closest('a')?.href};
    }
    """)
    print(json.dumps(found, indent=2))
    # wait for navigation
    page.wait_for_timeout(3000)
    # get current url
    url = page.url()
    print('URL after click:', url)
f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
