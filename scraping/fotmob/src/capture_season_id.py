from scrapling import StealthyFetcher
import json, re

f = StealthyFetcher()
def action(page):
    # Find season selector containing 2023/2024
    # Try clicking any element with that text
    el = page.evaluate("""
    () => {
        const els = Array.from(document.querySelectorAll('*')).filter(e=>e.innerText && e.innerText.includes('2023/2024'));
        return els.length;
    }
    """)
    print('elements found', el)
    # click first
    page.evaluate("""
    () => {
        const els = Array.from(document.querySelectorAll('*')).filter(e=>e.innerText && e.innerText.includes('2023/2024'));
        if(els.length>0) els[0].click();
    }
    """)
    page.wait_for_timeout(4000)
    # collect current URLs from performance entries
    urls = page.evaluate("""
    () => {
        return performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('/stats/season/'));
    }
    """)
    print('resource urls:', urls)
    # get final page url
    print('final url', page.url())

f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
