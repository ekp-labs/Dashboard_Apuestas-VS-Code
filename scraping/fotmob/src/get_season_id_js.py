from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    # wait for page load
    # click season 2023/2024
    clicked = page.evaluate("""
    () => {
        const els = Array.from(document.querySelectorAll('*')).filter(e=>e.innerText && e.innerText.includes('2023/2024'));
        if(els.length>0){ els[0].click(); return true; }
        return false;
    }
    """)
    print('clicked', clicked)
    # give time for SPA navigation
    # try to get current href from window location via evaluate
    url = page.evaluate("() => window.location.href")
    print('url', url)
    # try to find links containing /stats/season/
    links = page.evaluate("""
    () => {
        const a = Array.from(document.querySelectorAll('a')).map(x=>x.href).filter(h=>h.includes('/stats/season/') && h.includes('/laliga'));
        return [...new Set(a)].slice(0,20);
    }
    """)
    print('links', links)

f.fetch('https://www.fotmob.com/leagues/87/stats/laliga', network_idle=True, wait=10000, page_action=action)
